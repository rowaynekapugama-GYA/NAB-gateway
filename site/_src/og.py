# Link preview cards (the image shown when a page link is shared by SMS, WhatsApp,
# iMessage, email, LinkedIn, Facebook or Slack). One image per page, 1200 x 630.
#
# build.py reads OG to write the og: and twitter: tags. make_og.py renders the
# images into assets/og/. Re-run make_og.py after changing anything here.
#
# Each card: img (banner photo in assets/img), pos (background position),
# flip (mirror the photo), tag, h (headline), and card (the floating card on the
# right): (title, subtitle, amount, chip, chip colour, button) plus ticks (up to 3).

INVOICE = dict(card=('Northside Physio', 'Invoice INV-0238', '$121.00', 'Due 25 Oct', 'blue', 'Pay now'),
               ticks=['Paid by card through your NAB Gateway', 'Settles to your NAB account', 'Marked paid in Xero'])

OG = {
    'index': dict(img='owner-tablet', pos='40% 30%', flip=True,
                  tag='For businesses that use Xero and bank with NAB',
                  h='Card payments on your Xero invoices, through your own NAB&nbsp;Gateway.', **INVOICE),
    'how-it-works': dict(img='light-dusk', pos='center', tag='How it works',
                         h='From Xero invoice to your NAB account, step by step.', **INVOICE),
    'features': dict(img='light-warm', pos='center', tag='Features',
                     h='Everything between the invoice and your bank. Handled.',
                     card=('Your dashboard', 'This week', '$8,412.50', 'Paid by card', 'green', None),
                     ticks=['Pay now on every Xero invoice', 'Autopay for regular customers', 'Reminders sent for you']),
    'customers': dict(img='owner-laptop', pos='62% 26%', tag='For your customers',
                      h='Your customers get the easy version.',
                      card=('Northside Physio', 'Invoice INV-0238', '$121.00', 'Autopay on', 'amber', 'Pay $121.00'),
                      ticks=['No account or password needed', 'Save the card for next time', 'Switch autopay on or off']),
    'pricing': dict(img='light-ink', pos='center', tag='Pricing',
                    h='Simple monthly plans. Card fees stay as agreed with NAB.',
                    card=('Growth', 'Up to 1,000 invoices a month', '$99', 'Per month', 'blue', 'Sign up'),
                    ticks=['Starter from $49.95 a month', 'No application or approval wait', 'Set up in under five minutes']),
    'security': dict(img='card-circuit', pos='70% 55%', tag='Security',
                     h='Security and data protection.',
                     card=('Saved card', 'Visa ending 1111, held as a NAB token', 'Encrypted', 'Protected', 'green', None),
                     ticks=['Payments processed by NAB', 'Money settles to your account', 'Transiqe never holds your money']),
    'solutions-services': dict(img='owner-laptop', pos='62% 26%', tag='Service-based businesses',
                               h='Get paid for your time, without chasing it.',
                               card=('Monthly retainer', 'Olive &amp; Co Pty Ltd', '$1,320.00', 'Autopay 1 Dec', 'amber', None),
                               ticks=['Retainers and memberships', 'Appointments and projects', 'Paid on the due date']),
    'solutions-hospitality': dict(img='light-gold', pos='center', tag='Restaurants and cafes',
                                  h='Card payments for the sales that go out on an invoice.',
                                  card=('Function deposit', '40 guests, Saturday 13 Dec', '$1,500.00', 'Deposit', 'amber', 'Pay now'),
                                  ticks=['Catering orders', 'Functions and events', 'Corporate accounts']),
    'solutions-ecommerce': dict(img='light-teal', pos='center', tag='E-commerce',
                                h='For the orders that go out on an invoice.',
                                card=('Wholesale order 1042', '24 units, Bayside Gifts', '$2,184.00', 'Trade account', 'blue', 'Pay now'),
                                ticks=['Wholesale and trade', 'Custom and made-to-order', 'Standing orders on autopay']),
    'solutions-accountants': dict(img='owner-tablet', pos='40% 30%', flip=True, tag='Bookkeepers and accountants',
                                  h='Card payments that reconcile themselves in Xero.',
                                  card=('Payment recorded in Xero', 'INV-0238, Northside Physio', '$121.00', 'Reconciled', 'green', None),
                                  ticks=['Recorded against the right invoice', 'Bank reference attached', 'Less matching, cleaner books']),
    'faq': dict(img='light-warm', pos='center', tag='FAQ', h='Questions, answered.',
                card=('How long does setup take?', 'Getting started', 'Under 5 min', 'Answered', 'green', None),
                ticks=['Setup and NAB Gateway', 'Payments, fees and autopay', 'Xero, security and billing']),
    'help': dict(img='light-dusk', pos='center', tag='Help centre', h='Step-by-step guides to get you set up.',
                 card=('Getting started', '6 guides', 'Sign up', 'Step 1', 'blue', None),
                 ticks=['Connect Xero', 'Connect your NAB Gateway', 'Switch on Pay now']),
    'blog': dict(img='light-teal', pos='center', tag='Articles', h='Guides on getting paid on time.',
                 card=('Latest articles', 'For businesses that invoice from Xero', '3 guides', 'New', 'amber', None),
                 ticks=['Autopay and direct debit', 'Retainers without the chasing', 'What to ask NAB']),
    'article-autopay-vs-direct-debit': dict(img='light-ink', pos='center', tag='Article',
                                           h='Autopay and direct debit are not the same thing.',
                                           card=('Autopay', 'Recurring card payment', 'Opt in', 'Card', 'blue', None),
                                           ticks=['Customer chooses to opt in', 'Charged on the due date', 'Opt out at any time']),
    'article-retainers-autopay': dict(img='light-warm', pos='center', tag='Article',
                                      h='Retainers without the chasing.',
                                      card=('Monthly retainer', 'Repeating invoice in Xero', '$1,320.00', 'Autopay 1 Dec', 'amber', None),
                                      ticks=['1 September: paid automatically', '1 October: paid automatically', '1 November: paid automatically']),
    'article-nab-gateway-checklist': dict(img='light-dusk', pos='center', tag='Article',
                                          h='What to ask NAB about a NAB Gateway account.',
                                          card=('Your checklist', 'Before you connect', '9 questions', 'Getting started', 'blue', None),
                                          ticks=['Cards accepted and fees', 'Where and when it settles', 'Refunds and saved cards']),
}

LEGAL = dict(img='card-circuit', pos='70% 55%', card=None, ticks=[])
OG['terms'] = dict(LEGAL, tag='Legal', h='Terms of service.')
OG['privacy'] = dict(LEGAL, tag='Legal', h='Privacy policy.')
OG['autopay-terms'] = dict(LEGAL, tag='Legal', h='Autopay terms.')
