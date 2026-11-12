"""Render Podologie Instagram graphics (carousels 1080x1350, stories/reel frames 1080x1920)."""
import sys, json, pathlib, base64
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Repo-Root. Fonts: ROOT/fonts via `npm pack @fontsource/cormorant-garamond @fontsource/inter` + entpacken
F = ROOT / "fonts"
CG = next(F.glob("fontsource-cormorant-garamond-*/files"))
IN = next(F.glob("fontsource-inter-*/files"))
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

FOOT = "Podologie Praxis wohlGefühl bei S. Wilt"
SUB = "Staatlich geprüfter Podologe · Mönchengladbach"

def _u(path):
    return "data:font/woff2;base64,"+base64.b64encode(pathlib.Path(path).read_bytes()).decode()

CSS = f"""
@font-face{{font-family:CG;src:url('{_u(CG/"cormorant-garamond-latin-600-normal.woff2")}');font-weight:600}}
@font-face{{font-family:CG;src:url('{_u(CG/"cormorant-garamond-latin-500-normal.woff2")}');font-weight:500}}
@font-face{{font-family:IN;src:url('{_u(IN/"inter-latin-400-normal.woff2")}');font-weight:400}}
@font-face{{font-family:IN;src:url('{_u(IN/"inter-latin-500-normal.woff2")}');font-weight:500}}
@font-face{{font-family:IN;src:url('{_u(IN/"inter-latin-600-normal.woff2")}');font-weight:600}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:var(--w);height:var(--h);background:#F7F9F8;color:#2B3733;font-family:IN;position:relative;overflow:hidden}}
.wrap{{position:absolute;inset:0;padding:110px 100px;display:flex;flex-direction:column}}
.band{{position:absolute;left:0;right:0;top:0;height:14px;background:linear-gradient(90deg,#9DB5A6,#8EA7B6)}}
.kicker{{font-family:IN;font-weight:600;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:#6F8F7E}}
.count{{position:absolute;top:110px;right:100px;font-size:26px;color:#9AA7A2;font-weight:500}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center}}
h1{{font-family:CG;font-weight:600;font-size:var(--h1);line-height:1.05;color:#24332E;margin-bottom:44px}}
.line{{width:96px;height:4px;background:#9DB5A6;margin-bottom:44px;border-radius:2px}}
p{{font-size:var(--p);line-height:1.5;color:#3E4C47;margin-bottom:26px}}
p.note{{font-size:calc(var(--p)*.8);color:#6F7D78}}
.num{{font-family:CG;font-weight:600;font-size:150px;line-height:.9;color:#B9CCC0;margin-bottom:24px}}
.foot{{border-top:2px solid #E1E8E4;padding-top:30px;display:flex;justify-content:space-between;align-items:flex-end}}
.foot b{{font-family:CG;font-weight:600;font-size:38px;color:#24332E;display:block}}
.foot span{{font-size:24px;color:#7A8883}}
.foot i{{font-style:normal;font-size:24px;color:#6F8F7E;font-weight:500}}
.cta{{display:inline-block;margin-top:20px;padding:22px 36px;border:2px solid #9DB5A6;border-radius:60px;font-size:30px;color:#2B3733;font-weight:500}}
"""

def slide_html(s, w, h, total, idx):
    h1 = s.get("h1size", 96 if h == 1350 else 128)
    p = s.get("psize", 38 if h == 1350 else 50)
    parts = []
    if s.get("num"): parts.append(f'<div class="num">{s["num"]}</div>')
    if s.get("title"): parts.append(f'<h1>{s["title"]}</h1><div class="line"></div>')
    for t in s.get("body", []): parts.append(f"<p>{t}</p>")
    for t in s.get("notes", []): parts.append(f'<p class="note">{t}</p>')
    if s.get("cta"): parts.append(f'<div><span class="cta">{s["cta"]}</span></div>')
    count = f'<div class="count">{idx}/{total}</div>' if total > 1 else ""
    hint = s.get("hint", "")
    return f"""<html><head><style>:root{{--w:{w}px;--h:{h}px;--h1:{h1}px;--p:{p}px}}{CSS}</style></head>
<body><div class="band"></div>{count}<div class="wrap"><div class="kicker">{s.get('kicker','')}</div>
<div class="main">{''.join(parts)}</div>
<div class="foot"><div><b>{FOOT}</b><span>{SUB}</span></div><i>{hint}</i></div></div></body></html>"""

def render(spec_path):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome")
        for set_ in spec:
            w, h = set_["size"]
            d = OUT / set_["name"]; d.mkdir(exist_ok=True)
            pg = b.new_page(viewport={"width": w, "height": h})
            n = len(set_["slides"])
            for i, s in enumerate(set_["slides"], 1):
                pg.set_content(slide_html(s, w, h, n if set_.get("count", True) else 1, i))
                pg.wait_for_timeout(250)
                pg.screenshot(path=str(d / f"{i:02d}.jpg"), type="jpeg", quality=92)
        b.close()

if __name__ == "__main__":
    render(sys.argv[1])
