# Solutions pages: one per kind of business. Names and figures in the cards are samples.

def vig(title, sub, pill, pill_text, amt=''):
    a = f'<div class="amt num">{amt}</div>' if amt else ''
    return (f'<div class="vig"><div class="top"><div><b>{title}</b><span class="muted">{sub}</span></div>'
            f'<span class="pill {pill}">{pill_text}</span></div>{a}</div>')


def sol_art(cards):
    pos = ['left:6%;top:4%', 'right:0;top:2%', 'right:2%;top:50%', 'left:2%;bottom:2%']
    cls = ['fa', 'fb', 'fc', 'fd']
    return '<div class="art" aria-hidden="true">' + ''.join(
        fl(c, pos[i], i, [10, 22, 30, 18][i], [-4, 3, -2, 2][i], [8, 6.5, 7.5, 9][i], cls[i]) for i, c in enumerate(cards)) + '</div>'


def mini_card(who, sub, amt, btn=None, pill=None):
    b = f'<div class="btn cobalt block sm">{btn}</div>' if btn else ''
    p = f'<span class="pill {pill[0]}" style="margin-top:2px">{pill[1]}</span>' if pill else ''
    return f'<div class="glass mini"><div class="who">{who}</div><div class="tiny muted">{sub}</div><div class="amt num">{amt}</div>{b}{p}</div>'


def chip(kind, title, sub='', ok=False, toggle=False):
    lead = '<span class="dotok"></span>' if ok else ('<span class="toggle"></span>' if toggle else '')
    s = f'<small>{sub}</small>' if sub else ''
    cls = {'glass': 'glass chipx', 'dark': 'chipx dark', 'warm': 'chipx warm'}[kind]
    return f'<div class="{cls}">{lead}<span>{title}{s}</span></div>'


def solution_page(name, key, title, desc, tag, h1, lede, img, pos, cls, art, flip,
                  intro, cases, flow, note, faqs):
    hero_html = (f'<div class="hero-grid with-art"><div class="copy"><span class="tag">{tag}</span><h1>{h1}</h1>'
                 f'<p class="lede">{lede}</p><div class="cta"><a class="btn white lg" href="{APP}/signup">Sign up <span class="arr">&rarr;</span></a>'
                 f'<a class="btn ghost lg" href="how-it-works.html">See how it works</a></div></div>{art}</div>')
    case_html = ''.join(f'<div class="case"><h3>{t}</h3><p>{p}</p>{v}</div>' for t, p, v in cases)
    flow_html = ''.join(f'<div><span class="k">{w}</span><b>{t}</b><p>{p}</p></div>' for w, t, p in flow)
    note_html = (f'<section class="band tight"><div class="wrap"><div class="tile ink" style="padding:clamp(24px,4vw,44px);display:grid;gap:10px;max-width:980px">'
                 f'<h3>{note[0]}</h3><p style="max-width:70ch">{note[1]}</p></div></div></section>') if note else ''
    faq_html = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faqs))
    body = hero('on-image', key, hero_html, img=img, cls=f'{cls} subhero', pos=pos, flip=flip) + f'''
<div class="wrap"><div class="connect">
  <span class="lbl">Works with your</span>
  <span class="lg"><img class="x" src="assets/logos/xero.png" alt="Xero" width="54" height="54"><span class="amp">+</span><img class="n" src="assets/logos/nab.png" alt="NAB" width="102" height="40"></span>
</div></div>

<section class="band"><div class="wrap">
  <div class="head"><div><span class="label">Where Transiqe fits</span><h2>{intro[0]} <span class="soft">{intro[1]}</span></h2></div>
  <p class="lede">{intro[2]}</p></div>
  <div class="cases">{case_html}</div>
  {SAMPLE_NOTE}
</div></section>

<section class="band tight"><div class="wrap">
  <div class="head single"><div><span class="label">How it runs</span><h2>From invoice to paid, <span class="soft">without you chasing.</span></h2></div></div>
  <div class="journey" style="grid-template-columns:repeat({len(flow)},minmax(0,1fr))">{flow_html}</div>
</div></section>

{note_html}

<section class="band tight"><div class="wrap faqwrap">
  <div><span class="label">Questions</span><h2 style="margin-top:16px">Common questions.</h2>
  <p style="margin-top:20px"><a class="textlink" href="faq.html">See all questions</a></p></div>
  <div class="faq">{faq_html}</div>
</div></section>

{CLOSER}
'''
    page(name, title, desc, body)


