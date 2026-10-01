# Preregistration — DRAFT v0.3.1, 2026-10-01 (no experiment has run)

Status: **DRAFT**, awaiting Pavle's approval. It freezes (commit tagged `prereg-v1`) before the first non-smoke run; after that, changes go below as dated amendments with the reason, and the original text stays.

History:
- v0.1 was written before the survey.
- v0.2 followed review round 1.
- v0.3 follows review round 2 (`docs/reviews/R2-opus.md`: 4 blockers, 10 majors, all accepted). The v0.3 changes:
  - steps-matched primary comparison, with the readout at the last step (no oracle);
  - the task-derived budget T(n);
  - T1-sharp = ASEntmax;
  - G2 trained exactly like T1;
  - mutually exclusive outcomes with a validity gate;
  - V0 for the brief's critical question;
  - a seed power rule;
  - no interim stopping;
  - cell-level mazes;
  - predecessor labels for shortest path;
  - reachability instances band-sampled.
- v0.3.1 follows review round 3 (`docs/reviews/R3-opus.md`): the validity gate is now per comparison; shortest path gets edge weights as input and a defined scorer; Holm applies to both the superior and the equivalence side; seeds come from a t-based power rule (`ngs/stats.py`); T(n) comes from the generated table; V3 is measured against G2's own plateau step. Its remaining design questions are listed under "Open before freeze".

## The question
Inside a weight-tied loop, does hard, state-conditioned top-k routing (a sparse graph rebuilt from the state each step, without step supervision) extrapolate in instance size further than (a) dense softmax attention and (b) ASEntmax-sharpened attention, at matched stored parameters and an equal step budget, given that it never executes more matmul FLOPs per step?

- **V0** also answers the brief's literal question: does a looped (recurrent) model beat a fixed-depth Transformer per stored parameter?
- **Not decided here:** knowledge storage. Recurrence does not raise it (R2-017; R4-184 is the same study).

