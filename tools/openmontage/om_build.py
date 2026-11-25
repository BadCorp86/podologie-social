"""Build HyperFrames (OpenMontage atelier) projects for the 4 kids reels."""
import os, sys, json, math, shutil, subprocess, re

ns = {"__name__": "om"}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "reels_build.py")).read(), ns)   # REELS, helpers, illustration funcs (no render)
G = ns["g_"]
B = ns
INK = G["INK"]; PAPER = G["PAPER"]; SAGE = G["SAGE"]; SAGE_L = G["SAGE_L"]; SAGE_M = G["SAGE_M"]
BLUE = G["BLUE"]; BLUE_L = G["BLUE_L"]; BLUE_D = G["BLUE_D"]; AMBER = G["AMBER"]; AMBER_D = G["AMBER_D"]
AMBER_L = G["AMBER_L"]; CORAL = G["CORAL"]; CORAL_L = G["CORAL_L"]; SKIN = G["SKIN"]; SW = G["SW"]
toe = G["toe"]; g = G["g"]; stars = G["stars"]; lbl = G["lbl"]; leader = G["leader"]; arrow = G["arrow"]
glucose = G["glucose"]; ikey = G["ikey"]; cell = G["cell"]; pancreas = G["pancreas"]; immune = G["immune"]
bubble = G["bubble"]; check_badge = G["check_badge"]; icon = G["icon"]; IC = G["IC"]; rbc = G["rbc"]
FOOT = G["FOOT"]; SHOE = G["SHOE"]; ILL = B["ILL"]; REELS = B["REELS"]

OUT = "/home/claude/om/projects"
REELDIR = "/home/claude/reels"

def dur(p):
    return float(subprocess.run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"', shell=True,
                                capture_output=True, text=True).stdout.strip())

def grp(i, body, extra=""):
    return f'<g id="{i}" {extra}>{body}</g>'

class TL:
    def __init__(self): self.lines = []
    def add(self, m, sel, vars_, t):
        self.lines.append(f'tl.{m}("{sel}", {vars_}, {t:.3f});')
    def frm(self, sel, vars_, t): self.add("from", sel, vars_, t)
    def to(self, sel, vars_, t): self.add("to", sel, vars_, t)
    def fromto(self, sel, a, b, t): self.lines.append(f'tl.fromTo("{sel}", {a}, {b}, {t:.3f});')

POP = '{scale:0, opacity:0, transformOrigin:"50% 50%", duration:0.45, ease:"back.out(2.2)"}'
FADEUP = '{y:40, opacity:0, duration:0.45, ease:"power3.out"}'

def svg(w, h, body):
    return f'<svg viewBox="0 0 {w} {h}" width="100%" aria-hidden="true" style="display:block;overflow:visible">{body}</svg>'

# -------- scene builders: return (svg_markup, w, h, bg) and add tweens ---------
def sc_a1(p, tl, cue):
    L = grp(f"{p}L", g(toe("roundcut", 2), 90, 40, 1.0))
    glow = grp(f"{p}glow", f'<ellipse cx="312" cy="215" rx="78" ry="130" fill="{CORAL}" opacity=".35"/>')
    st = grp(f"{p}st", stars(370, 120, 1.1))
    bx = grp(f"{p}bx", check_badge(110, 60, 34, False))
    div = grp(f"{p}div", f'<path d="M450,30 L450,440" stroke="{INK}" stroke-width="3" stroke-dasharray="4 14" stroke-linecap="round" opacity=".5"/>')
    R = grp(f"{p}R", g(toe("straight"), 550, 40, 1.0))
    bc = grp(f"{p}bc", check_badge(570, 60, 34, True))
    l1 = grp(f"{p}l1", lbl(220, 478, "Rund geschnitten", 32, weight=700))
    l2 = grp(f"{p}l2", lbl(680, 478, "Gerade geschnitten", 32, weight=700))
    tl.frm(f"#{p}L", '{x:-520, opacity:0, duration:0.7, ease:"power3.out"}', cue(0, 0) + 0.1)
    tl.frm(f"#{p}l1", FADEUP, cue(0, 0.3))
    tl.frm(f"#{p}glow", '{opacity:0, duration:0.3}', cue(0, 0.6))
    tl.to(f"#{p}glow", '{opacity:0.05, duration:0.35, yoyo:true, repeat:5, ease:"sine.inOut"}', cue(0, 0.6) + 0.3)
    tl.frm(f"#{p}st", POP, cue(1, 0))
    tl.frm(f"#{p}bx", POP, cue(1, 0.1))
    tl.to(f"#{p}L", '{rotation:-3, transformOrigin:"50% 100%", duration:0.08, yoyo:true, repeat:5}', cue(1, 0.05))
    tl.frm(f"#{p}div", '{opacity:0, duration:0.3}', cue(2, 0))
    tl.frm(f"#{p}R", '{x:520, opacity:0, duration:0.7, ease:"power3.out"}', cue(2, 0))
    tl.frm(f"#{p}l2", FADEUP, cue(2, 0.3))
    tl.frm(f"#{p}bc", POP, cue(2, 0.45))
    return L + glow + st + bx + div + R + bc + l1 + l2, 900, 500, BLUE_L

