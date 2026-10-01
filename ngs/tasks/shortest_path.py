"""Single-source shortest path on a connected weighted digraph.

Preregistered label (review R2 M10): for every node, the set of valid predecessors on a
shortest path (a node u is valid for v if dist[u] + w(u, v) == dist[v]); the source's
set is empty. Exact distances grow with n beyond any value seen in training, which
would floor every arm, so they are kept as ``dist`` for diagnostics only.
"""
import heapq

import numpy as np


def solve(n: int, edges: np.ndarray, weights: np.ndarray, source: int) -> np.ndarray:
    adj = [[] for _ in range(n)]
    for (u, v), w in zip(edges, weights):
        adj[u].append((v, int(w)))
    dist = np.full(n, -1, dtype=np.int64)
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if dist[u] != -1:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if dist[v] == -1:
                heapq.heappush(heap, (d + w, v))
    return dist


def valid_parents(n: int, edges: np.ndarray, weights: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """Boolean n×n matrix P with P[v, u] = True iff u is a valid shortest-path predecessor of v."""
    parents = np.zeros((n, n), dtype=bool)
    for (u, v), w in zip(edges, weights):
        if dist[u] >= 0 and dist[u] + w == dist[v]:
            parents[v, u] = True
    return parents


def make(n: int, rng: np.random.Generator, extra_edges_per_node: float = 1.0, max_weight: int = 9) -> dict:
    """A random spanning arborescence from the source (so every node is reachable)
    plus ``extra_edges_per_node * n`` random edges; integer weights in [1, max_weight]."""
    order = rng.permutation(n)
    source = int(order[0])
    tree = [(int(order[rng.integers(i)]), int(order[i])) for i in range(1, n)]
    extra = rng.integers(n, size=(int(extra_edges_per_node * n), 2))
    extra = [(int(u), int(v)) for u, v in extra if u != v]
    edges = np.array(sorted(set(tree) | set(extra)), dtype=np.int64).reshape(-1, 2)
    weights = rng.integers(1, max_weight + 1, size=len(edges)).astype(np.int64)
    dist = solve(n, edges, weights, source)
    return {"n": n, "edges": edges, "weights": weights, "source": source, "dist": dist,
            "answer": valid_parents(n, edges, weights, dist)}
