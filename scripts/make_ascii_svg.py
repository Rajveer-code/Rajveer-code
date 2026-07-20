#!/usr/bin/env python3
"""Portrait photo -> self-typing monochrome ASCII art inside a terminal window.

Prep (crop, denoise, CLAHE local-contrast) and convert (brightness -> glyph
ramp -> animated SVG) live in one script. No rembg/background removal: the
source sits on a near-black studio backdrop, so dark pixels map to spaces and
fall away. The art is wrapped in a rounded terminal window (title bar with
traffic-light dots + a whoami footer) and each row wipes in left-to-right.

Run:  python scripts/make_ascii_svg.py
Env:  STATIC=1  ->  frozen (non-animated) frame for local previews.
"""
import os
import cv2
import numpy as np

# ---- content --------------------------------------------------------------
SRC        = "source-photo.jpg"
OUT        = "avatar-ascii.svg"
TITLE      = "rajveer@github: ~$ ./portrait.sh"
WHOAMI     = "rajveer@github:~$ whoami "
NAME       = "Rajveer Singh Pall"

# ---- portrait tunables ----------------------------------------------------
CROP  = (0.29, 0.14, 0.73, 0.40)   # left, top, right, bottom (head + shoulders)
COLS  = 100                         # character columns (reference density)
CELL_ASPECT = 0.50                  # glyph height:width, sets the row count
RAW_BG_CUTOFF = 34                  # raw gray below this -> blank (kills backdrop)
BILATERAL     = (7, 55, 55)         # d, sigmaColor, sigmaSpace
CLAHE_CLIP    = 1.6
CLAHE_TILE    = (8, 8)
GAMMA         = 1.15
RAMP = " .`:-=+*cs#%@"              # sparse -> dense (dense = brightest on dark)

# ---- window / layout (mirrors the reference terminal card) ----------------
W        = 840
PAD_X    = 20
ART_W    = 800                      # text stretched to this via textLength
BAR_H    = 30
FS       = 12.9
ROW_H    = 15
INK      = "#c9d1d9"
BG0, BG1 = "#111722", "#0d1117"
BORDER   = "#30363d"
DOTS     = ["#ff5f56", "#ffbd2e", "#27c93f"]
DIM      = "#7d8590"
STEP     = 0.11                     # per-row stagger + wipe duration (s)
# ---------------------------------------------------------------------------


def build_grid():
    img = cv2.imread(SRC, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"could not read {SRC}")
    h, w = img.shape
    l, t, r, b = CROP
    img = img[int(t * h):int(b * h), int(l * w):int(r * w)]

    ch, cw = img.shape
    rows = max(1, int(round(COLS * (ch / cw) * CELL_ASPECT)))

    d, sc, ss = BILATERAL
    smooth = cv2.bilateralFilter(img, d, sc, ss)
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=CLAHE_TILE).apply(smooth)

    raw_small = cv2.resize(smooth, (COLS, rows), interpolation=cv2.INTER_AREA)
    cl_small  = cv2.resize(clahe,  (COLS, rows), interpolation=cv2.INTER_AREA)

    t_norm = np.power(cl_small / 255.0, GAMMA)
    idx = np.clip((t_norm * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)

    grid = [[" " if raw_small[y, x] < RAW_BG_CUTOFF else RAMP[idx[y, x]]
             for x in range(COLS)] for y in range(rows)]

    # despeckle: drop isolated glyphs (< 2 inked 8-neighbours)
    def inked(y, x):
        return 0 <= y < rows and 0 <= x < COLS and grid[y][x] != " "
    cleaned = [row[:] for row in grid]
    for y in range(rows):
        for x in range(COLS):
            if grid[y][x] != " ":
                n = sum(inked(y + dy, x + dx)
                        for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx))
                if n < 2:
                    cleaned[y][x] = " "
    # keep full width (uniform textLength / wipe); spaces render as nothing
    return ["".join(row) for row in cleaned]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(lines, static=False):
    rows = len(lines)
    art_top = BAR_H + 7
    H = art_top + rows * ROW_H + 45
    foot_line = art_top + rows * ROW_H
    foot_y = foot_line + 19

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,'
        f'Consolas,monospace" role="img" aria-label="ASCII self-portrait">',
        f'<defs><linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG0}"/>'
        f'<stop offset="1" stop-color="{BG1}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#pbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" '
        f'stroke="{BORDER}"/>',
        f'<line x1="0" y1="{BAR_H}" x2="{W}" y2="{BAR_H}" stroke="{BORDER}"/>',
    ]
    for i, col in enumerate(DOTS):
        out.append(f'<circle cx="{20 + i*16}" cy="15" r="5" fill="{col}"/>')
    out.append(
        f'<text x="{W/2}" y="19" fill="{DIM}" font-size="12" '
        f'text-anchor="middle">{esc(TITLE)}</text>')

    for i, line in enumerate(lines):
        base = round(art_top + i * ROW_H + FS * 0.86, 1)
        clip_y = art_top + i * ROW_H
        txt = esc(line)
        if static:
            out.append(
                f'<text xml:space="preserve" x="{PAD_X}" y="{base}" fill="{INK}" '
                f'font-size="{FS}" textLength="{ART_W}" lengthAdjust="spacing">'
                f'{txt}</text>')
            continue
        begin = round(i * STEP, 3)
        out.append(
            f'<clipPath id="pr{i}"><rect x="{PAD_X}" y="{clip_y}" height="{ROW_H}" '
            f'width="0"><animate attributeName="width" from="0" to="{ART_W}" '
            f'begin="{begin}s" dur="{STEP}s" fill="freeze"/></rect></clipPath>'
            f'<g clip-path="url(#pr{i})"><text xml:space="preserve" x="{PAD_X}" '
            f'y="{base}" fill="{INK}" font-size="{FS}" textLength="{ART_W}" '
            f'lengthAdjust="spacing">{txt}</text></g>'
            f'<rect y="{clip_y + 1}" width="8" height="13" fill="{INK}" '
            f'opacity="0"><animate attributeName="x" from="{PAD_X}" '
            f'to="{PAD_X + ART_W}" begin="{begin}s" dur="{STEP}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{begin}s"/>'
            f'<set attributeName="opacity" to="0" begin="{round(begin+STEP,3)}s"/>'
            f'</rect>')

    # footer prompt + blinking cursor
    cur_x = round(PAD_X + (len(WHOAMI) + len(NAME)) * 7.25, 0)
    out.append(f'<line x1="0" y1="{foot_line}" x2="{W}" y2="{foot_line}" stroke="{BORDER}"/>')
    out.append(
        f'<text x="{PAD_X}" y="{foot_y}" fill="{DIM}" font-size="13">{esc(WHOAMI)}'
        f'<tspan fill="{INK}">{esc(NAME)}</tspan></text>')
    out.append(
        f'<rect x="{cur_x}" y="{foot_y - 12}" width="8" height="14" fill="{INK}">'
        f'<animate attributeName="opacity" values="1;1;0;0" '
        f'keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>')

    out.append("</svg>")
    return "".join(out)


def main():
    lines = build_grid()
    svg = build_svg(lines, static=os.environ.get("STATIC") == "1")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}: {COLS} cols x {len(lines)} rows")


if __name__ == "__main__":
    main()
