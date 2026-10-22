// Central configuration. Everything comes from environment variables with
// sensible demo defaults so `npm run dev` works with zero setup.
import { randomBytes } from 'node:crypto';

const env = process.env;

export const config = {
  // 'demo' uses the built-in Xero simulator and mock NAB gateway.
  // 'live' uses the real Xero OAuth2 API and the NAB Transact adapter.
  mode: env.APP_MODE || 'demo',
  port: Number(env.PORT || 3000),
  baseUrl: env.BASE_URL || `http://localhost:${env.PORT || 3000}`,
  appName: env.APP_NAME || 'PayBridge',
  dbPath: env.DB_PATH || './data/paybridge.db',

  // 32+ char secret. Used for session signing and AES-256-GCM encryption of
  // gateway credentials and Xero refresh tokens at rest.
  appSecret: env.APP_SECRET || 'demo-only-secret-change-me-before-live-use-0000',

  // Platform admin login (super admin across all tenants)
  adminEmail: env.ADMIN_EMAIL || 'admin@paybridge.local',
  adminPassword: env.ADMIN_PASSWORD || 'admin1234',

  xero: {
    clientId: env.XERO_CLIENT_ID || '',
    clientSecret: env.XERO_CLIENT_SECRET || '',
    redirectUri: env.XERO_REDIRECT_URI || `${env.BASE_URL || 'http://localhost:3000'}/app/xero/callback`,
    webhookKey: env.XERO_WEBHOOK_KEY || '',
    scopes: 'openid profile email offline_access accounting.transactions accounting.contacts accounting.settings',
  },

  // NAB Transact (or whichever NAB gateway product NAB provisions).
  // Per-business credentials are stored encrypted in the DB; these are only
  // environment-level defaults such as the test endpoint.
  nab: {
    testEndpoint: env.NAB_TEST_ENDPOINT || 'https://transact.nab.com.au/test/xmlapi/payment',
    liveEndpoint: env.NAB_LIVE_ENDPOINT || 'https://transact.nab.com.au/live/xmlapi/payment',
    testPeriodicEndpoint: env.NAB_TEST_PERIODIC_ENDPOINT || 'https://transact.nab.com.au/xmlapi/periodic',
    livePeriodicEndpoint: env.NAB_LIVE_PERIODIC_ENDPOINT || 'https://transact.nab.com.au/xmlapi/periodic',
    hostedPaymentUrl: env.NAB_HOSTED_URL || 'https://transact.nab.com.au/live/hpp/payment',
  },

  // Scheduler: how often to look for autopay charges that are due.
  jobIntervalMs: Number(env.JOB_INTERVAL_MS || 60_000),
  jobToken: env.JOB_TOKEN || randomBytes(8).toString('hex'),

  // Autopay retry policy
  autopay: {
    maxAttempts: 3,
    retryDays: 2,
  },
};

export const isDemo = () => config.mode !== 'live';
