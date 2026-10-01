"""Multi-query associative recall: n key-value pairs, then queries over the keys."""
import numpy as np


def solve(keys: np.ndarray, values: np.ndarray, queries: np.ndarray) -> np.ndarray:
    table = dict(zip(keys.tolist(), values.tolist()))
    return np.array([table[q] for q in queries.tolist()], dtype=np.int64)


def make(n: int, rng: np.random.Generator, vocab: int = 4096, n_queries: int | None = None) -> dict:
    """Distinct keys (so recall is well defined); values may repeat. Keys and values
    share one vocabulary of size ``vocab``, which must be ≥ n."""
    if vocab < n:
        raise ValueError("vocab must be >= n for distinct keys")
    keys = rng.choice(vocab, size=n, replace=False).astype(np.int64)
    values = rng.integers(vocab, size=n).astype(np.int64)
    queries = rng.choice(keys, size=n_queries or n, replace=True).astype(np.int64)
    return {"n": n, "keys": keys, "values": values, "queries": queries,
            "answer": solve(keys, values, queries)}
