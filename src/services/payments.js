// Recording a card payment: write to our ledger, write back to Xero, send
// the receipt. Also the autopay runner and the "save card" flow.
import { all, audit, get, insert, now, settings, today, update } from '../db.js';
import { config } from '../config.js';
import { gatewayClient, gatewayConnection, xeroClient, xeroConnection } from '../providers/index.js';
import { refreshInvoice } from './sync.js';
import { notifyBusiness, sendAutopayFailed, sendReceipt } from './notifications.js';

const round = (n) => Math.round(n * 100) / 100;

export function savePaymentMethod(business, customer, tok, { makeDefault = true } = {}) {
  if (makeDefault) update('customers', customer.id, { autopay_payment_method_id: null });
  if (makeDefault) all('SELECT id FROM payment_methods WHERE customer_id=?', [customer.id]).forEach((m) => update('payment_methods', m.id, { is_default: 0 }));
  const id = insert('payment_methods', {
    business_id: business.id, customer_id: customer.id, gateway_token: tok.gateway_token,
    card_brand: tok.card_brand, last4: tok.last4, expiry_month: tok.expiry_month, expiry_year: tok.expiry_year,
    cardholder: tok.cardholder || null, is_default: makeDefault ? 1 : 0, created_at: now(),
  });
  audit(business.id, `customer:${customer.id}`, 'payment_method.saved', 'payment_method', id, { brand: tok.card_brand, last4: tok.last4 });
  return get('SELECT * FROM payment_methods WHERE id=?', [id]);
}

// Record a successful (or failed) gateway outcome against an invoice.
export async function recordPayment(business, invoice, outcome, { source, customer, payment_method_id = null, amount }) {
  const amt = round(amount ?? invoice.amount_due);
  const id = insert('payments', {
    business_id: business.id, customer_id: customer?.id || invoice.customer_id, invoice_id: invoice.id,
    payment_method_id, amount: amt, currency: invoice.currency, status: outcome.approved ? 'succeeded' : 'failed',
    source, gateway_txn_id: outcome.txnId || null, gateway_code: outcome.code, gateway_message: outcome.message,
    xero_writeback_status: outcome.approved ? 'pending' : 'n/a', created_at: now(),
  });
  audit(business.id, source, outcome.approved ? 'payment.succeeded' : 'payment.failed', 'payment', id, { invoice: invoice.number, amount: amt, code: outcome.code });
  let payment = get('SELECT * FROM payments WHERE id=?', [id]);
  if (!outcome.approved) return payment;

  // Optimistically mark locally paid; Xero's webhook will confirm.
  update('invoices', invoice.id, {
    amount_paid: round((invoice.amount_paid || 0) + amt), amount_due: round(invoice.amount_due - amt),
    status: round(invoice.amount_due - amt) <= 0 ? 'PAID' : 'AUTHORISED',
    autopay_scheduled_for: null, autopay_next_attempt_at: null, updated_at: now(),
  });

  payment = await writeBackToXero(business, payment);
  const cust = customer || (invoice.customer_id ? get('SELECT * FROM customers WHERE id=?', [invoice.customer_id]) : null);
  if (cust?.email && settings(business).send_receipts) sendReceipt(business, cust, invoice, payment);
  return payment;
}

export async function writeBackToXero(business, payment) {
  const invoice = get('SELECT * FROM invoices WHERE id=?', [payment.invoice_id]);
  try {
    const x = xeroClient(xeroConnection(business.id));
    const r = await x.createPayment({
      invoiceId: invoice.xero_invoice_id, accountCode: settings(business).xero_payment_account_code,
      amount: payment.amount, date: today(), reference: `${config.appName} ${payment.gateway_txn_id || ''}`.trim(),
    });
    update('payments', payment.id, { xero_payment_id: r.PaymentID, xero_writeback_status: 'done', xero_writeback_error: null });
    audit(business.id, 'system', 'xero.payment_recorded', 'payment', payment.id, { xero_payment_id: r.PaymentID });
    await refreshInvoice(business, invoice.xero_invoice_id).catch(() => {});
  } catch (e) {
    update('payments', payment.id, { xero_writeback_status: 'failed', xero_writeback_error: e.message });
    audit(business.id, 'system', 'xero.payment_writeback_failed', 'payment', payment.id, { error: e.message });
    notifyBusiness(business, `Xero write-back failed for ${invoice.number}`, `Payment ${payment.gateway_txn_id} was taken but could not be recorded in Xero: ${e.message}. It will be retried automatically.`);
  }
  return get('SELECT * FROM payments WHERE id=?', [payment.id]);
}