# ---------------------------------------------------------------- services
solution_page(
    'solutions-services', 'services', 'Transiqe for service-based businesses',
    'Card payments and autopay on the Xero invoices you send for your services: retainers, appointments, projects and memberships, paid through your own NAB Gateway.',
    'Service-based businesses', 'Get paid for your time, without chasing it.',
    'For consultants, agencies, clinics, trades, tutors and anyone who invoices for a service. Your Xero invoices get a Pay now button connected to your own NAB Gateway, and regular clients can put their invoices on autopay.',
    'owner-laptop', '62% 26%', '', sol_art([
        mini_card('Monthly retainer', 'Olive &amp; Co Pty Ltd', '$1,320.00', pill=('amber', 'Autopay on 1 Dec')),
        chip('glass', 'Session paid', '$121.00, Priya Sharma', ok=True),
        chip('dark', 'Marked paid in Xero', 'INV-0238, just now', ok=True),
        chip('warm', 'Reminder sent', 'INV-0224, 3 days overdue'),
    ]), False,
    ('Retainers, sessions and projects.', 'All paid the same way.',
     'Whatever you sell your time for, the invoice still comes from Xero. Transiqe adds the card payment, the reminders and the bookkeeping that follows.'),
    [
        ('Retainers and memberships', 'Set up a repeating invoice in Xero. Clients who opt in to autopay are charged on the day they choose, every month.',
         vig('Monthly retainer', 'Olive &amp; Co Pty Ltd', 'amber', 'Autopay 1 Dec', '$1,320.00')),
        ('Appointments and sessions', 'Send the invoice straight after the session. Your client can pay by card from the email, on their phone.',
         vig('Physio session, 45 minutes', 'Priya Sharma', 'blue', 'Pay now', '$121.00')),
        ('Projects and milestones', 'Invoice a deposit, then each milestone. Every payment lands against the right invoice in Xero.',
         vig('Website build, milestone 2 of 3', 'Coastline Builders', 'green', 'Paid by card', '$4,400.00')),
        ('Overdue invoices', 'Reminders go out with the Pay now button, so paying is one tap for your client.',
         vig('Payment reminder', 'INV-0224, 3 days overdue', 'grey', 'Reminder sent', '$660.00')),
    ],
    [('You', 'Finish the work', 'Or reach the next billing date for a retainer.'),
     ('You', 'Send the invoice from Xero', 'With a Pay now button on it.'),
     ('Your client', 'Pays by card', 'Or is charged automatically if they chose autopay.'),
     ('Transiqe', 'Records it in Xero', 'The money settles to your NAB account.')],
    None,
    [('Can different clients pay at different times?', 'Yes. Each client chooses whether to use autopay and when their card is charged: when the invoice is issued, on the due date, or a set number of days before.'),
     ('What if a client prefers to pay by bank transfer?', 'They still can. The Pay now button is an extra option on your invoice. Payments made any other way are recorded in Xero as they are today.'),
     ('Do my clients need an account?', 'No. They pay from the invoice. If they want to see past invoices or manage autopay, they can sign in to their portal with a link sent to their email.')],
)

