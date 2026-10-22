import { Router } from 'express';
import { config, isDemo } from '../config.js';
import { all, audit, get, insert, now, run, settings, today, update } from '../db.js';
import { encrypt, token } from '../crypto.js';
import { requireUser } from '../auth.js';
import { appPage, badge, date, datetime, esc, field, money, stat, table } from '../layout.js';
import { gatewayClient, gatewayConnection, xeroClient, xeroConnection, xeroLive, xeroMock } from '../providers/index.js';
import { fullSync } from '../services/sync.js';
import { chargeInvoiceWithSavedCard, refundPayment, runAutopay } from '../services/payments.js';
import { payLinkUrl, sendMagicLink, sendPayLink, sendPortalInvite } from '../services/notifications.js';

export const router = Router();
router.use(requireUser);

const page = (req, opts) => appPage({ business: req.business, user: req.user, flash: req.flash, ...opts });

// ---------------- Overview ----------------
router.get('/', (req, res) => {
  const b = req.business; const s = settings(b);
  const xero = xeroConnection(b.id); const gw = gatewayConnection(b.id);
  const month = today().slice(0, 7);
  const collected = get("SELECT COALESCE(SUM(amount),0) v, COUNT(*) n FROM payments WHERE business_id=? AND status='succeeded' AND substr(created_at,1,7)=?", [b.id, month]);
  const outstanding = get("SELECT COALESCE(SUM(amount_due),0) v, COUNT(*) n FROM invoices WHERE business_id=? AND status='AUTHORISED' AND amount_due>0", [b.id]);
  const overdue = get("SELECT COALESCE(SUM(amount_due),0) v, COUNT(*) n FROM invoices WHERE business_id=? AND status='AUTHORISED' AND amount_due>0 AND due_date<?", [b.id, today()]);
  const autopay = get('SELECT COUNT(*) n FROM customers WHERE business_id=? AND autopay_enabled=1', [b.id]);
  const customers = get('SELECT COUNT(*) n FROM customers WHERE business_id=?', [b.id]);
  const recent = all('SELECT p.*, i.number, c.name cname FROM payments p LEFT JOIN invoices i ON i.id=p.invoice_id LEFT JOIN customers c ON c.id=p.customer_id WHERE p.business_id=? ORDER BY p.id DESC LIMIT 8', [b.id]);
  const upcoming = all("SELECT i.*, c.name cname FROM invoices i JOIN customers c ON c.id=i.customer_id WHERE i.business_id=? AND i.autopay_next_attempt_at IS NOT NULL AND i.status='AUTHORISED' ORDER BY i.autopay_next_attempt_at LIMIT 8", [b.id]);

  const xeroOk = xero?.status === 'connected'; const gwOk = gw?.status === 'connected';
  const payNowOk = !!s.xero_paynow_configured;
  const setup = `
  <div class="steps">
    <div class="step ${xeroOk ? 'done' : ''}"><div class="n">1</div><div><div class="t">Connect Xero</div>
      ${xeroOk ? `<div class="small">Connected to <strong>${esc(xero.tenant_name)}</strong>. Last sync ${datetime(xero.last_sync_at) || 'never'}. <form class="inline" method="post" action="/app/xero/sync"><button class="btn sm secondary">Sync now</button></form> <form class="inline" method="post" action="/app/xero/disconnect"><button class="btn sm secondary">Disconnect</button></form></div>`
        : `<div class="small muted">Authorise ${esc(config.appName)} to read your contacts and invoices and record payments.</div><a class="btn sm" href="/app/xero/connect">Connect Xero</a>`}</div></div>
    <div class="step ${gwOk ? 'done' : ''}"><div class="n">2</div><div><div class="t">Connect your NAB gateway</div>
      ${gwOk ? `<div class="small">Merchant <strong>${esc(gw.merchant_id)}</strong> (${esc(gw.environment)}). <a href="/app/gateway">Manage</a></div>` : `<div class="small muted">Enter the merchant ID and transaction password NAB gave you. Funds settle directly to your NAB account.</div><a class="btn sm" href="/app/gateway">Add gateway details</a>`}</div></div>
    <div class="step ${payNowOk ? 'done' : ''}"><div class="n">3</div><div><div class="t">Put the Pay Now button on your Xero invoices</div>
      <div class="small muted">Add this custom payment URL in Xero so the Pay Now button on Xero's own online invoice comes to us. <a href="/app/settings#paynow">Instructions</a></div></div></div>
    <div class="step ${xeroOk && gwOk ? 'done' : ''}"><div class="n">4</div><div><div class="t">You're live</div><div class="small muted">New invoices get a pay link, new contacts get a portal invite, and autopay runs on schedule.</div></div></div>
  </div>`;

  res.send(page(req, {
    title: 'Overview', active: 'overview', body: `
    ${!(xeroOk && gwOk && payNowOk) ? `<h2>Setup</h2>${setup}` : ''}
    <h2>This month</h2>
    <div class="grid c4">
      ${stat('Collected by card', money(collected.v), `${collected.n} payments`)}
      ${stat('Outstanding', money(outstanding.v), `${outstanding.n} invoices`)}
      ${stat('Overdue', money(overdue.v), `${overdue.n} invoices`)}
      ${stat('Customers on autopay', `${autopay.n} / ${customers.n}`)}
    </div>
    <div class="grid c2" style="margin-top:16px">
      <div><h2>Recent payments</h2>${table(['When', 'Customer', 'Invoice', 'Amount', 'Status'], recent.map((p) => [datetime(p.created_at), esc(p.cname), `<a href="/app/invoices/${p.invoice_id}">${esc(p.number)}</a>`, money(p.amount, p.currency), badge(p.status)]), 'No payments yet.')}</div>
      <div><h2>Upcoming autopay</h2>${table(['Scheduled', 'Customer', 'Invoice', 'Amount'], upcoming.map((i) => [date(i.autopay_next_attempt_at), esc(i.cname), `<a href="/app/invoices/${i.id}">${esc(i.number)}</a>`, money(i.amount_due, i.currency)]), 'Nothing scheduled.')}</div>
    </div>
    ${xeroOk && gwOk && payNowOk ? `<details style="margin-top:20px"><summary>Connections</summary>${setup}</details>` : ''}`,
  }));
});

