"""Preregistered statistics (docs/PREREGISTRATION.md; review R3 majors on power and gating).

- ``n_seeds``: paired TOST at true Δ = 0, two one-sided t-tests at level α, power 1−β,
  computed with t quantiles (not the normal approximation), clipped to [lo, hi].
- ``informative``: the per-comparison validity gate (review R3, B1): a comparison is
  uninformative only if BOTH arms are at the floor or BOTH at the ceiling.
- ``classify``: the four mutually exclusive outcomes from paired per-seed differences.
"""
import math

import numpy as np
from scipy import stats as st


def n_seeds(sigma: float, delta: float, alpha: float = 0.05, power: float = 0.8,
            lo: int = 5, hi: int = 15) -> int:
    """Smallest n with (t_{1-α,n-1} + t_{1-β/2,n-1})·σ/√n ≤ δ, clipped to [lo, hi].
    Returns hi + 1 if even hi seeds are not enough (the family is then underpowered)."""
    beta = 1.0 - power
    for n in range(2, 1000):
        df = n - 1
        if (st.t.ppf(1 - alpha, df) + st.t.ppf(1 - beta / 2, df)) * sigma / math.sqrt(n) <= delta:
            return min(max(n, lo), hi) if n <= hi else hi + 1
    return hi + 1


def informative(nauc_a: float, nauc_b: float, low: float = 0.1, high: float = 0.9) -> bool:
    return not (max(nauc_a, nauc_b) < low or min(nauc_a, nauc_b) > high)


def classify(diffs, delta: float = 0.05) -> str:
    """diffs = paired per-seed nAUC(G2) − nAUC(X). Outcomes are mutually exclusive."""
    d = np.asarray(diffs, dtype=float)
    n = len(d)
    mean = float(d.mean())
    se = float(d.std(ddof=1) / math.sqrt(n)) if n > 1 else float("inf")
    t95, t90 = st.t.ppf(0.975, n - 1), st.t.ppf(0.95, n - 1)
    lo95, hi95 = mean - t95 * se, mean + t95 * se
    lo90, hi90 = mean - t90 * se, mean + t90 * se
    if mean >= delta and lo95 > 0:
        return "superior"
    if mean <= -delta and hi95 < 0:
        return "inferior"
    if -delta < lo90 and hi90 < delta:
        return "equivalent"
    return "inconclusive"
