// Xero webhook processing. Xero sends thin events ({eventCategory, eventType,
// resourceId, tenantId}); we fetch the resource and run the sync logic.
// Events are stored first (idempotent on event_key) then processed, so a
// redelivery never double-sends a pay link or double-schedules autopay.
import { createHmac, timingSafeEqual } from 'node:crypto';
import { config } from '../config.js';
import { get, insert, now, update } from '../db.js';
import { xeroClient } from '../providers/index.js';
import { upsertContact, upsertInvoice } from './sync.js';

export function verifyXeroSignature(rawBody, signature) {
  if (!config.xero.webhookKey) return false;
  const expected = createHmac('sha256', config.xero.webhookKey).update(rawBody).digest('base64');
  const a = Buffer.from(expected); const b = Buffer.from(signature || '');
  return a.length === b.length && timingSafeEqual(a, b);
}

export async function ingestXeroEvents(events) {
  const out = [];
  for (const ev of events) {
    const key = `xero:${ev.tenantId}:${ev.eventCategory}:${ev.eventType}:${ev.resourceId}:${ev.eventDateUtc || ''}`;
    const conn = get('SELECT * FROM connections WHERE provider=? AND tenant_id=?', ['xero', ev.tenantId]);
    let id;
    try {
      id = insert('webhook_events', {
        business_id: conn?.business_id || null, provider: 'xero', event_key: key,
        category: ev.eventCategory, type: ev.eventType, resource_id: ev.resourceId,
        payload_json: JSON.stringify(ev), received_at: now(),
      });
    } catch {
      out.push({ key, status: 'duplicate' });
      continue; // duplicate delivery
    }
    if (!conn) { update('webhook_events', id, { status: 'ignored', error: 'Unknown tenant', processed_at: now() }); continue; }
    try {
      const business = get('SELECT * FROM businesses WHERE id=?', [conn.business_id]);
      const x = xeroClient(conn);
      if (ev.eventCategory === 'CONTACT') {
        const c = await x.contact(ev.resourceId);
        if (c) upsertContact(business, c);
      } else if (ev.eventCategory === 'INVOICE') {
        const i = await x.invoice(ev.resourceId);
        if (i) upsertInvoice(business, i);
      }
      update('webhook_events', id, { status: 'processed', processed_at: now() });
      out.push({ key, status: 'processed' });
    } catch (e) {
      update('webhook_events', id, { status: 'failed', error: e.message, processed_at: now() });
      out.push({ key, status: 'failed', error: e.message });
    }
  }
  return out;
}
