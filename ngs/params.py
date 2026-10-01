"""Single registry of budgets and hyperparameters.

Every entry: (value, provenance). Provenance is a claim_id from evidence/claims.csv,
a derivation ID, or "ASSUMPTION:<why>". Values mirror docs/PREREGISTRATION.md's
Constants block; tests/test_params_prereg.py fails if the two disagree.
"""

PARAMS = {
    "budget_samples": (1000, "D3; instances per T(n) cell, docs/generated/budgets.md"),
    "budget_seed": (0, "D3"),
    "param_match_tolerance": (0.05, "ASSUMPTION:prereg, stored parameters within ±5% across arms"),
    "equivalence_margin": (0.05, "ASSUMPTION:prereg, δ in nAUC units for superior/inferior/equivalent"),
    "seeds_min": (5, "ASSUMPTION:prereg; R6-014 (high OOD variance) argues against fewer"),
    "seeds_max": (15, "ASSUMPTION:prereg, cost cap of the power rule"),
    "budget_factor": (1.5, "D3"),
    "budget_quantile": (0.99, "D3"),
    "budget_floor": (4, "D3"),
    "g2_k": (8, "ASSUMPTION:prereg, fixed a priori; k=4 is an ablation"),
    "frontier_accuracy": (0.95, "ASSUMPTION:prereg, n* threshold (secondary metric)"),
    "informative_low": (0.1, "ASSUMPTION:prereg validity gate (review R2 B2)"),
    "informative_high": (0.9, "ASSUMPTION:prereg validity gate (review R2 B2)"),
    "families_required": (4, "ASSUMPTION:prereg, of 6 families"),
    "halting_step_ratio": (0.7, "ASSUMPTION:prereg V3"),
    "wallclock_ratio_limit": (2.0, "ASSUMPTION:prereg V5"),
    "tuning_trials": (8, "ASSUMPTION:prereg, per arm per family, in-distribution validation only"),
}


def get(name: str):
    return PARAMS[name][0]
