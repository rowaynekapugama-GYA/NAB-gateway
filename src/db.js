// SQLite via Node's built-in node:sqlite (no native build step).
// Swap this module for Postgres/Supabase in production; every query goes
// through the small helpers below so the swap is contained.
import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { config } from './config.js';

mkdirSync(dirname(config.dbPath), { recursive: true });
export const db = new DatabaseSync(config.dbPath);
db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;');

export const now = () => new Date().toISOString();
export const today = () => new Date().toISOString().slice(0, 10);

export function run(sql, params = []) {
  return db.prepare(sql).run(...params);
}
export function get(sql, params = []) {
  return db.prepare(sql).get(...params);
}
export function all(sql, params = []) {
  return db.prepare(sql).all(...params);
}
export function insert(table, obj) {
  const keys = Object.keys(obj);
  const sql = `INSERT INTO ${table} (${keys.join(',')}) VALUES (${keys.map(() => '?').join(',')})`;
  const r = db.prepare(sql).run(...keys.map((k) => obj[k]));
  return Number(r.lastInsertRowid);
}
export function update(table, id, obj) {
  const keys = Object.keys(obj);
  if (!keys.length) return;
  const sql = `UPDATE ${table} SET ${keys.map((k) => `${k}=?`).join(',')} WHERE id=?`;
  db.prepare(sql).run(...keys.map((k) => obj[k]), id);
}
export function tx(fn) {
  db.exec('BEGIN');
  try {
    const r = fn();
    db.exec('COMMIT');
    return r;
  } catch (e) {
    db.exec('ROLLBACK');
    throw e;
  }
}

