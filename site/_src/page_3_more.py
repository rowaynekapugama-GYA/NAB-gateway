# ------------------------------------------------------------------ features
def frow(title, text, visual, checks=()):
    cl = ''.join(f'<li>{c}</li>' for c in checks)
    cl = f'<ul class="checks">{cl}</ul>' if cl else ''
    return f'<div class="rowx"><div class="txt"><h3>{title}</h3><p>{text}</p>{cl}</div><div class="vis">{visual}</div></div>'

feat_hero = '''<div class="hero-grid with-art"><div class="copy">
  <span class="tag">Features</span>
  <h1>Take card payments on your invoices without a third-party processor.</h1>
  <p class="lede">If you use Xero and bank with NAB, you already have everything you need. Transiqe connects the two and looks after the payment, the reminders and the bookkeeping that follows.</p>
</div>'''+ ART_FEATURES + '''</div>'''

features = hero('on-image', 'features', feat_hero, img='light-warm', cls='subhero') + f'''

<section class="band"><div class="wrap"><div class="rows">
  {frow('Pay by card, straight from your Xero invoice',
        'A Pay now button is attached to the invoices you send from Xero. Your customer clicks it, sees exactly what is due and pays by card. The payment runs through your own NAB Gateway.',
        f'<div class="stage">{SCREEN_INVOICE}</div>',
        ['Works on the invoices you already send', 'The amount always comes from the invoice', 'Card fields provided by NAB Gateway'])}
  {frow('Your NAB account, your NAB rate',
        'You no longer need a separate payment processor to take a card payment. You transact directly through your NAB Gateway account and pay the fees you agreed with NAB as a NAB customer. Transiqe adds nothing to them.',
        '<div class="tile ink" style="padding:clamp(24px,4vw,44px)"><h3>What stays with NAB</h3><ul class="checks"><li>The card fees, as agreed in your merchant agreement</li><li>The money, which settles to your NAB account</li><li>The relationship, including your statements and support</li></ul><p style="margin-top:18px;font-size:14.5px">Transiqe is software. It is never in possession of your funds.</p></div>')}
  {frow('Autopay your customers control',
        'Customers can save a card and opt in to automatic payments, and opt out again whenever they like. They choose when their card is charged and get a receipt every time.',
        f'<div class="stage ember">{SCREEN_AUTOPAY}</div>',
        ['Opt in while paying, or from the portal', 'Opt out at any time', 'Clear terms shown before they agree'])}
  {frow('Repeating invoices, synced automatically',
        'Set up a repeating invoice in Xero and every invoice it creates flows into Transiqe. Customers on autopay are charged automatically. Everyone else receives the invoice with a Pay now button.',
        '<div class="tile oat" style="padding:clamp(24px,4vw,44px)"><div class="label">Monthly retainer, Olive &amp; Co Pty Ltd</div><div style="display:grid;gap:8px;margin-top:16px"><div class="field"><span>1 September</span><b>Paid automatically</b></div><div class="field"><span>1 October</span><b>Paid automatically</b></div><div class="field"><span>1 November</span><b>Paid automatically</b></div><div class="field"><span>1 December</span><b style="color:var(--amber-ink)">Scheduled</b></div></div></div>')}
  {frow('A portal for every customer',
        'Each of your customers gets a portal where they can see their invoices, pay what is due, download receipts and manage their saved card. It carries your business name, not ours.',
        f'<div class="stage">{SCREEN_PORTAL}</div>',
        ['No password to remember', 'Every open and paid invoice in one place'])}
  {frow('Reminders, receipts and well-designed emails',
        'Invoice emails, payment reminders, receipts and declined-card notices go out for you, in your name. You can see every email that has been sent to each customer.',
        f'<div class="stage ember">{SCREEN_EMAIL}</div>',
        ['Payment reminders with a Pay now button', 'A receipt after every payment', 'A full record of what was sent and when'])}
  {frow('Reconciled in Xero',
        'Every card payment is recorded against its invoice in Xero as it happens, with the payment reference. Your invoices show as paid and your books match what lands in your NAB account.',
        f'<div class="stage">{SCREEN_DASH}</div>',
        ['Invoices marked paid automatically', 'One dashboard for paid, due and on autopay'])}
</div>{SAMPLE_NOTE}</div></section>

<section class="band tight"><div class="wrap">
  <div class="grid g2">
    <div class="tile oat"><div class="feat" style="border:0;padding:0"><div class="ic" style="background:#fff">{ICON['users']}</div><h3>Your customers come with you</h3><p style="font-size:16px">Once you connect Xero, all your customers are brought into Transiqe automatically, along with their open invoices. There is nothing to re-enter, and new customers you add in Xero appear on their own.</p></div></div>
    <div class="tile oat"><div class="feat" style="border:0;padding:0"><div class="ic" style="background:#fff">{ICON['doc']}</div><h3>No Xero? Invoice from Transiqe</h3><p style="font-size:16px">If you don't use Xero, you can create and send invoices straight from Transiqe. Your customers get the same Pay now button, portal and autopay, connected to your NAB Gateway.</p></div></div>
  </div>
</div></section>

{CLOSER}
'''
page('features', 'Features · Transiqe',
     'Pay now on your Xero invoices, autopay your customers control, repeating invoices, a customer portal, reminders and receipts, and payments recorded in Xero. All through your own NAB Gateway.',
     features)

