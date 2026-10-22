// Customer portal: magic-link sign in, invoices, pay, saved cards, autopay.
import { Router } from 'express';
import { config, isDemo } from '../config.js';
import { all, audit, get, now, run, settings, update } from '../db.js';
import { sign, verifySigned } from '../crypto.js';
import { endSession, requireCustomer, startSession } from '../auth.js';
import { badge, date, datetime, esc, field, money, portalPage, table } from '../layout.js';
import { gatewayClient, gatewayConnection } from '../providers/index.js';
import { sendMagicLink } from '../services/notifications.js';
import { savePaymentMethod } from '../services/payments.js';

export const router = Router();

router.get('/', (req, res, next) => {
  if (req.customer) return next();
  const biz = req.query.biz ? get('SELECT * FROM businesses WHERE slug=?', [req.query.biz]) : null;
  res.send(portalPage({
    title: 'Customer portal', business: biz, flash: req.flash, body: `
    <div class="card" style="max-width:480px"><h3>Sign in with your email</h3>
    <p class="small muted">Enter the email address your invoices are sent to and we will email you a secure sign-in link. No password needed.</p>
    <form method="post" action="/portal/request-link">${biz ? `<input type="hidden" name="biz" value="${esc(biz.slug)}">` : ''}${field('Email', 'email', { type: 'email', required: true })}<button class="btn">Email me a sign-in link</button></form></div>`,
  }));
});

router.post('/request-link', (req, res) => {
  const email = String(req.body.email || '').trim().toLowerCase();
  const matches = all('SELECT c.*, b.name bname FROM customers c JOIN businesses b ON b.id=c.business_id WHERE lower(c.email)=?', [email]);
  const links = [];
  for (const c of matches) {
    const business = get('SELECT * FROM businesses WHERE id=?', [c.business_id]);
    const id = sendMagicLink(business, c);
    links.push({ c, id });
  }
  // Always say the same thing so the form does not reveal who is a customer.
  let msg = 'If that email is on file, a sign-in link is on its way.';
  if (isDemo() && links.length) {
    const urls = links.map(({ id, c }) => { const m = get('SELECT body_html FROM outbox WHERE id=?', [id]); const u = (m.body_html.match(/href="([^"]+\/portal\/login\/[^"]+)"/) || [])[1]; return `${c.bname}: ${u}`; });
    msg += ` Demo shortcut: ${urls.join(' | ')}`;
  }
  res.flash('info', msg); res.redirect('/portal');
});

router.get('/login/:token', (req, res) => {
  const ml = get('SELECT * FROM magic_links WHERE token=? AND used_at IS NULL AND expires_at>?', [req.params.token, now()]);
  if (!ml) { res.flash('err', 'That sign-in link has expired or was already used. Request a new one.'); return res.redirect('/portal'); }
  update('magic_links', ml.id, { used_at: now() });
  const c = get('SELECT * FROM customers WHERE id=?', [ml.customer_id]);
  update('customers', c.id, { portal_status: 'active', last_login_at: now() });
  audit(c.business_id, `customer:${c.id}`, 'portal.login', 'customer', c.id, null);
  startSession(res, 'customer', c.id);
  res.redirect('/portal');
});

router.post('/logout', (req, res) => { endSession(req, res, 'customer'); res.redirect('/portal'); });

router.use(requireCustomer);
const page = (req, opts) => portalPage({ business: req.customerBusiness, customer: req.customer, flash: req.flash, ...opts });

router.get('/', (req, res) => {
  const c = req.customer; const b = req.customerBusiness;
  const open = all("SELECT * FROM invoices WHERE customer_id=? AND status='AUTHORISED' AND amount_due>0 ORDER BY due_date", [c.id]);
  const recent = all("SELECT * FROM invoices WHERE customer_id=? AND status IN ('PAID','VOIDED') ORDER BY updated_at DESC LIMIT 10", [c.id]);
  const pm = c.autopay_payment_method_id ? get('SELECT * FROM payment_methods WHERE id=?', [c.autopay_payment_method_id]) : null;
  const totalDue = open.reduce((s, i) => s + i.amount_due, 0);
  res.send(page(req, {
    title: `Hi ${c.name.split(' ')[0]}`, active: 'invoices', body: `
    <div class="grid c3"><div class="stat"><div class="stat-v">${money(totalDue)}</div><div class="stat-l">Outstanding across ${open.length} invoice${open.length === 1 ? '' : 's'}</div></div>
    <div class="stat"><div class="stat-v">${c.autopay_enabled ? 'On' : 'Off'}</div><div class="stat-l">Automatic payments${pm ? ` · ${esc(pm.card_brand)} •••• ${esc(pm.last4)}` : ''}</div><a class="small" href="/portal/autopay">Manage</a></div>
    <div class="stat"><div class="stat-v">${esc(b.name)}</div><div class="stat-l">${esc(settings(b).portal_welcome)}</div></div></div>
    <h2>Invoices awaiting payment</h2>
    ${table(['Invoice', 'Issued', 'Due', 'Amount due', ''], open.map((i) => [esc(i.number) + (i.reference ? `<div class="small muted">${esc(i.reference)}</div>` : ''), date(i.issue_date), `${date(i.due_date)}${i.due_date < now().slice(0, 10) ? ' <span class="badge red">overdue</span>' : ''}`, money(i.amount_due, i.currency),
      i.autopay_next_attempt_at ? `<span class="badge amber">auto-pay ${date(i.autopay_next_attempt_at)}</span> <a class="small" href="/pay/${i.pay_token}?src=portal">pay now instead</a>` : `<a class="btn sm" href="/pay/${i.pay_token}?src=portal">Pay now</a>`]), 'You are all paid up.')}
    <h2>Recent</h2>${table(['Invoice', 'Issued', 'Total', 'Status'], recent.map((i) => [esc(i.number), date(i.issue_date), money(i.total, i.currency), badge(i.status)]), 'No history yet.')}`,
  }));
});

