"""Sort a list of n integers."""
import numpy as np


def solve(xs: np.ndarray) -> np.ndarray:
    return np.array(sorted(xs.tolist()), dtype=np.int64)


def make(n: int, rng: np.random.Generator, vocab: int = 1024) -> dict:
    xs = rng.integers(vocab, size=n).astype(np.int64)
    return {"n": n, "xs": xs, "answer": solve(xs)}
