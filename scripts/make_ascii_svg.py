#!/usr/bin/env python3
"""Turn a portrait photo into a self-typing, monochrome ASCII-art SVG.

One script on purpose: prep (crop, denoise, CLAHE local-contrast) and convert
(brightness -> glyph ramp -> animated SVG) live together. No rembg / background
removal is needed here because the source already sits on a near-black studio
backdrop: dark pixels map to spaces and simply fall away on a dark README.

Run:  python scripts/make_ascii_svg.py
Env:  STATIC=1  ->  emit a frozen (non-animated) frame for local previews.
"""
import os
import cv2
import numpy as np

# ---- tunables -------------------------------------------------------------
SRC   = "source-photo.jpg"
OUT   = "avatar-ascii.svg"

# crop as fractions of (w, h): head + a hint of shoulders so the face carries
# the portrait instead of the busy dark suit.
CROP  = (0.29, 0.14, 0.73, 0.40)   # left, top, right, bottom

COLS  = 58                          # character columns
CELL_ASPECT = 0.52                  # glyph height:width, sets the row count

RAW_BG_CUTOFF = 34                  # raw gray below this -> blank (kills backdrop)
BILATERAL     = (7, 55, 55)         # d, sigmaColor, sigmaSpace (flatten suit texture)
CLAHE_CLIP    = 1.6
CLAHE_TILE    = (8, 8)
GAMMA         = 1.15                # <1 lifts midtones, >1 deepens shadows

RAMP = " .`:-=+*cs#%@"              # sparse -> dense  (dense = brightest on dark bg)

FONT_SIZE = 12
CHAR_W    = 7.05                    # monospace advance at FONT_SIZE
LINE_H    = 12.6
COLOR     = "#b9c7d6"              # cool light gray
CURSOR    = "#22d3ee"              # cyan typing cursor
STEP      = 0.026                   # per-row start stagger (s)
DUR       = 0.42                    # per-row wipe duration (s)
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

    # bilateral: flatten suit/backdrop texture while keeping face + glasses
    # edges, so CLAHE sharpens structure instead of amplifying JPEG speckle.
    d, sc, ss = BILATERAL
    smooth = cv2.bilateralFilter(img, d, sc, ss)
    clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=CLAHE_TILE).apply(smooth)

    raw_small = cv2.resize(smooth, (COLS, rows), interpolation=cv2.INTER_AREA)
    cl_small  = cv2.resize(clahe,  (COLS, rows), interpolation=cv2.INTER_AREA)

    t_norm = np.power(cl_small / 255.0, GAMMA)
    idx = np.clip((t_norm * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)

    grid = [[" " if raw_small[y, x] < RAW_BG_CUTOFF else RAMP[idx[y, x]]
             for x in range(COLS)] for y in range(rows)]

    # despeckle: drop isolated glyphs (fewer than 2 inked 8-neighbours) so the
    # silhouette stays clean instead of dusted with stray characters.
    def inked(y, x):
        return 0 <= y < rows and 0 <= x < COLS and grid[y][x] != " "
    cleaned = [row[:] for row in grid]
    for y in range(rows):
        for x in range(COLS):
            if grid[y][x] == " ":
                continue
            n = sum(inked(y + dy, x + dx)
                    for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx))
            if n < 2:
                cleaned[y][x] = " "
    return ["".join(row).rstrip() for row in cleaned]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(lines, static=False):
    rows = len(lines)
    W = round(COLS * CHAR_W, 1)
    H = round(rows * LINE_H + 6, 1)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="ASCII self-portrait">',
        f'<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'
        f'"DejaVu Sans Mono",monospace;font-size:{FONT_SIZE}px;fill:{COLOR};'
        f'font-weight:500;letter-spacing:0;}}</style>',
    ]
    defs, body = [], []
    for i, line in enumerate(lines):
        y = round((i + 1) * LINE_H, 1)
        txt = esc(line) if line else ""
        if static or not txt:
            body.append(
                f'<text x="0" y="{y}" xml:space="preserve">{txt}</text>')
            continue
        begin = round(i * STEP, 3)
        end = round(begin + DUR, 3)
        cid = f"c{i}"
        defs.append(
            f'<clipPath id="{cid}"><rect x="0" y="{round(i*LINE_H,1)}" '
            f'width="0" height="{LINE_H+3}"><animate attributeName="width" '
            f'from="0" to="{W}" dur="{DUR}s" begin="{begin}s" '
            f'fill="freeze"/></rect></clipPath>')
        body.append(
            f'<text x="0" y="{y}" xml:space="preserve" '
            f'clip-path="url(#{cid})">{txt}</text>')
        body.append(
            f'<rect x="0" y="{round(i*LINE_H+2,1)}" width="{CHAR_W}" '
            f'height="{FONT_SIZE}" fill="{CURSOR}" opacity="0">'
            f'<animate attributeName="x" from="0" to="{W}" dur="{DUR}s" '
            f'begin="{begin}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.85" begin="{begin}s"/>'
            f'<set attributeName="opacity" to="0" begin="{end}s"/></rect>')
    if defs:
        out.append("<defs>" + "".join(defs) + "</defs>")
    out.extend(body)
    out.append("</svg>")
    return "\n".join(out)


def main():
    lines = build_grid()
    svg = build_svg(lines, static=os.environ.get("STATIC") == "1")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}: {COLS} cols x {len(lines)} rows")


if __name__ == "__main__":
    main()
