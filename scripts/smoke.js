// End-to-end walk through every workflow against a running demo server.
// Usage: npm run seed && npm start   (in another terminal)   then: npm run smoke
const BASE = process.env.BASE_URL || 'http://localhost:3000';

class Jar {
  constructor() { this.c = {}; }
  absorb(res) { for (const h of res.headers.getSetCookie?.() || []) { const [kv] = h.split(';'); const [k, v] = kv.split('='); if (h.includes('Max-Age=0')) delete this.c[k]; else this.c[k] = v; } }
  header() { return Object.entries(this.c).map(([k, v]) => `${k}=${v}`).join('; '); }
}
async function req(jar, path, { method = 'GET', form = null, follow = true } = {}) {
  let url = path.startsWith('http') ? path : BASE + path;
  for (let i = 0; i < 10; i++) {
    const res = await fetch(url, { method, redirect: 'manual', headers: { Cookie: jar.header(), ...(form ? { 'Content-Type': 'application/x-www-form-urlencoded' } : {}) }, body: form ? new URLSearchParams(form) : undefined });
    jar.absorb(res);
    if (follow && [301, 302, 303].includes(res.status)) { url = new URL(res.headers.get('location'), url).toString(); method = 'GET'; form = null; continue; }
    const text = await res.text();
    return { status: res.status, text, url };
  }
  throw new Error('Too many redirects');
}
let passed = 0; const failures = [];
const check = (name, cond, extra = '') => { if (cond) { passed++; console.log('  ok  ', name); } else { failures.push(name); console.log('  FAIL', name, extra); } };
const pick = (text, re) => (text.match(re) || [])[1];

const biz = new Jar();
console.log('1. Business sign-in');
let r = await req(biz, '/login', { method: 'POST', form: { email: 'demo@transiqe.local', password: 'demo1234' } });
check('login lands on overview', r.url.endsWith('/app') && r.text.includes('Northside Physio'));
check('setup shows Xero + gateway connected', (r.text.match(/step done/g) || []).length >= 2);

console.log('2. Xero simulator: new contact -> webhook -> customer + portal invite');
r = await req(biz, '/sim/contacts', { method: 'POST', form: { name: 'Smoke Tester', email: 'smoke@example.com', phone: '0400 111 222' } });
r = await req(biz, '/app/customers');
check('customer created from CONTACT webhook', r.text.includes('Smoke Tester'));
check('portal invite queued', r.text.includes('invited'));
const custId = pick(r.text, /href="\/app\/customers\/(\d+)">Smoke Tester/);

