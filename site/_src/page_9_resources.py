# Resources: FAQ, Help centre, Articles.

def res_hero(key, tag, h1, lede, img, cls='', search=None):
    s = ''
    if search:
        s = (f'<div class="searchbox"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/>'
             f'<path d="M20 20l-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
             f'<label class="sr" for="q-{key}">{search[0]}</label><input id="q-{key}" type="search" placeholder="{search[0]}" data-filter="{search[1]}" autocomplete="off"></div>')
    inner = f'<div class="hero-grid"><div class="copy"><span class="tag">{tag}</span><h1>{h1}</h1><p class="lede">{lede}</p>{s}</div></div>'
    return hero('on-image', key, inner, img=img, cls=f'{cls} subhero')

# ================================================================== FAQ
FAQ = [
 ('getting-started', 'Getting started', [
  ('What is Transiqe?', 'Transiqe is software that connects your Xero invoices to your own NAB Gateway account. Your invoices get a Pay now button, your customers pay by card, the money settles to your NAB account, and the payment is recorded back in Xero.'),
  ('What do I need to use Transiqe?', 'A NAB Gateway account, which NAB provides to its business customers for taking card payments online, and a Xero subscription. If you do not use Xero, you can send invoices from Transiqe itself.'),
  ('How long does setup take?', 'Under five minutes if you have your NAB Gateway details to hand. Sign up, connect Xero, connect your NAB Gateway and switch on Pay now. The <a href="help.html#getting-started">setup guide</a> walks through each step.'),
  ('Do I need to apply or wait for approval?', 'Not from Transiqe. There is no application and no approval wait. You do need an active NAB Gateway account, which is arranged with NAB.'),
  ('I do not have a NAB Gateway account yet. What should I do?', 'Speak to your NAB business banker. Our article <a href="article-nab-gateway-checklist.html">What to ask NAB about a NAB Gateway account</a> lists the questions worth asking.'),
 ]),
 ('payments', 'Payments and fees', [
  ('How is this different from the payment option I use now?', 'Most payment add-ons are separate processors. They take the payment, charge their own fee and pay you out later. Transiqe is software only. The payment runs through your own NAB Gateway and settles to your NAB account, at the fees you agreed with NAB.'),
  ('What does it cost to take a card payment?', 'Card fees are the ones in your merchant agreement with NAB, and NAB charges them to you directly. Transiqe adds no percentage and no per-payment fee. You pay Transiqe a flat monthly subscription for the software.'),
  ('Does Transiqe hold my money?', 'No. Card payments go from your customer to your NAB merchant facility and settle to your account. Transiqe moves the information: the invoice to your customer and the payment record back to Xero.'),
  ('When does the money reach my account?', 'On NAB’s settlement timetable under your merchant agreement. Transiqe is not in the money flow, so it does not hold or delay settlement.'),
  ('Which cards can my customers use?', 'The card types your NAB Gateway facility is set up to accept. Check with NAB if you are not sure which ones are enabled.'),
  ('Will my customers pay a surcharge?', 'Not from Transiqe. Customers pay the amount on the invoice, and Transiqe never adds a card surcharge.'),
  ('How do refunds work?', 'Refund a payment from your Transiqe dashboard, or manually in your NAB Gateway if you prefer. Either way the money goes back to your customer’s card.'),
 ]),
 ('autopay', 'Autopay and repeating invoices', [
  ('What is autopay?', 'Autopay lets your customer save their card and have your future invoices paid automatically, on the timing they choose. It is always the customer’s choice and they see the <a href="autopay-terms.html">autopay terms</a> before they agree.'),
  ('Can customers turn autopay off?', 'Yes, at any time, from their portal or by asking you. Turning it off stops future automatic payments straight away.'),
  ('Is autopay the same as a direct debit?', 'No. Autopay is a recurring card payment. A direct debit takes money from a bank account. They have different rules. Our article <a href="article-autopay-vs-direct-debit.html">Autopay and direct debit are not the same thing</a> explains the difference.'),
  ('How do repeating invoices work?', 'Set them up in Xero as you do now. Each invoice Xero creates flows into Transiqe. Customers on autopay are charged automatically, and everyone else gets the invoice with a Pay now button.'),
  ('What happens if a card is declined?', 'Your customer is told straight away and can pay with another card. For autopay, Transiqe lets them know, tries again, and tells you both if it still cannot collect. The invoice stays open in Xero the whole time.'),
 ]),
 ('xero', 'Xero', [
  ('What does Transiqe do in my Xero account?', 'It reads your contacts and invoices and records payments against invoices. It does not create, edit or delete your invoices.'),
  ('Are my customers imported?', 'Yes. When you connect Xero, your customers and their open invoices are brought into Transiqe automatically, and new ones keep coming across as you add them.'),
  ('How do I add the Pay now button to my invoices?', 'Add Transiqe as a payment service on your invoice branding theme in Xero. The <a href="help.html#pay-now">Pay now guide</a> shows where.'),
  ('I do not use Xero. Can I still use Transiqe?', 'Yes. You can create and send invoices straight from Transiqe. Your customers get the same Pay now button, portal and autopay.'),
 ]),
 ('customers', 'Your customers', [
  ('Do my customers need an account?', 'No. They pay from the invoice. If they want to see past invoices or manage autopay, they can sign in to their portal with a link sent to their email.'),
  ('What is the customer portal?', 'A page for each of your customers, under your business name, where they can see open and paid invoices, pay what is due, download receipts and manage their saved card and autopay.'),
  ('Will my customers see the Transiqe name?', 'Your invoices, emails and the portal carry your business name. The web address of the payment page and its small print show that it is provided by Transiqe.'),
 ]),
 ('security', 'Security and privacy', [
  ('Does Transiqe store card numbers?', 'No. Card details are entered into fields provided by NAB Gateway. Transiqe keeps only the token NAB issues for saved cards, plus the card brand, last four digits and expiry. See <a href="security.html">security</a>.'),
  ('How is personal information handled?', 'Under the Privacy Act 1988 and the Australian Privacy Principles. Our <a href="privacy.html">privacy policy</a> sets out what we collect, why, and who we share it with.'),
  ('How do I report a security issue?', 'Email security@transiqe.com with enough detail for us to reproduce it.'),
 ]),
 ('billing', 'Plans and billing', [
  ('How much does Transiqe cost?', 'Starter is $49.95 a month for up to 100 invoices. Growth is $99 a month for up to 1,000 invoices. If you send more than 1,000 a month, talk to us. See <a href="pricing.html">pricing</a>.'),
  ('Are card fees included in my plan?', 'No. Card fees are charged by NAB under your merchant agreement. Your plan covers the Transiqe software only.'),
  ('Can I cancel?', 'Yes, at any time. Cancellation takes effect at the end of the billing period you have paid for. Your invoices in Xero and your merchant facility with NAB are not affected.'),
 ]),
]

