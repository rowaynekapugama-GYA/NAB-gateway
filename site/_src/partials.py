# Shared pieces: icons and the illustrative product screens.
# All business names, people and figures in the screens are sample data.

def ic(path):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'

ICON = {
    'card': ic('<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M2.5 10h19"/>'),
    'repeat': ic('<path d="M17 2l4 4-4 4"/><path d="M3 11V9a3 3 0 013-3h15"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a3 3 0 01-3 3H3"/>'),
    'clock': ic('<circle cx="12" cy="12" r="9"/><path d="M12 7.5V12l3 2"/>'),
    'user': ic('<circle cx="12" cy="8" r="4"/><path d="M4 20c0-3.6 3.6-6 8-6s8 2.4 8 6"/>'),
    'mail': ic('<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M3 7.5l9 6 9-6"/>'),
    'check': ic('<path d="M4.5 12.5l5 5 10-11"/>'),
    'users': ic('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.2 3-5.2 6.5-5.2s6.5 2 6.5 5.2"/><path d="M16 4.8a3.5 3.5 0 010 6.4"/><path d="M18 15c2.1.6 3.5 2.2 3.5 5"/>'),
    'doc': ic('<path d="M6 2.5h8l4.5 4.5V21.5H6z"/><path d="M14 2.5V7h4.5"/><path d="M9 12.5h6M9 16.5h4"/>'),
    'shield': ic('<path d="M12 2.5l8 3.5v5.5c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'),
    'bank': ic('<path d="M3 9.5l9-6 9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 20.5h18"/>'),
    'link': ic('<path d="M10 14a4.5 4.5 0 006.4 0l3-3a4.5 4.5 0 00-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 00-6.4 0l-3 3A4.5 4.5 0 0011 19.4l1-1"/>'),
    'bell': ic('<path d="M6 16.5V11a6 6 0 0112 0v5.5l1.5 2h-15z"/><path d="M10 21h4"/>'),
}

BAR = '<div class="bar"><i></i><i></i><i></i><div class="url">{}</div></div>'

SCREEN_DASH = f'''<div class="screen">
{BAR.format('app.transiqe.com')}
<div class="body">
  <div class="side"><div class="l"><img src="assets/mark.svg" alt="">transiqe</div>
    <a class="on">Overview</a><a>Invoices</a><a>Customers</a><a>Payments</a><a>Autopay</a><a>Emails</a><a>Settings</a></div>
  <div class="main">
    <h5>Northside Physio</h5>
    <div class="stats">
      <div class="stat"><b class="num">$18,420</b><span>Collected by card this month</span></div>
      <div class="stat"><b class="num">$6,115</b><span>Outstanding across 9 invoices</span></div>
      <div class="stat"><b class="num">$1,386</b><span>Overdue across 2 invoices</span></div>
      <div class="stat"><b class="num">38 of 51</b><span>Customers on autopay</span></div>
    </div>
    <div class="scrollx"><table class="tbl">
      <thead><tr><th>When</th><th>Customer</th><th>Invoice</th><th class="r">Amount</th><th>Payment</th><th>Xero</th></tr></thead>
      <tbody>
        <tr><td>Today, 9:02 am</td><td>Marcus Bell</td><td>INV-0231</td><td class="r num">$594.00</td><td><span class="pill green">Autopay</span></td><td><span class="pill green">Marked paid</span></td></tr>
        <tr><td>Today, 8:40 am</td><td>Olive &amp; Co Pty Ltd</td><td>INV-0229</td><td class="r num">$1,320.00</td><td><span class="pill green">Paid by card</span></td><td><span class="pill green">Marked paid</span></td></tr>
        <tr><td>Yesterday</td><td>Priya Sharma</td><td>INV-0226</td><td class="r num">$121.00</td><td><span class="pill green">Paid by card</span></td><td><span class="pill green">Marked paid</span></td></tr>
        <tr><td>Yesterday</td><td>Dan Harker</td><td>INV-0224</td><td class="r num">$66.00</td><td><span class="pill amber">Card declined, retrying</span></td><td><span class="pill grey">Awaiting payment</span></td></tr>
      </tbody>
    </table></div>
  </div>
</div></div>'''

