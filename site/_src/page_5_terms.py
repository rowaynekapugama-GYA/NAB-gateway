UPDATED = '25 November 2026'
ADDRESS = '119 Willoughby Road, Crows Nest NSW 2065'
DRAFT = '<div class="draftbar">Draft for legal review. Items highlighted like <span class="confirm">this</span> need to be confirmed before this page is published.</div>'

def legal_head(title, lede):
    return (plain_top() + f'<section class="band tight" style="padding-bottom:0"><div class="wrap"><span class="tag paper">Legal</span>'
            f'<h1 style="font-size:clamp(32px,4.4vw,54px);max-width:20ch">{title}</h1><p class="lede" style="margin-top:16px">{lede}</p>'
            f'<p class="meta-line">Last updated {UPDATED}</p></div></section>')

terms_sections = [
 ('about', '1. About these terms', f'''
<p>Transiqe is a software service operated by {ENTITY} (ABN {ABN}) of {ADDRESS} (<strong>Transiqe</strong>, <strong>we</strong>, <strong>us</strong>).</p>
<p>These terms are an agreement between us and the business that creates a Transiqe account (<strong>you</strong>). By creating an account or using the service you accept them. If you accept on behalf of a company or other organisation, you confirm that you are authorised to bind it.</p>
<p>These terms should be read with our <a href="privacy.html">privacy policy</a> and our <a href="autopay-terms.html">autopay terms</a>, which form part of this agreement. The people you send invoices to are referred to as your <strong>customers</strong>.</p>'''),
 ('service', '2. What Transiqe is, and what it is not', '''
<p>Transiqe connects your accounting software to your own NAB Gateway account so that your customers can pay your invoices by card. It also provides a customer portal, automatic payments your customers can opt in to, emails sent to your customers on your behalf, and records of payments.</p>
<div class="note"><strong>Transiqe is software only.</strong> We are not a bank, an authorised deposit-taking institution, a merchant acquirer, a payment facilitator or a provider of financial product advice. We do not hold, receive, transmit or control your money or your customers' money at any time.</div>
<p>Card payments are processed by National Australia Bank Limited (<strong>NAB</strong>) under the merchant agreement between you and NAB, and settle to the account nominated in that agreement. NAB's fees, settlement times, chargeback rules and other terms are a matter between you and NAB.</p>
<p>Transiqe is not affiliated with, endorsed by or acting on behalf of NAB or Xero Limited.</p>'''),
 ('eligibility', '3. Eligibility and your account', '''
<ul>
<li>You must be carrying on a business in Australia, hold an ABN, and hold (or be in the process of obtaining) a NAB Gateway account in your own name.</li>
<li>The information you give us must be accurate and kept up to date.</li>
<li>You are responsible for everything done through your account, for keeping your sign-in details confidential, and for controlling which of your staff have access.</li>
<li>You must tell us promptly if you suspect unauthorised access to your account.</li>
</ul>'''),
 ('connections', '4. Connecting Xero and NAB Gateway', '''
<p><strong>Your authority to us.</strong> When you connect Xero, you authorise us to read your contacts and invoices, to keep them synchronised, and to record payments against your invoices. When you connect your NAB Gateway account, you authorise us to submit payment, tokenisation and refund requests to it on your instruction and on the instruction of your customers acting under an authority they have given you.</p>
<p><strong>Your responsibilities.</strong> You are responsible for:</p>
<ul>
<li>your merchant agreement with NAB and your compliance with it, including card scheme rules;</li>
<li>all fees charged by NAB and by Xero;</li>
<li>the security of your NAB Gateway and Xero credentials;</li>
<li>the accuracy of the information held in Xero, which Transiqe relies on.</li>
</ul>
<p><strong>Third-party services.</strong> The service depends on systems operated by NAB, Xero and others. We do not control them and are not responsible for their availability, their decisions (including decisions to approve, decline, hold or reverse a payment) or changes they make. If a third party changes or withdraws something the service relies on, we may need to change or suspend the affected feature.</p>
<p>You can disconnect Xero or your NAB Gateway account at any time. Features that depend on a connection will stop working while it is disconnected.</p>'''),
 ('customers', '5. Your customers, invoices and payments', '''
<p>You are the supplier of the goods or services you invoice for and the merchant for every card payment. We are not a party to any transaction between you and your customers. You are responsible for:</p>
<ul>
<li>the content and accuracy of your invoices, and for only invoicing amounts your customers genuinely owe;</li>
<li>your goods and services, your own terms of trade, and compliance with the Australian Consumer Law;</li>
<li>refunds, disputes and chargebacks. A refund you issue through Transiqe is paid from your merchant facility;</li>
<li>complying with the law on card surcharges. You must not use the service to apply a surcharge that is not permitted;</li>
<li>having a lawful basis to give us your customers' details and to contact them, and telling them how their information is handled (see section 9).</li>
</ul>
<p><strong>Emails sent for you.</strong> Transiqe sends invoices, reminders, receipts and payment notices to your customers in your name. You instruct us to send them and you are the sender for the purposes of the Spam Act 2003 (Cth). You must only use the service to send messages that relate to your invoices and your relationship with that customer.</p>
<p><strong>Automatic payments.</strong> A customer's card may only be charged automatically if the customer has opted in through Transiqe and accepted the <a href="autopay-terms.html">autopay terms</a>. You must honour a customer's request to stop automatic payments, must only charge amounts that are due on an invoice issued to that customer, and must comply with the business obligations in the autopay terms.</p>'''),
 ('acceptable-use', '6. Acceptable use', '''
<p>You must not, and must not allow anyone else to:</p>
<ul>
<li>use the service for anything unlawful, fraudulent or misleading, or to take payment for goods or services that are illegal or that NAB or the card schemes prohibit;</li>
<li>process payments on behalf of another business, or through a NAB Gateway account that is not yours;</li>
<li>store, or try to obtain, full card numbers or card security codes other than through the fields provided by the service;</li>
<li>interfere with, probe or try to gain unauthorised access to the service, or copy, resell or reverse engineer it;</li>
<li>upload anything that contains malicious code or that infringes someone else's rights.</li>
</ul>'''),
 ('fees', '7. Fees and billing', '''
<p><strong>Plans.</strong> Our subscription fees and the number of invoices included in each plan are set out on our <a href="pricing.html">pricing page</a>, or in a written quote where we have agreed pricing with you. <span class="confirm">An invoice counts towards your plan when it is made available for payment through Transiqe in a calendar month.</span></p>
<p><strong>Billing.</strong> <span class="confirm">Subscription fees are charged monthly in advance to the payment method you nominate, starting when your free setup period ends.</span> <span class="confirm">Fees are stated in Australian dollars and are [inclusive / exclusive] of GST.</span> We will give you a tax invoice for each payment.</p>
<p><strong>Going over your plan.</strong> <span class="confirm">If you exceed your plan's invoice allowance, we will let you know and move you to the plan that fits your volume from your next billing date.</span></p>
<p><strong>Changes to fees.</strong> We may change our fees by giving you at least 30 days' written notice. If you do not accept a change you may cancel before it takes effect.</p>
<p><strong>Late or failed payment.</strong> If a subscription payment fails, we will tell you and try again. If it remains unpaid 14 days after we notify you, we may suspend your account until it is paid.</p>
<p><strong>Refunds.</strong> Except as required by law, including the Australian Consumer Law, subscription fees already paid are not refundable.</p>
<p><strong>NAB and Xero fees are separate.</strong> Our fees do not include anything charged by NAB or Xero.</p>'''),
 ('changes-service', '8. The service, support and changes', '''
<p>We will provide the service with due care and skill and will take reasonable steps to keep it available and secure. We do not promise that it will be uninterrupted or free of errors. We may carry out maintenance, and we will try to do so at times that cause the least disruption.</p>
<p>We may add, change or remove features. If a change will materially reduce the service you are paying for, we will give you at least 30 days' notice where we reasonably can, and you may cancel.</p>
<p>Support is available by email at <a href="mailto:hello@transiqe.com">hello@transiqe.com</a>.</p>'''),
 ('privacy', '9. Privacy and your customers\' information', '''
<p>We handle personal information in accordance with our <a href="privacy.html">privacy policy</a> and the Privacy Act 1988 (Cth).</p>
<p>You provide us with your customers' personal information so that we can provide the service to you. As between us, that information is yours. We will use it only to provide and secure the service, as you instruct, and as the law requires. We will not sell it or use it to market to your customers.</p>
<p>You must comply with the privacy laws that apply to you, including telling your customers that you use a service provider to issue invoices and take payments. You may refer them to our privacy policy for how we handle their information.</p>
<p>If either of us becomes aware of a data breach involving your customers' information held in the service, that party will tell the other without undue delay, and we will each cooperate in assessing it and meeting any notification obligations.</p>'''),
 ('ip', '10. Intellectual property', '''
<p>We own the service, including its software, design, trade marks and documentation. We grant you a non-exclusive, non-transferable right to use the service for your own business while your account is active.</p>
<p>You own your data. You grant us the rights we need to host, process and display it in order to provide the service. We may use information that does not identify you or your customers to maintain and improve the service.</p>
<p>If you give us feedback, we may use it without obligation to you.</p>'''),
 ('confidentiality', '11. Confidentiality', '''
<p>Each of us must keep the other's confidential information confidential, use it only for the purposes of this agreement, and protect it with reasonable care. This does not apply to information that is public, already known, independently developed, or required to be disclosed by law.</p>'''),
 ('consumer', '12. Your rights under the Australian Consumer Law', '''
<p>Nothing in these terms excludes, restricts or modifies any right or remedy you have under the Australian Consumer Law or any other law that cannot lawfully be excluded.</p>
<p>Where the Australian Consumer Law applies and permits us to limit our liability for a failure to comply with a consumer guarantee, our liability is limited, at our option, to supplying the service again or paying the cost of having it supplied again.</p>'''),
 ('liability', '13. Liability', '''
<p>This section applies subject to section 12.</p>
<p><strong>What we are not responsible for.</strong> To the extent permitted by law, we are not liable for loss or damage arising from:</p>
<ul>
<li>the acts, omissions, systems or decisions of NAB, Xero, a card scheme, a card issuer or any other third party, including outages, delays, declined or reversed payments, holds on settlement and chargebacks;</li>
<li>fees or charges payable under your merchant agreement or your Xero subscription;</li>
<li>any dispute between you and your customer, or the goods or services you supply;</li>
<li>inaccurate information in your accounting software, or instructions you or your staff give through your account;</li>
<li>unauthorised access to your account that results from your failure to keep your credentials secure;</li>
<li>events beyond our reasonable control.</li>
</ul>
<p><strong>Types of loss.</strong> To the extent permitted by law, neither of us is liable to the other for loss of profit, revenue, goodwill or opportunity, or for any indirect or consequential loss, arising out of this agreement.</p>
<p><strong>Cap.</strong> To the extent permitted by law, our total liability to you arising out of this agreement in any 12 month period is limited to the subscription fees you paid us in that period.</p>
<p><strong>What is not limited.</strong> Nothing in this section limits liability for fraud, wilful misconduct, or anything that cannot be limited by law.</p>
<p><strong>Shared responsibility.</strong> A party's liability is reduced to the extent that the other party caused or contributed to the loss, and each of us must take reasonable steps to mitigate our loss.</p>'''),
 ('indemnity', '14. Indemnity', '''
<p>You indemnify us against loss, damage, cost or expense (including reasonable legal costs) that we incur as a result of a claim by a third party, including your customer, NAB or a regulator, to the extent it arises from:</p>
<ul>
<li>your breach of these terms, the autopay terms or the law;</li>
<li>your invoices, goods or services, or a dispute with your customer;</li>
<li>a payment, refund or automatic payment made on your instruction.</li>
</ul>
<p>This indemnity is reduced to the extent that we caused or contributed to the loss.</p>'''),
 ('ending', '15. Suspension and ending this agreement', '''
<p><strong>You</strong> may cancel at any time from your account or by emailing us. Cancellation takes effect at the end of the billing period you have paid for.</p>
<p><strong>We</strong> may suspend or end your access:</p>
<ul>
<li>immediately, if we reasonably believe it is necessary to prevent fraud, unlawful activity or a security risk, if NAB or a regulator requires it, or if your NAB Gateway account is closed or suspended;</li>
<li>on 14 days' notice, if you breach these terms and do not fix the breach in that time, or if fees remain unpaid;</li>
<li>on 30 days' notice for any other reason, in which case we will refund any fees paid for the period after the end date.</li>
</ul>
<p>We will act reasonably in exercising these rights and will tell you why, unless the law prevents us.</p>
<p><strong>When this agreement ends:</strong> scheduled automatic payments stop; Pay now links stop working; your invoices in Xero and your merchant facility with NAB are not affected. You may export your data for <span class="confirm">30 days</span> after the end date. After that we will delete or de-identify it, except where we must keep it by law (see our privacy policy).</p>'''),
 ('changes-terms', '16. Changes to these terms', '''
<p>We may update these terms from time to time. If a change is likely to be detrimental to you, we will give you at least 30 days' notice by email or in your account, and you may cancel before it takes effect without penalty. Other changes take effect when the updated terms are published. The date at the top of this page shows when they were last changed.</p>'''),
 ('disputes', '17. Disputes and governing law', '''
<p>If you have a complaint, please contact us first at <a href="mailto:hello@transiqe.com">hello@transiqe.com</a>. We will acknowledge it within 5 business days and work with you in good faith to resolve it. If we cannot resolve it within 30 days, either of us may refer it to mediation before starting court proceedings, except where urgent relief is needed.</p>
<p>These terms are governed by the laws of New South Wales, Australia. Each of us submits to the non-exclusive jurisdiction of the courts of New South Wales.</p>'''),
 ('general', '18. General', '''
<ul>
<li><strong>Notices.</strong> We will send notices to the email address on your account. You can send notices to us at the address in section 19.</li>
<li><strong>Assignment.</strong> You may not transfer this agreement without our consent, which we will not unreasonably withhold. We may transfer it as part of a sale or restructure of our business, provided your rights are not reduced.</li>
<li><strong>Severance.</strong> If part of these terms is unenforceable, the rest continues to apply.</li>
<li><strong>Waiver.</strong> A right is only waived in writing.</li>
<li><strong>Whole agreement.</strong> These terms, the privacy policy, the autopay terms and any written quote are the whole agreement between us about the service.</li>
<li><strong>Relationship.</strong> We are an independent contractor. Nothing in these terms makes either of us the other's partner, agent or employee, except that we act on your instruction when we submit requests to your NAB Gateway account and send emails in your name.</li>
</ul>'''),
 ('contact', '19. Contact', f'''
<p>{ENTITY}, trading as Transiqe<br>ABN {ABN}<br>{ADDRESS}<br>Email: <a href="mailto:hello@transiqe.com">hello@transiqe.com</a></p>'''),
]

page('terms', 'Terms of service · Transiqe',
     'The terms that apply to businesses using Transiqe to take card payments on their invoices through their own NAB Gateway.',
     legal_head('Terms of service', 'The agreement between Transiqe and the businesses that use it. We have written it in plain language. Please read it before you create an account.')
     + docpage(terms_sections, DRAFT))