// Retry any payments whose Xero write-back failed.
export async function retryWritebacks() {
  const pending = all("SELECT p.* FROM payments p WHERE p.status='succeeded' AND p.xero_writeback_status='failed' ORDER BY p.id LIMIT 20");
  for (const p of pending) {
    const business = get('SELECT * FROM businesses WHERE id=?', [p.business_id]);
    await writeBackToXero(business, p);
  }
  return pending.length;
}

// Charge one invoice from the customer's saved card (autopay or manual "charge now").
export async function chargeInvoiceWithSavedCard(business, invoice, { source = 'autopay', paymentMethodId } = {}) {
  const customer = get('SELECT * FROM customers WHERE id=?', [invoice.customer_id]);
  const pm = get('SELECT * FROM payment_methods WHERE id=? AND status=?', [paymentMethodId || customer?.autopay_payment_method_id, 'active']);
  if (!customer || !pm) {
    update('invoices', invoice.id, { autopay_scheduled_for: null, autopay_next_attempt_at: null, autopay_last_error: 'No active saved card' });
    return { approved: false, message: 'No active saved card' };
  }
  const gw = gatewayClient(gatewayConnection(business.id));
  const outcome = await gw.chargeToken({ token: pm.gateway_token, amount: invoice.amount_due, currency: invoice.currency, reference: invoice.number });
  const payment = await recordPayment(business, invoice, outcome, { source, customer, payment_method_id: pm.id });

  if (!outcome.approved) {
    const attempts = (invoice.autopay_attempts || 0) + 1;
    const willRetry = source === 'autopay' && attempts < config.autopay.maxAttempts;
    const next = new Date(Date.now() + config.autopay.retryDays * 864e5).toISOString();
    update('invoices', invoice.id, {
      autopay_attempts: attempts, autopay_last_error: `${outcome.code} ${outcome.message}`,
      autopay_next_attempt_at: willRetry ? next : null,
    });
    if (customer.email) sendAutopayFailed(business, customer, invoice, outcome.message, willRetry);
    if (!willRetry) notifyBusiness(business, `Autopay stopped for ${invoice.number}`, `${customer.name}'s card was declined ${attempts} times (${outcome.message}). The invoice remains outstanding.`);
  }
  return { ...outcome, payment };
}

// The scheduler: find invoices whose autopay attempt time has arrived.
export async function runAutopay(asOf = new Date()) {
  const due = all(
    "SELECT i.* FROM invoices i JOIN customers c ON c.id=i.customer_id WHERE i.status='AUTHORISED' AND i.amount_due>0 AND c.autopay_enabled=1 AND i.autopay_next_attempt_at IS NOT NULL AND i.autopay_next_attempt_at<=? ORDER BY i.id LIMIT 50",
    [asOf.toISOString()],
  );
  const results = [];
  for (const inv of due) {
    const business = get('SELECT * FROM businesses WHERE id=?', [inv.business_id]);
    if (!gatewayConnection(business.id)) continue;
    try {
      const r = await chargeInvoiceWithSavedCard(business, inv, { source: 'autopay' });
      results.push({ invoice: inv.number, approved: r.approved, message: r.message });
    } catch (e) {
      update('invoices', inv.id, { autopay_last_error: e.message, autopay_next_attempt_at: new Date(Date.now() + 3600e3).toISOString() });
      results.push({ invoice: inv.number, approved: false, message: e.message });
    }
  }
  return results;
}

export async function refundPayment(business, payment, amount) {
  const gw = gatewayClient(gatewayConnection(business.id));
  const r = await gw.refund({ txnId: payment.gateway_txn_id, amount, reference: `REFUND ${payment.id}` });
  if (r.approved) {
    update('payments', payment.id, { status: 'refunded' });
    audit(business.id, 'user', 'payment.refunded', 'payment', payment.id, { amount, txn: r.txnId });
  }
  return r;
}
