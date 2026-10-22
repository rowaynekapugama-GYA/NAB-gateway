# Developer handover

Read this with `README.md` (how to run it) and `WORKFLOWS.md` (what it does and why). This document is the technical map: architecture, data model, request flows, integration contracts, and what has to happen before go-live.

## 1. What you are inheriting

A working multi-tenant Node.js application that sits between Xero and a business's NAB card gateway. It is deliberately dependency-light so it is easy to read and move:

- Node 22.13+ (uses built-in `node:sqlite`, `fetch`, `crypto`)
- Express 4 for routing, server-rendered HTML (no front-end framework, no template engine, no build step)
- SQLite for storage (one file, WAL mode)
- Two provider interfaces (Xero, payment gateway), each with a real and a simulated implementation

Everything in the demo path is real code except the two external systems, which are swapped in by `APP_MODE`. The business dashboard, customer portal, pay pages, scheduler, webhook ingestion, write-back, audit log and outbox are the production code paths.

## 2. Architecture

```
                 +------------------+        OAuth2 / REST / webhooks        +-----------+
   browser  ---> |  Express app     | <------------------------------------> |   Xero    |
   (business,    |  server.js       |                                        +-----------+
    customer,    |                  |     hosted page redirect + XML API      +-----------+
    admin)       |  routes/ -> services/ -> providers/ -> db.js  <--------->  | NAB gateway|
                 +------------------+                                        +-----------+
                        |  setInterval / POST /jobs/run
                        v
                  scheduler: runAutopay(), retryWritebacks()
```

Layering rule: **routes** parse requests and render HTML; **services** hold business logic and are the only layer that writes to the ledger tables; **providers** talk to external systems and know nothing about our tables except what they are handed; **db.js** owns the schema.

### Files

| File | Responsibility |
|---|---|
| `server.js` | Mounts routes, static files, error handler, in-process scheduler |
| `src/config.js` | All environment variables with demo defaults; `isDemo()` |
| `src/db.js` | Schema (created on boot, idempotent), `run/get/all/insert/update/tx` helpers, `audit()`, `settings(business)` |
| `src/crypto.js` | AES-256-GCM `encrypt/decrypt`, scrypt passwords, HMAC `sign/verifySigned`, random tokens |
| `src/auth.js` | Cookie sessions (three kinds: `user`, `customer`, `admin`), flash messages, `require*` guards |
| `src/layout.js` | HTML shells (`appPage`, `portalPage`, `plainPage`), `table`, `field`, `badge`, money/date formatters |
| `src/providers/index.js` | Picks mock vs live for a given connection |
| `src/providers/xero/live.js` | OAuth2 auth URL, code exchange, token refresh, Accounting API client |
| `src/providers/xero/mock.js` | In-DB Xero organisation with contacts, invoices, repeating invoices, payments, webhook queue |
| `src/providers/gateway/nabtransact.js` | NAB Transact: Echo, hosted page URL builder, HPP return parsing, Periodic trigger, refund |
| `src/providers/gateway/mock.js` | Mock gateway with hosted page, tokens, test-card behaviours |
| `src/services/sync.js` | `upsertContact`, `upsertInvoice` (the "what do we do with a new invoice" decision), `fullSync`, `refreshInvoice` |
| `src/services/payments.js` | `recordPayment`, `writeBackToXero`, `retryWritebacks`, `chargeInvoiceWithSavedCard`, `runAutopay`, `refundPayment`, `savePaymentMethod` |
| `src/services/webhooks.js` | Xero signature check, idempotent `ingestXeroEvents` |
| `src/services/notifications.js` | Every outbound email, via the `outbox` table; `deliver()` is the single hook for a real mailer |
| `src/routes/*.js` | See route map below |
| `scripts/seed.js` | Demo business + data; `scripts/reset.js` wipes the DB; `scripts/smoke.js` end-to-end test |

## 3. Data model

All tables are in `src/db.js`. Money is stored as REAL in dollars, rounded to cents in code (`round()`), which is fine for AUD invoices; move to integer cents if you add multi-currency.

Core tables:

- `businesses`: a tenant. `short_code` is used in the Xero Pay Now URL. `settings_json` holds per-tenant options (defaults in `settings()` in db.js).
- `users`: logins for a business (role column exists, only `owner` is used so far).
- `connections`: one row per `(business, provider)` where provider is `xero` or `gateway`. Secrets (`access_token_enc`, `refresh_token_enc`, `credentials_enc`) are AES-GCM encrypted with `APP_SECRET`.
- `customers`: mirror of a Xero contact plus portal and autopay state. `autopay_payment_method_id` is the card that will be charged.
- `invoices`: mirror of a Xero ACCREC invoice plus `pay_token` (public pay-link id) and the autopay schedule fields (`autopay_scheduled_for`, `autopay_next_attempt_at`, `autopay_attempts`, `autopay_last_error`).
- `payment_methods`: stored-card tokens from the gateway. Never a PAN. `status` is `active` or `removed`.
- `payments`: our ledger. One row per gateway attempt (succeeded or failed). `xero_writeback_status` is `pending`, `done`, `failed` or `n/a`.
- `webhook_events`: every Xero event, unique on `event_key`, so redeliveries are no-ops.
- `magic_links`, `sessions`: portal sign-in and cookie sessions.
- `outbox`: every email with full HTML, for delivery and for the dashboard.
- `audit_log`: who did what. Call `audit()` for anything a support person would want to see.

