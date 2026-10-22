import express from 'express';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { config } from './src/config.js';
import './src/db.js';
import { attachIdentity } from './src/auth.js';
import { router as publicRoutes } from './src/routes/public.js';
import { router as appRoutes } from './src/routes/app.js';
import { router as payRoutes } from './src/routes/pay.js';
import { router as portalRoutes } from './src/routes/portal.js';
import { router as simRoutes } from './src/routes/sim.js';
import { router as webhookRoutes } from './src/routes/webhooks.js';
import { router as adminRoutes } from './src/routes/admin.js';
import { retryWritebacks, runAutopay } from './src/services/payments.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
export const app = express();
app.disable('x-powered-by');
app.set('trust proxy', true);

app.use(webhookRoutes);                      // raw body, before urlencoded parsing
app.use(express.urlencoded({ extended: false }));
app.use(express.static(join(__dirname, 'public'), { maxAge: '1h' }));
app.use(attachIdentity);
app.use(publicRoutes);
app.use('/app', appRoutes);
app.use(payRoutes);
app.use('/portal', portalRoutes);
app.use(simRoutes);
app.use(adminRoutes);
app.get('/health', (req, res) => res.json({ ok: true, mode: config.mode, time: new Date().toISOString() }));

app.use((err, req, res, next) => { // eslint-disable-line no-unused-vars
  console.error(err);
  res.status(500).send(`<pre>Something went wrong: ${String(err.message)}</pre>`);
});

// In-process scheduler (for long-running hosts). Serverless hosts call POST /jobs/run instead.
async function tick() {
  try { await runAutopay(); await retryWritebacks(); } catch (e) { console.error('scheduler error', e); }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  app.listen(config.port, () => {
    console.log(`${config.appName} running in ${config.mode} mode at ${config.baseUrl}`);
    setInterval(tick, config.jobIntervalMs).unref();
  });
}