def sc_a2(p, tl, cue):
    out = ""
    labels = ["rot", "entzündet", "wildes Fleisch"]
    times = [cue(0, 0), cue(0, 0.5), cue(1, 0)]
    for i, n in enumerate([1, 2, 3]):
        body = g(toe("straight", n), 20 + i*300, 30, 0.9) + (stars(250 + i*300, 70, 0.8) if n >= 2 else "") \
               + lbl(137 + i*300, 420, labels[i], 34, weight=700)
        out += grp(f"{p}t{i}", body)
        tl.frm(f"#{p}t{i}", '{y:80, scale:0.7, opacity:0, transformOrigin:"50% 100%", duration:0.55, ease:"back.out(1.8)"}', times[i])
    return out, 900, 450, "#FFFFFF"

def sc_a3(p, tl, cue):
    t1 = grp(f"{p}t1", g(toe("straight", 1), 90, 40, 1.0))
    tamp = grp(f"{p}tamp", g(f'<path d="M196,120 L214,128 L214,190 L198,196 Z" fill="#FFFFFF" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>', 90, 40, 1.0))
    t2 = grp(f"{p}t2", g(toe("straight"), 550, 40, 1.0))
    brace = grp(f"{p}brace", g(f'<path d="M52,164 C56,150 66,150 72,156 L188,156 C194,150 204,150 208,164" fill="none" stroke="{BLUE}" stroke-width="10" stroke-linecap="round"/>', 550, 40, 1.0))
    la = grp(f"{p}la", leader(300, 160, 380, 120) + lbl(390, 112, "Polster", 30, "start", weight=700))
    lb = grp(f"{p}lb", leader(760, 196, 820, 470) + lbl(800, 505, "Spange", 30, "middle", weight=700))
    tl.frm(f"#{p}t1", '{y:120, opacity:0, duration:0.6, ease:"power3.out"}', cue(0, 0) + 0.1)
    tl.frm(f"#{p}t2", '{y:120, opacity:0, duration:0.6, ease:"power3.out"}', cue(0, 0) + 0.3)
    tl.frm(f"#{p}tamp", '{x:90, opacity:0, duration:0.6, ease:"power2.out"}', cue(1, 0.05))
    tl.frm(f"#{p}la", '{opacity:0, duration:0.4}', cue(1, 0.2))
    tl.frm(f"#{p}brace", '{scaleX:0, transformOrigin:"50% 50%", opacity:0, duration:0.6, ease:"back.out(1.6)"}', cue(1, 0.45))
    tl.frm(f"#{p}lb", '{opacity:0, duration:0.4}', cue(1, 0.55))
    return t1 + tamp + t2 + brace + la + lb, 900, 540, BLUE_L

def sc_warn(p, tl, cue):
    ic = grp(f"{p}ic", f'<g transform="translate(320,40) scale(10.8)" fill="none" stroke="#A93A22" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{IC["alert"]}</g>')
    tx = grp(f"{p}tx", f'<text x="450" y="400" text-anchor="middle" style="font-family:Kalam;font-weight:700;font-size:72px" fill="{INK}">Erst zum Arzt</text>')
    tl.frm(f"#{p}ic", POP, cue(0, 0))
    tl.to(f"#{p}ic", '{rotation:8, transformOrigin:"50% 80%", duration:0.09, yoyo:true, repeat:7, ease:"sine.inOut"}', cue(0, 0) + 0.5)
    tl.frm(f"#{p}tx", FADEUP, cue(0, 0.3))
    return ic + tx, 900, 440, CORAL_L

def sc_b1(p, tl, cue):
    foot = grp(f"{p}foot", FOOT)
    cal = grp(f"{p}cal", f'<ellipse cx="764" cy="346" rx="54" ry="34" fill="{CORAL}" opacity=".25"/><path d="M732,340 C748,326 784,326 800,344" fill="none" stroke="#C9A85E" stroke-width="12" stroke-linecap="round"/>')
    shoe = grp(f"{p}shoe", SHOE)
    ars = "".join(grp(f"{p}ar{i}", a) for i, a in enumerate([arrow(764, 210, 764, 300), arrow(690, 228, 724, 304), arrow(840, 236, 808, 308)]))
    bub = grp(f"{p}bub", bubble(60, 40, 400, ["Jeden Tag", "dieselbe Stelle …"], (420, 210)))
    tl.frm(f"#{p}foot", '{opacity:0, y:30, duration:0.5}', cue(0, 0))
    tl.frm(f"#{p}shoe", '{opacity:0, y:-60, duration:0.6, ease:"bounce.out"}', cue(0, 0.15))
    for i in range(3):
        tl.frm(f"#{p}ar{i}", '{y:-70, opacity:0, duration:0.35, ease:"power2.in"}', cue(0, 0.35) + i*0.12)
        tl.to(f"#{p}ar{i}", '{y:-22, duration:0.3, yoyo:true, repeat:5, ease:"sine.inOut"}', cue(0, 0.35) + 0.5 + i*0.12)
    tl.frm(f"#{p}bub", POP, cue(0, 0.5))
    tl.frm(f"#{p}cal", '{scale:0, transformOrigin:"50% 50%", duration:0.6, ease:"back.out(2.5)"}', cue(1, 0.1))
    return foot + cal + shoe + ars + bub, 900, 560, SAGE_L

