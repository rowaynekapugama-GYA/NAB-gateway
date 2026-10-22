// All outbound email goes through the outbox table. In demo mode nothing is
// actually sent; the business dashboard shows the outbox so you can click the
// links. In live mode wire `deliver()` to SMTP2GO, Postmark, SES etc.
import { config } from '../config.js';
import { insert, now, get, settings, update } from '../db.js';
import { token } from '../crypto.js';

const money = (n, cur = 'AUD') => new Intl.NumberFormat('en-AU', { style: 'currency', currency: cur }).format(n || 0);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function queue(business, to, subject, bodyHtml, kind) {
  const id = insert('outbox', {
    business_id: business.id, to_email: to.email, to_name: to.name, subject, body_html: bodyHtml, kind, created_at: now(),
  });
  deliver(id).catch(() => {});
  return id;
}

async function deliver(id) {
  // Hook for a real email provider. For now mark as sent immediately.
  update('outbox', id, { status: 'sent', sent_at: now() });
}

export function payLinkUrl(invoice) {
  return `${config.baseUrl}/pay/${invoice.pay_token}`;
}

export function portalLoginUrl(customer) {
  // Create a single-use magic link valid for 7 days.
  const t = token();
  insert('magic_links', { customer_id: customer.id, token: t, expires_at: new Date(Date.now() + 7 * 864e5).toISOString(), created_at: now() });
  return `${config.baseUrl}/portal/login/${t}`;
}

function shell(business, inner) {
  return `<div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;color:#222">
  <div style="background:${esc(business.brand_colour)};color:#fff;padding:16px 20px;border-radius:8px 8px 0 0"><strong>${esc(business.name)}</strong></div>
  <div style="border:1px solid #e5e5e5;border-top:0;padding:20px;border-radius:0 0 8px 8px">${inner}
  <p style="color:#777;font-size:12px;margin-top:24px">Payments are processed securely through ${esc(business.name)}'s NAB merchant facility. Card details are never stored by ${esc(config.appName)}.</p></div></div>`;
}

export function sendPayLink(business, customer, invoice) {
  const url = payLinkUrl(invoice);
  const html = shell(business, `
    <p>Hi ${esc(customer.name)},</p>
    <p>Invoice <strong>${esc(invoice.number)}</strong> for <strong>${money(invoice.amount_due, invoice.currency)}</strong> is due on ${esc(invoice.due_date)}.</p>
    <p><a href="${url}" style="background:${esc(business.brand_colour)};color:#fff;padding:12px 20px;border-radius:6px;text-decoration:none;display:inline-block">Pay by card</a></p>
    <p>You can also view all your invoices and set up automatic payments in your <a href="${portalLoginUrl(customer)}">customer portal</a>.</p>`);
  update('invoices', invoice.id, { pay_link_sent_at: now() });
  return queue(business, customer, `Invoice ${invoice.number} from ${business.name}: ${money(invoice.amount_due, invoice.currency)}`, html, 'pay_link');
}

export function sendPortalInvite(business, customer) {
  const s = settings(business);
  const html = shell(business, `
    <p>Hi ${esc(customer.name)},</p>
    <p>${esc(business.name)} now offers a secure online portal where you can view invoices, pay by card and switch on automatic payments so you never miss a due date.</p>
    <p>${esc(s.portal_welcome)}</p>
    <p><a href="${portalLoginUrl(customer)}" style="background:${esc(business.brand_colour)};color:#fff;padding:12px 20px;border-radius:6px;text-decoration:none;display:inline-block">Open your portal</a></p>`);
  update('customers', customer.id, { portal_status: customer.portal_status === 'active' ? 'active' : 'invited', invited_at: now() });
  return queue(business, customer, `Your ${business.name} customer portal`, html, 'portal_invite');
}

export function sendMagicLink(business, customer) {
  const html = shell(business, `
    <p>Hi ${esc(customer.name)},</p>
    <p>Use the link below to sign in to your ${esc(business.name)} portal. It is valid for 7 days and can be used once.</p>
    <p><a href="${portalLoginUrl(customer)}" style="background:${esc(business.brand_colour)};color:#fff;padding:12px 20px;border-radius:6px;text-decoration:none;display:inline-block">Sign in</a></p>`);
  return queue(business, customer, `Sign in to your ${business.name} portal`, html, 'magic_link');
}

export function sendReceipt(business, customer, invoice, payment) {
  const html = shell(business, `
    <p>Hi ${esc(customer.name)},</p>
    <p>Thanks, we received your payment of <strong>${money(payment.amount, payment.currency)}</strong> for invoice <strong>${esc(invoice.number)}</strong>.</p>
    <table style="font-size:14px"><tr><td>Reference</td><td>${esc(payment.gateway_txn_id)}</td></tr>
    <tr><td>Date</td><td>${esc(payment.created_at.slice(0, 10))}</td></tr>
    <tr><td>Method</td><td>${esc(payment.source === 'autopay' ? 'Automatic card payment' : 'Card')}</td></tr></table>`);
  return queue(business, customer, `Receipt for invoice ${invoice.number}`, html, 'receipt');
}

export function sendAutopayFailed(business, customer, invoice, message, willRetry) {
  const html = shell(business, `
    <p>Hi ${esc(customer.name)},</p>
    <p>We tried to collect <strong>${money(invoice.amount_due, invoice.currency)}</strong> for invoice <strong>${esc(invoice.number)}</strong> from your saved card, but the payment was not approved (${esc(message)}).</p>
    <p>${willRetry ? 'We will try again in a couple of days.' : 'We have stopped automatic attempts for this invoice.'} You can pay now or update your card in your <a href="${portalLoginUrl(customer)}">customer portal</a>.</p>`);
  return queue(business, customer, `Action needed: payment for invoice ${invoice.number} did not go through`, html, 'autopay_failed');
}

export function notifyBusiness(business, subject, bodyText) {
  if (!business.email) return null;
  return queue(business, { email: business.email, name: business.name }, subject, shell(business, `<p>${esc(bodyText)}</p>`), 'business_alert');
}