faq_chips = ''.join(f'<a href="#{i}">{t}</a>' for i, t, _ in FAQ)
faq_body = ''
for i, t, qs in FAQ:
    items = ''.join(f'<details data-q><summary>{q}</summary><p>{a}</p></details>' for q, a in qs)
    faq_body += f'<section class="faqcat" id="{i}" data-group><h2>{t}</h2><div class="faq">{items}</div></section>'

faq_page = res_hero('faq', 'FAQ', 'Questions, answered.', 'Straight answers about how Transiqe works, what it costs, and what your customers see. Can’t find yours? Email hello@transiqe.com.',
                    'light-warm', search=('Search questions', '#faq-list')) + f'''
<section class="band"><div class="wrap faqlayout">
  <nav class="chips" aria-label="Topics">{faq_chips}</nav>
  <div id="faq-list">{faq_body}<p class="empty" data-empty hidden>No questions match that search. Try another word, or email hello@transiqe.com.</p></div>
</div></section>
{CLOSER}
'''
page('faq', 'FAQ · Transiqe', 'Answers to common questions about Transiqe: setup, card payments and fees, autopay, Xero, your customers, security and billing.', faq_page)

# ================================================================== Help centre
def guide(gid, title, steps, note=''):
    st = ''.join(f'<li>{s}</li>' for s in steps)
    n = f'<p class="gnote">{note}</p>' if note else ''
    return f'<details class="guide" id="{gid}" data-q><summary>{title}</summary><div class="gbody"><ol>{st}</ol>{n}</div></details>'

