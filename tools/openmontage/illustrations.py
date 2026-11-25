import json, os, math

ROOT = "/home/claude/canvas/project"

INK = "#17302E"; PAPER = "#F3F6F4"
SKIN = "#F1CDB3"; SKIN_SH = "#E0AF91"; NAIL = "#FBF0EA"
SAGE = "#3D6B57"; SAGE_L = "#D3E3CD"; SAGE_M = "#A9C4A4"
BLUE = "#2E6FA3"; BLUE_L = "#D7E6F1"; BLUE_D = "#1F5582"
CORAL = "#D85C41"; CORAL_L = "#F6D3C8"
AMBER = "#F2B441"; AMBER_D = "#C98A12"; AMBER_L = "#F8E7BF"
GREY = "#5B6B6A"; LAV = "#B9B4D3"

HEAD = "font-family:'Bricolage Grotesque',system-ui,sans-serif"
HAND = "font-family:Kalam,'Comic Sans MS',cursive;font-weight:700"

SW = 4  # line weight

# ---------------- icons (stroke, 24 grid) ----------------
IC = {
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4M12 17h.01"/>',
 "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88M14.47 14.48 20 20M8.12 8.12 12 12"/>',
 "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
 "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
 "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
 "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
 "steth": '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "pill": '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
 "syringe": '<path d="m18 2 4 4M17 7l3-3M19 9 8.7 19.3a2.4 2.4 0 0 1-3.4 0l-.6-.6a2.4 2.4 0 0 1 0-3.4L15 5M9 11l4 4M5 19l-3 3M14 4l6 6"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 "hand": '<path d="M18 11V6a2 2 0 0 0-4 0M14 10V4a2 2 0 0 0-4 0v2M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/>',
 "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
 "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
 "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
}

def icon(name, color=INK, size=40):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[name]}</svg>')

# ---------------- drawing helpers ----------------
def g(body, x=0, y=0, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})">{body}</g>'

def stars(x, y, s=1.0, c=CORAL):
    out = ""
    for (dx, dy, r) in [(0, 0, 16), (30, -24, 11), (34, 18, 9)]:
        r *= s
        cx, cy = x + dx*s, y + dy*s
        out += f'<path d="M{cx},{cy-r} L{cx+r*0.28},{cy-r*0.28} L{cx+r},{cy} L{cx+r*0.28},{cy+r*0.28} L{cx},{cy+r} L{cx-r*0.28},{cy+r*0.28} L{cx-r},{cy} L{cx-r*0.28},{cy-r*0.28} Z" fill="{c}"/>'
    return out

def toe(nail="straight", inflam=0, tamp=False, brace=False):
    o = []
    if inflam:
        o.append(f'<ellipse cx="222" cy="175" rx="{40+inflam*12}" ry="{90+inflam*12}" fill="{CORAL}" opacity="{0.10+inflam*0.07}"/>')
    o.append(f'<path d="M0,380 C0,250 -8,120 30,60 C60,8 200,8 230,60 C268,120 260,250 260,380 Z" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    o.append(f'<path d="M218,380 C224,250 232,140 214,86 C244,132 250,250 247,380 Z" fill="{SKIN_SH}"/>')
    o.append(f'<path d="M38,300 C28,210 36,145 58,110" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity=".55"/>')
    o.append(f'<path d="M222,300 C232,210 224,145 202,110" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity=".55"/>')
    if inflam:
        w = 14 + inflam*10
        o.append(f'<path d="M198,104 C{230+w},140 {232+w},230 214,286 C226,226 220,160 198,104 Z" fill="{CORAL_L if inflam==1 else CORAL}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    if nail == "roundcut":
        o.append(f'<path d="M62,250 L62,142 C62,96 94,70 130,70 C166,70 198,96 198,142 L210,178 L198,250 C170,262 90,262 62,250 Z" fill="{NAIL}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
    else:
        o.append(f'<path d="M62,250 L62,104 C62,80 80,68 130,68 C180,68 198,80 198,104 L198,250 C170,262 90,262 62,250 Z" fill="{NAIL}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>')
        o.append(f'<path d="M68,90 L192,90" stroke="{INK}" stroke-width="2.5" opacity=".35"/>')
    o.append(f'<path d="M96,250 C102,226 158,226 164,250" fill="#FFFFFF" opacity=".75"/>')
    o.append(f'<rect x="82" y="112" width="12" height="96" rx="6" fill="#FFFFFF" opacity=".7"/>')
    if inflam >= 3:
        o.append(f'<circle cx="236" cy="128" r="18" fill="#B8442C" stroke="{INK}" stroke-width="3"/><circle cx="246" cy="160" r="14" fill="#B8442C" stroke="{INK}" stroke-width="3"/><circle cx="231" cy="124" r="5" fill="#fff" opacity=".6"/>')
    if tamp:
        o.append(f'<path d="M196,120 L214,128 L214,190 L198,196 Z" fill="#FFFFFF" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>')
    if brace:
        o.append(f'<path d="M52,164 C56,150 66,150 72,156 L188,156 C194,150 204,150 208,164" fill="none" stroke="{BLUE}" stroke-width="10" stroke-linecap="round"/>')
    return "".join(o)

def check_badge(cx, cy, r=34, ok=True):
    fill = SAGE if ok else CORAL
    mark = (f'<path d="M{cx-14},{cy+1} L{cx-4},{cy+12} L{cx+16},{cy-11}"' if ok else f'<path d="M{cx-11},{cy-11} L{cx+11},{cy+11} M{cx+11},{cy-11} L{cx-11},{cy+11}"')
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{SW}"/>{mark} fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'

def bubble(x, y, w, lines, tail=(0, 0), size=34, fill="#FFFFFF"):
    lh = size * 1.18
    h = len(lines) * lh + 34
    tx, ty = tail
    t = ""
    if tx or ty:
        bx = x + w*0.3
        t = f'<path d="M{bx},{y+h-4} L{tx},{ty} L{bx+46},{y+h-4} Z" fill="{fill}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/><path d="M{bx+3},{y+h-6} L{bx+43},{y+h-6}" stroke="{fill}" stroke-width="8"/>'
    txt = "".join(f'<tspan x="{x+w/2}" dy="{0 if i==0 else lh}">{l}</tspan>' for i, l in enumerate(lines))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(h/2, 44)}" fill="{fill}" stroke="{INK}" stroke-width="{SW}"/>{t}'
            f'<text x="{x+w/2}" y="{y+17+size*0.9}" text-anchor="middle" style="{HAND};font-size:{size}px" fill="{INK}">{txt}</text>')

def lbl(x, y, t, size=28, anchor="middle", color=INK, weight=600):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{HEAD};font-weight:{weight};font-size:{size}px" fill="{color}">{t}</text>'

def leader(x1, y1, x2, y2):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{INK}" stroke-width="2.5"/><circle cx="{x1}" cy="{y1}" r="6" fill="{INK}"/>'

def arrow(x1, y1, x2, y2, c=CORAL, w=7, curve=None):
    a = math.atan2(y2-y1, x2-x1)
    if curve:
        cx, cy = curve
        a = math.atan2(y2-cy, x2-cx)
        line = f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
    else:
        line = f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
    L = 24
    p1 = (x2 - L*math.cos(a-0.45), y2 - L*math.sin(a-0.45)); p2 = (x2 - L*math.cos(a+0.45), y2 - L*math.sin(a+0.45))
    return line + f'<path d="M{x2},{y2} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}" stroke="{c}" stroke-width="3" stroke-linejoin="round"/>'

def glucose(cx, cy, r=28, face=True, mood="ok"):
    pts = " ".join(f"{cx+r*math.cos(math.pi/3*i+math.pi/6):.1f},{cy+r*math.sin(math.pi/3*i+math.pi/6):.1f}" for i in range(6))
    o = f'<polygon points="{pts}" fill="{AMBER}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    o += f'<path d="M{cx-r*0.55},{cy-r*0.45} L{cx-r*0.1},{cy-r*0.72}" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
    if face:
        e = r*0.26
        o += f'<circle cx="{cx-e}" cy="{cy-2}" r="{r*0.09+1}" fill="{INK}"/><circle cx="{cx+e}" cy="{cy-2}" r="{r*0.09+1}" fill="{INK}"/>'
        if mood == "worry":
            o += f'<path d="M{cx-e},{cy+r*0.42} Q{cx},{cy+r*0.22} {cx+e},{cy+r*0.42}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        else:
            o += f'<path d="M{cx-e},{cy+r*0.25} Q{cx},{cy+r*0.48} {cx+e},{cy+r*0.25}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    return o

def ikey(x, y, s=1.0, rot=0, color=BLUE):
    body = (f'<circle cx="0" cy="0" r="20" fill="{color}" stroke="{INK}" stroke-width="3.5"/><circle cx="0" cy="0" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M18,-7 L74,-7 L74,7 L66,7 L66,19 L56,19 L56,7 L48,7 L48,15 L38,15 L38,7 L18,7 Z" fill="{color}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M-10,-10 L-4,-15" stroke="#fff" stroke-width="3.5" stroke-linecap="round" opacity=".7"/>')
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{body}</g>'

def rbc(cx, cy, r=22):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.72}" fill="#E07A62" stroke="{INK}" stroke-width="3"/><ellipse cx="{cx}" cy="{cy}" rx="{r*0.45}" ry="{r*0.28}" fill="#C85A44"/>'

