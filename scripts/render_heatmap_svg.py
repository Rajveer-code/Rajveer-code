#!/usr/bin/env python3
"""Draw data/contributions.json as an animated 53x7 contribution heatmap SVG.

Rounded, colour-graded boxes reveal on a diagonal (line-after-line slide-in,
play once then freeze), with month labels, weekday labels, a Less->More legend
and a stats footer. Cyan/teal ramp to match the profile's palette.
"""
import datetime as dt
import json

IN, OUT = "data/contributions.json", "contrib-heatmap.svg"

# none -> brightest, cyan/teal to match the rest of the profile
PALETTE = ["#161b22", "#0e3a3a", "#0f766e", "#0891b2", "#22d3ee"]

CELL, GAP = 13, 4
STEP = CELL + GAP
PAD_L, PAD_T = 30, 22          # room for weekday + month labels
PAD_R, PAD_B = 16, 34          # room for legend + footer
TEXT = "#8b949e"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WK_STEP = 0.03                 # per-column reveal stagger (s)
DUR = 0.45


def main():
    with open(IN, encoding="utf-8") as f:
        data = json.load(f)
    days = data["days"]
    weeks = data["weeks"]

    grid_w = PAD_L + weeks * STEP + PAD_R
    grid_h = PAD_T + 7 * STEP + PAD_B
    W, H = grid_w, grid_h

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="GitHub contribution heatmap">',
        f'<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'
        f'monospace;font-size:10px;fill:{TEXT};}}'
        f'.b{{opacity:0}}</style>',
    ]

    # weekday labels (Mon/Wed/Fri) — rows are Sun=0..Sat=6
    for row, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = PAD_T + row * STEP + CELL - 3
        out.append(f'<text x="2" y="{y}">{lab}</text>')

    # month labels: first column whose first-of-month falls in it
    seen = set()
    for d in days:
        date = dt.date.fromisoformat(d["date"])
        if date.day <= 7 and d["row"] == 0 and date.month not in seen:
            seen.add(date.month)
            x = PAD_L + d["col"] * STEP
            out.append(f'<text x="{x}" y="{PAD_T-8}">{MONTHS[date.month-1]}</text>')

    # cells
    for d in days:
        x = PAD_L + d["col"] * STEP
        y = PAD_T + d["row"] * STEP
        color = PALETTE[min(d["level"], len(PALETTE) - 1)]
        begin = round(d["col"] * WK_STEP, 3)
        out.append(
            f'<rect class="b" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="3" fill="{color}">'
            f'<animate attributeName="opacity" from="0" to="1" dur="{DUR}s" '
            f'begin="{begin}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="0 -7" to="0 0" dur="{DUR}s" begin="{begin}s" fill="freeze" '
            f'additive="sum"/></rect>')

    # footer: total (left) + legend Less [] [] [] [] More (right)
    fy = PAD_T + 7 * STEP + 18
    total = data["total_last_year"]
    out.append(
        f'<text x="{PAD_L}" y="{fy}" style="fill:#c9d1d9;font-size:11px">'
        f'{total:,} contributions in the last year</text>')

    legend_x = W - PAD_R - (len(PALETTE) * (11 + 3) + 62)
    out.append(f'<text x="{legend_x}" y="{fy}">Less</text>')
    lx = legend_x + 26
    for i, col in enumerate(PALETTE):
        out.append(
            f'<rect x="{lx + i*14}" y="{fy-9}" width="11" height="11" rx="2" '
            f'fill="{col}"/>')
    out.append(f'<text x="{lx + len(PALETTE)*14 + 3}" y="{fy}">More</text>')

    out.append("</svg>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"wrote {OUT}: {weeks} weeks, {total} contributions")


if __name__ == "__main__":
    main()