HELP = [
 ('getting-started', 'Getting started', MI['route'], 'Sign up, connect Xero and NAB Gateway, switch on Pay now', [
  guide('sign-up', 'Create your Transiqe account', [
     f'Go to <a href="{APP}/signup">app.transiqe.com/signup</a>.',
     'Enter your name, your business name and your work email, and choose a password.',
     'Choose your plan. You land on your dashboard with a short setup checklist.']),
  guide('connect-xero', 'Connect Xero', [
     'On your dashboard, select <b>Connect Xero</b>.',
     'Sign in to Xero and choose the organisation you invoice from.',
     'Approve the connection. Transiqe can read contacts and invoices and record payments. It does not create, edit or delete invoices.',
     'Your customers and open invoices are imported automatically. New ones keep coming across as you add them in Xero.']),
  guide('nab-keys', 'Find your NAB Gateway details', [
     'Sign in to your NAB Gateway account.',
     'Note your merchant ID. It is shown at the top of the page as your Transacting ID.',
     'Go to <b>Payment Configuration</b>, then <b>Key Management</b>.',
     'Select <b>Generate key</b> and choose a REST shared secret key.',
     'Copy the key ID and the shared secret. The shared secret is only shown once, so keep it somewhere safe until you have added it to Transiqe.'],
     'If your NAB Gateway screens look different, your NAB contact can point you to your API keys.'),
  guide('connect-nab', 'Connect your NAB Gateway', [
     'In Transiqe, go to <b>Settings</b>, then <b>NAB Gateway</b>.',
     'Enter your merchant ID, key ID and shared secret.',
     'Select <b>Save</b>. Transiqe checks the connection with NAB and shows <b>Connected</b> when it works.']),
  guide('pay-now', 'Switch on Pay now in Xero', [
     'In Transiqe, go to <b>Settings</b> and copy your Pay now link.',
     'In Xero, open your invoice settings and go to <b>Payment services</b>.',
     'Add a payment service, choose <b>Custom payment URL</b>, and paste your Pay now link.',
     'Apply it to the invoice branding themes you use. Invoices sent with those themes now carry a Pay now button.']),
  guide('test', 'Send yourself a test invoice', [
     'In Xero, create an invoice for a small amount to yourself and approve it.',
     'Open the invoice from the email and select <b>Pay now</b>.',
     'Pay with your own card. The payment appears in your Transiqe dashboard and the invoice is marked paid in Xero.',
     'Refund it from the dashboard if you like. See <a href="#refund">refunding a payment</a>.']),
 ]),
 ('getting-paid', 'Getting paid', MI['spark'], 'How customers pay, reminders, refunds and declined cards', [
  guide('how-customers-pay', 'How your customer pays an invoice', [
     'Your customer opens the invoice email and selects <b>Pay now</b>.',
     'They see your business name, the invoice and the amount due.',
     'They enter their card into fields provided by NAB Gateway and confirm.',
     'They get a receipt, the money settles to your NAB account, and the invoice is marked paid in Xero.']),
  guide('reminders', 'Payment reminders', [
     'Transiqe sends reminders for overdue invoices automatically, each with the Pay now button.',
     'To send an invoice again yourself, open it in <b>Invoices</b> and select <b>Email pay link</b>.',
     'Every email sent to a customer is listed in your account, so you can see what went out and when.']),
  guide('refund', 'Refunding a payment', [
     'Go to <b>Payments</b> and find the payment.',
     'Select <b>Refund</b> and confirm.',
     'The money goes back to the customer’s card through your NAB Gateway.',
     'Prefer to do it yourself? You can also refund the payment manually in your NAB Gateway.',
     'Record the refund in Xero as you normally would.']),
  guide('declined', 'When a card is declined', [
     'If a customer’s card is declined while paying, they are told straight away and can try another card.',
     'If an autopay charge is declined, the customer is emailed and the payment is tried again.',
     'If it still cannot be collected, automatic attempts stop and you are both told. The invoice stays open in Xero.']),
 ]),
 ('autopay', 'Autopay', MI['user'], 'Opting in, turning it off, repeating invoices', [
  guide('autopay-on', 'How customers turn on autopay', [
     'When paying an invoice, your customer ticks the option to save their card and pay future invoices automatically.',
     'Or they sign in to their portal and go to <b>Autopay and cards</b>.',
     'They choose when their card is charged and accept the autopay terms.']),
  guide('autopay-off', 'Turning autopay off for a customer', [
     'Go to <b>Customers</b> and open the customer.',
     'Under <b>Autopay</b>, turn it off and save.',
     'Any scheduled charges for that customer are cancelled. Customers can also turn it off themselves in their portal.']),
  guide('repeating', 'Repeating invoices with autopay', [
     'Set up the repeating invoice in Xero as usual.',
     'Each invoice Xero creates flows into Transiqe automatically.',
     'Customers on autopay are charged on the timing they chose. Everyone else receives the invoice with a Pay now button.']),
 ]),
 ('customers', 'Your customers', MI['brief'], 'Portal invites and customer details', [
  guide('portal-invite', 'Inviting a customer to their portal', [
     'Go to <b>Customers</b> and open the customer.',
     'Select <b>Send portal invite</b>. They receive an email with a secure sign-in link.',
     'Customers can also request a new link at any time from the portal sign-in page.']),
  guide('customer-email', 'Updating a customer’s email address', [
     'Update the contact in Xero and the change comes across to Transiqe.',
     'Or open the customer in Transiqe, change the email and save. This does not change Xero.']),
 ]),
 ('account', 'Account and billing', MI['calc'], 'Keys, connections and your subscription', [
  guide('replace-keys', 'Replacing your NAB Gateway keys', [
     'In NAB Gateway, generate a new REST shared secret key as described in <a href="#nab-keys">finding your NAB Gateway details</a>.',
     'In Transiqe, go to <b>Settings</b>, then <b>NAB Gateway</b>, and select <b>Replace keys</b>.',
     'Enter the new key ID and shared secret and save. Replace your keys straight away if you think they may have been exposed.']),
  guide('disconnect-xero', 'Disconnecting Xero', [
     'In Transiqe, go to <b>Settings</b> and select <b>Disconnect</b> next to Xero. You can also remove the connection from inside Xero.',
     'Your customers and invoices stay in Transiqe, but new invoices stop coming across until you connect again.']),
  guide('cancel', 'Cancelling your subscription', [
     'Email hello@transiqe.com from the address on your account, or cancel from your account settings.',
     'Cancellation takes effect at the end of the billing period you have paid for.',
     'Scheduled autopay charges stop. Your invoices in Xero and your merchant facility with NAB are not affected.']),
 ]),
]

