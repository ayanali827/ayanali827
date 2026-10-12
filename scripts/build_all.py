"""One command to rebuild every generated asset.

    pip install -r requirements.txt
    python scripts/build_all.py [github-username]

Builds: animated banner, skill radar, language stack. Then tries the live GitHub stats card
(needs network; set GITHUB_TOKEN to avoid rate limits). If that step fails the other assets are still written.
"""
import pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
user = sys.argv[1] if len(sys.argv) > 1 else "ayanali827"

def run(script, *args, required=True):
    r = subprocess.run([sys.executable, str(HERE / script), *args])
    if r.returncode and required:
        sys.exit(r.returncode)
    return r.returncode

run("banner/generate.py")
run("radar.py")
run("langs.py")
if run("cards.py", user, required=False):
    print("! stats card skipped (network/rate limit) - existing card kept")
print("all assets built")
