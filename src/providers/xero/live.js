// Real Xero OAuth 2.0 + Accounting API adapter. Used when APP_MODE=live.
// Docs: https://developer.xero.com/documentation/guides/oauth2/auth-flow/
import { config } from '../../config.js';
import { decrypt, encrypt } from '../../crypto.js';
import { get, now, update } from '../../db.js';

const AUTH_URL = 'https://login.xero.com/identity/connect/authorize';
const TOKEN_URL = 'https://identity.xero.com/connect/token';
const API = 'https://api.xero.com/api.xro/2.0';

export function getAuthUrl(state) {
  const p = new URLSearchParams({
    response_type: 'code',
    client_id: config.xero.clientId,
    redirect_uri: config.xero.redirectUri,
    scope: config.xero.scopes,
    state,
  });
  return `${AUTH_URL}?${p}`;
}

async function tokenRequest(body) {
  const basic = Buffer.from(`${config.xero.clientId}:${config.xero.clientSecret}`).toString('base64');
  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { Authorization: `Basic ${basic}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(body),
  });
  if (!res.ok) throw new Error(`Xero token error ${res.status}: ${await res.text()}`);
  return res.json();
}

// Exchange the auth code, then list the tenants the user authorised.
export async function handleCallback(code) {
  const tok = await tokenRequest({ grant_type: 'authorization_code', code, redirect_uri: config.xero.redirectUri });
  const conns = await fetch('https://api.xero.com/connections', {
    headers: { Authorization: `Bearer ${tok.access_token}` },
  }).then((r) => r.json());
  const tenant = conns.find((c) => c.tenantType === 'ORGANISATION') || conns[0];
  if (!tenant) throw new Error('No Xero organisation was authorised');
  return {
    tenantId: tenant.tenantId,
    tenantName: tenant.tenantName,
    accessToken: tok.access_token,
    refreshToken: tok.refresh_token,
    expiresAt: new Date(Date.now() + tok.expires_in * 1000).toISOString(),
  };
}

async function freshAccessToken(connection) {
  const expires = new Date(connection.token_expires_at || 0).getTime();
  if (expires - Date.now() > 60_000) return decrypt(connection.access_token_enc);
  const tok = await tokenRequest({ grant_type: 'refresh_token', refresh_token: decrypt(connection.refresh_token_enc) });
  update('connections', connection.id, {
    access_token_enc: encrypt(tok.access_token),
    refresh_token_enc: encrypt(tok.refresh_token),
    token_expires_at: new Date(Date.now() + tok.expires_in * 1000).toISOString(),
  });
  return tok.access_token;
}

export function client(connection) {
  const call = async (method, path, body) => {
    const conn = get('SELECT * FROM connections WHERE id=?', [connection.id]);
    const token = await freshAccessToken(conn);
    const res = await fetch(`${API}${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        'Xero-Tenant-Id': conn.tenant_id,
        Accept: 'application/json',
        ...(body ? { 'Content-Type': 'application/json' } : {}),
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`Xero ${method} ${path} failed ${res.status}: ${await res.text()}`);
    return res.json();
  };
  return {
    async organisation() { return (await call('GET', '/Organisation')).Organisations[0]; },
    async contacts() { return (await call('GET', '/Contacts?where=IsCustomer%3Dtrue&includeArchived=false')).Contacts; },
    async contact(id) { return (await call('GET', `/Contacts/${id}`)).Contacts[0]; },
    async invoices() {
      // Unpaid customer invoices. Xero pages at 100; loop until empty.
      const out = [];
      for (let page = 1; page < 50; page++) {
        const r = await call('GET', `/Invoices?where=Type%3D%22ACCREC%22%20AND%20Status%3D%3D%22AUTHORISED%22&page=${page}`);
        out.push(...r.Invoices);
        if (r.Invoices.length < 100) break;
      }
      return out;
    },
    async invoice(id) { return (await call('GET', `/Invoices/${id}`)).Invoices[0]; },
    async invoiceByNumber(number) { return (await call('GET', `/Invoices/${encodeURIComponent(number)}`)).Invoices[0]; },
    async accounts() { return (await call('GET', '/Accounts?where=EnablePaymentsToAccount%3D%3Dtrue')).Accounts; },
    // Records the card payment against the invoice so Xero marks it paid.
    async createPayment({ invoiceId, accountCode, amount, date, reference }) {
      const r = await call('PUT', '/Payments', {
        Payments: [{ Invoice: { InvoiceID: invoiceId }, Account: { Code: accountCode }, Date: date, Amount: amount, Reference: reference }],
      });
      return r.Payments[0];
    },
  };
}

// Marks a connection as needing re-auth, e.g. after a refresh token is revoked.
export function markDisconnected(connectionId, reason) {
  update('connections', connectionId, { status: 'disconnected', meta_json: JSON.stringify({ reason, at: now() }) });
}