help_cats = ''.join(f'<a class="hcat" href="#{i}"><span class="dd-ic">{ic}</span><span><b>{t}</b><small>{d}</small><em>{len(gs)} guides</em></span></a>' for i, t, ic, d, gs in HELP)
help_body = ''.join(f'<section class="hsec" id="{i}" data-group><h2>{t}</h2>{"".join(gs)}</section>' for i, t, ic, d, gs in HELP)

help_page = res_hero('help', 'Help centre', 'How can we help?', 'Step-by-step guides for setting up Transiqe, getting paid, autopay and your account.',
                     'light-dusk', 'cool', search=('Search the guides', '#help-list')) + f'''
<section class="band tight"><div class="wrap">
  <div class="hcats">{help_cats}</div>
</div></section>
<section class="band" style="padding-top:0"><div class="wrap">
  <div id="help-list" class="hlist">{help_body}<p class="empty" data-empty hidden>No guides match that search. Try another word, or email hello@transiqe.com.</p></div>
  <div class="tile oat" style="margin-top:36px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap">
    <div><h3>Still stuck?</h3><p style="margin-top:6px">Email the team that builds Transiqe and we will help you get set up.</p></div>
    <a class="btn ink" href="mailto:hello@transiqe.com">hello@transiqe.com</a>
  </div>
  <p class="tiny muted" style="margin-top:14px">Guides describe Transiqe, Xero and NAB Gateway as they work in November 2026. Screen names in Xero and NAB Gateway may change.</p>
</div></section>
'''
page('help', 'Help centre · Transiqe', 'Step-by-step guides for setting up Transiqe: connecting Xero and NAB Gateway, switching on Pay now, autopay, refunds and your account.', help_page)

