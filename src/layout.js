// Minimal server-side HTML helpers. No template engine needed.
import { config, isDemo } from './config.js';

export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
export const money = (n, cur = 'AUD') => new Intl.NumberFormat('en-AU', { style: 'currency', currency: cur || 'AUD' }).format(Number(n || 0));
export const date = (s) => (s ? new Date(String(s).length === 10 ? s + 'T00:00:00' : s).toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' }) : '');
export const datetime = (s) => (s ? new Date(s).toLocaleString('en-AU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '');

export function badge(status) {
  const map = {
    AUTHORISED: 'blue', PAID: 'green', VOIDED: 'grey', DELETED: 'grey', DRAFT: 'grey', SUBMITTED: 'grey',
    succeeded: 'green', failed: 'red', refunded: 'amber', pending: 'amber', done: 'green', 'n/a': 'grey',
    connected: 'green', disconnected: 'red', invited: 'amber', active: 'green', none: 'grey', processed: 'green', received: 'amber',
    sent: 'green', queued: 'amber', ignored: 'grey', duplicate: 'grey',
  };
  return `<span class="badge ${map[status] || 'grey'}">${esc(status === 'AUTHORISED' ? 'Awaiting payment' : status)}</span>`;
}

export function flashHtml(flash) {
  return flash ? `<div class="flash ${esc(flash.type)}">${esc(flash.text)}</div>` : '';
}

const head = (title, brand) => `<!doctype html><html lang="en-AU"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)} · ${esc(config.appName)}</title>
<link rel="icon" href="/favicon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="/style.css">${brand ? `<style>:root{--brand:${esc(brand)}}</style>` : ''}</head>`;

const demoBanner = () => (isDemo() ? `<div class="demo-banner">Demo mode: Xero and the NAB gateway are simulated. Open the <a href="/sim">Xero simulator</a> to create contacts and invoices.</div>` : '');

// Business dashboard shell
export function appPage({ title, business, user, body, flash, active }) {
  const nav = [
    ['/app', 'Overview', 'overview'], ['/app/invoices', 'Invoices', 'invoices'], ['/app/customers', 'Customers', 'customers'],
    ['/app/payments', 'Payments', 'payments'], ['/app/autopay', 'Autopay', 'autopay'], ['/app/outbox', 'Outbox', 'outbox'],
    ['/app/activity', 'Activity', 'activity'], ['/app/settings', 'Settings', 'settings'],
  ];
  return `${head(title)}<body class="app">
${demoBanner()}
<div class="shell"><aside class="side">
  <div class="logo">${esc(config.appName)}</div>
  <div class="biz"><div class="biz-name">${esc(business.name)}</div><div class="muted small">${esc(user.email)}</div></div>
  <nav>${nav.map(([h, l, k]) => `<a href="${h}" class="${active === k ? 'on' : ''}">${l}</a>`).join('')}</nav>
  <div class="side-foot">${isDemo() ? '<a href="/sim">Xero simulator</a>' : ''}<form method="post" action="/logout"><button class="link">Sign out</button></form></div>
</aside><main class="main"><h1>${esc(title)}</h1>${flashHtml(flash)}${body}</main></div></body></html>`;
}

// Customer portal shell (branded per business)
export function portalPage({ title, business, customer, body, flash, active }) {
  const nav = customer ? [['/portal', 'Invoices', 'invoices'], ['/portal/payments', 'Payments', 'payments'], ['/portal/autopay', 'Autopay & cards', 'autopay'], ['/portal/account', 'Account', 'account']] : [];
  return `${head(title, business?.brand_colour)}<body class="portal">
${demoBanner()}
<header class="ptop"><div class="wrap"><div class="pbrand">${business?.logo_url ? `<img src="${esc(business.logo_url)}" alt="">` : ''}<span>${esc(business?.name || config.appName)}</span></div>
${customer ? `<nav>${nav.map(([h, l, k]) => `<a href="${h}" class="${active === k ? 'on' : ''}">${l}</a>`).join('')}<form method="post" action="/portal/logout"><button class="link">Sign out</button></form></nav>` : ''}</div></header>
<main class="wrap"><h1>${esc(title)}</h1>${flashHtml(flash)}${body}</main>
<footer class="pfoot wrap muted small">Secure card payments via ${esc(business?.name || 'the business')}'s NAB merchant facility. Card details are entered on the bank's page and never stored by ${esc(config.appName)}.</footer>
</body></html>`;
}

// Plain centred shell (login, signup, pay page, errors)
export function plainPage({ title, body, flash, brand, wide = false }) {
  return `${head(title, brand)}<body class="plain">${demoBanner()}<main class="centre ${wide ? 'wide' : ''}">${flashHtml(flash)}${body}</main></body></html>`;
}

export function table(headers, rows, empty = 'Nothing here yet.') {
  if (!rows.length) return `<p class="muted">${esc(empty)}</p>`;
  return `<table><thead><tr>${headers.map((h) => `<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
}

export function field(label, name, { type = 'text', value = '', required = false, placeholder = '', help = '', options = null, step = null } = {}) {
  const id = `f_${name}`;
  let input;
  if (options) {
    input = `<select id="${id}" name="${name}">${options.map(([v, l]) => `<option value="${esc(v)}" ${String(v) === String(value) ? 'selected' : ''}>${esc(l)}</option>`).join('')}</select>`;
  } else if (type === 'textarea') {
    input = `<textarea id="${id}" name="${name}" rows="3">${esc(value)}</textarea>`;
  } else {
    input = `<input id="${id}" type="${type}" name="${name}" value="${esc(value)}" ${required ? 'required' : ''} placeholder="${esc(placeholder)}" ${step ? `step="${step}"` : ''}>`;
  }
  return `<label class="field"><span>${esc(label)}</span>${input}${help ? `<small class="muted">${help}</small>` : ''}</label>`;
}

export function stat(label, value, sub = '') {
  return `<div class="stat"><div class="stat-v">${value}</div><div class="stat-l">${esc(label)}</div>${sub ? `<div class="muted small">${sub}</div>` : ''}</div>`;
}