router.get('/payments', (req, res) => {
  const rows = all('SELECT p.*, i.number FROM payments p LEFT JOIN invoices i ON i.id=p.invoice_id WHERE p.customer_id=? ORDER BY p.id DESC', [req.customer.id]);
  res.send(page(req, { title: 'Payment history', active: 'payments', body: table(['When', 'Invoice', 'Amount', 'How', 'Result', 'Reference'], rows.map((p) => [datetime(p.created_at), esc(p.number), money(p.amount, p.currency), esc(p.source === 'autopay' ? 'Automatic' : 'Card'), badge(p.status), `<span class="mono">${esc(p.gateway_txn_id || '')}</span>`]), 'No payments yet.') }));
});

router.get('/autopay', (req, res) => {
  const c = req.customer; const b = req.customerBusiness; const s = settings(b);
  const cards = all("SELECT * FROM payment_methods WHERE customer_id=? AND status='active' ORDER BY is_default DESC, id DESC", [c.id]);
  res.send(page(req, {
    title: 'Automatic payments and cards', active: 'autopay', body: `
    ${!s.autopay_allowed ? `<div class="notice">${esc(b.name)} has not enabled automatic payments.</div>` : ''}
    <div class="grid c2"><div class="card"><h3>Automatic payments</h3>
      <p class="small muted">When ${esc(b.name)} issues an invoice in Xero, we charge your saved card for the amount due at the time you choose, and email you a receipt. Cancel any time.</p>
      <form method="post" action="/portal/autopay">
        <label class="check"><input type="checkbox" name="autopay_enabled" value="1" ${c.autopay_enabled ? 'checked' : ''} ${cards.length && s.autopay_allowed ? '' : 'disabled'}> <span><strong>Pay my invoices automatically</strong></span></label>
        ${field('When', 'autopay_timing', { options: [['due_date', 'On the due date'], ['on_issue', 'As soon as the invoice is issued'], ['days_before', 'A few days before the due date']], value: c.autopay_timing || s.autopay_default_timing })}
        ${field('Days before due date', 'autopay_days_before', { type: 'number', value: c.autopay_days_before || s.autopay_days_before })}
        ${cards.length ? field('Card to charge', 'autopay_payment_method_id', { options: cards.map((m) => [m.id, `${m.card_brand} •••• ${m.last4} (exp ${m.expiry_month}/${m.expiry_year})`]), value: c.autopay_payment_method_id || cards[0].id }) : '<p class="small muted">Add a card first.</p>'}
        <button class="btn" ${cards.length ? '' : 'disabled'}>Save</button>
      </form></div>
    <div class="card"><h3>Saved cards</h3>
      ${cards.length ? cards.map((m) => `<div class="row between" style="padding:8px 0;border-bottom:1px solid var(--line)"><span>${esc(m.card_brand)} •••• ${esc(m.last4)} <span class="muted small">exp ${m.expiry_month}/${m.expiry_year}</span></span><form method="post" action="/portal/cards/${m.id}/remove" onsubmit="return confirm('Remove this card?')"><button class="link small">Remove</button></form></div>`).join('') : '<p class="muted small">No saved cards.</p>'}
      <p class="small muted" style="margin-top:10px">Cards are stored by NAB, not by ${esc(b.name)} or ${esc(config.appName)}. We only keep the last four digits and a reference token.</p>
      <form method="post" action="/portal/cards/add"><button class="btn secondary sm" ${s.autopay_allowed && gatewayConnection(b.id) ? '' : 'disabled'}>Add a card</button></form>
      <p class="small muted">You will be taken to NAB's secure page. A small verification may show on your statement and is reversed automatically.</p>
    </div></div>`,
  }));
});

