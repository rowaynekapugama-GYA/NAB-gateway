// Public pay pages: the per-invoice pay link, the Xero "Pay Now" entry point,
// and the return leg from the gateway's hosted payment page.
import { Router } from 'express';
import { config } from '../config.js';
import { all, audit, get, now, settings, update } from '../db.js';
import { sign, verifySigned } from '../crypto.js';
import { badge, date, esc, money, plainPage } from '../layout.js';
import { gatewayClient, gatewayConnection, xeroClient, xeroConnection } from '../providers/index.js';
import { upsertInvoice } from '../services/sync.js';
import { recordPayment, savePaymentMethod } from '../services/payments.js';
import { portalLoginUrl } from '../services/notifications.js';

export const router = Router();

function load(token) {
  const invoice = get('SELECT * FROM invoices WHERE pay_token=?', [token]);
  if (!invoice) return null;
  const business = get('SELECT * FROM businesses WHERE id=?', [invoice.business_id]);
  const customer = invoice.customer_id ? get('SELECT * FROM customers WHERE id=?', [invoice.customer_id]) : null;
  return { invoice, business, customer };
}

function invoiceCard(business, invoice, customer) {
  const lines = JSON.parse(invoice.line_items_json || '[]');
  return `<div class="card">
    <div class="row between"><div><div class="muted small">Invoice</div><strong>${esc(invoice.number)}</strong></div><div class="right"><div class="muted small">Due ${date(invoice.due_date)}</div>${badge(invoice.status)}</div></div>
    ${customer ? `<p class="small muted" style="margin-top:8px">Billed to ${esc(customer.name)}</p>` : ''}
    <table class="invoice-lines" style="margin-top:10px"><tbody>
    ${lines.map((l) => `<tr><td>${esc(l.description)}</td><td class="num">${esc(l.quantity)} × ${money(l.unit_amount, invoice.currency)}</td><td class="num">${money(l.line_amount, invoice.currency)}</td></tr>`).join('')}
    <tr><td colspan="2" class="num">GST</td><td class="num">${money(invoice.tax, invoice.currency)}</td></tr>
    <tr class="total-row"><td colspan="2" class="num">Amount due</td><td class="num">${money(invoice.amount_due, invoice.currency)}</td></tr></tbody></table></div>`;
}

// Xero "Pay Now" button lands here with Xero's placeholders filled in.
router.get('/x/:code/pay', async (req, res) => {
  const business = get('SELECT * FROM businesses WHERE short_code=?', [req.params.code]);
  if (!business) return res.status(404).send(plainPage({ title: 'Not found', body: '<div class="card">Unknown business.</div>' }));
  const number = String(req.query.inv || '').trim();
  let invoice = get('SELECT * FROM invoices WHERE business_id=? AND number=?', [business.id, number]);
  if (!invoice) {
    // Not synced yet (webhook delay): fetch it directly from Xero by number.
    try {
      const xi = await xeroClient(xeroConnection(business.id)).invoiceByNumber(number);
      if (xi) invoice = upsertInvoice(business, xi, { notify: false })?.invoice;
    } catch { /* fall through */ }
  }
  if (!invoice) return res.status(404).send(plainPage({ title: 'Invoice not found', brand: business.brand_colour, body: `<div class="card"><h2>We could not find invoice ${esc(number)}</h2><p>Please contact ${esc(business.name)}${business.phone ? ` on ${esc(business.phone)}` : ''}.</p></div>` }));
  audit(business.id, 'xero_paynow', 'paylink.opened_from_xero', 'invoice', invoice.id, null);
  res.redirect(`/pay/${invoice.pay_token}?src=xero`);
});

