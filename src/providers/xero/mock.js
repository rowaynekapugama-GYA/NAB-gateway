// Xero simulator used in demo mode. Behaves like a tiny Xero organisation:
// contacts, invoices, repeating invoices, payments, and webhook events that
// are delivered in-process to the platform's webhook handler.
import { randomUUID } from 'node:crypto';
import { all, get, insert, now, run, today, update } from '../../db.js';
import { shortCode } from '../../crypto.js';

const uuid = () => randomUUID();

export function ensureOrg(name) {
  const tenant_id = uuid();
  const id = insert('xsim_orgs', {
    tenant_id, name: `${name} (Demo Xero)`, short_code: '!' + shortCode(5), created_at: now(),
  });
  return get('SELECT * FROM xsim_orgs WHERE id=?', [id]);
}

export function getOrg(tenant_id) {
  return get('SELECT * FROM xsim_orgs WHERE tenant_id=?', [tenant_id]);
}

function queueEvent(tenant_id, category, type, resource_id) {
  insert('xsim_webhook_queue', { tenant_id, category, type, resource_id, created_at: now() });
}

// ---------- Contacts ----------
export function createContact(tenant_id, { name, email, phone }) {
  const contact_id = uuid();
  insert('xsim_contacts', { tenant_id, contact_id, name, email, phone, updated_at: now() });
  queueEvent(tenant_id, 'CONTACT', 'CREATE', contact_id);
  return getContact(tenant_id, contact_id);
}
export function updateContact(tenant_id, contact_id, fields) {
  const c = get('SELECT * FROM xsim_contacts WHERE contact_id=?', [contact_id]);
  update('xsim_contacts', c.id, { ...fields, updated_at: now() });
  queueEvent(tenant_id, 'CONTACT', 'UPDATE', contact_id);
}
export function listContacts(tenant_id) {
  return all('SELECT * FROM xsim_contacts WHERE tenant_id=? ORDER BY name', [tenant_id]);
}
export function getContact(tenant_id, contact_id) {
  return get('SELECT * FROM xsim_contacts WHERE tenant_id=? AND contact_id=?', [tenant_id, contact_id]);
}

// ---------- Invoices ----------
function totals(lines) {
  const subtotal = lines.reduce((s, l) => s + Number(l.quantity) * Number(l.unit_amount), 0);
  const tax = lines.reduce((s, l) => s + (l.tax_type === 'OUTPUT' ? Number(l.quantity) * Number(l.unit_amount) * 0.1 : 0), 0);
  return { subtotal: round(subtotal), tax: round(tax), total: round(subtotal + tax) };
}
const round = (n) => Math.round(n * 100) / 100;

export function createInvoice(tenant_id, { contact_id, reference, issue_date, due_date, lines, status = 'AUTHORISED', repeating_invoice_id = null }) {
  const org = getOrg(tenant_id);
  const number = `INV-${String(org.next_invoice_no).padStart(4, '0')}`;
  update('xsim_orgs', org.id, { next_invoice_no: org.next_invoice_no + 1 });
  const t = totals(lines);
  const invoice_id = uuid();
  insert('xsim_invoices', {
    tenant_id, invoice_id, contact_id, number, reference, status,
    issue_date: issue_date || today(), due_date: due_date || addDays(issue_date || today(), 7),
    subtotal: t.subtotal, tax: t.tax, total: t.total, amount_due: t.total, amount_paid: 0,
    line_items_json: JSON.stringify(lines), repeating_invoice_id, updated_at: now(),
  });
  queueEvent(tenant_id, 'INVOICE', 'CREATE', invoice_id);
  return getInvoice(tenant_id, invoice_id);
}
export function listInvoices(tenant_id) {
  return all('SELECT * FROM xsim_invoices WHERE tenant_id=? ORDER BY issue_date DESC, id DESC', [tenant_id]);
}
export function getInvoice(tenant_id, invoice_id) {
  return get('SELECT * FROM xsim_invoices WHERE tenant_id=? AND invoice_id=?', [tenant_id, invoice_id]);
}
export function findInvoiceByNumber(tenant_id, number) {
  return get('SELECT * FROM xsim_invoices WHERE tenant_id=? AND number=?', [tenant_id, number]);
}
export function setInvoiceStatus(tenant_id, invoice_id, status) {
  const inv = getInvoice(tenant_id, invoice_id);
  update('xsim_invoices', inv.id, { status, updated_at: now() });
  queueEvent(tenant_id, 'INVOICE', 'UPDATE', invoice_id);
}

// ---------- Payments ----------
export function createPayment(tenant_id, { invoice_id, account_code, amount, date, reference }) {
  const inv = getInvoice(tenant_id, invoice_id);
  if (!inv) throw new Error('Invoice not found in Xero simulator');
  if (inv.status !== 'AUTHORISED') throw new Error(`Invoice ${inv.number} is ${inv.status}; payments can only be applied to AUTHORISED invoices`);
  if (amount > inv.amount_due + 0.005) throw new Error(`Payment ${amount} exceeds amount due ${inv.amount_due}`);
  const payment_id = uuid();
  insert('xsim_payments', { tenant_id, payment_id, invoice_id, account_code, amount, date, reference, created_at: now() });
  const amount_paid = round(inv.amount_paid + amount);
  const amount_due = round(inv.total - amount_paid);
  update('xsim_invoices', inv.id, { amount_paid, amount_due, status: amount_due <= 0 ? 'PAID' : 'AUTHORISED', updated_at: now() });
  queueEvent(tenant_id, 'INVOICE', 'UPDATE', invoice_id);
  return { payment_id };
}
export function listPayments(tenant_id) {
  return all('SELECT p.*, i.number FROM xsim_payments p JOIN xsim_invoices i ON i.invoice_id=p.invoice_id WHERE p.tenant_id=? ORDER BY p.id DESC', [tenant_id]);
}