router.post('/autopay', (req, res) => {
  const c = req.customer; const f = req.body;
  const card = f.autopay_payment_method_id ? get("SELECT * FROM payment_methods WHERE id=? AND customer_id=? AND status='active'", [f.autopay_payment_method_id, c.id]) : null;
  const enabled = f.autopay_enabled === '1' && !!card && settings(req.customerBusiness).autopay_allowed;
  update('customers', c.id, { autopay_enabled: enabled ? 1 : 0, autopay_timing: f.autopay_timing, autopay_days_before: Number(f.autopay_days_before || 0), autopay_payment_method_id: card?.id || null, updated_at: now() });
  audit(c.business_id, `customer:${c.id}`, enabled ? 'customer.autopay_enabled' : 'customer.autopay_disabled', 'customer', c.id, { via: 'portal', timing: f.autopay_timing });
  // Re-plan open invoices to the new preference.
  run('UPDATE invoices SET autopay_scheduled_for=NULL, autopay_next_attempt_at=NULL WHERE customer_id=?', [c.id]);
  if (enabled) {
    for (const i of all("SELECT * FROM invoices WHERE customer_id=? AND status='AUTHORISED' AND amount_due>0", [c.id])) {
      let when = i.due_date || now().slice(0, 10);
      if (f.autopay_timing === 'on_issue') when = now().slice(0, 10);
      if (f.autopay_timing === 'days_before') { const d = new Date(when + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() - Number(f.autopay_days_before || 0)); when = d.toISOString().slice(0, 10); }
      if (when < now().slice(0, 10)) when = now().slice(0, 10);
      update('invoices', i.id, { autopay_scheduled_for: when, autopay_next_attempt_at: when + 'T00:00:00.000Z', autopay_attempts: 0, autopay_last_error: null });
    }
  }
  res.flash('ok', enabled ? 'Automatic payments are on.' : 'Automatic payments are off.'); res.redirect('/portal/autopay');
});

router.post('/cards/:id/remove', (req, res) => {
  const c = req.customer;
  const m = get('SELECT * FROM payment_methods WHERE id=? AND customer_id=?', [req.params.id, c.id]);
  if (m) {
    update('payment_methods', m.id, { status: 'removed' });
    if (c.autopay_payment_method_id === m.id) { update('customers', c.id, { autopay_payment_method_id: null, autopay_enabled: 0 }); run('UPDATE invoices SET autopay_next_attempt_at=NULL WHERE customer_id=?', [c.id]); }
    audit(c.business_id, `customer:${c.id}`, 'payment_method.removed', 'payment_method', m.id, null);
  }
  res.flash('ok', 'Card removed.'); res.redirect('/portal/autopay');
});

// Add a card without paying an invoice: zero-value tokenisation on the hosted page.
router.post('/cards/add', async (req, res) => {
  const c = req.customer; const b = req.customerBusiness;
  const intent = `addcard:${c.id}:${Date.now()}`;
  const returnUrl = `${config.baseUrl}/portal/cards/return?i=${encodeURIComponent(intent)}&s=${sign(intent)}`;
  try {
    const gw = gatewayClient(gatewayConnection(b.id));
    const co = await gw.createCheckout({ amount: 0, currency: 'AUD', reference: `CARD-${c.id}`, description: `Save card for ${b.name}`, returnUrl, tokenise: true });
    res.redirect(co.redirectUrl);
  } catch (e) { res.flash('err', e.message); res.redirect('/portal/autopay'); }
});

router.get('/cards/return', async (req, res) => {
  const c = req.customer; const b = req.customerBusiness;
  const intent = String(req.query.i || '');
  if (!verifySigned(intent, String(req.query.s || '')) || intent.split(':')[1] !== String(c.id)) { res.flash('err', 'Could not verify the card setup.'); return res.redirect('/portal/autopay'); }
  try {
    const gw = gatewayClient(gatewayConnection(b.id));
    const outcome = await gw.completeCheckout(req.query.checkout, req.query);
    if (outcome.approved && outcome.token) {
      const pm = savePaymentMethod(b, c, outcome.token);
      if (!c.autopay_payment_method_id) update('customers', c.id, { autopay_payment_method_id: pm.id });
      res.flash('ok', `${outcome.token.card_brand} ending ${outcome.token.last4} saved. Turn on automatic payments below if you would like us to use it.`);
    } else res.flash('err', `Card was not saved (${outcome.message}).`);
  } catch (e) { res.flash('err', e.message); }
  res.redirect('/portal/autopay');
});

router.get('/account', (req, res) => {
  const c = req.customer;
  const others = all('SELECT c.id, b.name, b.slug FROM customers c JOIN businesses b ON b.id=c.business_id WHERE lower(c.email)=? AND c.id<>?', [String(c.email || '').toLowerCase(), c.id]);
  res.send(page(req, {
    title: 'Account', active: 'account', body: `
    <div class="card"><dl class="kv"><dt>Name</dt><dd>${esc(c.name)}</dd><dt>Email</dt><dd>${esc(c.email || '')}</dd><dt>Phone</dt><dd>${esc(c.phone || '')}</dd></dl>
    <p class="small muted" style="margin-top:10px">Details come from ${esc(req.customerBusiness.name)}'s records. Contact them to change your email address.</p></div>
    ${others.length ? `<div class="card"><h3>Other businesses you pay through this portal</h3>${others.map((o) => `<p><a href="/portal?biz=${esc(o.slug)}">${esc(o.name)}</a> <span class="small muted">(request a new sign-in link)</span></p>`).join('')}</div>` : ''}`,
  }));
});
