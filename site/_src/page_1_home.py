home_hero = f'''
<div class="hero-grid">
  <div class="copy">
    <span class="tag">For businesses that use Xero and bank with NAB</span>
    <h1>Card payments on your Xero invoices, through your own NAB Gateway.</h1>
    <p class="lede">Transiqe adds a Pay now button to your Xero invoices and connects it to the NAB Gateway account you already have. Your customer pays by card. The money settles to your NAB account at the rate you agreed with NAB, and the invoice is marked paid in Xero.</p>
    <div class="cta"><a class="btn white lg" href="{APP}/signup">Sign up <span class="arr">&rarr;</span></a><a class="btn ghost lg" href="how-it-works.html">See how it works</a></div>
    <div class="hero-note"><span><i></i>Set up in under five minutes</span><span><i></i>No third-party payment processor in between</span><span><i></i>Transiqe never holds your money</span></div>
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
<div class="wrap"><div class="connect">
  <span class="lbl">Connects your</span>
  <span class="lg"><img class="x" src="assets/logos/xero.png" alt="Xero" width="54" height="54"><span class="amp">+</span><img class="n" src="assets/logos/nab.png" alt="NAB" width="102" height="40"></span>
  <span class="div" aria-hidden="true"></span>
  <span class="facts"><span>Built for Australian businesses</span><span>No approval wait</span><span>Live in under five minutes</span></span>
</div></div>

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

<section class="band" id="setup"><div class="wrap split">
  <div class="archwrap">
    <div class="arch"><img src="assets/img/owner-laptop.jpg" alt="A business owner setting up Transiqe on her laptop" loading="lazy">
      <p class="quote">Connect Xero. Connect NAB. Send your next invoice.</p></div>
    <div class="logoband" aria-hidden="true"><span class="bub"><img src="assets/logos/xero.png" alt=""></span><span class="plus">+</span><span class="bub nab"><img src="assets/logos/nab-star.png" alt=""></span><span class="plus">=</span><span class="bub tq"><img src="assets/mark.svg" alt=""></span></div>
  </div>
  <div>
    <span class="label">Get set up</span>
    <h2 style="margin-top:16px">Up and running in under five minutes.</h2>
    <p class="lede" style="margin-top:16px">There is no application to Transiqe and no approval to wait for. If you already have a NAB Gateway account, connect it and Xero and you are ready to take card payments.</p>
    <ol class="stepsx">
      <li><div><span class="tm">1 min</span><b>Sign up</b><p>Your name, your business and your email. Choose your plan.</p></div></li>
      <li><div><span class="tm">1 min</span><b>Connect Xero</b><p>Sign in to Xero and approve. Your customers and open invoices come across automatically.</p></div></li>
      <li><div><span class="tm">2 min</span><b>Connect your NAB Gateway</b><p>Add the details from your NAB Gateway account. Card payments run on your own facility.</p></div></li>
      <li><div><span class="tm">1 min</span><b>Switch on Pay now, and you are off</b><p>Add Transiqe as the payment option on your Xero invoices. Your next invoice can be paid by card.</p></div></li>
    </ol>
    <p class="fineprint">You need an active NAB Gateway account. If you do not have one yet, your NAB business banker can set it up for you.</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px"><a class="btn ink lg" href="{APP}/signup">Sign up <span class="arr">&rarr;</span></a><a class="btn line lg" href="help.html#getting-started">Read the setup guide</a></div>
  </div>
</div></section>

<section class="band tight"><div class="wrap">
  <div class="head">
    <div><span class="label">After that</span>
      <h2>What happens on every invoice. <span class="soft">Nothing new to learn.</span></h2></div>
    <p class="lede">You keep working in Xero. Your customer pays by card, NAB settles it to your account, and Transiqe records it back in Xero.</p>
  </div>
  <div class="journey">
    <div><span class="k">You</span><b>Send the invoice from Xero</b><p>Or let a repeating invoice go out on its own.</p></div>
    <div><span class="k">Your customer</span><b>Clicks Pay now</b><p>The button is on the invoice they receive. No account needed.</p></div>
    <div><span class="k">Your customer</span><b>Pays by card</b><p>The card fields are provided by NAB Gateway, connected to your account.</p></div>
    <div><span class="k">NAB</span><b>Settles to your NAB account</b><p>Under your own merchant agreement, at your agreed rate.</p></div>
    <div><span class="k">Transiqe</span><b>Marks it paid in Xero</b><p>The payment is recorded against the invoice and a receipt is sent.</p></div>
  </div>
  <p style="margin-top:26px"><a class="textlink" href="how-it-works.html">See every step, start to finish</a></p>
</div></section>

<section class="band" id="built-for"><div class="wrap">
  <div class="head">
    <div><span class="label">Who it is for</span>
      <h2>Built for businesses of every size. <span class="soft">If you invoice, it fits.</span></h2></div>
    <p class="lede">From a sole trader sending a handful of invoices a month to an organisation sending thousands, the setup is the same and the card fees stay with NAB.</p>
  </div>
  <div class="sizes">
    <div class="size"><div class="bars" aria-hidden="true"><i class="on" style="height:30%"></i><i style="height:50%"></i><i style="height:72%"></i><i style="height:100%"></i></div>
      <h3>Small businesses</h3><p>Sole traders, practices and small teams who want invoices paid on time without chasing or paying a middleman.</p><span class="plan-tag">Usually <span>Starter</span></span></div>
    <div class="size mid"><div class="bars" aria-hidden="true"><i class="on" style="height:30%"></i><i class="on" style="height:50%"></i><i class="on" style="height:72%"></i><i style="height:100%"></i></div>
      <h3>Medium-sized businesses</h3><p>Growing teams with regular clients, retainers and repeating invoices, where autopay and reconciliation save hours each month.</p><span class="plan-tag">Usually <span>Growth</span></span></div>
    <div class="size"><div class="bars" aria-hidden="true"><i class="on" style="height:30%"></i><i class="on" style="height:50%"></i><i class="on" style="height:72%"></i><i class="on" style="height:100%"></i></div>
      <h3>Larger organisations</h3><p>Businesses sending more than 1,000 invoices a month, or with several entities. We will tailor a plan around your volume.</p><span class="plan-tag">Talk to us <span>Custom</span></span></div>
  </div>
  <div class="inds">
    <a class="ind a" href="solutions-services.html"><span class="ic">{MI['brief']}</span><h3>Service-based businesses</h3><p>Retainers, appointments, projects and memberships, paid on time.</p>
      <div class="vig"><div class="top"><div><b>Monthly retainer</b><span class="muted">Olive &amp; Co Pty Ltd</span></div><span class="pill amber">Autopay 1 Dec</span></div><div class="amt num">$1,320.00</div></div><span class="go">Service-based businesses</span></a>
    <a class="ind b" href="solutions-hospitality.html"><span class="ic">{MI['cup']}</span><h3>Restaurants and cafes</h3><p>Catering orders, function deposits and corporate accounts, paid by card.</p>
      <div class="vig"><div class="top"><div><b>Function deposit</b><span class="muted">40 guests, Saturday 13 Dec</span></div><span class="pill blue">Pay now</span></div><div class="amt num">$1,500.00</div></div><span class="go">Restaurants and cafes</span></a>
    <a class="ind c" href="solutions-ecommerce.html"><span class="ic">{MI['bag']}</span><h3>E-commerce</h3><p>Wholesale, trade and made-to-order sales that go out on an invoice.</p>
      <div class="vig"><div class="top"><div><b>Wholesale order 1042</b><span class="muted">24 units, trade account</span></div><span class="pill green">Paid by card</span></div><div class="amt num">$2,184.00</div></div><span class="go">E-commerce</span></a>
  </div>
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

<section class="band tight"><div class="wrap split">
  <div class="stage">
    <div class="recon">
      <div class="rh"><span class="x"><img src="assets/logos/xero.png" alt="">Payment recorded in Xero</span><span class="pill green">Reconciled</span></div>
      <dl>
        <dt>Invoice</dt><dd>INV-0238, Northside Physio</dd>
        <dt>Customer</dt><dd>Priya Sharma</dd>
        <dt>Amount</dt><dd class="num">$121.00</dd>
        <dt>Paid to account</dt><dd>NAB Gateway clearing</dd>
        <dt>Reference</dt><dd class="num">NAB 7F3K2A</dd>
        <dt>Date</dt><dd class="num">25 Oct 2026</dd>
      </dl>
      <div class="rf"><span class="pill grey">No manual matching</span><span class="pill grey">Bank reference attached</span></div>
    </div>
  </div>
  <div>
    <span class="label">For bookkeepers and accountants</span>
    <h2 style="margin-top:16px">Made easy for the people who keep the books.</h2>
    <p class="lede" style="margin-top:16px">Every card payment is recorded against the right invoice in Xero as it happens, with the bank reference attached. Nothing to key in and nothing to chase.</p>
    <ul class="checks" style="max-width:500px">
      <li style="background:var(--oat)">Payments land against the invoice they paid</li>
      <li style="background:var(--oat)">You choose the Xero account payments are recorded to</li>
      <li style="background:var(--oat)">Card fees stay on the NAB statement, where you expect them</li>
      <li style="background:var(--oat)">A full record of every payment, refund and autopay change</li>
    </ul>
    <p style="margin-top:24px"><a class="textlink" href="solutions-accountants.html">Transiqe for bookkeepers and accountants</a></p>
  </div>
</div></section>

<section class="band tight"><div class="wrap"><div class="aus">
  <div>
    <span class="label">Made here</span>
    <h2 style="margin-top:16px">Built for Australian businesses.</h2>
    <p class="lede" style="margin-top:16px">Transiqe is built and supported in Sydney, for businesses that invoice in Australian dollars and bank with an Australian bank.</p>
    <span class="ausmark"><img src="assets/logos/nab.png" alt="NAB"><span>Works with NAB Gateway</span></span>
  </div>
  <ul>
    <li><b>Your Australian bank</b><span>Card payments run on your own NAB merchant facility and settle to your NAB account.</span></li>
    <li><b>Priced in Australian dollars</b><span>One flat monthly price. No foreign exchange, no percentage of your takings.</span></li>
    <li><b>Your Xero invoices, unchanged</b><span>GST, tax invoices and your branding stay exactly as Xero produces them.</span></li>
    <li><b>Australian privacy law</b><span>Personal information is handled under the Privacy Act 1988 and the Australian Privacy Principles.</span></li>
    <li><b>No surcharge on your customers</b><span>Customers pay the amount on the invoice. Transiqe never adds a card surcharge.</span></li>
    <li><b>Local support</b><span>Talk to the team that builds it, in your time zone, at hello@transiqe.com.</span></li>
  </ul>
</div></div></section>

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
    <p style="margin-top:22px"><a class="textlink" href="faq.html">See all questions</a></p>
  </div>
</div></section>

{CLOSER}
'''

page('index', 'Transiqe: card payments on your Xero invoices, through your own NAB Gateway',
     'Transiqe adds a Pay now button to your Xero invoices and connects it to your own NAB Gateway. Customers pay by card, the money settles to your NAB account at your agreed NAB rate, and the invoice is marked paid in Xero.',
     home)
