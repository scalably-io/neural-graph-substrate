"""D3: the iteration budget is computed from the task, not tuned on a model."""
import numpy as np

from ngs.budget import budget, required_steps
from ngs.tasks import maze, shortest_path


def test_bfs_depth_on_a_path():
    inst = {"n": 5, "edges": np.array([[0, 1], [1, 2], [2, 3], [3, 4]]), "source": 0}
    assert required_steps("reachability", inst) == 4


def test_bellman_ford_rounds_prefer_fewest_hops_among_shortest():
    # 0->2 directly (weight 2) ties with 0->1->2 (1+1): one hop suffices
    inst = {"n": 3, "edges": np.array([[0, 1], [1, 2], [0, 2]]), "weights": np.array([1, 1, 2]), "source": 0}
    assert required_steps("shortest_path", inst) == 1


def test_maze_steps_equal_cell_distance():
    inst = maze.make(6, np.random.default_rng(3))
    path_cells = int(inst["cell_answer"].sum())            # perfect maze: unique path
    assert required_steps("maze", inst) == path_cells - 1


def test_budget_is_deterministic_and_covers_local_needs():
    for family, n in (("reachability", 32), ("shortest_path", 32), ("maze", 6), ("automaton", 32)):
        t = budget(family, n, samples=50)
        assert t == budget(family, n, samples=50)
        needs = [required_steps(family, __import__("ngs.tasks", fromlist=["TASKS"]).TASKS[family](n, np.random.default_rng(10_000 + i))) for i in range(50)]
        assert np.mean([x <= t for x in needs]) >= 0.97, (family, t, max(needs))


def test_budget_grows_with_size():
    assert budget("maze", 9, samples=50) < budget("maze", 17, samples=50)
    assert budget("automaton", 16, samples=10) < budget("automaton", 64, samples=10)
