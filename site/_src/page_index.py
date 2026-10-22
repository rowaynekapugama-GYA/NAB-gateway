extra = """<style>
.hero{padding:70px 0 40px}
.hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
@media(max-width:960px){.hero .wrap{grid-template-columns:1fr}}
.hero h1{max-width:12ch}
.hero .actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.hero .proof{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}

/* the flow: invoice from Xero, paid by card, back into Xero */
.flow{position:relative;height:420px}
.flow .node{position:absolute;padding:18px 20px;width:250px;border-radius:24px}
.flow .node .t{font:600 13px var(--font-body);color:var(--ink-3);margin-bottom:6px}
.flow .node .v{font:700 20px var(--font-display);letter-spacing:-.03em}
.flow .xero{left:0;top:30px}
.flow .bank{right:0;top:30px;text-align:right}
.flow .result{left:50%;transform:translateX(-50%);bottom:10px;width:300px;text-align:center}
.flow .wire{position:absolute;left:125px;right:125px;top:84px;height:3px;border-radius:3px;background:linear-gradient(90deg,rgba(59,91,255,.15),rgba(25,198,192,.15))}
.flow .card{position:absolute;top:58px;left:110px;width:88px;height:56px;border-radius:12px;background:linear-gradient(135deg,#0B1026,#2A3568);color:#fff;box-shadow:0 20px 40px -14px rgba(11,16,38,.6);padding:10px 12px;font:600 10px var(--font-body);animation:ride 6s cubic-bezier(.65,0,.35,1) infinite}
.flow .card i{display:block;width:22px;height:16px;border-radius:4px;background:linear-gradient(135deg,#FFD66B,#F2A93B);margin-bottom:8px}
.flow .status{display:inline-flex;align-items:center;gap:8px;margin-top:10px;font-weight:700;color:#117A50}
.flow .status .tick{width:22px;height:22px;border-radius:50%;background:var(--mint);color:#fff;display:grid;place-items:center;font-size:13px;transform:scale(0);animation:pop 6s ease infinite}
.flow .pulse{position:absolute;left:50%;top:84px;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--cobalt);box-shadow:0 0 0 0 rgba(59,91,255,.5);animation:ping 6s ease-out infinite}
.flow .drop{animation:drop 6s ease infinite}
@keyframes ride{0%,12%{transform:translateX(0);opacity:0}18%{opacity:1}55%{transform:translateX(300px);opacity:1}62%,100%{transform:translateX(300px);opacity:0}}
@keyframes ping{0%,50%{box-shadow:0 0 0 0 rgba(59,91,255,.45)}70%,100%{box-shadow:0 0 0 24px rgba(59,91,255,0)}}
@keyframes pop{0%,60%{transform:scale(0)}68%{transform:scale(1.15)}72%,95%{transform:scale(1)}100%{transform:scale(0)}}
@keyframes drop{0%,58%{opacity:0;transform:translate(-50%,16px)}66%,95%{opacity:1;transform:translate(-50%,0)}100%{opacity:0}}
@media(max-width:560px){.flow{height:470px}.flow .node{width:46%}.flow .wire{left:46%;right:46%}.flow .card{left:40%}.flow .result{width:90%}}

.strip{padding:10px 0 20px}
.strip .row{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
@media(max-width:860px){.steps{grid-template-columns:1fr}}
.step{padding:28px}
.step .n{width:34px;height:34px;border-radius:50%;background:var(--abyss);color:#fff;display:grid;place-items:center;font:700 14px var(--font-display);margin-bottom:16px}
.step p{color:var(--ink-2)}
.showcase{padding:30px;border-radius:var(--r-xl)}
.showcase .screen{transform:perspective(1600px) rotateX(2deg);transition:transform .4s}
.showcase:hover .screen{transform:perspective(1600px) rotateX(0)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
@media(max-width:900px){.split{grid-template-columns:1fr}}
.fee{padding:32px}
.fee ul.plain{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:14px}
.fee li{padding-top:14px;border-top:1px solid var(--glass-line);color:var(--ink-2)}
.fee li b{color:var(--abyss);display:block;font-family:var(--font-display);letter-spacing:-.02em;margin-bottom:4px}
.cta-block{padding:54px;text-align:center;display:grid;justify-items:center;gap:18px}
.faq details{padding:18px 24px;margin-bottom:10px}
.faq summary{cursor:pointer;font-weight:700;font-family:var(--font-display);letter-spacing:-.02em;font-size:17px;list-style:none;display:flex;justify-content:space-between;align-items:center}
.faq summary::after{content:"+";font-size:22px;color:var(--cobalt)}
.faq details[open] summary::after{content:"–"}
.faq details p{margin-top:10px;color:var(--ink-2);max-width:70ch}
</style>"""