def vessel(x, y, w, h, n_glu=5, glu_faces=True):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#F7DCD3" stroke="{INK}" stroke-width="{SW}"/>'
    o += f'<rect x="{x+14}" y="{y+14}" width="{w-28}" height="{h-28}" rx="{(h-28)/2}" fill="#FCEDE8" stroke="#E7A897" stroke-width="3"/>'
    import random
    random.seed(w + h + n_glu)
    for i in range(4):
        o += rbc(x + 60 + i*(w-120)/3, y + h*0.30 + (i % 2)*h*0.42, 20)
    for i in range(n_glu):
        o += glucose(x + 100 + i*(w-200)/max(1, n_glu-1), y + h*0.55 + (-1)**i * h*0.12, 24, glu_faces)
    return o

def cell(cx, cy, r, open_=True, dull=False, rusty=False, key_in=True):
    cyto = "#E4EBDC" if dull else SAGE_L
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cyto}" stroke="{INK}" stroke-width="{SW+1}"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r-16}" fill="none" stroke="{SAGE_M}" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>'
    # nucleus
    o += f'<circle cx="{cx+r*0.30}" cy="{cy+r*0.22}" r="{r*0.24}" fill="{"#C9D2C2" if dull else SAGE_M}" stroke="{INK}" stroke-width="3.5"/><circle cx="{cx+r*0.36}" cy="{cy+r*0.18}" r="{r*0.07}" fill="{INK}" opacity=".5"/>'
    # mitochondria
    for (mx, my, rot) in [(0.25, -0.38, -20), (-0.05, 0.45, 25)]:
        X, Y = cx + r*mx, cy + r*my
        o += f'<g transform="translate({X},{Y}) rotate({rot})"><ellipse cx="0" cy="0" rx="{r*0.18}" ry="{r*0.09}" fill="{"#D9D3C3" if dull else "#F2C46B"}" stroke="{INK}" stroke-width="3"/><path d="M{-r*0.12},0 q{r*0.03},{-r*0.06} {r*0.06},0 t{r*0.06},0 t{r*0.06},0" fill="none" stroke="{INK}" stroke-width="2.5"/></g>'
        if not dull:
            o += f'<path d="M{X+r*0.2},{Y-r*0.12} l14,-14 M{X+r*0.24},{Y} l20,0 M{X+r*0.2},{Y+r*0.12} l14,14" stroke="{AMBER_D}" stroke-width="4" stroke-linecap="round"/>'
    # receptor on membrane at angle 205deg, transporter at 160deg
    ax = math.radians(200)
    rx_, ry_ = cx + r*math.cos(ax), cy + r*math.sin(ax)
    rec = (f'<path d="M-16,30 L-16,0 L-34,-34 L-20,-40 L-4,-10 L4,-10 L20,-40 L34,-34 L16,0 L16,30 Z" fill="{"#B8C9D6" if rusty else BLUE_L}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    if rusty:
        rec += f'<circle cx="-22" cy="-30" r="5" fill="#B26A3A"/><circle cx="8" cy="12" r="4" fill="#B26A3A"/><circle cx="24" cy="-24" r="4" fill="#B26A3A"/>'
    o += f'<g transform="translate({rx_},{ry_}) rotate({math.degrees(ax)+90})">{rec}</g>'
    if key_in:
        kx, ky = cx + (r+58)*math.cos(ax), cy + (r+58)*math.sin(ax)
        o += ikey(kx, ky, 0.9, math.degrees(ax)+180 - 180 + 0, BLUE)
    # transporter (door)
    at = math.radians(160)
    tx, ty = cx + r*math.cos(at), cy + r*math.sin(at)
    if open_:
        door = f'<rect x="-30" y="-20" width="16" height="40" rx="5" fill="{SAGE}" stroke="{INK}" stroke-width="3.5"/><rect x="14" y="-20" width="16" height="40" rx="5" fill="{SAGE}" stroke="{INK}" stroke-width="3.5"/>'
    else:
        door = f'<rect x="-30" y="-20" width="60" height="40" rx="8" fill="{"#8A9A92" if dull else SAGE}" stroke="{INK}" stroke-width="3.5"/><path d="M0,-20 L0,20" stroke="{INK}" stroke-width="3"/>'
    o += f'<g transform="translate({tx},{ty}) rotate({math.degrees(at)+90})">{door}</g>'
    return o, (tx, ty), (rx_, ry_)

def pancreas(x, y, s=1.0, attacked=False, keys=True):
    o = (f'<path d="M0,110 C10,30 120,20 200,44 C300,70 420,40 520,18 C600,0 660,40 640,100 C622,150 540,150 460,146 C360,142 300,170 220,200 C100,244 -8,200 0,110 Z" fill="#EDB9A3" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
         f'<path d="M30,160 C120,200 210,180 300,150 C380,124 470,128 560,126" fill="none" stroke="#D9937A" stroke-width="5" stroke-linecap="round"/>')
    for (bx, by) in [(90, 80), (170, 120), (250, 90), (330, 110), (410, 80), (480, 100), (560, 70)]:
        o += f'<circle cx="{bx}" cy="{by}" r="9" fill="#E3A08A"/>'
    # islet
    o += f'<circle cx="300" cy="96" r="44" fill="{BLUE_L}" stroke="{INK}" stroke-width="3.5"/>'
    for (ix, iy) in [(-16, -14), (14, -16), (-18, 14), (16, 14), (0, 0)]:
        if attacked:
            o += f'<circle cx="{300+ix}" cy="{96+iy}" r="11" fill="#C9CED6" stroke="{INK}" stroke-width="2.5"/><path d="M{300+ix-6},{96+iy-6} l12,12" stroke="{CORAL}" stroke-width="3"/>'
        else:
            o += f'<circle cx="{300+ix}" cy="{96+iy}" r="11" fill="{BLUE}" stroke="{INK}" stroke-width="2.5"/>'
    return g(o, x, y, s)

def immune(cx, cy, s=1.0):
    o = (f'<path d="M-30,-6 C-40,-30 -14,-44 4,-34 C20,-48 46,-30 36,-8 C52,8 36,34 14,30 C4,46 -26,40 -26,20 C-46,14 -46,-2 -30,-6 Z" fill="{LAV}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
         f'<circle cx="2" cy="-2" r="12" fill="#8E86B5" stroke="{INK}" stroke-width="3"/>')
    return g(o, cx, cy, s)

def svg(w, h, body, alt):
    return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{alt}" style="display:block">{body}</svg>'

# foot side view + ghost shoe (viewBox 900x560)
FOOT = (f'<path d="M150,0 L330,0 C322,90 332,175 385,252 C470,292 560,330 650,344 C700,322 750,328 778,352 C805,374 828,392 830,420 C832,452 815,472 790,472 L70,472 C42,472 30,452 34,420 C40,340 70,270 120,240 C135,160 145,80 150,0 Z" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
        f'<path d="M60,452 L818,452 C812,466 802,472 790,472 L70,472 C62,472 58,462 60,452 Z" fill="{SKIN_SH}"/>'
        f'<path d="M150,0 C146,60 140,120 132,170" fill="none" stroke="{SKIN_SH}" stroke-width="16" stroke-linecap="round"/>'
        f'<path d="M700,350 C712,372 714,398 704,420" fill="none" stroke="{INK}" stroke-width="3" opacity=".45" stroke-linecap="round"/>')
SHOE = (f'<path d="M100,170 C170,160 330,186 404,232 C500,284 640,298 760,326 C836,344 868,392 868,446 L868,500 L18,500 L18,430 C18,330 54,222 100,170 Z" fill="#FFFFFF" fill-opacity=".38" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
        f'<path d="M14,500 L872,500 L872,520 C872,534 862,542 848,542 L36,542 C22,542 14,532 14,520 Z" fill="#2F4446" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
        f'<path d="M30,488 L860,488" stroke="{INK}" stroke-width="3" stroke-dasharray="10 10" opacity=".5"/>')

# ---------------- slide template ----------------
def caption_box(t):
    return (f'<div style="position:absolute;left:-4px;top:-4px;background:{AMBER_L};border:4px solid {INK};border-radius:0 0 16px 0;'
            f'padding:10px 22px 12px;{HAND};font-size:32px;line-height:1.1;color:{INK}">{t}</div>')

def panel_html(p):
    cap = caption_box(p["caption"]) if p.get("caption") else ""
    bg = p.get("bg", "#FFFFFF")
    return (f'<div style="position:relative;background:{bg};border:4px solid {INK};border-radius:14px;overflow:hidden;flex:{p.get("flex","1 1 0")};min-width:0;padding:{p.get("pad","64px 18px 14px")}">'
            f'{cap}{p["svg"]}{p.get("below","")}</div>')

def fact_rows(rows):
    out = ""
    for (ic, txt, tone) in rows:
        col = {"sage": SAGE, "blue": BLUE, "coral": CORAL, "amber": AMBER_D, "ink": INK}[tone]
        bgc = {"sage": SAGE_L, "blue": BLUE_L, "coral": CORAL_L, "amber": AMBER_L, "ink": "#E3E8E6"}[tone]
        out += (f'<div style="display:flex;align-items:center;gap:24px">'
                f'<div style="flex:0 0 72px;height:72px;border-radius:50%;background:{bgc};border:3px solid {INK};display:flex;align-items:center;justify-content:center">{icon(ic, col, 38)}</div>'
                f'<div style="{HEAD};font-weight:500;font-size:34px;line-height:1.28;color:{INK};text-wrap:pretty">{txt}</div></div>')
    return f'<div style="display:flex;flex-direction:column;gap:22px">{out}</div>'

def dots(n, total, col):
    d = "".join(f'<span style="width:{36 if i==n else 12}px;height:12px;border-radius:6px;background:{col if i==n else "#B9C4C1"};display:block"></span>' for i in range(total))
    return f'<div style="display:flex;gap:8px;align-items:center" aria-label="Folie {n+1} von {total}">{d}</div>'

def cta_band():
    return (f'<div style="display:flex;align-items:center;gap:26px;background:{INK};border-radius:18px;padding:24px 30px;color:#fff">'
            f'<div style="flex:0 0 68px;height:68px;border-radius:50%;background:{SAGE_M};display:flex;align-items:center;justify-content:center">{icon("phone", INK, 34)}</div>'
            f'<div style="{HEAD};font-size:30px;line-height:1.3"><div style="font-weight:700;font-size:36px">Termin: 02161 / 69 80 580</div>'
            f'<div style="font-weight:500;color:#D9E4E1">WhatsApp 0152 / 264 12 617 oder wohlgefuehl-mg.de</div></div></div>')

def question_bar(t, space):
    return (f'<div style="background:#FFFFFF;border:4px dashed {INK};border-radius:18px;padding:22px 28px;{HAND};font-size:38px;line-height:1.15;text-align:center;color:{INK}">{t}</div>'
            f'<div style="height:{space}px"></div>')

def slide(sp):
    col = sp["color"]
    blocks = []
    if sp.get("panels"):
        dirn = "row" if sp.get("row") else "column"
        blocks.append(f'<div style="display:flex;flex-direction:{dirn};gap:18px">' + "".join(panel_html(p) for p in sp["panels"]) + "</div>")
    if sp.get("extra"):
        blocks.append(sp["extra"])
    if sp.get("warn"):
        blocks.append(f'<div style="display:flex;align-items:center;gap:20px;background:{CORAL_L};border:3px solid {INK};border-radius:16px;padding:18px 26px">'
                      f'{icon("alert", "#A93A22", 40)}<div style="{HEAD};font-weight:600;font-size:31px;line-height:1.28;color:{INK}">{sp["warn"]}</div></div>')
    if sp.get("facts"):
        blocks.append(fact_rows(sp["facts"]))
    if sp.get("question"):
        blocks.append(question_bar(sp["question"], sp.get("qspace", 170)))
    if sp.get("cta"):
        blocks.append(cta_band())
    content = "\n".join(blocks)
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{sp["title"]}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800&amp;family=Kalam:wght@700&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:{BLUE}}}a:hover{{color:{INK}}}
</style>
</helmet>
<div style="width:1080px;height:1920px;box-sizing:border-box;position:relative;overflow:hidden;background:{PAPER};color:{INK}">
<div style="position:absolute;left:0;top:0;width:1080px;height:14px;background:{col}"></div>
<div style="position:absolute;right:-180px;top:-180px;width:560px;height:560px;border-radius:50%;background:{sp.get("tint", SAGE_L)};opacity:.55"></div>
<div style="position:relative;box-sizing:border-box;padding:226px 72px 0;display:flex;flex-direction:column;gap:30px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div style="{HEAD};font-weight:700;font-size:26px;color:{col}">{sp["tag"]}</div>
{dots(sp["n"], sp["total"], col)}
</div>
<h1 style="margin:0 0 6px;{HEAD};font-weight:800;font-size:{sp.get("hsize",86)}px;line-height:1.0;letter-spacing:-2px;color:{INK};text-wrap:balance">{sp["headline"]}</h1>
{content}
</div>
<div style="position:absolute;left:72px;right:72px;top:1628px;display:flex;justify-content:space-between;gap:24px;border-top:2px solid #B9C4C1;padding-top:14px;{HEAD};font-weight:500;font-size:20px;line-height:1.4;color:{GREY}">
<div><div style="font-weight:700;color:{INK}">Podologie Praxis wohlGefühl bei S. Wilt</div><div>Eickener Str. 55, 41061 Mönchengladbach</div></div>
<div style="text-align:right"><div>Allgemeine Information, keine Diagnose.</div><div>Mit KI erstellt</div></div>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":1920}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''

