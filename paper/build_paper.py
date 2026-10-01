#!/usr/bin/env python3
"""Build the research note from the evidence register: paper/paper.src.md -> paper/paper.md.

Every number in the prose is a {{placeholder}} filled here from evidence/claims.csv (parsed from the
claim's own quote or claim text), evidence/coverage.csv, docs/ and ngs/. The build fails on a typed
digit outside the ID allowlist, an unresolved placeholder, an unknown or ACCESS-FAILED claim ID, an
em or en dash, or a hype word. Reference: SR-2026-003's build_paper.py (house pattern).
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ngs.params import get  # noqa: E402

CLAIMS = {r["claim_id"]: r for r in csv.DictReader(open(ROOT / "evidence/claims.csv"))}
MATRIX = list(csv.DictReader(open(ROOT / "evidence/matrix.csv")))
COVER = list(csv.DictReader(open(ROOT / "evidence/coverage.csv")))
NUM = re.compile(r"\d+(?:\.\d+)?")


def qn(cid: str, i: int = 0) -> str:
    """i-th number in the claim's verbatim quote (so the prose number is the source's number)."""
    return NUM.findall(CLAIMS[cid]["quote"].replace(",", ""))[i]


def cn(cid: str, i: int = 0) -> str:
    """i-th number in the claim text (for table-cell quotes whose context lives in the claim)."""
    return NUM.findall(CLAIMS[cid]["claim"].replace(",", ""))[i]


def table(header, rows) -> str:
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] +
                     ["| " + " | ".join(r) + " |" for r in rows])


V: dict[str, str] = {}
V["version"] = "v0.1 (draft)"
V["date"] = "2026-10-01"                # pinned: a rebuild on another day reproduces the same note

# --- the ledger itself ---
by = {}
for r in CLAIMS.values():
    by[r["status"]] = by.get(r["status"], 0) + 1
V.update(n_claims=str(sum(v for k, v in by.items() if k != "ACCESS-FAILED")), n_failed=str(by.get("ACCESS-FAILED", 0)),
         n_reported=str(by["REPORTED"]), n_theorem=str(by["THEOREM"]), n_design=str(by["DESIGN"]),
         n_author=str(by["AUTHOR-CLAIM"]), n_code=str(by["CODE"]), n_derived=str(by["DERIVED"]),
         n_approaches=str(len(MATRIX)),
         n_workstreams=str(len([p for p in (ROOT / "evidence/research").glob("R*-*.csv")
                                if not p.name.endswith("-matrix.csv") and "review-additions" not in p.name])),
         n_blockers=str(sum(len(re.findall(r"^### B\d", p.read_text(), re.M)) for p in (ROOT / "docs/reviews").glob("R*-opus.md"))),
         n_reviews=str(len(list((ROOT / "docs/reviews").glob("R*-opus.md")))),
         n_reviews_total=str(len(list((ROOT / "docs/reviews").glob("*.md")))),
         n_negative=str(sum(1 for l in (ROOT / "docs/NEGATIVE-FINDINGS.md").read_text().splitlines() if l.startswith("| 20"))),
         q10_unknown=str(sum(1 for r in MATRIX if r["q10_more_iterations_help"].strip().lower().startswith("unknown"))),
         q10_na=str(sum(1 for r in MATRIX if r["q10_more_iterations_help"].strip().lower().startswith(("n/a", "na")))))
comps = [f"C{i}" for i in range(1, 14)]
V.update(n_systems=str(len(COVER)), n_components=str(len(comps)),
         best_y=str(max(sum(r[c] == "Y" for c in comps) for r in COVER)),
         never_y=", ".join(c for c in comps if all(r[c] != "Y" for r in COVER)))

# --- recurrence vs depth, per parameter and per FLOP ---
V.update(ouro_lo=qn("R2-016", 4), ouro_hi=qn("R2-016", 5),
         ouro_vs4b=f"{float(NUM.findall(CLAIMS['R2-199']['notes'])[-1]):.1f}",
         smelt_lo=qn("R2-089", 0), smelt_hi=qn("R2-089", 1),
         loop_r=qn("R5-092", 0), loop_small=qn("R5-092", 1), loop_match=qn("R5-092", 2), loop_cost=qn("R5-092", 3),
         phi=qn("R4-185", 0), bits=qn("R2-017", 0), hrm_gap=qn("R4-165", 0),
         ouro_peak=qn("R2-018", 0), onestep_from=cn("R2-036", 1), onestep_to=qn("R2-036", 1))
# --- routing evidence ---
V.update(lt2_dense=qn("R7-005", 1), lt2_sparse=qn("R7-006", 1),
         mpnn_max=qn("R4-001", -1), gat_full=qn("R4-002", -1), rt_plain=qn("R4-176", 0), rt_edge=qn("R4-176", 1),
         dnar_lo=qn("R6-011", 0), dnar_hi=qn("R6-011", 1), trm_plain=qn("R7-032", 1), trm_conv=qn("R7-033", 1),
         trm_len=qn("R7-032", 0), asent=qn("R6-016", 0), ndr=qn("R6-012", 0),
         gat_star=qn("R6-017", -3), niah_dense=qn("R7-010", -1), niah_hybrid=qn("R7-011", -1),
         niah_train=cn("R7-010", 3), niah_test=cn("R7-010", 2),
         rgnn_x=qn("R1-027", 0), rgnn_collapse=qn("R1-029", 0),
         dt_from=cn("R4-024", 0), dt_to=cn("R4-024", 2), dt_acc=qn("R4-024", 2))
# Guard: where a claim's value field holds a number, the number pulled from its quote must equal it
for key, cid in (("mpnn_max", "R4-001"), ("gat_full", "R4-002"), ("rt_plain", "R4-176"), ("lt2_dense", "R7-005"),
                 ("lt2_sparse", "R7-006"), ("trm_plain", "R7-032"), ("trm_conv", "R7-033"), ("asent", "R6-016"),
                 ("ndr", "R6-012"), ("dt_acc", "R4-024"), ("onestep_to", "R2-036"), ("smelt_lo", "R2-089"),
                 ("loop_small", "R5-092"), ("phi", "R4-185"), ("bits", "R2-017"), ("hrm_gap", "R4-165"),
                 ("rgnn_x", "R1-027"), ("rgnn_collapse", "R1-029"), ("dnar_hi", "R6-011"), ("ouro_peak", "R2-018"),
                 ("gat_star", "R6-017"), ("niah_hybrid", "R7-011")):
    assert float(V[key]) == float(NUM.findall(CLAIMS[cid]["value"])[0]), (key, cid, V[key], CLAIMS[cid]["value"])
# --- the proposed protocol (from the registry and the generated budget table) ---
budgets = (ROOT / "docs/generated/budgets.md").read_text()
reach = re.search(r"\| reachability \| (.+) \|", budgets).group(1).split(" · ")
maze = re.search(r"\| maze \| (.+) \|", budgets).group(1).split(" · ")
V.update(k=str(get("g2_k")), delta=str(get("equivalence_margin")), seeds_lo=str(get("seeds_min")), seeds_hi=str(get("seeds_max")),
         budget_factor=str(get("budget_factor")), param_tol=f"{get('param_match_tolerance') * 100:.0f}",
         reach_first=reach[0], reach_last=reach[-1], maze_first=maze[0], maze_last=maze[-1])
for key in ("reach_first", "reach_last", "maze_first", "maze_last"):
    n_, t_ = V[key].split(" → ")
    V[key] = f"{t_} steps at {n_} nodes" if key.startswith("reach") else f"{t_} steps at {n_} cells per side"

# --- LT2, the whole Table 5 (review N2: never one row) ---
lt2_rows = [CLAIMS[f"R6-0{i}"] for i in range(18, 26)]
def _lt2(r):
    name = re.match(r"(.+?) \d", r["quote"]).group(1)
    mixer = r["claim"].split(f"{name} (", 1)[1].rsplit("): NIAH", 1)[0]
    vals = re.findall(r"\d+\.\d", r["quote"])
    return [name, mixer] + vals[:15] + [r["claim_id"]]
LT2 = [_lt2(r) for r in lt2_rows]
by_name = {x[0]: x for x in LT2}
V.update(
         gat_star_mean=qn("R6-017", -4), gat_full_mean=qn("R6-017", -2))

# --- tables ---
V["T_lt2_know"] = table(["model (looped = weights shared over four steps)", "mixer", "SWDE", "SQuAD", "FDA", "TQA", "NQ", "DROP", "claim"],
                        [x[:2] + x[2:8] + [x[-1]] for x in LT2])
V["T_lt2_ret"] = table(["model", "test 1, shorter", "test 1, trained length", "test 1, longer", "test 2, shorter", "test 2, trained",
                        "test 2, longer", "test 3, shorter", "test 3, trained", "test 3, longer", "claim"],
                       [[x[0]] + x[8:17] + [x[-1]] for x in LT2])
V["n_long_quotes"] = str(sum(1 for r in CLAIMS.values() if r["status"] != "ACCESS-FAILED" and len(r["quote"].split()) > 40))
V["n_abstract_only"] = "PENDING_ABSTRACT"
mark = {"Y": "yes", "P": "partly", "N": "no", "?": "not established"}
V["T_coverage"] = table(["system"] + comps, [[r["system"]] + [mark[r[c]] for c in comps] for r in COVER])

# --- render + guards ---
src = (ROOT / "paper/paper.src.md").read_text()
used = set(re.findall(r"\{\{(\w+)\}\}", src))
missing = used - V.keys() - {"T_evidence"}
assert not missing, f"placeholders without a value: {sorted(missing)}"
ALLOWED = re.compile(r"\{\{\w+\}\}|SR-\d{4}-\d{3}|R\d-\d{3}|C1[0-3]|C\d|E\d{3}|D\d|V\d|[TG][0-3]\b|T1-sharp|"
                     r"\b\d{4}\.\d{4,5}\b|\b20\d\d\b|^#+ \d+(\.\d+)*|^\d+\. |Figure \d|Table \d|Appendix [A-C]|"
                     r"[Ss]ection \d(\.\d)?|answers? \d|\bS5\b|\bA5\b|\bLT2\b|\bN2\b|CC BY 4\.0|Apache-2\.0|Opus 5\.5|GPT-6", re.M)
stray = [ln for ln in ALLOWED.sub("", src).splitlines() if re.search(r"\d", ln)]
assert not stray, "typed numbers in template (use a placeholder):\n" + "\n".join(stray[:20])
out = re.sub(r"\{\{(\w+)\}\}", lambda m: V.get(m.group(1), m.group(0)), src)
cited = sorted(set(re.findall(r"\bR\d-\d{3}\b", out)), key=lambda c: (int(c[1]), int(c[3:])))
n_abs = sum(1 for c in cited if CLAIMS.get(c, {}).get("locator", "").strip().lower().startswith("abstract"))
out = out.replace("PENDING_ABSTRACT", str(n_abs))
for cid in cited:
    assert cid in CLAIMS, f"unknown claim {cid}"
    assert CLAIMS[cid]["status"] != "ACCESS-FAILED", f"cites ACCESS-FAILED claim {cid}"
for e in set(re.findall(r"\bE\d{3}\b", out)):
    assert f"| {e} |" in (ROOT / "EXPERIMENTS.md").read_text(), f"unknown experiment {e}"
for d in set(re.findall(r"\bD\d\b", out)):
    assert f"## {d}." in (ROOT / "docs/DERIVATIONS.md").read_text(), f"unknown derivation {d}"
ev = [[c, CLAIMS[c]["status"], CLAIMS[c]["claim"].replace("|", "/"), CLAIMS[c]["quote"].replace("|", "/"), CLAIMS[c]["source_url"]]
      for c in cited]
bad_dash = [l[:90] for l in out.splitlines() if "—" in l or "–" in l]
assert not bad_dash, "em/en dash in the note:\n" + "\n".join(bad_dash[:8])
out = out.replace("{{T_evidence}}", table(["ID", "status", "claim", "verbatim quote", "source"], ev))   # quotes stay verbatim
for w in ("revolutionary", "groundbreaking", "game-chang", "unprecedented", "breakthrough", "paradigm shift"):
    assert w not in out.lower(), f"hype word: {w}"
assert "PENDING" not in out, "unfilled late placeholder"
(ROOT / "paper/paper.md").write_text(out)
words = len(re.sub(r"^\|.*$", "", out, flags=re.M).split())
print(f"paper/paper.md: {words:,} words of prose (tables excluded), {len(used)} placeholders, {len(cited)} claim IDs cited")
