// Demo-only: the Xero simulator UI and the mock NAB hosted payment page.
import { Router } from 'express';
import { isDemo } from '../config.js';
import { get, today } from '../db.js';
import { requireUser } from '../auth.js';
import { appPage, badge, date, esc, field, money, plainPage, table } from '../layout.js';
import { gwMock, xeroConnection, xeroMock } from '../providers/index.js';
import { ingestXeroEvents } from '../services/webhooks.js';

export const router = Router();

// ---------- Mock NAB hosted payment page (public, no login) ----------
router.get('/gsim/checkout/:id', (req, res) => {
  const c = get('SELECT * FROM gsim_checkouts WHERE checkout_id=?', [req.params.id]);
  if (!c) return res.status(404).send('Unknown checkout');
  if (c.status !== 'open') return res.redirect(c.return_url + (c.return_url.includes('?') ? '&' : '?') + 'checkout=' + c.checkout_id);
  res.send(plainPage({
    title: 'NAB Transact (simulated)', body: `
    <div class="hpp"><div class="bank">NAB TRANSACT · SECURE PAYMENT PAGE (SIMULATED)</div>
    <p class="small muted">In production this page is hosted by NAB. Card details are entered here and never reach the platform.</p>
    <dl class="kv"><dt>Merchant</dt><dd>${esc(c.merchant_id)}</dd><dt>Reference</dt><dd>${esc(c.reference)}</dd><dt>Description</dt><dd>${esc(c.description || '')}</dd><dt>Amount</dt><dd><strong>${money(c.amount, c.currency)}</strong>${c.tokenise ? ' <span class="badge blue">card will be stored</span>' : ''}</dd></dl>
    <form method="post" action="/gsim/checkout/${c.checkout_id}" style="margin-top:14px">
      ${field('Card number', 'pan', { value: '4111 1111 1111 1111', required: true })}
      <div class="grid c2">${field('Expiry (MM/YY)', 'expiry', { value: '12/29', required: true })}${field('CVV', 'cvv', { value: '123', required: true })}</div>
      ${field('Name on card', 'cardholder', { value: 'TEST CARDHOLDER' })}
      <button class="btn" style="width:100%">Pay ${money(c.amount, c.currency)}</button>
    </form>
    <details style="margin-top:12px"><summary class="small">Test cards</summary><ul class="small">
      <li><code>4111 1111 1111 1111</code> approved; stored card keeps approving</li>
      <li><code>4000 0000 0000 0002</code> declined (05 Do Not Honour)</li>
      <li><code>4000 0000 0000 0119</code> approved now, but later autopay charges on the stored card decline</li>
      <li><code>4000 0000 0000 9995</code> insufficient funds (51)</li></ul></details></div>`,
  }));
});
router.post('/gsim/checkout/:id', (req, res) => {
  try {
    const { returnUrl } = gwMock.processHostedCard(req.params.id, req.body);
    res.redirect(returnUrl + (returnUrl.includes('?') ? '&' : '?') + 'checkout=' + req.params.id);
  } catch (e) { res.status(400).send(e.message); }
});

// ---------- Xero simulator (requires business login) ----------
router.use('/sim', (req, res, next) => (isDemo() ? next() : res.status(404).send('Simulator is only available in demo mode')));
router.use('/sim', requireUser);

async function deliver(tenant_id) {
  const pending = xeroMock.pendingEvents(tenant_id);
  if (!pending.length) return [];
  const events = pending.map((e) => ({ resourceUrl: `sim://${e.category}/${e.resource_id}`, resourceId: e.resource_id, eventDateUtc: e.created_at, eventType: e.type, eventCategory: e.category, tenantId: tenant_id, tenantType: 'ORGANISATION' }));
  const r = await ingestXeroEvents(events);
  xeroMock.markDelivered(pending.map((e) => e.id));
  return r;
}

function ctx(req) {
  const conn = xeroConnection(req.business.id);
  if (!conn) return null;
  return { conn, tenant_id: conn.tenant_id, org: xeroMock.getOrg(conn.tenant_id) };
}