# ---------------------------------------------------------------- restaurants and cafes
solution_page(
    'solutions-hospitality', 'hospitality', 'Transiqe for restaurants and cafes',
    'Card payments on the invoices restaurants and cafes send: catering orders, function deposits, corporate accounts and wholesale, paid through your own NAB Gateway.',
    'Restaurants and cafes', 'Card payments for the sales that go out on an invoice.',
    'Catering orders, functions and events, and businesses that run an account with you. Send the invoice from Xero, your customer pays by card, and the money settles to your NAB account.',
    'light-gold', 'center', '', sol_art([
        mini_card('Function deposit', '40 guests, Saturday 13 Dec', '$1,500.00', btn='Pay now'),
        chip('glass', 'Corporate account', 'Monthly invoice, on autopay', toggle=True),
        chip('dark', 'Marked paid in Xero', 'Catering order, just now', ok=True),
        chip('warm', 'Catering order paid', 'Office lunch for 25'),
    ]), False,
    ('Catering, functions and accounts.', 'The orders that come with an invoice.',
     'Counter and table sales stay on your EFTPOS terminal. Transiqe looks after the sales you invoice, so they are paid by card and recorded in Xero without chasing.'),
    [
        ('Catering orders', 'Quote and invoice office lunches, platters and events. The client pays by card from the invoice before the order goes out.',
         vig('Catering order', 'Office lunch for 25, Friday', 'blue', 'Pay now', '$875.00')),
        ('Functions and events', 'Take a deposit to hold the date, then invoice the balance after the event. Both are paid by card and recorded in Xero.',
         vig('Function deposit', '40 guests, Saturday 13 Dec', 'green', 'Paid by card', '$1,500.00')),
        ('Corporate and regular accounts', 'Businesses that run a tab with you get one invoice a week or a month. They can opt in to autopay so it is paid on the due date.',
         vig('Monthly account', 'Harbourside Legal', 'amber', 'Autopay 30 Nov', '$2,340.00')),
        ('Wholesale and trade', 'If you supply coffee, baked goods or meals to other businesses, invoice them from Xero and get paid by card.',
         vig('Wholesale beans, 12 kg', 'The Corner Store', 'green', 'Paid by card', '$456.00')),
    ],
    [('You', 'Confirm the order or booking', 'Catering, a function, or a month on account.'),
     ('You', 'Send the invoice from Xero', 'A deposit, the balance, or the monthly account.'),
     ('Your customer', 'Pays by card', 'Or is charged on the due date if they chose autopay.'),
     ('Transiqe', 'Records it in Xero', 'The money settles to your NAB account.')],
    ('Transiqe works alongside your EFTPOS terminal.', 'Transiqe is for sales you invoice. For customers paying at the counter or the table, keep using your EFTPOS terminal and point-of-sale system as you do today.'),
    [('Does Transiqe replace my EFTPOS or point-of-sale system?', 'No. Transiqe is for invoiced sales such as catering, functions and accounts. Counter and table sales stay on your EFTPOS terminal.'),
     ('Can I take a deposit and then the balance?', 'Yes. Send them as two invoices from Xero, each with a Pay now button. Both payments are recorded in Xero against their own invoice.'),
     ('Do my corporate customers have to use autopay?', 'No. Autopay is always the customer’s choice. They can pay each invoice from the email instead.')],
)

# ---------------------------------------------------------------- e-commerce
solution_page(
    'solutions-ecommerce', 'ecommerce', 'Transiqe for e-commerce businesses',
    'Card payments on the orders e-commerce businesses invoice: wholesale, trade accounts, custom orders and standing orders, paid through your own NAB Gateway.',
    'E-commerce', 'For the orders that go out on an invoice.',
    'Wholesale and trade customers, custom and made-to-order jobs, and regular orders. Invoice from Xero, your customer pays by card through your own NAB Gateway, and the payment is recorded back in Xero.',
    'light-teal', 'center', 'cool', sol_art([
        mini_card('Wholesale order 1042', '24 units, Bayside Gifts', '$2,184.00', btn='Pay now'),
        chip('glass', 'Trade account', 'Autopay on the due date', toggle=True),
        chip('dark', 'Marked paid in Xero', 'Order 1042, just now', ok=True),
        chip('warm', 'Custom order deposit', 'Order 2207, paid'),
    ]), False,
    ('Wholesale, trade and custom orders.', 'Paid by card, straight to your NAB account.',
     'Your online store handles its own checkout. Transiqe handles the sales you invoice, so business customers can pay by card instead of you waiting on a bank transfer.'),
    [
        ('Wholesale and stockists', 'Invoice the retailers who stock your products. They pay by card from the invoice instead of by bank transfer days later.',
         vig('Wholesale order 1042', '24 units, Bayside Gifts', 'blue', 'Pay now', '$2,184.00')),
        ('Trade accounts', 'Customers on 14 or 30-day terms can opt in to autopay, so their card is charged on the due date.',
         vig('Trade account, November', 'Ridge Builders Supply', 'amber', 'Autopay 30 Nov', '$3,960.00')),
        ('Custom and made-to-order', 'Invoice a deposit before you start and the balance before you ship.',
         vig('Custom dining table, deposit', 'Order 2207', 'green', 'Paid by card', '$1,200.00')),
        ('Standing orders', 'Use repeating invoices in Xero for regular orders, with autopay for customers who opt in.',
         vig('Coffee, 2 kg monthly', 'Standing order', 'amber', 'Autopay 1 Dec', '$96.00')),
    ],
    [('Your customer', 'Places the order', 'Wholesale, trade or custom.'),
     ('You', 'Send the invoice from Xero', 'A deposit, the full amount, or the month on account.'),
     ('Your customer', 'Pays by card', 'Or is charged on the due date if they chose autopay.'),
     ('Transiqe', 'Records it in Xero', 'The money settles to your NAB account.')],
    ('Your online store’s checkout stays as it is.', 'Transiqe handles the orders you invoice. Checkout through your own NAB Gateway for online stores is on the way. If you would like early access, email hello@transiqe.com.'),
    [('Does Transiqe work with my online store’s checkout?', 'Not yet. Today Transiqe handles the orders you invoice from Xero or from Transiqe. Checkout for online stores through your own NAB Gateway is on the way.'),
     ('Can trade customers pay on terms?', 'Yes. The invoice carries its due date from Xero. Customers can pay any time before then, or opt in to autopay so their card is charged on the due date.'),
     ('Are card fees different for large orders?', 'Card fees are set by your merchant agreement with NAB. Transiqe adds nothing to them, whatever the size of the order.')],
)

