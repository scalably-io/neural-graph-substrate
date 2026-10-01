# Review R2 (Opus, fresh context): SYNTHESIS v0.2 + PREREGISTRATION draft v0.2

Reviewer: adversarial, fresh context, 2026-10-01. Read-only, except for this file. Findings (a)–(f) were written before reading `R1-opus.md` or `NEGATIVE-FINDINGS.md`.

## (a) Verdict

**FIX-THEN-SHIP.** The literature verdict (§0 and §12, LM substrate: no) is mostly supported and honestly hedged. The preregistration's primary metric has four defects that need fixing before `prereg-v1` is frozen:
- a fixed FLOP grid that floors every arm at out-of-distribution sizes;
- an equivalence verdict that can be reached by construction;
- test-set oracle selection of T;
- a sharpness control that is the weak variant.

Each of these alone could make the headline result an artefact.

---

## (b) BLOCKERS

### B1. The fixed FLOP grid makes AUC_F identically 0 for every arm over most of the ladder, and it credits G2's cheaper aggregation as "inductive bias"

- **Where:** PREREGISTRATION, Matching rules.
- **Sentence:** "Comparisons are made at matched executed-FLOP budgets on a fixed grid F ∈ {F₁…F₆} per task, log-spaced, set from T1's cost at n_train." Primary metric: "AUC_F … at FLOP budget F".
- **What is wrong.** A per-instance budget fixed at n_train cannot buy even one dense step a few rungs up the ladder.

  Computed with `ngs.flops` (d = 128, reachability, n_train = 16). F₆ is taken as T1's cost at n_train with T_max = c·n_train, which is the most generous reading.

  | c | n where T1 can afford < 1 step | T1 steps affordable at n = 1024 | steps needed at n = 1024 (T_max = c·n) |
  |---|---|---|---|
  | 0.5 | 128 (0.87 steps) | 0.05 | 512 |
  | 1 | 256 (0.76 steps) | 0.11 | 1024 |
  | 2 | 512 (0.61 steps) | 0.22 | 2048 |

  The consequences:
  - Beyond about 8–16× n_train every arm's credited accuracy is 0 at every budget.
  - ΔAUC_F there is exactly 0 with zero seed variance. That is the regime the "≥ 16 × n_train" ladder was added to probe.
  - In the remaining region, G2 affords more steps per budget than T1, because its executed matmul is lower:
    - G2/T1 = 0.708 at N = 1024 and 0.536 at N = 14,161, including non-matmul at a 16× weight.
    - So G2 runs 1.4–1.9× more steps at large n.
    - This contradicts §4: "The comparison is about inductive bias, not efficiency."
- **Evidence:** `ngs/flops.py` output above (CODE/DERIVED, this review); SYNTHESIS §4.
- **Fix.**
  1. Define budgets per n, as F_j(n) = φ_j × (T1 cost per step at n) × T_max(n) with φ_j ∈ {1/32 … 1}, so the grid scales with instance cost.
  2. Report a steps-matched view (same T for every arm) alongside it, so inductive bias is separated from per-step efficiency.
  3. State which of the two decides V1.

### B2. The null verdict ("the gain is recurrence and sharpness, not routing") can be produced by floors and ceilings alone, and TOST with 5 seeds is likely underpowered

