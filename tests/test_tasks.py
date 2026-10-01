"""D1: every task solver agrees with an independent brute-force method."""
import itertools

import numpy as np
import pytest

from ngs.tasks import TASKS, associative_recall, automaton, maze, reachability, shortest_path, sorting

SEEDS = range(25)


def rng(seed):
    return np.random.default_rng(seed)


@pytest.mark.parametrize("seed", SEEDS)
def test_reachability_matches_transitive_closure(seed):
    inst = reachability.make(12, rng(seed))
    n = inst["n"]
    reach = np.eye(n, dtype=bool)
    for u, v in inst["edges"]:
        reach[u, v] = True
    for k in range(n):                       # Warshall
        reach |= reach[:, [k]] & reach[[k], :]
    assert np.array_equal(inst["answer"], reach[inst["source"]].astype(np.int64))


@pytest.mark.parametrize("seed", SEEDS)
def test_shortest_path_matches_floyd_warshall(seed):
    inst = shortest_path.make(10, rng(seed))
    n, inf = inst["n"], 10**9
    d = np.full((n, n), inf, dtype=np.int64)
    np.fill_diagonal(d, 0)
    for (u, v), w in zip(inst["edges"], inst["weights"]):
        d[u, v] = min(d[u, v], w)
    for k in range(n):
        d = np.minimum(d, d[:, [k]] + d[[k], :])
    dist = inst["dist"]
    assert (dist >= 0).all(), "generator promises every node reachable"
    assert np.array_equal(dist, d[inst["source"]])
    # label: valid predecessor sets, checked edge by edge against the brute-force distances
    w = {(int(u), int(v)): int(x) for (u, v), x in zip(inst["edges"], inst["weights"])}
    expected = np.zeros((n, n), dtype=bool)
    for (u, v), x in w.items():
        expected[v, u] = d[inst["source"], u] + x == d[inst["source"], v]
    assert np.array_equal(inst["answer"], expected)
    assert not inst["answer"][inst["source"]].any()
    assert all(inst["answer"][v].any() for v in range(n) if v != inst["source"]), "every non-source node has a parent"


@pytest.mark.parametrize("seed", SEEDS)
def test_associative_recall_matches_linear_scan(seed):
    inst = associative_recall.make(16, rng(seed), vocab=64)
    expected = [int(inst["values"][list(inst["keys"]).index(q)]) for q in inst["queries"]]
    assert inst["answer"].tolist() == expected
    assert len(set(inst["keys"].tolist())) == 16


@pytest.mark.parametrize("seed", SEEDS)
def test_sorting_matches_bubble_sort(seed):
    inst = sorting.make(15, rng(seed))
    xs = inst["xs"].tolist()
    for i in range(len(xs)):
        for j in range(len(xs) - 1 - i):
            if xs[j] > xs[j + 1]:
                xs[j], xs[j + 1] = xs[j + 1], xs[j]
    assert inst["answer"].tolist() == xs


@pytest.mark.parametrize("seed", SEEDS)
def test_maze_is_perfect_and_path_is_valid(seed):
    n = 6
    inst = maze.make(n, rng(seed))
    grid, path = inst["grid"], inst["answer"]
    free = int(grid.sum())
    assert free == n * n + (n * n - 1), "perfect maze: n² cells + n²-1 passages (a spanning tree)"
    assert path[inst["start"]] == 1 and path[inst["goal"]] == 1
    assert (path <= grid).all(), "path only on free squares"
    cells = list(zip(*np.nonzero(path)))
    for r, c in cells:                       # a simple path: endpoints degree 1, interior degree 2
        deg = sum(path[r + dr, c + dc] for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= r + dr < grid.shape[0] and 0 <= c + dc < grid.shape[1])
        assert deg == (1 if (r, c) in (inst["start"], inst["goal"]) else 2)


@pytest.mark.parametrize("seed", SEEDS)
def test_percolated_maze_label_is_union_of_shortest_paths(seed):
    n = 4
    inst = maze.make(n, rng(seed), percolation=0.3)
    grid = inst["grid"]
    free = [tuple(p) for p in np.argwhere(grid == 1)]
    idx = {p: i for i, p in enumerate(free)}
    inf = 10**9
    d = np.full((len(free), len(free)), inf, dtype=np.int64)
    np.fill_diagonal(d, 0)
    for (r, c), i in idx.items():
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            j = idx.get((r + dr, c + dc))
            if j is not None:
                d[i, j] = 1
    for k in range(len(free)):                # Floyd–Warshall over free squares
        d = np.minimum(d, d[:, [k]] + d[[k], :])
    s, g = idx[inst["start"]], idx[inst["goal"]]
    expected = np.zeros_like(grid)
    for p, i in idx.items():
        if d[s, i] + d[i, g] == d[s, g]:
            expected[p] = 1
    assert np.array_equal(inst["answer"], expected)


@pytest.mark.parametrize("seed", SEEDS)
def test_maze_cell_view_matches_grid(seed):
    n = 6
    inst = maze.make(n, rng(seed), percolation=0.2)
    grid = inst["grid"]
    assert np.array_equal(inst["cell_answer"], inst["answer"][1::2, 1::2].reshape(-1))
    for u, v in inst["cell_edges"]:                       # every edge is an open passage between neighbours
        (ru, cu), (rv, cv) = divmod(int(u), n), divmod(int(v), n)
        assert abs(ru - rv) + abs(cu - cv) == 1
        assert grid[ru + rv + 1, cu + cv + 1] == 1
    open_passages = sum(int(grid[r, c]) for r in range(1, 2 * n) for c in range(1, 2 * n) if (r % 2) != (c % 2))
    assert len(inst["cell_edges"]) == 2 * open_passages     # both directions, none missing


def test_reachability_fraction_is_in_band():
    for n in (12, 64, 256):
        fr = [reachability.make(n, rng(s))["answer"].mean() for s in range(20)]
        assert all(0.2 <= f <= 0.8 for f in fr), (n, fr)


def test_percolation_creates_cycles():
    n = 8
    extra = [int(maze.make(n, rng(s), percolation=0.3)["grid"].sum()) - (2 * n * n - 1) for s in range(10)]
    assert all(e >= 0 for e in extra) and sum(extra) > 0, "perfect maze has 2n²-1 free squares; extras are cycles"


@pytest.mark.parametrize("seed", SEEDS)
def test_automaton_matches_stepwise_simulation(seed):
    inst = automaton.make(20, rng(seed), k=4)
    perms = list(itertools.permutations(range(4)))
    state = tuple(range(4))
    for t, g in enumerate(inst["word"]):
        p = perms[g]
        state = tuple(p[state[x]] for x in range(4))
        assert perms[inst["answer"][t]] == state


def test_generators_are_deterministic_per_seed():
    for name, make in TASKS.items():
        a, b = make(8, rng(7)), make(8, rng(7))
        assert np.array_equal(np.asarray(a["answer"]), np.asarray(b["answer"])), name
