#!/usr/bin/env python3
"""Charts as inline SVG, generated from evidence/coverage.csv (never hand-drawn).

House chart pattern (locked 2026-09-18, as in SR-2026-003): our subject in brand green
#00c896, context in de-emphasis gray #9a978f; ink #0a0a09, muted #5a5a55, grid #e2dfd8,
paper #faf9f7; Instrument Serif title, Figtree labels, JetBrains Mono ticks; <title>
hover on every mark; role="img" + aria-label; responsive viewBox.
Validator (dataviz validate_palette.js, light, surface #faf9f7, run 2026-10-01): gray fails
the chroma floor by design (de-emphasis role, not a category); green/gray deutan ΔE 6.1
and green contrast 2.06:1 are relieved by SHAPE encoding (filled dot = yes, ring = partial,
small dot = no, "?" = not established) plus the full table in the paper.
Writes figures/coverage.svg and figures/index.html (preview).
"""
import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GREEN, GRAY, INK, MUTED, GRID, PAPER = "#00c896", "#9a978f", "#0a0a09", "#5a5a55", "#e2dfd8", "#faf9f7"
SERIF = "'Instrument Serif', Georgia, serif"
SANS = "Figtree, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', Menlo, monospace"
COMPONENTS = [
    ("C1", "persistent node states"), ("C2", "sparse directed graph"), ("C3", "shared message function"),
    ("C4", "shared update function"), ("C5", "recurrent evolution over T steps"), ("C6", "learned top-k routing / edge creation"),
    ("C7", "hyperedges"), ("C8", "state-conditioned topology"), ("C9", "persistent associative memory"),
    ("C10", "distributed readouts"), ("C11", "confidence / convergence signal"), ("C12", "learned adaptive halting"),
    ("C13", "topology and node roles evolve"),
]
WORD = {"Y": "has it", "P": "partly", "N": "does not", "?": "not established in our ledger"}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def mark(v: str, x: float, y: float, tip: str) -> str:
    t = f"<title>{esc(tip)}</title>"
    if v == "Y":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{GREEN}" stroke="{PAPER}" stroke-width="2">{t}</circle>'
    if v == "P":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{PAPER}" stroke="{GREEN}" stroke-width="2.5">{t}</circle>'
    if v == "N":
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{GRAY}">{t}</circle>'
    return (f'<g><rect x="{x-9:.1f}" y="{y-9:.1f}" width="18" height="18" fill="{PAPER}" fill-opacity="0"/>'
            f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{GRAY}">?</text>{t}</g>')


def chart_coverage(rows: list[dict]) -> str:
    n_c = len(COMPONENTS)
    W, x0, colw, top, rowh = 1100, 360, 46, 340, 34
    H = top + rowh * (len(rows) + 1) + 120
    xs = [x0 + colw * i + colw / 2 for i in range(n_c)]
    best = max(sum(r[c] == "Y" for c, _ in COMPONENTS) for r in rows)
    never = [c for c, _ in COMPONENTS if all(r[c] != "Y" for r in rows)]
    aria = (f"Which of the {n_c} components of the proposed self-routing recurrent graph appear in the {len(rows)} closest published systems. "
            f"The most any single system fully has is {best} of {n_c}. Components no system fully has: {', '.join(never)}.")
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(aria)}">',
         f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<text x="24" y="44" font-family="{SERIF}" font-size="27" fill="{INK}">Most parts exist somewhere. In our scoring, no system has more than {best} of {n_c}.</text>',
         f'<text x="24" y="70" font-family="{SANS}" font-size="13" fill="{MUTED}">The {n_c} components of the proposed recurrent self-routing graph (columns) in the {len(rows)} closest published systems (rows; the first is a union of looped-Transformer papers).</text>',
         f'<text x="24" y="88" font-family="{SANS}" font-size="13" fill="{MUTED}">Every filled or ringed mark rests on a cited claim whose quote supports it (hover for IDs). Fully present in no system: {", ".join(never)}.</text>']
    # legend (shape carries meaning, not colour alone)
    lx = 24
    for v, lab in (("Y", "has it"), ("P", "partly"), ("N", "does not"), ("?", "not established")):
        s.append(mark(v, lx + 8, 116, WORD[v]))
        s.append(f'<text x="{lx + 22}" y="120" font-family="{SANS}" font-size="12" fill="{INK}">{lab}</text>')
        lx += 22 + 8 * len(lab) + 26
    # column heads, rotated
    for (c, name), x in zip(COMPONENTS, xs):
        s.append(f'<text x="{x:.1f}" y="{top - 14}" font-family="{SANS}" font-size="11" fill="{INK}" '
                 f'transform="rotate(-55 {x:.1f} {top - 14})"><tspan font-family="{MONO}" fill="{MUTED}">{c} </tspan>{esc(name)}</text>')
    for i, r in enumerate(rows):
        y = top + rowh * i + rowh / 2
        if i % 2 == 0:
            s.append(f'<rect x="{x0 - 300}" y="{y - rowh / 2:.1f}" width="{colw * n_c + 300}" height="{rowh}" fill="{GRID}" fill-opacity="0.35"/>')
        s.append(f'<text x="{x0 - 12}" y="{y + 4:.1f}" text-anchor="end" font-family="{SANS}" font-size="12" fill="{INK}">{esc(r["system"])}</text>')
        for (c, name), x in zip(COMPONENTS, xs):
            ids = r[c + "_ids"].replace(";", ", ") or "none cited"
            s.append(mark(r[c], x, y, f'{r["system"]} · {c} {name}: {WORD[r[c]]} · {ids}'))
        ny = sum(r[c] == "Y" for c, _ in COMPONENTS)
        s.append(f'<text x="{x0 + colw * n_c + 10}" y="{y + 4:.1f}" font-family="{MONO}" font-size="11" fill="{MUTED}">{ny}/{n_c}</text>')
    # the candidate row: what the brief asks for, all thirteen
    yc = top + rowh * len(rows) + rowh / 2 + 10
    s.append(f'<line x1="{x0 - 300}" y1="{yc - rowh / 2 - 2:.1f}" x2="{x0 + colw * n_c + 40}" y2="{yc - rowh / 2 - 2:.1f}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<text x="{x0 - 12}" y="{yc + 4:.1f}" text-anchor="end" font-family="{SANS}" font-size="12" font-weight="600" fill="{INK}">The proposed design (the brief)</text>')
    for (c, name), x in zip(COMPONENTS, xs):
        s.append(mark("Y", x, yc, f"proposed design · {c} {name}: required"))
    s.append(f'<text x="{x0 + colw * n_c + 10}" y="{yc + 4:.1f}" font-family="{MONO}" font-size="11" fill="{INK}">{n_c}/{n_c}</text>')
    s.append(f'<text x="24" y="{H - 44}" font-family="{SANS}" font-size="12" fill="{MUTED}">Grey "does not" comes from the researchers\' coverage tables; "?" means we found no supporting claim in our ledger (re-scored after reviews N1 to N3 and Astra, 2026-10-01).</text>')
    s.append(f'<text x="{W - 24}" y="{H - 14}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">'
             f'scalably<tspan fill="{GREEN}">.</tspan>io · neural-graph-substrate</text>')
    s.append("</svg>")
    return "\n".join(s)


def main():
    rows = list(csv.DictReader(open(ROOT / "evidence/coverage.csv")))
    out = ROOT / "figures"
    out.mkdir(exist_ok=True)
    svg = chart_coverage(rows)
    (out / "coverage.svg").write_text(svg)
    (out / "index.html").write_text(f'<!doctype html><meta charset="utf-8"><title>SR-2026-006 charts</title>'
                                    f'<body style="margin:0;background:{PAPER};max-width:1040px"><figure style="margin:20px">{svg}</figure></body>')
    print("wrote figures/coverage.svg, figures/index.html")


if __name__ == "__main__":
    main()
