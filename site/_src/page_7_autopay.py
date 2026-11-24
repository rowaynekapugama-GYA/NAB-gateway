autopay_sections = [
 ('summary', 'The short version', '''
<div class="note key"><strong>If you opt in to autopay,</strong> you are authorising the business that invoices you to charge your saved card for each invoice it issues to you, on the timing you choose, until you turn autopay off. You can turn it off at any time in your customer portal. You will be sent every invoice and a receipt for every payment. This is a card payment authority, not a direct debit from a bank account.</div>'''),
 ('parties', '1. Who is involved', f'''
<ul>
<li><strong>You</strong> are the person or organisation paying invoices.</li>
<li><strong>The Business</strong> is the business that issues invoices to you and whose name appears on them. The Business is the merchant. It is the one that charges your card and receives your payment.</li>
<li><strong>Transiqe</strong> is the software the Business uses to send invoices and take payments. It is operated by {ENTITY} (ABN {ABN}). Transiqe does not charge your card for itself, does not receive your money, and is not a party to what you buy from the Business.</li>
<li><strong>NAB</strong> (National Australia Bank) processes the card payment for the Business and stores your card securely.</li>
</ul>
<p>These terms apply between you and the Business. Sections 10 and 11 also set out what Transiqe and the Business each commit to.</p>'''),
 ('authority', '2. What you are authorising', '''
<p>By opting in to automatic payments (<strong>autopay</strong>) you:</p>
<ul>
<li>ask for your card to be saved for future payments to the Business. NAB stores the card and gives the Business a secure token that stands in for it. Neither the Business nor Transiqe stores your full card number or security code;</li>
<li>authorise the Business to charge that card for the amount due on each invoice it issues to you, without asking you again each time;</li>
<li>confirm that you are the cardholder or are authorised to use the card.</li>
</ul>
<p>The amounts and dates are not fixed in advance. They depend on the invoices the Business issues to you. This authority continues until you cancel it (section 6) or it ends (section 9).</p>'''),
 ('when', '3. When your card is charged', '''
<p>You choose when each invoice is charged. The options offered may include when the invoice is issued, on its due date, or a set number of days before the due date. You can change your choice at any time in your portal, and the change applies to invoices that have not yet been charged.</p>
<p>If a scheduled date falls on a day when a payment cannot be processed, the charge may be made on the next available day.</p>
<p>The amount charged is the amount due on the invoice at the time of the charge. If the Business applies a fee that the law permits, it will be shown on the invoice or before you pay.</p>'''),
 ('notice', '4. What you will be told', '''
<ul>
<li><strong>Every invoice</strong> is sent to your email address, showing the amount and the due date.</li>
<li><strong>A receipt</strong> is sent after each successful payment, showing the amount, the date and the invoice it paid.</li>
<li><strong>A notice</strong> is sent if a payment fails, with a link to pay another way.</li>
</ul>
<p>Your portal always shows what is scheduled, what has been paid, and which card will be used. Please keep your email address up to date with the Business so these messages reach you.</p>'''),
 ('failed', '5. If a payment fails', '''
<p>If your card is declined, expired or has insufficient funds, you will be notified and the payment <span class="confirm">will be attempted again up to two more times over the following days</span>. If it still cannot be collected, automatic attempts for that invoice stop and both you and the Business are told.</p>
<p>The invoice remains payable. You can pay it at any time using the Pay now button or from your portal. Your card issuer may charge you a fee for a declined payment, and the Business's own terms may deal with late payment. Those are matters between you and them.</p>'''),
 ('cancel', '6. Changing or cancelling autopay', '''
<p>You can, at any time and without giving a reason:</p>
<ul>
<li><strong>turn autopay off</strong> in your customer portal, under Autopay and cards;</li>
<li><strong>change or remove your saved card</strong> in your portal. Removing the card you use for autopay turns autopay off;</li>
<li><strong>ask the Business</strong> to turn autopay off for you.</li>
</ul>
<p>Cancelling takes effect immediately for any charge that has not already been submitted to the bank. There is no fee for cancelling.</p>
<p>Turning autopay off does not cancel any invoice or change what you owe the Business. Invoices that are due remain payable, and you can pay them individually.</p>
<p>You can also ask your card issuer to stop payments to a merchant. We recommend turning autopay off in the portal as well, so that no further attempts are made.</p>'''),
 ('disputes', '7. Refunds and disputes', '''
<p>If you think you have been charged the wrong amount, charged for an invoice you do not recognise, or charged after you cancelled, contact the Business first, using the contact details on your invoice. The Business can refund a payment, and the refund is returned to the card that was charged.</p>
<p>If you cannot resolve it with the Business, you may be able to dispute the transaction with your card issuer. Nothing in these terms affects your rights with your card issuer or your rights under the Australian Consumer Law.</p>
<p>If you believe a card was saved or charged without your authority, tell the Business and your card issuer straight away. You can also email Transiqe at <a href="mailto:hello@transiqe.com">hello@transiqe.com</a> and we will help identify the Business and the payment.</p>'''),
 ('your-part', '8. What you agree to do', '''
<ul>
<li>Only save a card you are authorised to use.</li>
<li>Keep enough available funds or credit on the card to cover invoices as they fall due.</li>
<li>Update your saved card if it expires, is replaced or is cancelled.</li>
<li>Check the invoices and receipts you are sent, and raise any concern promptly.</li>
</ul>'''),
 ('ending', '9. When this authority ends', '''
<p>Your autopay authority ends when you cancel it, when you remove the saved card, when the Business turns it off or stops using Transiqe, or when automatic attempts for an invoice have failed and stopped as described in section 5. If the Business stops using Transiqe, no further automatic payments are made through Transiqe and your saved card token is deleted.</p>'''),
 ('privacy', '10. Your information and your card', '''
<p>Your card details are entered into fields provided by NAB Gateway and are stored by NAB. Transiqe keeps the token NAB issues, the card brand, the last four digits and the expiry date, so that you can recognise your card. A token can only be used for payments to the Business it was created for.</p>
<p>Transiqe keeps a record of when you opted in, the terms that applied, and each payment made. Your personal information is handled in accordance with the <a href="privacy.html">privacy policy</a>, which also explains what the software does automatically.</p>'''),
 ('business', '11. What the Business commits to', '''
<p>Each business that offers autopay through Transiqe agrees with Transiqe that it will:</p>
<ul>
<li>only enrol a customer in autopay through the Transiqe opt-in, with these terms shown before the customer agrees;</li>
<li>only charge amounts that are due on an invoice issued to that customer;</li>
<li>act on a customer's request to stop autopay promptly, and never switch it back on without the customer opting in again;</li>
<li>deal with refund requests and disputes fairly and in line with the Australian Consumer Law and its merchant agreement;</li>
<li>keep its customers' contact details accurate so that invoices, receipts and notices reach them;</li>
<li>not describe autopay as a bank direct debit, and not use it to take payment for anything other than its own invoices.</li>
</ul>'''),
 ('changes', '12. Changes to these terms', '''
<p>These terms may be updated. If a change affects an authority you have already given, you will be told by email at least <span class="confirm">14 days</span> before it takes effect, and you can turn autopay off if you do not agree. The date at the top of this page shows when the terms were last changed.</p>'''),
 ('contact', '13. Contact', f'''
<p><strong>About an invoice, a payment or a refund:</strong> contact the Business, using the details on your invoice.</p>
<p><strong>About Transiqe or these terms:</strong> {ENTITY}, trading as Transiqe, {ADDRESS}. Email <a href="mailto:hello@transiqe.com">hello@transiqe.com</a>.</p>'''),
]

page('autopay-terms', 'Autopay terms · Transiqe',
     'The terms that apply when a customer saves a card and opts in to automatic payment of invoices from a business that uses Transiqe, including how to cancel.',
     legal_head('Autopay terms', 'The terms that apply when you save a card and choose to have a business\'s invoices paid automatically. They explain what you are authorising, what you will be told, and how to stop.')
     + docpage(autopay_sections, DRAFT))
