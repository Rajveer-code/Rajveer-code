# Setup — profile README art

This folder **is** the `Rajveer-code/Rajveer-code` profile repo. Push its
contents to a repo named exactly `Rajveer-code` (your username) and the
`README.md` renders on your profile.

## Files

```
README.md          your profile page
avatar-ascii.svg   self-typing ASCII portrait   (regen on photo change)
info-card.svg      neofetch-style info card     (regen on content change)
source-photo.jpg   portrait source
scripts/           the two generators + requirements
```

## Regenerate the art (only when the photo or facts change)

```bash
python -m venv .venv && . .venv/Scripts/activate        # Windows
pip install -r scripts/requirements.txt                  # portrait deps
python scripts/make_ascii_svg.py     # -> avatar-ascii.svg
python scripts/make_info_card.py     # -> info-card.svg   (stdlib only)
```

Portrait tuning lives in the constants block of `scripts/make_ascii_svg.py`
(`CROP`, `COLS`, `RAW_BG_CUTOFF`, `CLAHE_CLIP`, `GAMMA`). `STATIC=1 python …`
emits a frozen, non-animated frame; card content is the `BLOCKS` list in
`make_info_card.py`.

## Notes

- Self-contained SVG — GitHub strips `<script>` and inline CSS from READMEs
  but renders SVG (with its SMIL animations) via `<img>`, so the motion lives
  inside each SVG file.
- The `whoami` portrait + card sit in a `<table>` (the only reliable way to
  put two images on one row on GitHub); on narrow mobile the two columns don't
  stack — a known GitHub-markdown limitation.
