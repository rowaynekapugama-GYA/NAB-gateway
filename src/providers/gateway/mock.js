// Mock NAB gateway for demo mode. Mimics the three things we need from the
// real gateway: a hosted payment page (so card data never touches us), a
// stored-card token, and a server-to-server charge against that token.
//
// Test cards on the hosted page:
//   4111 1111 1111 1111  approves, and the token always approves later
//   4000 0000 0000 0002  declines (code 05 Do Not Honour)
//   4000 0000 0000 0119  approves now, token fails on later autopay charges
import { randomUUID } from 'node:crypto';
import { get, insert, now, update } from '../../db.js';
import { config } from '../../config.js';

const brandOf = (pan) => (pan.startsWith('4') ? 'Visa' : pan.startsWith('5') ? 'Mastercard' : pan.startsWith('3') ? 'Amex' : 'Card');

export function client(connection) {
  const merchant_id = connection.merchant_id || 'DEMO0001';
  return {
    kind: 'mock',
    async verifyCredentials() { return { ok: true, message: 'Mock gateway accepts any credentials' }; },

    async createCheckout({ amount, currency = 'AUD', reference, description, returnUrl, tokenise = false }) {
      const checkout_id = randomUUID();
      insert('gsim_checkouts', {
        checkout_id, merchant_id, amount, currency, reference, description, return_url: returnUrl,
        tokenise: tokenise ? 1 : 0, created_at: now(),
      });
      return { checkoutId: checkout_id, redirectUrl: `${config.baseUrl}/gsim/checkout/${checkout_id}` };
    },

    // Called after the hosted page redirects back. Returns the outcome.
    async completeCheckout(checkoutId) {
      const c = get('SELECT * FROM gsim_checkouts WHERE checkout_id=?', [checkoutId]);
      if (!c || c.status !== 'complete') return { approved: false, code: 'XX', message: 'Checkout not completed' };
      return JSON.parse(c.result_json);
    },

    async chargeToken({ token, amount, currency = 'AUD', reference }) {
      const t = get('SELECT * FROM gsim_tokens WHERE merchant_id=? AND token=?', [merchant_id, token]);
      if (!t) return { approved: false, code: '14', message: 'Invalid card token' };
      const approved = t.behaviour === 'approve';
      const res = approved ? { code: '00', message: 'Approved' } : t.behaviour === 'insufficient'
        ? { code: '51', message: 'Insufficient Funds' } : { code: '05', message: 'Do Not Honour' };
      const txn_id = 'MOCK' + randomUUID().replace(/-/g, '').slice(0, 12).toUpperCase();
      insert('gsim_transactions', {
        merchant_id, txn_id, token, amount, currency, reference, approved: approved ? 1 : 0,
        response_code: res.code, response_text: res.message, created_at: now(),
      });
      return { approved, txnId: txn_id, code: res.code, message: res.message };
    },

    async refund({ txnId, amount }) {
      const orig = get('SELECT * FROM gsim_transactions WHERE merchant_id=? AND txn_id=?', [merchant_id, txnId]);
      if (!orig) return { approved: false, code: '14', message: 'Original transaction not found' };
      const txn_id = 'MOCKR' + randomUUID().replace(/-/g, '').slice(0, 11).toUpperCase();
      insert('gsim_transactions', {
        merchant_id, txn_id, token: orig.token, amount: -amount, currency: orig.currency,
        reference: `REFUND ${orig.reference}`, approved: 1, response_code: '00', response_text: 'Approved', created_at: now(),
      });
      return { approved: true, txnId: txn_id, code: '00', message: 'Approved' };
    },
  };
}

// Used by the fake hosted page when the customer submits a test card.
export function processHostedCard(checkoutId, { pan, expiry, cardholder }) {
  const c = get('SELECT * FROM gsim_checkouts WHERE checkout_id=?', [checkoutId]);
  if (!c || c.status !== 'open') throw new Error('Checkout is not open');
  const digits = pan.replace(/\D/g, '');
  const [mm, yy] = expiry.split('/').map((s) => Number(s.trim()));
  let behaviour = 'approve';
  let approvedNow = true;
  if (digits === '4000000000000002') { approvedNow = false; behaviour = 'decline'; }
  if (digits === '4000000000000119') { approvedNow = true; behaviour = 'decline'; }
  if (digits === '4000000000009995') { approvedNow = false; behaviour = 'insufficient'; }

  const txn_id = 'MOCK' + randomUUID().replace(/-/g, '').slice(0, 12).toUpperCase();
  let tokenInfo = null;
  if (c.tokenise && approvedNow) {
    const token = 'tok_' + randomUUID().replace(/-/g, '');
    insert('gsim_tokens', {
      merchant_id: c.merchant_id, token, card_brand: brandOf(digits), last4: digits.slice(-4),
      expiry_month: mm, expiry_year: 2000 + yy, cardholder, behaviour, created_at: now(),
    });
    tokenInfo = { gateway_token: token, card_brand: brandOf(digits), last4: digits.slice(-4), expiry_month: mm, expiry_year: 2000 + yy, cardholder };
  }
  insert('gsim_transactions', {
    merchant_id: c.merchant_id, txn_id, token: tokenInfo?.gateway_token || null, amount: c.amount, currency: c.currency,
    reference: c.reference, approved: approvedNow ? 1 : 0,
    response_code: approvedNow ? '00' : behaviour === 'insufficient' ? '51' : '05',
    response_text: approvedNow ? 'Approved' : behaviour === 'insufficient' ? 'Insufficient Funds' : 'Do Not Honour',
    created_at: now(),
  });
  const result = {
    approved: approvedNow, txnId: txn_id,
    code: approvedNow ? '00' : behaviour === 'insufficient' ? '51' : '05',
    message: approvedNow ? 'Approved' : behaviour === 'insufficient' ? 'Insufficient Funds' : 'Do Not Honour',
    card: { brand: brandOf(digits), last4: digits.slice(-4) },
    token: tokenInfo,
  };
  update('gsim_checkouts', c.id, { status: 'complete', result_json: JSON.stringify(result) });
  return { result, returnUrl: c.return_url };
}
