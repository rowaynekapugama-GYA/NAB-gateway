# Transiqe: workflows, decisions and open questions

## 1. The problem in one line

Xero + Pinch works but Pinch's per-transaction fees are too high. Replace Pinch with the business's own NAB merchant facility (NAB Transact or whichever gateway product NAB provisions), keep everything else the business and its customers are used to, and make it a product any small business can sign up to.

## 2. Actors and their screens

| Actor | Where | What they do |
|---|---|---|
| Business owner / bookkeeper | `/app` | Sign up, connect Xero, enter NAB credentials, watch invoices and payments, manage customers and autopay, settings |
| Customer of the business | `/pay/<token>` and `/portal` | Pay a single invoice; see all invoices, save a card, set up autopay, view history |
| Xero | webhooks + API | Source of truth for contacts and invoices; receives payments back |
| NAB gateway | hosted page + API | Takes the card, issues a token, charges the token later, settles to the business's account |
| Platform admin (you) | `/admin` | See every business, sign in as one for support |

## 3. The workflows

### 3.1 Business onboarding
1. Sign up (business name, owner email, password). A business record, a short code (used in the Xero Pay Now URL) and an owner user are created.
2. Connect Xero: standard OAuth 2.0 consent flow with `offline_access`, `accounting.transactions`, `accounting.contacts`, `accounting.settings`. We store the refresh token encrypted and the tenant ID. Immediately after connecting we do a full sync of customers (contacts) and open invoices. The full sync does **not** send pay links (so connecting does not spam existing customers); the business can press "Sync now" with notifications on if they want to.
3. Connect NAB: merchant ID, SecureXML transaction password, hosted-page password, test/live. Stored AES-256-GCM encrypted. We run an Echo request to verify.
4. Paste the Pay Now custom payment URL into Xero (Settings → Payment services → Custom payment URL) and assign it to the invoice branding theme. This is a manual step in Xero's UI; Xero has no API for it.

### 3.2 New customer in Xero → portal exists
- Xero fires `CONTACT/CREATE`. We fetch the contact, create a `customers` row with a portal token.
- If the contact has an email, we send a portal invite (magic link). If not, the customer still exists and the business can add an email in our UI (without touching Xero) and invite later.
- The portal is per business. If one person is a customer of two businesses on the platform, they get two portals; the Account page lists the other businesses and lets them request a link.

### 3.3 New invoice in Xero (manual or from a repeating invoice)
- Xero fires `INVOICE/CREATE` (and `UPDATE` when approved). Repeating invoices generate normal invoices, so this path covers both. We only act on `ACCREC` invoices in `AUTHORISED` status with an amount due.
- Decision:
  - customer has **autopay on and a saved card** → schedule a charge for the customer's timing (on issue / due date / N days before). No pay-link email; they get a receipt after the charge.
  - otherwise → email a pay link (if the business setting is on and the customer has an email).
- Invoice updates (`VOIDED`, `PAID` in Xero by other means, amount changed) are mirrored and any pending autopay is cancelled when the invoice stops being payable.

### 3.4 Pay once by card
Three entry points, same page:
- the pay-link email → `/pay/<token>`
- Xero's own online invoice Pay Now button → `/x/<business code>/pay?inv=[INVOICENUMBER]&amt=[AMOUNTDUE]&cur=[CURRENCY]&org=[SHORTCODE]` → we look the invoice up by number (fetching from Xero on the fly if the webhook has not arrived yet) → `/pay/<token>`
- the portal's Pay now button

Flow: pay page shows the live amount due (always from our mirror, never from the URL, so a tampered `amt` cannot underpay) → optional "save this card and autopay future invoices" tick → redirect to NAB's hosted payment page with a signed return URL → NAB redirects back → we verify the signature on our own return parameters and the gateway's result → record payment → write Payment to Xero → receipt email → thank-you page. The return leg is idempotent (refreshing the page does not double-record).

### 3.5 Autopay
- Enabling: tick on the pay page while paying, or in the portal (add a card via a $0 tokenisation on the hosted page, then switch on). Business staff can also set it from the customer page once a card exists; the customer's own choice always wins.
- Timing options: on issue, on due date (default), N days before due. Business sets the default; customer can override.
- Scheduler: every `JOB_INTERVAL_MS` (and/or `POST /jobs/run` from a cron) picks invoices whose `autopay_next_attempt_at` has passed and charges the stored token via the Periodic/trigger API.
- Failure: customer emailed, retry in 2 days, max 3 attempts, then stop and alert both parties. Invoice stays open with a pay link. (Configurable in `config.autopay`.)
- Changing the preference re-plans all open invoices. Removing the autopay card turns autopay off.

