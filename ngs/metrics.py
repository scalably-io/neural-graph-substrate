"""Preregistered scoring: instance-level exact match per family (review R3, B2).

Every scorer takes the generator's instance and a model prediction in the same shape
as the label, and returns True only if the whole instance is right.
"""
import numpy as np


def exact_nodes(inst: dict, pred: np.ndarray) -> bool:
    """Reachability, maze (``cell_answer``), sorting, recall, S5: every element equal."""
    label = inst["cell_answer"] if "cell_answer" in inst else inst["answer"]
    pred = np.asarray(pred)
    return pred.shape == label.shape and bool(np.array_equal(pred, label))


def exact_parents(inst: dict, pred_parent: np.ndarray) -> bool:
    """Shortest path. ``pred_parent[v]`` = the node the model points to as v's predecessor
    (any value for the source). Correct iff every non-source node points to a member
    of its valid-predecessor set; several valid parents are all accepted."""
    valid = inst["answer"]                      # n×n bool, valid[v, u]
    n, src = inst["n"], inst["source"]
    pred_parent = np.asarray(pred_parent)
    if pred_parent.shape != (n,):
        return False
    return all(valid[v, int(pred_parent[v])] for v in range(n) if v != src)


SCORERS = {
    "reachability": exact_nodes,
    "maze": exact_nodes,
    "sorting": exact_nodes,
    "associative_recall": exact_nodes,
    "automaton": exact_nodes,
    "shortest_path": exact_parents,
}
