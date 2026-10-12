# Setup (5 minutes)

1. Create a **public** repo named exactly `ayanali827` (same as your username) and push this folder to it.
2. Go to **Actions → Update profile assets → Run workflow** once. This replaces the "pending" stats card with real numbers.
   If the push step fails: **Settings → Actions → General → Workflow permissions → Read and write**.
3. Pin your 4–6 best repos on your profile page.

## Editing

| What | File | Then |
|---|---|---|
| Banner rows, bench bars, pipeline chips, Status words | `assets/banner.json` | `python scripts/build_all.py` |
| Radar skills (all equal = 8 right now) | `assets/skills.json` | same |
| Language stack (equal share each) | `assets/langmix.json` | same |
| Sweep speed / radar slices | `SWEEP`, `SECTORS` in `scripts/banner/generate.py` | same |
| Everything else | `README.md` | commit |

The GitHub Action rebuilds everything on every push to `assets/*.json` or `scripts/**`, and refreshes the stats card daily.
