"""Directed reachability: label every node reachable from a source node.

Preregistered generator (review R2 minor 6): with plain ER sampling at mean out-degree
1.5, ~20% of instances reach only the source, a trivial instance. Instances are
rejection-sampled so the reachable fraction lies in [lo, hi] (default 0.2–0.8),
which also blocks the all-reachable / none-reachable degree heuristics (R4-067).
"""
from collections import deque

import numpy as np


def solve(n: int, edges: np.ndarray, source: int) -> np.ndarray:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    seen = np.zeros(n, dtype=np.int64)
    seen[source] = 1
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = 1
                queue.append(v)
    return seen


def _sample(n: int, rng: np.random.Generator, mean_out_degree: float) -> tuple[np.ndarray, int]:
    p = min(1.0, mean_out_degree / max(n - 1, 1))
    mask = rng.random((n, n)) < p
    np.fill_diagonal(mask, False)
    return np.argwhere(mask).astype(np.int64), int(rng.integers(n))


def make(n: int, rng: np.random.Generator, mean_out_degree: float = 1.5,
         lo: float = 0.2, hi: float = 0.8, max_tries: int = 10_000) -> dict:
    for _ in range(max_tries):
        edges, source = _sample(n, rng, mean_out_degree)
        answer = solve(n, edges, source)
        if lo <= answer.mean() <= hi:
            return {"n": n, "edges": edges, "source": source, "answer": answer}
    raise RuntimeError(f"no instance with reachable fraction in [{lo}, {hi}] after {max_tries} tries (n={n})")