// ---------- Repeating invoices ----------
export function createRepeating(tenant_id, { contact_id, reference, period, unit, due_days, next_date, lines }) {
  const repeating_id = uuid();
  insert('xsim_repeating', {
    tenant_id, repeating_id, contact_id, reference, period, unit, due_days, next_date,
    line_items_json: JSON.stringify(lines), updated_at: now(),
  });
  return get('SELECT * FROM xsim_repeating WHERE repeating_id=?', [repeating_id]);
}
export function listRepeating(tenant_id) {
  return all('SELECT * FROM xsim_repeating WHERE tenant_id=? ORDER BY next_date', [tenant_id]);
}
// Simulates Xero's overnight job that turns repeating templates into invoices.
export function runRepeating(tenant_id, asOf = today()) {
  const due = all('SELECT * FROM xsim_repeating WHERE tenant_id=? AND status=? AND next_date<=?', [tenant_id, 'AUTHORISED', asOf]);
  const created = [];
  for (const r of due) {
    const inv = createInvoice(tenant_id, {
      contact_id: r.contact_id, reference: r.reference, issue_date: r.next_date,
      due_date: addDays(r.next_date, r.due_days), lines: JSON.parse(r.line_items_json),
      repeating_invoice_id: r.repeating_id,
    });
    created.push(inv);
    update('xsim_repeating', r.id, { next_date: advance(r.next_date, r.period, r.unit), updated_at: now() });
  }
  return created;
}

// ---------- Accounts (chart of accounts subset) ----------
export function listAccounts() {
  return [
    { code: '090', name: 'Business Bank Account', type: 'BANK', enable_payments: true },
    { code: '091', name: 'NAB Transact Clearing', type: 'CURRENT', enable_payments: true },
    { code: '200', name: 'Sales', type: 'REVENUE', enable_payments: false },
  ];
}

// ---------- Webhook delivery ----------
export function pendingEvents(tenant_id) {
  return all('SELECT * FROM xsim_webhook_queue WHERE tenant_id=? AND delivered_at IS NULL ORDER BY id', [tenant_id]);
}
export function markDelivered(ids) {
  for (const id of ids) run('UPDATE xsim_webhook_queue SET delivered_at=? WHERE id=?', [now(), id]);
}

// ---------- helpers ----------
export function addDays(dateStr, days) {
  const d = new Date(dateStr + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() + Number(days));
  return d.toISOString().slice(0, 10);
}
function advance(dateStr, period, unit) {
  const d = new Date(dateStr + 'T00:00:00Z');
  if (unit === 'WEEKLY') d.setUTCDate(d.getUTCDate() + 7 * period);
  else d.setUTCMonth(d.getUTCMonth() + Number(period));
  return d.toISOString().slice(0, 10);
}

// Adapter used by the platform's sync code (same shape as live.js client)
export function client(connection) {
  const tenant_id = connection.tenant_id;
  const toInvoice = (i) => i && ({
    InvoiceID: i.invoice_id, InvoiceNumber: i.number, Reference: i.reference, Status: i.status,
    Type: 'ACCREC', Contact: { ContactID: i.contact_id }, DateString: i.issue_date, DueDateString: i.due_date,
    CurrencyCode: 'AUD', SubTotal: i.subtotal, TotalTax: i.tax, Total: i.total, AmountDue: i.amount_due,
    AmountPaid: i.amount_paid, LineItems: JSON.parse(i.line_items_json || '[]').map((l) => ({
      Description: l.description, Quantity: l.quantity, UnitAmount: l.unit_amount, TaxType: l.tax_type,
    })), RepeatingInvoiceID: i.repeating_invoice_id,
  });
  const toContact = (c) => c && ({ ContactID: c.contact_id, Name: c.name, EmailAddress: c.email, Phones: c.phone ? [{ PhoneType: 'DEFAULT', PhoneNumber: c.phone }] : [] });
  return {
    async organisation() { const o = getOrg(tenant_id); return { Name: o.name, ShortCode: o.short_code }; },
    async contacts() { return listContacts(tenant_id).map(toContact); },
    async contact(id) { return toContact(getContact(tenant_id, id)); },
    async invoices() { return listInvoices(tenant_id).filter((i) => i.status !== 'DRAFT').map(toInvoice); },
    async invoice(id) { return toInvoice(getInvoice(tenant_id, id)); },
    async invoiceByNumber(number) { return toInvoice(findInvoiceByNumber(tenant_id, number)); },
    async accounts() { return listAccounts().map((a) => ({ Code: a.code, Name: a.name, Type: a.type, EnablePaymentsToAccount: a.enable_payments })); },
    async createPayment({ invoiceId, accountCode, amount, date, reference }) {
      const r = createPayment(tenant_id, { invoice_id: invoiceId, account_code: accountCode, amount, date, reference });
      return { PaymentID: r.payment_id };
    },
  };
}
