#!/usr/bin/env python3
"""Hand-author a neofetch-style info card SVG that prints in line by line.

The contribution graph already covers GitHub stats, so this panel carries the
story the numbers can't: who, where, what's shipped, how to reach him. Every
value here traces to the profile README / ORCID and is edited by hand.

Run:  python scripts/make_info_card.py
Env:  STATIC=1  ->  frozen (non-animated) frame for local previews.
"""
import os

OUT = "info-card.svg"

USER, HOST = "rajveer", "github"

# (key, value, value-color)  --  keys are right-padded so the colons line up.
CYAN, GRAY, AMBER, ROSE, TEAL = "#22d3ee", "#c9d1d9", "#fbbf24", "#fb7185", "#5eead4"
ROWS = [
    ("Role",     "ML Researcher — Trustworthy & Causal ML", GRAY),
    ("Host",     "B.Tech CSBS · Gyan Ganga IT&S, India", GRAY),
    ("Applying", "US MS (CS / ML) · Fall 2027", AMBER),
    ("Focus",    "Deployment-shift reliability · Fairness", GRAY),
    ("Methods",  "Causal Forests · Double ML · RDD · DiD · DFL", GRAY),
    ("Stack",    "Python · R · SQL · PyTorch · scikit-learn", GRAY),
    ("NLP",      "FinBERT · Transformers · SHAP · RAG", GRAY),
    ("Papers",   "1 accepted (IEEE) · 3 under review", TEAL),
    ("Scale",    "HMDA 42M · BRFSS 1.28M · NHANES · 14.5k calls", GRAY),
    ("ORCID",    "0009-0001-6762-6134", GRAY),
    ("Email",    "rajveerpall04@gmail.com", GRAY),
    ("Web",      "rajveer-code-github-io.vercel.app", CYAN),
]
SWATCHES = ["#0b2447", "#1d4ed8", "#0891b2", "#14b8a6", "#22d3ee", "#fbbf24", "#fb7185"]

# ---- layout ---------------------------------------------------------------
FS      = 13
LINE    = 21
PAD_X   = 14
PAD_Y   = 26
KEYW    = max(len(k) for k, *_ in ROWS)
CHAR_W  = 8.2           # safe monospace advance at FS=13 (over-estimate so
                        # the widest value never clips the viewBox at any scale)
STEP    = 0.11          # per-line stagger (s)
DUR     = 0.5


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tspan(text, color, bold=False):
    w = ';font-weight:700' if bold else ''
    return f'<tspan style="fill:{color}{w}">{esc(text)}</tspan>'


def anim(i):
    """Fade + slide-in for line index i (0 = title)."""
    begin = round(i * STEP, 3)
    return (f'<animate attributeName="opacity" from="0" to="1" dur="{DUR}s" '
            f'begin="{begin}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-10 0" to="0 0" dur="{DUR}s" begin="{begin}s" fill="freeze"/>')


def main():
    static = os.environ.get("STATIC") == "1"
    inner_w = PAD_X * 2 + int((KEYW + 3 + max(len(v) for _, v, _ in ROWS)) * CHAR_W)
    W = max(470, inner_w)
    # title, rule, rows, rule, swatch row
    n_lines = 1 + 1 + len(ROWS) + 1 + 1
    H = PAD_Y + n_lines * LINE + 12
    rule_w = W - PAD_X * 2

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-label="neofetch info card">',
        f'<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'
        f'"DejaVu Sans Mono",monospace;font-size:{FS}px;dominant-baseline:middle;}}'
        f'.g{{opacity:{1 if static else 0};}}</style>',
    ]

    def line_y(i):
        return PAD_Y + i * LINE + LINE // 2

    op = ' opacity="1"' if static else ''
    # 0: title  user@host ~
    y = line_y(0)
    out.append(
        f'<g class="g"{op}>{"" if static else anim(0)}'
        f'<text x="{PAD_X}" y="{y}">'
        f'{tspan(USER, AMBER, True)}{tspan("@", GRAY)}{tspan(HOST, CYAN, True)}'
        f'{tspan("  ~ neofetch", "#6e7681")}</text></g>')
    # 1: rule
    yr = line_y(1)
    out.append(
        f'<g class="g"{op}>{"" if static else anim(1)}'
        f'<line x1="{PAD_X}" y1="{yr}" x2="{PAD_X+rule_w}" y2="{yr}" '
        f'stroke="#30363d" stroke-width="1"/></g>')
    # rows
    for j, (k, v, color) in enumerate(ROWS):
        i = 2 + j
        y = line_y(i)
        key = k.ljust(KEYW)
        out.append(
            f'<g class="g"{op}>{"" if static else anim(i)}'
            f'<text x="{PAD_X}" y="{y}" xml:space="preserve">'
            f'{tspan(key, CYAN)}{tspan("  ", GRAY)}{tspan(v, color)}</text></g>')
    # rule
    i = 2 + len(ROWS)
    yr = line_y(i)
    out.append(
        f'<g class="g"{op}>{"" if static else anim(i)}'
        f'<line x1="{PAD_X}" y1="{yr}" x2="{PAD_X+rule_w}" y2="{yr}" '
        f'stroke="#30363d" stroke-width="1"/></g>')
    # swatches
    i += 1
    y = line_y(i) - 8
    sw = 17
    swatch = []
    for s, col in enumerate(SWATCHES):
        swatch.append(
            f'<rect x="{PAD_X + s*(sw+5)}" y="{y}" width="{sw}" height="{sw}" '
            f'rx="3" fill="{col}"/>')
    out.append(f'<g class="g"{op}>{"" if static else anim(i)}{"".join(swatch)}</g>')

    out.append("</svg>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"wrote {OUT}: {W}x{H}")


if __name__ == "__main__":
    main()