Simulator tables (`xsim_*`, `gsim_*`) exist only for demo mode and can be dropped in production.

Invariants worth keeping:

- An invoice is payable only when `status='AUTHORISED' AND amount_due>0`. Every pay path and the scheduler checks this.
- `autopay_next_attempt_at` is the single source of truth for "the scheduler should try this". Clearing it cancels autopay for the invoice.
- `payments.gateway_txn_id` is unique in practice; the hosted-page return handler uses it for idempotency.

## 4. Route map

Public:

| Method | Path | Purpose |
|---|---|---|
| GET/POST | `/signup`, `/login`, `/logout` | Business accounts |
| GET | `/x/:code/pay?inv=&amt=&cur=&org=` | Entry from Xero's Pay Now button. Looks invoice up by number (fetching from Xero if not synced yet), redirects to `/pay/:token`. `amt` is never trusted. |
| GET | `/pay/:token` | Pay page for one invoice |
| POST | `/pay/:token/start` | Creates a gateway checkout, redirects to hosted page |
| GET | `/pay/:token/return?i=&s=&checkout=` | Return from hosted page. `i` is a signed intent (`invoiceId:saveCard:source:ts`), `s` its HMAC. Records payment, saves card, writes back, redirects to `/done`. Idempotent. |
| GET | `/pay/:token/done` | Thank-you page |
| GET/POST | `/portal`, `/portal/request-link`, `/portal/login/:token`, `/portal/logout` | Customer sign-in (magic link) |
| POST | `/webhooks/xero` | Xero webhook (raw body, HMAC check, 200/401, async processing) |
| POST | `/jobs/run` | Cron entry point, `Authorization: Bearer JOB_TOKEN` |
| GET | `/health` | Liveness |

Business dashboard (`/app/*`, requires user session): overview, `xero/connect`, `xero/callback`, `xero/sync`, `xero/disconnect`, `gateway` (GET/POST), `gateway/verify`, `invoices`, `invoices/:id` (+ `/send`, `/charge`, `/cancel-autopay`), `customers`, `customers/:id` (+ `/invite`, `/autopay`, `/cards/:mid/remove`), `payments`, `payments/:id/refund`, `autopay`, `autopay/run` (demo), `outbox`, `outbox/:id`, `activity`, `settings` (GET/POST).

Customer portal (`/portal/*`, requires customer session): `/` invoices, `/payments`, `/autopay` (GET/POST), `/cards/add`, `/cards/return`, `/cards/:id/remove`, `/account`.

Demo only: `/sim/*` (Xero simulator, requires business login) and `/gsim/checkout/:id` (mock hosted page, public).

Admin: `/admin/login`, `/admin`, `/admin/impersonate/:id`.

## 5. Request flows in detail

### 5.1 Xero webhook → invoice → action
1. Xero POSTs `{events:[{resourceId, eventCategory, eventType, tenantId, eventDateUtc}]}` with header `x-xero-signature` (base64 HMAC-SHA256 of the raw body using the webhook key).
2. `routes/webhooks.js` verifies with the raw body, replies immediately, then calls `ingestXeroEvents` on `setImmediate`.
3. `ingestXeroEvents` inserts a `webhook_events` row keyed on tenant+category+type+resource+date; a duplicate insert means "already handled". It finds the `connections` row by `tenant_id`, fetches the resource with the live client, and calls `upsertContact` or `upsertInvoice`.
4. `upsertInvoice` on a **new** AUTHORISED invoice: if the customer has `autopay_enabled` and a card, it computes the charge date from the customer's timing (falling back to the business default) and sets `autopay_next_attempt_at`; otherwise it emails a pay link (if the business setting allows and the customer has an email). On an **existing** invoice it mirrors the new state and clears autopay if the invoice stopped being payable.

### 5.2 Pay once (hosted page)
1. `/pay/:token/start` builds a signed return URL and calls `gateway.createCheckout({amount, reference, returnUrl, tokenise})`. Mock returns a local URL; NAB adapter returns the HPP URL with fingerprint.
2. Customer pays on the hosted page. Gateway redirects to `returnUrl&checkout=<id>` (mock) or with NAB's own result parameters (live).
3. `/pay/:token/return` verifies `s` over `i`, calls `gateway.completeCheckout(checkoutId, query)` which normalises the result to `{approved, txnId, code, message, card, token}`. If `token` is present and the customer ticked save, `savePaymentMethod` stores it and autopay is switched on; other open invoices for that customer are scheduled.
4. `recordPayment` writes the `payments` row, optimistically marks the invoice paid, calls `writeBackToXero` (creates a Xero Payment), then sends the receipt.

