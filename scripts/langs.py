"""Hand-authored 'language stack' card: every language gets an EQUAL share (assets/langmix.json).
Writes assets/card-langs-{dark,light}.svg.  It is a stack, not a usage statistic, so no percentages are shown.
"""
import json, pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEMES = {
    "dark":  dict(bg="#0d1117", border="#30363d", text="#c9d1d9", muted="#8b949e", accent="#79c0ff",
                  pal=["#79c0ff", "#d2a8ff", "#7ee787", "#ffa657", "#ff7b72", "#f2cc60", "#56d4dd", "#a5d6ff"]),
    "light": dict(bg="#ffffff", border="#d0d7de", text="#24292f", muted="#57606a", accent="#0969da",
                  pal=["#0969da", "#8250df", "#1a7f37", "#bc4c00", "#cf222e", "#9a6700", "#1b7c83", "#218bff"]),
}

def render(cfg, t, w=480):
    langs = cfg["languages"]; n = len(langs); bx, bw, by, bh = 30, w - 60, 56, 14
    seg = bw / n
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{{H}}">',
           f'<rect x="1" y="1" width="{w-2}" height="{{H2}}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
           f'<text x="30" y="38" font-family="monospace" font-size="18" font-weight="bold" fill="{t["accent"]}">{escape(cfg["title"])}</text>']
    for i, name in enumerate(langs):                                  # equal-width segments of one bar
        col = t["pal"][i % len(t["pal"])]
        out.append(f'<rect x="{bx + i*seg:.1f}" y="{by}" width="{seg - 3:.1f}" height="{bh}" rx="4" fill="{col}" opacity="0">'
                   f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{0.3 + i*0.2:.1f}s" fill="freeze"/></rect>')
    cols = 2; y0 = by + bh + 34
    for i, name in enumerate(langs):
        col = t["pal"][i % len(t["pal"])]; x = 30 + (i % cols) * 215; y = y0 + (i // cols) * 28
        out.append(f'<circle cx="{x+5}" cy="{y-4}" r="5" fill="{col}"/>'
                   f'<text x="{x+18}" y="{y}" font-family="monospace" font-size="14" fill="{t["text"]}">{escape(name)}</text>')
    H = y0 + ((n - 1) // cols) * 28 + 26
    return "\n".join(out).replace("{H}", str(H)).replace("{H2}", str(H - 2)) + "\n</svg>"

if __name__ == "__main__":
    cfg = json.loads((ROOT / "assets/langmix.json").read_text())
    for name, t in THEMES.items():
        (ROOT / f"assets/card-langs-{name}.svg").write_text(render(cfg, t))
    print("language stack written")
