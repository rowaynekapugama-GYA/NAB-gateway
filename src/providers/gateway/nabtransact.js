// NAB Transact adapter (live mode). Implements the same interface as mock.js.
//
// NAB Transact exposes:
//   - Hosted Payment Page (customer enters card on NAB's page; we get a
//     signed result back on the return URL). PCI scope stays at SAQ A.
//   - SecureXML "Payment" API for server-to-server transactions.
//   - "Periodic" API for stored payors (the token we keep for autopay):
//     actionType=add stores the card against a clientID (CRN), and
//     actionType=trigger charges that CRN later without card data.
//
// Field names below follow the NAB Transact SecureXML / Periodic guides.
// NAB is still supplying the final integration pack, so every request
// builder is isolated here and marked VERIFY where the exact field or
// endpoint should be checked against the pack before go-live.
import { randomUUID, createHash } from 'node:crypto';
import { config } from '../../config.js';
import { decrypt } from '../../crypto.js';

const CARD_TYPES = { Visa: '6', Mastercard: '6', Amex: '6' }; // txnSource 23 = internet

function creds(connection) {
  const c = JSON.parse(decrypt(connection.credentials_enc) || '{}');
  return {
    merchantId: connection.merchant_id,
    password: c.transaction_password,          // SecureXML transaction password
    hppPassword: c.hpp_password || c.transaction_password, // Hosted page password  VERIFY
    environment: connection.environment || 'test',
  };
}

const ts = () => {
  const d = new Date();
  const p = (n, l = 2) => String(n).padStart(l, '0');
  // NAB format: YYYYDDMMHHNNSSKKK000sOOO  (note DD before MM)  VERIFY
  return `${d.getFullYear()}${p(d.getDate())}${p(d.getMonth() + 1)}${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}${p(d.getMilliseconds(), 3)}000+600`;
};
const cents = (amount) => Math.round(Number(amount) * 100);
const esc = (s) => String(s ?? '').replace(/[<>&'"]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
const pick = (xml, tag) => (xml.match(new RegExp(`<${tag}>([^<]*)</${tag}>`)) || [])[1];

async function post(url, xml) {
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'text/xml' }, body: xml });
  const text = await res.text();
  if (!res.ok) throw new Error(`NAB Transact HTTP ${res.status}: ${text.slice(0, 300)}`);
  return text;
}

function envelope({ merchantId, password }, requestType, body) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<NABTransactMessage>
  <MessageInfo>
    <messageID>${randomUUID().replace(/-/g, '').slice(0, 30)}</messageID>
    <messageTimestamp>${ts()}</messageTimestamp>
    <timeoutValue>60</timeoutValue>
    <apiVersion>${requestType === 'Periodic' ? 'spxml-4.2' : 'xml-4.2'}</apiVersion>
  </MessageInfo>
  <MerchantInfo>
    <merchantID>${esc(merchantId)}</merchantID>
    <password>${esc(password)}</password>
  </MerchantInfo>
  <RequestType>${requestType}</RequestType>
  ${body}
