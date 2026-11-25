"""Render the link preview images (assets/og/<page>.jpg, 1200 x 630) from og.py.

    pip install playwright && playwright install chromium
    python3 site/_src/make_og.py            # all pages
    python3 site/_src/make_og.py index pricing

Fonts load from Google Fonts. To render offline, set OG_FONT_DIR to a folder that
holds sora-latin-wght-normal.woff2 and manrope-latin-wght-normal.woff2.
Images are kept under 250 KB because some messaging apps skip larger previews.
"""
import asyncio, io, os, sys, html
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

SRC = Path(__file__).resolve().parent
SITE = SRC.parent
sys.path.insert(0, str(SRC))
from og import OG  # noqa: E402

FONT_DIR = os.environ.get('OG_FONT_DIR')
if FONT_DIR:
    FONTS = (f"<style>@font-face{{font-family:'Sora';font-weight:100 800;src:url('file://{FONT_DIR}/sora-latin-wght-normal.woff2')}}"
             f"@font-face{{font-family:'Manrope';font-weight:200 800;src:url('file://{FONT_DIR}/manrope-latin-wght-normal.woff2')}}</style>")
else:
    FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600&family=Manrope:wght@500;600;700;800&display=block">'

TICK = '<svg viewBox="0 0 20 20" width="18" height="18"><circle cx="10" cy="10" r="10" fill="#1f9d55"/><path d="M5.6 10.3l2.9 2.9 5.9-6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHIP = {'blue': ('#e6ebff', '#2b46d9'), 'green': ('#dff5e7', '#17733f'), 'amber': ('#fdecd2', '#8a4b06')}

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden;background:#0b1020}
body{font-family:Manrope,system-ui,sans-serif;color:#fff;position:relative;-webkit-font-smoothing:antialiased}
.bg{position:absolute;inset:-2px;background-size:cover}
.bg.flip{transform:scaleX(-1)}
.shade{position:absolute;inset:0;background:
  linear-gradient(90deg,rgba(8,11,26,.93) 0%,rgba(8,11,26,.82) 38%,rgba(8,11,26,.35) 64%,rgba(8,11,26,.12) 100%),
  linear-gradient(0deg,rgba(8,11,26,.55) 0%,rgba(8,11,26,0) 40%)}
.warm{position:absolute;right:-120px;bottom:-160px;width:620px;height:620px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(255,150,80,.35),rgba(255,150,80,0));filter:blur(10px)}
.copy{position:absolute;left:64px;top:56px;width:640px;height:518px;display:flex;flex-direction:column}
.logo{height:40px;width:auto;display:block;align-self:flex-start}
.tag{align-self:flex-start;margin-top:44px;font-size:17px;font-weight:700;letter-spacing:.01em;padding:8px 16px;border-radius:999px;
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.28)}
h1{font-family:Sora,system-ui,sans-serif;font-weight:600;font-size:58px;line-height:1.06;letter-spacing:-.025em;margin-top:20px;text-wrap:balance}
h1.long{font-size:52px}
.works{margin-top:auto;align-self:flex-start;display:flex;align-items:center;gap:14px;background:#fff;color:#141824;
  border-radius:999px;padding:10px 22px 10px 20px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.works span{font-size:17px;font-weight:700;color:#4a5060}
.works .x{height:40px;width:40px}
.works .plus{font-size:20px;color:#9aa0ad;font-weight:600}
.works .n{height:34px;width:auto}
.card{position:absolute;right:60px;top:118px;width:384px;border-radius:26px;padding:24px 24px 20px;color:#141824;
  background:rgba(255,255,255,.86);border:1px solid rgba(255,255,255,.7);
  backdrop-filter:blur(18px) saturate(1.3);-webkit-backdrop-filter:blur(18px) saturate(1.3);
  box-shadow:0 30px 70px rgba(5,8,20,.45),0 2px 0 rgba(255,255,255,.6) inset;transform:rotate(-1.5deg)}
.card .top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.card b{font-size:20px;font-weight:800;display:block}
.card small{font-size:15px;color:#5d6373;display:block;margin-top:3px}
.chip{font-size:14px;font-weight:800;padding:5px 11px;border-radius:999px;white-space:nowrap}
.amt{font-family:Sora,system-ui,sans-serif;font-weight:600;font-size:48px;letter-spacing:-.02em;margin:16px 0 4px}
.btn{margin-top:14px;height:52px;border-radius:999px;background:linear-gradient(180deg,#4a63ff,#3350f5);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:19px;box-shadow:0 8px 20px rgba(51,80,245,.35)}
.ticks{margin-top:16px;border-top:1px solid rgba(20,24,36,.1);padding-top:14px;display:grid;gap:10px}
.ticks div{display:flex;align-items:center;gap:10px;font-size:16px;font-weight:600;color:#2b3040}
.card.low{top:auto;bottom:46px;width:360px}
.card.low .ticks{display:none}
.pill{position:absolute;right:300px;bottom:44px;display:flex;align-items:center;gap:10px;padding:12px 18px;border-radius:18px;
  background:rgba(14,18,34,.78);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  font-weight:700;font-size:16px;box-shadow:0 16px 40px rgba(0,0,0,.35);transform:rotate(1.5deg)}
.pill i{width:10px;height:10px;border-radius:50%;background:#35d07f;box-shadow:0 0 0 4px rgba(53,208,127,.25)}
.legal{position:absolute;right:120px;top:150px;width:250px;height:300px;border-radius:30px;display:grid;place-items:center;
  background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)}
'''


def card_html(c):
    low = ' low' if c['img'].startswith('owner') else ''  # keep faces in photos clear
    if not c.get('card'):
        return ('<div class="legal"><svg viewBox="0 0 24 24" width="120" height="120" fill="none" stroke="#fff" stroke-width="1.4" '
                'stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.5l8 3.2v6c0 5-3.4 8.6-8 9.8-4.6-1.2-8-4.8-8-9.8v-6z"/>'
                '<path d="M8.5 12.2l2.4 2.4 4.6-4.8"/></svg></div>')
    title, sub, amt, chip, tone, btn = c['card']
    bg, fg = CHIP[tone]
    ticks = ''.join(f'<div>{TICK}{t}</div>' for t in c.get('ticks', []))
    return (f'<div class="card{low}"><div class="top"><div><b>{title}</b><small>{sub}</small></div>'
            f'<span class="chip" style="background:{bg};color:{fg}">{chip}</span></div>'
            f'<div class="amt">{amt}</div>'
            + (f'<div class="btn">{btn}</div>' if btn else '')
            + (f'<div class="ticks">{ticks}</div>' if ticks else '') + '</div>')


def page_html(c):
    img = (SITE / 'assets/img' / f"{c['img']}.jpg").as_uri()
    a = lambda p: (SITE / 'assets' / p).as_uri()
    long = ' class="long"' if len(html.unescape(c['h'])) > 62 else ''
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body>
<div class="bg{' flip' if c.get('flip') else ''}" style="background-image:url('{img}');background-position:{c.get('pos', 'center')}"></div>
<div class="shade"></div><div class="warm"></div>
{card_html(c)}
<div class="copy"><img class="logo" src="{a('wordmark-white.svg')}" alt="">
<span class="tag">{c['tag']}</span><h1{long}>{c['h']}</h1>
<div class="works"><span>Works with your</span><img class="x" src="{a('logos/xero.png')}" alt=""><span class="plus">+</span><img class="n" src="{a('logos/nab.png')}" alt=""></div>
</div></body></html>'''


async def main(names):
    out = SITE / 'assets/og'
    out.mkdir(exist_ok=True)
    tmp = SRC / '.og_tmp.html'
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
        for name in names:
            tmp.write_text(page_html(OG[name]), encoding='utf-8')
            await pg.goto(tmp.as_uri())
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(300)
            png = await pg.screenshot(type='png')
            im = Image.open(io.BytesIO(png)).convert('RGB')
            for q in (86, 80, 74, 68):
                buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
                if buf.tell() < 250_000:
                    break
            (out / f'{name}.jpg').write_bytes(buf.getvalue())
            print(f'{name}.jpg {buf.tell() // 1024} KB')
        await br.close()
    tmp.unlink(missing_ok=True)


if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:] or list(OG)))