// ---------------- Xero connection ----------------
router.get('/xero/connect', (req, res) => {
  const b = req.business;
  if (isDemo()) {
    const org = xeroMock.ensureOrg(b.name);
    run('DELETE FROM connections WHERE business_id=? AND provider=?', [b.id, 'xero']);
    insert('connections', { business_id: b.id, provider: 'xero', status: 'connected', tenant_id: org.tenant_id, tenant_name: org.name, connected_at: now() });
    audit(b.id, `user:${req.user.id}`, 'xero.connected', 'connection', null, { tenant: org.name, demo: true });
    res.flash('ok', `Connected to ${org.name}. Use the Xero simulator to add contacts and invoices.`);
    return res.redirect('/app');
  }
  const state = token(16);
  res.cookie?.('xero_state', state);
  res.setHeader('Set-Cookie', `xero_state=${state}; Path=/; HttpOnly; SameSite=Lax; Max-Age=600`);
  res.redirect(xeroLive.getAuthUrl(`${b.id}.${state}`));
});

router.get('/xero/callback', async (req, res) => {
  const b = req.business;
  try {
    const { code, state } = req.query;
    if (!code || !state || !String(state).startsWith(`${b.id}.`)) throw new Error('Invalid OAuth state');
    const t = await xeroLive.handleCallback(code);
    run('DELETE FROM connections WHERE business_id=? AND provider=?', [b.id, 'xero']);
    insert('connections', {
      business_id: b.id, provider: 'xero', status: 'connected', tenant_id: t.tenantId, tenant_name: t.tenantName,
      access_token_enc: encrypt(t.accessToken), refresh_token_enc: encrypt(t.refreshToken), token_expires_at: t.expiresAt, connected_at: now(),
    });
    audit(b.id, `user:${req.user.id}`, 'xero.connected', 'connection', null, { tenant: t.tenantName });
    const stats = await fullSync(b);
    res.flash('ok', `Connected to ${t.tenantName}. Imported ${stats.contacts} contacts and ${stats.invoices} invoices.`);
  } catch (e) {
    res.flash('err', `Xero connection failed: ${e.message}`);
  }
  res.redirect('/app');
});

router.post('/xero/sync', async (req, res) => {
  try {
    const stats = await fullSync(req.business, { notify: req.body.notify === '1' });
    res.flash('ok', `Synced ${stats.contacts} contacts and ${stats.invoices} invoices from Xero.`);
  } catch (e) { res.flash('err', `Sync failed: ${e.message}`); }
  res.redirect(req.get('referer') || '/app');
});

router.post('/xero/disconnect', (req, res) => {
  run('DELETE FROM connections WHERE business_id=? AND provider=?', [req.business.id, 'xero']);
  audit(req.business.id, `user:${req.user.id}`, 'xero.disconnected', 'connection', null, null);
  res.flash('info', 'Xero disconnected. Existing invoices and customers are kept.');
  res.redirect('/app');
});

// ---------------- Gateway connection ----------------
router.get('/gateway', (req, res) => {
  const gw = gatewayConnection(req.business.id);
  res.send(page(req, {
    title: 'NAB gateway', active: 'overview', body: `
    <div class="grid c2"><div class="card">
      <h2>${gw ? 'Update' : 'Add'} gateway credentials</h2>
      <p class="small muted">These are stored encrypted (AES-256-GCM) and only ever sent to NAB. Your customers' card numbers are entered on NAB's hosted page and never reach ${esc(config.appName)}; we keep only the card token NAB returns.</p>
      <form method="post" action="/app/gateway">
        ${field('Gateway', 'gateway_kind', { options: [['nab_transact', 'NAB Transact'], ...(isDemo() ? [['mock', 'Mock gateway (demo)']] : [])], value: gw?.gateway_kind || (isDemo() ? 'mock' : 'nab_transact') })}
        ${field('Merchant ID', 'merchant_id', { required: true, value: gw?.merchant_id || (isDemo() ? 'DEMO0001' : ''), placeholder: 'e.g. ABC0001' })}
        ${field('Transaction password', 'transaction_password', { type: 'password', placeholder: gw ? 'Leave blank to keep current' : '', help: 'From the NAB Transact integration pack (SecureXML password)' })}
        ${field('Hosted payment page password (if different)', 'hpp_password', { type: 'password', placeholder: gw ? 'Leave blank to keep current' : 'Optional' })}
        ${field('Environment', 'environment', { options: [['test', 'Test'], ['live', 'Live']], value: gw?.environment || 'test' })}
        <div class="row"><button class="btn">Save and verify</button>${gw ? '<a class="btn secondary" href="/app">Back</a>' : ''}</div>
      </form>
    </div>
    <div class="card"><h3>What NAB needs to give you</h3>
      <ul class="small">
        <li>Merchant ID and SecureXML transaction password (server-to-server API)</li>
        <li>Hosted Payment Page enabled, with the fingerprint password</li>
        <li>Stored card / Periodic payments enabled on the facility (needed for autopay)</li>
        <li>Refunds via API enabled</li>
        <li>Test merchant credentials for the test environment</li>
      </ul>
      <h3>Settlement</h3><p class="small">NAB settles card takings to your NAB business account. Merchant fees are billed separately by NAB, so payments can be recorded in Xero at face value against your bank account or a clearing account (see Settings).</p>
      ${gw ? `<h3>Status</h3><p>${badge(gw.status)} ${esc(gw.gateway_kind)} · ${esc(gw.merchant_id)} · ${esc(gw.environment)}</p><form method="post" action="/app/gateway/verify"><button class="btn sm secondary">Re-test connection</button></form>` : ''}
    </div></div>`,
  }));
});