def sc_b2(p, tl, cue):
    full = G["b2"]
    # split: everything except cone/labels/stars as base; rebuild cone, nerve flash, labels separately
    base_parts = full.split(f'<path d="M318,104')[0]
    cone = grp(f"{p}cone", f'<path d="M318,104' + full.split(f'<path d="M318,104')[1].split(G["stars"](500, 360, 0.9))[0])
    st = grp(f"{p}st", stars(500, 360, 0.9) + stars(370, 370, 0.7))
    nerveflash = grp(f"{p}nf", f'<path d="M60,300 C150,330 250,290 340,318 C380,330 400,350 450,352 C500,350 520,330 560,318 C650,290 750,330 860,300" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>')
    labels = grp(f"{p}lab", leader(160, 150, 160, 70) + lbl(120, 58, "Hornhaut", 28, "start", weight=700)
                 + leader(600, 150, 680, 70) + lbl(700, 58, "Kern (Dorn)", 28, "start", weight=700)
                 + leader(800, 312, 800, 352) + lbl(800, 384, "Nerv", 28, weight=700)
                 + leader(120, 498, 120, 545) + lbl(120, 578, "Knochen", 28, weight=700))
    tl.frm(f"#{p}base", '{opacity:0, duration:0.4}', cue(0, 0))
    tl.frm(f"#{p}cone", '{scaleY:0.08, transformOrigin:"50% 0%", duration:1.6, ease:"power2.inOut"}', cue(0, 0.25))
    tl.frm(f"#{p}lab", '{opacity:0, duration:0.5}', cue(1, 0))
    tl.frm(f"#{p}nf", '{opacity:0, duration:0.2}', cue(2, 0.15))
    tl.to(f"#{p}nf", '{opacity:0.2, duration:0.25, yoyo:true, repeat:7}', cue(2, 0.15) + 0.2)
    tl.frm(f"#{p}st", POP, cue(2, 0.25))
    return grp(f"{p}base", base_parts) + nerveflash + cone + st + labels, 900, 600, "#FFFFFF"

def sc_b3(p, tl, cue):
    blade = grp(f"{p}blade", g(f'<rect x="0" y="40" width="210" height="80" rx="10" fill="#D6DCDD" stroke="{INK}" stroke-width="{SW}"/><circle cx="70" cy="80" r="12" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><rect x="100" y="70" width="70" height="20" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>', 560, 60, 1.0))
    x = grp(f"{p}x", f'<path d="M560,40 L790,200 M790,40 L560,200" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>')
    lb2 = grp(f"{p}lb2", lbl(675, 320, "Klinge", 30, weight=700))
    toeb = grp(f"{p}toe", g(f'<path d="M0,240 C0,140 -6,70 24,36 C50,4 170,4 196,36 C226,70 220,140 220,240 Z" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}"/>', 130, 30, 1.0))
    cal = grp(f"{p}cal", g(f'<path d="M80,60 C90,50 130,50 140,60" fill="none" stroke="#C9A85E" stroke-width="10" stroke-linecap="round"/>', 130, 30, 1.0))
    ring = grp(f"{p}ring", g(f'<ellipse cx="110" cy="150" rx="128" ry="44" fill="#CFE3E7" fill-opacity=".85" stroke="{INK}" stroke-width="{SW}"/><ellipse cx="110" cy="150" rx="60" ry="18" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>', 130, 30, 1.0))
    lb1 = grp(f"{p}lb1", lbl(240, 320, "Weicher Schutz", 30, weight=700))
    tl.frm(f"#{p}blade", '{opacity:0, x:60, duration:0.4}', cue(0, 0))
    tl.frm(f"#{p}lb2", '{opacity:0, duration:0.3}', cue(0, 0.1))
    tl.frm(f"#{p}x", '{scale:0, transformOrigin:"50% 50%", duration:0.4, ease:"back.out(3)"}', cue(0, 0.45))
    tl.frm(f"#{p}toe", '{opacity:0, y:60, duration:0.5}', cue(1, 0))
    tl.frm(f"#{p}cal", '{opacity:0, duration:0.3}', cue(1, 0))
    tl.to(f"#{p}cal", '{opacity:0, scale:0.2, transformOrigin:"50% 50%", duration:0.6}', cue(1, 0.7))
    tl.frm(f"#{p}ring", '{y:-160, opacity:0, duration:0.7, ease:"bounce.out"}', cue(2, 0.1))
    tl.frm(f"#{p}lb1", '{opacity:0, duration:0.3}', cue(2, 0.4))
    return toeb + cal + ring + lb1 + blade + x + lb2, 900, 340, SAGE_L

def plate():
    return (f'<ellipse cx="170" cy="250" rx="150" ry="52" fill="#FFFFFF" stroke="{INK}" stroke-width="{SW}"/><ellipse cx="170" cy="244" rx="104" ry="32" fill="none" stroke="#C9D2CF" stroke-width="3"/>'
            f'<path d="M96,236 C92,186 120,166 150,170 C176,162 214,170 214,206 L214,240 Z" fill="#E4B877" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<circle cx="236" cy="216" r="30" fill="#E86A4F" stroke="{INK}" stroke-width="3.5"/><path d="M236,186 C240,174 248,170 256,170" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')

def vessel_empty(x, y, w, h):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#F7DCD3" stroke="{INK}" stroke-width="{SW}"/>'
    o += f'<rect x="{x+14}" y="{y+14}" width="{w-28}" height="{h-28}" rx="{(h-28)/2}" fill="#FCEDE8" stroke="#E7A897" stroke-width="3"/>'
    for i in range(4):
        o += rbc(x + 60 + i*(w-120)/3, y + h*0.30 + (i % 2)*h*0.42, 20)
    return o

