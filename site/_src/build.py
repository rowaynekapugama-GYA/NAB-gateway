# Assembles the static site from partials. Run: python3 _src/build.py (from site/)
import pathlib, re
SRC = pathlib.Path(__file__).parent
OUT = SRC.parent

HEAD = """<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon-32.png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://transiqe.com/assets/og.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/transiqe.css">{extra_css}</head><body class="{body_class}"><div class="ambient"><i></i></div>
"""

NAV = """<header class="nav"><div class="bar glass pill strong">
<a class="logo" href="index.html"><img src="assets/mark.svg" alt="">transiqe</a>
<nav class="links"><a href="features.html" {f}>Features</a><a href="customers.html" {c}>For your customers</a><a href="pricing.html" {p}>Pricing</a><a href="security.html" {s}>Security</a></nav>
<div class="cta"><a class="btn glassy sm" href="login.html">Sign in</a><a class="btn primary sm" href="signup.html">Start free</a></div>
</div></header>
"""

FOOTER = """<footer><div class="wrap"><div class="cols">
<div><a class="logo" href="index.html" style="display:inline-flex;align-items:center;gap:8px;font:700 18px var(--font-display);color:var(--abyss);letter-spacing:-.03em"><img src="assets/mark.svg" width="24" alt="">transiqe</a>
<p style="margin-top:10px;max-width:32ch">Card payments and autopay for Xero invoices, through your own bank. Built in Sydney for Australian small businesses.</p></div>
<div><h4>Product</h4><a href="features.html">Features</a><a href="customers.html">For your customers</a><a href="pricing.html">Pricing</a><a href="security.html">Security</a></div>
<div><h4>Account</h4><a href="login.html">Business sign in</a><a href="portal.html">Customer portal</a><a href="signup.html">Create an account</a></div>
<div><h4>Company</h4><a href="mailto:hello@transiqe.com">hello@transiqe.com</a><a href="#">Privacy</a><a href="#">Terms</a></div>
</div><p class="tiny">Transiqe is a product of Generate Your Audience Pty Ltd, ABN 68 620 590 481. Transiqe is not a bank and never holds your money: payments settle directly from your customer's card to your merchant account. Xero is a trademark of Xero Limited. NAB is a trademark of National Australia Bank Limited.</p></div></footer>
</body></html>"""

def page(name, title, desc, body, active='', body_class='', extra_css=''):
    nav = NAV.format(**{k: ('class="on"' if active == k else '') for k in 'fcps'})
    html = HEAD.format(title=title, desc=desc, body_class=body_class, extra_css=extra_css) + nav + body + FOOTER
    (OUT / f'{name}.html').write_text(html)
    print('wrote', name + '.html')

def partial(name):
    return (SRC / f'{name}.html').read_text()

for p in sorted(SRC.glob('page_*.py')):
    ns = {'page': page, 'partial': partial}
    exec(p.read_text(), ns)