const schema = `
CREATE TABLE IF NOT EXISTS businesses (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  short_code TEXT UNIQUE NOT NULL,
  abn TEXT, email TEXT, phone TEXT, website TEXT,
  brand_colour TEXT DEFAULT '#0f4c81',
  logo_url TEXT,
  settings_json TEXT DEFAULT '{}',
  plan TEXT DEFAULT 'trial',
  status TEXT DEFAULT 'active',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  business_id INTEGER NOT NULL REFERENCES businesses(id),
  email TEXT NOT NULL,
  name TEXT,
  password_hash TEXT NOT NULL,
  role TEXT DEFAULT 'owner',
  created_at TEXT NOT NULL,
  UNIQUE(business_id, email)
);

CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,            -- user | customer | admin
  subject_id INTEGER,
  token TEXT UNIQUE NOT NULL,
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS connections (
  id INTEGER PRIMARY KEY,
  business_id INTEGER NOT NULL REFERENCES businesses(id),
  provider TEXT NOT NULL,        -- xero | gateway
  status TEXT DEFAULT 'connected',
  tenant_id TEXT, tenant_name TEXT,
  access_token_enc TEXT, refresh_token_enc TEXT, token_expires_at TEXT,
  gateway_kind TEXT,             -- nab_transact | mock
  merchant_id TEXT,
  credentials_enc TEXT,          -- encrypted JSON of gateway secrets
  environment TEXT DEFAULT 'test',
  meta_json TEXT DEFAULT '{}',
  connected_at TEXT, last_sync_at TEXT,
  UNIQUE(business_id, provider)
);

CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY,
  business_id INTEGER NOT NULL REFERENCES businesses(id),
  xero_contact_id TEXT,
  name TEXT NOT NULL,
  email TEXT, phone TEXT,
  portal_token TEXT UNIQUE,
  portal_status TEXT DEFAULT 'none',   -- none | invited | active
  autopay_enabled INTEGER DEFAULT 0,
  autopay_timing TEXT,                 -- on_issue | due_date | days_before
  autopay_days_before INTEGER DEFAULT 0,
  autopay_payment_method_id INTEGER,
  invited_at TEXT, last_login_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  UNIQUE(business_id, xero_contact_id)
);

CREATE TABLE IF NOT EXISTS magic_links (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  token TEXT UNIQUE NOT NULL,
  expires_at TEXT NOT NULL,
  used_at TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS invoices (
  id INTEGER PRIMARY KEY,
  business_id INTEGER NOT NULL REFERENCES businesses(id),
  customer_id INTEGER REFERENCES customers(id),
  xero_invoice_id TEXT,
  number TEXT, reference TEXT,
  status TEXT,                   -- DRAFT | SUBMITTED | AUTHORISED | PAID | VOIDED | DELETED
  issue_date TEXT, due_date TEXT,
  currency TEXT DEFAULT 'AUD',
  subtotal REAL, tax REAL, total REAL,
  amount_due REAL, amount_paid REAL DEFAULT 0,
  pay_token TEXT UNIQUE,
  line_items_json TEXT DEFAULT '[]',
  repeating_invoice_id TEXT,
  autopay_scheduled_for TEXT,
  autopay_attempts INTEGER DEFAULT 0,
  autopay_next_attempt_at TEXT,
  autopay_last_error TEXT,
  pay_link_sent_at TEXT,
  created_at TEXT NOT NULL, updated_at TEXT,
  UNIQUE(business_id, xero_invoice_id)
);

CREATE TABLE IF NOT EXISTS payment_methods (
  id INTEGER PRIMARY KEY,
  business_id INTEGER NOT NULL REFERENCES businesses(id),
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  gateway_token TEXT NOT NULL,   -- token/CRN issued by the gateway; never a PAN
  card_brand TEXT, last4 TEXT, expiry_month INTEGER, expiry_year INTEGER, cardholder TEXT,
  is_default INTEGER DEFAULT 0,
  status TEXT DEFAULT 'active',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY,
  business_id INTEGER NOT NULL REFERENCES businesses(id),
  customer_id INTEGER REFERENCES customers(id),
  invoice_id INTEGER REFERENCES invoices(id),
  payment_method_id INTEGER,
  amount REAL NOT NULL,
  currency TEXT DEFAULT 'AUD',
  status TEXT NOT NULL,          -- succeeded | failed | refunded
  source TEXT,                   -- pay_link | xero_paynow | portal | autopay
  gateway_txn_id TEXT, gateway_code TEXT, gateway_message TEXT,
  xero_payment_id TEXT,
  xero_writeback_status TEXT DEFAULT 'pending',
  xero_writeback_error TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS webhook_events (
  id INTEGER PRIMARY KEY,
  business_id INTEGER,
  provider TEXT NOT NULL,
  event_key TEXT UNIQUE,         -- idempotency key
  category TEXT, type TEXT, resource_id TEXT,
  payload_json TEXT,
  status TEXT DEFAULT 'received',
  error TEXT,
  received_at TEXT NOT NULL, processed_at TEXT
);

CREATE TABLE IF NOT EXISTS outbox (
  id INTEGER PRIMARY KEY,
  business_id INTEGER,
  to_email TEXT, to_name TEXT,
  subject TEXT, body_html TEXT,
  kind TEXT,
  status TEXT DEFAULT 'queued',
  created_at TEXT NOT NULL, sent_at TEXT
);

CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY,
  business_id INTEGER,
  actor TEXT,
  action TEXT NOT NULL,
  entity_type TEXT, entity_id TEXT,
  detail_json TEXT,
  created_at TEXT NOT NULL
);

-- ---------- Xero simulator (demo mode only) ----------
CREATE TABLE IF NOT EXISTS xsim_orgs (
  id INTEGER PRIMARY KEY,
  tenant_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  short_code TEXT,
  next_invoice_no INTEGER DEFAULT 1,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS xsim_contacts (
  id INTEGER PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  contact_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL, email TEXT, phone TEXT,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS xsim_invoices (
  id INTEGER PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  invoice_id TEXT UNIQUE NOT NULL,
  contact_id TEXT NOT NULL,
  number TEXT, reference TEXT,
  status TEXT DEFAULT 'AUTHORISED',
  issue_date TEXT, due_date TEXT,
  subtotal REAL, tax REAL, total REAL, amount_due REAL, amount_paid REAL DEFAULT 0,
  line_items_json TEXT,
  repeating_invoice_id TEXT,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS xsim_repeating (
  id INTEGER PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  repeating_id TEXT UNIQUE NOT NULL,
  contact_id TEXT NOT NULL,
  reference TEXT,
  period INTEGER DEFAULT 1, unit TEXT DEFAULT 'MONTHLY',
  due_days INTEGER DEFAULT 7,
  next_date TEXT,
  line_items_json TEXT,
  status TEXT DEFAULT 'AUTHORISED',
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS xsim_payments (
  id INTEGER PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  payment_id TEXT UNIQUE NOT NULL,
  invoice_id TEXT NOT NULL,
  account_code TEXT, amount REAL, date TEXT, reference TEXT,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS xsim_webhook_queue (
  id INTEGER PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  category TEXT, type TEXT, resource_id TEXT,
  created_at TEXT NOT NULL,
  delivered_at TEXT
);

-- ---------- Mock NAB gateway (demo mode only) ----------
CREATE TABLE IF NOT EXISTS gsim_tokens (
  id INTEGER PRIMARY KEY,
  merchant_id TEXT NOT NULL,
  token TEXT UNIQUE NOT NULL,
  card_brand TEXT, last4 TEXT, expiry_month INTEGER, expiry_year INTEGER, cardholder TEXT,
  behaviour TEXT DEFAULT 'approve',   -- approve | decline | insufficient
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS gsim_transactions (
  id INTEGER PRIMARY KEY,
  merchant_id TEXT NOT NULL,
  txn_id TEXT UNIQUE NOT NULL,
  token TEXT, amount REAL, currency TEXT, reference TEXT,
  approved INTEGER, response_code TEXT, response_text TEXT,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS gsim_checkouts (
  id INTEGER PRIMARY KEY,
  checkout_id TEXT UNIQUE NOT NULL,
  merchant_id TEXT NOT NULL,
  amount REAL, currency TEXT, reference TEXT, description TEXT,
  return_url TEXT, tokenise INTEGER DEFAULT 0,
  status TEXT DEFAULT 'open',
  result_json TEXT,
  created_at TEXT NOT NULL
);
`;

db.exec(schema);

export function audit(business_id, actor, action, entity_type, entity_id, detail) {
  insert('audit_log', {
    business_id, actor, action, entity_type, entity_id: entity_id == null ? null : String(entity_id),
    detail_json: detail ? JSON.stringify(detail) : null, created_at: now(),
  });
}

export function settings(business) {
  const defaults = {
    autopay_allowed: true,
    autopay_default_timing: 'due_date',   // on_issue | due_date | days_before
    autopay_days_before: 3,
    send_pay_link_on_invoice: true,
    send_receipts: true,
    xero_payment_account_code: '090',     // account the payment is recorded against in Xero
    amex_surcharge_pct: 0,                // Visa/Mastercard/eftpos surcharging is banned from 1 Oct 2026
    reminder_days_after_due: 3,
    portal_welcome: 'Pay invoices securely by card and set up automatic payments.',
  };
  let parsed = {};
  try { parsed = JSON.parse(business.settings_json || '{}'); } catch { /* ignore */ }
  return { ...defaults, ...parsed };
}
