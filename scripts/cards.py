"""Generate the self-hosted GitHub stats card (no third-party card services).
Writes assets/card-stats-{dark,light}.svg (the language card is hand-authored: see scripts/langs.py).
Usage: GITHUB_TOKEN=... python scripts/cards.py ayanali827   (token optional, avoids rate limits)
"""
import json, os, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
USER = sys.argv[1] if len(sys.argv) > 1 else "ayanali827"
THEMES = {
    "dark":  dict(bg="#0d1117", border="#30363d", text="#c9d1d9", muted="#8b949e", accent="#79c0ff"),
    "light": dict(bg="#ffffff", border="#d0d7de", text="#24292f", muted="#57606a", accent="#0969da"),
}

def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def collect():
    user = api(f"/users/{USER}")
    repos, page = [], 1
    while True:
        batch = api(f"/users/{USER}/repos?per_page=100&type=owner&page={page}")
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    return {"Public repos": user["public_repos"],
            "Stars earned": sum(r["stargazers_count"] for r in own),
            "Forks of my repos": sum(r["forks_count"] for r in own),
            "Followers": user["followers"]}

def stats_svg(stats, t):
    rows = "".join(f'<text x="30" y="{80 + i*34}" font-family="monospace" font-size="15" fill="{t["muted"]}">{k}</text>'
                   f'<text x="450" y="{80 + i*34}" text-anchor="end" font-family="monospace" font-size="17" '
                   f'font-weight="bold" fill="{t["text"]}">{v}</text>' for i, (k, v) in enumerate(stats.items()))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="{80 + len(stats)*34}">'
            f'<rect x="1" y="1" width="478" height="{78 + len(stats)*34}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            f'<text x="30" y="40" font-family="monospace" font-size="18" font-weight="bold" fill="{t["accent"]}">{USER} / stats</text>'
            f'{rows}</svg>')

if __name__ == "__main__":
    stats = collect()
    (ROOT / "assets").mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (ROOT / f"assets/card-stats-{name}.svg").write_text(stats_svg(stats, t))
    print("cards written:", stats)