# The invoice your customer receives, with the Pay now button.
SCREEN_INVOICE = f'''<div class="screen phone">
{BAR.format('Invoice from Northside Physio')}
<div class="inv">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px"><div><div class="biz">Northside Physio</div><div class="tiny muted" style="margin-top:3px">Invoice INV-0238</div></div><span class="pill blue">Due 25 Oct</span></div>
  <table>
    <tr><td>Follow-up consultation</td><td class="num">$95.00</td></tr>
    <tr><td>Exercise band</td><td class="num">$15.00</td></tr>
    <tr><td class="muted">GST</td><td class="num muted">$11.00</td></tr>
    <tr class="t"><td>Amount due</td><td class="num">$121.00</td></tr>
  </table>
  <div class="btn cobalt block" style="margin-top:16px">Pay now</div>
  <p class="tiny muted" style="text-align:center;margin-top:10px">Pay securely by card. No surcharge.</p>
</div></div>'''

# The pay page: card fields come from NAB Gateway.
SCREEN_PAY = f'''<div class="screen phone">
{BAR.format('app.transiqe.com')}
<div class="inv">
  <div class="biz">Northside Physio</div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:10px"><span class="muted small">Invoice INV-0238</span><b class="num" style="font:500 26px var(--display);letter-spacing:-.04em">$121.00</b></div>
  <div style="display:grid;gap:8px;margin-top:14px">
    <div class="field"><span>Card number</span><b class="num">4111 •••• •••• 1111</b></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div class="field"><span>Expiry</span><b class="num">12 / 29</b></div><div class="field"><span>CVC</span><b>•••</b></div></div>
  </div>
  <p class="tiny muted" style="margin-top:8px">Card fields are provided by NAB Gateway.</p>
  <label style="display:flex;gap:9px;align-items:flex-start;font-size:12.5px;color:var(--ink-2);margin:12px 0 14px"><span style="flex:none;width:16px;height:16px;border-radius:5px;background:var(--cobalt);margin-top:2px"></span><span>Save this card and pay future invoices from Northside Physio automatically.</span></label>
  <div class="btn cobalt block">Pay $121.00</div>
</div></div>'''

SCREEN_PORTAL = f'''<div class="screen">
{BAR.format('app.transiqe.com/portal')}
<div class="ptop"><span>Northside Physio</span><nav><i class="on">Invoices</i><i>Payments</i><i>Autopay and cards</i><i>Account</i></nav></div>
<div class="main" style="padding:18px 20px">
  <h5>Hi Priya</h5>
  <div class="stats" style="grid-template-columns:repeat(3,minmax(0,1fr))">
    <div class="stat"><b class="num">$132.00</b><span>Outstanding, 1 invoice</span></div>
    <div class="stat"><b>On</b><span>Autopay, Visa ending 1111</span></div>
    <div class="stat"><b>Due date</b><span>When your card is charged</span></div>
  </div>
  <div class="scrollx"><table class="tbl">
    <thead><tr><th>Invoice</th><th>Issued</th><th>Due</th><th class="r">Amount due</th><th></th></tr></thead>
    <tbody>
      <tr><td>INV-0241<br><span class="muted">Follow-up consultation</span></td><td>1 Nov</td><td>8 Nov</td><td class="r num">$132.00</td><td><span class="pill amber">Autopay on 8 Nov</span></td></tr>
      <tr><td>INV-0238<br><span class="muted">Follow-up consultation</span></td><td>18 Oct</td><td>25 Oct</td><td class="r num">$0.00</td><td><span class="pill green">Paid</span></td></tr>
      <tr><td>INV-0226<br><span class="muted">Standard consultation</span></td><td>4 Oct</td><td>11 Oct</td><td class="r num">$0.00</td><td><span class="pill green">Paid</span></td></tr>
    </tbody>
  </table></div>
</div></div>'''

SCREEN_EMAIL = '''<div class="mail">
<div class="meta">From Northside Physio &nbsp;·&nbsp; To Priya Sharma</div>
<div class="hd">Northside Physio</div>
<div class="bd">Hi Priya,<br><br>Your invoice <b style="color:var(--ink)">INV-0238</b> for <b style="color:var(--ink)">$121.00</b> is due on 25 October.<br>
<span class="btn cobalt sm" style="margin:14px 0">Pay now</span><br>
<span class="tiny muted">You can also see all your invoices and switch on automatic payments in your customer portal.</span></div></div>'''

