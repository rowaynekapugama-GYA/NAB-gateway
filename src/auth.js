import { get, insert, now, run } from './db.js';
import { token } from './crypto.js';

const COOKIES = { user: 'pb_session', customer: 'pb_portal', admin: 'pb_admin' };
const TTL = { user: 14, customer: 30, admin: 1 }; // days

export function parseCookies(req) {
  const out = {};
  (req.headers.cookie || '').split(';').forEach((p) => {
    const i = p.indexOf('=');
    if (i > 0) out[p.slice(0, i).trim()] = decodeURIComponent(p.slice(i + 1).trim());
  });
  return out;
}

export function setCookie(res, name, value, { days = 14, path = '/' } = {}) {
  const parts = [`${name}=${encodeURIComponent(value)}`, `Path=${path}`, 'HttpOnly', 'SameSite=Lax'];
  if (days > 0) parts.push(`Max-Age=${days * 86400}`); else parts.push('Max-Age=0');
  const prev = res.getHeader('Set-Cookie');
  res.setHeader('Set-Cookie', [...(Array.isArray(prev) ? prev : prev ? [prev] : []), parts.join('; ')]);
}

export function startSession(res, kind, subject_id) {
  const t = token();
  insert('sessions', { kind, subject_id, token: t, expires_at: new Date(Date.now() + TTL[kind] * 864e5).toISOString(), created_at: now() });
  setCookie(res, COOKIES[kind], t, { days: TTL[kind] });
}

export function endSession(req, res, kind) {
  const t = parseCookies(req)[COOKIES[kind]];
  if (t) run('DELETE FROM sessions WHERE token=?', [t]);
  setCookie(res, COOKIES[kind], '', { days: 0 });
}

function lookup(req, kind) {
  const t = parseCookies(req)[COOKIES[kind]];
  if (!t) return null;
  const s = get('SELECT * FROM sessions WHERE token=? AND kind=? AND expires_at>?', [t, kind, now()]);
  return s;
}

// Attaches req.user / req.business / req.customer / req.admin when present.
export function attachIdentity(req, res, next) {
  const us = lookup(req, 'user');
  if (us) {
    req.user = get('SELECT * FROM users WHERE id=?', [us.subject_id]);
    if (req.user) req.business = get('SELECT * FROM businesses WHERE id=?', [req.user.business_id]);
  }
  const cs = lookup(req, 'customer');
  if (cs) {
    req.customer = get('SELECT * FROM customers WHERE id=?', [cs.subject_id]);
    if (req.customer) req.customerBusiness = get('SELECT * FROM businesses WHERE id=?', [req.customer.business_id]);
  }
  req.admin = !!lookup(req, 'admin');
  // flash
  const cookies = parseCookies(req);
  if (cookies.pb_flash) { try { req.flash = JSON.parse(cookies.pb_flash); } catch { /* ignore */ } setCookie(res, 'pb_flash', '', { days: 0 }); }
  res.flash = (type, text) => setCookie(res, 'pb_flash', JSON.stringify({ type, text }), { days: 1 });
  next();
}

export const requireUser = (req, res, next) => (req.user && req.business ? next() : res.redirect('/login?next=' + encodeURIComponent(req.originalUrl)));
export const requireCustomer = (req, res, next) => (req.customer ? next() : res.redirect('/portal'));
export const requireAdmin = (req, res, next) => (req.admin ? next() : res.redirect('/admin/login'));
