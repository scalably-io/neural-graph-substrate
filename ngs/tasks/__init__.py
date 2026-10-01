"""Seeded algorithmic task generators with exact solvers (docs/DERIVATIONS.md D1).

Every generator has the signature ``make(n, rng) -> dict`` and returns plain numpy
arrays: the model inputs plus ``answer``. Instance size ``n`` is the axis of the
extrapolation ladder in docs/PREREGISTRATION.md.
"""
from . import associative_recall, automaton, maze, reachability, shortest_path, sorting

TASKS = {
    "reachability": reachability.make,
    "shortest_path": shortest_path.make,
    "associative_recall": associative_recall.make,
    "sorting": sorting.make,
    "maze": maze.make,
    "automaton": automaton.make,
}
