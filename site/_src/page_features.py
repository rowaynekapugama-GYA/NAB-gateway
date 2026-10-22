css = """<style>
.pagehead{padding:70px 0 20px}
.pagehead h1{max-width:16ch;font-size:clamp(36px,5vw,60px)}
.feature{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;padding:40px 0}
.feature:nth-child(even) .text{order:2}
.feature .text h2{font-size:clamp(26px,3vw,36px)}
.feature .text p{margin-top:14px;color:var(--ink-2);max-width:50ch;font-size:17px}
.feature ul{margin:18px 0 0;padding:0;list-style:none;display:grid;gap:8px}
.feature li{display:flex;gap:10px;align-items:flex-start;color:var(--ink-2)}
.feature li::before{content:"";width:18px;height:18px;border-radius:50%;flex-shrink:0;margin-top:3px;background:linear-gradient(135deg,var(--cobalt),var(--lagoon));mask:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="black" d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1.6 14.4l-4-4 1.4-1.4 2.6 2.6 5.8-5.8 1.4 1.4-7.2 7.2z"/></svg>') center/contain no-repeat;-webkit-mask:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="black" d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1.6 14.4l-4-4 1.4-1.4 2.6 2.6 5.8-5.8 1.4 1.4-7.2 7.2z"/></svg>') center/contain no-repeat}
.feature .shot{padding:22px}
@media(max-width:900px){.feature{grid-template-columns:1fr}.feature:nth-child(even) .text{order:0}}
.mini{display:grid;gap:10px;padding:22px}
.mini .row{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;background:#fff;border-radius:14px;border:1px solid var(--glass-line);font-size:13.5px}
.mini .row b{font-family:var(--font-display);letter-spacing:-.02em}
.email{padding:22px}
.email .msg{background:#fff;border-radius:16px;border:1px solid var(--glass-line);overflow:hidden;font-size:13px}
.email .msg .hd{padding:12px 16px;background:linear-gradient(135deg,#0F766E,#13A89E);color:#fff;font-weight:700}
.email .msg .bd{padding:16px}
.email .msg .bd .b{display:inline-block;margin-top:10px;padding:9px 14px;border-radius:999px;background:#0F766E;color:#fff;font-weight:700}
</style>"""

body = """
<section class="pagehead"><div class="wrap">
  <h1>Everything between the invoice and the bank, handled.</h1>
  <p class="lede" style="margin-top:18px">Transiqe sits beside Xero and your merchant facility. These are the pieces it takes care of, in the order your customers meet them.</p>
</div></section>

<section style="padding-top:10px"><div class="wrap">

<div class="feature">
  <div class="text"><h2>A pay-by-card link on every invoice</h2><p>The moment an invoice is approved in Xero, Transiqe emails the customer a link that opens a branded pay page showing exactly what's due. Xero's own online invoice gets the same button, so customers who open the Xero email land in the same place.</p>
  <ul><li>Works for invoices you type and invoices Xero generates from repeating templates</li><li>The amount always comes from Xero, never from the link, so it can't be tampered with</li><li>Your logo and colours, your business name on the statement</li></ul></div>
  <div class="shot glass">{pay}</div>
</div>

<div class="feature">
  <div class="text"><h2>Autopay the customer controls</h2><p>Customers tick one box while paying to save their card with the bank. From then on, new invoices are charged automatically, at the timing they choose, with a receipt every time. They can change the timing, swap the card or switch it off from the portal.</p>
  <ul><li>Charge on issue, on the due date, or a set number of days before</li><li>Declines are retried every two days, up to three times, then both of you are told</li><li>Void an invoice in Xero and the scheduled charge is cancelled automatically</li></ul></div>
  <div class="mini glass">
    <div class="row"><span>Automatic payments</span><b style="color:#117A50">On</b></div>
    <div class="row"><span>When to charge</span><b>On the due date</b></div>
    <div class="row"><span>Card</span><b>Visa •••• 1111</b></div>
    <div class="row"><span>Next charge</span><b>INV-0238 · 25 Oct · $121.00</b></div>
    <div class="row"><span>Last receipt</span><b>INV-0226 · emailed</b></div>
  </div>
</div>

<div class="feature">
  <div class="text"><h2>Written back to Xero, reconciled</h2><p>Each successful card payment is recorded against its invoice in Xero within seconds, dated that day, referenced with the bank's transaction ID and posted to the account you choose. Your bank feed then matches one to one.</p>
  <ul><li>Record to your bank account, or to a clearing account if your bank batches settlements</li><li>If Xero is unreachable, the payment is kept and the write-back retried until it lands; you're told if it can't</li><li>Refunds go back to the customer's card from the dashboard</li></ul></div>
  <div class="shot glass">{dashboard}</div>
</div>

<div class="feature">
  <div class="text"><h2>A portal for every customer, automatically</h2><p>Create a contact in Xero and their portal already exists. They sign in with an emailed link, see every open and paid invoice, pay what's due, and manage their saved cards and autopay. No account to set up, no password to reset.</p>
  <ul><li>Branded with your name, logo and colour</li><li>Invite sent automatically when a contact has an email, or on demand from the dashboard</li><li>One person who deals with several businesses on Transiqe gets a portal for each</li></ul></div>
  <div class="shot glass">{portal}</div>
</div>

<div class="feature">
  <div class="text"><h2>The emails, done properly</h2><p>Pay links, portal invites, receipts and declined-payment notices all go out in your name and show in your outbox, so you can see what each customer received and when.</p>
  <ul><li>Plain, short emails in your branding</li><li>Business alerts for anything that needs a human: a write-back that failed, autopay stopped after retries</li><li>Nothing goes out twice, even when Xero redelivers an event</li></ul></div>
  <div class="email glass"><div class="msg"><div class="hd">Northside Physio</div><div class="bd">Hi Priya,<br><br>Invoice <b>INV-0238</b> for <b>$121.00</b> is due on 25 October.<br><span class="b">Pay by card</span><br><br><span class="muted">You can also view all your invoices and set up automatic payments in your customer portal.</span></div></div></div>
</div>

</div></section>

<section><div class="wrap"><div class="cta-block glass" style="padding:48px;text-align:center;display:grid;justify-items:center;gap:16px">
  <h2 style="text-align:center;max-width:20ch">See it running on your own invoices.</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center"><a class="btn primary lg" href="signup.html">Start free</a><a class="btn glassy lg" href="pricing.html">Pricing</a></div>
</div></div></section>
""".replace('{pay}', partial('screen_pay')).replace('{dashboard}', partial('screen_dashboard')).replace('{portal}', partial('screen_portal'))

page('features', 'Features · Transiqe', 'Pay-by-card links, customer-controlled autopay, Xero write-back, customer portals and the emails, all handled.', body, active='f', extra_css=css)