SCREEN_AUTOPAY = '''<div class="screen phone">
<div class="inv">
  <h5 style="margin-bottom:14px">Automatic payments</h5>
  <div style="display:grid;gap:8px">
    <div class="field"><span>Autopay</span><b style="color:var(--mint)">On</b></div>
    <div class="field"><span>Charge my card</span><b>On the due date</b></div>
    <div class="field"><span>Card</span><b class="num">Visa ending 1111</b></div>
    <div class="field"><span>Next payment</span><b class="num">INV-0241, 8 Nov, $132.00</b></div>
  </div>
  <div class="btn line block sm" style="margin-top:14px">Turn autopay off</div>
  <p class="tiny muted" style="text-align:center;margin-top:10px">You can change or cancel this at any time.</p>
</div></div>'''

SCREEN_CONNECT = '''<div class="screen phone">
<div class="inv">
  <h5 style="margin-bottom:14px">Get set up</h5>
  <div style="display:grid;gap:8px">
    <div class="field"><span>Xero</span><b style="color:var(--mint)">Connected</b></div>
    <div class="field"><span>Customers imported</span><b class="num">51</b></div>
    <div class="field"><span>Open invoices imported</span><b class="num">9</b></div>
    <div class="field"><span>NAB Gateway</span><b style="color:var(--mint)">Connected</b></div>
    <div class="field"><span>Pay now on invoices</span><b style="color:var(--mint)">On</b></div>
  </div>
  <p class="tiny muted" style="margin-top:12px">You are ready to take card payments.</p>
</div></div>'''

SAMPLE_NOTE = '<p class="tiny muted" style="margin-top:14px">Screens are illustrative and show sample data.</p>'

CLOSER = f'''<section class="band tight"><div class="wrap"><div class="closer has-img"><img class="bg" src="assets/img/light-warm.jpg" alt="" loading="lazy">
  <h2>Connect Xero and your NAB Gateway. Take your first card payment this week.</h2>
  <p>No application and no approval wait. Connect Xero and your NAB Gateway, and your invoices keep going out of Xero exactly as they do today.</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn ink lg" href="{APP}/signup">Sign up <span class="arr">&rarr;</span></a><a class="btn white lg" href="mailto:hello@transiqe.com">Talk to us</a></div>
</div></div></section>'''

PLANS = f'''<div class="plans">
  <div class="plan"><h3>Starter</h3><div><span class="price num">$49.95</span> <span class="per">per month</span></div>
    <p class="for">Up to 100 invoices a month.</p>
    <ul><li>Pay now on your Xero invoices</li><li>Autopay and repeating invoices</li><li>Customer portal</li><li>Reminders and receipts</li><li>Payments recorded in Xero</li></ul>
    <a class="btn ink" href="{APP}/signup">Sign up</a></div>
  <div class="plan hot"><h3>Growth</h3><div><span class="price num">$99</span> <span class="per">per month</span></div>
    <p class="for">Up to 1,000 invoices a month.</p>
    <ul><li>Everything in Starter</li><li>Ten times the invoice allowance</li><li>One flat price, however many of the 1,000 you use</li></ul>
    <a class="btn white" href="{APP}/signup">Sign up</a></div>
  <div class="plan"><h3>More than 1,000</h3><div><span class="price">Talk to us</span></div>
    <p class="for">For businesses sending more than 1,000 invoices a month.</p>
    <ul><li>Everything in Growth</li><li>Pricing to suit your volume</li><li>Help getting set up</li></ul>
    <a class="btn line" href="mailto:hello@transiqe.com">Talk to us</a></div>
</div>
<p class="small muted" style="margin-top:16px">Prices are in Australian dollars. Card fees are charged by NAB under your own merchant agreement and are not part of your Transiqe subscription.</p>'''