</NABTransactMessage>`;
}

export function client(connection) {
  const c = creds(connection);
  const paymentUrl = c.environment === 'live' ? config.nab.liveEndpoint : config.nab.testEndpoint;
  const periodicUrl = c.environment === 'live' ? config.nab.livePeriodicEndpoint : config.nab.testPeriodicEndpoint;

  return {
    kind: 'nab_transact',

    // Echo test: a zero-value "Echo" request validates merchant ID/password.
    async verifyCredentials() {
      try {
        const xml = envelope(c, 'Echo', '');
        const out = await post(paymentUrl, xml);
        const code = pick(out, 'statusCode');
        return { ok: code === '000', message: `${code} ${pick(out, 'statusDescription') || ''}`.trim() };
      } catch (e) {
        return { ok: false, message: e.message };
      }
    },

    // Hosted Payment Page: we redirect the customer to NAB with a signed
    // fingerprint; NAB redirects back to returnUrl with the result.
    // The exact field set (vendor_name, payment_reference, amount, fingerprint,
    // return_link_url, store_card) comes from NAB's HPP guide.  VERIFY
    async createCheckout({ amount, currency = 'AUD', reference, description, returnUrl, tokenise = false }) {
      const checkoutId = randomUUID();
      const amt = cents(amount);
      const timestamp = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14);
      const fingerprint = createHash('sha1')
        .update(`${c.merchantId}|${c.hppPassword}|0|${reference}|${amt}|${timestamp}`).digest('hex');
      const params = new URLSearchParams({
        vendor_name: c.merchantId,
        payment_alert: '',
        payment_reference: reference,
        amount: String(amt),
        currency,
        fp_timestamp: timestamp,
        fingerprint,
        return_link_url: `${returnUrl}${returnUrl.includes('?') ? '&' : '?'}checkout=${checkoutId}`,
        return_link_text: 'Return to invoice',
        store_card: tokenise ? '1' : '0',
        display_receipt: 'false',
        information_fields: description || '',
      });
      return { checkoutId, redirectUrl: `${config.nab.hostedPaymentUrl}?${params}` };
    },

    // Interpret the HPP return parameters. NAB posts/returns fields such as
    // payment_reference, bank_reference, summarycode, restext, rescode,
    // card_type, pan (masked), expirydate, and a token/CRN when store_card=1.
    // VERIFY field names and the response fingerprint check.
    async completeCheckout(checkoutId, params = {}) {
      const approved = String(params.summarycode) === '1' || params.rescode === '00';
      return {
        approved,
        txnId: params.bank_reference || params.txnid || null,
        code: params.rescode || (approved ? '00' : 'XX'),
        message: params.restext || (approved ? 'Approved' : 'Declined'),
        card: { brand: params.card_type || 'Card', last4: String(params.pan || '').slice(-4) },
        token: approved && params.token ? {
          gateway_token: params.token, card_brand: params.card_type || 'Card',
          last4: String(params.pan || '').slice(-4),
          expiry_month: Number(String(params.expirydate || '').slice(0, 2)) || null,
          expiry_year: 2000 + (Number(String(params.expirydate || '').slice(-2)) || 0),
          cardholder: params.cardholder || null,
        } : null,
      };
    },

    // Charge a stored payor (CRN) via the Periodic API, actionType=trigger.
    async chargeToken({ token, amount, currency = 'AUD', reference }) {
      const body = `<Periodic>
    <PeriodicList count="1">
      <PeriodicItem ID="1">
        <actionType>trigger</actionType>
        <clientID>${esc(token)}</clientID>
        <amount>${cents(amount)}</amount>
        <currency>${currency}</currency>
        <transactionReference>${esc(reference)}</transactionReference>
      </PeriodicItem>
    </PeriodicList>
  </Periodic>`;
      const out = await post(periodicUrl, envelope(c, 'Periodic', body));
      const code = pick(out, 'responseCode');
      return {
        approved: pick(out, 'successful') === 'yes',
        txnId: pick(out, 'txnID') || pick(out, 'receipt'),
        code, message: pick(out, 'responseText'),
      };
    },

    // Refund against the original transaction (txnType 4).
    async refund({ txnId, amount, reference }) {
      const body = `<Payment>
    <TxnList count="1">
      <Txn ID="1">
        <txnType>4</txnType>
        <txnSource>23</txnSource>
        <amount>${cents(amount)}</amount>
        <purchaseOrderNo>${esc(reference || 'REFUND')}</purchaseOrderNo>
        <txnID>${esc(txnId)}</txnID>
      </Txn>
    </TxnList>
  </Payment>`;
      const out = await post(paymentUrl, envelope(c, 'Payment', body));
      return {
        approved: pick(out, 'approved') === 'Yes',
        txnId: pick(out, 'txnID'), code: pick(out, 'responseCode'), message: pick(out, 'responseText'),
      };
    },
  };
}