# ------------------------------------------------------------------ customers
cust_hero = '''<div class="hero-grid with-art"><div class="copy">
  <span class="tag">For your customers</span>
  <h1>Paying you should be the easy part.</h1>
  <p class="lede">Your customers see your business name, your invoice and one clear button. They pay by card in under a minute, and they stay in control of anything automatic.</p>
</div>'''+ ART_CUSTOMERS + '''</div>'''

customers = hero('on-image', 'customers', cust_hero, img='owner-laptop', cls='subhero', pos='62% 26%') + f'''

<section class="band"><div class="wrap">
  <div class="head"><div><span class="label">What your customer sees</span><h2>Three screens. <span class="soft">That is all it takes.</span></h2></div>
  <p class="lede">No app to download and no account to create. The invoice arrives, they click Pay now, they enter a card.</p></div>
  <div class="grid g3 trio">
    <div><div class="stage">{SCREEN_EMAIL}</div><h4 style="margin-top:18px">1. Your invoice arrives</h4><p class="muted" style="margin-top:6px">In their inbox, from your business, with a Pay now button.</p></div>
    <div><div class="stage ember">{SCREEN_PAY}</div><h4 style="margin-top:18px">2. They pay by card</h4><p class="muted" style="margin-top:6px">The card fields are provided by NAB Gateway. The amount comes from the invoice.</p></div>
    <div><div class="stage">{SCREEN_AUTOPAY}</div><h4 style="margin-top:18px">3. They can choose autopay</h4><p class="muted" style="margin-top:6px">Optional. They decide, and they can turn it off at any time.</p></div>
  </div>
  {SAMPLE_NOTE}
</div></section>

<section class="band tight"><div class="wrap split">
  <div>
    <span class="label">The customer portal</span>
    <h2 style="margin-top:16px">Everything they owe and everything they have paid, <span class="soft">in one place.</span></h2>
    <p class="lede" style="margin-top:18px">Every customer gets a portal under your business name. They sign in with a secure link sent to their email, so there is no password to set up or forget.</p>
    <ul class="checks" style="max-width:480px">
      <li style="background:var(--oat)">See open invoices and pay them</li>
      <li style="background:var(--oat)">See past payments and receipts</li>
      <li style="background:var(--oat)">Add, change or remove a saved card</li>
      <li style="background:var(--oat)">Switch autopay on or off</li>
    </ul>
    <p style="margin-top:24px"><a class="btn line" href="{APP}/portal">Open the customer portal</a></p>
  </div>
  <div class="stage">{SCREEN_PORTAL}</div>
</div></section>

<section class="band"><div class="wrap">
  <div class="head single"><div><span class="label">Fair to your customers</span><h2>Automatic payments, <span class="soft">on their terms.</span></h2></div></div>
  <ul class="plainlist">
    <li><h4>Autopay is always opt-in</h4><p>A customer is only ever charged automatically if they have chosen it. They see plain-language terms first, including what will be charged and when. Read the <a href="autopay-terms.html">autopay terms</a>.</p></li>
    <li><h4>They can opt out at any time</h4><p>From their portal, in a couple of clicks, or by asking you. Opting out stops future automatic payments straight away.</p></li>
    <li><h4>They are told about every payment</h4><p>Customers receive every invoice and a receipt after each payment, so they always know what was charged and why.</p></li>
    <li><h4>Their card details are handled by NAB</h4><p>Card details are entered into fields provided by NAB Gateway. Transiqe does not store full card numbers or security codes. See <a href="security.html">security</a>.</p></li>
  </ul>
</div></section>

{CLOSER}
'''
page('customers', 'For your customers · Transiqe',
     'What your customers see: your invoice with a Pay now button, a simple card payment, a portal for their invoices and receipts, and autopay they can opt in and out of.',
     customers)

