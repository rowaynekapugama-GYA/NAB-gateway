// Real Xero webhook endpoint (live mode). Xero's "Intent to receive"
// check requires: 200 with empty body when the signature is valid, 401 when
// it is not. Processing happens after we respond so Xero never times out.
import { Router, raw } from 'express';
import { config } from '../config.js';
import { ingestXeroEvents, verifyXeroSignature } from '../services/webhooks.js';
import { runAutopay, retryWritebacks } from '../services/payments.js';

export const router = Router();

router.post('/webhooks/xero', raw({ type: '*/*', limit: '2mb' }), (req, res) => {
  const body = req.body.toString('utf8');
  if (!verifyXeroSignature(body, req.get('x-xero-signature'))) return res.status(401).end();
  res.status(200).end();
  let payload;
  try { payload = JSON.parse(body); } catch { return; }
  setImmediate(() => ingestXeroEvents(payload.events || []).catch((e) => console.error('webhook processing error', e)));
});

// Cron entry point for serverless hosts (Vercel Cron, Cloud Scheduler).
// Protected by JOB_TOKEN; the in-process scheduler calls the same functions.
router.post('/jobs/run', async (req, res) => {
  if (req.get('authorization') !== `Bearer ${config.jobToken}`) return res.status(401).end();
  const autopay = await runAutopay();
  const writebacks = await retryWritebacks();
  res.json({ autopay, writebacks_retried: writebacks });
});
