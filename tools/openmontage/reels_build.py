import os, sys, json, subprocess, math, shutil

ns = {}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "illustrations.py")).read(), ns)   # reuse illustrations + helpers (rewrites the same slide files)
g_ = ns
INK = g_["INK"]; PAPER = g_["PAPER"]; SAGE = g_["SAGE"]; SAGE_L = g_["SAGE_L"]; BLUE = g_["BLUE"]; BLUE_L = g_["BLUE_L"]
BLUE_D = g_["BLUE_D"]; AMBER_D = g_["AMBER_D"]; AMBER_L = g_["AMBER_L"]; CORAL = g_["CORAL"]; CORAL_L = g_["CORAL_L"]
svg = g_["svg"]; icon = g_["icon"]; toe = g_["toe"]; gg = g_["g"]; stars = g_["stars"]; lbl = g_["lbl"]

OUT = "/home/claude/reels"
MODEL = "/home/claude/tts/vits-piper-de_DE-thorsten-high/de_DE-thorsten-high.onnx"
FPS = 30

# ---- extra illustrations ----
three = "".join(gg(toe("straight", n), 20 + i*300, 30, 0.9) + (stars(250 + i*300, 70, 0.8) if n >= 2 else "") for i, n in enumerate([1, 2, 3])) \
        + lbl(137, 420, "rot", 34, weight=700) + lbl(437, 420, "entzündet", 34, weight=700) + lbl(737, 420, "wildes Fleisch", 34, weight=700)
ILL = {
 "a1": (g_["a1"], 900, 500, BLUE_L), "a2": (three, 900, 450, "#FFFFFF"), "a3": (g_["a3"], 900, 520, BLUE_L),
 "b1": (g_["b1"], 900, 560, SAGE_L), "b2": (g_["b2"], 900, 600, "#FFFFFF"), "b3": (g_["b3_ill"], 900, 340, SAGE_L),
 "c1": (g_["c1"], 900, 570, AMBER_L), "c2": (g_["c2"], 900, 580, BLUE_L), "c3": (g_["c3"], 900, 580, SAGE_L),
 "c4": (g_["c4"], 900, 580, "#EEF0EC"), "d1a": (g_["d1a"], 900, 330, BLUE_L), "d1b": (g_["d1b"], 900, 360, SAGE_L),
 "e1": (g_["e1"], 900, 560, CORAL_L),
}
def icon_trio(items, col, bg):
    cells = ""
    for i, (ic, t) in enumerate(items):
        x = 150 + i*300
        cells += (f'<circle cx="{x}" cy="190" r="110" fill="{bg}" stroke="{INK}" stroke-width="5"/>'
                  f'<g transform="translate({x-60},130) scale(5)" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ns["IC"][ic]}</g>'
                  + lbl(x, 370, t, 36, weight=700))
    return cells
ILL["e2"] = (icon_trio([("eye", "Anschauen"), ("search", "Prüfen"), ("hand", "Abtasten")], "#A93A22", CORAL_L), 900, 400, "#FFFFFF")
ILL["e3"] = (icon_trio([("steth", "Arzt"), ("users", "zusammen"), ("shield", "Podologe")], BLUE_D, BLUE_L), 900, 400, "#FFFFFF")