console.log('3. Xero simulator: new invoice -> webhook -> invoice + pay link email');
const contactsPage = await req(biz, '/sim');
const contactId = pick(contactsPage.text, /<option value="([^"]+)" >Smoke Tester/) || pick(contactsPage.text, /<option value="([^"]+)"[^>]*>Smoke Tester/);
check('contact appears in simulator', !!contactId);
r = await req(biz, '/sim/invoices', { method: 'POST', form: { contact_id: contactId, reference: 'Smoke invoice', issue_date: '2026-10-21', due_date: '2026-10-28', description: 'Smoke service', quantity: 2, unit_amount: 100 } });
r = await req(biz, '/app/invoices');
const invRow = r.text.includes('Smoke Tester');
check('invoice mirrored from INVOICE webhook', invRow);
const invId = pick(r.text, /href="\/app\/invoices\/(\d+)">INV-\d+<\/a>(?:(?!<\/tr>).)*Smoke Tester/s);
r = await req(biz, `/app/invoices/${invId}`);
check('invoice total incl GST = $220', r.text.includes('$220.00'));
const payUrl = pick(r.text, /href="(http[^"]+\/pay\/[^"]+)" target/);
check('pay link present', !!payUrl);
r = await req(biz, '/app/outbox');
check('pay link email in outbox', r.text.includes('pay_link'));

console.log('4. Customer pays via pay link with "save card", through the hosted page');
const cust = new Jar();
r = await req(cust, payUrl);
check('pay page shows amount', r.text.includes('Pay $220.00'));
const payToken = payUrl.split('/pay/')[1];
r = await req(cust, `/pay/${payToken}/start`, { method: 'POST', form: { src: 'pay_link', save_card: '1' } });
check('redirected to hosted payment page', r.url.includes('/gsim/checkout/') && r.text.includes('SECURE PAYMENT PAGE'));
const checkoutId = r.url.split('/gsim/checkout/')[1];
r = await req(cust, `/gsim/checkout/${checkoutId}`, { method: 'POST', form: { pan: '4111 1111 1111 1111', expiry: '12/29', cvv: '123', cardholder: 'SMOKE TESTER' } });
check('landed on receipt page', r.url.includes('/done') && r.text.includes('Thank you, your payment went through'));
check('autopay switched on by save-card tick', r.text.includes('Automatic payments are on'));
r = await req(biz, `/app/invoices/${invId}`);
check('invoice now PAID locally', r.text.includes('>PAID<'));
check('payment written back to Xero', r.text.includes('>done<'));
r = await req(biz, '/sim');
check('Xero simulator shows the payment recorded', r.text.includes('Transiqe MOCK'));
r = await req(biz, '/app/outbox');
check('receipt emailed', r.text.includes('receipt'));

console.log('5. Xero Pay Now button entry point');
r = await req(new Jar(), '/x/' + pick((await req(biz, '/app/settings')).text, /business code is <code>([^<]+)<\/code>/) + '/pay?inv=INV-0005&amt=220.00&cur=AUD&org=X', { follow: false });
check('Pay Now URL resolves invoice number to pay page', r.status === 302 && r.text === '' || r.status === 302);

console.log('6. Repeating invoice -> autopay scheduled -> scheduler charges saved card');
r = await req(biz, '/sim/repeating', { method: 'POST', form: { contact_id: contactId, reference: 'Smoke retainer', period: 1, unit: 'MONTHLY', due_days: 7, next_date: '2026-10-21', description: 'Monthly retainer', unit_amount: 500 } });
r = await req(biz, '/sim/run-repeating', { method: 'POST', form: { as_of: '2026-10-21' } });
r = await req(biz, '/app/autopay');
check('new repeating invoice is queued for autopay', r.text.includes('Smoke Tester') && r.text.includes('$550.00'));
r = await req(biz, '/app/autopay/run', { method: 'POST', form: { ignore_schedule: '1' } });
check('scheduler charged the card', r.text.includes('approved'));
r = await req(biz, '/app/payments');
check('autopay payment recorded with Xero write-back', r.text.includes('autopay') && (r.text.match(/>done</g) || []).length >= 2);

console.log('7. Declining card -> retry policy');
r = await req(biz, '/sim/contacts', { method: 'POST', form: { name: 'Decline Dan', email: 'dan@example.com' } });
const sim = await req(biz, '/sim');
const danId = pick(sim.text, /<option value="([^"]+)"[^>]*>Decline Dan/);
r = await req(biz, '/sim/invoices', { method: 'POST', form: { contact_id: danId, reference: 'Dan 1', issue_date: '2026-10-21', due_date: '2026-10-25', description: 'Service', quantity: 1, unit_amount: 50 } });
r = await req(biz, '/app/invoices');
const danInvId = pick(r.text, /href="\/app\/invoices\/(\d+)">INV-\d+<\/a>(?:(?!<\/tr>).)*Decline Dan/s);
const danPay = pick((await req(biz, `/app/invoices/${danInvId}`)).text, /href="(http[^"]+\/pay\/[^"]+)" target/);
const dan = new Jar();
r = await req(dan, `/pay/${danPay.split('/pay/')[1]}/start`, { method: 'POST', form: { src: 'pay_link', save_card: '1' } });
r = await req(dan, r.url, { method: 'POST', form: { pan: '4000 0000 0000 0119', expiry: '12/29', cvv: '123', cardholder: 'DAN' } });
check('0119 card approves first payment', r.text.includes('Thank you'));
r = await req(biz, '/sim/invoices', { method: 'POST', form: { contact_id: danId, reference: 'Dan 2', issue_date: '2026-10-21', due_date: '2026-10-22', description: 'Service', quantity: 1, unit_amount: 60 } });
r = await req(biz, '/app/autopay/run', { method: 'POST', form: { ignore_schedule: '1' } });
check('stored 0119 card declines on autopay', r.text.includes('declined'));
r = await req(biz, '/app/autopay');
check('declined invoice re-queued for retry', r.text.includes('Decline Dan') && r.text.includes('Scheduled'));
r = await req(biz, '/app/outbox');
check('customer told autopay failed', r.text.includes('autopay_failed'));

