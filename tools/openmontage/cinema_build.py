"""Kino-Look Reels 5-8: Texte, Piper-Stimme, HyperFrames-Projekt."""
import os, sys, re, json, shutil, subprocess
src = open("/home/claude/design2/gen.py").read()
exec(src[:src.index("def frame(")])          # liefert ic(), Farben
MODEL = "/home/claude/tts/vits-piper-de_DE-thorsten-high/de_DE-thorsten-high.onnx"
OUT = "/home/claude/om/cine"
KENN = "Markennennung · Mit KI erstellt (Stimme und Grafik) · Allgemeine Information, keine Diagnose"
CARDS_END = "Termin: 02161 / 69 80 580 · WhatsApp 0152 / 264 12 617"

REELS = [
 dict(slug="reel-5-nova-pro", title="Mein Lieblingsgerät", tag="RUCK Nova Pro", warm=False, brand="RUCK Nova Pro",
  scenes=[("nova","Was brummt denn da?",[("Hörst du das Brummen?",)*2,("Das ist mein Lieblingsgerät in der Praxis.",)*2]),
          ("nova","Das RUCK Nova Pro",[("Es heißt Nova Pro, von der Firma Ruck.",)*2,("Und es ist ganz leicht zu bedienen.",)*2]),
          ("hand","Sanft statt kratzen",[("Am Gerät hängt ein Handstück mit einem kleinen Aufsatz.",)*2,("Der dreht sich und trägt Hornhaut ab. Schicht für Schicht, ganz sanft.",)*2]),
          ("screen","Alles auf dem Touchscreen",[("Hier stelle ich das Tempo ein.",)*2,("Und ich kann Profile speichern.",)*2]),
          ("heart","Leise und gut zu führen",[("Das Gerät ist leise und gut zu führen.",)*2,("Darum arbeite ich so gern damit.",)*2]),
          ("end","",[("Komm vorbei und spür den Unterschied.",)*2])]),
 dict(slug="reel-6-nagelspange", title="Nagelspange statt Schneiden", tag="Eingewachsener Nagel", warm=True, brand="Unguisan Blue Light Gel",
  scenes=[("toe","Autsch! Der Nagel wächst ein",[("Autsch! Der Nagel wächst ein.",)*2,("Muss man ihn immer abschneiden? Nicht unbedingt.",)*2]),
          ("clip","Die Spange",[("Es gibt eine dünne Spange.",)*2,("Sie hebt die Nagelkante ganz langsam an.",)*2]),
          ("gel","Das Blue-Light-Gel",[("Befestigt wird sie mit einem Gel, das mit blauem Licht hart wird.",)*2,("Das Gel bleibt elastisch. Der Nagel kann sich bewegen.",)*2]),
          ("shield","Für Kinder, Sportler, Diabetiker",[("Das nutze ich bei Kindern, Sportlern und Menschen mit Diabetes.",)*2,("Ob es für dich passt, schaue ich vorher genau an.",)*2]),
          ("end","",[("Ruf an und vereinbare einen Termin.",)*2])]),
 dict(slug="reel-7-pilzempfindlich", title="Juckt es zwischen den Zehen?", tag="Fußpilz und Hautpflege", warm=False, brand="Allpresan No. 7",
  scenes=[("toe","Juckt es? Schuppt es?",[("Juckt es zwischen den Zehen?",)*2,("Oder schuppt die Haut?",)*2]),
          ("shield","Haut = Schutzmauer",[("Deine Haut ist wie eine Schutzmauer.",)*2,("Ist sie kaputt, kommen Keime leichter hinein.",)*2]),
          ("list","Erst abklären lassen",[("Das kann ein Zeichen für Fußpilz sein.",)*2,("Lass es abklären, von einer Ärztin oder einem Podologen.",)*2]),
          ("foam","Pflege dazu",[("Zur Pflege nutze ich die Allpresan Nummer sieben Schaumcreme.",)*2,("Sie begleitet die Behandlung. Sie ersetzt sie nicht.",)*2]),
          ("end","",[("Fragen? Ruf einfach an.",)*2])]),
 dict(slug="reel-8-diabetes-check", title="Der tägliche Fuß-Check", tag="Diabetes und Füße", warm=True, brand="GEHWOL",
  scenes=[("heart","Diabetes und Füße",[("Diabetes und Füße. Das gehört zusammen.",)*2,("Denn Füße können dann weniger spüren.",)*2]),
          ("list","Der 3er-Check",[("Schau jeden Tag eine Minute hin.",)*2,("Gibt es Risse, Blasen oder eine rote Stelle?",)*2]),
          ("foam","Pflegen, nicht aufweichen",[("Creme die Füße jeden Tag ein, aber nicht zwischen den Zehen.",)*2,("Welche Pflege von Gehwol passt, zeige ich dir in der Praxis.",)*2]),
          ("shield","Regelmäßig zur Fußpflege",[("Geh regelmäßig zur Fußpflege.",)*2,("Wir sehen, was du nicht spürst.",)*2]),
          ("end","",[("Ruf an und vereinbare deinen Termin.",)*2])]),
]
# Aussprache nur für Sprecher
PRON = {"Unguisan":"Ungwisan","GEHWOL":"Gehwol"}