# ---------------------------------------------------------------- bookkeepers and accountants
solution_page(
    'solutions-accountants', 'accountants', 'Transiqe for bookkeepers and accountants',
    'When your clients take card payments through Transiqe, each payment is recorded against the invoice it paid in Xero, with the bank reference attached.',
    'Bookkeepers and accountants', 'Card payments that reconcile themselves in Xero.',
    'When your clients take card payments through Transiqe, each payment is recorded against the invoice it paid, with the bank reference attached. Less matching, fewer questions, cleaner books.',
    'owner-tablet', '30% 28%', 'cool', sol_art([
        mini_card('Payment recorded in Xero', 'INV-0238, Northside Physio', '$121.00', pill=('green', 'Reconciled')),
        chip('glass', 'Paid to account', 'NAB Gateway clearing'),
        chip('dark', 'Bank reference attached', 'NAB 7F3K2A', ok=True),
        chip('warm', 'Activity log', 'Every payment and autopay change'),
    ]), True,
    ('Fewer card payments to match.', 'More time for the work that matters.',
     'Transiqe records each card payment in Xero against the invoice it paid, so the bank feed matches without a hunt through spreadsheets and emails.'),
    [
        ('Payments against the right invoice', 'Each card payment is recorded in Xero against the invoice it paid, dated the day it was made.',
         vig('Payment recorded', 'INV-0238, Northside Physio', 'green', 'Reconciled', '$121.00')),
        ('Your choice of account', 'Record payments to the business bank account or to a clearing account, whichever suits how NAB settles for your client.',
         vig('Paid to account', 'NAB Gateway clearing', 'grey', 'Set in Transiqe')),
        ('Bank reference on every payment', 'The NAB reference is on the payment in Xero, so matching it to the bank feed is quick.',
         vig('Reference', 'NAB 7F3K2A', 'green', 'Matched', '$121.00')),
        ('A clear record', 'Every payment, refund, declined card and autopay change is logged in your client’s Transiqe account.',
         vig('Activity', 'Autopay turned off by customer', 'grey', 'Logged')),
    ],
    [('Your client', 'Sends the invoice from Xero', 'Nothing changes in how they invoice.'),
     ('Their customer', 'Pays by card', 'Through your client’s own NAB Gateway.'),
     ('NAB', 'Settles to their account', 'Under their own merchant agreement.'),
     ('Transiqe', 'Records it in Xero', 'Against the invoice, with the reference.'),
     ('You', 'Reconcile', 'The payment is already where it belongs.')],
    ('Looking after several clients?', 'Talk to us about setting Transiqe up across your practice. Email hello@transiqe.com and tell us how many clients you look after.'),
    [('Does Transiqe change anything in my client’s Xero file?', 'It reads contacts and invoices and records payments against invoices. It does not create, edit or delete invoices.'),
     ('Where do the card fees show up?', 'Card fees are charged by NAB under your client’s merchant agreement and appear on their NAB merchant statement. Transiqe records the payment in Xero at the amount paid.'),
     ('How are refunds handled?', 'Refunds are issued from the Transiqe dashboard and go back to the customer’s card through NAB Gateway. Record the refund in Xero as you normally would.')],
)
