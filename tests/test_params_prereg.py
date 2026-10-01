"""The parameter registry and the preregistration's Constants block must agree (review R2 M9)."""
import re
from pathlib import Path

from ngs.params import PARAMS

PREREG = Path(__file__).resolve().parent.parent / "docs" / "PREREGISTRATION.md"


def prereg_constants() -> dict:
    text = PREREG.read_text()
    block = text.split("## Constants", 1)[1].split("```")[1]
    out = {}
    for line in block.strip().splitlines():
        name, value = (s.strip() for s in line.split("=", 1))
        out[name] = float(value) if re.search(r"[.]", value) else int(value)
    return out


def test_every_prereg_constant_is_in_params_with_the_same_value():
    pre = prereg_constants()
    assert pre, "Constants block not found"
    for name, value in pre.items():
        assert name in PARAMS, f"{name} missing from ngs/params.py"
        assert PARAMS[name][0] == value, (name, PARAMS[name][0], value)


def test_params_has_no_constant_the_prereg_lacks():
    assert set(PARAMS) == set(prereg_constants())


def test_budget_defaults_match_params():
    import inspect
    from ngs.budget import budget
    sig = inspect.signature(budget).parameters
    assert sig["factor"].default == PARAMS["budget_factor"][0]
    assert sig["floor"].default == PARAMS["budget_floor"][0]
    assert sig["samples"].default == PARAMS["budget_samples"][0]
    assert sig["seed"].default == PARAMS["budget_seed"][0]
