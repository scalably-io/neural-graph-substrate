"""Preregistered iteration budget T(n) per task family (docs/DERIVATIONS.md D3).

Review R2 (B3, M2): a single c·n tuned on a baseline arm does not transfer across
families, and picking the best step on test labels is an oracle. Instead every looped
arm gets the same budget, computed from the TASK before any model is trained:

    D(instance) = steps a purely local (one-hop-per-step) exact algorithm needs
    T(n)        = ceil(1.5 × q99 of D over 1000 instances, seed 0), at least 4

so the most local arm (G1) has enough steps, and global arms get more than they need
(they must stay stable: V4). Readout is at the last step; no step selection on labels.
"""
import math
from collections import deque
import heapq

import numpy as np

from .tasks import TASKS


def _bfs_depth(n: int, edges: np.ndarray, source: int) -> int:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[int(u)].append(int(v))
    dist = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return max(dist.values())


def _bellman_ford_rounds(inst: dict) -> int:
    """Fewest hops on any shortest path, maximised over nodes: the rounds a synchronous
    Bellman-Ford (one hop per step) needs."""
    n = inst["n"]
    adj = [[] for _ in range(n)]
    for (u, v), w in zip(inst["edges"], inst["weights"]):
        adj[int(u)].append((int(v), int(w)))
    best = {}
    heap = [(0, 0, inst["source"])]
    while heap:
        d, h, u = heapq.heappop(heap)
        if u in best:
            continue
        best[u] = h
        for v, w in adj[u]:
            if v not in best:
                heapq.heappush(heap, (d + w, h + 1, v))
    return max(best.values())


def required_steps(family: str, inst: dict) -> int:
    if family == "reachability":
        return _bfs_depth(inst["n"], inst["edges"], inst["source"])
    if family == "shortest_path":
        return _bellman_ford_rounds(inst)
    if family == "maze":
        n = inst["n"]
        dist = {inst["cell_start"]: 0}
        adj = [[] for _ in range(n * n)]
        for u, v in inst["cell_edges"]:
            adj[int(u)].append(int(v))
        queue = deque([inst["cell_start"]])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return dist[inst["cell_goal"]]
    if family == "sorting":
        return len(inst["xs"])
    if family == "associative_recall":
        return 2 * len(inst["keys"]) + len(inst["queries"])
    if family == "automaton":
        return len(inst["word"])
    raise ValueError(f"unknown family {family!r}")


def budget(family: str, n: int, samples: int = 1000, seed: int = 0, factor: float = 1.5, floor: int = 4) -> int:
    make = TASKS[family]
    d = [required_steps(family, make(n, np.random.default_rng(seed * 1_000_003 + i))) for i in range(samples)]
    return max(floor, math.ceil(factor * float(np.quantile(d, 0.99))))