router.get('/sim', (req, res) => {
  const c = ctx(req);
  if (!c) return res.send(appPage({ title: 'Xero simulator', business: req.business, user: req.user, flash: req.flash, body: '<div class="card">Connect Xero first (it is instant in demo mode): <a class="btn sm" href="/app/xero/connect">Connect Xero</a></div>' }));
  const contacts = xeroMock.listContacts(c.tenant_id); const invoices = xeroMock.listInvoices(c.tenant_id);
  const repeating = xeroMock.listRepeating(c.tenant_id); const payments = xeroMock.listPayments(c.tenant_id); const pending = xeroMock.pendingEvents(c.tenant_id);
  const contactOpts = contacts.map((x) => [x.contact_id, x.name]);
  res.send(appPage({
    title: 'Xero simulator', business: req.business, user: req.user, flash: req.flash, body: `
    <div class="callout">This stands in for the real Xero organisation <strong>${esc(c.org.name)}</strong>. Anything you do here fires the same webhooks real Xero would, so you can watch the platform react. ${pending.length ? `<form class="inline" method="post" action="/sim/deliver"><button class="btn sm">Deliver ${pending.length} pending webhook${pending.length > 1 ? 's' : ''}</button></form>` : '<span class="badge green">webhooks delivered</span>'}</div>
    <div class="grid c2">
      <form class="card" method="post" action="/sim/contacts"><h3>Add a contact (customer)</h3>${field('Name', 'name', { required: true, placeholder: 'e.g. Priya Sharma' })}${field('Email', 'email', { type: 'email', placeholder: 'priya@example.com' })}${field('Phone', 'phone')}<button class="btn sm">Create contact</button></form>
      <form class="card" method="post" action="/sim/invoices"><h3>Create an invoice</h3>${field('Contact', 'contact_id', { options: contactOpts })}${field('Reference', 'reference', { placeholder: 'e.g. October services' })}
        <div class="grid c2">${field('Issue date', 'issue_date', { type: 'date', value: today() })}${field('Due date', 'due_date', { type: 'date', value: xeroMock.addDays(today(), 7) })}</div>
        ${field('Line description', 'description', { value: 'Consulting services' })}<div class="grid c2">${field('Quantity', 'quantity', { type: 'number', value: 1, step: '0.01' })}${field('Unit price (ex GST)', 'unit_amount', { type: 'number', value: 250, step: '0.01' })}</div>
        <button class="btn sm" ${contacts.length ? '' : 'disabled'}>Create and approve invoice</button></form>
      <form class="card" method="post" action="/sim/repeating"><h3>Create a repeating invoice</h3>${field('Contact', 'contact_id', { options: contactOpts })}${field('Reference', 'reference', { value: 'Monthly retainer' })}
        <div class="grid c2">${field('Every', 'period', { type: 'number', value: 1 })}${field('Unit', 'unit', { options: [['MONTHLY', 'month(s)'], ['WEEKLY', 'week(s)']] })}</div>
        <div class="grid c2">${field('Next invoice date', 'next_date', { type: 'date', value: today() })}${field('Due days after issue', 'due_days', { type: 'number', value: 7 })}</div>
        ${field('Line description', 'description', { value: 'Monthly retainer' })}${field('Amount (ex GST)', 'unit_amount', { type: 'number', value: 500, step: '0.01' })}
        <button class="btn sm" ${contacts.length ? '' : 'disabled'}>Create repeating template</button></form>
      <form class="card" method="post" action="/sim/run-repeating"><h3>Run Xero's overnight job</h3><p class="small muted">Xero generates invoices from repeating templates on their next date. Pick a date to pretend it is that day.</p>${field('As of', 'as_of', { type: 'date', value: today() })}<button class="btn sm" ${repeating.length ? '' : 'disabled'}>Generate due repeating invoices</button></form>
    </div>
    <h2>Contacts</h2>${table(['Name', 'Email', 'Contact ID'], contacts.map((x) => [esc(x.name), esc(x.email || ''), `<span class="mono small">${esc(x.contact_id)}</span>`]))}
    <h2>Invoices</h2>${table(['Number', 'Contact', 'Issued', 'Due', 'Total', 'Due', 'Status', ''], invoices.map((i) => [esc(i.number) + (i.repeating_invoice_id ? ' <span class="badge grey">repeating</span>' : ''), esc(contacts.find((x) => x.contact_id === i.contact_id)?.name || ''), date(i.issue_date), date(i.due_date), money(i.total), money(i.amount_due), badge(i.status), i.status === 'AUTHORISED' ? `<form method="post" action="/sim/invoices/${i.invoice_id}/void"><button class="btn sm secondary">Void</button></form>` : '']))}
    <h2>Repeating templates</h2>${table(['Reference', 'Contact', 'Schedule', 'Next date'], repeating.map((r) => [esc(r.reference), esc(contacts.find((x) => x.contact_id === r.contact_id)?.name || ''), `every ${r.period} ${r.unit.toLowerCase()}`, date(r.next_date)]))}
    <h2>Payments recorded in Xero</h2>${table(['Invoice', 'Amount', 'Date', 'Account', 'Reference'], payments.map((p) => [esc(p.number), money(p.amount), date(p.date), esc(p.account_code), esc(p.reference)]), 'None yet. These appear when the platform writes a card payment back.')}`,
  }));
});

