def row(n, title, text, visual, checks=()):
    cl = ''.join(f'<li>{c}</li>' for c in checks)
    cl = f'<ul class="checks">{cl}</ul>' if cl else ''
    return f'<div class="rowx"><div class="txt"><span class="n">{n}</span><h3>{title}</h3><p>{text}</p>{cl}</div><div class="vis">{visual}</div></div>'

how_hero = f'''<div class="hero-grid"><div class="copy">
  <span class="tag">How it works</span>
  <h1>From Xero invoice to money in your NAB account, step by step.</h1>
  <p class="lede">You set Transiqe up once. After that, every invoice you send from Xero can be paid by card through your own NAB Gateway, and the payment is recorded back in Xero for you.</p>
</div></div>'''

how = hero('on-image', 'how', how_hero, img='owner-tablet', cls='cool subhero', pos='70% 30%') + f'''

<section class="band"><div class="wrap">
  <div class="part"><span class="k">Part one</span><h2>Set up, once.</h2></div>
  <div class="rows">
    {row(1, 'Create your Transiqe account', 'Enter your business name and email and you are in. It is free while you set up, so you can connect everything and send a test invoice before you pay anything.',
         f'<div class="stage">{SCREEN_CONNECT}</div>')}
    {row(2, 'Connect Xero', 'Click Connect Xero, sign in to Xero and approve. Transiqe reads your customers and invoices and records payments against them. It does not change how you invoice.',
         f'<div class="stage ember"><div class="screen phone"><div class="inv"><h5 style="margin-bottom:14px">Imported from Xero</h5><div style="display:grid;gap:8px"><div class="field"><span>Marcus Bell</span><b class="num">2 open invoices</b></div><div class="field"><span>Olive &amp; Co Pty Ltd</span><b class="num">1 open invoice</b></div><div class="field"><span>Priya Sharma</span><b class="num">1 open invoice</b></div><div class="field"><span>Dan Harker</span><b class="num">1 open invoice</b></div><div class="field"><span>47 more customers</span><b class="num">4 open invoices</b></div></div><p class="tiny muted" style="margin-top:12px">New customers and invoices you add in Xero appear here automatically.</p></div></div></div>',
         ['All your Xero customers are imported automatically', 'Open invoices come across with them', 'New customers and invoices stay in sync'])}
    {row(3, 'Connect your NAB Gateway', 'Link the NAB Gateway account NAB has set up for your business. From then on, card payments on your invoices run through your own merchant facility and settle to your NAB account.',
         '<div class="tile ink" style="padding:clamp(24px,4vw,44px)"><h3>What is NAB Gateway?</h3><p style="margin-top:10px">It is the online card payment facility NAB provides to its business customers. If you bank with NAB and do not have it yet, your NAB business banker can set it up.</p><ul class="checks"><li>Your merchant agreement with NAB</li><li>The card fees you agreed with NAB</li><li>Settlement to your NAB account</li></ul></div>')}
    {row(4, 'Switch on Pay now', 'Add Transiqe as the payment option on your Xero invoices. We give you the link and show you exactly where it goes. Every invoice you send from then on carries a Pay now button.',
         f'<div class="stage">{SCREEN_INVOICE}</div>',
         ['One-off invoices', 'Repeating invoices', 'Send yourself a test invoice to see it working'])}
  </div>
</div></section>

<section class="band" style="background:var(--oat)"><div class="wrap">
  <div class="part"><span class="k">Part two</span><h2>Then, on every invoice.</h2></div>
  <div class="rows">
    {row(1, 'You send the invoice from Xero', 'Exactly as you do today. Your customer receives the invoice with a Pay now button on it. If you do not use Xero, you can create and send the invoice from Transiqe instead.',
         f'<div class="stage" style="background:#fff">{SCREEN_EMAIL}</div>')}
    {row(2, 'Your customer clicks Pay now and pays by card', 'They see the invoice and the amount due and enter their card. The card fields are provided by NAB Gateway and connected to your account, so the payment goes straight to your merchant facility.',
         f'<div class="stage ember">{SCREEN_PAY}</div>',
         ['No account or password needed', 'The amount always comes from the invoice', 'They can save the card for next time'])}
    {row(3, 'The money settles to your NAB account', 'NAB processes the payment under your own merchant agreement and pays it into your NAB account. Transiqe is never in possession of the money, and there is no payout to wait for from us.',
         '<div class="tile ink" style="padding:clamp(24px,4vw,44px)"><div class="label" style="color:rgba(255,255,255,.6)">Where the money goes</div><div style="display:grid;gap:10px;margin-top:18px"><div class="stop" style="background:rgba(255,255,255,.08);color:#fff;flex:none">Your customer&#39;s card</div><div class="stop" style="background:linear-gradient(135deg,var(--apricot),var(--ember));color:#2a1206;flex:none">Your NAB Gateway<small style="color:rgba(42,18,6,.72)">The card fees you agreed with NAB</small></div><div class="stop" style="background:rgba(255,255,255,.08);color:#fff;flex:none">Your NAB account</div></div></div>')}
    {row(4, 'Transiqe marks the invoice paid in Xero', 'The payment is recorded against the invoice in Xero with its reference, and your customer gets a receipt. Your dashboard shows what has been paid, what is due and what is on autopay.',
         f'<div class="stage" style="background:#fff">{SCREEN_DASH}</div>')}
  </div>
  {SAMPLE_NOTE}
</div></section>

<section class="band"><div class="wrap">
  <div class="part"><span class="k">Part three</span><h2>Repeating invoices and autopay.</h2></div>
  <div class="rows">
    {row(1, 'Set up the repeating invoice in Xero', 'Use repeating invoices in Xero as you normally would for retainers, memberships or regular services. Each invoice Xero creates flows into Transiqe automatically.',
         '<div class="tile oat" style="padding:clamp(24px,4vw,44px)"><div class="label">Monthly retainer, Olive &amp; Co Pty Ltd</div><div style="display:grid;gap:8px;margin-top:16px"><div class="field"><span>1 September</span><b>Paid automatically</b></div><div class="field"><span>1 October</span><b>Paid automatically</b></div><div class="field"><span>1 November</span><b>Paid automatically</b></div><div class="field"><span>1 December</span><b style="color:var(--amber-ink)">Scheduled</b></div></div></div>')}
    {row(2, 'Your customer opts in to autopay', 'When they pay an invoice, or from their portal, your customer can choose to save their card and have future invoices paid automatically. It is their choice, they see the terms first, and they can opt out at any time.',
         f'<div class="stage ember">{SCREEN_AUTOPAY}</div>',
         ['Customers opt in and out themselves', 'A receipt is sent after every payment', 'Customers not on autopay simply get Pay now'])}
  </div>
</div></section>

<section class="band tight"><div class="wrap">
  <div class="head single"><div><span class="label">The less usual days</span><h2>When something doesn't go to plan.</h2></div></div>
  <ul class="plainlist">
    <li><h4>A card is declined</h4><p>Your customer is told straight away and can pay with another card. For autopay, Transiqe lets them know, tries again, and tells you both if it still cannot collect. The invoice stays open in Xero the whole time.</p></li>
    <li><h4>An invoice is overdue</h4><p>Transiqe sends payment reminders for you, each with the Pay now button, so chasing does not depend on you remembering.</p></li>
    <li><h4>You need to refund a payment</h4><p>Refund it from your Transiqe dashboard and the money goes back to your customer's card through your NAB Gateway.</p></li>
    <li><h4>You void or change an invoice in Xero</h4><p>Transiqe follows Xero. If an invoice is voided or already paid another way, any scheduled autopay for it is cancelled.</p></li>
  </ul>
</div></section>

{CLOSER}
'''

page('how-it-works', 'How Transiqe works, step by step',
     'Connect Xero, connect your NAB Gateway and switch on Pay now. Then every Xero invoice can be paid by card, settle to your NAB account and be marked paid in Xero.',
     how)