### 5.3 Autopay
`runAutopay()` selects invoices with `autopay_next_attempt_at <= now` whose customer has autopay on, then `chargeInvoiceWithSavedCard` → `gateway.chargeToken` → `recordPayment`. On decline: increment attempts, set the next attempt in `config.autopay.retryDays`, email the customer; after `maxAttempts`, stop and alert the business. Runs from `setInterval` in `server.js` and from `POST /jobs/run`.

### 5.4 Add a card without paying
Portal → `/portal/cards/add` → `createCheckout` with `amount: 0, tokenise: true` → hosted page → `/portal/cards/return` → `savePaymentMethod`. Note for NAB: confirm whether a $0 tokenisation is supported on the HPP or whether it must be a Periodic `add` with a small verification amount.

## 6. Provider contracts

Both gateway implementations expose:

```js
verifyCredentials() -> { ok, message }
createCheckout({ amount, currency, reference, description, returnUrl, tokenise }) -> { checkoutId, redirectUrl }
completeCheckout(checkoutId, returnParams) -> { approved, txnId, code, message, card:{brand,last4}, token:{gateway_token, card_brand, last4, expiry_month, expiry_year, cardholder}|null }
chargeToken({ token, amount, currency, reference }) -> { approved, txnId, code, message }
refund({ txnId, amount, reference }) -> { approved, txnId, code, message }
```

Both Xero implementations expose:

```js
organisation(), contacts(), contact(id), invoices(), invoice(id), invoiceByNumber(number), accounts()
createPayment({ invoiceId, accountCode, amount, date, reference }) -> { PaymentID }
```

Adding another bank's gateway later means one new file in `src/providers/gateway/` and one line in `providers/index.js`.

## 7. Security notes

- Card data never touches the app. Only gateway tokens are stored.
- Gateway credentials and Xero refresh tokens are encrypted at rest; `APP_SECRET` must be long, random and kept out of the repo. Rotating it requires re-encrypting the `connections` table.
- Return URLs from the hosted page carry an HMAC-signed intent, so a forged return cannot mark an invoice paid; `completeCheckout` must still validate the gateway's own response signature in live mode (marked `VERIFY` in the NAB adapter).
- Pay links and portal tokens are 96-bit random; magic links are single use and expire in 7 days.
- Cookies are `HttpOnly; SameSite=Lax`. Add `Secure` once behind HTTPS (one line in `auth.js`).
- The `amt` parameter from Xero's Pay Now URL is ignored; the amount always comes from our mirror of the invoice.
- CSRF: forms are same-origin and cookies are SameSite=Lax, which blocks cross-site POSTs in modern browsers. Add a CSRF token if you need to support older browsers.

## 8. Before go-live checklist

1. Confirm NAB product and fill the `VERIFY` items in `nabtransact.js`: endpoint URLs, HPP parameter names and fingerprint recipe, how the stored-card token is returned, Periodic `trigger` request/response fields, response signature validation.
2. Create the Xero app (Web app, OAuth 2.0), set `XERO_CLIENT_ID/SECRET/REDIRECT_URI`, register `/webhooks/xero` for Contacts and Invoices, set `XERO_WEBHOOK_KEY`, pass Xero's "Intent to receive" check. Note: Xero webhooks require a public HTTPS URL; use ngrok or a staging host for development.
3. Implement `deliver()` in `notifications.js` against the chosen mailer (SMTP2GO is already used elsewhere by GYA). Add a plain-text alternative to each email.
4. Decide on the database. SQLite is fine for a pilot on a single host with persistent disk. For Vercel/serverless or multiple instances, swap `db.js` for Postgres (Supabase). Only `db.js` and the few `substr()` SQL calls need changing.
5. Set `APP_MODE=live`, `BASE_URL` to the public HTTPS origin, a real `APP_SECRET`, `JOB_TOKEN`, and admin credentials.
6. Set up the scheduler: either keep the in-process timer on a long-running host, or a cron hitting `POST /jobs/run` every few minutes.
7. Add `Secure` to cookies, put the app behind HTTPS, set `trust proxy` correctly for the host.
8. Run `npm run smoke` in demo mode after any change; then repeat the same journey manually against NAB's test environment with their test cards.

## 9. Known gaps and suggested next steps

- Refunds are sent to the card but not recorded in Xero (needs a credit note or overpayment flow).
- Partial payments are supported in the data model but the UI always charges the full amount due.
- No staff invite UI (users table supports it).
- No rate limiting on `/portal/request-link` or `/login`; add before public launch.
- Emails are HTML only.
- Direct debit (bank account) is not implemented; the gateway interface could carry it if NAB offers it.
- Tests: `scripts/smoke.js` is an integration test against a running server. Unit tests for `sync.js` and `payments.js` would be the next most valuable addition.