# ------------------------------------------------------------------ pricing
price_hero = '''<div class="hero-grid with-art"><div class="copy">
  <span class="tag">Pricing</span>
  <h1>A flat monthly price. No percentage of your invoices.</h1>
  <p class="lede">You pay Transiqe for the software. You pay NAB the card fees you agreed with NAB. Nobody takes a cut in between.</p>
</div>'''+ ART_PRICING + '''</div>'''

pricing = hero('on-image', 'pricing', price_hero, img='light-ink', cls='cool subhero') + f'''

<section class="band"><div class="wrap">
  {PLANS}
</div></section>

<section class="band tight"><div class="wrap">
  <div class="head"><div><span class="label">Every plan includes</span><h2>The whole product, <span class="soft">on every plan.</span></h2></div>
  <p class="lede">Plans differ only by how many invoices you send each month. You never pay more to unlock a feature.</p></div>
  <div class="feats">
    <div class="feat"><div class="ic">{ICON['card']}</div><h4>Pay now on Xero invoices</h4><p>Connected to your own NAB Gateway.</p></div>
    <div class="feat"><div class="ic">{ICON['clock']}</div><h4>Autopay</h4><p>Opt-in automatic payments your customers control.</p></div>
    <div class="feat"><div class="ic">{ICON['repeat']}</div><h4>Repeating invoices</h4><p>Synced from Xero automatically.</p></div>
    <div class="feat"><div class="ic">{ICON['user']}</div><h4>Customer portal</h4><p>For every one of your customers.</p></div>
    <div class="feat"><div class="ic">{ICON['bell']}</div><h4>Reminders and receipts</h4><p>Sent for you, in your name.</p></div>
    <div class="feat"><div class="ic">{ICON['check']}</div><h4>Xero reconciliation</h4><p>Payments recorded against invoices.</p></div>
    <div class="feat"><div class="ic">{ICON['users']}</div><h4>Customer import</h4><p>Your Xero customers, brought in automatically.</p></div>
    <div class="feat"><div class="ic">{ICON['doc']}</div><h4>Invoicing without Xero</h4><p>Send invoices from Transiqe itself.</p></div>
  </div>
</div></section>

<section class="band tight"><div class="wrap split">
  <div class="tile ink" style="padding:clamp(26px,4vw,48px)">
    <h3>What you pay NAB</h3>
    <p style="margin-top:10px">Card payments are processed on your own NAB merchant facility. The fees are the ones in your agreement with NAB, and NAB charges them to you directly. They are not part of your Transiqe subscription, and Transiqe adds nothing to them.</p>
  </div>
  <div class="tile ember" style="padding:clamp(26px,4vw,48px)">
    <h3>What you pay Transiqe</h3>
    <p style="margin-top:10px">One flat monthly subscription for the software, based on how many invoices you send. No setup fee, no per-payment fee and no percentage of your takings.</p>
  </div>
</div></section>

<section class="band tight"><div class="wrap faqwrap">
  <div><span class="label">Pricing questions</span><h2 style="margin-top:16px">The short answers.</h2></div>
  <div class="faq">
    <details open><summary>Are card fees included in the plan price?</summary><p>No. Card fees are charged by NAB under your own merchant agreement, at the rate you agreed with NAB. Your Transiqe plan covers the software only.</p></details>
    <details><summary>Does Transiqe take a percentage of each payment?</summary><p>No. There is no percentage and no per-payment fee from Transiqe. You pay the flat monthly price for your plan.</p></details>
    <details><summary>Do I need to apply or wait for approval?</summary><p>Not from Transiqe. Sign up, choose your plan and connect Xero and your NAB Gateway. If you do not have a NAB Gateway account yet, that is arranged with NAB.</p></details>
    <details><summary>What if I send more than 1,000 invoices a month?</summary><p>Talk to us at hello@transiqe.com and we will price a plan around your volume.</p></details>
  </div>
</div></section>

{CLOSER}
'''
page('pricing', 'Pricing · Transiqe',
     'Starter $49.95 a month for up to 100 invoices. Growth $99 a month for up to 1,000 invoices. A flat price for the software, with card fees staying between you and NAB.',
     pricing)