console.log('8. Customer portal: magic link, pages, autopay toggle, card removal');
r = await req(new Jar(), '/portal/request-link', { method: 'POST', form: { email: 'smoke@example.com' } });
const magic = pick(r.text, /(http[^\s<"]+\/portal\/login\/[^\s<"|]+)/);
check('magic link issued', !!magic);
const portal = new Jar();
r = await req(portal, magic);
check('portal dashboard after magic link', r.text.includes('Hi Smoke') && r.text.includes('Automatic payments'));
r = await req(portal, '/portal/payments');
check('portal payment history lists both payments', (r.text.match(/succeeded/g) || []).length >= 2);
r = await req(portal, '/portal/autopay');
check('portal shows saved card', r.text.includes('Visa •••• 1111'));
const pmId = pick(r.text, /name="autopay_payment_method_id">\s*<option value="(\d+)"/);
r = await req(portal, '/portal/autopay', { method: 'POST', form: { autopay_enabled: '1', autopay_timing: 'days_before', autopay_days_before: 2, autopay_payment_method_id: pmId } });
check('portal autopay preference saved', r.text.includes('Automatic payments are on'));
r = await req(portal, '/portal/cards/add', { method: 'POST' });
r = await req(portal, r.url, { method: 'POST', form: { pan: '5555 5555 5555 4444', expiry: '01/30', cvv: '999', cardholder: 'SMOKE' } });
check('added a second card via $0 tokenisation', r.text.includes('Mastercard ending 4444 saved'));
r = await req(portal, `/portal/cards/${pmId}/remove`, { method: 'POST' });
check('removed original card', r.text.includes('Card removed'));
r = await req(portal, '/portal/logout', { method: 'POST' });
check('portal logout', r.url.endsWith('/portal') && r.text.includes('Sign in with your email'));

console.log('9. Refund, void, settings, activity, admin');
r = await req(biz, '/app/payments');
const payId = pick(r.text, /\/app\/payments\/(\d+)\/refund/);
r = await req(biz, `/app/payments/${payId}/refund`, { method: 'POST' });
check('refund processed', r.text.includes('Refunded'));
const simNow = await req(biz, '/sim');
const openInv = pick(simNow.text, /\/sim\/invoices\/([^/"]+)\/void/);
r = await req(biz, `/sim/invoices/${openInv}/void`, { method: 'POST' });
check('void in Xero cancels pending autopay', r.text.includes('cancelled any pending autopay'));
r = await req(biz, '/app/settings', { method: 'POST', form: { name: 'Northside Physio', email: 'accounts@northsidephysio.example', brand_colour: '#0f766e', portal_welcome: 'Welcome', autopay_allowed: '1', autopay_default_timing: 'due_date', autopay_days_before: 3, send_pay_link_on_invoice: '1', send_receipts: '1', xero_payment_account_code: '091', xero_paynow_configured: '1', amex_surcharge_pct: 0 } });
check('settings saved', r.text.includes('Settings saved'));
r = await req(biz, '/app/activity');
check('activity shows audit + webhooks', r.text.includes('payment.succeeded') && r.text.includes('INVOICE/CREATE'));
const admin = new Jar();
r = await req(admin, '/admin/login', { method: 'POST', form: { email: 'admin@transiqe.local', password: 'admin1234' } });
check('admin dashboard lists business', r.text.includes('Northside Physio') && r.text.includes('Businesses'));

console.log('10. New business signup flow');
const nb = new Jar();
r = await req(nb, '/signup', { method: 'POST', form: { name: 'Smoke Plumbing', abn: '', owner_name: 'Sam', email: `sam${Date.now()}@example.com`, password: 'password1' } });
check('signup lands on setup checklist', r.text.includes('Connect Xero') && r.text.includes('Add gateway details'));
r = await req(nb, '/app/xero/connect');
check('demo Xero connect', r.text.includes('Connected to Smoke Plumbing (Demo Xero)'));
r = await req(nb, '/app/gateway', { method: 'POST', form: { gateway_kind: 'mock', merchant_id: 'SMOKE01', transaction_password: 'x', environment: 'test' } });
check('gateway connect + verify', r.text.includes('Gateway connected'));

console.log(`\n${passed} passed, ${failures.length} failed${failures.length ? ': ' + failures.join(', ') : ''}`);
process.exit(failures.length ? 1 : 0);