def sc_c1(p, tl, cue):
    pl = grp(f"{p}pl", plate() + lbl(170, 360, "Essen", 30, weight=700))
    ar = grp(f"{p}ar", arrow(250, 330, 470, 400, INK, 6, (330, 430)))
    ve = grp(f"{p}ve", vessel_empty(430, 300, 450, 200) + lbl(655, 548, "Blut", 30, weight=700))
    gl = ""
    for i, (x, y) in enumerate([(530, 400), (620, 360), (700, 420), (790, 380)]):
        gl += grp(f"{p}g{i}", glucose(x, y, 26))
    bub = grp(f"{p}bub", bubble(470, 40, 400, ["Wir wollen", "in die Zellen!"], (640, 330)))
    tl.frm(f"#{p}pl", POP, cue(0, 0))
    tl.frm(f"#{p}ve", '{opacity:0, x:80, duration:0.5}', cue(0, 0.2))
    tl.frm(f"#{p}ar", '{scale:0, opacity:0, transformOrigin:"0% 0%", duration:0.5}', cue(0, 0.5))
    for i in range(4):
        tl.frm(f"#{p}g{i}", '{x:-260, y:-60, scale:0.2, opacity:0, transformOrigin:"50% 50%", duration:0.6, ease:"power2.out"}', cue(1, 0) + i*0.18)
        tl.to(f"#{p}g{i}", '{x:18, duration:0.6, yoyo:true, repeat:5, ease:"sine.inOut"}', cue(1, 0) + 0.7 + i*0.1)
    tl.frm(f"#{p}bub", POP, cue(1, 0.45))
    return pl + ve + ar + gl + bub, 900, 570, AMBER_L

def sc_c3e(p, tl, cue):
    cb, door, rec = cell(560, 300, 250, open_=True, key_in=False)
    c = grp(f"{p}cell", cb)
    gl = "".join(grp(f"{p}g{i}", glucose(x, y, 28)) for i, (x, y) in enumerate([(470, 230), (540, 420), (640, 260)]))
    zap = grp(f"{p}zap", f'<g transform="translate(110,120) scale(7)" fill="{AMBER}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round">{IC["zap"]}</g>')
    tl.frm(f"#{p}cell", '{scale:0.6, opacity:0, transformOrigin:"50% 50%", duration:0.6, ease:"back.out(1.6)"}', cue(0, 0))
    for i in range(3):
        tl.frm(f"#{p}g{i}", '{x:-420, opacity:0, duration:0.7, ease:"power2.out"}', cue(0, 0.3) + i*0.2)
    tl.frm(f"#{p}zap", POP, cue(0, 0.75))
    tl.to(f"#{p}zap", '{scale:1.15, transformOrigin:"50% 50%", duration:0.3, yoyo:true, repeat:7, ease:"sine.inOut"}', cue(1, 0))
    tl.to(f"#{p}cell", '{scale:1.03, transformOrigin:"50% 50%", duration:0.4, yoyo:true, repeat:5, ease:"sine.inOut"}', cue(1, 0))
    return c + gl + zap, 900, 580, SAGE_L

def sc_c2(p, tl, cue):
    cb, door, rec = cell(720, 170, 140, open_=False, key_in=False)
    c = grp(f"{p}cell", cb)
    pan = grp(f"{p}pan", pancreas(10, 330, 0.8) + lbl(260, 560, "Bauchspeicheldrüse", 30, weight=700))
    keys = "".join(grp(f"{p}k{i}", ikey(x, y, 0.9, r)) for i, (x, y, r) in enumerate([(420, 260, -20), (500, 330, 10), (360, 200, -35)]))
    kl = grp(f"{p}kl", lbl(700, 420, "Insulin", 40, weight=800, color=BLUE_D))
    tl.frm(f"#{p}cell", POP, cue(0, 0))
    tl.to(f"#{p}cell", '{x:8, duration:0.07, yoyo:true, repeat:7}', cue(0, 0.55))
    tl.frm(f"#{p}pan", '{opacity:0, y:60, duration:0.5}', cue(1, 0))
    for i in range(3):
        tl.frm(f"#{p}k{i}", '{x:-150, y:150, scale:0, opacity:0, transformOrigin:"50% 50%", duration:0.7, ease:"back.out(1.7)"}', cue(1, 0.35) + i*0.2)
    tl.frm(f"#{p}kl", FADEUP, cue(1, 0.7))
    tl.to(f"#{p}pan", '{scale:1.05, transformOrigin:"30% 70%", duration:0.35, yoyo:true, repeat:3, ease:"sine.inOut"}', cue(2, 0.1))
    return c + pan + keys + kl, 900, 580, BLUE_L