# ---- reels (cards = one subtitle + one spoken line) ----
END = {"ill": "end", "cards": [("Fragen zu deinen Füßen? Ruf uns an.", "Fragen zu deinen Füßen? Ruf uns an. Podologie Praxis Wohlgefühl in Mönchengladbach.")]}
REELS = [
 dict(slug="reel-1-insulin", title="Warum braucht der Körper Insulin?", tag="Diabetes einfach erklärt", color=AMBER_D, scenes=[
   {"ill": "c1", "cards": ["Wenn du isst, macht dein Körper aus dem Essen Zucker.", "Dieser Zucker heißt Glukose. Er schwimmt mit dem Blut durch den Körper."]},
   {"ill": "c3", "cards": ["Deine Zellen brauchen den Zucker. Er gibt ihnen Energie.", "Energie zum Rennen, Spielen und Denken."]},
   {"ill": "c2", "cards": ["Aber jede Zelle hat eine Tür. Und die ist zu.", "Zum Öffnen braucht sie einen Schlüssel. Er heißt Insulin.", "Das Insulin kommt aus der Bauchspeicheldrüse."]},
   {"ill": "c3", "cards": ["Der Schlüssel passt ins Schloss. Die Tür geht auf.", "Der Zucker kommt in die Zelle. Jetzt hat sie Energie."]},
   {"ill": "c4", "cards": ["Bei Diabetes klappt das nicht richtig.", "Der Zucker bleibt draußen im Blut. Die Zelle hat Hunger."]},
   {"ill": "d1a", "cards": ["Bei Typ 1 macht der Körper fast kein Insulin mehr. Der Schlüssel fehlt."]},
   {"ill": "d1b", "cards": ["Bei Typ 2 ist der Schlüssel da. Aber das Schloss klemmt."]},
   {"ill": "e1", "cards": ["Zu viel Zucker im Blut kann auch den Füßen schaden. Darum passen wir gut auf sie auf."]},
   END]),
 dict(slug="reel-2-huehnerauge", title="Warum tut ein Hühnerauge weh?", tag="Druckstelle und Hühnerauge", color=SAGE, scenes=[
   {"ill": "b1", "cards": ["Drückt der Schuh jeden Tag an der gleichen Stelle, wehrt sich die Haut.", "Sie wird dick und hart. Das ist Hornhaut."]},
   {"ill": "b2", "cards": ["Drückt es immer weiter, wächst ein harter Kern nach innen.", "Wie ein kleiner Dorn. Das ist ein Hühnerauge.", "Der Dorn drückt auf einen Nerv. Darum tut jeder Schritt weh."]},
   {"ill": "b3", "cards": ["Bitte nicht selbst schneiden!", "Der Podologe entfernt den Kern ganz vorsichtig.", "Ein weicher Schutz nimmt den Druck weg."]},
   END]),
 dict(slug="reel-3-nagel", title="Was ist ein eingewachsener Nagel?", tag="Eingewachsener Nagel", color=BLUE, scenes=[
   {"ill": "a1", "cards": ["Schneidest du den Zehennagel rund, kann die Ecke in die Haut wachsen.", "Das tut weh.", "Besser: den Nagel gerade schneiden. Und nicht zu kurz."]},
   {"ill": "a2", "cards": ["Erst wird die Haut rot. Dann entzündet sie sich.", "Später kann wildes Fleisch wachsen."]},
   {"ill": "a3", "cards": ["Der Podologe hilft ganz ohne Schneiden.", "Mit einem kleinen Polster oder einer Spange. Sie hebt den Nagel sanft an."]},
   {"ill": "warn", "cards": ["Eiter oder Fieber? Dann bitte zuerst zum Arzt."]},
   END]),
 dict(slug="reel-4-stein-im-schuh", title="Der Stein, den man nicht spürt", tag="Diabetes und Füße", color=CORAL, scenes=[
   {"ill": "e1", "cards": ["Stell dir vor, ein Steinchen ist in deinem Schuh.", "Das merkst du sofort, oder?", "Bei Diabetes können die Nerven im Fuß leiser werden.", "Dann spürt man das Steinchen nicht. Und es entsteht eine Wunde."]},
   {"ill": "e2", "cards": ["Darum jeden Tag die Füße anschauen. Auch unten und zwischen den Zehen.", "Und die Schuhe innen abtasten, bevor du sie anziehst."]},
   {"ill": "e3", "cards": ["Der Arzt kann auch Podologie verordnen.", "Dann helfen Arzt und Podologe zusammen."]},
   END]),
]