- **Where:** PREREGISTRATION, Verdict rules, V1-null.
- **Sentence:** "G2 is declared equivalent to max(T1, T1-sharp) on a family if the 90% CI of ΔAUC_F lies within ±δ, with δ = 0.05 × the AUC range of the ladder, at ≥ 4 of 6 budgets."
- **What is wrong.**
  1. **Trivial equivalence.** If every arm reaches 100% at n_train and 0% beyond 2× (common on these tasks), or every arm is floored (B1), the CI collapses inside ±δ and the program publishes its prior as a finding. Nothing in the rule requires that any arm actually extrapolates.
  2. **"AUC range of the ladder" is undefined.** It could mean the theoretical maximum (ladder width × 1.0) or the observed range across arms. If observed, δ shrinks toward 0 exactly when everything floors.
  3. **Power is too low.** With 5 unpaired seeds per arm, df ≈ 8, the 90% CI half-width is ≈ t₀.₉₅ × SD × √(2/5) ≈ 1.18 SD.
     - Equivalence at a true Δ = 0 then needs a seed SD of normalised AUC below δ / 1.18 ≈ 4.2 percentage points.
     - Length or size extrapolation is notoriously seed-sensitive: R4-123 "high sensitivity to random seed (±6–8%)" on COGS.
     - A 2026 looped-Transformer paper reports length generalisation in looped Transformers is "brittle, yielding high out-of-distribution (OOD) variance, even across well-performing in-distribution solutions" (https://arxiv.org/abs/2606.29983, abstract, fetched 2026-10-01).
     - So the non-trivial outcome is likely "inconclusive" by construction, while the trivial one (point 1) is likely "equivalent". Both are biased toward the stated prior.
  4. **Outcome coverage is incomplete.**
     - V1 and V1-null are not exclusive: a CI of [0.01, 0.04] with δ = 0.05 satisfies both.
     - There is no outcome for "G2 worse than max(T1, T1-sharp)". This is the likely result if selection collapses (§11), and it currently falls into "inconclusive".
- **Fix.**
  - Define δ in absolute normalised-AUC units, frozen.
  - Add a validity gate: a family counts toward V1 or V1-null only if some arm reaches n* ≥ 2·n_train and the positive-control contrast T1 vs T0 is detected.
  - Pair seeds (same data seed across arms) and run a power analysis on pilot variance before the freeze (or preregister a sequential seed rule).
  - Add "V1-inferior".
  - Make the verdicts mutually exclusive, with an explicit tie-break.

### B3. "Best over T" is an oracle stopping time chosen on test labels

- **Where:** PREREGISTRATION, Iteration budget.
- **Sentence:** "the accuracy credited at budget F is the best over T whose executed FLOPs ≤ F."
- **What is wrong.**
  - The credited accuracy is the maximum over roughly log₂(c·n) checkpoints, selected per (arm, n, F) on the test labels.
  - It is optimistic for every arm, and most optimistic for arms whose accuracy-vs-T curve oscillates or overthinks (R2-018, R4-034). So it is not arm-neutral.
  - The project's own ledger flags the same flaw in DT-Recall: R4-024 note, "Peak accuracy chosen post hoc over iterations (selection on test curve)."
  - It also breaks V3. G3 halts for real, while G2 is credited with an oracle T, so "G3 keeps G2's AUC_F within δ" compares a real policy with an oracle. "G2's mean executed iterations" has no definition when T is oracle-picked.
- **Fix.**
  - Pick T(n) per arm on a held-out validation set at each n, or freeze a rule (e.g. T = T_max(n), or last step) as primary.
  - Report best-over-T only as a labelled upper bound.

### B4. T1-sharp uses the weak sharpening variant, and §0.4 attributes the strong variant's result to it

- **Where:**
  - SYNTHESIS §0.4: "α-entmax (R6-003, up to 1000× length extrapolation on synthetic tasks)".
  - SYNTHESIS §3 and PREREGISTRATION: "T1-sharp | 1.5-entmax, looped (Scalable-Softmax as an ablation)".
- **What is wrong.** The 1000× result belongs to ASEntmax, i.e. α-entmax with a learnable, length-scaled temperature. The same abstract says ASEntmax "substantially outperforms softmax, scalable softmax, and fixed-temperature α-entmax baselines, achieving up to 1000× length extrapolation" (`evidence/sources/R6/2506.16640.abstract.txt`; the R6-003 source).
  - Fixed 1.5-entmax is the baseline that paper beats.
  - The reframed question is "routing beyond sharpness", so a weak sharpness control biases V1 toward G2 and makes a positive result uninterpretable.
- **Fix.**
  - T1-sharp = ASEntmax as specified in R6-003's source, with fixed 1.5-entmax and SSMax as ablations.
  - Correct §0.4 to "ASEntmax (α-entmax + adaptive scalable temperature)".
  - Consider NDR geometric attention as well (M7).

---

## (c) MAJOR

### M1. Routing is not the single variable between T1, T1-sharp and G2: Gumbel noise and a dense-to-sparse curriculum exist only in G2

- **Where:** SYNTHESIS §3 ("T1 vs G2 then differ only in the routing rule") and §4.3 ("g_ij is Gumbel noise in training only and k is annealed from N down to k").
- **What is wrong.**
  - Score noise is a regulariser and exploration device.
  - k-annealing makes G2 train as T1 (k = N) first and then sparsify, i.e. a curriculum that T1 and T1-sharp do not get.
  - Ablation 6 turns these off inside G2, but the headline contrast carries them.
- **Fix.** Either:
  - give T1 and T1-sharp the matched treatments (Gumbel or logit noise of the same scale; α or temperature annealing toward the final sharpness over the same schedule); or
  - make the headline G2 noise-free and fixed-k, and report the annealed version as an ablation.

  Also state whether β is learned per arm. β·A interacts differently with a soft normaliser and with a hard top-k cut: with large β, G2 degenerates to G1 plus extra edges.

### M2. Every pilot-set constant is tuned on a baseline arm, and c does not transfer across families

- **Where:**
  - PREREGISTRATION: "c fixed in the pilot as the smallest value at which G1 reaches its own plateau on reachability at n_train".
  - "The PE scheme is chosen in a pilot on T1 only".
  - "F … set from T1's cost".
- **What is wrong.**
  1. **The pilot favours the baselines, and so the null.** PE, c and F are all chosen to suit T1 or G1. That is conservative for V1 but biased toward V1-null, which the draft says is its prior.
  2. **A single linear c cannot fit both families.** Measured with the repository's generators (30–50 seeds each, this review):
     - Reachability on ER with mean out-degree 1.5 needs few steps: source eccentricity is 3.3 on average (max 11) at n = 16 and 16.1 (max 30) at n = 1024.
     - So any c that suffices at n = 16 gives T_max(1024) = c·1024, roughly 20–30× more steps than the task needs, and those steps are paid in FLOPs.
     - Mazes need far more steps than c·side. The mean shortest-path length in grid squares is 4.0× the side at 9×9, 12.1× at 37×37 and 17.1× at 52×52, with a maximum of 2,545 squares at 59×59.
     - A c tuned on reachability (where steps grow ~log n) under-budgets diameter-bound arms on mazes, unless "n" means grid squares, in which case it is enormous (M3).
  3. **"n" is never defined per family:** nodes, side, pairs or length.
- **Fix.**
  - Define n and T_max(n) per family from the task's diameter scaling (log n for ER reachability; path length for mazes).
  - Choose PE on a union of T1 and G2 pilots by a frozen rule, or treat PE as a crossed factor.

### M3. The maze rung is 14,161 grid squares, not 3,481 nodes, and the feasibility claim rests on an unstated encoding choice

- **Where:**
  - SYNTHESIS §0.5: "The 59×59-maze rung (3,481 nodes)".
  - SYNTHESIS §12: "dense at ~3.5k nodes".
- **What is wrong.** `ngs/tasks/maze.py` emits a (2n+1)² grid. `maze.make(59)` returns a (119, 119) grid (6,961 free squares), and the label lives on the grid. 3,481 is only correct if cells are nodes and walls become features or edges, which is not specified.
- **Back-of-envelope.**

  Assumptions:
  - d = 128, d_ff = 512, 4 heads;
  - RTX 4090 ≈ 165 TFLOP/s dense bf16 tensor peak and ≈ 1 TB/s memory bandwidth. These figures come from memory and are **unverified**;
  - ~40% MFU;
  - 500 test mazes per percolation level.

  | Encoding | N | T1 FLOPs/step (`ngs.flops`) | G2 FLOPs/step | Score matrix per head (bf16) |
  |---|---|---|---|---|
  | grid squares | 14,161 | 1.08e11 | 5.7e10 + selection | 2.0e8 entries = 401 MB |
  | cells | 3,481 | 7.6e9 | 4.5e9 | (≈ 16× cheaper per step) |

  - **Grid encoding, T1.** A local arm needs about 1,000–2,500 steps; DT-Recall used 984 (R4-025). At T = 2,500 that is 2.7e14 FLOP per maze, about 4 s with FlashAttention, so feasible.
  - **Grid encoding, entmax and G2.** T1-sharp (entmax) and G2 (`torch.topk`) must materialise the score matrix: 1.6 GB per instance at 4 heads, more in fp32 plus sort workspace, so batch ≤ 4 on 24 GB.
    - Score traffic alone is ≥ 3 GB per step, so ≥ 3 ms per step and ≥ 8 s per maze at 2,500 steps, before entmax's sort or bisection.
    - 4 materialising configurations × 5 seeds × 3 percolations × 500 mazes is about 30,000 maze-evaluations, or about 70–125 GPU-hours for the top rung's evaluation alone.
    - The 52×52 rung adds about 60% of that.
    - Mazes alone could consume most of the 170–670 GPU-hour budget.
  - **Cell encoding.** About 16× cheaper per step, and comfortable.
  - **If n means grid squares** and c ≈ 1, T_max = 14,161, which multiplies all of the above by about 5.7.
- **Fix.** Fix the maze encoding and n in the preregistration, and re-derive the cost from `ngs.flops` with the actual T_max.

### M4. The FLOP model omits the entmax cost and understates top-k selection, both in ways that move matched-FLOP results

- **Where:** `ngs/flops.py` and D2.
- **What is wrong.**
  - **No entmax arm.** T1-sharp can only be counted as "dense" softmax (5·N² non-matmul). Exact 1.5-entmax needs a sort (≈ N² log₂ N per head) or about 20–30 bisection passes over N² entries. At N = 1024 that is about 2–6× the softmax term, and it is entirely non-matmul.
  - **Selection is cheaper in the model than softmax.** The model makes G2 cheaper than T1 in both matmul and non-matmul: G2's non-matmul is 5Nk + 3N², below T1's 5N², at k = 8. Yet the cited measurement says row-wise top-k takes 11.6–26.9% of training time (R5-081). The heap-style N²·⌈log₂k⌉ term does not represent radix-select passes on a GPU.
  - **Excluded per-step terms.** These are excluded from the per-step count although they run every step in looped arms:
    - the injection term B̄·Enc(X), if B̄ is applied per step (it can be cached);
    - per-step readouts (§4.6 reads out at every step, needed for best-over-T);
    - LayerNorms;
    - the G3 halting head and the convergence rule's ‖H^{t+1} − H^t‖.

    They are small, but they differ between T0/G0 (no injection) and the looped arms.
- **Fix.**
  - Add an `entmax` arm with sort and bisection variants.
  - Calibrate the selection and entmax terms against a measured microbenchmark on the target GPU, and report the calibration.
  - Count per-step readout and halting.
  - Pin all of this in `tests/test_flops.py`.

### M5. The owner's critical question (capacity per stored parameter vs a fixed-depth Transformer) has no verdict rule, and T0/G0 are under-specified

- **Where:**
  - BRIEF: "Can this architecture achieve greater reasoning/computational capacity per stored parameter than a conventional fixed-depth Transformer…?"
  - PREREGISTRATION: V1–V5 never mention T0.
- **What is wrong.**
  - T0 is trained but nothing decides on it.
  - How T0 and G0 (L distinct blocks, no loop) are evaluated under a T sweep and an F grid is undefined.
  - The iso-FLOP T0 "L = T blocks at T1 width": which T? T_train, or T_max(n), which varies with n?
  - Whether T0 and G0 get per-layer deep supervision is also unspecified.
- **Fix.**
  - Add V0: T1 and G2 vs T0 (iso-param), with the same statistics. This is the brief's literal question, and the expected positive control for B2.
  - Specify L, readouts and evaluation for the non-looped arms.

### M6. Selection and multiplicity are unspecified, and the gate in §12 is an unregistered interim analysis

- **Where:**
  - PREREGISTRATION V1: "G2 (best k) beats max(T1, T1-sharp)".
  - SYNTHESIS §12 gate 5: "If G2 is TOST-equivalent … there, finish the remaining families at minimum size and publish the negative."
- **What is wrong.**
  - **Selection level.** "Best k" and "max" are selected on what data, and at what level (per seed, per budget or per family)? A max over noisy estimates is biased upward on both sides.
  - **Correlated budgets.** The six budgets are nested and highly correlated, so "≥ 4 of 6 budgets × ≥ 4 of 6 families" has no stated family-wise error rate.
  - **The gate conflicts with the preregistration.** Gate 5 stops on 2 pilot families and shrinks the rest, while the preregistration requires ≥ 4 of 6 families. That is optional stopping conditional on the interim result.
- **Fix.**
  - Pre-specify k and the T1 variant on validation data, or include the selection in a bootstrap.
  - State the family-wise α, by simulation under the null if necessary.
  - Either preregister the interim rule with its α-spending, or delete gate 5.

### M7. Directly relevant prior work is missing in Transformer and NAR vocabulary (one row was in the ledger but uncited), and it narrows the novelty claim

All quotes below were fetched on 2026-10-01.

- **Discrete Neural Algorithmic Reasoning.**
  - Source: https://arxiv.org/html/2402.11628. It is in the ledger as R4-048 (AUTHOR-CLAIM) and R4-163 (repo), and **not cited in SYNTHESIS**.
  - "we enforce attention to be hard attention. We found this property important not only for interpretability but also for size generalization, as hard attention allows us to overcome the annealing of the attention weights for arbitrarily large graphs"
  - The processor "recurrently updates these features"; train "at most 16 nodes", test "sizes from 16 to 1600 nodes".
  - So hard selection inside a weight-shared loop, motivated by dispersion and tested on 100× size extrapolation, is published.
  - It is hint-supervised, over task-graph neighbours rather than learned top-k over all nodes, and not FLOP-matched. §0.4's "what we did not find" survives only in that narrower form.
- **Neural Data Router.**
  - Source: https://arxiv.org/abs/2110.07732 (PDF, §1 and §2.2).
  - Weight sharing "as is done in Universal Transformers", plus "geometric attention designed to attend to the closest matching element", "100% length generalization accuracy on the classic compositional table lookup task".
  - This is a weight-tied Transformer with sharp, selective attention for length generalisation. It belongs in §1 and §2, and it is a natural extra sharp-attention arm or reproduction target.
- **Universal Transformers for Circuit Computations.**
  - Source: https://arxiv.org/abs/2608.31067.
  - "identify evaluable subexpressions at each iteration via masked hard attention … Combined with an autonomous halting criterion … resulting in exact length generalization."
  - This covers hard attention, iteration and halting with length generalisation. It is a constructed parameterisation, but it overlaps G2 + G3.
- **Stabilizing Extrapolation in Looped Transformers via Learned Stochastic Stopping.**
  - Source: https://arxiv.org/abs/2606.29983.
  - "Introducing stochasticity into the number of loops during training sharply reduces OOD variance".
  - This bears on G3, on the seed count (B2), and on whether random-T training should be identical across arms.
- **Transformer Programs (Friedman et al., 2023).** **Lead, unverified.** DNAR's text says "Similar to Transformer Programs". It is reportedly hard attention learned with Gumbel annealing, i.e. G2's training trick.

**Fix.** Add these to the ledger and to §1, §2 and §0.4. Restate the open item as: "learned, state-conditioned top-k over all nodes vs ASEntmax-sharpened attention inside the same loop, at matched cost, without step supervision". Also run the Transformer-vocabulary searches before the freeze, not after.

### M8. The §0.2 "for" evidence is partly mis-categorised, and counter-evidence is uneven in §0.3 and §2

- **R3-105** is filed under "For edge- or selection-structured computation", but AKOrN's gain comes from oscillator (Kuramoto) dynamics, not edges or selection. The ledger quote also omits that more self-attention steps "hurt ID accuracy" (R3-105 claim text).
- **R4-063** is an AUTHOR-CLAIM about fixed-depth Transformers. Its own ledger note says it "says nothing about T1", yet it sits in a list about looped Transformers at matched compute, and the label is missing.
- **R4-001/002** are step-supervised (hint) processors, so they are relevant but differently trained from the proposed design. Say so.
- **§0.3** says "Controlled studies find ~2 bits per parameter (R2-017, R4-184)". These are one study (same source, same quote) counted twice. R4-165 and R2-046 are likewise one ARC blog post.
- **§2 marks "Time replaces depth on algorithmic tasks" as Established** (R2-157, R4-024, R3-120/121). These are all one paper and one model family on two grid or sequence tasks. The same document's counter-evidence is not shown in that row:
  - maze extrapolation is dead-end filling and fails with cycles (R4-032/033);
  - Ouro degrades past its trained depth (R2-018);
  - LM test-time recurrence saturates (R2-095).

  Downgrade it to "Supported on local and sequence algorithmic tasks, with caveats".

### M9. The parameter registry contradicts the v0.2 preregistration

`ngs/params.py` (CODE) says:
- `"seeds": 3`, `"ood_ladder_factor": 4`;
- `"test_time_iteration_factor": (4, "… T_test = 4 x T_train")`, which is the rule §5 says "is dropped";
- `"flop_match_tolerance": 0.10`, which is not in v0.2.

Project rules make `params.py` the single registry, so any code written now would run the v0.1 design. Update it before the freeze, and add a test that the preregistration constants and `params.py` agree.

### M10. The run plan and cost leave out most of the planned work, and one task has a built-in floor

- **Where:** SYNTHESIS §12: "8 arm configurations … × 6 families × 5 seeds = 240 runs".
- **Not counted:**
  - T0 iso-param and iso-FLOP (2 configurations);
  - the G3 rule control;
  - the SSMax ablation of T1-sharp;
  - the three maze percolation levels (train or test only? unspecified);
  - every §10 ablation. Ablations 2–7 are about 6 one-variable ablations across up to 5 looped arms × 6 families × 5 seeds, which is easily another 300–900 runs;
  - the reproductions #1–#5;
  - the evaluation cost of the large rungs (M3).

  "0.5–2 GPU-h each" is not derived from anything. The arithmetic itself checks: 336 × 0.5–2 h = 168–672 h; × $0.45 = $76–302; × $0.60 = $101–403.
- **Built-in floor in shortest path.** Exact distances are integers up to roughly 9 × path length, so at n = 1024 the output values far exceed anything seen at n_train = 16. This is a value-extrapolation confound that floors every arm and feeds B2.
- **Fix.** Cost ablations explicitly, mark them as optional, and switch shortest path to predecessor or edge-on-path labels, or relative comparisons.

---

## (d) MINOR / wording

1. §0.5: "At the training sizes (N ≤ ~1k)". Training sizes are 16 (graphs) and 361 squares (9×9 maze). 1k is a test size.
2. §2 "Established" rows cite AUTHOR-CLAIM rows as establishment: R4-070 (attention = message passing) and R6-004 ("potentially limits"). The R4-070 statement is a standard identity, but it should be cited as a derivation, not an author claim.
3. §2 "Supported: sparse routing does not pay on GPUs at small N" leans on R5-133. R5-133 is about per-edge MLP messages, which G2 does not use, since G2 uses attention messages. R1-135 is an AUTHOR-CLAIM. Mark the row partial.
4. §7 cites R2-161 for "k annealing + Gumbel noise in G2". R2-161 (Shazeer MoE) supports noise plus balancing losses, not k-annealing.
5. §3 excludes cross-input memory because "attention is already the recall store, R3-002". R3-002 is about within-input retrieval and says nothing about persistent cross-input memory, which is what the brief asked for. The deferral is fine, but the justification is a non-sequitur.
6. Reachability generator: at mean out-degree 1.5, 18–24% of instances have only the source reachable (measured over n = 16–1024, 50 seeds each). "Balanced lookahead (to do)" is load-bearing for V1 on that family. The current generator is not the preregistered one.
7. Additive β·A + PE_ij biases rule out the FlashAttention kernel for T1, because SDPA with a float mask uses another backend, and a bias of size N² must be materialised. §8 implies FlashAttention for T0/T1.
8. V3: "within δ" has no CI rule. V4: "AUC does not decrease as T increases" is ill-typed, because AUC is integrated over n. The intent is accuracy-vs-T at fixed OOD n.
9. §12: "Reproduce #1–#3 (ASSUMPTION: about a day and under $20)" has no basis given. DT-Recall maze training time is not in the ledger.
10. Brief coverage: "topology and node roles allowed to evolve" (node roles) is never addressed. Hyperedges and memory are deferred honestly (§3, §10.8). The approach matrix leaves q10 unknown for 80 of 121 rows; this is disclosed, but it is the brief's central question 10 ("whether additional inference iterations improve capability").
11. The preregistration does not say whether maze percolation > 0 appears in training or only at test. They are different shifts (size vs structure, §11).

---

## (e) Citation audit (44 IDs checked against `claims.csv` quote, status and notes; 4 also against cached sources)

| Claim ID | § | Supports? | Note |
|---|---|---|---|
| R4-080 | 0.1, 3 | Y | AUTHOR-CLAIM, labelled correctly |
| R2-016 | 0.1 | Y | parameter-matched only, stated |
| R2-199 | 0.1 | Y | DERIVED 1.4×, consistent |
| R2-093 | 0.1 | Y | parameter-matched, stated |
| R2-089 | 0.1, 12 | Y | strict matching; quote checked in source |
| R5-092 | 0.1 | Y | |
| R4-185 | 0.1 | Y | LM loss, stated |
| R4-001 | 0.2, 9 | partial | step-supervised and unmatched; not stated in §0.2 |
| R4-002 | 0.2 | partial | GAT-full is also a step-supervised processor; same caveat |
| R4-176 | 0.2 | Y | |
| R3-105 | 0.2 | partial | oscillator dynamics, not edge or selection; "hurt ID accuracy" omitted |
| R4-063 | 0.2 | N | fixed-depth only; AUTHOR-CLAIM unlabelled; ledger note says it says nothing about T1 |
| R4-165 | 0.2, 12 | Y | duplicate of R2-046 |
| R1-088 | 0.2 | Y | |
| R1-091 | 0.2 | Y | node classification; scope fine for "tuned baselines" |
| R2-017 / R4-184 | 0.3, 12 | partial | one study counted as "studies" |
| R6-008 | 0.4 | Y | |
| R6-006 / R6-007 | 0.4 | Y | baselines-and-tasks note verified (0 "looped" or "universal transformer" hits in the cached text) |
| R1-067 | 0.4 | Y | |
| R6-001 | 0.4 | Y | THEOREM |
| R6-002 | 0.4 | Y | |
| R6-004 | 0.4, 2 | partial | AUTHOR-CLAIM listed as "Established" |
| R6-003 | 0.4, 3 | **N** | 1000× is ASEntmax, not the fixed α-entmax the arm uses (B4) |
| R5-086 | 0.5 | Y | large graph, scope stated |
| R5-131 | 0.5 | Y | DERIVED; arithmetic rechecked (0.75^1024 ≈ 10^-128) |
| R5-133 | 0.5, 2 | partial | per-edge MLP; not G2's message type |
| R5-017 / 041 / 042 | 0.5 | Y | long context only, stated |
| R2-097 | 12 | Y | |
| R2-095 | 1, 12 | Y | |
| R4-179 | 5 | Y | DERIVED, correct |
| R4-061 | 5 | Y | THEOREM |
| R4-025 | 5, 9 | Y | |
| R4-024 | 1, 6 | Y | the post-hoc peak caveat in its note applies to our own B3 |
| R6-009 | 4, 7 | Y | corrected from v0.1, consistent |
| R2-064 / R2-065 | 4, 7 | Y | |
| R2-036 | 6 | Y | |
| R5-134 | 6 | Y | |
| R4-140 | 12 | Y | step-count supervision noted in ledger, not in §12 |
| R4-005 / R6-005 | 3 | Y | AUTHOR-CLAIM, labelled |
| R2-161 | 7, 11 | partial | supports noise and balancing, not k-annealing |
| R2-149 | 4, 7 | Y | used honestly (ACT collapses) |
| R2-152 | 4 | Y | |
| R5-071 / R5-072 | 8, 12 | Y | price arithmetic correct |
| R5-081 | 11 | Y | also undermines the flops.py selection term (M4) |
| R5-103 | 11 | Y | AUTHOR-CLAIM, labelled |
| R4-123 | 6, 9 | Y | |
| R2-157 / R3-120 / R3-121 | 2 | partial | one paper; "Established" overstated (M8) |
| R4-033 / R4-032 | 6, 9, 11 | Y | |
| R1-098 / R4-173 | 2 | Y | constructions, stated |

Summary: 34 Y, 12 partial, 2 N (R6-003 as used, R4-063 as used).

---

## (f) What I checked and found sound

- **FLOP model (as far as it goes).**
  - `ngs/flops.py` matches D2 term by term (8Nd² + 4N·d_ff·d + 2P_s·d + 2P_m·d).
  - The quoted G2/T1 ratios reproduce exactly: 0.995, 0.966, 0.879 and 0.717 at N = 16, 64, 256 and 1024.
  - The v0.1 double-QKᵀ error is fixed, and the tests pin k = N ≡ dense.
- **Price arithmetic.** 336 run-equivalents, 168–672 h, $76–302 and $101–403 are all correct. The tuning count (8 × 8 × 6 × 0.25 = 96) is correct.
- **Task generators.**
  - Maze labels (union of shortest paths via two BFS) are correct, and percolation creates cycles.
  - S5 uses composition order p[q] consistently.
  - MQAR keys are distinct.
  - Shortest-path graphs are guaranteed reachable.
- **Unmatched comparisons.** The verdict's LM-substrate "no" is well supported, and the draft is honest that literature comparisons are unmatched. Ouro's and Parcae's parameter-only matching is flagged correctly.
- **AUTHOR-CLAIM labelling.** This is mostly correct in §0 and §3, with the R4-063 and §2 exceptions above.
- **Reframing.** "Not a new substrate; the matched test is the contribution" is the right scope, and §0.4 discloses that the novelty searches were thin and in GNN vocabulary.
- **Arms vs brief.** All brief-requested comparators are present (Transformer, GNN, recurrent fixed GNN, learned topology, plus halting). The hypergraph arm is dropped with a reason.
- **Brief outputs.** All 12 requested outputs are present as sections (1 SOTA → §1; 2 → §2; 3 → §3; 4 → §4; 5 → §6; 6 → §7; 7 → §8; 8 → §9; 9 → §10; 10 → §11; 11 and 12 → §12).

---

## (g) New vs already raised in R1-opus.md

Read after (a)–(f) were written. R1 reviewed v0.1, so several of its fixes are the v0.2 text this review attacks.

| R2 finding | Status vs R1 |
|---|---|
| **B1** fixed F grid floors all arms; per-step efficiency credited as inductive bias | **New.** R1 B3/B4 led to c·n and executed FLOPs. Neither R1 nor v0.2 checked what a fixed grid set at n_train buys at large n. |
| **B2** trivial equivalence from floors and ceilings; undefined δ; TOST power at 5 seeds; non-exclusive verdicts; no "inferior" outcome | **Partly new.** R1 M9 asked for TOST, ≥ 5 seeds and AUC (now in v0.2). Every point listed here is new. |
| **B3** oracle best-over-T on test labels; V3 asymmetry | **New.** R1 (f) noted DT-Recall's post-hoc peak in a literature number, not in our own metric. |
| **B4** T1-sharp is fixed 1.5-entmax, which ASEntmax beats; §0.4 misattributes the 1000× | **New.** R1 B2 asked for a sharpness arm and quoted the 1000× without separating ASEntmax from fixed α-entmax. |
| **M1** Gumbel and k-annealing only in G2 | **New as a confound.** R1 M3 proposed them as G2's fix and did not flag the asymmetry. |
| **M2** pilot constants tuned on baselines; c does not transfer (measured eccentricity and path lengths); n undefined per family | **New.** R1 B3 proposed T(n) = c·n. |
| **M3** maze is 14,161 grid squares in the generator, not 3,481 nodes; memory and time estimate | **New.** R1 M7 also used 3,481, so both reviews and the draft missed this. |
| **M4** no entmax cost; selection term understated vs R5-081; per-step readout and halting excluded | **New.** R1 B4 fixed the double-QKᵀ only. |
| **M5** no verdict rule for the brief's per-parameter question vs T0; T0/G0 evaluation undefined | **Partly new.** R1 M6 asked for iso-param vs iso-FLOP T0 (adopted). The missing V-rule and the evaluation under the T sweep and F grid are new. |
| **M6** selection of best k and max; multiplicity; gate 5 as unregistered interim analysis | **New.** |
| **M7** literature: DNAR (ledger R4-048, uncited), NDR, 2608.31067, 2606.29983 | **New hits.** R1 M1 asked for Transformer-vocabulary searches and found ReSSFormer; its own searches did not find these. |
| **M8** R3-105 and R4-063 mis-categorised; R2-017/R4-184 and R4-165/R2-046 are duplicates; "Established" time-replaces-depth | **New, and partly contrary to R1.** R1 B1 recommended adding R3-105 and R4-063 to the "for" list; R2 finds them off-target. |
| **M9** `params.py` stale vs prereg v0.2 | **New.** |
| **M10** run plan omits ablations and evaluation; shortest-path value-extrapolation floor | **Partly raised.** The run-plan undercount was R1 M10 for v0.1; it recurs in v0.2 for the ablations. The shortest-path floor is new. |
| **Minor 1** "training sizes N ≤ ~1k" | **Partly raised.** R1 M7 raised the N regime; this is the residual wording. |
| **Minor 9** "<$20" basis | **Already raised** (R1 minor 11); the label was added, but the basis is still missing. |
| **Minors 2–8, 10, 11** | **New.** |