S = []
NAG = dict(tag="Eingewachsener Nagel", color=BLUE, tint=BLUE_L, total=3)
DRU = dict(tag="Druckstelle und Hühnerauge", color=SAGE, tint=SAGE_L, total=3)
INS = dict(tag="Diabetes einfach erklärt", color=AMBER_D, tint=AMBER_L, total=4)
TYP = dict(tag="Typ 1 oder Typ 2", color=BLUE_D, tint=BLUE_L, total=2)
FUS = dict(tag="Diabetes und Füße", color=CORAL, tint=CORAL_L, total=2)

# ===== A1 =====
a1 = (g(toe("roundcut", 2), 90, 40, 1.0) + stars(370, 120, 1.1) + check_badge(110, 60, 34, False)
      + f'<path d="M450,30 L450,440" stroke="{INK}" stroke-width="3" stroke-dasharray="4 14" stroke-linecap="round" opacity=".5"/>'
      + g(toe("straight"), 550, 40, 1.0) + check_badge(570, 60, 34, True)
      + lbl(220, 478, "Rund geschnitten", 32, weight=700) + lbl(680, 478, "Gerade geschnitten", 32, weight=700))
S.append(dict(NAG, file="Main.dc.html", title="Eingewachsener Nagel: Ursache", n=0,
    headline="Warum wächst ein Nagel ein?",
    panels=[dict(caption="Die Ecke macht den Unterschied", bg=BLUE_L, svg=svg(900, 500, a1, "Links ein rund geschnittener Nagel, dessen Ecke in die entzündete Haut drückt; rechts ein gerade geschnittener Nagel ohne Entzündung"))],
    facts=[("scissors", "Nägel gerade schneiden, Ecken nicht abrunden.", "blue"), ("ruler", "Nicht zu kurz – die Nagelecke soll über die Haut reichen.", "blue")],
    question="Wie schneidest du deine Zehennägel?", qspace=150))

