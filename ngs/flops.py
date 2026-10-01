"""Per-step forward FLOPs of one recurrent block, per instance (docs/DERIVATIONS.md D2).

Convention: 1 multiply-add = 2 FLOPs. Two counts are kept apart (review R1, B4):
- ``executed``: what the specified implementation actually runs (dense masked
  attention does all N² work even when most entries are masked).
- ``useful``: the sparse-analytic count (only selected / adjacent pairs).
Matmul and non-matmul FLOPs are separate, because a non-matmul FLOP costs ~16x a
matmul FLOP on an A100 (evidence R5-011).

Block = pre-norm attention (Q, K, V, O projections) + MLP with hidden width d_ff.
Routing rules (``arm``):
- "dense"  T0/T1: every node receives from all N nodes.
- "mask"   G0/G1: receives from task neighbours, implemented as dense masked
           attention (executed = dense; useful = 2·E·d for scores and aggregation).
- "topk"   G2/G3: dense scores, then top-k per receiver, then a gather-aggregate
           over the k selected values that reuses the scores (no second QKᵀ).
- "entmax" T1-sharp: dense scores and dense mixing (weights are sparse, the kernel is
           not), plus an entmax threshold found by bisection over each score row.

Per-step extras (review R2 M4), off by default so D2's core numbers stay comparable:
``readout_dim`` adds the per-step readout 2·N·d·r; ``inject`` adds an uncached input
injection 2·N·d². Selection and entmax costs are approximations; the preregistration
calibrates them with a GPU microbenchmark before any compute-matched claim.
"""
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class StepFlops:
    matmul: int
    nonmatmul: int

    @property
    def total(self) -> int:
        return self.matmul + self.nonmatmul


def _projections_and_mlp(n: int, d: int, d_ff: int) -> int:
    return 2 * n * 4 * d * d + 2 * n * 2 * d * d_ff


ENTMAX_BISECTION_ITERS = 25     # approximate; calibrated by microbenchmark before use
ENTMAX_OPS_PER_ITER = 4         # subtract threshold, clamp, power, row-sum per entry


def step_flops(arm: str, n: int, d: int, d_ff: int | None = None, k: int | None = None,
               edges: int | None = None, count: str = "executed",
               readout_dim: int = 0, inject: bool = False) -> StepFlops:
    d_ff = 4 * d if d_ff is None else d_ff
    base = _projections_and_mlp(n, d, d_ff) + 2 * n * d * readout_dim + (2 * n * d * d if inject else 0)
    if arm in ("dense", "entmax"):
        pairs_scored = pairs_mixed = n * n
        topk_ops = ENTMAX_BISECTION_ITERS * ENTMAX_OPS_PER_ITER * n * n if arm == "entmax" else 0
    elif arm == "mask":
        if edges is None:
            raise ValueError("mask arm needs edges")
        pairs_scored = pairs_mixed = n * n if count == "executed" else edges
        topk_ops = 0
    elif arm == "topk":
        if k is None or not 1 <= k <= n:
            raise ValueError("topk arm needs 1 <= k <= n")
        pairs_scored = n * n                      # scores are dense in every count: selection needs them
        pairs_mixed = n * k
        topk_ops = 0 if k == n else n * n * max(1, math.ceil(math.log2(k)))   # heap-style selection, approximate
    else:
        raise ValueError(f"unknown arm {arm!r}")
    matmul = base + 2 * pairs_scored * d + 2 * pairs_mixed * d
    softmax_ops = 5 * pairs_mixed                 # exp, max, sum, divide, subtract per mixed entry (approximate)
    return StepFlops(matmul=matmul, nonmatmul=softmax_ops + topk_ops)


def run_flops(arm: str, n: int, d: int, steps: int, **kw) -> StepFlops:
    s = step_flops(arm, n, d, **kw)
    return StepFlops(matmul=s.matmul * steps, nonmatmul=s.nonmatmul * steps)
