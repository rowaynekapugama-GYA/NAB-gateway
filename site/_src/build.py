# Builds the static marketing site from the page modules in this folder.
# Run from anywhere:  python3 site/_src/build.py
# Output: site/*.html  (plain HTML, no build step needed to host it)
import pathlib, sys, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from og import OG

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent
APP = 'https://app.transiqe.com'          # the platform: sign in, sign up, customer portal
SITE = 'https://www.transiqe.com'
# Where link preview images are loaded from. Messaging apps need a full web address,
# so this must be a host that serves this version of the site. Change it to SITE
# once www.transiqe.com points at the new site.
OG_HOST = 'https://transiqeworkingmodel.vercel.app'
ENTITY = 'Generate Your Audience Pty Ltd'
ABN = '68 620 590 481'

def _ic(path):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'

MI = {
    'route': _ic('<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H15a3.5 3.5 0 010 7H9a3.5 3.5 0 000 7h6.5"/>'),
    'spark': _ic('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>'),
    'user': _ic('<circle cx="12" cy="8" r="4"/><path d="M4 20c0-3.6 3.6-6 8-6s8 2.4 8 6"/>'),
    'shield': _ic('<path d="M12 2.5l8 3.5v5.5c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'),
    'brief': _ic('<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M9 7V5.5A1.5 1.5 0 0110.5 4h3A1.5 1.5 0 0115 5.5V7"/><path d="M3 12.5h18"/>'),
    'cup': _ic('<path d="M4 9h13v5a5 5 0 01-5 5H9a5 5 0 01-5-5z"/><path d="M17 10.5h1.5a2.5 2.5 0 010 5H17"/><path d="M8 3.5c0 1 1 1.3 1 2.5M12 3.5c0 1 1 1.3 1 2.5"/>'),
    'bag': _ic('<path d="M5 8h14l-1.2 11.2a2 2 0 01-2 1.8H8.2a2 2 0 01-2-1.8z"/><path d="M9 8V6.5a3 3 0 016 0V8"/>'),
    'calc': _ic('<rect x="5" y="2.5" width="14" height="19" rx="2.5"/><path d="M8.5 6.5h7"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01M8.5 14.5h.01M12 14.5h.01M15.5 14.5h.01M8.5 18h.01M12 18h.01M15.5 18h.01"/>'),
    'help': _ic('<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 114 2c-.9.6-1.5 1.1-1.5 2.2"/><path d="M12 17h.01"/>'),
    'book': _ic('<path d="M4 5.5A2.5 2.5 0 016.5 3H20v15H6.5A2.5 2.5 0 004 20.5z"/><path d="M4 20.5A2.5 2.5 0 016.5 18H20v3H6.5"/>'),
    'news': _ic('<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M7 8.5h10M7 12h10M7 15.5h6"/>'),
}

# (key, label, href, icon, description)
MENU = [
    ('Product', [
        ('how', 'How it works', 'how-it-works.html', 'route', 'From Xero invoice to money in your NAB account'),
        ('features', 'Features', 'features.html', 'spark', 'Pay now, autopay, portal, reminders and reconciliation'),
        ('customers', 'For your customers', 'customers.html', 'user', 'What the people paying you see'),
        ('security', 'Security', 'security.html', 'shield', 'How payments and data are protected'),
    ], 'setup'),
    ('Solutions', [
        ('services', 'Service-based businesses', 'solutions-services.html', 'brief', 'Retainers, appointments, projects and memberships'),
        ('hospitality', 'Restaurants and cafes', 'solutions-hospitality.html', 'cup', 'Catering, functions, deposits and trade accounts'),
        ('ecommerce', 'E-commerce', 'solutions-ecommerce.html', 'bag', 'Wholesale, trade and made-to-order sales'),
        ('accountants', 'Bookkeepers and accountants', 'solutions-accountants.html', 'calc', 'Card payments that reconcile themselves in Xero'),
    ], 'aus'),
    ('Pricing', 'pricing.html', 'pricing'),
    ('Resources', [
        ('faq', 'FAQ', 'faq.html', 'help', 'Straight answers to common questions'),
        ('help', 'Help centre', 'help.html', 'book', 'Step-by-step setup and how-to guides'),
        ('blog', 'Articles', 'blog.html', 'news', 'Guides on getting paid on time'),
    ], 'article'),
]

CHEV = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def _menu_card(kind):
    if kind == 'setup':
        return ('<a class="dd-card warm" href="how-it-works.html"><span class="dd-logos"><img src="assets/logos/xero.png" alt="Xero" width="40" height="40">'
                '<span class="dd-plus">+</span><img class="nabmark" src="assets/logos/nab.png" alt="NAB" width="82" height="32"></span>'
                '<b>Set up in under five minutes</b><small>Connect Xero and your NAB Gateway, switch on Pay now, and send your next invoice.</small><span class="dd-go">See how it works</span></a>')
    if kind == 'aus':
        return ('<a class="dd-card photo" href="index.html#built-for"><img src="assets/img/owner-laptop-900.webp" alt="" loading="lazy">'
                '<span class="dd-over"><b>Built for Australian businesses</b><small>Small, growing and larger businesses that invoice from Xero and bank with NAB.</small></span></a>')
    return ('<a class="dd-card ink" href="article-autopay-vs-direct-debit.html"><span class="dd-tag">Latest article</span>'
            '<b>Autopay and direct debit are not the same thing</b><small>What each one is, who can cancel it, and what to tell your customers.</small><span class="dd-go">Read the article</span></a>')