# ===== A2 =====
def stage(n, label):
    return dict(caption=f"Stufe {n}", bg="#FFFFFF", flex="1 1 0", pad="58px 10px 12px",
                svg=svg(300, 460, g(toe("straight", n), 18, 40, 1.0) + (stars(250, 70, 0.8) if n >= 2 else ""), f"Zeh, Stufe {n}: {label}"),
                below=f'<div style="{HEAD};font-weight:700;font-size:29px;text-align:center;margin-top:4px">{label}</div>')
S.append(dict(NAG, file="A2-Nagel-Stufen.dc.html", title="Eingewachsener Nagel: Stufen", n=1,
    headline="So entwickelt es sich", row=True,
    panels=[stage(1, "Rötung"), stage(2, "Entzündung"), stage(3, "Wildes Fleisch")],
    facts=[("clock", "Je früher behandelt, desto schonender und schneller.", "blue"), ("drop", "Stufe 2 kann Eiter bilden, Stufe 3 blutet leicht.", "coral")],
    warn="Eiter, Fieber, starke Schwellung oder Diabetes: bitte zuerst ärztlich abklären lassen."))

# ===== A3 =====
a3 = (g(toe("straight", 1, tamp=True), 90, 40, 1.0) + g(toe("straight", brace=True), 550, 40, 1.0)
      + leader(300, 160, 380, 120) + lbl(390, 112, "Tamponade", 30, "start", weight=700)
      + leader(760, 196, 820, 470) + lbl(800, 505, "Spange", 30, "middle", weight=700))