router.get('/pay/:token', (req, res) => {
  const ctx = load(req.params.token);
  if (!ctx) return res.status(404).send(plainPage({ title: 'Not found', body: '<div class="card">This payment link is not valid.</div>' }));
  const { invoice, business, customer } = ctx;
  const s = settings(business); const gw = gatewayConnection(business.id);
  const payable = invoice.status === 'AUTHORISED' && invoice.amount_due > 0;
  const canSave = s.autopay_allowed && !!customer;
  res.send(plainPage({
    title: `Pay invoice ${invoice.number}`, brand: business.brand_colour, flash: req.flash, body: `
    <div class="brand-mark">${business.logo_url ? `<img src="${esc(business.logo_url)}" alt="" style="height:32px;vertical-align:middle"> ` : ''}${esc(business.name)}</div>
    ${invoiceCard(business, invoice, customer)}
    ${payable ? (gw ? `<div class="card"><h3>Pay by card</h3>
      <form method="post" action="/pay/${invoice.pay_token}/start">
        <input type="hidden" name="src" value="${esc(req.query.src || 'pay_link')}">
        ${canSave ? `<label class="check"><input type="checkbox" name="save_card" value="1"> <span>Save this card securely with NAB and pay future invoices from ${esc(business.name)} automatically on their due date. You can turn this off any time in your portal.</span></label>` : ''}
        <button class="btn" style="width:100%">Pay ${money(invoice.amount_due, invoice.currency)}</button>
      </form>
      <p class="small muted" style="margin-top:10px">You will be taken to NAB's secure payment page. No surcharge applies.</p></div>`
      : `<div class="card"><p>${esc(business.name)} has not finished setting up card payments yet. Please contact them for other ways to pay.</p></div>`)
      : `<div class="card"><p>${invoice.status === 'PAID' ? 'This invoice has been paid. Thank you!' : 'This invoice is no longer payable online.'}</p></div>`}
    ${customer ? `<p class="small muted">See all your invoices or manage automatic payments in your <a href="/portal?biz=${esc(business.slug)}">customer portal</a>.</p>` : ''}`,
  }));
});

router.post('/pay/:token/start', async (req, res) => {
  const ctx = load(req.params.token);
  if (!ctx) return res.status(404).send('Invalid link');
  const { invoice, business, customer } = ctx;
  if (!(invoice.status === 'AUTHORISED' && invoice.amount_due > 0)) return res.redirect(`/pay/${invoice.pay_token}`);
  const save = req.body.save_card === '1' && settings(business).autopay_allowed && !!customer;
  const src = req.body.src === 'xero' ? 'xero_paynow' : (req.body.src === 'portal' ? 'portal' : 'pay_link');
  const intent = `${invoice.id}:${save ? 1 : 0}:${src}:${Date.now()}`;
  const returnUrl = `${config.baseUrl}/pay/${invoice.pay_token}/return?i=${encodeURIComponent(intent)}&s=${sign(intent)}`;
  try {
    const gw = gatewayClient(gatewayConnection(business.id));
    const co = await gw.createCheckout({
      amount: invoice.amount_due, currency: invoice.currency, reference: invoice.number,
      description: `${business.name} invoice ${invoice.number}`, returnUrl, tokenise: save,
    });
    audit(business.id, src, 'checkout.started', 'invoice', invoice.id, { checkout: co.checkoutId, save });
    res.redirect(co.redirectUrl);
  } catch (e) {
    res.flash('err', `Could not start payment: ${e.message}`); res.redirect(`/pay/${invoice.pay_token}`);
  }
});

router.get('/pay/:token/return', async (req, res) => {
  const ctx = load(req.params.token);
  if (!ctx) return res.status(404).send('Invalid link');
  const { invoice, business } = ctx;
  let customer = ctx.customer;
  const intent = String(req.query.i || '');
  if (!verifySigned(intent, String(req.query.s || ''))) { res.flash('err', 'Payment return could not be verified.'); return res.redirect(`/pay/${invoice.pay_token}`); }
  const [, saveFlag, src] = intent.split(':');
  const checkoutId = req.query.checkout;
  try {
    const gw = gatewayClient(gatewayConnection(business.id));
    const outcome = await gw.completeCheckout(checkoutId, req.query);
    // Idempotency: the customer may refresh the return page.
    if (outcome.txnId && get('SELECT id FROM payments WHERE gateway_txn_id=?', [outcome.txnId])) return res.redirect(`/pay/${invoice.pay_token}/done?txn=${encodeURIComponent(outcome.txnId)}`);
    const fresh = get('SELECT * FROM invoices WHERE id=?', [invoice.id]);
    let pm = null;
    if (outcome.approved && saveFlag === '1' && outcome.token && customer) {
      pm = savePaymentMethod(business, customer, outcome.token);
      update('customers', customer.id, { autopay_enabled: 1, autopay_payment_method_id: pm.id, portal_status: customer.portal_status === 'none' ? 'invited' : customer.portal_status, updated_at: now() });
      audit(business.id, `customer:${customer.id}`, 'customer.autopay_enabled', 'customer', customer.id, { via: 'pay_page' });
      customer = get('SELECT * FROM customers WHERE id=?', [customer.id]);
      // Any other open invoices for this customer now get scheduled too.
      for (const other of all("SELECT * FROM invoices WHERE customer_id=? AND id<>? AND status='AUTHORISED' AND amount_due>0 AND autopay_next_attempt_at IS NULL", [customer.id, invoice.id])) {
        const when = other.due_date && other.due_date > now().slice(0, 10) ? other.due_date : now().slice(0, 10);
        update('invoices', other.id, { autopay_scheduled_for: when, autopay_next_attempt_at: when + 'T00:00:00.000Z' });
      }
    }
    const payment = await recordPayment(business, fresh, outcome, { source: src, customer, payment_method_id: pm?.id || null });
    if (!outcome.approved) { res.flash('err', `Payment was not approved (${outcome.message}). No money was taken; please try another card.`); return res.redirect(`/pay/${invoice.pay_token}`); }
    res.redirect(`/pay/${invoice.pay_token}/done?txn=${encodeURIComponent(payment.gateway_txn_id || '')}`);
  } catch (e) {
    res.flash('err', `Something went wrong confirming the payment: ${e.message}`); res.redirect(`/pay/${invoice.pay_token}`);
  }
});

router.get('/pay/:token/done', (req, res) => {
  const ctx = load(req.params.token);
  if (!ctx) return res.status(404).send('Invalid link');
  const { invoice, business, customer } = ctx;
  const p = get('SELECT * FROM payments WHERE invoice_id=? AND gateway_txn_id=?', [invoice.id, req.query.txn]) || get("SELECT * FROM payments WHERE invoice_id=? AND status='succeeded' ORDER BY id DESC", [invoice.id]);
  res.send(plainPage({
    title: 'Payment received', brand: business.brand_colour, body: `
    <div class="brand-mark">${esc(business.name)}</div>
    <div class="card"><h2>Thank you, your payment went through</h2>
      <dl class="kv"><dt>Invoice</dt><dd>${esc(invoice.number)}</dd><dt>Amount</dt><dd>${money(p?.amount, invoice.currency)}</dd><dt>Reference</dt><dd class="mono">${esc(p?.gateway_txn_id || '')}</dd><dt>Receipt</dt><dd>${customer?.email ? `emailed to ${esc(customer.email)}` : 'available in your portal'}</dd></dl>
      ${customer?.autopay_enabled ? `<div class="notice">Automatic payments are on. Future invoices from ${esc(business.name)} will be charged to your saved card on their due date, and you will get a receipt each time.</div>` : ''}
    </div>
    ${customer ? `<p class="small"><a class="btn secondary" href="${portalLoginUrl(customer)}">Open your customer portal</a></p>` : ''}`,
  }));
});