# ---------------------------------------------------------------- banner graphics
# Floating interface cards shown on the right of each banner. Decorative: aria-hidden.
def fl(inner, pos, n=0, d=14, rot=0, dur=7, c=''):
    return f'<div class="fl {c}" style="{pos};--n:{n};--d:{d};--rot:{rot}deg;--dur:{dur}s">{inner}</div>'

ART_FEATURES = '<div class="art" aria-hidden="true">' + ''.join([
    fl('<div class="glass mini"><div class="who">Northside Physio</div><div class="tiny muted">Invoice INV-0238</div><div class="amt num">$121.00</div><div class="btn cobalt block sm">Pay now</div></div>', 'left:8%;top:6%', 0, 10, -4, 8, 'fa'),
    fl('<div class="glass chipx"><span class="toggle"></span><span>Autopay<small>Customer opted in</small></span></div>', 'right:2%;top:2%', 1, 22, 3, 6.5, 'fb'),
    fl('<div class="chipx dark"><span class="dotok"></span><span>Marked paid in Xero<small>INV-0238, just now</small></span></div>', 'right:0;top:46%', 2, 30, -2, 7.5, 'fc'),
    fl('<div class="chipx warm"><span>Reminder sent<small>INV-0224, 2 days overdue</small></span></div>', 'left:0;bottom:4%', 3, 18, 2, 9, 'fd'),
]) + '</div>'

ART_HOW = ('<div class="art" aria-hidden="true"><div class="flowcol"><i class="pk"></i>'
    '<div class="glass chipx" style="--k:0"><span>Xero invoice<small>Sent to your customer</small></span></div>'
    '<div class="glass chipx" style="--k:1;margin-left:26px"><span>Pay now<small>Customer pays by card</small></span></div>'
    '<div class="chipx warm" style="--k:2;margin-left:52px"><span>Your NAB Gateway<small>At your agreed NAB rate</small></span></div>'
    '<div class="glass chipx" style="--k:3;margin-left:26px"><span>Your NAB account<small>Paid to you directly</small></span></div>'
    '<div class="chipx dark" style="--k:4"><span class="dotok"></span><span>Marked paid in Xero</span></div>'
    '</div></div>')

ART_PRICING = '<div class="art" aria-hidden="true">' + ''.join([
    fl('<div class="glass mini"><div class="who">Starter</div><div class="amt num">$49.95</div><div class="tiny muted">per month, up to 100 invoices</div></div>', 'left:4%;top:8%', 0, 12, -5, 8, 'pa'),
    fl('<div class="chipx dark" style="display:block;padding:16px;width:230px;white-space:normal"><div style="font:600 13.5px var(--display)">Growth</div><div class="num" style="font:500 28px/1 var(--display);letter-spacing:-.04em;margin:10px 0">$99</div><small>per month, up to 1,000 invoices</small></div>', 'right:2%;top:30%', 1, 24, 4, 7, 'pb'),
    fl('<div class="chipx warm"><span>0% of your invoices<small>A flat price for the software</small></span></div>', 'left:14%;bottom:2%', 2, 32, -2, 9, 'pc'),
]) + '</div>'

ART_SECURITY = '<div class="art" aria-hidden="true">' + ''.join([
    fl('<div class="chipx dark"><span class="dotok"></span><span>Card fields by NAB Gateway</span></div>', 'right:4%;top:14%', 0, 14, 2, 8),
    fl('<div class="chipx dark"><span class="dotok"></span><span>Tokens stored, not card numbers</span></div>', 'right:16%;top:42%', 1, 22, -2, 7),
    fl('<div class="chipx dark"><span class="dotok"></span><span>Funds never held by Transiqe</span></div>', 'right:0;top:70%', 2, 30, 1, 9),
]) + '</div>'

ART_CUSTOMERS = '<div class="art" aria-hidden="true">' + ''.join([
    fl('<div class="glass chipx"><span class="dotok"></span><span>Payment received<small>Receipt sent to Priya</small></span></div>', 'right:2%;bottom:8%', 0, 20, -2, 7),
    fl('<div class="glass chipx"><span class="toggle"></span><span>Autopay<small>On, until you turn it off</small></span></div>', 'right:22%;bottom:38%', 1, 30, 3, 8.5),
]) + '</div>'
