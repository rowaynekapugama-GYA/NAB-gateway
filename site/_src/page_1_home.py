home_hero = f'''
<div class="hero-grid">
  <div class="copy">
    <span class="tag">For businesses that use Xero and bank with NAB</span>
    <h1>Card payments on your Xero invoices, through your own NAB Gateway.</h1>
    <p class="lede">Transiqe adds a Pay now button to your Xero invoices and connects it to the NAB Gateway account you already have. Your customer pays by card. The money settles to your NAB account at the rate you agreed with NAB, and the invoice is marked paid in Xero.</p>
    <div class="cta"><a class="btn white lg" href="{APP}/signup">Start free <span class="arr">&rarr;</span></a><a class="btn ghost lg" href="how-it-works.html">See how it works</a></div>
    <div class="hero-note"><span><i></i>No third-party payment processor in between</span><span><i></i>Transiqe never holds your money</span></div>
  </div>
  <div class="glass paycard" aria-label="Example of an invoice being paid">
    <div class="row"><div><div class="who">Northside Physio</div><div class="tiny muted">Invoice INV-0238 to Priya Sharma</div></div><span class="pill blue">Due 25 Oct</span></div>
    <div class="amt num">$121.00</div>
    <div class="tiny muted">Sent from Xero</div>
    <div class="btn cobalt block paybtn">Pay now</div>
    <ul>
      <li>Paid by card through your NAB Gateway</li>
      <li>Settles to your NAB account</li>
      <li>Marked paid in Xero, receipt sent</li>
    </ul>
  </div>
</div>'''

