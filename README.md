# Transiqe

Bridge between Xero and a business's own NAB merchant facility. Any small business signs up, connects Xero, enters their NAB gateway credentials, and from then on:

- every Xero invoice (including ones generated from repeating invoices) gets a **Pay by card** link emailed to the customer, and the **Pay Now** button on Xero's own online invoice points here too
- every Xero contact gets a **customer portal** (magic-link sign in, no passwords) where they can see invoices, pay, save a card and switch on **autopay**
- customers on autopay are **charged automatically** when their Xero invoices fall due (or on issue, or N days before)
- every successful card payment is **written back to Xero** as a Payment, so the invoice shows as paid and bank reconciliation is automatic
- receipts, failed-payment notices and retries are handled for them

Funds settle straight to the business's NAB account. The platform never sees card numbers: the customer enters them on NAB's hosted page and we keep only the token NAB returns.

## Run it (demo mode, no credentials needed)

```bash
npm install
npm run dev       # http://localhost:3000  (demo data is seeded automatically on first start)
npm run smoke     # optional: scripted end-to-end test of every workflow (server must be running)
```

To put the demo online without installing anything, use the **Deploy to Render** button (free tier, uses `render.yaml`):

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/rowaynekapugama-GYA/NAB-gateway)

Sign in at `/login` with **demo@transiqe.local / demo1234**. Platform admin is at `/admin` (admin@transiqe.local / admin1234).

In demo mode Xero and NAB are simulated in-process:

- **Xero simulator** (`/sim`): create contacts, invoices and repeating invoices; run the "overnight job"; void invoices. Each action fires the same webhook events real Xero sends.
- **Mock NAB hosted page** (`/gsim/checkout/...`): test cards `4111 1111 1111 1111` (approve), `4000 0000 0000 0002` (decline), `4000 0000 0000 0119` (approve now, stored card declines later), `4000 0000 0000 9995` (insufficient funds).
- **Outbox** (`/app/outbox`): every email the platform would send, with clickable links so you can walk the customer journey.
- **Autopay** page has a "Run scheduler now" button so you don't have to wait for due dates.

Suggested 5-minute tour:

1. Sign in, look at Overview, then open the Xero simulator and create a contact with an email. Check Customers (portal invite queued) and Outbox.
2. Create an invoice for that contact. Check Invoices and open the pay-link email in the Outbox.
3. Open the pay link, tick "save this card", pay with 4111... Watch the invoice go PAID, the payment appear in Payments with Xero write-back "done", and the simulator's "Payments recorded in Xero" table.
4. Create a repeating invoice for the same contact and run the overnight job. The new invoice is queued on the Autopay page. Press "Run scheduler now" and it is charged from the saved card.
5. In the portal (request a sign-in link at `/portal` with the contact's email), toggle autopay timing, add a second card, remove one.

## Going live

Set `APP_MODE=live` and the variables in `.env.example`:

1. **Xero app**: create one at developer.xero.com (Web app, OAuth 2.0). Redirect URI `https://<host>/app/xero/callback`. Register the webhook `https://<host>/webhooks/xero` for Contacts and Invoices and copy the webhook key. One app serves every business on the platform.
2. **NAB**: each business enters its own merchant ID and passwords on `/app/gateway`. They are stored encrypted (AES-256-GCM with `APP_SECRET`). `src/providers/gateway/nabtransact.js` has the request builders; lines marked `VERIFY` must be checked against the integration pack NAB is sending (field names, endpoint URLs, fingerprint recipe, stored-card response fields).
3. **Email**: `src/services/notifications.js` `deliver()` is the single hook; point it at SMTP2GO/Postmark/SES.
4. **Database**: `src/db.js` is SQLite via Node's built-in `node:sqlite` (Node 22.13+). Every query goes through four helpers so swapping to Postgres/Supabase is contained to that file.
5. **Scheduler**: on a long-running host the in-process timer runs every `JOB_INTERVAL_MS`. On serverless (Vercel), point a cron at `POST /jobs/run` with `Authorization: Bearer $JOB_TOKEN`.

## Layout

```
server.js                     express app, routes, scheduler
src/config.js                 env config, demo/live switch
src/db.js                     schema + tiny query helpers (SQLite)
src/crypto.js                 AES-GCM encryption, password hashing, signed tokens
src/auth.js                   cookie sessions for business users, customers, admin
src/layout.js                 HTML shells and helpers (no template engine)
src/providers/xero/live.js    real Xero OAuth2 + Accounting API
src/providers/xero/mock.js    Xero simulator (demo)
src/providers/gateway/nabtransact.js   NAB Transact adapter (live)
src/providers/gateway/mock.js          mock gateway + fake hosted page (demo)
src/services/sync.js          contact/invoice mirroring and the "new invoice" decision
src/services/payments.js      record payment, Xero write-back, autopay runner, refunds
src/services/webhooks.js      Xero webhook verification and idempotent ingestion
src/services/notifications.js outbox/email
src/routes/public.js          landing, signup, login
src/routes/app.js             business dashboard
src/routes/pay.js             pay link, Xero Pay Now entry, hosted-page return
src/routes/portal.js          customer portal
src/routes/sim.js             demo simulators
src/routes/webhooks.js        /webhooks/xero and /jobs/run
src/routes/admin.js           platform admin
scripts/seed.js, reset.js, smoke.js
docs/WORKFLOWS.md             the workflows, decisions and open questions
```
