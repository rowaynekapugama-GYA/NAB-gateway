# Builds the static marketing site from the page modules in this folder.
# Run from anywhere:  python3 site/_src/build.py
# Output: site/*.html  (plain HTML, no build step needed to host it)
import pathlib, sys, html

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent
APP = 'https://app.transiqe.com'          # the platform: sign in, sign up, customer portal
SITE = 'https://www.transiqe.com'
ENTITY = 'Generate Your Audience Pty Ltd'
ABN = '68 620 590 481'

NAV_LINKS = [
    ('how-it-works.html', 'How it works', 'how'),
    ('features.html', 'Features', 'features'),
    ('customers.html', 'For your customers', 'customers'),
    ('pricing.html', 'Pricing', 'pricing'),
    ('security.html', 'Security', 'security'),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600&family=Manrope:wght@500;600;700;800&display=swap">')


def head_tags(title, desc, name):
    t, d = html.escape(title), html.escape(desc)
    return (f'<title>{t}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{d}">\n'
            f'<link rel="canonical" href="{SITE}/{"" if name == "index" else name + ".html"}">\n'
            f'<link rel="icon" href="assets/favicon-32.png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">\n'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
            f'<meta property="og:image" content="{SITE}/assets/og.png"><meta property="og:type" content="website">\n'
            f'{FONTS}\n<link rel="stylesheet" href="css/site.css">\n')


def nav(mode, active=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{cur if k == active else ""}>{l}</a>' for h, l, k in NAV_LINKS)
    cta = 'white' if mode == 'on-image' else 'ink'
    return f'''<header>
<div class="nav {mode}">
  <a class="logo" href="index.html"><img src="assets/mark.svg" alt="" width="30" height="30">transiqe</a>
  <nav class="links" aria-label="Main">{links}</nav>
  <div class="acts"><a class="signin" href="{APP}/login">Sign in</a><a class="btn {cta} sm" href="{APP}/signup">Start free</a>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" id="menu-btn">&#9776;</button></div>
</div>
<div class="mobile-menu" id="mobile-menu">{links}<a href="{APP}/login">Sign in</a><a href="{APP}/portal">Customer portal</a></div>
</header>'''


def footer():
    return f'''<footer><div class="wrap">
<div class="cols">
  <div><a class="logo" href="index.html"><img src="assets/mark.svg" alt="" width="26" height="26">transiqe</a>
  <p style="margin-top:12px;max-width:34ch">Card payments on your Xero invoices, through your own NAB Gateway. Built in Sydney for Australian businesses.</p></div>
  <div><h4>Product</h4><a href="how-it-works.html">How it works</a><a href="features.html">Features</a><a href="customers.html">For your customers</a><a href="pricing.html">Pricing</a></div>
  <div><h4>Account</h4><a href="{APP}/login">Business sign in</a><a href="{APP}/signup">Create an account</a><a href="{APP}/portal">Customer portal</a></div>
  <div><h4>Trust</h4><a href="security.html">Security</a><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms of service</a><a href="autopay-terms.html">Autopay terms</a></div>
  <div><h4>Contact</h4><a href="mailto:hello@transiqe.com">hello@transiqe.com</a><a href="mailto:security@transiqe.com">security@transiqe.com</a></div>
</div>
<p class="fine">Transiqe is a product of {ENTITY}, ABN {ABN}. Transiqe is software. It is not a bank or a payment processor and never holds your money: card payments are processed by NAB under your own merchant agreement and settle to your account. Xero is a trademark of Xero Limited. NAB is a trademark of National Australia Bank Limited. Transiqe is not affiliated with or endorsed by either company.</p>
</div></footer>
<script>(function(){{var b=document.getElementById('menu-btn'),m=document.getElementById('mobile-menu');if(!b||!m)return;b.addEventListener('click',function(){{var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');}});}})();</script>'''


def hero(mode, active, inner, img=None, cls='', pos='center'):
    """Rounded photo panel with the navigation inside it."""
    pic = ''
    if img:
        pic = (f'<picture><source type="image/webp" media="(max-width:700px)" srcset="assets/img/{img}-900.webp">'
               f'<source type="image/webp" srcset="assets/img/{img}.webp">'
               f'<img src="assets/img/{img}.jpg" alt="" style="object-position:{pos}" fetchpriority="high"></picture>')
    return f'<div class="shell"><section class="panel {cls}">{pic}<div class="inner">{nav("on-image", active)}{inner}</div></section></div>'


def plain_top(active=''):
    return f'<div class="wrap topbar">{nav("on-paper", active)}</div>'


PAGES = {}


def page(name, title, desc, body):
    PAGES[name] = (title, desc, body)
    doc = (f'<!doctype html>\n<html lang="en-AU">\n<head>\n<meta charset="utf-8">\n'
           f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
           f'{head_tags(title, desc, name)}</head>\n<body>\n{body}\n{footer()}\n</body>\n</html>\n')
    (OUT / f'{name}.html').write_text(doc)
    print('wrote', f'{name}.html', len(doc) // 1024, 'KB')


def redirect(name, target):
    (OUT / f'{name}.html').write_text(
        f'<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>Transiqe</title>'
        f'<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}"></head>'
        f'<body><p>Taking you to <a href="{target}">{target}</a>.</p></body></html>\n')
    print('wrote redirect', f'{name}.html')


def run():
    ns = dict(page=page, hero=hero, plain_top=plain_top, redirect=redirect, APP=APP, SITE=SITE, ENTITY=ENTITY, ABN=ABN)
    exec((SRC / 'partials.py').read_text(), ns)
    for p in sorted(SRC.glob('page_*.py')):
        exec(p.read_text(), ns)
    # Old static auth pages now hand straight over to the platform.
    redirect('login', f'{APP}/login')
    redirect('signup', f'{APP}/signup')
    redirect('portal', f'{APP}/portal')
    # Optional: a body-only copy of the home page for previewing in a wrapped viewer.
    if len(sys.argv) > 2 and sys.argv[1] == '--fragment':
        t, d, b = PAGES['index']
        pathlib.Path(sys.argv[2]).write_text(head_tags(t, d, 'index').replace(t, 'Transiqe Website', 1) + b + '\n' + footer() + '\n')
        print('wrote fragment', sys.argv[2])


if __name__ == '__main__':
    run()