# ================================================================== Articles
ARTICLES = [
 ('article-autopay-vs-direct-debit', 'Autopay and direct debit are not the same thing',
  'What each one is, who can stop it, and what to tell your customers so there are no surprises.',
  '25 November 2026', '5 min read', 'light-ink', 'Autopay', '''
<p>Customers often call any automatic payment a direct debit. In Australia the two work differently, and the difference matters when a customer wants to stop paying, or disputes a charge. If you offer autopay, it helps to use the right words.</p>
<h2>What autopay is</h2>
<p>Autopay in Transiqe is a recurring card payment. Your customer saves their card while paying an invoice, or in their portal, and agrees to have your future invoices paid automatically. The card is stored by NAB, and your business charges it for each invoice on the timing your customer chose.</p>
<p>Nothing is taken from a bank account directly. The payment goes through the card networks, the same way as if your customer had typed in their card that day.</p>
<h2>What a direct debit is</h2>
<p>A direct debit takes money straight from a bank account. The customer signs a direct debit request that lets a business, or a company acting for it, debit their account. Newer arrangements use PayTo, where the customer approves a payment agreement in their own banking app and can pause or cancel it there.</p>
<h2>Who can stop each one</h2>
<ul>
<li><strong>Autopay.</strong> Your customer can turn it off at any time in their portal, or ask you to. Transiqe stops future charges straight away. They can also ask their card issuer about stopping payments to a merchant, or dispute a charge they do not recognise.</li>
<li><strong>Direct debit.</strong> A customer can ask their own bank to cancel a direct debit, and the bank must act on the request.</li>
</ul>
<p>Because the rules differ, calling autopay a direct debit can give a customer the wrong idea of how to stop it, or where to go if something goes wrong.</p>
<h2>What to tell your customers</h2>
<p>Keep it short and plain. Something like this works well in an email or on your invoice:</p>
<div class="note">You can now have our invoices paid automatically by saving a card when you pay. You choose when your card is charged, you will get every invoice and a receipt for every payment, and you can turn it off at any time from your customer portal.</div>
<p>Transiqe shows the <a href="autopay-terms.html">autopay terms</a> to every customer before they opt in, so the details are covered. Your job is to make the offer clearly and to respect a customer’s request to stop.</p>
<h2>The short version</h2>
<ul>
<li>Autopay is a saved card, charged for each invoice. Direct debit is a bank account debit.</li>
<li>Customers stop autopay in their portal or by asking you, and Transiqe stops future charges straight away.</li>
<li>Say autopay, not direct debit, so customers know exactly what they have agreed to.</li>
</ul>'''),
 ('article-retainers-autopay', 'Retainers without the chasing: repeating invoices and autopay',
  'How to set up monthly billing in Xero so regular clients are paid on time, every time, without a reminder.',
  '25 November 2026', '4 min read', 'light-warm', 'Getting paid', '''
<p>If you bill the same clients every month, the invoice is the easy part. Getting it paid on time is where the hours go. Combining repeating invoices in Xero with autopay in Transiqe takes most of that work away.</p>
<h2>1. Set up the repeating invoice in Xero</h2>
<p>Create a repeating invoice for each retainer client, as you do now. Pick a billing day you will keep, such as the first of the month, and set the due date your terms allow. Each invoice Xero creates flows into Transiqe automatically.</p>
<h2>2. Offer autopay to your regular clients</h2>
<p>The first time a client pays by card, they can tick a box to save their card and have future invoices paid automatically. You can also send them a portal invite, where they can switch autopay on with the card they choose.</p>
<p>Tell clients before you ask. A one-line note in your next invoice email is enough: what autopay is, that it is optional, and that they can turn it off at any time.</p>
<h2>3. Let clients choose the timing</h2>
<p>Some clients want to be charged the day the invoice arrives. Others prefer the due date, or a few days before it. Transiqe lets each client pick, which makes autopay an easier yes for finance teams with their own payment runs.</p>
<h2>4. Know what happens when a card fails</h2>
<p>Cards expire and limits get reached. If an autopay charge is declined, the client is emailed with a link to pay another way, and the charge is tried again. If it still cannot be collected, automatic attempts stop and you are both told. The invoice stays open in Xero, so nothing falls through the gaps.</p>
<h2>A month later</h2>
<p>On billing day, Xero creates the invoices, Transiqe charges the clients on autopay, the money settles to your NAB account, and each invoice is marked paid in Xero. The clients who are not on autopay get the invoice with a Pay now button, and a reminder if it goes overdue.</p>
<div class="note">Tip: start with your five most regular clients. Once they are on autopay, the rest usually follow when they see how little they need to do.</div>'''),
 ('article-nab-gateway-checklist', 'What to ask NAB about a NAB Gateway account',
  'A short checklist for the conversation with your NAB business banker, so your account is set up for invoices and autopay from day one.',
  '25 November 2026', '4 min read', 'light-dusk', 'Getting started', '''
<p>To take card payments through Transiqe, you need a NAB Gateway account: the facility NAB provides for taking card payments online. If you do not have one yet, your NAB business banker can set it up. These are the questions worth asking so it suits invoicing and autopay from the start.</p>
<h2>About the facility</h2>
<ul>
<li><strong>Is it set up for online payments?</strong> Invoice payments are made online, without the card in front of you, so the facility needs to allow that.</li>
<li><strong>Which cards will it accept?</strong> Ask which card types are enabled, and whether American Express is included or arranged separately.</li>
<li><strong>What are the fees?</strong> Ask for the rate, any monthly fee, and how fees are charged to you. These are between you and NAB, and Transiqe adds nothing to them.</li>
<li><strong>Where and when does it settle?</strong> Confirm which account payments settle to and how long settlement takes.</li>
</ul>
<h2>About saved cards and autopay</h2>
<ul>
<li><strong>Can cards be stored for future payments?</strong> Autopay needs the facility to save a customer’s card securely as a token, so future invoices can be charged without the card details.</li>
<li><strong>Are refunds enabled?</strong> You will want to be able to refund from your Transiqe dashboard, as well as manually in NAB Gateway.</li>
<li><strong>Is extra authentication required?</strong> Ask whether customers will be asked to confirm some payments with their bank, and when.</li>
</ul>
<h2>About connecting Transiqe</h2>
<ul>
<li><strong>Can I generate API keys?</strong> Transiqe connects using a REST shared secret key, which you generate in NAB Gateway under Payment Configuration and Key Management.</li>
<li><strong>Who do I call if something stops working?</strong> Note your NAB Gateway support contact alongside your merchant ID.</li>
</ul>
<h2>What to have ready</h2>
<p>Your ABN and business details, a description of what you sell and how you invoice, and your website if you have one. Once your NAB Gateway account is live, connecting it to Transiqe takes a couple of minutes. The <a href="help.html#getting-started">setup guide</a> walks you through it.</p>'''),
]

