privacy_sections = [
 ('about', '1. About this policy', f'''
<p>Transiqe is operated by {ENTITY} (ABN {ABN}) (<strong>Transiqe</strong>, <strong>we</strong>, <strong>us</strong>). This policy explains how we collect, use, store and share personal information, and how you can access it, correct it or make a complaint.</p>
<p>We handle personal information in accordance with the Privacy Act 1988 (Cth) and the Australian Privacy Principles.</p>'''),
 ('who', '2. Whose information we handle, and our role', '''
<p>We handle personal information about three groups of people:</p>
<ul>
<li><strong>Business users.</strong> People who create or use a Transiqe account for their business.</li>
<li><strong>Payers.</strong> People who receive an invoice from a business that uses Transiqe, pay it through Transiqe, or use that business's customer portal.</li>
<li><strong>Visitors.</strong> People who visit our website or contact us.</li>
</ul>
<div class="note"><strong>If you are a payer:</strong> the business that invoiced you decides what information about you is in its records and why. We handle it as that business's service provider, to issue its invoices and take its payments. Questions about an invoice, a payment or the information a business holds about you are best put to that business first. You can also contact us directly using the details in section 16.</div>'''),
 ('collect', '3. What we collect', '''
<table>
<thead><tr><th>About</th><th>What we collect</th></tr></thead>
<tbody>
<tr><td>Business users</td><td>Name, email address, phone number, business name, ABN and business address; sign-in details (passwords are stored only as salted hashes); the Xero organisation connected; NAB Gateway merchant identifiers and connection details; subscription and billing details; records of actions taken in the account.</td></tr>
<tr><td>Payers</td><td>Name, email address, phone number and postal address as held in the business's accounting records; invoices addressed to them, including line items, amounts and due dates; payment history; automatic payment settings and the record of consent to them; for saved cards, a token issued by NAB Gateway, the card brand, last four digits and expiry date; emails sent to them and whether they were delivered.</td></tr>
<tr><td>Visitors</td><td>Information you give us when you contact us; technical information such as IP address, browser type, pages visited and the time of the visit.</td></tr>
</tbody></table>
<p><strong>Card details.</strong> Full card numbers and card security codes are entered into fields provided by NAB Gateway. We do not store them.</p>
<p><strong>Invoice content.</strong> Invoice descriptions are written by the business. Depending on the business, they may reveal sensitive information, for example that someone has received a health service. We handle invoice content only to deliver and take payment for the invoice, and we do not use it for any other purpose.</p>
<p>We do not knowingly collect information from children, and the service is not directed at people under 18.</p>'''),
 ('how', '4. How we collect it', '''
<ul>
<li><strong>From you,</strong> when you create an account, pay an invoice, use the portal, save a card, change your settings or contact us.</li>
<li><strong>From the business that invoices you.</strong> When a business connects its accounting software, its customer and invoice records are imported into Transiqe and kept in sync. If you are a payer, this is usually how we first receive your details.</li>
<li><strong>From Xero and NAB Gateway,</strong> which send us invoice information, payment outcomes and card tokens.</li>
<li><strong>Automatically,</strong> through server logs and cookies when you use our website or the service.</li>
</ul>'''),
 ('why', '5. Why we collect, hold and use it', '''
<p>We use personal information to:</p>
<ul>
<li>provide the service, including importing customers and invoices, sending invoices and reminders, presenting invoices for payment, submitting payment and refund requests to the business's NAB Gateway account, running automatic payments a payer has authorised, and recording payments in the business's accounting software;</li>
<li>provide customer portals and verify the identity of people signing in;</li>
<li>send service messages such as receipts, payment notices and security alerts;</li>
<li>manage business accounts, billing and support;</li>
<li>keep the service secure, detect and prevent fraud and misuse, and keep audit records;</li>
<li>maintain and improve the service, using information that does not identify individuals wherever we can;</li>
<li>comply with our legal obligations.</li>
</ul>
<p>We do not sell personal information. We do not use payers' information to market to them.</p>'''),
 ('automated', '6. Automated processing and decisions', '''
<p>From 10 December 2026 the Privacy Act requires organisations to explain where computer programs are used to make, or substantially assist in making, decisions that could significantly affect a person's rights or interests. We want to be clear about what is automated in Transiqe.</p>
<table>
<thead><tr><th>What the software does automatically</th><th>Personal information used</th></tr></thead>
<tbody>
<tr><td><strong>Charging a saved card for an invoice.</strong> Where a payer has opted in to automatic payments, the software submits a charge for the amount due on the date the payer chose.</td><td>Payer identity, the invoice amount and due date, the payer's automatic payment settings, the card token.</td></tr>
<tr><td><strong>Retrying or stopping an automatic payment.</strong> If a charge is declined, the software notifies the payer, tries again on a set schedule and stops after a set number of attempts.</td><td>The payment outcome returned by NAB Gateway, the number of attempts, the payer's contact details.</td></tr>
<tr><td><strong>Cancelling a scheduled payment.</strong> If an invoice is voided or paid another way, the scheduled charge is cancelled.</td><td>Invoice status from the business's accounting software.</td></tr>
<tr><td><strong>Sending invoices, reminders and receipts.</strong> These are triggered by invoice dates and payment events.</td><td>Payer contact details, invoice and payment details.</td></tr>
<tr><td><strong>Matching a payment to an invoice</strong> and recording it in the business's accounting software.</td><td>Invoice and payment references.</td></tr>
</tbody></table>
<p>These steps carry out instructions that the payer or the business has already given. A payer can stop automatic payments at any time, and a person at the business can review, refund or override any of them.</p>
<p><strong>Decisions made by others.</strong> Whether a card payment is approved or declined is decided by NAB, the card scheme and the card issuer, which may use their own automated fraud and risk checks. We do not make that decision.</p>
<p><strong>What we do not do.</strong> We do not use automated tools to assess creditworthiness, set prices, decide who may be a customer of a business, or build profiles of individuals.</p>'''),
 ('disclose', '7. Who we share it with', '''
<ul>
<li><strong>The business concerned.</strong> A business can see the information about its own customers, invoices and payments. If you are a payer, the business that invoiced you sees your payments and automatic payment settings.</li>
<li><strong>National Australia Bank,</strong> through NAB Gateway, to process card payments, refunds and card tokens for the business.</li>
<li><strong>Xero,</strong> where the business has connected it, to read invoices and record payments.</li>
<li><strong>Our service providers,</strong> who help us run the service: <span class="confirm">cloud hosting [provider], email delivery [provider], error monitoring and analytics [providers]</span>. They may only use the information to provide services to us.</li>
<li><strong>Professional advisers, insurers and auditors,</strong> under obligations of confidence.</li>
<li><strong>Regulators, courts and law enforcement,</strong> where we are required or authorised by law.</li>
<li><strong>A buyer or successor,</strong> if our business or the service is sold or restructured, on the basis that this policy continues to apply.</li>
</ul>'''),
 ('overseas', '8. Sending information overseas', '''
<p><span class="confirm">Our application and database are hosted in [Australia / country]. Some of our service providers store or process information outside Australia, in [list countries, for example the United States].</span></p>
<p>Before we disclose personal information to an overseas recipient, we take reasonable steps to make sure it will handle the information consistently with the Australian Privacy Principles, including through our contracts with it.</p>'''),
 ('security', '9. How we protect it', '''
<p>We take reasonable steps to protect personal information from misuse, interference, loss and unauthorised access. These include encryption in transit, encryption of credentials and tokens at rest, access controls, audit logging and keeping card data within NAB's payment environment. More detail is on our <a href="security.html">security page</a>.</p>
<p>No system is completely secure. If you think your account or information has been compromised, tell us straight away.</p>'''),
 ('retention', '10. How long we keep it', '''
<p>We keep personal information for as long as the business's account is active and for as long afterwards as we need it for the purposes in this policy or as the law requires.</p>
<ul>
<li>Payment and invoice records are kept for <span class="confirm">7 years</span>, in line with financial record-keeping obligations.</li>
<li>When a business closes its account, its data can be exported for <span class="confirm">30 days</span> and is then deleted or de-identified, apart from records we must keep by law.</li>
<li>A saved card token is deleted when the payer removes the card or the business's account is closed.</li>
</ul>
<p>When we no longer need personal information we destroy it or de-identify it.</p>'''),
 ('access', '11. Accessing and correcting your information', '''
<p>You can ask us for a copy of the personal information we hold about you and ask us to correct it if it is inaccurate, out of date or incomplete.</p>
<ul>
<li><strong>Business users</strong> can see and update most of their information in their account.</li>
<li><strong>Payers</strong> can see their invoices, payments, saved cards and automatic payment settings in the customer portal. Because your details come from the business's own records, the quickest way to correct them is usually to ask that business. You can also ask us and we will work with the business to respond.</li>
</ul>
<p>We will respond within 30 days. We do not charge for making a request. If we cannot give you access or make a correction, we will tell you why in writing.</p>'''),
 ('marketing', '12. Marketing', '''
<p>We may send business users information about Transiqe. Every marketing message includes a way to unsubscribe, and you can opt out at any time by emailing us. We do not send marketing to payers. Emails that payers receive through Transiqe are invoices, reminders, receipts and notices sent on behalf of the business that invoiced them.</p>'''),
 ('cookies', '13. Cookies', '''
<p>We use cookies that are necessary to keep you signed in and to keep the service secure. <span class="confirm">We also use [analytics tool] to understand how our website is used.</span> You can block cookies in your browser, but parts of the service that require you to be signed in will not work without them.</p>'''),
 ('breach', '14. Data breaches', '''
<p>If personal information we hold is involved in a data breach that is likely to result in serious harm, we will notify the affected individuals and the Office of the Australian Information Commissioner, as required by the Notifiable Data Breaches scheme. Where the information belongs to a business's customers, we will also tell that business without undue delay.</p>'''),
 ('complaints', '15. Complaints', '''
<p>If you think we have mishandled your personal information, please contact us using the details below. We will acknowledge your complaint within 5 business days and aim to resolve it within 30 days.</p>
<p>If you are not satisfied with our response, you can complain to the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au">oaic.gov.au</a> or on 1300 363 992.</p>'''),
 ('contact', '16. Contact us', f'''
<p>Privacy Officer<br>{ENTITY}, trading as Transiqe<br>{ADDRESS}<br>Email: <a href="mailto:privacy@transiqe.com"><span class="confirm">privacy@transiqe.com</span></a></p>'''),
 ('changes', '17. Changes to this policy', '''
<p>We may update this policy from time to time. The date at the top of the page shows when it was last changed. If we make a significant change, we will tell business users by email or in their account before it takes effect.</p>'''),
]

page('privacy', 'Privacy policy · Transiqe',
     'How Transiqe collects, uses, stores and shares personal information about businesses and the customers who pay their invoices, including what is automated.',
     legal_head('Privacy policy', 'What we collect, why we collect it, who we share it with, and the choices you have. This applies to businesses that use Transiqe and to the customers who pay their invoices.')
     + docpage(privacy_sections, DRAFT))
