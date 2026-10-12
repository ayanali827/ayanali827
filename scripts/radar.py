"""Draw a radar chart from assets/skills.json -> assets/radar-{dark,light}.svg (stdlib only)."""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEMES = {
    "dark":  dict(bg="#0d1117", grid="#30363d", text="#c9d1d9", fill="#79c0ff", line="#79c0ff"),
    "light": dict(bg="#ffffff", grid="#d0d7de", text="#24292f", fill="#0969da", line="#0969da"),
}

def render(cfg, t, size=420, max_val=10, rings=5):
    skills = cfg["skills"]; n = len(skills); c = size / 2; r = size * 0.28; W = 560; cx = W / 2
    pt = lambda i, v: (cx + r * v / max_val * math.sin(2 * math.pi * i / n),
                       c - r * v / max_val * math.cos(2 * math.pi * i / n))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{size}" viewBox="0 0 {W} {size}">',
           f'<rect width="{W}" height="{size}" rx="12" fill="{t["bg"]}"/>']
    for k in range(1, rings + 1):
        pts = " ".join("%.1f,%.1f" % pt(i, max_val * k / rings) for i in range(n))
        out.append(f'<polygon points="{pts}" fill="none" stroke="{t["grid"]}"/>')
    for i, (name, v) in enumerate(skills.items()):
        x, y = pt(i, max_val)
        out.append(f'<line x1="{cx}" y1="{c}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["grid"]}"/>')
        lx, ly = pt(i, max_val * 1.18)
        anchor = "middle" if abs(lx - cx) < 8 else ("start" if lx > cx else "end")
        out.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="{anchor}" font-family="monospace" '
                   f'font-size="12" fill="{t["text"]}">{name}</text>')
    poly = " ".join("%.1f,%.1f" % pt(i, v) for i, v in enumerate(skills.values()))
    out.append(f'<polygon points="{poly}" fill="{t["fill"]}" fill-opacity="0.25" stroke="{t["line"]}" stroke-width="2"/>')
    out.append("</svg>")
    return "\n".join(out)

if __name__ == "__main__":
    cfg = json.loads((ROOT / "assets/skills.json").read_text())
    for name, t in THEMES.items():
        (ROOT / f"assets/radar-{name}.svg").write_text(render(cfg, t))
    print("radar written")