def nav(mode, active=''):
    cur = ' aria-current="page"'
    desk, mob = [], []
    for n, entry in enumerate(MENU):
        label = entry[0]
        if isinstance(entry[1], str):
            href, key = entry[1], entry[2]
            desk.append(f'<a class="top" href="{href}"{cur if key == active else ""}>{label}</a>')
            mob.append(f'<a class="mm-link" href="{href}">{label}</a>')
            continue
        items, card = entry[1], entry[2]
        on = any(k == active for k, *_ in items)
        lis = ''.join(f'<a class="dd-item" href="{h}"{cur if k == active else ""}><span class="dd-ic">{MI[i]}</span><span><b>{l}</b><small>{d}</small></span></a>'
                      for k, l, h, i, d in items)
        desk.append(f'<div class="dd"><button class="dd-btn{" on" if on else ""}" type="button" aria-expanded="false" aria-haspopup="true">{label}{CHEV}</button>'
                    f'<div class="dd-panel" role="group" aria-label="{label}"><div class="dd-list{" one" if len(items) < 4 else ""}">{lis}</div>{_menu_card(card)}</div></div>')
        mlis = ''.join(f'<a href="{h}"><span class="dd-ic">{MI[i]}</span><span><b>{l}</b><small>{d}</small></span></a>' for k, l, h, i, d in items)
        mob.append(f'<details class="mm-group"{" open" if on else ""}><summary>{label}{CHEV}</summary><div class="mm-items">{mlis}</div></details>')
    cta = 'white' if mode == 'on-image' else 'ink'
    return f'''<header>
<div class="nav {mode}">
  <a class="logo" href="index.html"><img src="assets/mark.svg" alt="" width="30" height="30">transiqe</a>
  <nav class="links" aria-label="Main">{''.join(desk)}</nav>
  <div class="acts"><a class="signin" href="{APP}/login">Sign in</a><a class="btn {cta} sm" href="{APP}/signup">Sign up</a>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu" id="menu-btn"><span></span><span></span></button></div>
</div>
<div class="mobile-menu" id="mobile-menu">{''.join(mob)}
  <div class="mm-acts"><a class="btn line" href="{APP}/login">Sign in</a><a class="btn ink" href="{APP}/signup">Sign up</a></div>
  <a class="mm-small" href="{APP}/portal">Paying an invoice? Go to the customer portal</a>
</div>
</header>'''


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600&family=Manrope:wght@500;600;700;800&display=swap">')


def head_tags(title, desc, name):
    t, d = html.escape(title), html.escape(desc)
    key = name if name in OG else 'index'
    img = f'{OG_HOST}/assets/og/{key}.jpg'
    alt = html.escape('Transiqe: ' + re.sub('<[^>]+>', '', html.unescape(OG[key]['h'])))
    return (f'<title>{t}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{d}">\n'
            f'<link rel="canonical" href="{SITE}/{"" if name == "index" else name + ".html"}">\n'
            f'<link rel="icon" href="assets/favicon-32.png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">\n'
            f'<meta property="og:site_name" content="Transiqe"><meta property="og:type" content="website">\n'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">\n'
            f'<meta property="og:image" content="{img}"><meta property="og:image:type" content="image/jpeg">'
            f'<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta property="og:image:alt" content="{alt}">\n'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">'
            f'<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{img}">\n'
            f'{FONTS}\n<link rel="stylesheet" href="css/site.css">\n')


def footer():
    return f'''<footer><div class="wrap">
<div class="cols">
  <div><a class="logo" href="index.html"><img src="assets/mark.svg" alt="" width="26" height="26">transiqe</a>
  <p style="margin-top:12px;max-width:34ch">Card payments on your Xero invoices, through your own NAB Gateway. Built in Sydney for Australian businesses.</p>
  <div class="foot-logos"><img src="assets/logos/xero.png" alt="Xero" width="34" height="34"><img src="assets/logos/nab.png" alt="NAB" width="72" height="28"></div></div>
  <div><h4>Product</h4><a href="how-it-works.html">How it works</a><a href="features.html">Features</a><a href="customers.html">For your customers</a><a href="pricing.html">Pricing</a><a href="security.html">Security</a></div>
  <div><h4>Solutions</h4><a href="solutions-services.html">Service-based businesses</a><a href="solutions-hospitality.html">Restaurants and cafes</a><a href="solutions-ecommerce.html">E-commerce</a><a href="solutions-accountants.html">Bookkeepers and accountants</a></div>
  <div><h4>Resources</h4><a href="faq.html">FAQ</a><a href="help.html">Help centre</a><a href="blog.html">Articles</a><a href="mailto:hello@transiqe.com">hello@transiqe.com</a></div>
  <div><h4>Account</h4><a href="{APP}/login">Business sign in</a><a href="{APP}/signup">Sign up</a><a href="{APP}/portal">Customer portal</a></div>
  <div><h4>Legal</h4><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms of service</a><a href="autopay-terms.html">Autopay terms</a></div>
</div>
<p class="fine">Transiqe is a product of {ENTITY}, ABN {ABN}. Transiqe is software. It is not a bank or a payment processor and never holds your money: card payments are processed by NAB under your own merchant agreement and settle to your account. Xero is a trademark of Xero Limited. NAB is a trademark of National Australia Bank Limited. Transiqe is not affiliated with or endorsed by either company.</p>
</div></footer>
<script src="js/site.js" defer></script>'''


def hero(mode, active, inner, img=None, cls='', pos='center', flip=False):
    """Rounded photo panel with the navigation inside it."""
    pic = ''
    if img:
        pic = (f'<picture{" class=" + chr(34) + "flip" + chr(34) if flip else ""}><source type="image/webp" media="(max-width:700px)" srcset="assets/img/{img}-900.webp">'
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
    ns = dict(page=page, hero=hero, plain_top=plain_top, redirect=redirect, APP=APP, SITE=SITE, ENTITY=ENTITY, ABN=ABN, MI=MI)
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
