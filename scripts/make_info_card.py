#!/usr/bin/env python3
"""Neofetch-style info card SVG in a terminal window, printed line by line.

The contribution graph already covers GitHub stats, so this panel carries the
story numbers can't: who, what's shipped, how to reach him. Every value traces
to the profile README / ORCID and is edited by hand. Rows fade + slide in on a
spline-eased stagger inside a rounded terminal window.

Run:  python scripts/make_info_card.py
Env:  STATIC=1  ->  frozen frame for local previews.
"""
import os

OUT = "info-card.svg"
TITLE = "rajveer@github: ~$ neofetch"

# blocks: ("header",), ("row", key, val), ("section", label), ("bullet", text)
BLOCKS = [
    ("header",),
    ("row", "Now",     "ML Researcher — Trustworthy & Causal ML"),
    ("row", "Edu",     "B.Tech CSBS · Gyan Ganga IT&S, India"),
    ("row", "Goal",    "US MS (CS / ML) · Fall 2027"),
    ("row", "Focus",   "Deployment-shift reliability · Fairness"),
    ("section", "— Stack"),
    ("row", "Methods", "Causal Forests · Double ML · RDD · DiD"),
    ("row", "ML",      "XGBoost · CatBoost · PyTorch · sklearn"),
    ("row", "NLP",     "FinBERT · Transformers · SHAP · RAG"),
    ("row", "Lang",    "Python · R · SQL"),
    ("section", "— Highlights"),
    ("bullet", "1 paper accepted (IEEE) · 3 under review"),
    ("bullet", "HMDA 42M · BRFSS 1.28M · NHANES · 14.5k calls"),
    ("bullet", "TrustShift — 4-domain deployment-shift audit"),
]

# ---- layout / palette (mirrors the reference card) ------------------------
W        = 480
PAD_X    = 20
VAL_X    = 112
BAR_H    = 30
STEP_Y   = 20.5
SEC_GAP  = 10.3          # extra space before a section header
FS       = 12.5
BG0, BG1 = "#111722", "#0d1117"
BORDER   = "#30363d"
DOTS     = ["#ff5f56", "#ffbd2e", "#27c93f"]
DIM      = "#7d8590"
KEY      = "#ffa657"     # orange
VAL      = "#c9d1d9"
SECT     = "#58a6ff"     # blue
GREEN    = "#3fb950"
CYAN     = "#22d3ee"
BEGIN0   = 0.15
BEGIN_DT = 0.06
DUR      = 0.4
# ---------------------------------------------------------------------------


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("'", "&#x27;"))


def layout():
    """Assign a baseline y to each block; return (blocks_with_y, height)."""
    placed, y = [], BAR_H
    for blk in BLOCKS:
        if blk[0] == "header":
            y += 30
        elif blk[0] == "section":
            y += SEC_GAP + STEP_Y
        else:
            y += STEP_Y
        placed.append((y, blk))
    return placed, round(y + 49.5)


def anim(idx, extra=""):
    b = round(BEGIN0 + idx * BEGIN_DT, 3)
    return (f'<animate attributeName="opacity" from="0" to="1" begin="{b}s" '
            f'dur="{DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="0 5" to="0 0" begin="{b}s" dur="{DUR}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.2 0.8 0.2 1"/>{extra}')


def build(static=False):
    placed, H = layout()
    o0 = ' opacity="1"' if static else ' opacity="0"'
    tr = '' if static else ' transform="translate(0,5)"'

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,'
        f'Consolas,monospace" role="img" aria-label="neofetch info card">',
        f'<defs><linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG0}"/>'
        f'<stop offset="1" stop-color="{BG1}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" '
        f'stroke="{BORDER}"/>',
        f'<line x1="0" y1="{BAR_H}" x2="{W}" y2="{BAR_H}" stroke="{BORDER}"/>',
    ]
    for i, col in enumerate(DOTS):
        out.append(f'<circle cx="{20 + i*16}" cy="15" r="5" fill="{col}"/>')
    out.append(
        f'<text x="{W/2}" y="19" fill="{DIM}" font-size="12" '
        f'text-anchor="middle">{esc(TITLE)}</text>')

    for idx, (y, blk) in enumerate(placed):
        g = f'<g{o0}{tr}>'
        if blk[0] == "header":
            inner = (
                f'<text x="{PAD_X}" y="{y}" font-size="14" font-weight="700">'
                f'<tspan fill="{GREEN}">rajveer</tspan>'
                f'<tspan fill="{DIM}">@</tspan>'
                f'<tspan fill="{CYAN}">github</tspan></text>'
                f'<line x1="152" y1="{y-4}" x2="460" y2="{y-4}" stroke="{BORDER}" '
                f'stroke-opacity="0.8"/>')
        elif blk[0] == "section":
            inner = (
                f'<text x="{PAD_X}" y="{y}" fill="{SECT}" font-size="{FS}" '
                f'font-weight="700">{esc(blk[1])}</text>'
                f'<line x1="{PAD_X + len(blk[1])*8 + 8}" y1="{y-4}" x2="460" '
                f'y2="{y-4}" stroke="{BORDER}" stroke-opacity="0.8"/>')
        elif blk[0] == "bullet":
            inner = (
                f'<circle cx="23" cy="{y-4}" r="2.5" fill="{GREEN}"/>'
                f'<text x="34" y="{y}" fill="{VAL}" font-size="{FS}">'
                f'{esc(blk[1])}</text>')
        else:
            inner = (
                f'<text x="{PAD_X}" y="{y}" fill="{KEY}" font-size="{FS}" '
                f'font-weight="700">{esc(blk[1])}</text>'
                f'<text x="{VAL_X}" y="{y}" fill="{VAL}" font-size="{FS}">'
                f'{esc(blk[2])}</text>')
        anims = "" if static else anim(idx)
        out.append(f'{g}{inner}{anims}</g>')

    out.append("</svg>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print(f"wrote {OUT}: {W}x{H}, {len(BLOCKS)} blocks")


if __name__ == "__main__":
    build(static=os.environ.get("STATIC") == "1")
