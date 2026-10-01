"""State tracking: running composition of permutations in S_k (the S5 word problem by default).

S5 is non-solvable, so its word problem is NC1-complete; constant-depth Transformers
are expected to fail it at long lengths unless they are given more depth or steps
(the theory rows in the evidence ledger decide how this is cited). The answer is
the prefix product after every step, so the task is a sequence of n states.
"""
import itertools

import numpy as np


def group(k: int) -> np.ndarray:
    """All permutations of range(k), lexicographic; row i is element i."""
    return np.array(list(itertools.permutations(range(k))), dtype=np.int64)


def compose(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """(p ∘ q)(x) = p[q[x]]: apply q first, then p."""
    return p[q]


def solve(word: np.ndarray, k: int) -> np.ndarray:
    elems = group(k)
    index = {tuple(e): i for i, e in enumerate(elems)}
    state = np.arange(k)
    out = np.empty(len(word), dtype=np.int64)
    for t, g in enumerate(word):
        state = compose(elems[g], state)
        out[t] = index[tuple(state)]
    return out


def make(n: int, rng: np.random.Generator, k: int = 5) -> dict:
    order = len(group(k))
    word = rng.integers(order, size=n).astype(np.int64)
    return {"n": n, "k": k, "word": word, "answer": solve(word, k)}
