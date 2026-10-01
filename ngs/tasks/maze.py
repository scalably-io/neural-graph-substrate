"""Maze on an n×n cell grid: mark every square that lies on a shortest start→goal path.

Grid encoding is (2n+1)×(2n+1): 1 = free, 0 = wall, cells at odd coordinates.
With percolation 0 the maze is perfect (a spanning tree), so the label is the unique
path. Percolation > 0 opens extra interior walls, creating cycles; this defeats the
dead-end-filling shortcut that solves perfect mazes (evidence R4-032/R4-033), and the
label becomes the union of all shortest paths (well defined when several exist).
"""
from collections import deque

import numpy as np

STEPS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _bfs(grid: np.ndarray, src: tuple[int, int]) -> np.ndarray:
    h, w = grid.shape
    dist = np.full(grid.shape, -1, dtype=np.int64)
    dist[src] = 0
    queue = deque([src])
    while queue:
        r, c = queue.popleft()
        for dr, dc in STEPS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr, nc] and dist[nr, nc] == -1:
                dist[nr, nc] = dist[r, c] + 1
                queue.append((nr, nc))
    return dist


def solve(grid: np.ndarray, start: tuple[int, int], goal: tuple[int, int]) -> np.ndarray:
    """Squares v with d(start, v) + d(v, goal) = d(start, goal)."""
    ds, dg = _bfs(grid, start), _bfs(grid, goal)
    best = ds[goal]
    return ((ds >= 0) & (dg >= 0) & (ds + dg == best)).astype(np.int64)


def make(n: int, rng: np.random.Generator, percolation: float = 0.0) -> dict:
    """Randomised depth-first backtracker; then each remaining interior wall between two
    cells is opened with probability ``percolation``; start and goal are distinct random cells."""
    size = 2 * n + 1
    grid = np.zeros((size, size), dtype=np.int64)
    visited = np.zeros((n, n), dtype=bool)
    stack = [(int(rng.integers(n)), int(rng.integers(n)))]
    visited[stack[0]] = True
    grid[2 * stack[0][0] + 1, 2 * stack[0][1] + 1] = 1
    while stack:
        r, c = stack[-1]
        nbrs = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= r + dr < n and 0 <= c + dc < n and not visited[r + dr, c + dc]]
        if not nbrs:
            stack.pop()
            continue
        nr, nc = nbrs[rng.integers(len(nbrs))]
        visited[nr, nc] = True
        grid[2 * nr + 1, 2 * nc + 1] = 1
        grid[r + nr + 1, c + nc + 1] = 1   # the wall between (r,c) and (nr,nc)
        stack.append((nr, nc))
    if percolation > 0:
        walls = [(r, c) for r in range(1, size - 1) for c in range(1, size - 1)
                 if grid[r, c] == 0 and (r % 2) != (c % 2)]   # walls between two cells
        for r, c in walls:
            if rng.random() < percolation:
                grid[r, c] = 1
    cells =rng.choice(n * n, size=2, replace=False) if n > 1 else np.array([0, 0])
    start = (2 * int(cells[0] // n) + 1, 2 * int(cells[0] % n) + 1)
    goal = (2 * int(cells[1] // n) + 1, 2 * int(cells[1] % n) + 1)
    answer = solve(grid, start, goal)
    return {"n": n, "grid": grid, "start": start, "goal": goal, "percolation": percolation,
            "answer": answer, **cell_view(grid, start, goal, answer)}


def cell_view(grid: np.ndarray, start: tuple[int, int], goal: tuple[int, int], answer: np.ndarray) -> dict:
    """Cell-level encoding (the preregistered one): node i = cell (r, c) with i = r·n + c,
    an undirected edge per open passage, and a per-cell label. A cell is on a shortest
    grid path iff its centre square is, so the label is read at odd coordinates."""
    n = (grid.shape[0] - 1) // 2
    edges = []
    for r in range(n):
        for c in range(n):
            if c + 1 < n and grid[2 * r + 1, 2 * c + 2]:
                edges += [(r * n + c, r * n + c + 1), (r * n + c + 1, r * n + c)]
            if r + 1 < n and grid[2 * r + 2, 2 * c + 1]:
                edges += [(r * n + c, (r + 1) * n + c), ((r + 1) * n + c, r * n + c)]
    cell = lambda p: ((p[0] - 1) // 2) * n + (p[1] - 1) // 2
    return {"cell_edges": np.array(edges, dtype=np.int64).reshape(-1, 2),
            "cell_start": cell(start), "cell_goal": cell(goal),
            "cell_answer": answer[1::2, 1::2].reshape(-1).astype(np.int64)}
