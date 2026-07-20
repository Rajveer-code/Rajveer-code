# Setup — animated profile README

This folder **is** the `Rajveer-code/Rajveer-code` profile repo. Push its
contents to a repo named exactly `Rajveer-code` (your username) and the
`README.md` renders on your profile.

## Files

```
README.md               your profile page (badge layout + grafted animated SVGs)
avatar-ascii.svg        self-typing ASCII portrait   (static — regen on photo change)
info-card.svg           neofetch-style info card     (static — regen on content change)
contrib-heatmap.svg     live contribution heatmap    (auto-refreshed daily)
source-photo.jpg        portrait source
data/contributions.json scraped calendar + stats     (auto-refreshed daily)
scripts/                the five generators + pinned requirements
.github/workflows/      daily cron that refreshes the heatmap
```

The committed `contrib-heatmap.svg` ships as an **empty placeholder** (all
zeros). It fills with real data the moment the Action runs — see step 2.

## Push it

```bash
gh repo create Rajveer-code --public --source . --push   # from this folder
# or: git init && git add . && git commit && git remote add origin ... && git push
```

## 1. Enable the daily refresh

The workflow already grants `contents: write` and triggers on `push` to
`main`, so the first push runs it automatically. To run it by hand:
**Actions tab → "Update profile art" → Run workflow.** It scrapes your public
contribution calendar (no token) and commits a fresh `contrib-heatmap.svg`.

## 2. Regenerate the static art (only when the photo or facts change)

```bash
python -m venv .venv && . .venv/Scripts/activate        # Windows
pip install -r scripts/requirements.txt
pip install opencv-python-headless numpy                 # portrait deps
python scripts/make_ascii_svg.py     # -> avatar-ascii.svg   (tunables at top of file)
python scripts/make_info_card.py     # -> info-card.svg
```

Portrait tuning lives in the constants block of `scripts/make_ascii_svg.py`
(`CROP`, `COLS`, `RAW_BG_CUTOFF`, `CLAHE_CLIP`, `GAMMA`). `STATIC=1 python …`
emits a frozen, non-animated frame.

## Notes

- Everything is self-contained SVG — no third-party stats services, no token.
  GitHub strips `<script>` and inline CSS from READMEs but renders SVG (with
  its SMIL/CSS animations) via `<img>`, which is why the motion lives inside
  each SVG file.
- The `whoami` portrait + card sit in a `<table>` (the only reliable way to
  put two images on one row on GitHub); on narrow mobile the two columns don't
  stack — a known GitHub-markdown limitation of the side-by-side technique.
