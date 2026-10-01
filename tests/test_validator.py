"""The evidence validator must reject each defect it claims to catch."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("validate_evidence", ROOT / "scripts" / "validate_evidence.py")
ve = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ve)

GOOD = {
    "claim_id": "R9-001", "branch": "LOOP", "claim": "Looped model reaches 0.98 accuracy", "value": "0.98",
    "unit": "accuracy", "status": "REPORTED", "source_url": "https://arxiv.org/abs/0000.00000",
    "locator": "Table 2", "quote": "our looped model reaches 0.98 accuracy at length 64", "source_date": "2025",
    "retrieved": "2026-10-01", "confidence": "High", "notes": "vs fixed-depth, param-matched",
}


def row(**kw):
    return {**GOOD, **kw}


def test_good_row_passes():
    assert ve.check(row()) == []


def test_each_defect_is_rejected():
    cases = {
        "bad claim_id": row(claim_id="R9-1"),
        "bad branch": row(branch="TRANSFORMERS"),
        "bad status": row(status="MEASURED"),
        "bad confidence": row(confidence="high"),
        "bad retrieved date": row(retrieved="1 Oct 2026"),
        "missing source_url": row(source_url="arxiv.org/abs/1"),
        "missing locator": row(locator="  "),
        "missing quote": row(quote=""),
        "quote too long": row(quote="0.98 " + "word " * 60),
        "DERIVED without formula": row(status="DERIVED", notes=""),
        "number not in quote": row(value="0.97"),
    }
    for expected, bad in cases.items():
        errs = ve.check(bad)
        assert len(errs) == 1 and expected in errs[0], (expected, errs)


def test_access_failed_needs_no_quote():
    assert ve.check(row(status="ACCESS-FAILED", quote="", locator="", source_url="")) == []


def test_matrix_rejects_unknown_claim_ids_and_empty_cells():
    mrow = {h: "unknown" for h in ve.MATRIX_HEADER}
    mrow.update(approach_id="A9-01", family="LOOP", name="x", primary_ref="y", year_venue="2025",
                claim_ids="R9-001")
    assert ve.check_matrix(mrow, {"R9-001"}) == []
    assert any("not in merged" in e for e in ve.check_matrix(mrow, set()))
    assert any("empty q2_edges" in e for e in ve.check_matrix({**mrow, "q2_edges": ""}, {"R9-001"}))
    assert any("no claim_ids" in e for e in ve.check_matrix({**mrow, "claim_ids": ""}, {"R9-001"}))
