"""evidence/coverage.csv (the headline chart's data) must cite only real, citable claims."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIMS = {r["claim_id"]: r for r in csv.DictReader(open(ROOT / "evidence/claims.csv"))}
ROWS = list(csv.DictReader(open(ROOT / "evidence/coverage.csv")))
COMPONENTS = [f"C{i}" for i in range(1, 14)]


def test_values_are_in_the_scale():
    for r in ROWS:
        for c in COMPONENTS:
            assert r[c] in {"Y", "P", "N", "?"}, (r["system"], c, r[c])


def test_every_yes_or_partial_cites_a_claim_and_every_id_is_citable():
    for r in ROWS:
        for c in COMPONENTS:
            ids = [i for i in r[c + "_ids"].split(";") if i]
            if r[c] in ("Y", "P"):
                assert ids, (r["system"], c)
            for i in ids:
                assert i in CLAIMS, (r["system"], c, i)
                assert CLAIMS[i]["status"] != "ACCESS-FAILED", (r["system"], c, i)


def test_no_scored_system_has_every_component():
    assert all(sum(r[c] == "Y" for c in COMPONENTS) < len(COMPONENTS) for r in ROWS)