def frame_html(reel, ill, text, kind="normal"):
    col = reel["color"]
    if ill == "end":
        body = (f'<div style="position:absolute;left:60px;right:60px;top:470px;height:700px;border:5px solid {INK};border-radius:28px;background:{INK};color:#fff;'
                f'display:flex;flex-direction:column;justify-content:center;gap:34px;padding:0 60px;box-sizing:border-box">'
                f'<div style="font-family:Kalam;font-weight:700;font-size:60px;line-height:1.1;color:#D3E3CD">Fragen zu deinen Füßen?</div>'
                f'<div style="font-family:\'Bricolage Grotesque\';font-weight:800;font-size:76px;line-height:1.05">02161 / 69 80 580</div>'
                f'<div style="font-family:\'Bricolage Grotesque\';font-weight:500;font-size:40px;line-height:1.35;color:#D9E4E1">WhatsApp 0152 / 264 12 617<br>wohlgefuehl-mg.de</div>'
                f'<div style="font-family:\'Bricolage Grotesque\';font-weight:700;font-size:36px;line-height:1.3;border-top:3px solid #4B6563;padding-top:26px">Podologie Praxis wohlGefühl bei S. Wilt<br><span style="font-weight:500;color:#D9E4E1">Eickener Str. 55, Mönchengladbach</span></div></div>')
        text = None
    elif ill == "warn":
        body = (f'<div style="position:absolute;left:60px;right:60px;top:470px;height:700px;border:5px solid {INK};border-radius:28px;background:{CORAL_L};'
                f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px">{icon("alert", "#A93A22", 260)}'
                f'<div style="font-family:Kalam;font-weight:700;font-size:64px;color:{INK}">Erst zum Arzt</div></div>')
    else:
        s, w, h, bg = ILL[ill]
        body = (f'<div style="position:absolute;left:60px;right:60px;top:470px;height:700px;border:5px solid {INK};border-radius:28px;background:{bg};'
                f'display:flex;align-items:center;justify-content:center;overflow:hidden;box-sizing:border-box;padding:24px">'
                f'<div style="width:100%;max-height:640px;display:flex;align-items:center">{svg(w, h, s, "")}</div></div>')
    sub = ""
    if text:
        sub = (f'<div style="position:absolute;left:60px;width:840px;top:1210px;min-height:230px;box-sizing:border-box;background:#FFFFFF;border:5px solid {INK};border-radius:28px;'
               f'padding:28px 36px;display:flex;align-items:center;justify-content:center;text-align:center;'
               f'font-family:\'Bricolage Grotesque\';font-weight:700;font-size:54px;line-height:1.18;color:{INK};text-wrap:balance">{text}</div>')
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><style>body{{margin:0}}</style></head><body>
<div style="width:1080px;height:1920px;position:relative;overflow:hidden;background:{PAPER};color:{INK}">
<div style="position:absolute;left:0;top:0;width:1080px;height:16px;background:{col}"></div>
<div style="position:absolute;right:-200px;top:-200px;width:620px;height:620px;border-radius:50%;background:{reel.get("tint", "#E3EBE7")};opacity:.6"></div>
<div style="position:absolute;left:60px;top:228px;font-family:'Bricolage Grotesque';font-weight:700;font-size:32px;color:{col}">{reel["tag"]}</div>
<h1 style="position:absolute;left:60px;width:880px;top:276px;margin:0;font-family:'Bricolage Grotesque';font-weight:800;font-size:68px;line-height:1.02;letter-spacing:-1.5px;text-wrap:balance">{reel["title"]}</h1>
{body}
{sub}
<div style="position:absolute;left:60px;top:1502px;font-family:'Bricolage Grotesque';font-weight:500;font-size:24px;color:#5B6B6A">Mit KI erstellt, KI-Stimme. Allgemeine Information, keine Diagnose.</div>
</div></body></html>'''

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:]); sys.exit(1)
    return r.stdout

def dur(p):
    return float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').strip())

def tts(text, out):
    if not os.path.exists(out):
        p = subprocess.run(["python3", "-m", "piper", "-m", MODEL, "-f", out, "--length-scale", "1.12", "--sentence-silence", "0.25"],
                           input=text, text=True, capture_output=True)
        if p.returncode != 0: print(p.stderr); sys.exit(1)
    return dur(out)

def build(reel, only_frames=False):
    from playwright.sync_api import sync_playwright
    wd = os.path.join(OUT, reel["slug"]); os.makedirs(wd, exist_ok=True)
    tint = {AMBER_D: AMBER_L, SAGE: SAGE_L, BLUE: BLUE_L, CORAL: CORAL_L}[reel["color"]]
    reel["tint"] = tint
    plan = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for si, sc in enumerate(reel["scenes"]):
            for ci, card in enumerate(sc["cards"]):
                shown, spoken = (card if isinstance(card, tuple) else (card, card))
                png = os.path.join(wd, f"s{si:02d}c{ci:02d}.png")
                pg.set_content(frame_html(reel, sc["ill"], shown))
                pg.wait_for_timeout(150)
                pg.screenshot(path=png)
                plan.append((si, ci, png, spoken, ci == len(sc["cards"]) - 1))
        b.close()
    if only_frames:
        return
    # audio + timing
    parts = []
    for (si, ci, png, spoken, last) in plan:
        wav = png.replace(".png", ".wav")
        d = tts(spoken, wav)
        hold = d + (0.55 if last else 0.25)
        if si == len(reel["scenes"]) - 1 and last:
            hold = d + 1.4
        parts.append((si, png, wav, hold))
    # padded audio
    alist = os.path.join(wd, "audio.txt")
    with open(alist, "w") as f:
        for i, (si, png, wav, hold) in enumerate(parts):
            pw = wav.replace(".wav", "_pad.wav")
            run(f'ffmpeg -y -v error -i "{wav}" -af "apad=whole_dur={hold:.3f}" -ar 44100 -ac 1 "{pw}"')
            f.write(f"file '{pw}'\n")
    run(f'ffmpeg -y -v error -f concat -safe 0 -i "{alist}" -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 44100 -ac 2 -c:a aac -b:a 160k "{wd}/voice.m4a"')
    # video per scene with slow zoom
    vlist = os.path.join(wd, "video.txt")
    with open(vlist, "w") as vf:
        for si in range(len(reel["scenes"])):
            sp = [x for x in parts if x[0] == si]
            T = sum(x[3] for x in sp)
            lst = os.path.join(wd, f"scene{si:02d}.txt")
            with open(lst, "w") as f:
                for (_, png, _, hold) in sp:
                    f.write(f"file '{png}'\nduration {hold:.3f}\n")
                f.write(f"file '{sp[-1][1]}'\n")
            tmp = os.path.join(wd, f"scene{si:02d}.tmp.mp4"); fin = os.path.join(wd, f"scene{si:02d}.mp4")
            fade = f",fade=t=in:st=0:d=0.25" if si > 0 else ""
            run(f'ffmpeg -y -v error -f concat -safe 0 -i "{lst}" -vf "fps={FPS},scale=w=\'trunc(1080*(1+0.035*t/{T:.3f})/2)*2\':h=-2:eval=frame:flags=bicubic,crop=1080:1920,format=yuv420p{fade},trim=duration={T:.3f},setsar=1" '
                f'-c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -r {FPS} "{tmp}"')
            os.replace(tmp, fin)
            vf.write(f"file '{fin}'\n")
    run(f'ffmpeg -y -v error -f concat -safe 0 -i "{vlist}" -c copy "{wd}/video.mp4"')
    final = os.path.join(OUT, f"{reel['slug']}.mp4")
    run(f'ffmpeg -y -v error -i "{wd}/video.mp4" -i "{wd}/voice.m4a" -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart "{final}.tmp.mp4"')
    os.replace(final + ".tmp.mp4", final)
    print(reel["slug"], round(dur(final), 1), "s")

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    frames_only = "--frames" in sys.argv
    for r in REELS:
        if which in ("all", r["slug"]):
            build(r, frames_only)