def run(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    return r.stdout
def dur(p): return float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').strip())
def tts(text, out):
    if not os.path.exists(out):
        p = subprocess.run(["python3","-m","piper","-m",MODEL,"-f",out,"--length-scale","1.12","--sentence-silence","0.25"],input=text,text=True,capture_output=True)
        if p.returncode: print(p.stderr); sys.exit(1)
    return dur(out)

def build(r):
    wd = f"{OUT}/{r['slug']}"; hf = f"{wd}/hyperframes"
    if os.path.exists(hf): shutil.rmtree(hf)
    os.makedirs(f"{hf}/assets", exist_ok=True)
    for f,dst in (("/home/claude/om/gsap.min.js","gsap.min.js"),(os.path.expanduser("~/.fonts/Bricolage.ttf"),"Bricolage.ttf"),(os.path.expanduser("~/.fonts/Kalam-Bold.ttf"),"Kalam-Bold.ttf")):
        shutil.copy(f, f"{hf}/assets/{dst}")
    t = 0.0; plan = []; parts = []
    n = len(r["scenes"])
    for si,(icon,head,cards) in enumerate(r["scenes"]):
        cs = []
        for ci,(shown,spoken) in enumerate(cards):
            sp = spoken
            for k,v in PRON.items(): sp = sp.replace(k, v)
            wav = f"{wd}/s{si}c{ci}.wav"; d = tts(sp, wav)
            last = ci == len(cards)-1
            hold = d + (0.5 if last else 0.25)
            if si == n-1 and last: hold = d + 2.6
            cs.append((t,d,hold,shown)); parts.append((wav,hold)); t += hold
        plan.append((icon,head,cs))
    total = round(t,3)
    lst = f"{wd}/audio.txt"
    with open(lst,"w") as f:
        for i,(w,h) in enumerate(parts):
            pw = w.replace(".wav","_pad.wav")
            run(f'ffmpeg -y -v error -i "{w}" -af "apad=whole_dur={h:.3f}" -ar 48000 -ac 2 "{pw}"')
            f.write(f"file '{pw}'\n")
    run(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -ac 2 "{hf}/assets/narration.wav"')
    warm = r["warm"]
    glow = "#F2C25B" if warm else "#7FD1B9"
    spot = "#6B4A14" if warm else "#1F5A52"; base = "#2A1D0B" if warm else "#0E2422"
    tl = []; clips = []; caps = []
    for si,(icon,head,cs) in enumerate(plan):
        s0 = cs[0][0]; sd = sum(c[2] for c in cs); p = f"s{si}"
        if icon == "end":
            inner = (f'<div id="{p}in" style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:36px;padding:0 70px;box-sizing:border-box">'
                     f'<div style="font-family:Kalam;font-weight:700;font-size:58px;color:{glow}">Mein Favorit in der Praxis</div>'
                     f'<div style="font-family:Bricolage;font-weight:800;font-size:104px;line-height:1.0;letter-spacing:-2px">{r["brand"]}</div>'
                     f'<div style="height:3px;background:#ffffff44"></div>'
                     f'<div style="font-family:Bricolage;font-weight:800;font-size:72px">02161 / 69 80 580</div>'
                     f'<div style="font-family:Bricolage;font-weight:500;font-size:40px;line-height:1.35;color:#C9DAD3">WhatsApp 0152 / 264 12 617<br>Podologie Praxis wohlGefühl bei S. Wilt<br>Eickener Str. 55, Mönchengladbach</div>'
                     f'<div style="font-family:Bricolage;font-weight:500;font-size:28px;line-height:1.35;color:#9FB8B0">{KENN}</div></div>')
            if si == 0: pass
            tl.append(f'tl.from("#{p}in > *", {{y:50, opacity:0, duration:0.6, stagger:0.15, ease:"power3.out"}}, {s0+0.1:.3f});')
        else:
            svg = ic(icon,"#F3F6F4","#2E5A55").replace('width="150" height="150"','width="720" height="720"')
            inner = (f'<div id="{p}in" style="position:absolute;inset:0">'
                     f'<div id="{p}head" style="position:absolute;left:70px;right:70px;top:300px;font-family:Bricolage;font-weight:800;font-size:92px;line-height:1.02;letter-spacing:-2px">{head}</div>'
                     f'<div id="{p}ic" style="position:absolute;left:180px;top:560px;width:720px;height:720px;filter:drop-shadow(0 0 60px {glow}88)">{svg}</div></div>')
            tl.append(f'tl.from("#{p}head", {{y:60, opacity:0, duration:0.55, ease:"power3.out"}}, {s0+0.05:.3f});')
            tl.append(f'tl.from("#{p}ic", {{scale:0.55, opacity:0, transformOrigin:"50% 50%", duration:0.7, ease:"back.out(1.7)"}}, {s0+0.15:.3f});')
            tl.append(f'tl.to("#{p}in", {{scale:1.07, transformOrigin:"50% 55%", duration:{sd:.3f}, ease:"none"}}, {s0:.3f});')
            tl.append(f'tl.to("#{p}ic", {{y:-18, duration:1.4, yoyo:true, repeat:{max(1,int(sd/1.4))}, ease:"sine.inOut"}}, {s0+0.9:.3f});')
        tl.append(f'tl.from("#{p}panel", {{opacity:0, duration:0.4}}, {s0:.3f});')
        if si < n-1: tl.append(f'tl.to("#{p}panel", {{opacity:0, duration:0.3}}, {s0+sd-0.3:.3f});')
        bgst = f'style="background:radial-gradient(ellipse at 50% 38%, {spot} 0%, {base} 62%, #050B0A 100%)"' if icon=="end" else ""
        clips.append(f'<div id="{p}panel" {bgst} class="clip panel" data-start="{s0:.3f}" data-duration="{sd:.3f}" data-track-index="{2+si%2}" data-layout-allow-overflow>{inner}</div>')
        if icon == "end": 
            continue
        for ci,(cs_,cd,ch,text) in enumerate(cs):
            cid = f"{p}c{ci}"; ws = text.split(" ")
            spans = " ".join(f'<span id="{cid}w{i}" class="w">{w}</span>' for i,w in enumerate(ws))
            caps.append(f'<div id="{cid}" class="clip cap" data-start="{cs_:.3f}" data-duration="{ch:.3f}" data-track-index="5"><div class="capbox">{spans}</div></div>')
            tl.append(f'tl.from("#{cid} .capbox", {{y:24, opacity:0, duration:0.25, ease:"power2.out"}}, {cs_:.3f});')
            wts = [len(w)+2 for w in ws]; tot = sum(wts); acc = 0.0
            for wi in range(len(ws)):
                wt = cs_ + 0.05 + acc/tot*cd*0.96; acc += wts[wi]
                tl.append(f'tl.to("#{cid}w{wi}", {{opacity:1, color:"{glow}", duration:0.1}}, {wt:.3f});')
                tl.append(f'tl.to("#{cid}w{wi}", {{color:"#FFFFFF", duration:0.2}}, {wt+max(0.18,wts[wi]/tot*cd*0.96):.3f});')
    grain = "<svg width='0' height='0'></svg>"
    html = f'''<!doctype html>
<html lang="de"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<title>{r["title"]}</title><script src="assets/gsap.min.js"></script>
<style>
@font-face {{ font-family: Bricolage; src: url(assets/Bricolage.ttf); font-weight: 200 800; }}
@font-face {{ font-family: Kalam; src: url(assets/Kalam-Bold.ttf); font-weight: 700; }}
body {{ margin:0; background:#050B0A; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:Bricolage,system-ui,sans-serif; color:#fff; }}
#bg {{ position:absolute; inset:0; background: radial-gradient(ellipse at 50% 38%, {spot} 0%, {base} 62%, #050B0A 100%); }}
#vig {{ position:absolute; inset:0; box-shadow: inset 0 0 260px rgba(0,0,0,.75); pointer-events:none; }}
.panel {{ position:absolute; left:0; top:0; width:1080px; height:1920px; overflow:hidden; }}
#lower {{ position:absolute; left:70px; top:130px; font-size:34px; font-weight:700; letter-spacing:.5px; color:{glow}; }}
#tagl {{ position:absolute; left:70px; top:180px; font-size:30px; font-weight:500; color:#C9DAD3; }}
.cap {{ position:absolute; left:70px; top:1400px; width:940px; height:300px; }}
.capbox {{ width:100%; box-sizing:border-box; background:rgba(0,0,0,.62); border-radius:24px; padding:26px 34px; display:flex; flex-wrap:wrap; align-items:center; justify-content:center; text-align:center; font-weight:700; font-size:58px; line-height:1.2; column-gap:.25em; min-height:200px; }}
.w {{ display:inline-block; opacity:.45; }}
#ki {{ position:absolute; left:70px; right:70px; top:1790px; font-size:24px; font-weight:500; color:#9FB8B0; text-align:center; }}
</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{total}" data-fps="30">
<div id="base" class="clip" data-start="0" data-duration="{total}" data-track-index="0" data-layout-allow-overflow>
<div id="bg"></div><div id="vig"></div>
<div id="lower">PODOLOGIE WOHLGEFÜHL</div><div id="tagl">{r["tag"]}</div>
<div id="ki">{KENN}</div></div>
{"".join(clips)}{"".join(caps)}
<audio id="narration" src="assets/narration.wav" data-start="0" data-duration="{total}" data-track-index="10" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
tl.from("#lower", {{ x:-60, opacity:0, duration:0.6, ease:"power3.out" }}, 0.2);
tl.from("#tagl", {{ x:-60, opacity:0, duration:0.6, ease:"power3.out" }}, 0.35);
{chr(10).join(tl)}
window.__timelines["main"] = tl;
</script></body></html>
'''
    open(f"{hf}/index.html","w").write(html)
    return hf, total

if __name__ == "__main__":
    w = sys.argv[1] if len(sys.argv) > 1 else "all"
    for r in REELS:
        if w in ("all", r["slug"]): print(r["slug"], *build(r))