S.append(dict(NAG, file="A3-Nagel-Hilfe.dc.html", title="Eingewachsener Nagel: Was hilft", n=2,
    headline="Was der Podologe tun kann",
    panels=[dict(caption="Ohne Schnitt, ohne OP", bg=BLUE_L, svg=svg(900, 520, a3, "Links eine Tamponade unter dem Nagelrand, rechts eine Nagelkorrekturspange quer über dem Nagel"))],
    facts=[("shield", "Die Tamponade polstert den Nagelrand ab und entlastet die Haut.", "blue"), ("activity", "Die Spange hebt den Nagel sanft an und lenkt das Wachstum.", "blue")],
    cta=True))

# ===== B1 =====
b1 = (FOOT + f'<ellipse cx="764" cy="346" rx="54" ry="34" fill="{CORAL}" opacity=".25"/>'
      + f'<path d="M732,340 C748,326 784,326 800,344" fill="none" stroke="#C9A85E" stroke-width="12" stroke-linecap="round"/>' + SHOE
      + arrow(764, 210, 764, 300) + arrow(690, 228, 724, 304) + arrow(840, 236, 808, 308)
      + bubble(60, 40, 400, ["Jeden Tag", "dieselbe Stelle …"], (420, 210)))
S.append(dict(DRU, file="B1-Druck-Hornhaut.dc.html", title="Druckstellen: Entstehung", n=0,
    headline="Druck plus Reibung ergibt Hornhaut",
    panels=[dict(caption="Der Schuh drückt", bg=SAGE_L, svg=svg(900, 560, b1, "Fuß im zu engen Schuh, Druckpfeile auf den Zehenrücken, dort bildet sich Hornhaut"))],
    facts=[("shield", "Hornhaut schützt die Haut – bei Dauerdruck wird sie dick und hart.", "sage"), ("search", "Typisch: Zehenrücken, Zehenkuppen, Fußballen, zwischen den Zehen.", "sage")]))

# ===== B2 =====
b2 = (f'<path d="M0,120 C200,112 700,112 900,120 L900,190 L0,190 Z" fill="#EAD7AC" stroke="{INK}" stroke-width="3"/>'
      + "".join(f'<path d="M0,{132+i*14} C300,{126+i*14} 600,{126+i*14} 900,{132+i*14}" fill="none" stroke="#CDB57F" stroke-width="2"/>' for i in range(4))
      + f'<rect x="0" y="190" width="900" height="80" fill="#F3D2BD" stroke="{INK}" stroke-width="3"/>'
      + f'<rect x="0" y="270" width="900" height="110" fill="#F8E4D7" stroke="{INK}" stroke-width="3"/>'
      + "".join(f'<circle cx="{40+i*92}" cy="{410+(i%2)*20}" r="26" fill="#FBF0DF" stroke="#E8CFAE" stroke-width="3"/>' for i in range(10))
      + f'<rect x="0" y="380" width="900" height="80" fill="none"/>'
      + f'<path d="M0,470 C300,450 600,450 900,470 L900,520 L0,520 Z" fill="#ECE3CD" stroke="{INK}" stroke-width="3"/>'
      + "".join(f'<circle cx="{30+i*60}" cy="{494+(i%3)*6}" r="4" fill="#CDBF9B"/>' for i in range(15))
      + f'<path d="M60,300 C150,330 250,290 340,318 C380,330 400,350 450,352 C500,350 520,330 560,318 C650,290 750,330 860,300" fill="none" stroke="#E2A82A" stroke-width="9" stroke-linecap="round"/>'
      + f'<path d="M80,250 C200,236 300,262 420,244" fill="none" stroke="#D8735E" stroke-width="3"/>'
      + f'<path d="M318,104 L582,104 C590,104 594,110 592,118 L478,330 C468,348 432,348 422,330 L308,118 C306,110 310,104 318,104 Z" fill="#D8BE85" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/>'
      + "".join(f'<path d="M{330+i*12},{118+i*26} L{570-i*12},{118+i*26}" stroke="#B89A5C" stroke-width="2.5"/>' for i in range(7))
      + stars(500, 360, 0.9) + stars(370, 370, 0.7)
      + leader(860, 150, 860, 70) + lbl(860, 58, "Hornhaut", 28, "end", weight=700)
      + leader(600, 150, 680, 70) + lbl(700, 58, "Kern (Dorn)", 28, "start", weight=700)
      + leader(800, 312, 800, 352) + lbl(800, 384, "Nerv", 28, weight=700)
      + leader(120, 498, 120, 545) + lbl(120, 578, "Knochen", 28, weight=700))