home = hero('on-image', '', home_hero, img='owner-tablet', cls='cool', pos='40% 30%', flip=True) + f'''

<section class="band"><div class="wrap">
  <div class="head">
    <div><span class="label">Why Transiqe</span>
      <h2>You send the invoice from Xero. <span class="soft">The payment shouldn't need a middleman.</span></h2></div>
    <p class="lede">To take a card payment on a Xero invoice, most businesses plug in a separate payment processor. It charges its own fee on every payment, holds the money, and pays you out later. If you bank with NAB, you can use your own NAB Gateway instead. Transiqe is the software that connects it to Xero.</p>
  </div>
  <div class="routes">
    <div class="route usual">
      <div class="name">The usual way<small>A separate processor sits between your customer and your bank.</small></div>
      <div class="track"><i class="rail"></i><i class="coin"></i>
        <div class="stop">Xero invoice</div><span class="sep">&rarr;</span>
        <div class="stop mid">Third-party payment processor<small>Its own fee on every payment. Holds the money, pays out later.</small></div><span class="sep">&rarr;</span>
        <div class="stop">Your bank account</div>
      </div>
    </div>
    <div class="route ours">
      <div class="name">With Transiqe<small>Your invoice connects straight to your own NAB Gateway.</small></div>
      <div class="track"><i class="rail"></i><i class="coin"></i>
        <div class="stop">Xero invoice<small>With a Pay now button</small></div><span class="sep">&rarr;</span>
        <div class="stop key">Your NAB Gateway<small>The card fees you agreed with NAB</small></div><span class="sep">&rarr;</span>
        <div class="stop">Your NAB account<small>Paid to you directly</small></div><span class="sep">&rarr;</span>
        <div class="stop">Back in Xero<small>Invoice marked paid</small></div>
      </div>
    </div>
  </div>
</div></section>

<section class="band tight"><div class="wrap">
  <div class="bento">
    <div class="tile photo a">
      <picture><source type="image/webp" srcset="assets/img/owner-laptop-900.webp"><img src="assets/img/owner-laptop.jpg" alt="A business owner at home, working on a laptop" loading="lazy" style="object-position:66% 22%"></picture>
      <div class="over"><div class="glass chipcard"><div><b>Olive &amp; Co Pty Ltd paid $1,320.00</b><span class="s">INV-0229, paid by card, 8:40 am</span></div><span class="pill green">Marked paid in Xero</span></div></div>
    </div>
    <div class="tile ember b"><div class="big num">2</div><h4 style="margin-top:18px">connections to set up</h4><p>Xero and your NAB Gateway. That is the whole setup.</p></div>
    <div class="tile oat c"><div class="big num">0</div><h4 style="margin-top:18px">third parties in the middle</h4><p>Nothing sits between your customer's card and your NAB account.</p></div>
    <div class="tile ink d"><h3>You pay the rate you agreed with NAB.</h3><p style="max-width:60ch">Card payments run on your own NAB merchant facility, at the fees you agreed with NAB as a NAB customer. Transiqe adds no percentage and no per-payment fee on top. We charge a flat monthly subscription for the software.</p></div>
  </div>
</div></section>

<section class="band" id="how"><div class="wrap">
  <div class="head">
    <div><span class="label">How it works</span>
      <h2>Set up once. <span class="soft">Then every invoice can be paid by card.</span></h2></div>
    <p class="lede">Setup is three steps and most of it is signing in and approving. After that you keep working in Xero and Transiqe does the rest.</p>
  </div>
  <div class="ruler" aria-hidden="true"><span>Step 1</span><span>Step 2</span><span>Step 3</span><span>Ready</span></div>
  <div class="grid g3">
    <div class="tile oat step"><span class="n">1</span><h3>Connect Xero</h3><p>Sign in to Xero and approve the connection. Nothing changes in how you use Xero.</p>
      <ul class="checks"><li>Your customers are imported automatically</li><li>Your open invoices come across with them</li></ul></div>
    <div class="tile ink step dark"><span class="n">2</span><h3>Connect your NAB Gateway</h3><p>Link the NAB Gateway account you hold as a NAB customer. Card payments run on your facility.</p>
      <ul class="checks"><li>Settles to your NAB account</li><li>Your NAB rate, nothing added</li></ul></div>
    <div class="tile oat step"><span class="n">3</span><h3>Switch on Pay now</h3><p>Add Transiqe as the payment option on your Xero invoices. Every invoice now carries a Pay now button.</p>
      <ul class="checks"><li>Works for one-off invoices</li><li>Works for repeating invoices</li></ul></div>
  </div>
  <h3 style="margin:clamp(36px,5vw,56px) 0 0">What happens on every invoice after that</h3>
  <div class="journey">
    <div><span class="k">You</span><b>Send the invoice from Xero</b><p>Or let a repeating invoice go out on its own. Nothing new to learn.</p></div>
    <div><span class="k">Your customer</span><b>Clicks Pay now</b><p>The button is on the invoice they receive. No account needed.</p></div>
    <div><span class="k">Your customer</span><b>Pays by card</b><p>The card fields are provided by NAB Gateway, connected to your account.</p></div>
    <div><span class="k">NAB</span><b>Settles to your NAB account</b><p>Under your own merchant agreement, at your agreed rate.</p></div>
    <div><span class="k">Transiqe</span><b>Marks it paid in Xero</b><p>The payment is recorded against the invoice and a receipt is sent.</p></div>
  </div>
  <p style="margin-top:26px"><a class="textlink" href="how-it-works.html">See every step, start to finish</a></p>
</div></section>

<section class="band tight"><div class="wrap">
  <div class="head">
    <div><span class="label">What you get</span>
      <h2>Everything between the invoice and your bank. <span class="soft">Handled for you.</span></h2></div>
    <p class="lede">You keep invoicing from Xero. Transiqe looks after the payment, the reminders and the bookkeeping that follows.</p>
  </div>
  <div class="feats">
    <div class="feat"><div class="ic">{ICON['card']}</div><h4>Pay now on your Xero invoices</h4><p>The button is attached to the invoice you already send. Customers pay by card in under a minute.</p></div>
    <div class="feat"><div class="ic">{ICON['clock']}</div><h4>Autopay your customers control</h4><p>Customers can save a card and opt in to automatic payments, and opt out again whenever they like.</p></div>
    <div class="feat"><div class="ic">{ICON['repeat']}</div><h4>Repeating invoices, synced</h4><p>Set up a repeating invoice in Xero and it flows through. Customers on autopay are charged automatically.</p></div>
    <div class="feat"><div class="ic">{ICON['user']}</div><h4>A portal for every customer</h4><p>Customers sign in to see their invoices, pay what is due and manage their saved card.</p></div>
    <div class="feat"><div class="ic">{ICON['bell']}</div><h4>Reminders and receipts</h4><p>Payment reminders, receipts and declined-card notices go out for you, in your name.</p></div>
    <div class="feat"><div class="ic">{ICON['check']}</div><h4>Reconciled in Xero</h4><p>Every payment is recorded against its invoice in Xero, so your books match your bank.</p></div>
    <div class="feat"><div class="ic">{ICON['users']}</div><h4>Customers imported for you</h4><p>Connect Xero once and your customers appear in Transiqe automatically, and stay in sync.</p></div>
    <div class="feat"><div class="ic">{ICON['doc']}</div><h4>No Xero? Invoice from Transiqe</h4><p>If you don't use Xero, you can create and send invoices straight from Transiqe.</p></div>
  </div>
</div></section>

<section class="band tight"><div class="wrap">
  <div class="stage">{SCREEN_DASH}</div>
  {SAMPLE_NOTE}
</div></section>

<section class="band"><div class="wrap split">
  <div>
    <span class="label">For your customers</span>
    <h2 style="margin-top:16px">Your customers get the easy version.</h2>
    <p class="lede" style="margin-top:18px">They open your invoice, click Pay now and enter their card. If they would rather not think about it again, they can save the card and let future invoices pay themselves.</p>
    <ul class="checks" style="max-width:460px">
      <li style="background:var(--oat)">No account or password needed to pay</li>
      <li style="background:var(--oat)">A portal to see every invoice and receipt</li>
      <li style="background:var(--oat)">Autopay they can switch on or off at any time</li>
    </ul>
    <p style="margin-top:24px"><a class="textlink" href="customers.html">See what your customers see</a></p>
  </div>
  <div class="stage ember">{SCREEN_PAY}</div>
</div></section>

<section class="band tight"><div class="wrap">
  <div class="shell" style="padding:0"><div class="panel cool inview">
    <img class="bg" src="assets/img/card-circuit.jpg" alt="" loading="lazy" style="object-position:70% 50%">
    <div class="inner" style="padding:clamp(28px,5vw,72px)">
      <span class="tag">Fees</span>
      <h2 style="max-width:16ch">One bank, one rate. <span style="color:rgba(255,255,255,.6)">No one in the middle.</span></h2>
      <div class="grid g3" style="margin-top:clamp(24px,4vw,44px);max-width:980px">
        <div><h4 style="color:#fff">The rate stays with NAB</h4><p style="color:rgba(255,255,255,.75);margin-top:8px;font-size:15px">You pay the card fees you agreed with NAB. Transiqe adds nothing to them.</p></div>
        <div><h4 style="color:#fff">The money stays yours</h4><p style="color:rgba(255,255,255,.75);margin-top:8px;font-size:15px">Payments settle from your customer's card to your NAB account. We never hold funds.</p></div>
        <div><h4 style="color:#fff">We charge for software</h4><p style="color:rgba(255,255,255,.75);margin-top:8px;font-size:15px">A flat monthly subscription, based on how many invoices you send. No percentage of your takings.</p></div>
      </div>
    </div>
  </div></div>
</div></section>

<section class="band"><div class="wrap">
  <div class="head">
    <div><span class="label">Pricing</span><h2>Simple monthly pricing. <span class="soft">No percentage of your invoices.</span></h2></div>
    <p class="lede">Pick the plan that matches how many invoices you send. Card fees are separate and stay between you and NAB.</p>
  </div>
  {PLANS}
</div></section>

<section class="band tight"><div class="wrap faqwrap">
  <div>
    <span class="label">Questions</span>
    <h2 style="margin-top:16px">Questions, <span class="soft">answered.</span></h2>
    <div class="tile ember ask"><h4>Not sure it fits your setup?</h4><p style="margin:8px 0 16px">Tell us how you invoice today and we will tell you plainly whether Transiqe suits.</p><a class="btn white sm" href="mailto:hello@transiqe.com">hello@transiqe.com</a></div>
  </div>
  <div class="faq">
    <details open><summary>What do I need to use Transiqe?</summary><p>A NAB Gateway account, which NAB provides to its business customers for taking card payments online, and ideally a Xero subscription. If you don't use Xero, you can send invoices from Transiqe itself.</p></details>
    <details><summary>How is this different from the payment option I use now?</summary><p>Most payment add-ons are separate processors. They take the payment, charge their own fee and pay you out later. Transiqe is software only. The payment runs through your own NAB Gateway and settles to your NAB account, at the fees you agreed with NAB.</p></details>
    <details><summary>Does Transiqe hold my money?</summary><p>No. Card payments go from your customer to your NAB merchant facility and settle to your account. Transiqe moves the information: the invoice to your customer and the payment record back to Xero.</p></details>
    <details><summary>What happens with repeating invoices?</summary><p>Set them up in Xero as you do now. Each invoice Xero creates flows into Transiqe. Customers who have opted in to autopay are charged automatically, and everyone else gets the invoice with a Pay now button.</p></details>
    <details><summary>Can my customers opt out of automatic payments?</summary><p>Yes, at any time, from their portal or by asking you. Autopay is always the customer's choice and they see the terms before they opt in.</p></details>
    <details><summary>What changes in Xero?</summary><p>Very little. Your invoices gain a Pay now button, and payments appear against invoices as they are made. Your bookkeeper will see them recorded with the payment reference.</p></details>
  </div>
</div></section>

{CLOSER}
'''

page('index', 'Transiqe: card payments on your Xero invoices, through your own NAB Gateway',
     'Transiqe adds a Pay now button to your Xero invoices and connects it to your own NAB Gateway. Customers pay by card, the money settles to your NAB account at your agreed NAB rate, and the invoice is marked paid in Xero.',
     home)
