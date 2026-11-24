def docpage(sections, intro=''):
    toc = ''.join(f'<a href="#{i}">{t}</a>' for i, t, _ in sections)
    body = ''.join(f'<h2 id="{i}">{t}</h2>{h}' for i, t, h in sections)
    return f'<section class="band"><div class="wrap doc"><nav class="toc" aria-label="On this page"><b>On this page</b>{toc}</nav><article class="prose">{intro}{body}</article></div></section>'

sec_hero = '''<div class="hero-grid"><div class="copy">
  <span class="tag">Security</span>
  <h1>Security and data protection</h1>
  <p class="lede">Transiqe is designed so that card data is handled by NAB, funds are never held by Transiqe, and access to your Xero and NAB Gateway accounts is limited to what the service requires. This page sets out the controls in place.</p>
</div></div>'''

sec_intro = '''<div class="note key"><strong>In summary.</strong> Card details are entered into fields provided by NAB Gateway and are not stored by Transiqe. Payments settle from your customer's card to your NAB account under your own merchant agreement. Credentials and connection tokens are encrypted. You can revoke Transiqe's access to Xero and to your NAB Gateway at any time.</div>'''

sec_sections = [
 ('architecture', 'Payment architecture', '''
<p>Transiqe is a software service. It is not a bank, a merchant acquirer or a payment facilitator, and it does not take part in the settlement of funds.</p>
<p>Card payments are processed by National Australia Bank through the NAB Gateway account held by the business issuing the invoice. Transiqe sends payment requests to that account on the business's instruction and records the result. Each business's payments are processed only through its own NAB Gateway account.</p>'''),
 ('card-data', 'Cardholder data', '''
<p>Card details are entered into payment fields provided by NAB Gateway. Transiqe does not store full card numbers or card security codes.</p>
<p>Where a customer chooses to save a card, NAB Gateway issues a token that represents the card. Transiqe stores that token together with the card brand, the last four digits and the expiry date, so the card can be identified to its holder. A token can only be used through the NAB Gateway account of the business it was created for. It cannot be used to make a payment anywhere else.</p>
<p>This design is intended to keep cardholder data within NAB's payment environment and to minimise the card data handled by Transiqe and by the businesses that use it.</p>'''),
 ('funds', 'Funds', '''
<p>Transiqe never holds, receives or controls customer funds. Payments settle from the customer's card to the business's account in accordance with the business's merchant agreement with NAB. Transiqe cannot redirect settlement, and it has no access to the business's bank account.</p>'''),
 ('connections', 'Connections to Xero and NAB Gateway', '''
<p><strong>Xero.</strong> Businesses connect Xero using Xero's own authorisation flow. Transiqe does not see or store Xero passwords. Access is limited to what the service needs: reading contacts and invoices, and recording payments against invoices. Access can be revoked at any time from within Xero or from Transiqe.</p>
<p><strong>NAB Gateway.</strong> Connection details for a business's NAB Gateway account are encrypted before they are stored and are never displayed in full after they have been entered. They are used only to communicate with NAB Gateway on that business's behalf, and can be replaced or removed by the business at any time.</p>'''),
 ('encryption', 'Encryption', '''
<p>Data sent between browsers, Transiqe, Xero and NAB Gateway is encrypted in transit using TLS. Credentials, connection tokens and card tokens are encrypted at rest.</p>'''),
 ('access', 'Authentication and access', '''
<p><strong>Business accounts.</strong> Passwords are stored as salted hashes and never in readable form. Sessions expire, and a business can only ever see its own customers, invoices and payments.</p>
<p><strong>Customer portal.</strong> Customers sign in using a single-use link sent to the email address on their invoice. Links expire. There are no customer passwords to be guessed, reused or leaked.</p>'''),
 ('integrity', 'Payment integrity', '''
<ul>
<li>The amount charged is always taken from the invoice record, never from a link or a form field, so an altered link cannot change what is paid.</li>
<li>Responses from NAB Gateway are verified before a payment is recorded.</li>
<li>Payment events are processed once, so a repeated notification cannot record the same payment twice.</li>
<li>Refunds are sent through NAB Gateway to the card that made the original payment.</li>
</ul>'''),
 ('autopay', 'Automatic payments', '''
<p>A card is only charged automatically where its holder has opted in and accepted the <a href="autopay-terms.html">autopay terms</a>. Customers can withdraw that authority at any time from their portal. Customers are sent each invoice and a receipt for each payment. If an invoice is voided or paid by other means, any scheduled automatic payment for it is cancelled.</p>'''),
 ('audit', 'Logging and audit', '''
<p>Transiqe keeps a record for each business of connection changes, payments, refunds and changes to automatic payment settings, and of the emails sent to its customers. These records are available to the business in its account.</p>'''),
 ('privacy', 'Privacy', '''
<p>Personal information is handled in accordance with the Privacy Act 1988 (Cth) and the Australian Privacy Principles. Transiqe does not sell personal information. The <a href="privacy.html">privacy policy</a> sets out what is collected, why, and who it is shared with.</p>'''),
 ('incidents', 'Incident response', '''
<p>Suspected security incidents are investigated promptly. If an incident affects a business's data, Transiqe will tell that business without undue delay and provide the information it needs to respond. Where an incident is an eligible data breach under the Notifiable Data Breaches scheme, Transiqe will notify affected individuals and the Office of the Australian Information Commissioner as the law requires.</p>'''),
 ('your-part', 'Your responsibilities', '''
<p>Security is shared. Businesses using Transiqe are responsible for:</p>
<ul>
<li>keeping their Transiqe sign-in details confidential and using a strong, unique password;</li>
<li>controlling who in their business has access to Transiqe, Xero and NAB Gateway;</li>
<li>keeping their NAB Gateway credentials secure and replacing them if they may have been exposed;</li>
<li>telling Transiqe promptly about any suspected unauthorised access.</li>
</ul>'''),
 ('report', 'Reporting a vulnerability', '''
<p>If you believe you have found a security vulnerability in Transiqe, please email <a href="mailto:security@transiqe.com">security@transiqe.com</a> with enough detail for us to reproduce it. We ask that you act in good faith, do not access or alter data that is not yours, and give us reasonable time to respond before any public disclosure. We will acknowledge your report and keep you informed.</p>'''),
]

security = hero('on-image', 'security', sec_hero, img='card-circuit', cls='cool subhero', pos='70% 55%') + docpage(sec_sections, sec_intro)
page('security', 'Security and data protection · Transiqe',
     'How Transiqe protects payments and data: card details handled by NAB Gateway, funds never held by Transiqe, encrypted credentials, limited access to Xero, and clear incident response.',
     security)
