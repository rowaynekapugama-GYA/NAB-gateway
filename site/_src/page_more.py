css = """<style>
.pagehead{padding:70px 0 30px}
.pagehead h1{max-width:16ch;font-size:clamp(36px,5vw,60px)}
.plans{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;align-items:stretch}
@media(max-width:900px){.plans{grid-template-columns:1fr}}
.plan{padding:32px;display:grid;gap:14px;align-content:start}
.plan .price{font:700 44px var(--font-display);letter-spacing:-.04em}
.plan .price small{font:600 15px var(--font-body);color:var(--ink-3);letter-spacing:0}
.plan ul{margin:0;padding:0;list-style:none;display:grid;gap:8px;color:var(--ink-2);font-size:15px}
.plan li::before{content:"✓ ";color:var(--cobalt);font-weight:800}
.plan.hot{outline:2px solid rgba(59,91,255,.45);outline-offset:-2px}
.note{padding:28px;margin-top:24px;color:var(--ink-2)}
.timeline{display:grid;gap:12px;max-width:760px}
.timeline .t{display:grid;grid-template-columns:150px 1fr;gap:18px;padding:18px 22px}
.timeline .t b{font-family:var(--font-display);letter-spacing:-.02em}
.sec{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:800px){.sec{grid-template-columns:1fr}}
.feature-list{display:grid;gap:14px}
.feature-list .row{display:grid;grid-template-columns:44px 1fr;gap:16px;padding:20px 22px}
</style>"""

pricing = """
<section class="pagehead"><div class="wrap"><h1>Software pricing. The card fee stays your bank's.</h1>
<p class="lede" style="margin-top:18px">Transiqe charges a flat monthly fee for the automation. Your merchant facility is your own agreement with your bank, at your bank's rate, settling to your account. We never take a percentage of your invoices.</p></div></section>
<section style="padding-top:10px"><div class="wrap">
<div class="plans">
  <div class="plan glass sm"><h3>Starter</h3><div class="price">$29 <small>/ month</small></div><p class="muted">For sole traders and small practices sending a handful of invoices a week.</p>
    <ul><li>Up to 100 invoices a month</li><li>Pay-by-card links and Xero Pay now button</li><li>Customer portal and autopay</li><li>Reconciliation in Xero</li><li>Email support</li></ul><a class="btn glassy block" href="signup.html">Start free</a></div>
  <div class="plan glass sm hot"><h3>Growth</h3><div class="price">$79 <small>/ month</small></div><p class="muted">For busy practices and service businesses with retainers and repeating invoices.</p>
    <ul><li>Up to 1,000 invoices a month</li><li>Everything in Starter</li><li>Custom branding on portal and emails</li><li>Multiple staff logins</li><li>Priority support, same business day</li></ul><a class="btn primary block" href="signup.html">Start free</a></div>
  <div class="plan glass sm"><h3>Multi-site</h3><div class="price">Let's talk</div><p class="muted">For groups with several Xero organisations or several merchant facilities.</p>
    <ul><li>Unlimited invoices</li><li>Several Xero organisations under one login</li><li>Several merchant facilities</li><li>Onboarding call and bookkeeper training</li><li>Direct line to the team</li></ul><a class="btn glassy block" href="mailto:hello@transiqe.com">Contact us</a></div>
</div>
<div class="note glass sm"><h3 style="margin-bottom:8px">Your card fee stays with your bank</h3>
<p>Transiqe is a flat software subscription. Card payments run on your own merchant facility under your own agreement with your bank, at the rate they give you, settling to your account. We don't take a percentage of your invoices and we don't add anything on top of your bank's fee.</p></div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><h2>Getting set up, start to finish</h2></div>
  <div class="timeline">
    <div class="t glass sm"><b>Day 1</b><span>Create your account and connect Xero. Your contacts and open invoices appear in the dashboard. Nothing is emailed to customers yet.</span></div>
    <div class="t glass sm"><b>Day 1 to 10</b><span>Apply for NAB Transact if you don't have it. NAB sends a merchant ID and passwords. Paste them into Transiqe; we verify the connection on the spot.</span></div>
    <div class="t glass sm"><b>Same day</b><span>Paste the Pay now link into Xero's payment services and assign it to your invoice theme. Send a test invoice to yourself and pay it with NAB's test card.</span></div>
    <div class="t glass sm"><b>Ongoing</b><span>Invoices go out with a card button, customers switch on autopay, payments land in Xero. You check the dashboard when you feel like it.</span></div>
  </div>
</div></section>
"""

