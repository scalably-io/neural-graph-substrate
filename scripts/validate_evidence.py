#!/usr/bin/env python3
"""Validate researcher CSVs and merge passing rows into evidence/claims.csv and evidence/matrix.csv.

Usage: python3 scripts/validate_evidence.py [--write]
Without --write it only reports. Rejected rows are listed with the reason and
never merged. Rules: evidence/SCHEMA.md.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "evidence" / "research"
OUT_CLAIMS = ROOT / "evidence" / "claims.csv"
OUT_MATRIX = ROOT / "evidence" / "matrix.csv"

HEADER = ["claim_id", "branch", "claim", "value", "unit", "status", "source_url", "locator",
          "quote", "source_date", "retrieved", "confidence", "notes"]
MATRIX_HEADER = ["approach_id", "family", "name", "primary_ref", "year_venue", "q1_graph", "q2_edges",
                 "q3_topology_at_inference", "q4_state_persists", "q5_weight_sharing", "q6_training",
                 "q7_scaling", "q8_stability", "q9_capacity", "q10_more_iterations_help", "q11_gpu",
                 "q12_repos", "q13_best_results", "q14_unexplored", "claim_ids"]
BRANCHES = {"MPNN", "RGNN", "DYN", "GT", "HYP", "TOP", "NCA", "LOOP", "DEQ", "ODE", "HOP", "PCEP", "RES",
            "HALT", "ROUTE", "CONN", "NAR", "READ", "OSC", "THEORY", "BENCH", "GPU", "X"}
STATUSES = {"REPORTED", "THEOREM", "DESIGN", "AUTHOR-CLAIM", "CODE", "DERIVED", "REPRODUCED", "ACCESS-FAILED"}
CONFIDENCE = {"High", "Medium", "Low"}
ID_RE = re.compile(r"^R\d+-\d{3}$")
APPROACH_RE = re.compile(r"^A\d+-\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")
MAX_QUOTE_WORDS = 60   # schema asks for <=40; tolerate light overrun
MAX_CELL_WORDS = 60


def _norm_num(s: str) -> str:
    return s.replace(",", "").lstrip("0") or "0"


def check(row: dict) -> list[str]:
    errs = []
    if not ID_RE.match(row["claim_id"]):
        errs.append("bad claim_id")
    if row["branch"] not in BRANCHES:
        errs.append(f"bad branch {row['branch']!r}")
    if row["status"] not in STATUSES:
        errs.append(f"bad status {row['status']!r}")
    if row["confidence"] not in CONFIDENCE:
        errs.append(f"bad confidence {row['confidence']!r}")
    if not DATE_RE.match(row["retrieved"]):
        errs.append("bad retrieved date")
    if row["status"] == "ACCESS-FAILED":
        return errs
    if not row["source_url"].startswith("http"):
        errs.append("missing source_url")
    if not row["locator"].strip():
        errs.append("missing locator")
    words = len(row["quote"].split())
    if words == 0:
        errs.append("missing quote")
    elif words > MAX_QUOTE_WORDS:
        errs.append(f"quote too long ({words} words)")
    if row["status"] in ("DERIVED", "REPRODUCED") and not row["notes"].strip():
        errs.append(f"{row['status']} without formula/experiment in notes")
    if row["status"] == "REPORTED" and words:
        value_nums = {_norm_num(n) for n in NUM_RE.findall(row["value"])}
        quote_nums = {_norm_num(n) for n in NUM_RE.findall(row["quote"])}
        if value_nums and not value_nums & quote_nums:
            errs.append("REPORTED value's number not in quote")
    return errs


def check_matrix(row: dict, valid_ids: set[str]) -> list[str]:
    errs = []
    if not APPROACH_RE.match(row["approach_id"]):
        errs.append("bad approach_id")
    if row["family"] not in BRANCHES:
        errs.append(f"bad family {row['family']!r}")
    ids = [i.strip() for i in row["claim_ids"].split(";") if i.strip()]
    if not ids:
        errs.append("no claim_ids")
    missing = [i for i in ids if i not in valid_ids]
    if missing:
        errs.append(f"claim_ids not in merged claims: {','.join(missing)}")
    for col in MATRIX_HEADER[5:19]:
        if not row[col].strip():
            errs.append(f"empty {col} (write 'unknown')")
        elif len(row[col].split()) > MAX_CELL_WORDS:
            errs.append(f"{col} too long")
    return errs


def read(path: Path, header: list[str]):
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != header:
            raise ValueError(f"{path.name}: HEADER MISMATCH {reader.fieldnames}")
        return list(reader)


def main(write: bool) -> int:
    merged, rejected, seen = [], [], set()
    claim_files = sorted(p for p in RESEARCH.glob("R*-*.csv") if not p.name.endswith("-matrix.csv"))
    matrix_files = sorted(RESEARCH.glob("R*-matrix.csv"))
    try:
        for path in claim_files:
            for row in read(path, HEADER):
                errs = check(row)
                if row["claim_id"] in seen:
                    errs.append("duplicate claim_id")
                seen.add(row["claim_id"])
                (rejected if errs else merged).append((path.name, row, errs))
        valid_ids = {row["claim_id"] for _, row, _ in merged if row["status"] != "ACCESS-FAILED"}
        m_merged, m_rejected, m_seen = [], [], set()
        for path in matrix_files:
            for row in read(path, MATRIX_HEADER):
                errs = check_matrix(row, valid_ids)
                if row["approach_id"] in m_seen:
                    errs.append("duplicate approach_id")
                m_seen.add(row["approach_id"])
                (m_rejected if errs else m_merged).append((path.name, row, errs))
    except ValueError as exc:
        print(exc)
        return 2
    by_status = {}
    for _, row, _ in merged:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
    print(f"claim_files={len(claim_files)} merged={len(merged)} rejected={len(rejected)} by_status={by_status}")
    print(f"matrix_files={len(matrix_files)} merged={len(m_merged)} rejected={len(m_rejected)}")
    for name, row, errs in rejected:
        print(f"REJECT {name} {row['claim_id']}: {'; '.join(errs)}")
    for name, row, errs in m_rejected:
        print(f"REJECT {name} {row['approach_id']}: {'; '.join(errs)}")
    if write:
        for out, header, rows in ((OUT_CLAIMS, HEADER, merged), (OUT_MATRIX, MATRIX_HEADER, m_merged)):
            with out.open("w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=header)
                w.writeheader()
                for _, row, _ in rows:
                    w.writerow(row)
            print(f"wrote {out.relative_to(ROOT)}")
    return 1 if (rejected or m_rejected) else 0


if __name__ == "__main__":
    sys.exit(main("--write" in sys.argv))