router.post('/gateway', async (req, res) => {
  const b = req.business; const existing = gatewayConnection(b.id);
  const { gateway_kind, merchant_id, transaction_password, hpp_password, environment } = req.body;
  let creds = existing ? JSON.parse((await import('../crypto.js')).decrypt(existing.credentials_enc) || '{}') : {};
  if (transaction_password) creds.transaction_password = transaction_password;
  if (hpp_password) creds.hpp_password = hpp_password;
  if (gateway_kind === 'mock' && !creds.transaction_password) creds.transaction_password = 'demo';
  if (!creds.transaction_password) { res.flash('err', 'Transaction password is required.'); return res.redirect('/app/gateway'); }
  const fields = { gateway_kind, merchant_id, credentials_enc: encrypt(JSON.stringify(creds)), environment, status: 'connected', connected_at: now() };
  if (existing) update('connections', existing.id, fields); else insert('connections', { business_id: b.id, provider: 'gateway', ...fields });
  audit(b.id, `user:${req.user.id}`, 'gateway.saved', 'connection', null, { gateway_kind, merchant_id, environment });
  try {
    const v = await gatewayClient(gatewayConnection(b.id)).verifyCredentials();
    res.flash(v.ok ? 'ok' : 'err', v.ok ? `Gateway connected: ${v.message}` : `Saved, but verification failed: ${v.message}`);
  } catch (e) { res.flash('err', `Saved, but verification failed: ${e.message}`); }
  res.redirect('/app');
});

router.post('/gateway/verify', async (req, res) => {
  try { const v = await gatewayClient(gatewayConnection(req.business.id)).verifyCredentials(); res.flash(v.ok ? 'ok' : 'err', v.message); }
  catch (e) { res.flash('err', e.message); }
  res.redirect('/app/gateway');
});

// ---------------- Invoices ----------------
router.get('/invoices', (req, res) => {
  const f = req.query.f || 'open';
  const where = { open: "i.status='AUTHORISED' AND i.amount_due>0", overdue: `i.status='AUTHORISED' AND i.amount_due>0 AND i.due_date<'${today()}'`, paid: "i.status='PAID'", all: '1=1' }[f] || '1=1';
  const rows = all(`SELECT i.*, c.name cname, c.autopay_enabled FROM invoices i LEFT JOIN customers c ON c.id=i.customer_id WHERE i.business_id=? AND ${where} ORDER BY i.due_date DESC, i.id DESC LIMIT 300`, [req.business.id]);
  res.send(page(req, {
    title: 'Invoices', active: 'invoices', body: `
    <div class="tabs">${['open', 'overdue', 'paid', 'all'].map((k) => `<a href="?f=${k}" class="${f === k ? 'on' : ''}">${k[0].toUpperCase() + k.slice(1)}</a>`).join('')}</div>
    ${table(['Invoice', 'Customer', 'Issued', 'Due', 'Total', 'Due', 'Status', 'Autopay'], rows.map((i) => [
      `<a href="/app/invoices/${i.id}">${esc(i.number)}</a>${i.repeating_invoice_id ? ' <span class="badge grey">repeating</span>' : ''}`, esc(i.cname || '—'), date(i.issue_date), date(i.due_date),
      money(i.total, i.currency), money(i.amount_due, i.currency), badge(i.status),
      i.autopay_next_attempt_at ? `<span class="badge amber">${date(i.autopay_next_attempt_at)}</span>` : i.autopay_last_error ? '<span class="badge red">failed</span>' : (i.autopay_enabled ? '<span class="badge grey">on</span>' : ''),
    ]), 'No invoices in this view. Invoices arrive from Xero via webhook or Sync now.')}`,
  }));
});

