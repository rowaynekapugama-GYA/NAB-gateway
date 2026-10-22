import { Router } from 'express';
import { config, isDemo } from '../config.js';
import { audit, get, insert, now } from '../db.js';
import { hashPassword, shortCode, verifyPassword } from '../crypto.js';
import { endSession, startSession } from '../auth.js';
import { esc, field, plainPage } from '../layout.js';

export const router = Router();

const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40) || 'business';

router.get('/', (req, res) => {
  if (req.user) return res.redirect('/app');
  res.send(plainPage({
    title: 'Welcome', wide: true, flash: req.flash, body: `
    <div class="brand-mark">${esc(config.appName)}</div>
    <div class="card">
      <h2>Get paid by card straight from Xero, through your own NAB merchant account</h2>
      <p>Connect Xero and your NAB gateway once. Every invoice gets a Pay-by-card link, every customer gets a portal, and customers who switch on autopay are charged automatically when their Xero invoices fall due. Payments are written back to Xero so reconciliation is automatic.</p>
      <div class="row" style="margin-top:14px"><a class="btn" href="/signup">Create a business account</a><a class="btn secondary" href="/login">Sign in</a><a class="btn secondary" href="/portal">Customer portal</a></div>
    </div>
    ${isDemo() ? `<div class="card"><h3>Demo accounts</h3><p class="small">Run <code>npm run seed</code> to create <strong>demo@paybridge.local / demo1234</strong> (a business with sample customers and invoices). Platform admin: <strong>${esc(config.adminEmail)} / ${esc(config.adminPassword)}</strong> at <a href="/admin">/admin</a>.</p></div>` : ''}`,
  }));
});

router.get('/signup', (req, res) => {
  res.send(plainPage({
    title: 'Create your account', flash: req.flash, body: `
    <div class="brand-mark">${esc(config.appName)}</div>
    <div class="card"><h2>Create a business account</h2>
    <form method="post" action="/signup">
      ${field('Business name', 'name', { required: true, placeholder: 'e.g. Northside Physio Pty Ltd' })}
      ${field('ABN (optional)', 'abn')}
      ${field('Your name', 'owner_name', { required: true })}
      ${field('Work email', 'email', { type: 'email', required: true })}
      ${field('Password', 'password', { type: 'password', required: true, help: 'At least 8 characters' })}
      <button class="btn">Create account</button>
    </form></div>
    <p class="small muted">Already have an account? <a href="/login">Sign in</a></p>`,
  }));
});

router.post('/signup', (req, res) => {
  const { name, abn, owner_name, email, password } = req.body;
  if (!name || !email || !password || password.length < 8) { res.flash('err', 'Please complete all fields; password needs 8+ characters.'); return res.redirect('/signup'); }
  let slug = slugify(name);
  while (get('SELECT id FROM businesses WHERE slug=?', [slug])) slug = `${slugify(name)}-${shortCode(3)}`;
  const business_id = insert('businesses', { name, slug, short_code: shortCode(6), abn: abn || null, email, created_at: now() });
  const user_id = insert('users', { business_id, email: email.toLowerCase(), name: owner_name, password_hash: hashPassword(password), role: 'owner', created_at: now() });
  audit(business_id, `user:${user_id}`, 'business.created', 'business', business_id, { name });
  startSession(res, 'user', user_id);
  res.flash('ok', 'Welcome! Follow the setup steps below to connect Xero and your NAB gateway.');
  res.redirect('/app');
});

router.get('/login', (req, res) => {
  res.send(plainPage({
    title: 'Sign in', flash: req.flash, body: `
    <div class="brand-mark">${esc(config.appName)}</div>
    <div class="card"><h2>Sign in</h2>
    <form method="post" action="/login">
      <input type="hidden" name="next" value="${esc(req.query.next || '')}">
      ${field('Email', 'email', { type: 'email', required: true })}
      ${field('Password', 'password', { type: 'password', required: true })}
      <button class="btn">Sign in</button>
    </form></div>
    <p class="small muted">New here? <a href="/signup">Create a business account</a> · Customer? <a href="/portal">Go to the portal</a></p>`,
  }));
});

router.post('/login', (req, res) => {
  const { email, password, next } = req.body;
  const user = get('SELECT * FROM users WHERE email=?', [String(email || '').toLowerCase()]);
  if (!user || !verifyPassword(password || '', user.password_hash)) { res.flash('err', 'Email or password is incorrect.'); return res.redirect('/login'); }
  startSession(res, 'user', user.id);
  res.redirect(next && next.startsWith('/') ? next : '/app');
});

router.post('/logout', (req, res) => { endSession(req, res, 'user'); res.redirect('/login'); });