### 3.6 Write-back and reconciliation
- A successful charge creates a Xero **Payment** against the invoice for the full amount, dated today, against a configurable account (default: a "NAB Transact Clearing" account; the business bank account also works). Reference is `Transiqe <gateway txn id>` so it is searchable.
- Recommended bookkeeping: NAB settles gross to the bank and bills merchant fees separately, so recording at face value is correct. If NAB batches settlements, a clearing account makes the bank feed reconcile cleanly (one bank line vs one clearing-account transfer per settlement).
- If write-back fails (Xero down, token revoked, invoice edited) the payment is still recorded here, the business is alerted, and the scheduler retries.
- Refunds go to the card via the gateway; recording the refund in Xero is manual for now (overpayment/credit note handling is a later step).

### 3.7 Customer portal
Magic-link sign in (email a single-use 7-day link; no passwords). Pages: invoices awaiting payment (with autopay dates), payment history, autopay and cards, account. Branded with the business's colour and logo.

## 4. Key design decisions and why

- **Hosted payment page, not our own card form.** Keeps the platform out of PCI DSS scope beyond SAQ A, which is what makes a self-serve multi-tenant product feasible. Autopay works off NAB's stored-card token, never a PAN.
- **Each business uses its own NAB merchant facility.** That is what removes the Pinch margin: no platform in the money flow, no payfac licence needed, settlements go straight to the business. The trade-off is each business must apply to NAB for a facility (NAB currently quotes $30/month for up to $2,000 turnover then 1.5% per transaction when settling to a NAB account) and configure it. The onboarding checklist and the gateway page list exactly what they need from NAB.
- **Xero is the source of truth.** We never create invoices; we mirror them and push payments back. This keeps bookkeepers happy and means the business keeps working exactly as before.
- **No card surcharges.** The RBA ban on surcharging eftpos/Visa/Mastercard started 1 October 2026, which also removes the "customer pays the fee" model Pinch offered. The only allowed surcharge left is on American Express (outside the ban); there is a setting for that if NAB enables Amex.
- **Demo mode with faithful simulators.** The Xero simulator fires the same webhook shape as real Xero and the mock gateway follows the same hosted-page → token → trigger shape as NAB Transact, so the UI, data model and edge cases (declines, voids, retries, duplicate webhooks) can all be tested now, before NAB's pack arrives.
- **Idempotent webhooks and return legs.** Xero batches and redelivers; customers refresh pages. Both are safe.

## 5. What is simulated vs real

| Piece | Status |
|---|---|
| Business dashboard, portal, pay pages, settings, admin | Real, working |
| Data model, sessions, encryption, audit log, outbox | Real |
| Xero OAuth, API client, webhook signature verification | Real code, untested against live Xero (needs a Xero app client ID) |
| NAB Transact adapter | Request builders written against the public SecureXML/Periodic/HPP formats; items marked `VERIFY` in the file must be checked against NAB's pack |
| Email delivery | Outbox table; `deliver()` hook to connect SMTP2GO/Postmark |
| Database | SQLite (fine for a pilot); swap `src/db.js` for Postgres before scale |

## 6. Open questions for NAB (ask when their details arrive)

1. Which product exactly: NAB Transact (hosted payment page + SecureXML + Periodic) or the newer NAB Gateway? The adapter assumes NAB Transact.
2. Hosted Payment Page: exact field list, fingerprint recipe, and whether `store_card`/tokenisation is returned on the HPP response or requires a separate Periodic `add` call.
3. Stored-card charging: Periodic `trigger` by `clientID` (CRN), or a token-based SecureXML payment? Field names for the response.
4. 3-D Secure requirements for the first (customer-present) payment, and whether merchant-initiated autopay charges are exempt.
5. Test environment credentials and the exact test/live endpoint URLs.
6. Settlement timing and whether settlements are batched (affects the clearing-account recommendation).
7. Whether one platform can register many merchants (each business signs its own merchant agreement with NAB; we need to know the onboarding path to tell businesses).
8. Refund API availability and partial refunds.

## 7. Open questions for you

1. Product name and domain (Transiqe is a placeholder).
2. Pricing model for the platform (monthly per business, per-transaction cents, or tiered) since there is no margin on the card fee itself.
3. Should the platform support gateways other than NAB later (e.g. CommBank, Westpac)? The adapter interface already allows it.
4. Direct debit (bank account) as a second payment method through NAB? Common ask for larger recurring amounts.
5. Multi-user per business (staff logins with roles) is stubbed (`users.role`) but there is no invite UI yet.