router.get('/invoices/:id', (req, res) => {
  const i = get('SELECT * FROM invoices WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  if (!i) return res.status(404).send('Not found');
  const c = i.customer_id ? get('SELECT * FROM customers WHERE id=?', [i.customer_id]) : null;
  const pays = all('SELECT * FROM payments WHERE invoice_id=? ORDER BY id DESC', [i.id]);
  const lines = JSON.parse(i.line_items_json || '[]');
  const pm = c?.autopay_payment_method_id ? get('SELECT * FROM payment_methods WHERE id=?', [c.autopay_payment_method_id]) : null;
  res.send(page(req, {
    title: `Invoice ${i.number}`, active: 'invoices', body: `
    <div class="grid c2"><div>
      <div class="card"><div class="row between"><div><strong>${esc(c?.name || 'No customer')}</strong> ${c ? `<a class="small" href="/app/customers/${c.id}">view</a>` : ''}</div>${badge(i.status)}</div>
      <dl class="kv" style="margin-top:12px"><dt>Issued</dt><dd>${date(i.issue_date)}</dd><dt>Due</dt><dd>${date(i.due_date)}</dd><dt>Reference</dt><dd>${esc(i.reference || '—')}</dd><dt>Xero ID</dt><dd class="mono">${esc(i.xero_invoice_id)}</dd>${i.repeating_invoice_id ? `<dt>Repeating</dt><dd class="mono">${esc(i.repeating_invoice_id)}</dd>` : ''}</dl>
      <table class="invoice-lines" style="margin-top:12px"><thead><tr><th>Description</th><th class="num">Qty</th><th class="num">Unit</th><th class="num">Amount</th></tr></thead><tbody>
      ${lines.map((l) => `<tr><td>${esc(l.description)}</td><td class="num">${esc(l.quantity)}</td><td class="num">${money(l.unit_amount, i.currency)}</td><td class="num">${money(l.line_amount, i.currency)}</td></tr>`).join('')}
      <tr><td colspan="3" class="num">Subtotal</td><td class="num">${money(i.subtotal, i.currency)}</td></tr><tr><td colspan="3" class="num">GST</td><td class="num">${money(i.tax, i.currency)}</td></tr>
      <tr class="total-row"><td colspan="3" class="num">Total</td><td class="num">${money(i.total, i.currency)}</td></tr><tr class="total-row"><td colspan="3" class="num">Amount due</td><td class="num">${money(i.amount_due, i.currency)}</td></tr></tbody></table></div>
      <h2>Payments</h2>${table(['When', 'Source', 'Amount', 'Gateway ref', 'Result', 'Xero'], pays.map((p) => [datetime(p.created_at), esc(p.source), money(p.amount, p.currency), `<span class="mono">${esc(p.gateway_txn_id || '')}</span>`, `${badge(p.status)} <span class="small muted">${esc(p.gateway_code)} ${esc(p.gateway_message)}</span>`, badge(p.xero_writeback_status)]))}
    </div><div>
      <div class="card"><h3>Actions</h3>
        ${i.status === 'AUTHORISED' && i.amount_due > 0 ? `
        <p class="small">Pay link: <a class="mono" href="${payLinkUrl(i)}" target="_blank">${payLinkUrl(i)}</a></p>
        <div class="row">
          <form method="post" action="/app/invoices/${i.id}/send"><button class="btn sm" ${c?.email ? '' : 'disabled'}>Email pay link</button></form>
          <form method="post" action="/app/invoices/${i.id}/charge"><button class="btn sm secondary" ${pm ? '' : 'disabled'} onclick="return confirm('Charge ${esc(c?.name)}\\'s saved card ${pm ? pm.last4 : ''} for ${money(i.amount_due)}?')">Charge saved card now</button></form>
        </div>
        ${!c?.email ? '<p class="small muted">Customer has no email address. Add one on the customer page.</p>' : ''}
        ${i.pay_link_sent_at ? `<p class="small muted">Pay link last sent ${datetime(i.pay_link_sent_at)}</p>` : ''}
        ${i.autopay_next_attempt_at ? `<div class="notice">Autopay scheduled for ${date(i.autopay_next_attempt_at)} (attempt ${i.autopay_attempts + 1}). <form class="inline" method="post" action="/app/invoices/${i.id}/cancel-autopay"><button class="link">Cancel</button></form></div>` : ''}
        ${i.autopay_last_error ? `<div class="callout">Last autopay error: ${esc(i.autopay_last_error)}</div>` : ''}`
      : '<p class="muted small">This invoice is not payable (paid, voided or draft).</p>'}
      </div>
    </div></div>`,
  }));
});

router.post('/invoices/:id/send', (req, res) => {
  const i = get('SELECT * FROM invoices WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  const c = get('SELECT * FROM customers WHERE id=?', [i.customer_id]);
  if (c?.email) { sendPayLink(req.business, c, i); res.flash('ok', `Pay link emailed to ${c.email}.`); } else res.flash('err', 'Customer has no email.');
  res.redirect(`/app/invoices/${i.id}`);
});

router.post('/invoices/:id/charge', async (req, res) => {
  const i = get('SELECT * FROM invoices WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  try {
    const r = await chargeInvoiceWithSavedCard(req.business, i, { source: 'manual' });
    res.flash(r.approved ? 'ok' : 'err', r.approved ? `Charged ${money(i.amount_due)}: ${r.message}` : `Declined: ${r.message}`);
  } catch (e) { res.flash('err', e.message); }
  res.redirect(`/app/invoices/${i.id}`);
});

router.post('/invoices/:id/cancel-autopay', (req, res) => {
  const i = get('SELECT * FROM invoices WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  update('invoices', i.id, { autopay_scheduled_for: null, autopay_next_attempt_at: null });
  audit(req.business.id, `user:${req.user.id}`, 'invoice.autopay_cancelled', 'invoice', i.id, null);
  res.redirect(`/app/invoices/${i.id}`);
});

// ---------------- Customers ----------------
router.get('/customers', (req, res) => {
  const rows = all(`SELECT c.*, (SELECT COUNT(*) FROM invoices i WHERE i.customer_id=c.id AND i.status='AUTHORISED' AND i.amount_due>0) open_n,
    (SELECT COALESCE(SUM(amount_due),0) FROM invoices i WHERE i.customer_id=c.id AND i.status='AUTHORISED') open_v,
    (SELECT COUNT(*) FROM payment_methods m WHERE m.customer_id=c.id AND m.status='active') cards
    FROM customers c WHERE c.business_id=? ORDER BY c.name`, [req.business.id]);
  res.send(page(req, {
    title: 'Customers', active: 'customers', body: table(['Customer', 'Email', 'Portal', 'Autopay', 'Saved cards', 'Open invoices'], rows.map((c) => [
      `<a href="/app/customers/${c.id}">${esc(c.name)}</a>`, esc(c.email || '—'), badge(c.portal_status), c.autopay_enabled ? '<span class="badge green">on</span>' : '<span class="badge grey">off</span>', String(c.cards), `${c.open_n} (${money(c.open_v)})`,
    ]), 'No customers yet. They are created automatically from Xero contacts.'),
  }));
});

router.get('/customers/:id', (req, res) => {
  const c = get('SELECT * FROM customers WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  if (!c) return res.status(404).send('Not found');
  const invs = all('SELECT * FROM invoices WHERE customer_id=? ORDER BY issue_date DESC LIMIT 50', [c.id]);
  const cards = all("SELECT * FROM payment_methods WHERE customer_id=? AND status='active' ORDER BY is_default DESC, id DESC", [c.id]);
  const pays = all('SELECT p.*, i.number FROM payments p LEFT JOIN invoices i ON i.id=p.invoice_id WHERE p.customer_id=? ORDER BY p.id DESC LIMIT 20', [c.id]);
  res.send(page(req, {
    title: c.name, active: 'customers', body: `
    <div class="grid c2"><div>
      <div class="card"><h3>Details</h3>
        <form method="post" action="/app/customers/${c.id}">
          ${field('Email', 'email', { type: 'email', value: c.email || '', help: 'Used for pay links, portal invites and receipts. Changing it here does not change Xero.' })}
          ${field('Phone', 'phone', { value: c.phone || '' })}
          <button class="btn sm">Save</button>
        </form>
        <dl class="kv" style="margin-top:14px"><dt>Xero contact</dt><dd class="mono">${esc(c.xero_contact_id)}</dd><dt>Portal</dt><dd>${badge(c.portal_status)} ${c.last_login_at ? `last login ${datetime(c.last_login_at)}` : ''}</dd></dl>
        <div class="row" style="margin-top:10px">
          <form method="post" action="/app/customers/${c.id}/invite"><button class="btn sm secondary" ${c.email ? '' : 'disabled'}>${c.portal_status === 'none' ? 'Send portal invite' : 'Re-send portal link'}</button></form>
        </div>
      </div>
      <div class="card"><h3>Autopay</h3>
        <form method="post" action="/app/customers/${c.id}/autopay">
          <label class="check"><input type="checkbox" name="autopay_enabled" value="1" ${c.autopay_enabled ? 'checked' : ''} ${cards.length ? '' : 'disabled'}> <span>Automatically charge the saved card for new Xero invoices${cards.length ? '' : ' (needs a saved card; the customer adds one through the portal or pay page)'}</span></label>
          ${field('When to charge', 'autopay_timing', { options: [['', `Business default (${settings(req.business).autopay_default_timing.replace('_', ' ')})`], ['on_issue', 'As soon as the invoice is issued'], ['due_date', 'On the due date'], ['days_before', 'A few days before the due date']], value: c.autopay_timing || '' })}
          ${field('Days before due (if applicable)', 'autopay_days_before', { type: 'number', value: c.autopay_days_before || 3 })}
          ${cards.length > 1 ? field('Card to use', 'autopay_payment_method_id', { options: cards.map((m) => [m.id, `${m.card_brand} •••• ${m.last4} (${m.expiry_month}/${m.expiry_year})`]), value: c.autopay_payment_method_id || cards[0]?.id }) : ''}
          <button class="btn sm">Save autopay</button>
        </form>
        <p class="small muted" style="margin-top:10px">Customers can also manage this themselves in the portal. A customer's own choice always wins.</p>
      </div>
    </div><div>
      <div class="card"><h3>Saved cards</h3>
        ${cards.length ? cards.map((m) => `<div class="row between" style="padding:6px 0;border-bottom:1px solid var(--line)"><span>${esc(m.card_brand)} •••• ${esc(m.last4)} <span class="muted small">exp ${m.expiry_month}/${m.expiry_year}</span> ${m.id === c.autopay_payment_method_id ? '<span class="badge green">autopay</span>' : ''}</span><form method="post" action="/app/customers/${c.id}/cards/${m.id}/remove"><button class="link small">Remove</button></form></div>`).join('') : '<p class="muted small">None. Card tokens are created when the customer ticks "save card" on the pay page or adds one in the portal.</p>'}
      </div>
      <h2>Invoices</h2>${table(['Invoice', 'Due', 'Amount due', 'Status'], invs.map((i) => [`<a href="/app/invoices/${i.id}">${esc(i.number)}</a>`, date(i.due_date), money(i.amount_due, i.currency), badge(i.status)]))}
      <h2>Payments</h2>${table(['When', 'Invoice', 'Amount', 'Status'], pays.map((p) => [datetime(p.created_at), esc(p.number), money(p.amount, p.currency), badge(p.status)]))}
    </div></div>`,
  }));
});

router.post('/customers/:id', (req, res) => {
  const c = get('SELECT * FROM customers WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  update('customers', c.id, { email: req.body.email || null, phone: req.body.phone || null, updated_at: now() });
  res.flash('ok', 'Customer updated.'); res.redirect(`/app/customers/${c.id}`);
});
router.post('/customers/:id/invite', (req, res) => {
  const c = get('SELECT * FROM customers WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  if (c.email) { (c.portal_status === 'none' ? sendPortalInvite : sendMagicLink)(req.business, c); res.flash('ok', `Portal link sent to ${c.email}.`); }
  res.redirect(`/app/customers/${c.id}`);
});
router.post('/customers/:id/autopay', (req, res) => {
  const c = get('SELECT * FROM customers WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  const card = req.body.autopay_payment_method_id ? get('SELECT * FROM payment_methods WHERE id=? AND customer_id=?', [req.body.autopay_payment_method_id, c.id]) : get("SELECT * FROM payment_methods WHERE customer_id=? AND status='active' ORDER BY is_default DESC, id DESC", [c.id]);
  const enabled = req.body.autopay_enabled === '1' && !!card;
  update('customers', c.id, { autopay_enabled: enabled ? 1 : 0, autopay_timing: req.body.autopay_timing || null, autopay_days_before: Number(req.body.autopay_days_before || 0), autopay_payment_method_id: card?.id || null, updated_at: now() });
  audit(req.business.id, `user:${req.user.id}`, enabled ? 'customer.autopay_enabled' : 'customer.autopay_disabled', 'customer', c.id, null);
  if (!enabled) run('UPDATE invoices SET autopay_scheduled_for=NULL, autopay_next_attempt_at=NULL WHERE customer_id=?', [c.id]);
  res.flash('ok', 'Autopay settings saved.'); res.redirect(`/app/customers/${c.id}`);
});
router.post('/customers/:id/cards/:mid/remove', (req, res) => {
  const c = get('SELECT * FROM customers WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  update('payment_methods', Number(req.params.mid), { status: 'removed' });
  if (c.autopay_payment_method_id === Number(req.params.mid)) { update('customers', c.id, { autopay_payment_method_id: null, autopay_enabled: 0 }); run('UPDATE invoices SET autopay_next_attempt_at=NULL WHERE customer_id=?', [c.id]); }
  res.flash('ok', 'Card removed.'); res.redirect(`/app/customers/${c.id}`);
});

// ---------------- Payments ----------------
router.get('/payments', (req, res) => {
  const rows = all('SELECT p.*, i.number, c.name cname FROM payments p LEFT JOIN invoices i ON i.id=p.invoice_id LEFT JOIN customers c ON c.id=p.customer_id WHERE p.business_id=? ORDER BY p.id DESC LIMIT 300', [req.business.id]);
  res.send(page(req, {
    title: 'Payments', active: 'payments', body: table(['When', 'Customer', 'Invoice', 'Source', 'Amount', 'Result', 'Gateway ref', 'Xero', ''], rows.map((p) => [
      datetime(p.created_at), esc(p.cname), `<a href="/app/invoices/${p.invoice_id}">${esc(p.number)}</a>`, esc(p.source), money(p.amount, p.currency),
      `${badge(p.status)}<div class="small muted">${esc(p.gateway_code)} ${esc(p.gateway_message)}</div>`, `<span class="mono">${esc(p.gateway_txn_id || '')}</span>`,
      `${badge(p.xero_writeback_status)}${p.xero_writeback_error ? `<div class="small muted">${esc(p.xero_writeback_error)}</div>` : ''}`,
      p.status === 'succeeded' ? `<form method="post" action="/app/payments/${p.id}/refund" onsubmit="return confirm('Refund ${money(p.amount)} to the customer\\'s card?')"><button class="btn sm secondary">Refund</button></form>` : '',
    ]), 'No payments yet.'),
  }));
});

router.post('/payments/:id/refund', async (req, res) => {
  const p = get('SELECT * FROM payments WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  try {
    const r = await refundPayment(req.business, p, p.amount);
    res.flash(r.approved ? 'ok' : 'err', r.approved ? `Refunded ${money(p.amount)}. Remember to record the refund in Xero (manual step for now).` : `Refund failed: ${r.message}`);
  } catch (e) { res.flash('err', e.message); }
  res.redirect('/app/payments');
});

// ---------------- Autopay ----------------
router.get('/autopay', (req, res) => {
  const sched = all("SELECT i.*, c.name cname FROM invoices i JOIN customers c ON c.id=i.customer_id WHERE i.business_id=? AND i.autopay_next_attempt_at IS NOT NULL AND i.status='AUTHORISED' ORDER BY i.autopay_next_attempt_at", [req.business.id]);
  const failed = all("SELECT i.*, c.name cname FROM invoices i JOIN customers c ON c.id=i.customer_id WHERE i.business_id=? AND i.autopay_last_error IS NOT NULL AND i.autopay_next_attempt_at IS NULL AND i.status='AUTHORISED' AND i.amount_due>0 ORDER BY i.updated_at DESC", [req.business.id]);
  const cust = all('SELECT c.*, m.card_brand, m.last4 FROM customers c LEFT JOIN payment_methods m ON m.id=c.autopay_payment_method_id WHERE c.business_id=? AND c.autopay_enabled=1 ORDER BY c.name', [req.business.id]);
  res.send(page(req, {
    title: 'Autopay', active: 'autopay', body: `
    <p class="muted small">The scheduler runs every ${Math.round(config.jobIntervalMs / 1000)} seconds and charges any invoice whose scheduled time has passed. Failed charges retry every ${config.autopay.retryDays} days up to ${config.autopay.maxAttempts} attempts, then stop and notify both parties.</p>
    ${isDemo() ? '<form method="post" action="/app/autopay/run"><button class="btn sm">Run scheduler now (demo)</button> <label class="small muted"><input type="checkbox" name="ignore_schedule" value="1"> ignore scheduled dates and charge everything queued</label></form>' : ''}
    <h2>Scheduled</h2>${table(['Scheduled for', 'Customer', 'Invoice', 'Amount', 'Attempts'], sched.map((i) => [date(i.autopay_next_attempt_at), esc(i.cname), `<a href="/app/invoices/${i.id}">${esc(i.number)}</a>`, money(i.amount_due, i.currency), String(i.autopay_attempts)]), 'Nothing queued.')}
    <h2>Stopped after failures</h2>${table(['Customer', 'Invoice', 'Amount', 'Last error'], failed.map((i) => [esc(i.cname), `<a href="/app/invoices/${i.id}">${esc(i.number)}</a>`, money(i.amount_due, i.currency), esc(i.autopay_last_error)]), 'None.')}
    <h2>Customers on autopay</h2>${table(['Customer', 'Card', 'Timing'], cust.map((c) => [`<a href="/app/customers/${c.id}">${esc(c.name)}</a>`, `${esc(c.card_brand || '')} •••• ${esc(c.last4 || '')}`, esc((c.autopay_timing || 'default').replace('_', ' '))]), 'No customers have enabled autopay yet.')}`,
  }));
});

router.post('/autopay/run', async (req, res) => {
  if (req.body.ignore_schedule === '1') run("UPDATE invoices SET autopay_next_attempt_at=? WHERE business_id=? AND autopay_next_attempt_at IS NOT NULL AND status='AUTHORISED'", [now(), req.business.id]);
  const r = await runAutopay(new Date());
  res.flash('info', r.length ? r.map((x) => `${x.invoice}: ${x.approved ? 'approved' : 'declined'} (${x.message})`).join(' · ') : 'Nothing was due.');
  res.redirect('/app/autopay');
});

// ---------------- Outbox, activity ----------------
router.get('/outbox', (req, res) => {
  const rows = all('SELECT * FROM outbox WHERE business_id=? ORDER BY id DESC LIMIT 100', [req.business.id]);
  res.send(page(req, {
    title: 'Outbox', active: 'outbox', body: `<p class="muted small">Every email the platform sends to your customers. ${isDemo() ? 'In demo mode nothing is delivered; open an email here and click its links to walk the customer journey.' : ''}</p>
    ${table(['When', 'To', 'Subject', 'Type', 'Status', ''], rows.map((m) => [datetime(m.created_at), `${esc(m.to_name)}<div class="small muted">${esc(m.to_email)}</div>`, esc(m.subject), esc(m.kind), badge(m.status), `<a class="btn sm secondary" href="/app/outbox/${m.id}">Open</a>`]), 'No emails yet.')}`,
  }));
});
router.get('/outbox/:id', (req, res) => {
  const m = get('SELECT * FROM outbox WHERE id=? AND business_id=?', [req.params.id, req.business.id]);
  res.send(page(req, { title: m.subject, active: 'outbox', body: `<p class="small muted">To ${esc(m.to_name)} &lt;${esc(m.to_email)}&gt; · ${datetime(m.created_at)}</p><div class="card">${m.body_html}</div><a href="/app/outbox">Back to outbox</a>` }));
});
router.get('/activity', (req, res) => {
  const log = all('SELECT * FROM audit_log WHERE business_id=? ORDER BY id DESC LIMIT 100', [req.business.id]);
  const hooks = all('SELECT * FROM webhook_events WHERE business_id=? ORDER BY id DESC LIMIT 50', [req.business.id]);
  res.send(page(req, {
    title: 'Activity', active: 'activity', body: `
    <h2>Audit log</h2>${table(['When', 'Actor', 'Action', 'Entity', 'Detail'], log.map((l) => [datetime(l.created_at), esc(l.actor), `<code>${esc(l.action)}</code>`, `${esc(l.entity_type || '')} ${esc(l.entity_id || '')}`, `<span class="small mono">${esc(l.detail_json || '')}</span>`]))}
    <h2>Xero webhook events</h2>${table(['Received', 'Event', 'Resource', 'Status', 'Error'], hooks.map((h) => [datetime(h.received_at), `${esc(h.category)}/${esc(h.type)}`, `<span class="mono small">${esc(h.resource_id)}</span>`, badge(h.status), esc(h.error || '')]))}`,
  }));
});

// ---------------- Settings ----------------
router.get('/settings', async (req, res) => {
  const b = req.business; const s = settings(b);
  let accounts = [];
  try { accounts = await xeroClient(xeroConnection(b.id)).accounts(); } catch { /* not connected */ }
  const payNowUrl = `${config.baseUrl}/x/${b.short_code}/pay?inv=[INVOICENUMBER]&amt=[AMOUNTDUE]&cur=[CURRENCY]&org=[SHORTCODE]`;
  res.send(page(req, {
    title: 'Settings', active: 'settings', body: `
    <div class="grid c2"><div>
      <form method="post" action="/app/settings" class="card"><h3>Business and branding</h3>
        ${field('Business name', 'name', { value: b.name, required: true })}
        ${field('Notification email', 'email', { type: 'email', value: b.email || '', help: 'Where we send alerts (failed autopay, Xero write-back problems)' })}
        ${field('Phone', 'phone', { value: b.phone || '' })}${field('ABN', 'abn', { value: b.abn || '' })}
        ${field('Brand colour', 'brand_colour', { type: 'color', value: b.brand_colour })}
        ${field('Logo URL', 'logo_url', { value: b.logo_url || '' })}
        ${field('Portal welcome text', 'portal_welcome', { type: 'textarea', value: s.portal_welcome })}
        <h3>Autopay defaults</h3>
        <label class="check"><input type="checkbox" name="autopay_allowed" value="1" ${s.autopay_allowed ? 'checked' : ''}> <span>Let customers save a card and enable autopay</span></label>
        ${field('Default timing', 'autopay_default_timing', { options: [['on_issue', 'As soon as the invoice is issued'], ['due_date', 'On the due date'], ['days_before', 'A few days before the due date']], value: s.autopay_default_timing })}
        ${field('Days before due', 'autopay_days_before', { type: 'number', value: s.autopay_days_before })}
        <h3>Emails</h3>
        <label class="check"><input type="checkbox" name="send_pay_link_on_invoice" value="1" ${s.send_pay_link_on_invoice ? 'checked' : ''}> <span>Email a pay link when a new Xero invoice is issued (skipped for customers on autopay)</span></label>
        <label class="check"><input type="checkbox" name="send_receipts" value="1" ${s.send_receipts ? 'checked' : ''}> <span>Email receipts after successful card payments</span></label>
        <h3>Xero</h3>
        ${field('Record payments against account', 'xero_payment_account_code', { options: accounts.length ? accounts.map((a) => [a.Code, `${a.Code} ${a.Name}`]) : [[s.xero_payment_account_code, s.xero_payment_account_code]], value: s.xero_payment_account_code, help: 'NAB settles gross and bills fees separately, so your bank account works. A "NAB Transact Clearing" account makes bank reconciliation cleaner if settlements are batched.' })}
        <label class="check"><input type="checkbox" name="xero_paynow_configured" value="1" ${s.xero_paynow_configured ? 'checked' : ''}> <span>I have added the Pay Now URL in Xero (below)</span></label>
        <h3>Surcharges</h3>
        <p class="small muted">Card surcharges on Visa, Mastercard and eftpos are banned in Australia from 1 October 2026, so none are applied. American Express is outside the ban; if NAB enables Amex on your facility you may set a cost-recovery surcharge for Amex only.</p>
        ${field('Amex surcharge %', 'amex_surcharge_pct', { type: 'number', value: s.amex_surcharge_pct, step: '0.01' })}
        <button class="btn">Save settings</button>
      </form>
    </div><div>
      <div class="card" id="paynow"><h3>Pay Now button on Xero invoices</h3>
        <p class="small">In Xero go to <strong>Settings → Payment services → Add payment service → Custom payment URL</strong>, paste this URL, then assign it to your invoice branding theme. Xero fills in the placeholders when a customer clicks Pay Now on the online invoice.</p>
        <pre>${esc(payNowUrl)}</pre>
        <p class="small muted">Your business code is <code>${esc(b.short_code)}</code>. The placeholders in square brackets are Xero's and must stay exactly as shown.</p>
      </div>
      <div class="card"><h3>Xero webhook</h3>
        <p class="small">Registered once for the whole platform in the Xero developer portal (not per business): <code>${esc(config.baseUrl)}/webhooks/xero</code>, topics <strong>Contacts</strong> and <strong>Invoices</strong>. ${config.xero.webhookKey ? 'Webhook key is configured.' : '<span class="badge amber">XERO_WEBHOOK_KEY not set</span>'}</p>
        <p class="small">Customers are matched to Xero contacts; invoices created in Xero (including ones generated by repeating invoices) arrive here within seconds.</p>
      </div>
      <div class="card"><h3>Customer portal</h3><p class="small">Customers sign in at <code>${esc(config.baseUrl)}/portal</code> with a magic link sent to the email on their Xero contact. No passwords to support.</p></div>
    </div></div>`,
  }));
});

router.post('/settings', (req, res) => {
  const b = req.business; const s = settings(b); const f = req.body;
  const merged = {
    ...s, portal_welcome: f.portal_welcome, autopay_allowed: f.autopay_allowed === '1', autopay_default_timing: f.autopay_default_timing,
    autopay_days_before: Number(f.autopay_days_before || 0), send_pay_link_on_invoice: f.send_pay_link_on_invoice === '1', send_receipts: f.send_receipts === '1',
    xero_payment_account_code: f.xero_payment_account_code, xero_paynow_configured: f.xero_paynow_configured === '1', amex_surcharge_pct: Number(f.amex_surcharge_pct || 0),
  };
  update('businesses', b.id, { name: f.name, email: f.email || null, phone: f.phone || null, abn: f.abn || null, brand_colour: f.brand_colour || b.brand_colour, logo_url: f.logo_url || null, settings_json: JSON.stringify(merged) });
  audit(b.id, `user:${req.user.id}`, 'settings.updated', 'business', b.id, null);
  res.flash('ok', 'Settings saved.'); res.redirect('/app/settings');
});