## Arms
| Arm | Routing | Training |
|---|---|---|
| T0 | dense softmax, L distinct blocks. **Iso-param** (width reduced to T1's parameters ±5%) decides V0; **iso-FLOP** (L = T(n_train) blocks at T1 width) reported | per-layer readouts, same loss weights as the looped arms |
| T1 | dense softmax, looped | shared recipe (below) |
| T1-sharp | **ASEntmax** (α-entmax with adaptive scalable temperature, R6-016), looped; fixed 1.5-entmax and Scalable-Softmax are ablations | shared recipe |
| G0 | task adjacency as a hard mask, L distinct blocks (iso-param) | per-layer readouts |
| G1 | task adjacency (sequences: window of ±2 positions) as a hard mask, looped | shared recipe |
| G2 | top-k of current scores, **k = 8 fixed**, no noise, no annealing, looped | shared recipe |
| G3 | G2 + learned halting head (ACT-style, min 2 steps, max T(n)); a confidence + convergence rule is reported as a control | shared recipe + ponder cost |

**Shared recipe for every looped arm:**
- Same optimiser, same schedule, same tuning budget (8 trials, chosen on in-distribution validation only).
- Stochastic loop counts T ~ U[⌈T(n_train)/2⌉, T(n_train)] in training (R6-015).
- Deep supervision at every sampled step.
- Stable state transition: negative-diagonal Ā, ρ(Ā) < 1 (R6-009).
- Input injection every step.
- A learned edge-feature bias on the scores, e_ij = β·A_ij + embed(w_ij) (edge weight w for shortest path; 0 where there is no edge), initialised at 0 and identical in every arm.
- Gumbel noise and dense-to-sparse k annealing for G2 are **ablations**, never in the headline arm (review R2 M1).

**Position and identity signals, fixed now (no pilot tuning):**
- Graph and maze-cell tasks: random node identifiers per instance, drawn from [0, 4096) and embedded.
- Sequence tasks: random sorted position identifiers from [0, 4096), embedded.

The same signal goes to every arm. This is our choice; a related published scheme (randomised positional encodings) is a lead not yet verified in our ledger.

## Task families, size variable n, ladder
| Family | n means | Train | Test ladder (×√2 steps) | Label (graph- / sequence-level exact match) |
|---|---|---|---|---|
| Reachability | nodes | 16 | 16 → 1024 | reachable set; instances band-sampled to 20–80% reachable |
| Shortest path | nodes | 16 | 16 → 1024 | each node points to one predecessor via a bilinear pointer head shared by all arms; correct iff the pointer is in the valid-predecessor set (`ngs/metrics.py::exact_parents`) |
| Maze | cells per side (cell-level graph, open passages = edges) | 9 | 9 → 33 | cells on any shortest path; size shift at percolation 0, structure shift at percolation 0.3 (trained at 0 only) |
| Sorting | length | 16 | 16 → 256 | sorted sequence |
| Associative recall | key-value pairs | 16 | 16 → 256 | queried values |
| S5 state tracking | length | 16 | 16 → 512 | every prefix product |

## Iteration budget (D3, `ngs/budget.py`)
- **Rule.** T(n) = max(4, ⌈1.5 × 99th percentile over 1000 instances (seed 0) of D⌉), where D = the steps a one-hop-per-step exact algorithm needs. The values are frozen in `docs/generated/budgets.md` (`scripts/build_budgets.py`), never typed:
  - BFS depth (reachability);
  - Bellman–Ford rounds (shortest path);
  - cell distance start → goal (maze);
  - sequence length (sorting, recall, S5).
- **Use.** It is computed from the task before any training. Every looped arm runs exactly T(n) steps (G3: at most T(n)).
- **Readout.** Taken at the last executed step. The best accuracy over steps is reported only as a labelled upper bound.

## Compute matching
- **Primary: steps-matched.** All looped arms get the same T(n). By D2, G2's executed matmul FLOPs per step are ≤ T1's (equal at k = N), so a G2 advantage cannot come from extra matmul compute.
- **Reported, not deciding:** executed and useful FLOPs (matmul and non-matmul separately); training FLOPs; peak memory; analytic bytes; wall-clock on the same GPU in the same session. ASEntmax's extra non-matmul cost is reported.
- **Calibration.** Selection and entmax costs are calibrated with a microbenchmark on the rented GPU before any compute statement.
- **Secondary: FLOP-matched view.** Per-size budgets F_j(n) = φ_j × T1's executed cost at (n, T(n)), φ ∈ {1/8, 1/4, 1/2, 1}. Each arm runs the largest T ≤ T(n) it can afford (a rule, not a label-based choice).

## Metric
- **Primary.** nAUC = mean exact-match accuracy over the test rungs with n > n_train, in [0, 1]. Seeds are paired across arms (same data and initialisation seed).
- **Secondary.** n* (the largest n with accuracy ≥ 0.95) and full accuracy-vs-n curves.

## Statistics and outcomes (per family and comparison G2 vs X; δ = 0.05 nAUC)
**Validity gate, per comparison** (`ngs/stats.py::informative`). A comparison G2 vs X is uninformative only if **both** arms are below 0.10 (joint floor) or **both** above 0.90 (joint ceiling). A large win for either arm is never dropped.

**Outcomes** (mutually exclusive), from the paired mean difference Δ = nAUC(G2) − nAUC(X):

| Outcome | Condition |
|---|---|
| superior | Δ ≥ δ and the 95% CI lower bound > 0 |
| inferior | Δ ≤ −δ and the 95% CI upper bound < 0 |
| equivalent | the 90% CI lies inside (−δ, δ) |
| inconclusive | otherwise |

**Seeds.**
- An EXPLORATORY pilot on separate seeds (T1 and G2; reachability and maze) estimates σ, the SD of paired Δ.
- n_seeds = the smallest n with (t₀.₉₅,ₙ₋₁ + t₀.₉₀,ₙ₋₁)·σ/√n ≤ δ, clipped to [5, 15] (`ngs/stats.py::n_seeds`): paired TOST, α = 0.05 per side, power 0.8 at true Δ = 0, t quantiles rather than the normal approximation. At δ = 0.05 this gives 5 seeds for σ ≤ 0.03, 8 for σ = 0.04, 11 for 0.05, 15 for 0.06.
- If 15 seeds are not enough, the family is reported as underpowered.
- Pilot data never enter a verdict. There is no interim stopping.

## Verdict rules
- **V0 (the brief's question: recurrence vs fixed depth per parameter).** T1 vs T0 (iso-param), using the outcome classes above, family by family.
- **V1 (routing beats recurrence + sharpness).** On an informative family, G2 is superior to **both** T1 and T1-sharp. This is an intersection–union test, so no adjustment within the family.
  - **p-value per family:** the intersection–union p = max(p vs T1, p vs T1-sharp), each a one-sided paired t-test of Δ > 0; "superior" also needs Δ ≥ δ.
  - **Supported overall:** Holm-adjusted p < 0.05 and Δ ≥ δ on ≥ 4 informative comparisons (both T1 and T1-sharp comparisons informative).
- **V1-null.** On an informative family, G2 is equivalent to, or inferior to, at least one of T1 and T1-sharp.
  - **"The gain is recurrence and sharpness, not routing":** this holds on ≥ 4 informative families, with the equivalence side Holm-adjusted too (TOST p = the larger one-sided p), so both verdicts face the same multiplicity correction.
  - Otherwise **inconclusive**, reported as such. V1 and V1-null cannot both hold on the same family.
- **V2 (topology as program).** G2 superior to G1 on ≥ 3 informative families.
- **V3 (halting).** G3 equivalent to G2 (classes above) at ≤ 0.7 × G2's **plateau step**: the smallest T at which G2's validation accuracy is within 0.01 of its accuracy at T(n), measured on in-distribution validation. (Against T(n) itself the rule would pass almost automatically; review R3.) The rule-based control is reported alongside.
- **V4 (time replaces depth).** For each looped arm at its largest informative rung, accuracy at T ∈ {T(n)/4, T(n)/2, T(n), 2·T(n)} is non-decreasing within δ, and the state norm stays bounded.
- **V5 (hardware).** G2's median wall-clock per instance is ≤ 2 × T1's at the same T(n), same GPU, same session.
- Every outcome is published, including null, inconclusive, floor and ceiling.

## Open before freeze (review R3 majors; decided with Pavle after the pilot, each as a dated amendment)
1. ASEntmax adds learned parameters and an explicit log n size signal to T1-sharp. Either give every arm the same log n feature, or count it as part of the sharpness control and state it.
2. G2 with k = 8 attends to half the nodes at n_train = 16 but to 8 of 1024 at test. Fixed k is the hypothesis; k ∝ log n is the alternative to decide.
3. Very long T(n) for global arms makes the last-step metric partly a stability test. Report accuracy at G2's and T1's plateau steps as secondary.
4. T0's depth and the model width d are unspecified, and the random-ID embedding tables may dominate the parameter count. Fix d and L from the T1 pilot, and exclude ID tables from the ±5% match (count them separately).
5. "Superior" has ~50% power when the true effect equals δ. Accept it (a conservative claim) or set δ_superior < δ_equivalence.
6. (Added after note review N2, revised after N3, 2026-10-01.) Looped **recurrent controls** are missing: a pure linear-recurrence mixer and a recurrence + attention hybrid. In LT2 the winner depends on the task: the dense loop leads on knowledge recall but scores zero on retrieval beyond the training length, while recurrent and hybrid mixers (with and without routing) extrapolate; on retrieval tests two and three the routed hybrid beats pure recurrence (R6-018–R6-028, R6-032). Without these arms, a G2 win over T1 could reflect "a different mixer beats a dense loop" rather than routing.

## Exploratory
- Anything run before the freeze is labelled EXPLORATORY in EXPERIMENTS.md and cannot decide a verdict.
- Ablations (Gumbel, k annealing, k = 4, fixed 1.5-entmax, Scalable-Softmax, max aggregation, β off, injection off, Ā = I + L2) are reported as secondary. They are costed separately and run only after the headline arms.

## Constants (pinned to `ngs/params.py` by `tests/test_params_prereg.py`)
```
budget_samples = 1000
budget_seed = 0
param_match_tolerance = 0.05
equivalence_margin = 0.05
seeds_min = 5
seeds_max = 15
budget_factor = 1.5
budget_quantile = 0.99
budget_floor = 4
g2_k = 8
frontier_accuracy = 0.95
informative_low = 0.1
informative_high = 0.9
families_required = 4
halting_step_ratio = 0.7
wallclock_ratio_limit = 2.0
tuning_trials = 8
```