def sc_c3k(p, tl, cue):
    cx, cy, r = 600, 300, 250
    cb, door, rec = cell(cx, cy, r, open_=True, key_in=False)
    ax = math.radians(200)
    kx, ky = cx + (r+58)*math.cos(ax), cy + (r+58)*math.sin(ax)
    at = math.radians(160)
    closed = f'<g transform="translate({door[0]},{door[1]}) rotate({math.degrees(at)+90})"><rect x="-32" y="-22" width="64" height="44" rx="8" fill="{SAGE}" stroke="{INK}" stroke-width="3.5"/></g>'
    c = grp(f"{p}cell", cb)
    dc = grp(f"{p}dc", closed)
    key = grp(f"{p}key", ikey(kx, ky, 0.9, 0))
    gin = "".join(grp(f"{p}g{i}", glucose(door[0] + 60 + i*40, door[1] + 20 - i*30, 26)) for i in range(2))
    gout = grp(f"{p}go", glucose(140, 430, 28) + glucose(210, 480, 28))
    bub = grp(f"{p}bub", bubble(560, 20, 330, ["Jetzt habe", "ich Energie!"], (660, 150)))
    lab = grp(f"{p}lab", leader(rec[0] - 50, rec[1] - 30, 120, 80) + lbl(60, 70, "Schloss", 30, "start", weight=700)
              + leader(door[0] - 30, door[1] + 50, 110, 300) + lbl(50, 290, "Tür", 30, "start", weight=700))
    tl.frm(f"#{p}cell", '{opacity:0, duration:0.4}', cue(0, 0))
    tl.frm(f"#{p}lab", '{opacity:0, duration:0.4}', cue(0, 0.1))
    tl.frm(f"#{p}go", '{opacity:0, duration:0.4}', cue(0, 0.1))
    tl.frm(f"#{p}key", '{x:-320, y:-140, rotation:-40, opacity:0, transformOrigin:"50% 50%", duration:0.9, ease:"power3.inOut"}', cue(0, 0.15))
    tl.to(f"#{p}key", '{rotation:25, transformOrigin:"0% 50%", duration:0.25, ease:"power2.out"}', cue(0, 0.62))
    tl.to(f"#{p}dc", '{scaleY:0, opacity:0, transformOrigin:"50% 50%", duration:0.35}', cue(0, 0.75))
    tl.to(f"#{p}go", '{x:150, y:-120, opacity:0, duration:0.9, ease:"power2.in"}', cue(1, 0))
    for i in range(2):
        tl.frm(f"#{p}g{i}", '{x:-120, opacity:0, duration:0.6}', cue(1, 0.25) + i*0.2)
    tl.frm(f"#{p}bub", POP, cue(1, 0.55))
    return c + dc + key + gout + gin + lab + bub, 900, 580, SAGE_L

def sc_c4(p, tl, cue):
    cb, door, rec = cell(620, 300, 240, open_=False, dull=True, key_in=False)
    c = grp(f"{p}cell", cb)
    pts = [(110, 330), (180, 380), (250, 330), (130, 440), (210, 470), (290, 420), (90, 530), (180, 540), (300, 520)]
    crowd = "".join(grp(f"{p}g{i}", glucose(x, y, 28, True, "worry")) for i, (x, y) in enumerate(pts))
    gauge_bg = (f'<path d="M40,170 A110,110 0 0 1 260,170" fill="none" stroke="#DDE3E1" stroke-width="26" stroke-linecap="round"/>'
                f'<path d="M40,170 A110,110 0 0 1 150,60" fill="none" stroke="{SAGE_M}" stroke-width="26" stroke-linecap="round"/>'
                f'<path d="M150,60 A110,110 0 0 1 260,170" fill="none" stroke="{CORAL}" stroke-width="26" stroke-linecap="round"/>')
    gauge = grp(f"{p}gauge", g(gauge_bg + f'<circle cx="150" cy="170" r="14" fill="{INK}"/>', 30, 20, 0.85) + lbl(158, 205, "Blutzucker", 28, weight=700))
    needle = grp(f"{p}needle", g(f'<path d="M150,170 L232,96" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>', 30, 20, 0.85))
    bub = grp(f"{p}bub", bubble(560, 20, 320, ["Die Tür", "bleibt zu."], (640, 120)))
    tl.frm(f"#{p}cell", '{opacity:0, duration:0.4}', cue(0, 0))
    tl.frm(f"#{p}gauge", '{opacity:0, duration:0.4}', cue(0, 0.1))
    tl.frm(f"#{p}needle", '{rotation:-130, svgOrigin:"157.5 164.5", duration:1.4, ease:"power2.inOut"}', cue(0, 0.2))
    for i in range(len(pts)):
        tl.frm(f"#{p}g{i}", '{x:-200, opacity:0, duration:0.5}', cue(0, 0.1) + i*0.07)
        tl.to(f"#{p}g{i}", f'{{y:{-10 - (i % 3)*4}, duration:{0.3 + (i % 4)*0.05:.2f}, yoyo:true, repeat:7, ease:"sine.inOut"}}', cue(1, 0) + i*0.03)
    tl.frm(f"#{p}bub", POP, cue(1, 0.2))
    return c + gauge + needle + crowd + bub, 900, 580, "#EEF0EC"

def sc_d1a(p, tl, cue):
    base = grp(f"{p}pan", pancreas(130, 40, 1.0))
    hurt = grp(f"{p}hurt", pancreas(130, 40, 1.0, attacked=True))
    ims = "".join(grp(f"{p}i{i}", immune(x, y, s)) for i, (x, y, s) in enumerate([(380, 70, 1), (520, 150, 0.9), (250, 215, 0.85)]))
    bub = grp(f"{p}bub", bubble(600, 170, 280, ["Kein Insulin", "mehr da."], (560, 120), 32))
    tl.frm(f"#{p}pan", '{opacity:0, duration:0.4}', cue(0, 0))
    for i, (dx, dy) in enumerate([(-300, -100), (300, -60), (-200, 200)]):
        tl.frm(f"#{p}i{i}", f'{{x:{dx}, y:{dy}, opacity:0, duration:0.8, ease:"power2.out"}}', cue(0, 0.1) + i*0.15)
    tl.frm(f"#{p}hurt", '{opacity:0, duration:0.5}', cue(0, 0.55))
    tl.frm(f"#{p}bub", POP, cue(0, 0.7))
    return base + hurt + ims + bub, 900, 340, BLUE_L