S.append(dict(DRU, file="B2-Clavus-Kern.dc.html", title="Hühnerauge: der Kern", n=1,
    headline="Das Hühnerauge hat einen Dorn",
    panels=[dict(caption="Blick unter die Haut", bg="#FFFFFF", svg=svg(900, 600, b2, "Hautquerschnitt: der kegelförmige Kern des Hühnerauges drückt durch die Hautschichten auf einen Nerv"))],
    facts=[("zap", "Der harte Kern drückt in die Tiefe und reizt Nerven – darum sticht jeder Schritt.", "sage"), ("alert", "Bei Diabetes kann darunter unbemerkt eine Wunde entstehen.", "coral")]))

# ===== B3 =====
def dd(ok, items, title):
    col = SAGE if ok else CORAL
    bgc = SAGE_L if ok else CORAL_L
    li = "".join(f'<div style="display:flex;gap:14px;align-items:flex-start">{icon("check" if ok else "x", col if ok else "#A93A22", 34)}<div style="{HEAD};font-weight:500;font-size:30px;line-height:1.28">{t}</div></div>' for t in items)
    return (f'<div style="flex:1 1 0;min-width:0;background:{bgc};border:4px solid {INK};border-radius:18px;padding:26px 26px 30px;display:flex;flex-direction:column;gap:18px">'
            f'<div style="{HAND};font-size:40px;color:{INK}">{title}</div>{li}</div>')
b3_ill = (g(f'<path d="M0,240 C0,140 -6,70 24,36 C50,4 170,4 196,36 C226,70 220,140 220,240 Z" fill="{SKIN}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<ellipse cx="110" cy="150" rx="128" ry="44" fill="#CFE3E7" fill-opacity=".85" stroke="{INK}" stroke-width="{SW}"/><ellipse cx="110" cy="150" rx="60" ry="18" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M80,60 C90,50 130,50 140,60" fill="none" stroke="#C9A85E" stroke-width="10" stroke-linecap="round"/>', 130, 30, 1.0)
          + lbl(240, 320, "Silikon-Schutz", 30, weight=700)
          + g(f'<rect x="0" y="40" width="210" height="80" rx="10" fill="#D6DCDD" stroke="{INK}" stroke-width="{SW}"/><circle cx="70" cy="80" r="12" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><rect x="100" y="70" width="70" height="20" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>', 560, 60, 1.0)
          + f'<path d="M560,40 L790,200 M790,40 L560,200" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>'
          + lbl(675, 320, "Klinge", 30, weight=700))
S.append(dict(DRU, file="B3-Clavus-Hilfe.dc.html", title="Hühnerauge: Was hilft", n=2,
    headline="Was hilft und was nicht",
    panels=[dict(caption="Entlasten statt schneiden", bg=SAGE_L, svg=svg(900, 340, b3_ill, "Links ein Zeh mit Silikon-Schutzring, rechts eine durchgestrichene Rasierklinge"))],
    extra=f'<div style="display:flex;gap:18px">{dd(True, ["Kern schonend entfernen lassen", "Druck nehmen mit Polster und passenden Schuhen"], "So ja")}{dd(False, ["Selbst schneiden", "Säurepflaster, bei Diabetes nie"], "So nicht")}</div>',
    cta=True))

# ===== C1 =====
c1 = (f'<ellipse cx="170" cy="250" rx="150" ry="52" fill="#FFFFFF" stroke="{INK}" stroke-width="{SW}"/><ellipse cx="170" cy="244" rx="104" ry="32" fill="none" stroke="#C9D2CF" stroke-width="3"/>'
      + f'<path d="M96,236 C92,186 120,166 150,170 C176,162 214,170 214,206 L214,240 Z" fill="#E4B877" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/><path d="M110,232 C108,196 126,184 150,186 C172,180 200,188 200,210 L200,234 Z" fill="#F3D9A8"/>'
      + f'<circle cx="236" cy="216" r="30" fill="#E86A4F" stroke="{INK}" stroke-width="3.5"/><path d="M236,186 C240,174 248,170 256,170" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/><path d="M224,204 C226,198 232,196 236,198" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
      + arrow(250, 330, 470, 400, INK, 6, (330, 430))
      + vessel(430, 300, 450, 200, 4)
      + bubble(470, 40, 400, ["Wir wollen", "in die Zellen!"], (640, 330))
      + lbl(170, 360, "Essen", 30, weight=700) + lbl(655, 548, "Blut", 30, weight=700))
S.append(dict(INS, file="C1-Insulin-Zucker.dc.html", title="Diabetes erklärt: Zucker im Blut", n=0,
    headline="Essen wird zu Zucker im Blut",
    panels=[dict(caption="Nach dem Essen", bg=AMBER_L, svg=svg(900, 570, c1, "Ein Teller mit Brot und Apfel, ein Pfeil führt in ein Blutgefäß voller Glukose-Teilchen"))],
    facts=[("activity", "Aus Brot, Nudeln und Obst wird Glukose. Die Zellen brauchen sie als Energie.", "amber")],
    question="Quiz: Welches Organ bildet Insulin?", qspace=140))

# ===== C2 =====
c2 = (pancreas(40, 70, 1.0) + f'<circle cx="340" cy="166" r="62" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="6 8"/>'
      + ikey(520, 300, 0.9, 20) + ikey(600, 360, 0.9, 40) + ikey(700, 300, 0.8, 10) + ikey(440, 390, 0.85, 60)
      + f'<path d="M380,220 C420,260 440,280 470,300" fill="none" stroke="{BLUE}" stroke-width="4" stroke-dasharray="4 10" stroke-linecap="round"/>'
      + vessel(60, 440, 780, 120, 3, True).replace(f'fill="{AMBER}"', f'fill="{AMBER}"')
      + lbl(250, 50, "Bauchspeicheldrüse", 30, weight=700) + leader(340, 120, 450, 70) + lbl(460, 70, "Beta-Zellen", 28, "start", BLUE_D, 700)
      + lbl(770, 250, "Insulin", 32, weight=800, color=BLUE_D))
