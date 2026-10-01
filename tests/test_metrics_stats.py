"""Pins the preregistered scoring and statistics (review R3)."""
import numpy as np
import pytest

from ngs.metrics import exact_nodes, exact_parents
from ngs.stats import classify, informative, n_seeds
from ngs.tasks import shortest_path


def test_exact_parents_accepts_any_valid_parent_and_rejects_others():
    inst = shortest_path.make(40, np.random.default_rng(1))
    valid, src, n = inst["answer"], inst["source"], inst["n"]
    pick_first = np.array([np.flatnonzero(valid[v])[0] if v != src else 0 for v in range(n)])
    pick_last = np.array([np.flatnonzero(valid[v])[-1] if v != src else 0 for v in range(n)])
    assert exact_parents(inst, pick_first) and exact_parents(inst, pick_last)
    bad = pick_first.copy()
    v = next(v for v in range(n) if v != src)
    bad[v] = next(u for u in range(n) if not valid[v, u])
    assert not exact_parents(inst, bad)
    assert not exact_parents(inst, pick_first[:-1])


def test_exact_nodes_uses_cell_label_for_mazes():
    from ngs.tasks import maze
    inst = maze.make(5, np.random.default_rng(2))
    assert exact_nodes(inst, inst["cell_answer"].copy())
    assert not exact_nodes(inst, inst["answer"])          # grid-shaped prediction is the wrong encoding


def test_n_seeds_matches_t_based_power():
    assert n_seeds(sigma=0.01, delta=0.05) == 5                     # clipped up to the minimum
    assert n_seeds(sigma=0.5, delta=0.05) == 16                     # underpowered sentinel
    n = n_seeds(sigma=0.04, delta=0.05)
    assert 5 <= n <= 15
    from scipy import stats as st
    df = n - 1
    assert (st.t.ppf(0.95, df) + st.t.ppf(0.9, df)) * 0.04 / n ** 0.5 <= 0.05
    dfp = n - 2
    assert n == 5 or (st.t.ppf(0.95, dfp) + st.t.ppf(0.9, dfp)) * 0.04 / (n - 1) ** 0.5 > 0.05


def test_gate_is_per_comparison():
    assert informative(0.95, 0.30)          # a large win is NOT dropped as "ceiling"
    assert informative(0.05, 0.40)
    assert not informative(0.02, 0.05)      # joint floor
    assert not informative(0.95, 0.97)      # joint ceiling


@pytest.mark.parametrize("diffs,expected", [
    ([0.20, 0.22, 0.18, 0.21, 0.19], "superior"),
    ([-0.20, -0.22, -0.18, -0.21, -0.19], "inferior"),
    ([0.001, -0.002, 0.0, 0.002, -0.001], "equivalent"),
    ([0.3, -0.3, 0.25, -0.2, 0.1], "inconclusive"),
    ([0.03, 0.035, 0.032, 0.031, 0.034], "equivalent"),   # small, precise positive: equivalent, not superior
])
def test_classify_outcomes(diffs, expected):
    assert classify(diffs) == expected


def test_outcomes_are_exclusive_on_random_inputs():
    rng = np.random.default_rng(0)
    seen = set()
    for _ in range(2000):
        d = rng.normal(rng.uniform(-0.2, 0.2), rng.uniform(0.001, 0.2), size=rng.integers(5, 16))
        seen.add(classify(d))
    assert seen == {"superior", "inferior", "equivalent", "inconclusive"}
