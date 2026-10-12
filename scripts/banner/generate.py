"""Generate the ANIMATED terminal banner (assets/banner-{dark,light}.svg). Pure SMIL, no scripts.

LEFT  panel  PERCEPTION.LIVE - top-down 360-degree LiDAR scan of a street scene:
             stippled point cloud revealed by a rotating beam, detection boxes that lock on as the beam
             passes, A* search frontier + path, a robot following the smooth MPC trajectory with a DWA
             sampling fan, and the thesis pipeline stages lighting up in sequence.
RIGHT panel  SYSTEM.INFO rows (assets/banner.json) + animated THESIS.BENCH bars.

Usage:  pip install numpy ; python scripts/banner/generate.py     (edit assets/banner.json, re-run)
"""
import json, math, pathlib
from xml.sax.saxutils import escape
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
W, H = 1180, 664
SWEEP, SECTORS, R = 6.0, 36, 190          # seconds per revolution, radar slices, scan radius (px)

THEMES = {
    "light": dict(page="#f4f6fa", win="#ffffff", bar_line="#d9e0ea", panel="#eef3f7", panel_line="#d3dde8",
                  title="#6b7686", head="#0891b2", key="#6b7686", val="#1f2937", dots="#aeb9c6", pill="#bfe0ea",
                  live="#ef4444", ok="#10b981", dot="#1e1b4b", gnd="#7f8db0", corner="#9fcfdc", track="#dbe5ee",
                  amber="#d97706", violet="#7c3aed", mute="#9aa7b5"),
    "dark":  dict(page="#010409", win="#0d1117", bar_line="#21262d", panel="#161b22", panel_line="#30363d",
                  title="#8b949e", head="#79c0ff", key="#8b949e", val="#e6edf3", dots="#484f58", pill="#1f3a52",
                  live="#ff6b6b", ok="#3fb950", dot="#b6d8ff", gnd="#5d7fa3", corner="#2d5a7b", track="#21262d",
                  amber="#fbbf24", violet="#a78bfa", mute="#6e7681"),
}

# ----------------------------------------------------------------------------- scene (local coords: ego at 0,0; y down)
OBJS = [("CAR", -100, -60, 24, 46, 0), ("CAR", 95, 45, 24, 46, 18), ("CAR", -85, 115, 24, 46, 90),
        ("TRUCK", 100, -125, 30, 64, -8), ("PED", 34, -100, 7, 7, 0), ("PED", 47, -93, 7, 7, 0)]
WP = [(0, 0), (0, -38), (-16, -88), (-12, -135), (10, -172)]          # route waypoints (goal = last)

def rot(p, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)

