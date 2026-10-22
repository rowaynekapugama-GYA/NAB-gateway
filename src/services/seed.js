// Creates a demo business with a simulated Xero org, a mock NAB gateway,
// three customers and a handful of invoices so the dashboard has life in it.
// Runs from `npm run seed` and automatically on boot when AUTO_SEED=1.
import { get, insert, now, run, today, update } from '../db.js';
import { encrypt, hashPassword, shortCode } from '../crypto.js';
import { xeroMock } from '../providers/index.js';
import { ingestXeroEvents } from './webhooks.js';
import { savePaymentMethod } from './payments.js';

export const DEMO_EMAIL = 'demo@paybridge.local';
export const DEMO_PASSWORD = 'demo1234';

export async function seedDemo() {
const EMAIL = DEMO_EMAIL;
if (get('SELECT id FROM users WHERE email=?', [EMAIL])) return false;

const business_id = insert('businesses', {
  name: 'Northside Physio', slug: 'northside-physio', short_code: shortCode(6), abn: '12 345 678 901',
  email: 'accounts@northsidephysio.example', phone: '02 9000 0000', brand_colour: '#0f766e',
  settings_json: JSON.stringify({ autopay_default_timing: 'due_date', xero_payment_account_code: '091', portal_welcome: 'Pay your physio invoices by card and set up automatic payments so you never miss a due date.' }),
  created_at: now(),
});
insert('users', { business_id, email: EMAIL, name: 'Dana Demo', password_hash: hashPassword('demo1234'), role: 'owner', created_at: now() });
const business = get('SELECT * FROM businesses WHERE id=?', [business_id]);

// Xero (simulated) + gateway (mock)
const org = xeroMock.ensureOrg(business.name);
insert('connections', { business_id, provider: 'xero', status: 'connected', tenant_id: org.tenant_id, tenant_name: org.name, connected_at: now(), last_sync_at: now() });
insert('connections', { business_id, provider: 'gateway', status: 'connected', gateway_kind: 'mock', merchant_id: 'DEMO0001', credentials_enc: encrypt(JSON.stringify({ transaction_password: 'demo' })), environment: 'test', connected_at: now() });

const t = org.tenant_id;
const d = (n) => xeroMock.addDays(today(), n);
const line = (description, unit_amount, quantity = 1) => ({ description, quantity, unit_amount, tax_type: 'OUTPUT' });

const priya = xeroMock.createContact(t, { name: 'Priya Sharma', email: 'priya@example.com', phone: '0400 000 001' });
const marcus = xeroMock.createContact(t, { name: 'Marcus Bell', email: 'marcus@example.com', phone: '0400 000 002' });
const olive = xeroMock.createContact(t, { name: 'Olive & Co Pty Ltd', email: 'accounts@oliveandco.example', phone: null });

xeroMock.createInvoice(t, { contact_id: priya.contact_id, reference: 'Initial consult', issue_date: d(-20), due_date: d(-13), lines: [line('Initial consultation', 120)] });
xeroMock.createInvoice(t, { contact_id: priya.contact_id, reference: 'Follow-up', issue_date: d(-3), due_date: d(4), lines: [line('Standard consultation', 95), line('Exercise band', 15)] });
xeroMock.createInvoice(t, { contact_id: marcus.contact_id, reference: 'Rehab block', issue_date: d(-1), due_date: d(13), lines: [line('Rehabilitation program (6 sessions)', 540)] });
xeroMock.createInvoice(t, { contact_id: olive.contact_id, reference: 'Workplace assessments', issue_date: d(-10), due_date: d(-2), lines: [line('Ergonomic assessment', 380, 3)] });
xeroMock.createRepeating(t, { contact_id: olive.contact_id, reference: 'Monthly wellbeing program', period: 1, unit: 'MONTHLY', due_days: 14, next_date: today(), lines: [line('Monthly onsite wellbeing program', 1200)] });

// Deliver the webhooks so the platform mirrors everything.
const pending = xeroMock.pendingEvents(t);
await ingestXeroEvents(pending.map((e) => ({ resourceId: e.resource_id, eventType: e.type, eventCategory: e.category, tenantId: t, eventDateUtc: e.created_at })));
xeroMock.markDelivered(pending.map((e) => e.id));

// Marcus already saved a card and turned on autopay (simulating a previous payment).
const marcusC = get('SELECT * FROM customers WHERE business_id=? AND xero_contact_id=?', [business_id, marcus.contact_id]);
const tok = 'tok_seed_marcus';
insert('gsim_tokens', { merchant_id: 'DEMO0001', token: tok, card_brand: 'Visa', last4: '1111', expiry_month: 12, expiry_year: 2029, cardholder: 'MARCUS BELL', behaviour: 'approve', created_at: now() });
const pm = savePaymentMethod(business, marcusC, { gateway_token: tok, card_brand: 'Visa', last4: '1111', expiry_month: 12, expiry_year: 2029, cardholder: 'MARCUS BELL' });
update('customers', marcusC.id, { autopay_enabled: 1, autopay_payment_method_id: pm.id, portal_status: 'active' });
const marcusInv = get('SELECT * FROM invoices WHERE customer_id=?', [marcusC.id]);
update('invoices', marcusInv.id, { autopay_scheduled_for: marcusInv.due_date, autopay_next_attempt_at: marcusInv.due_date + 'T00:00:00.000Z' });
run('DELETE FROM outbox WHERE business_id=? AND kind=?', [business_id, 'pay_link']); // keep the demo outbox tidy; invites remain

return true;
}