S.append(dict(INS, file="C2-Insulin-Schluessel.dc.html", title="Diabetes erklärt: Insulin als Schlüssel", n=1,
    headline="Insulin ist der Schlüssel",
    panels=[dict(caption="Die Bauchspeicheldrüse reagiert", bg=BLUE_L, svg=svg(900, 580, c2, "Die Beta-Zellen der Bauchspeicheldrüse schicken Insulin-Schlüssel ins Blut"))],
    facts=[("key", "Steigt der Zucker, schütten die Beta-Zellen Insulin aus.", "blue"), ("drop", "Insulin reist mit dem Blut zu Muskeln, Fett und Leber.", "blue")]))

# ===== C3 =====
cbody, door, rec = cell(600, 300, 250, open_=True)
c3 = (cbody + glucose(150, 420, 30) + glucose(230, 470, 30) + glucose(130, 520, 28)
      + arrow(270, 440, door[0] - 10, door[1] + 8, INK, 6, (300, 400))
      + glucose(door[0] + 70, door[1] + 30, 28)
      + bubble(560, 20, 330, ["Jetzt habe", "ich Energie!"], (660, 150))
      + leader(rec[0] - 50, rec[1] - 30, 120, 80) + lbl(60, 70, "Rezeptor (Schloss)", 28, "start", weight=700)
      + leader(door[0] - 30, door[1] + 50, 110, 300) + lbl(50, 290, "Zucker-Tür", 28, "start", weight=700))
S.append(dict(INS, file="C3-Insulin-Tuer.dc.html", title="Diabetes erklärt: Tür auf", n=2,
    headline="Schlüssel rein, Tür auf",
    panels=[dict(caption="An der Zelle", bg=SAGE_L, svg=svg(900, 580, c3, "Insulin steckt im Rezeptor der Zelle, die Zucker-Tür ist offen, Glukose strömt hinein und wird zu Energie"))],
    facts=[("key", "Insulin dockt am Rezeptor an – wie ein Schlüssel im Schloss.", "sage"), ("zap", "Das öffnet Zucker-Türen. Glukose wird zu Energie, der Blutzucker sinkt.", "sage")]))

# ===== C4 =====
cbody4, door4, rec4 = cell(620, 300, 240, open_=False, dull=True, key_in=False)
crowd = "".join(glucose(x, y, 28, True, "worry") for (x, y) in [(110, 330), (180, 380), (250, 330), (130, 440), (210, 470), (290, 420), (90, 530), (180, 540), (300, 520)])
gauge = (f'<path d="M40,170 A110,110 0 0 1 260,170" fill="none" stroke="#DDE3E1" stroke-width="26" stroke-linecap="round"/>'
         f'<path d="M40,170 A110,110 0 0 1 150,60" fill="none" stroke="{SAGE_M}" stroke-width="26" stroke-linecap="round"/>'
         f'<path d="M150,60 A110,110 0 0 1 260,170" fill="none" stroke="{CORAL}" stroke-width="26" stroke-linecap="round"/>'
         f'<path d="M150,170 L232,96" stroke="{INK}" stroke-width="8" stroke-linecap="round"/><circle cx="150" cy="170" r="14" fill="{INK}"/>')
c4 = (cbody4 + crowd + g(gauge, 30, 20, 0.85) + lbl(158, 205, "Blutzucker", 28, weight=700)
      + bubble(560, 20, 320, ["Die Tür", "bleibt zu."], (640, 120)))
S.append(dict(INS, file="C4-Insulin-Tuer-zu.dc.html", title="Diabetes erklärt: Tür bleibt zu", n=3,
    headline="Ohne Schlüssel bleibt die Tür zu",
    panels=[dict(caption="Das ist Diabetes", bg="#EEF0EC", svg=svg(900, 580, c4, "Glukose staut sich vor der geschlossenen Zelle, die Blutzucker-Anzeige steht im roten Bereich"))],
    facts=[("alert", "Der Zucker bleibt im Blut. Auf Dauer schädigt das Gefäße und Nerven, auch an den Füßen.", "coral")],
    question="Typ 1 oder Typ 2 – kennst du den Unterschied?", qspace=110, hsize=80))

# ===== D1 =====
d1a = (pancreas(130, 40, 1.0, attacked=True) + immune(380, 70) + immune(520, 150, 0.9) + immune(250, 215, 0.85)
       + bubble(600, 170, 280, ["Kein Insulin", "mehr da."], (560, 120), 32))
cb, dr, rc = cell(660, 190, 150, open_=False, dull=False, rusty=True, key_in=True)
d1b = (cb + glucose(140, 160, 26, True, "worry") + glucose(210, 220, 26, True, "worry") + glucose(120, 250, 26, True, "worry")
       + f'<path d="M{rc[0]-90},{rc[1]-80} l16,10 l-16,10 M{rc[0]-40},{rc[1]-110} l6,18 l-18,-2" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round"/>'
       + bubble(30, 20, 330, ["Schlüssel da,", "Schloss klemmt."], (300, 140), 32))
S.append(dict(TYP, file="D1-Typ1-Typ2-Bild.dc.html", title="Typ 1 und Typ 2: Bild", n=0,
    headline="Typ 1 und Typ 2 im Bild",
    panels=[dict(caption="Typ 1", bg=BLUE_L, pad="60px 18px 10px", svg=svg(900, 330, d1a, "Typ 1: Immunzellen greifen die Beta-Zellen der Bauchspeicheldrüse an, es wird kaum Insulin gebildet")),
            dict(caption="Typ 2", bg=SAGE_L, pad="60px 18px 10px", svg=svg(900, 360, d1b, "Typ 2: Insulin steckt im Rezeptor, doch das Schloss reagiert kaum und die Zucker-Tür bleibt zu"))],
    ))