def scene_points(rng):
    ground, obj = [], []
    for r in range(14, R + 1, 14):                                  # LiDAR scan rings on the ground plane
        for a in np.arange(0, 360, 3.4 * 14 / r * 1.0):
            if rng.random() < 0.8:
                t = math.radians(a + rng.normal(0, 0.6)); rr = r + rng.normal(0, 0.7)
                ground.append((rr * math.cos(t), rr * math.sin(t)))
    for sx in (-1, 1):                                              # road edges (gently curving kerbs)
        for y in np.arange(-R, R, 4):
            ground.append((sx * 58 + 14 * math.sin(y / 45) + rng.normal(0, .6), y))
        for y in np.arange(-150, 150, 3):                           # building walls with gaps
            if rng.random() < 0.7 and (y // 40) % 3 != 1:
                obj.append((sx * 168 + rng.normal(0, 1.0), y))
    for k, (name, cx, cy, w, h, deg) in enumerate(OBJS):            # object returns: perimeter + sparse interior
        pts = []
        for x in np.arange(-w / 2, w / 2 + .1, 3): pts += [(x, -h / 2), (x, h / 2)]
        for y in np.arange(-h / 2, h / 2 + .1, 3): pts += [(-w / 2, y), (w / 2, y)]
        pts += [(rng.uniform(-w / 2, w / 2), rng.uniform(-h / 2, h / 2)) for _ in range(int(w * h / 40))]
        for p in pts:
            q = rot((p[0] + rng.normal(0, .4), p[1] + rng.normal(0, .4)), deg); obj.append((cx + q[0], cy + q[1]))
    return ground, obj

def catmull(P):
    P = [P[0]] + P + [P[-1]]; segs = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        segs.append((p1, c1, c2, p2))
    return segs

def bez(seg, t):
    p0, c1, c2, p1 = seg; u = 1 - t
    return tuple(u**3 * p0[i] + 3 * u * u * t * c1[i] + 3 * u * t * t * c2[i] + t**3 * p1[i] for i in (0, 1))

def paths():
    segs = catmull(WP)
    smooth = f"M{WP[0][0]} {WP[0][1]}" + "".join(f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p[0]:.1f} {p[1]:.1f}" for _, c1, c2, p in segs)
    dense = [bez(s, i / 40) for s in segs for i in range(41)]
    G = 12; nodes = []
    for x, y in dense:                                              # snap to grid -> 8-connected A* route
        n = (round(x / G) * G, round(y / G) * G)
        if not nodes or nodes[-1] != n: nodes.append(n)
    astar = "M" + "L".join(f"{x} {y}" for x, y in nodes)
    return smooth, astar, nodes, G

# ----------------------------------------------------------------------------- svg
def build(theme, cfg):
    t = THEMES[theme]; mono = "'JetBrains Mono','DejaVu Sans Mono',Menlo,Consolas,monospace"
    lx, ly, lw, lh = 35, 88, 418, 550
    rx, ry, rw, rh = 474, 88, 672, 550
    cxv, cyv = lx + lw / 2, ly + 244                                # ego position
    rng = np.random.default_rng(7)
    ground, obj = scene_points(rng)
    smooth, astar, nodes, G = paths()
    ang = lambda x, y: math.degrees(math.atan2(y, x)) % 360
    S = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{mono}">',
         f'<defs><clipPath id="scan"><circle cx="0" cy="0" r="{R}"/></clipPath></defs>',
         f'<rect width="{W}" height="{H}" fill="{t["page"]}"/>',
         f'<rect x="13" y="13" width="{W-26}" height="{H-26}" rx="16" fill="{t["win"]}" stroke="{t["bar_line"]}" stroke-width="2"/>',
         f'<line x1="14" y1="62" x2="{W-14}" y2="62" stroke="{t["bar_line"]}" stroke-width="2"/>',
         '<circle cx="38" cy="38" r="6.5" fill="#ff5f57"/><circle cx="59" cy="38" r="6.5" fill="#febc2e"/><circle cx="80" cy="38" r="6.5" fill="#28c840"/>',
         f'<text x="{W/2}" y="43" text-anchor="middle" font-size="13" fill="{t["title"]}">{escape(cfg["window_title"])}</text>']
    for (x, y, w, h) in [(lx, ly, lw, lh), (rx, ry, rw, rh)]:
        S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{t["panel"]}" stroke="{t["panel_line"]}" stroke-width="1.5"/>')
        S.append(f'<line x1="{x}" y1="{y+36}" x2="{x+w}" y2="{y+36}" stroke="{t["panel_line"]}" stroke-width="1.5"/>')
    # ---- left header + corners
    S.append(f'<text x="{lx+14}" y="{ly+24}" font-size="13" font-weight="bold" letter-spacing="1.5" fill="{t["head"]}">PERCEPTION.LIVE</text>')
    S.append(f'<text x="{lx+lw-14}" y="{ly+24}" text-anchor="end" font-size="11" fill="{t["key"]}">TOP-DOWN · 360° SCAN</text>')
    for ax, ay, dx, dy in [(lx+14, ly+52, 1, 1), (lx+lw-14, ly+52, -1, 1), (lx+14, ly+lh-118, 1, -1), (lx+lw-14, ly+lh-118, -1, -1)]:
        S.append(f'<path d="M{ax} {ay+dy*12}V{ay}H{ax+dx*12}" fill="none" stroke="{t["corner"]}" stroke-width="2"/>')
    # ---- scene group (local coords)
    S.append(f'<g transform="translate({cxv:.1f} {cyv:.1f})">')
    for rr, lab in [(R / 3, "10m"), (2 * R / 3, "20m"), (R, "30m")]:
        S.append(f'<circle r="{rr:.1f}" fill="none" stroke="{t["panel_line"]}" stroke-width="1" stroke-dasharray="2 4"/>')
        S.append(f'<text x="4" y="{-rr + 11:.1f}" font-size="8.5" fill="{t["mute"]}">{lab}</text>')
    S.append(f'<line x1="{-R}" y1="0" x2="{R}" y2="0" stroke="{t["panel_line"]}"/><line x1="0" y1="{-R}" x2="0" y2="{R}" stroke="{t["panel_line"]}"/>')
    # point cloud, split into radar sectors (ground dim / objects bright)
    S.append('<g clip-path="url(#scan)">')
    for kind, pts, col, sw in (("g", ground, t["gnd"], 1.1), ("o", obj, t["dot"], 1.9)):
        buckets = [[] for _ in range(SECTORS)]
        for x, y in pts: buckets[int(ang(x, y) / 360 * SECTORS) % SECTORS].append((x, y))
        for i, b in enumerate(buckets):
            d = "".join(f"M{x:.0f} {y:.0f}h.01" for x, y in b)
            S.append(f'<path d="{d}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" opacity="0.24">'
                     f'<animate attributeName="opacity" values="1;0.24;0.24" keyTimes="0;0.8;1" dur="{SWEEP}s" '
                     f'begin="{i / SECTORS * SWEEP:.3f}s" repeatCount="indefinite"/></path>')
    S.append('</g>')
    # A* search frontier: cells near the route flash as the search 'expands', then the route draws
    rngc = np.random.default_rng(3); cells = set()
    for (nx, ny) in nodes:
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                c = (nx + dx * G, ny + dy * G)
                if c not in nodes and rngc.random() < 0.035: cells.add(c)
    for (x, y) in sorted(cells):
        j = min(range(len(nodes)), key=lambda k: (nodes[k][0] - x) ** 2 + (nodes[k][1] - y) ** 2) / len(nodes)
        S.append(f'<rect x="{x-2.5}" y="{y-2.5}" width="5" height="5" fill="{t["amber"]}" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0.6;0.6;0" keyTimes="0;0.04;0.75;1" dur="{SWEEP}s" begin="{j*SWEEP*0.45:.2f}s" repeatCount="indefinite"/></rect>')
    S.append(f'<path d="{astar}" fill="none" stroke="{t["amber"]}" stroke-width="1.8" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
             f'<animate attributeName="stroke-dashoffset" values="1;0;0" keyTimes="0;0.5;1" dur="{SWEEP}s" repeatCount="indefinite"/></path>')
    S.append(f'<path d="{smooth}" fill="none" stroke="{t["head"]}" stroke-width="2.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
             f'<animate attributeName="stroke-dashoffset" values="1;1;0;0" keyTimes="0;0.35;0.9;1" dur="{SWEEP}s" repeatCount="indefinite"/></path>')
    gx, gy = WP[-1]                                                  # goal marker
    S.append(f'<circle cx="{gx}" cy="{gy}" r="3.5" fill="{t["head"]}"/><circle cx="{gx}" cy="{gy}" r="4" fill="none" stroke="{t["head"]}" stroke-width="1.5">'
             f'<animate attributeName="r" values="4;13" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0" dur="1.6s" repeatCount="indefinite"/></circle>')
    # detection boxes lock on when the beam passes their bearing
    for name, cx, cy, w, h, deg in OBJS:
        pad = 4; bt = ang(cx, cy) / 360 * SWEEP
        S.append(f'<g opacity="0.28"><animate attributeName="opacity" values="1;0.28;0.28" keyTimes="0;0.8;1" dur="{SWEEP}s" begin="{bt:.3f}s" repeatCount="indefinite"/>'
                 f'<g transform="translate({cx} {cy}) rotate({deg})"><rect x="{-w/2-pad}" y="{-h/2-pad}" width="{w+2*pad}" height="{h+2*pad}" fill="none" stroke="{t["head"]}" stroke-width="1.6"/></g>'
                 f'<text x="{cx - len(name)*2.6:.1f}" y="{cy - max(w, h)/2 - 9:.1f}" font-size="9" font-weight="bold" fill="{t["head"]}">{name}</text></g>')
    # beam
    S.append(f'<g><path d="M0 0L{R} 0L{R*math.cos(math.radians(-26)):.1f} {R*math.sin(math.radians(-26)):.1f}Z" fill="{t["head"]}" fill-opacity="0.15"/>'
             f'<line x1="0" y1="0" x2="{R}" y2="0" stroke="{t["head"]}" stroke-width="1.6"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{SWEEP}s" repeatCount="indefinite"/></g>')
    # robot + DWA sampling fan (moves and turns with the MPC trajectory; forward = +x)
    fan = ""
    for k_ in (-0.022, -0.014, -0.007, 0, 0.007, 0.014, 0.022):
        pts = [((math.sin(k_ * s) / k_, (1 - math.cos(k_ * s)) / k_) if k_ else (s, 0)) for s in np.linspace(0, 55, 14)]
        pts = [(x, y) for x, y in pts]
        best = abs(k_) < 1e-9
        fan += (f'<path d="M{"L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" fill="none" stroke="{t["violet"]}" stroke-width="{2 if best else 1}" '
                f'opacity="{0.95 if best else 0.45}"/>')
    S.append(f'<g>{fan}<path d="M-7 -5L8 0L-7 5Z" fill="{t["val"]}" stroke="{t["page"]}" stroke-width="1"/>'
             f'<animateMotion dur="{SWEEP}s" repeatCount="indefinite" rotate="auto" path="{smooth}" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;0.35;0.9;1"/></g>')
    S.append('</g>')
    # ---- pipeline chips (light up in sequence in sync with the sweep)
    chips = cfg["pipeline"]; cw_, gap = 84, 18; cy0 = ly + lh - 100
    for i, label in enumerate(chips):
        x0 = lx + 14 + i * (cw_ + gap)
        S.append(f'<rect x="{x0}" y="{cy0}" width="{cw_}" height="28" rx="5" fill="{t["head"]}" fill-opacity="0.06" stroke="{t["head"]}" stroke-width="1">'
                 f'<animate attributeName="fill-opacity" values="0.4;0.06;0.06" keyTimes="0;0.25;1" dur="{SWEEP}s" begin="{i/len(chips)*SWEEP:.2f}s" repeatCount="indefinite"/></rect>')
        S.append(f'<text x="{x0+cw_/2}" y="{cy0+18}" text-anchor="middle" font-size="10.5" fill="{t["val"]}">{escape(label)}</text>')
        if i < len(chips) - 1:
            S.append(f'<text x="{x0+cw_+gap/2}" y="{cy0+18}" text-anchor="middle" font-size="12" fill="{t["key"]}">›</text>')
    # legend + footer
    ly0 = ly + lh - 54
    for i, (lab, col, kind) in enumerate([("A*", t["amber"], "line"), ("DWA", t["violet"], "line"), ("MPC", t["head"], "line"), ("DET", t["head"], "box")]):
        x0 = lx + 24 + i * 98
        S.append(f'<line x1="{x0}" y1="{ly0-4}" x2="{x0+16}" y2="{ly0-4}" stroke="{col}" stroke-width="2.2"/>' if kind == "line"
                 else f'<rect x="{x0}" y="{ly0-9}" width="16" height="10" fill="none" stroke="{col}" stroke-width="1.6"/>')
        S.append(f'<text x="{x0+22}" y="{ly0}" font-size="10.5" fill="{t["key"]}">{lab}</text>')
    S.append(f'<text x="{lx+24}" y="{ly+lh-16}" font-size="10.5" fill="{t["key"]}">PTS {len(ground)+len(obj)} · SWEEP {SWEEP:.0f}s · A* → DWA → MPC</text>')
    # ---- right panel header
    S.append(f'<text x="{rx+16}" y="{ry+24}" font-size="13" font-weight="bold" letter-spacing="1.5" fill="{t["head"]}">SYSTEM.INFO</text>')
    S.append(f'<rect x="{rx+rw-166}" y="{ry+7}" width="148" height="24" rx="12" fill="{t["pill"]}"/>')
    S.append(f'<text x="{rx+rw-92}" y="{ry+24}" text-anchor="middle" font-size="14" font-weight="bold" fill="{t["head"]}">{escape(cfg["handle"])}</text>')
    S.append(f'<circle cx="{rx+rw-218}" cy="{ry+19}" r="4" fill="{t["live"]}"><animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    S.append(f'<text x="{rx+rw-208}" y="{ry+24}" font-size="12" font-weight="bold" fill="{t["live"]}">LIVE</text>')
    # ---- info rows
    cw, fs = 8.4, 14; y = ry + 68; step = 21.5
    for n, (key, val) in enumerate(cfg["rows"]):
        vals = val if isinstance(val, list) else [val]
        kx, vx = rx + 16, rx + rw - 18
        k_end = kx + len(key) * cw + 10; v_start = vx - max(len(v) for v in vals) * cw - 10
        t0 = 0.4 + n * 0.12
        S.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{t0:.2f}s" fill="freeze"/>'
                 f'<animateTransform attributeName="transform" type="translate" from="18 0" to="0 0" dur="0.35s" begin="{t0:.2f}s" fill="freeze"/>'
                 f'<text x="{kx}" y="{y:.1f}" font-size="{fs}" fill="{t["key"]}">{escape(key)}</text>')
        if v_start > k_end:
            S.append(f'<line x1="{k_end:.0f}" y1="{y-4:.1f}" x2="{v_start:.0f}" y2="{y-4:.1f}" stroke="{t["dots"]}" stroke-width="1.2" stroke-dasharray="0.1 3.4" stroke-linecap="round"/>')
        m = len(vals); kt = ";".join(f"{i / m:.4f}" for i in range(m))
        for i, v in enumerate(vals):
            if m == 1:
                S.append(f'<text x="{vx}" y="{y:.1f}" text-anchor="end" font-size="{fs}" fill="{t["val"]}">{escape(v)}</text>')
            else:
                ov = ";".join("1" if j == i else "0" for j in range(m))
                S.append(f'<text x="{vx}" y="{y:.1f}" text-anchor="end" font-size="{fs}" fill="{t["val"]}" opacity="{1 if i == 0 else 0}">{escape(v)}'
                         f'<animate attributeName="opacity" values="{ov}" keyTimes="{kt}" calcMode="discrete" dur="{3*m}s" repeatCount="indefinite"/></text>')
        S.append('</g>'); y += step
    # ---- bench bars
    b = cfg["bench"]; by0 = ry + 350
    S.append(f'<line x1="{rx+16}" y1="{by0-14}" x2="{rx+rw-16}" y2="{by0-14}" stroke="{t["panel_line"]}" stroke-width="1.5"/>')
    S.append(f'<text x="{rx+16}" y="{by0+6}" font-size="12" font-weight="bold" letter-spacing="1.5" fill="{t["head"]}">{escape(b["title"])}</text>')
    S.append(f'<text x="{rx+rw-16}" y="{by0+6}" text-anchor="end" font-size="11" fill="{t["key"]}">{escape(b["meta"])}</text>')
    bx0, bw = rx + 176, rw - 176 - 16 - 108
    for i, (lab, v, mx, txt) in enumerate(b["bars"]):
        yy = by0 + 34 + i * 25; frac = v / mx; col = t["head"] if "TransFusion" not in lab else t["mute"]; t0 = 2.9 + i * 0.35
        S.append(f'<text x="{rx+16}" y="{yy}" font-size="13" fill="{t["key"]}">{escape(lab)}</text>')
        S.append(f'<rect x="{bx0}" y="{yy-10}" width="{bw}" height="9" rx="4.5" fill="{t["track"]}"/>')
        S.append(f'<rect x="{bx0}" y="{yy-10}" width="0" height="9" rx="4.5" fill="{col}"><animate attributeName="width" from="0" to="{bw*frac:.1f}" dur="1.1s" begin="{t0:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/></rect>')
        S.append(f'<text x="{rx+rw-16}" y="{yy}" text-anchor="end" font-size="13" font-weight="bold" fill="{t["val"]}" opacity="0">{escape(txt)}'
                 f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{t0+0.9:.2f}s" fill="freeze"/></text>')
    S.append(f'<text x="{rx+16}" y="{by0+34+4*25+8}" font-size="14" fill="{t["head"]}">$ <tspan fill="{t["val"]}">_</tspan>'
             f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></text>')
    # ---- footer
    S.append(f'<line x1="{rx+16}" y1="{ry+rh-42}" x2="{rx+rw-16}" y2="{ry+rh-42}" stroke="{t["panel_line"]}" stroke-width="2"/>')
    S.append(f'<circle cx="{rx+20}" cy="{ry+rh-20}" r="3.5" fill="{t["ok"]}"><animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    S.append(f'<text x="{rx+30}" y="{ry+rh-16}" font-size="11.5" fill="{t["ok"]}">ALL SYSTEMS NOMINAL</text>')
    S.append(f'<text x="{rx+rw-16}" y="{ry+rh-16}" text-anchor="end" font-size="11.5" fill="{t["key"]}">{escape(cfg["footer_right"])}</text>')
    S.append('</svg>')
    return "\n".join(S)

if __name__ == "__main__":
    cfg = json.loads((ROOT / "assets/banner.json").read_text())
    for theme in THEMES:
        (ROOT / f"assets/banner-{theme}.svg").write_text(build(theme, cfg))
    print("banner written")