def art_card(a):
    slug, t, ex, d, rt, img, cat = a[:7]
    return (f'<a class="acard" href="{slug}.html"><span class="ai"><img src="assets/img/{img}-900.webp" alt="" loading="lazy"><span class="acat">{cat}</span></span>'
            f'<span class="ab"><span class="meta">{d} &middot; {rt}</span><b>{t}</b><small>{ex}</small><span class="go">Read the article</span></span></a>')

blog_page = res_hero('blog', 'Articles', 'Guides on getting paid on time.', 'Practical articles for Australian businesses that invoice from Xero: card payments, autopay, and setting up with NAB.',
                     'light-teal', 'cool') + f'''
<section class="band"><div class="wrap">
  <div class="acards">{''.join(art_card(a) for a in ARTICLES)}</div>
</div></section>
{CLOSER}
'''
page('blog', 'Articles · Transiqe', 'Practical guides for Australian businesses on card payments, autopay and getting paid on time from Xero.', blog_page)

for a in ARTICLES:
    slug, t, ex, d, rt, img, cat, body = a
    others = ''.join(art_card(o) for o in ARTICLES if o[0] != slug)
    inner = (f'<div class="hero-grid"><div class="copy"><span class="tag">{cat}</span><h1>{t}</h1><p class="lede">{ex}</p>'
             f'<p class="ameta">{d} &middot; {rt}</p></div></div>')
    html_ = hero('on-image', 'blog', inner, img=img, cls='cool subhero') + f'''
<section class="band"><div class="wrap"><article class="prose articlebody">{body}
  <p class="backlink"><a class="textlink" href="blog.html">All articles</a></p></article></div></section>
<section class="band tight" style="padding-top:0"><div class="wrap"><h2 style="font-size:clamp(24px,2.6vw,32px);margin-bottom:20px">More articles</h2><div class="acards two">{others}</div></div></section>
{CLOSER}
'''
    page(slug, f'{t} · Transiqe', ex, html_)