customers = """
<section class="pagehead"><div class="wrap"><h1>For the people paying you.</h1>
<p class="lede" style="margin-top:18px">Your customers never hear the word Transiqe unless they look for it. They see your name, your invoice, and the simplest way to pay it.</p></div></section>
<section style="padding-top:10px"><div class="wrap sec">
  <div class="glass" style="padding:24px">{pay}</div>
  <div class="feature-list">
    <div class="row glass sm"><div class="icon" style="margin:0"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12l5 5L20 6"/></svg></div><div><h4>One tap from the email</h4><p class="muted">The invoice email has a Pay by card button. The pay page shows the invoice, the amount, and one button. No account needed.</p></div></div>
    <div class="row glass sm"><div class="icon" style="margin:0"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7l8-4z"/></svg></div><div><h4>Card entered on the bank's page</h4><p class="muted">The card form is NAB's, not ours and not yours. If they save the card, the bank keeps it and we keep a reference, never the number.</p></div></div>
    <div class="row glass sm"><div class="icon" style="margin:0"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="9"/></svg></div><div><h4>Autopay they can switch off</h4><p class="muted">Customers choose whether to save a card and when it's charged. They can change the card or turn autopay off from the portal at any time, and every charge sends a receipt.</p></div></div>
    <div class="row glass sm"><div class="icon" style="margin:0"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 10h20"/></svg></div><div><h4>No surcharge, no surprises</h4><p class="muted">The amount on the invoice is the amount charged. Card surcharges on eftpos, Visa and Mastercard are banned in Australia and Transiqe never adds one.</p></div></div>
  </div>
</div></section>
<section><div class="wrap">
  <div class="section-head"><h2>The portal, when they want the full picture</h2><p class="lede">Every open invoice, every receipt, saved cards and autopay settings. Sign in is a link emailed to them, valid once, so there's no password to look after.</p></div>
  <div class="glass" style="padding:30px">{portal}</div>
  <p style="margin-top:20px"><a class="btn glassy" href="portal.html">Open the customer portal</a></p>
</div></section>
""".replace('{pay}', partial('screen_pay')).replace('{portal}', partial('screen_portal'))

security = """
<section class="pagehead"><div class="wrap"><h1>Built so card numbers never reach us.</h1>
<p class="lede" style="margin-top:18px">The design choice that matters most is the one you don't see: every card is entered on the bank's own hosted page. Everything else follows from that.</p></div></section>
<section style="padding-top:10px"><div class="wrap grid c2">
  <div class="card glass sm"><h3>Card data</h3><p>Customers type card details on NAB's hosted payment page. The bank returns a token for saved cards; Transiqe stores the token, the last four digits and the expiry, never the card number or security code. This keeps you and Transiqe in the lightest PCI DSS category.</p></div>
  <div class="card glass sm"><h3>Your money</h3><p>Transiqe never holds funds. Card payments settle from your merchant facility to your bank account under your own agreement with NAB. If Transiqe disappeared tomorrow, your money would still be in your account.</p></div>
  <div class="card glass sm"><h3>Credentials at rest</h3><p>Your gateway passwords and the Xero connection tokens are encrypted with AES-256-GCM before they're stored, and decrypted only in memory when a request to the bank or Xero is made.</p></div>
  <div class="card glass sm"><h3>Xero access</h3><p>Transiqe asks for the minimum Xero permissions: read contacts and invoices, record payments. It never creates or edits invoices, and you can disconnect it from inside Xero at any time.</p></div>
  <div class="card glass sm"><h3>Customer sign-in</h3><p>Customers sign in with single-use links that expire after seven days. There are no customer passwords to leak. Business logins use hashed passwords and expiring sessions.</p></div>
  <div class="card glass sm"><h3>Tamper-proof amounts</h3><p>The amount charged always comes from the invoice as recorded from Xero, never from a link or a form field, so a modified link cannot underpay an invoice. Returns from the bank's page are signed and checked before anything is recorded.</p></div>
</div></section>
<section><div class="wrap"><div class="glass" style="padding:36px"><h3>Where things run</h3><p style="margin-top:8px;color:var(--ink-2);max-width:70ch">Transiqe runs on Australian cloud infrastructure with encrypted backups. An audit log records every connection change, payment, refund and autopay decision per business, and you can see every email we sent on your behalf in your outbox. Questions about a security review, or a disclosure to make? Write to <a href="mailto:security@transiqe.com">security@transiqe.com</a>.</p></div></div></section>
"""

page('pricing', 'Pricing · Transiqe', 'Flat monthly software pricing. Your card fee stays at the bank rate, settling to your account.', pricing, active='p', extra_css=css)
page('customers', 'For your customers · Transiqe', 'What your customers see: one-tap card payment from the invoice email, a portal, and autopay they control.', customers, active='c', extra_css=css)
page('security', 'Security · Transiqe', 'Card numbers never reach Transiqe. Hosted bank payment page, encrypted credentials, minimal Xero permissions.', security, active='s', extra_css=css)