def sc_d1b(p, tl, cue):
    cb, dr, rc = cell(660, 190, 150, open_=False, dull=False, rusty=True, key_in=False)
    ax = math.radians(200)
    kx, ky = 660 + (150+58)*math.cos(ax), 190 + (150+58)*math.sin(ax)
    c = grp(f"{p}cell", cb)
    key = grp(f"{p}key", ikey(kx, ky, 0.9, 0))
    gl = "".join(grp(f"{p}g{i}", glucose(x, y, 26, True, "worry")) for i, (x, y) in enumerate([(140, 300), (210, 330), (100, 330)]))
    jam = grp(f"{p}jam", f'<path d="M{rc[0]-90},{rc[1]-80} l16,10 l-16,10 M{rc[0]-40},{rc[1]-110} l6,18 l-18,-2" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    bub = grp(f"{p}bub", bubble(30, 20, 330, ["Schlüssel da,", "Schloss klemmt."], (300, 140), 32))
    tl.frm(f"#{p}cell", '{opacity:0, duration:0.4}', cue(0, 0))
    tl.frm(f"#{p}key", '{x:-200, opacity:0, duration:0.6, ease:"power2.out"}', cue(0, 0.15))
    tl.to(f"#{p}key", '{rotation:10, transformOrigin:"0% 50%", duration:0.1, yoyo:true, repeat:9}', cue(0, 0.5))
    tl.frm(f"#{p}jam", POP, cue(0, 0.55))
    for i in range(3):
        tl.frm(f"#{p}g{i}", '{y:40, opacity:0, duration:0.4}', cue(0, 0.3) + i*0.1)
    tl.frm(f"#{p}bub", POP, cue(0, 0.65))
    return c + key + gl + jam + bub, 900, 380, SAGE_L

def sc_e1(p, tl, cue):
    foot = grp(f"{p}foot", FOOT + f'<path d="M240,10 C236,120 250,220 320,290 C420,360 560,400 640,410" fill="none" stroke="#E2A82A" stroke-width="9" stroke-linecap="round"/>')
    nerve_end = grp(f"{p}ne", f'<path d="M650,412 C700,416 740,412 780,404" fill="none" stroke="#E2A82A" stroke-width="9" stroke-linecap="round"/>')
    shoe = grp(f"{p}shoe", SHOE)
    stone = grp(f"{p}stone", f'<path d="M600,486 C604,470 624,462 642,466 C660,470 668,484 660,494 L606,496 Z" fill="#8E928A" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    wound = grp(f"{p}wound", f'<ellipse cx="630" cy="470" rx="22" ry="7" fill="{CORAL}" stroke="{INK}" stroke-width="2.5"/>')
    b1 = grp(f"{p}b1", bubble(560, 60, 320, ["Hier drückt", "doch etwas …"], (632, 456), 32))
    b2 = grp(f"{p}b2", bubble(40, 120, 230, ["Ich spüre", "nichts."], (180, 330), 32))
    lab = grp(f"{p}lab", leader(290, 250, 380, 190) + lbl(390, 188, "Nerv", 28, "start", weight=700))
    n = cue.n
    tl.frm(f"#{p}foot", '{opacity:0, duration:0.4}', cue(0, 0))
    tl.frm(f"#{p}shoe", '{opacity:0, duration:0.4}', cue(0, 0))
    tl.frm(f"#{p}stone", '{y:-260, opacity:0, duration:0.7, ease:"bounce.out"}', cue(0, 0.35))
    if n >= 3:
        tl.frm(f"#{p}b1", POP, cue(1, 0))
        tl.frm(f"#{p}lab", '{opacity:0, duration:0.4}', cue(2, 0))
        tl.to(f"#{p}ne", '{opacity:0.12, duration:0.8}', cue(2, 0.4))
        tl.frm(f"#{p}b2", POP, cue(3, 0))
        tl.frm(f"#{p}wound", POP, cue(3, 0.55))
        tl.to(f"#{p}b1", '{opacity:0, duration:0.3}', cue(3, 0))
    else:
        tl.frm(f"#{p}lab", '{opacity:0, duration:0.4}', cue(0, 0.3))
        tl.to(f"#{p}ne", '{opacity:0.12, duration:0.8}', cue(0, 0.45))
        tl.frm(f"#{p}b2", POP, cue(0, 0.6))
        tl.set_hidden = True
        tl.to(f"#{p}b1", '{opacity:0, duration:0.01}', cue(0, 0))
        tl.to(f"#{p}wound", '{opacity:0, duration:0.01}', cue(0, 0))
    return foot + nerve_end + shoe + stone + wound + lab + b1 + b2, 900, 560, CORAL_L

def trio(p, tl, cue, items, col, bg):
    out = ""
    for i, (ic, t) in enumerate(items):
        x = 150 + i*300
        body = (f'<circle cx="{x}" cy="190" r="110" fill="{bg}" stroke="{INK}" stroke-width="5"/>'
                f'<g transform="translate({x-60},130) scale(5)" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{IC[ic]}</g>'
                + lbl(x, 370, t, 36, weight=700))
        out += grp(f"{p}i{i}", body)
    return out

def sc_e2(p, tl, cue):
    out = trio(p, tl, cue, [("eye", "Anschauen"), ("search", "Prüfen"), ("hand", "Abtasten")], "#A93A22", CORAL_L)
    for i, t in enumerate([cue(0, 0), cue(0, 0.45), cue(1, 0.2)]):
        tl.frm(f"#{p}i{i}", POP, t)
    return out, 900, 400, "#FFFFFF"

def sc_e3(p, tl, cue):
    out = trio(p, tl, cue, [("steth", "Arzt"), ("users", "zusammen"), ("shield", "Podologe")], BLUE_D, BLUE_L)
    for i, t in enumerate([cue(0, 0), cue(1, 0.3), cue(0, 0.5)]):
        tl.frm(f"#{p}i{i}", POP, t)
    return out, 900, 400, "#FFFFFF"

SCENES = {"a1": sc_a1, "a2": sc_a2, "a3": sc_a3, "warn": sc_warn, "b1": sc_b1, "b2": sc_b2, "b3": sc_b3,
          "c1": sc_c1, "c2": sc_c2, "c3e": sc_c3e, "c3k": sc_c3k, "c4": sc_c4, "d1a": sc_d1a, "d1b": sc_d1b, "e1": sc_e1, "e2": sc_e2, "e3": sc_e3}

def end_card_html(p):
    return (f'<div id="{p}card" style="position:absolute;left:0;right:0;top:0;bottom:0;border-radius:24px;background:{INK};color:#fff;'
            f'display:flex;flex-direction:column;justify-content:center;gap:34px;padding:0 60px;box-sizing:border-box">'
            f'<div style="font-family:Kalam;font-weight:700;font-size:60px;line-height:1.1;color:#D3E3CD">Fragen zu deinen Füßen?</div>'
            f'<div style="font-family:Bricolage;font-weight:800;font-size:76px;line-height:1.05">02161 / 69 80 580</div>'
            f'<div style="font-family:Bricolage;font-weight:500;font-size:40px;line-height:1.35;color:#D9E4E1">WhatsApp 0152 / 264 12 617 oder wohlgefuehl-mg.de</div>'
            f'<div style="font-family:Bricolage;font-weight:700;font-size:36px;line-height:1.3;border-top:3px solid #4B6563;padding-top:26px">Podologie Praxis wohlGefühl bei S. Wilt, Eickener Str. 55, Mönchengladbach</div></div>')

class Cue:
    def __init__(self, cards): self.cards = cards; self.n = len(cards)
    def __call__(self, k, frac=0.0):
        if k >= self.n:
            k = self.n - 1; frac = max(frac, 0.5)
        s, d, h = self.cards[k]
        return s + frac * d

def words_html(cid, text):
    ws = text.split(" ")
    spans = "".join(f'<span id="{cid}w{i}" class="w">{w}</span> ' for i, w in enumerate(ws))
    return spans.strip(), ws

def build(reel):
    slug = reel["slug"]
    src = os.path.join(REELDIR, slug)
    proj = os.path.join(OUT, slug); hf = os.path.join(proj, "hyperframes")
    if os.path.exists(hf): shutil.rmtree(hf)
    os.makedirs(os.path.join(hf, "assets"), exist_ok=True)
    shutil.copy("/home/claude/om/gsap.min.js", os.path.join(hf, "assets", "gsap.min.js"))
    shutil.copy(os.path.expanduser("~/.fonts/Bricolage.ttf"), os.path.join(hf, "assets", "Bricolage.ttf"))
    shutil.copy(os.path.expanduser("~/.fonts/Kalam-Bold.ttf"), os.path.join(hf, "assets", "Kalam-Bold.ttf"))
    subprocess.run(f'ffmpeg -y -v error -i "{src}/voice.m4a" -ar 48000 -ac 2 "{hf}/assets/narration.wav"', shell=True, check=True)
    accent = reel["color"]
    # timing
    t = 0.0; scenes = []
    nsc = len(reel["scenes"])
    seen_c3 = False
    for si, sc in enumerate(reel["scenes"]):
        cards = []
        for ci, card in enumerate(sc["cards"]):
            shown = card[0] if isinstance(card, tuple) else card
            d = dur(os.path.join(src, f"s{si:02d}c{ci:02d}.wav"))
            last = ci == len(sc["cards"]) - 1
            hold = d + (0.55 if last else 0.25)
            if si == nsc - 1 and last: hold = d + 1.4
            cards.append((t, d, hold, shown))
            t += hold
        ill = sc["ill"]
        if ill == "c3":
            ill = "c3k" if seen_c3 else "c3e"; seen_c3 = True
        scenes.append((ill, cards))
    total = round(t, 3)
    tl = TL(); clips = []; caps = []
    for si, (ill, cards) in enumerate(scenes):
        p = f"s{si}"
        s0 = cards[0][0]; sdur = sum(c[2] for c in cards)
        cue = Cue([(c[0], c[1], c[2]) for c in cards])
        if ill == "end":
            inner = end_card_html(p)
            bg = INK
            tl.frm(f"#{p}panel", '{y:220, opacity:0, duration:0.6, ease:"power3.out"}', s0)
        else:
            body, w, h, bg = SCENES[ill](p, tl, cue)
            inner = f'<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;padding:28px;box-sizing:border-box">{svg(w, h, body)}</div>'
            tl.frm(f"#{p}panel", '{scale:0.92, opacity:0, transformOrigin:"50% 50%", duration:0.45, ease:"back.out(1.6)"}', s0)
        if si < nsc - 1:
            tl.to(f"#{p}panel", '{opacity:0, scale:0.97, transformOrigin:"50% 50%", duration:0.22}', s0 + sdur - 0.22)
        clips.append(f'<div id="{p}panel" class="clip panel" style="background:{bg}" data-start="{s0:.3f}" data-duration="{sdur:.3f}" data-track-index="{2 + si % 2}" data-layout-allow-overflow>{inner}</div>')
        if ill == "end": continue
        for ci, (cs, cd, ch, text) in enumerate(cards):
            cid = f"{p}c{ci}"
            spans, ws = words_html(cid, text)
            caps.append(f'<div id="{cid}" class="clip cap" data-start="{cs:.3f}" data-duration="{ch:.3f}" data-track-index="4"><div class="capbox">{spans}</div></div>')
            tl.frm(f"#{cid} .capbox", '{y:24, opacity:0, duration:0.25, ease:"power2.out"}', cs)
            weights = [len(w) + 2 for w in ws]; tot = sum(weights); acc = 0.0
            for wi, w in enumerate(ws):
                wt = cs + 0.05 + (acc / tot) * cd * 0.96
                acc += weights[wi]
                tl.to(f"#{cid}w{wi}", f'{{opacity:1, color:"{accent}", duration:0.1}}', wt)
                tl.to(f"#{cid}w{wi}", f'{{color:"{INK}", duration:0.2}}', wt + max(0.18, (weights[wi] / tot) * cd * 0.96))
    html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<title>{reel["title"]}</title>
<script src="assets/gsap.min.js"></script>
<style>
@font-face {{ font-family: Bricolage; src: url(assets/Bricolage.ttf); font-weight: 200 800; }}
@font-face {{ font-family: Kalam; src: url(assets/Kalam-Bold.ttf); font-weight: 700; }}
body {{ margin: 0; background: {PAPER}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: Bricolage, system-ui, sans-serif; color: {INK}; }}
#bg {{ position: absolute; inset: 0; background: {PAPER}; }}
#bgcircle {{ position: absolute; right: -200px; top: -200px; width: 620px; height: 620px; border-radius: 50%; background: {reel["tint"]}; opacity: .6; }}
#stripe {{ position: absolute; left: 0; top: 0; width: 1080px; height: 16px; background: {accent}; }}
#tag {{ position: absolute; left: 60px; top: 228px; font-weight: 700; font-size: 32px; color: {accent}; }}
#title {{ position: absolute; left: 60px; width: 880px; top: 276px; margin: 0; font-weight: 800; font-size: 68px; line-height: 1.02; letter-spacing: -1.5px; }}
.panel {{ position: absolute; left: 60px; top: 470px; width: 960px; height: 700px; border: 5px solid {INK}; border-radius: 28px; box-sizing: border-box; overflow: hidden; }}
.cap {{ position: absolute; left: 60px; top: 1205px; width: 840px; height: 260px; }}
.capbox {{ width: 100%; min-height: 230px; box-sizing: border-box; background: #FFFFFF; border: 5px solid {INK}; border-radius: 28px; padding: 26px 34px; display: flex; flex-wrap: wrap; align-items: center; justify-content: center; align-content: center; text-align: center; font-weight: 700; font-size: 54px; line-height: 1.18; column-gap: 0.25em; }}
.w {{ display: inline-block; opacity: .38; }}
#ki {{ position: absolute; left: 60px; top: 1502px; font-weight: 500; font-size: 24px; color: #5B6B6A; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{total}" data-fps="30">
<div id="base" class="clip" data-start="0" data-duration="{total}" data-track-index="0" data-layout-allow-overflow>
<div id="bg"></div><div id="bgcircle"></div><div id="stripe"></div>
<div id="tag">{reel["tag"]}</div>
<h1 id="title">{reel["title"]}</h1>
<div id="ki">Mit KI erstellt, KI-Stimme. Allgemeine Information, keine Diagnose.</div>
</div>
{"".join(clips)}
{"".join(caps)}
<audio id="narration" src="assets/narration.wav" data-start="0" data-duration="{total}" data-track-index="10" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
tl.from("#title", {{ y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }}, 0);
tl.from("#tag", {{ opacity: 0, duration: 0.4 }}, 0);
{chr(10).join(tl.lines)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
    open(os.path.join(hf, "index.html"), "w").write(html)
    json.dump({"project": slug, "runtime": "hyperframes", "composition_mode": "atelier", "duration": total,
               "decisions": [{"category": "render_runtime_selection", "subject": "Render runtime", "choice": "hyperframes",
                              "options_considered": ["hyperframes", "remotion", "ffmpeg"], "by": "Sergej 23.11.2026"},
                             {"category": "composition_mode", "subject": "Authoring mode", "choice": "atelier (assumed, user did not answer)"},
                             {"category": "voice_selection", "subject": "Narration TTS provider", "choice": "piper de_DE-thorsten-high"},
                             {"category": "music", "subject": "Background music", "choice": "none (pixabay unreachable, no keys)"}]},
              open(os.path.join(proj, "decision_log.json"), "w"), ensure_ascii=False, indent=1)
    return hf, total

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for r in REELS:
        r["tint"] = {AMBER_D: AMBER_L, SAGE: SAGE_L, BLUE: BLUE_L, CORAL: CORAL_L}[r["color"]]
        if which in ("all", r["slug"]):
            hf, total = build(r)
            print(r["slug"], hf, total)