body = """
<section class="hero"><div class="wrap">
  <div>
    <span class="chip"><span class="dot"></span>Live for Xero. Settles to your NAB account.</span>
    <h1 style="margin-top:22px">Get paid by card, straight from Xero.</h1>
    <p class="lede" style="margin-top:20px">Transiqe connects your Xero invoices to your own bank's card gateway. Customers pay in one tap or switch on autopay, and every payment lands back in Xero as reconciled. No middleman holding your money, no per-invoice margin.</p>
    <div class="actions"><a class="btn primary lg" href="signup.html">Start free</a><a class="btn glassy lg" href="features.html">See how it works</a></div>
    <div class="proof"><span class="chip">No surcharge, ever</span><span class="chip">Same-day settlement with NAB</span><span class="chip">Cards never touch us</span></div>
  </div>
  <div class="flow" aria-hidden="true">
    <div class="node glass sm xero"><div class="t">New invoice in Xero</div><div class="v">INV-0238 · $121.00</div><div class="tiny muted">Priya Sharma · due 25 Oct</div></div>
    <div class="node glass sm bank"><div class="t">Your NAB gateway</div><div class="v">Approved</div><div class="tiny muted">Visa •••• 1111 · settles today</div></div>
    <div class="wire"></div><div class="pulse"></div>
    <div class="card"><i></i>•••• 1111</div>
    <div class="node glass sm result drop"><div class="t">Back in Xero</div><div class="v">INV-0238 paid</div><div class="status"><span class="tick">✓</span>Reconciled, receipt sent</div></div>
  </div>
</div></section>

<section class="strip"><div class="wrap"><div class="row">
  <span class="chip">Pay-by-card link on every invoice</span><span class="chip">Customer portal for every contact</span><span class="chip">Autopay on due date</span><span class="chip">Repeating invoices handled</span><span class="chip">Written back to Xero</span>
</div></div></section>

<section><div class="wrap">
  <div class="section-head"><h2>Three connections. Then it runs itself.</h2><p class="lede">Setup takes an afternoon, mostly waiting on your bank. After that, Transiqe watches Xero and does the chasing.</p></div>
  <div class="steps">
    <div class="step glass sm"><div class="n">1</div><h3>Connect Xero</h3><p>Authorise Transiqe once. We read your contacts and invoices, and we record payments against invoices when they're paid. Nothing else changes in Xero.</p></div>
    <div class="step glass sm"><div class="n">2</div><h3>Connect your bank gateway</h3><p>Enter the merchant ID and password NAB gives you. Card details are entered on the bank's own secure page, and settlements go to your NAB account the same day.</p></div>
    <div class="step glass sm"><div class="n">3</div><h3>Add the Pay now button</h3><p>Paste one link into Xero's payment services. From then on every invoice, including the ones from repeating templates, has a card button and a customer portal behind it.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><h2>One screen for what's paid, what's due and what's on autopay.</h2><p class="lede">Every card payment, every scheduled charge and every Xero write-back in one place, so you never wonder whether a payment made it into the books.</p></div>
  <div class="showcase glass">{dashboard}</div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><h2>Built for the way small businesses actually invoice.</h2></div>
  <div class="grid c3">
    <div class="card glass sm"><div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 10h20"/></svg></div><h3>Pay by card, no surcharge</h3><p>From 1 October 2026 card surcharges are banned in Australia. Transiqe never adds one. The only card fee is the one on your own merchant facility, with your bank.</p></div>
    <div class="card glass sm"><div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="9"/></svg></div><h3>Autopay on the due date</h3><p>Customers save a card once and choose when they're charged: on issue, on the due date, or a few days before. Retainers and repeating invoices just get paid.</p></div>
    <div class="card glass sm"><div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12l5 5L20 6"/></svg></div><h3>Reconciled in Xero</h3><p>Every successful payment is recorded against its invoice in Xero within seconds, referenced with the bank transaction ID, so your bank feed matches first time.</p></div>
    <div class="card glass sm"><div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6"/></svg></div><h3>A portal for every customer</h3><p>When a contact is created in Xero, their portal already exists. They sign in with an emailed link, see every invoice, pay, and manage their saved cards.</p></div>
    <div class="card glass sm"><div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v16H4z"/><path d="M8 12h8M8 8h8M8 16h5"/></svg></div><h3>Receipts and reminders handled</h3><p>Pay links when invoices are issued, receipts when they're paid, a friendly note and a retry when a card declines. You see every email in the outbox.</p></div>
    <div class="card glass sm"><div class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7l8-4z"/></svg></div><h3>Cards never touch Transiqe</h3><p>Your customers type card numbers on the bank's hosted page. We keep only the token the bank hands back, which keeps you and us out of card-data compliance headaches.</p></div>
  </div>
</div></section>

<section><div class="wrap split">
  <div>
    <h2>Your customers get the easy version.</h2>
    <p class="lede" style="margin-top:16px">One tap from the invoice email, or a portal where everything is in one place. No account to create, no password to forget, no surcharge at the end.</p>
    <div style="margin-top:22px;display:grid;gap:10px">
      <span class="chip">Sign in with an emailed link</span><span class="chip">See every open and paid invoice</span><span class="chip">Save a card, set autopay timing, remove it any time</span>
    </div>
    <a class="btn glassy" style="margin-top:24px" href="customers.html">See the customer side</a>
  </div>
  <div class="glass showcase" style="padding:24px">{pay}</div>
</div></section>

<section><div class="wrap split">
  <div class="fee glass">
    <h3>What stays with your bank</h3>
    <ul class="plain">
      <li><b>The rate.</b> Card payments are processed on your own merchant facility, at the rate your bank agreed with you. Transiqe doesn't add a percentage, a per-transaction fee or a margin on top.</li>
      <li><b>The money.</b> Settlement goes from your customer's card to your bank account on your bank's timetable. Transiqe never holds funds in between.</li>
      <li><b>The relationship.</b> Your merchant agreement, your statements, your bank's support line. If you ever leave Transiqe, nothing about how you get paid changes.</li>
    </ul>
  </div>
  <div>
    <h2>One bank, one rate, no one in the middle.</h2>
    <p class="lede" style="margin-top:16px">Most pay-by-card tools sit between you and your money. Transiqe is software that connects Xero to the merchant facility you already have with your bank, and puts the automation on top. The card fee is whatever your bank charges you, and nothing else.</p>
    <a class="btn primary" style="margin-top:24px" href="pricing.html">See pricing</a>
  </div>
</div></section>

<section><div class="wrap"><div class="cta-block glass">
  <h2 style="max-width:18ch;text-align:center">Try it with your own Xero this week.</h2>
  <p class="lede" style="text-align:center">Free while you set up. Connect Xero in two minutes, add your NAB details when they arrive, and send your first pay-by-card invoice.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center"><a class="btn primary lg" href="signup.html">Create your account</a><a class="btn glassy lg" href="mailto:hello@transiqe.com">Talk to us</a></div>
</div></div></section>

<section class="faq"><div class="wrap" style="max-width:820px">
  <div class="section-head"><h2>Questions we get asked</h2></div>
  <details class="glass sm"><summary>Do I need a NAB account?</summary><p>You need a NAB merchant facility (NAB Transact), which NAB sets up for you. It settles to any Australian bank account, though NAB's best rate and same-day settlement apply when it settles to a NAB business account. Other banks' gateways are on the roadmap.</p></details>
  <details class="glass sm"><summary>Does Transiqe hold my money?</summary><p>No. Card payments go from your customer to your merchant facility and settle to your bank account. Transiqe only moves the information: the invoice to the customer, the payment back to Xero.</p></details>
  <details class="glass sm"><summary>What happens with repeating invoices?</summary><p>Xero generates them like any other invoice, so Transiqe sees them the same way. If the customer has autopay on, the invoice is charged on the schedule they chose. If not, they get a pay link.</p></details>
  <details class="glass sm"><summary>What if a customer's card declines?</summary><p>They get an email with a link to pay another way or update the card. Transiqe retries every two days, up to three attempts, then stops and tells you both. The invoice stays open in Xero the whole time.</p></details>
  <details class="glass sm"><summary>Can I still surcharge?</summary><p>Not on eftpos, Visa or Mastercard. The Reserve Bank's ban started on 1 October 2026, so Transiqe never applies a surcharge to those. American Express is outside the ban, and you can set an Amex-only cost-recovery fee if your facility accepts it.</p></details>
  <details class="glass sm"><summary>Is my bookkeeper going to hate this?</summary><p>They'll see payments appear against invoices in Xero with the bank reference in the description, recorded to the account you choose (your bank account or a clearing account). Nothing else in Xero changes.</p></details>
</div></section>
""".replace('{dashboard}', partial('screen_dashboard')).replace('{pay}', partial('screen_pay'))

page('index', 'Transiqe: card payments and autopay for Xero invoices, through your own bank',
     'Connect Xero to your NAB card gateway. Pay-by-card links, a customer portal, autopay on due dates and automatic reconciliation in Xero. No surcharges, no middleman.',
     body, active='', extra_css=extra)
