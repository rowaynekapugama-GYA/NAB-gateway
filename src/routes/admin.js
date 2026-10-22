// Platform admin: see every business on the platform, sign in as one for support.
import { Router } from 'express';
import { config } from '../config.js';
import { all, get } from '../db.js';
import { endSession, requireAdmin, startSession } from '../auth.js';
import { badge, datetime, esc, field, money, plainPage, table } from '../layout.js';

export const router = Router();

router.get('/admin/login', (req, res) => res.send(plainPage({ title: 'Platform admin', flash: req.flash, body: `<div class="brand-mark">${esc(config.appName)} admin</div><div class="card"><form method="post" action="/admin/login">${field('Email', 'email', { type: 'email', required: true })}${field('Password', 'password', { type: 'password', required: true })}<button class="btn">Sign in</button></form></div>` })));
router.post('/admin/login', (req, res) => {
  if (req.body.email === config.adminEmail && req.body.password === config.adminPassword) { startSession(res, 'admin', 0); return res.redirect('/admin'); }
  res.flash('err', 'Incorrect admin credentials.'); res.redirect('/admin/login');
});
router.post('/admin/logout', (req, res) => { endSession(req, res, 'admin'); res.redirect('/admin/login'); });

router.use('/admin', requireAdmin);

router.get('/admin', (req, res) => {
  const rows = all(`SELECT b.*, (SELECT COUNT(*) FROM customers c WHERE c.business_id=b.id) customers,
    (SELECT COUNT(*) FROM invoices i WHERE i.business_id=b.id) invoices,
    (SELECT COALESCE(SUM(amount),0) FROM payments p WHERE p.business_id=b.id AND p.status='succeeded') volume,
    (SELECT status FROM connections x WHERE x.business_id=b.id AND x.provider='xero') xero,
    (SELECT status FROM connections g WHERE g.business_id=b.id AND g.provider='gateway') gateway,
    (SELECT email FROM users u WHERE u.business_id=b.id ORDER BY u.id LIMIT 1) owner FROM businesses b ORDER BY b.id DESC`);
  const totals = get("SELECT COUNT(*) n, COALESCE(SUM(amount),0) v FROM payments WHERE status='succeeded'");
  res.send(plainPage({
    title: 'Platform admin', wide: true, flash: req.flash, body: `
    <div class="row between"><div class="brand-mark">${esc(config.appName)} admin</div><form method="post" action="/admin/logout"><button class="link small">Sign out</button></form></div>
    <div class="grid c3"><div class="stat"><div class="stat-v">${rows.length}</div><div class="stat-l">Businesses</div></div><div class="stat"><div class="stat-v">${money(totals.v)}</div><div class="stat-l">Processed (${totals.n} payments)</div></div><div class="stat"><div class="stat-v">${esc(config.mode)}</div><div class="stat-l">Mode</div></div></div>
    <h2>Businesses</h2>${table(['Business', 'Owner', 'Created', 'Xero', 'Gateway', 'Customers', 'Invoices', 'Volume', ''], rows.map((b) => [`${esc(b.name)}<div class="small muted">${esc(b.short_code)}</div>`, esc(b.owner || ''), datetime(b.created_at), badge(b.xero || 'none'), badge(b.gateway || 'none'), String(b.customers), String(b.invoices), money(b.volume), `<form method="post" action="/admin/impersonate/${b.id}"><button class="btn sm secondary">Sign in as</button></form>`]))}`,
  }));
});

router.post('/admin/impersonate/:id', (req, res) => {
  const u = get('SELECT * FROM users WHERE business_id=? ORDER BY id LIMIT 1', [req.params.id]);
  if (!u) { res.flash('err', 'No user for that business.'); return res.redirect('/admin'); }
  startSession(res, 'user', u.id); res.redirect('/app');
});