# ===== D2 =====
def cmp_row(label, a, b):
    cell_ = f"{HEAD};font-weight:500;font-size:29px;line-height:1.3;padding:20px 22px"
    return (f'<div style="display:grid;grid-template-columns:200px minmax(0,1fr) minmax(0,1fr);border-top:3px solid {INK}">'
            f'<div style="{cell_};font-weight:700;background:#FFFFFF">{label}</div>'
            f'<div style="{cell_};background:{BLUE_L};border-left:3px solid {INK}">{a}</div>'
            f'<div style="{cell_};background:{SAGE_L};border-left:3px solid {INK}">{b}</div></div>')
d2 = (f'<div style="border:4px solid {INK};border-radius:18px;overflow:hidden;background:#fff">'
      f'<div style="display:grid;grid-template-columns:200px minmax(0,1fr) minmax(0,1fr)">'
      f'<div></div><div style="{HAND};font-size:42px;padding:16px 22px;background:{BLUE};color:#fff;border-left:3px solid {INK}">Typ 1</div>'
      f'<div style="{HAND};font-size:42px;padding:16px 22px;background:{SAGE};color:#fff;border-left:3px solid {INK}">Typ 2</div></div>'
      + cmp_row("Was passiert", "Immunsystem zerstört die Beta-Zellen. Kaum Insulin.", "Insulin ist da, Zellen reagieren schlechter.")
      + cmp_row("Wer", "Oft junge Menschen, aber in jedem Alter.", "Meist Erwachsene. Die häufigste Form.")
      + cmp_row("Ursache", "Autoimmun, nicht durch Lebensstil.", "Veranlagung, wenig Bewegung, Übergewicht, Alter.")
      + cmp_row("Behandlung", "Insulin ist lebensnotwendig.", "Bewegung, Ernährung, Tabletten, später ggf. Insulin.")
      + '</div>')
S.append(dict(TYP, file="D2-Typ1-Typ2-Vergleich.dc.html", title="Typ 1 und Typ 2: Vergleich", n=1,
    headline="Der Unterschied auf einen Blick", extra=d2,
    warn="Beide Typen: Dauerhaft hoher Zucker kann Nerven und Gefäße in den Füßen schädigen."))

# ===== E1 =====
e1 = (FOOT + f'<path d="M240,10 C236,120 250,220 320,290 C420,360 560,400 640,410" fill="none" stroke="#E2A82A" stroke-width="9" stroke-linecap="round"/>'
      + f'<path d="M650,412 C700,416 740,412 780,404" fill="none" stroke="#E2A82A" stroke-width="9" stroke-linecap="round" stroke-dasharray="2 22" opacity=".8"/>'
      + SHOE
      + f'<path d="M600,486 C604,470 624,462 642,466 C660,470 668,484 660,494 L606,496 Z" fill="#8E928A" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/><path d="M616,474 C622,470 630,470 634,472" stroke="#fff" stroke-width="3" opacity=".6" stroke-linecap="round"/>'
      + bubble(560, 60, 320, ["Hier drückt", "doch etwas …"], (632, 456), 32)
      + bubble(40, 120, 230, ["Ich spüre", "nichts."], (180, 330), 32)
      + leader(290, 250, 380, 190) + lbl(390, 188, "Nerv", 28, "start", weight=700))
S.append(dict(FUS, file="E1-Diabetischer-Fuss.dc.html", title="Diabetes und Füße: Warum", n=0,
    headline="Der Stein, den man nicht spürt",
    panels=[dict(caption="Wenn Nerven leiser werden", bg=CORAL_L, svg=svg(900, 560, e1, "Ein Steinchen im Schuh drückt auf die Sohle, der Nerv leitet zu den Zehen hin nur noch schwach, der Fuß spürt nichts"))],
    facts=[("activity", "Hoher Zucker kann Nerven schädigen. Druck und Schmerz werden schlechter gespürt.", "coral"), ("drop", "Die Durchblutung leidet, kleine Wunden heilen langsamer.", "coral")]))

# ===== E2 =====
chk = [("eye", "Füße ansehen, auch Sohle und Zehenzwischenräume"), ("search", "Auf Rötung, Blasen, Risse und Hornhaut achten"),
       ("hand", "Schuhe vor dem Anziehen innen abtasten"), ("home", "Nicht barfuß laufen, keine Wärmflasche an die Füße"), ("scissors", "Nägel nicht selbst tief schneiden")]
e2 = (f'<div style="background:#fff;border:4px solid {INK};border-radius:18px;padding:22px 28px;display:flex;flex-direction:column;gap:6px">'
      f'<div style="{HAND};font-size:36px;color:{CORAL};margin-bottom:6px">Deine tägliche Fußkontrolle</div>'
      + "".join(f'<div style="display:flex;align-items:center;gap:22px;padding:12px 0;border-top:{"0" if i==0 else "2px solid #DCE3E1"}">'
                f'<div style="flex:0 0 64px;height:64px;border-radius:50%;background:{CORAL_L};border:3px solid {INK};display:flex;align-items:center;justify-content:center">{icon(ic, "#A93A22", 32)}</div>'
                f'<div style="{HEAD};font-weight:500;font-size:31px;line-height:1.25">{t}</div></div>' for i, (ic, t) in enumerate(chk))
      + '</div>'
      + f'<div style="display:flex;align-items:center;gap:22px;background:{BLUE_L};border:3px solid {INK};border-radius:18px;padding:20px 26px">'
        f'<div style="flex:0 0 64px;height:64px;border-radius:50%;background:#fff;border:3px solid {INK};display:flex;align-items:center;justify-content:center">{icon("steth", BLUE_D, 34)}</div>'
        f'<div style="{HEAD};font-weight:500;font-size:29px;line-height:1.3"><b>Podologie auf Verordnung:</b> Bei diabetischem Fußsyndrom kann Ihr Arzt sie verordnen. Arzt und Podologe arbeiten Hand in Hand.</div></div>')
S.append(dict(FUS, file="E2-Fusskontrolle.dc.html", title="Diabetes und Füße: tägliche Kontrolle", n=1,
    headline="Zwei Minuten täglich für die Füße", extra=e2, cta=True, hsize=80))

for sp in S:
    open(os.path.join(ROOT, sp["file"]), "w").write(slide(sp))
print("slides", len(S))