router.post('/sim/contacts', async (req, res) => {
  const c = ctx(req); const { name, email, phone } = req.body;
  xeroMock.createContact(c.tenant_id, { name, email: email || null, phone: phone || null });
  await deliver(c.tenant_id);
  res.flash('ok', `Contact ${name} created in Xero and the CONTACT/CREATE webhook delivered. Check Customers and the Outbox.`);
  res.redirect('/sim');
});
router.post('/sim/invoices', async (req, res) => {
  const c = ctx(req); const f = req.body;
  const inv = xeroMock.createInvoice(c.tenant_id, { contact_id: f.contact_id, reference: f.reference, issue_date: f.issue_date, due_date: f.due_date, lines: [{ description: f.description, quantity: Number(f.quantity), unit_amount: Number(f.unit_amount), tax_type: 'OUTPUT' }] });
  await deliver(c.tenant_id);
  res.flash('ok', `${inv.number} approved in Xero and the INVOICE/CREATE webhook delivered.`);
  res.redirect('/sim');
});
router.post('/sim/invoices/:id/void', async (req, res) => {
  const c = ctx(req);
  xeroMock.setInvoiceStatus(c.tenant_id, req.params.id, 'VOIDED');
  await deliver(c.tenant_id);
  res.flash('ok', 'Invoice voided in Xero; the platform cancelled any pending autopay for it.');
  res.redirect('/sim');
});
router.post('/sim/repeating', (req, res) => {
  const c = ctx(req); const f = req.body;
  xeroMock.createRepeating(c.tenant_id, { contact_id: f.contact_id, reference: f.reference, period: Number(f.period), unit: f.unit, due_days: Number(f.due_days), next_date: f.next_date, lines: [{ description: f.description, quantity: 1, unit_amount: Number(f.unit_amount), tax_type: 'OUTPUT' }] });
  res.flash('ok', 'Repeating template saved. Run the overnight job to generate invoices from it.');
  res.redirect('/sim');
});
router.post('/sim/run-repeating', async (req, res) => {
  const c = ctx(req);
  const made = xeroMock.runRepeating(c.tenant_id, req.body.as_of || today());
  await deliver(c.tenant_id);
  res.flash('ok', made.length ? `Generated ${made.map((i) => i.number).join(', ')} and delivered webhooks.` : 'No repeating templates were due by that date.');
  res.redirect('/sim');
});
router.post('/sim/deliver', async (req, res) => {
  const c = ctx(req); const r = await deliver(c.tenant_id);
  res.flash('ok', `Delivered ${r.length} webhook event(s).`); res.redirect('/sim');
});
