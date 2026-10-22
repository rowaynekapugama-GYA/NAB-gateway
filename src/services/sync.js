// Keeps the platform's mirror of Xero contacts and invoices up to date and
// decides what happens when a new invoice appears (send pay link, or
// schedule an automatic charge).
import { all, audit, get, insert, now, settings, today, update } from '../db.js';
import { token } from '../crypto.js';
import { xeroClient, xeroConnection } from '../providers/index.js';
import { sendPayLink, sendPortalInvite } from './notifications.js';

const phoneOf = (c) => (c.Phones || []).find((p) => p.PhoneNumber)?.PhoneNumber || null;

export function upsertContact(business, xc) {
  const existing = get('SELECT * FROM customers WHERE business_id=? AND xero_contact_id=?', [business.id, xc.ContactID]);
  const fields = { name: xc.Name, email: xc.EmailAddress || null, phone: phoneOf(xc), updated_at: now() };
  if (existing) {
    update('customers', existing.id, fields);
    return { customer: get('SELECT * FROM customers WHERE id=?', [existing.id]), created: false };
  }
  const id = insert('customers', {
    business_id: business.id, xero_contact_id: xc.ContactID, ...fields, portal_token: token(12), created_at: now(),
  });
  const customer = get('SELECT * FROM customers WHERE id=?', [id]);
  audit(business.id, 'system', 'customer.created_from_xero', 'customer', id, { name: customer.name });
  // Workflow: a new Xero contact gets a portal automatically. Invite if we
  // have an email; otherwise the business can add one and invite later.
  if (customer.email && settings(business).autopay_allowed) sendPortalInvite(business, customer);
  return { customer, created: true };
}

function autopayScheduleDate(business, customer, invoice) {
  const s = settings(business);
  const timing = customer.autopay_timing || s.autopay_default_timing;
  const days = customer.autopay_timing ? customer.autopay_days_before : s.autopay_days_before;
  if (timing === 'on_issue') return today();
  if (timing === 'days_before') {
    const d = new Date((invoice.due_date || today()) + 'T00:00:00Z');
    d.setUTCDate(d.getUTCDate() - Number(days || 0));
    const iso = d.toISOString().slice(0, 10);
    return iso < today() ? today() : iso;
  }
  return invoice.due_date && invoice.due_date >= today() ? invoice.due_date : today();
}

export function upsertInvoice(business, xi, { notify = true } = {}) {
  if (xi.Type && xi.Type !== 'ACCREC') return null; // bills are not ours
  const customer = xi.Contact?.ContactID
    ? get('SELECT * FROM customers WHERE business_id=? AND xero_contact_id=?', [business.id, xi.Contact.ContactID])
    : null;
  const existing = get('SELECT * FROM invoices WHERE business_id=? AND xero_invoice_id=?', [business.id, xi.InvoiceID]);
  const fields = {
    customer_id: customer?.id || existing?.customer_id || null,
    number: xi.InvoiceNumber, reference: xi.Reference || null, status: xi.Status,
    issue_date: (xi.DateString || xi.Date || '').slice(0, 10) || null,
    due_date: (xi.DueDateString || xi.DueDate || '').slice(0, 10) || null,
    currency: xi.CurrencyCode || 'AUD',
    subtotal: xi.SubTotal, tax: xi.TotalTax, total: xi.Total,
    amount_due: xi.AmountDue, amount_paid: xi.AmountPaid || 0,
    line_items_json: JSON.stringify((xi.LineItems || []).map((l) => ({
      description: l.Description, quantity: l.Quantity, unit_amount: l.UnitAmount, line_amount: l.LineAmount ?? (l.Quantity * l.UnitAmount),
    }))),
    repeating_invoice_id: xi.RepeatingInvoiceID || null,
    updated_at: now(),
  };

  let invoice;
  if (existing) {
    // If the invoice is no longer payable, clear any pending autopay.
    if (fields.status !== 'AUTHORISED' || fields.amount_due <= 0) {
      fields.autopay_scheduled_for = null;
      fields.autopay_next_attempt_at = null;
    }
    update('invoices', existing.id, fields);
    invoice = get('SELECT * FROM invoices WHERE id=?', [existing.id]);
    return { invoice, created: false };
  }

  const id = insert('invoices', { business_id: business.id, xero_invoice_id: xi.InvoiceID, pay_token: token(12), created_at: now(), ...fields });
  invoice = get('SELECT * FROM invoices WHERE id=?', [id]);
  audit(business.id, 'system', 'invoice.created_from_xero', 'invoice', id, { number: invoice.number, total: invoice.total });

  // Workflow decision for a new payable invoice
  if (invoice.status === 'AUTHORISED' && invoice.amount_due > 0 && customer) {
    if (customer.autopay_enabled && customer.autopay_payment_method_id) {
      const when = autopayScheduleDate(business, customer, invoice);
      update('invoices', id, { autopay_scheduled_for: when, autopay_next_attempt_at: when + 'T00:00:00.000Z' });
      audit(business.id, 'system', 'invoice.autopay_scheduled', 'invoice', id, { when });
      invoice = get('SELECT * FROM invoices WHERE id=?', [id]);
    } else if (notify && settings(business).send_pay_link_on_invoice && customer.email) {
      sendPayLink(business, customer, invoice);
    }
  }
  return { invoice, created: true };
}

// Pull everything from Xero (used on first connect and the manual "Sync now").
export async function fullSync(business, { notify = false } = {}) {
  const conn = xeroConnection(business.id);
  const x = xeroClient(conn);
  const stats = { contacts: 0, invoices: 0 };
  for (const c of await x.contacts()) { upsertContact(business, c); stats.contacts++; }
  for (const i of await x.invoices()) { if (upsertInvoice(business, i, { notify })) stats.invoices++; }
  update('connections', conn.id, { last_sync_at: now() });
  audit(business.id, 'system', 'xero.synced', 'connection', conn.id, stats);
  return stats;
}

export async function refreshInvoice(business, xeroInvoiceId) {
  const x = xeroClient(xeroConnection(business.id));
  const xi = await x.invoice(xeroInvoiceId);
  return xi ? upsertInvoice(business, xi).invoice : null;
}

export function openInvoicesFor(customer_id) {
  return all("SELECT * FROM invoices WHERE customer_id=? AND status='AUTHORISED' AND amount_due>0 ORDER BY due_date", [customer_id]);
}
