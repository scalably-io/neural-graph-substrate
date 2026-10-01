# Review R3 (Opus, fresh context): SYNTHESIS v0.3 + PREREGISTRATION draft v0.3, 2026-10-01

Scope: preregistration soundness, the single-variable claim, the D3 budget, code, citation fidelity, coverage of the brief. Sections (a)–(f) were written before I read R1-opus.md, R2-opus.md or NEGATIVE-FINDINGS.md; (g) was added afterwards.

## (a) Verdict

**FIX-THEN-SHIP.** The program is well built and mostly honest. Three things must change before the owner sees it:
- the validity gate can produce or erase a V1 verdict by construction;
- the shortest-path family has no input channel for edge weights and no scoring rule;
- one sentence in §0.4 states something false about the closest prior work.

## (b) BLOCKERS

### B1. The validity gate is chosen on the outcome and can decide V1 / V1-null by construction
- **Where.** PREREGISTRATION §Statistics: "A family is **informative** only if the best looped arm's nAUC is in [0.10, 0.90]." This works together with V1 / V1-null, which need "≥ 4 informative families", and with the "equivalent" outcome class.
- **What is wrong.** The gate looks at the best of *all* looped arms. That set includes G2 itself and G1, which is given the true task graph. Three failures follow.
  1. **A large G2 win is erased.** Take G2 = 0.95 and T1 = T1-sharp = 0.20. The best looped arm is 0.95, so the family is marked "ceiling" and does not count. The bigger the routing effect, the more likely V1 loses the family.
  2. **G1 can push graph families out of the count whatever G2 and T1 do.** G1 is a recurrent GNN with the task graph as a hard mask. That is exactly the setting where the ledger reports large extrapolation:
     - R1-027: "can extrapolate well to graphs that are 1,000 times larger";
     - R4-025: DT-Recall reaches 97.30% on 59×59 mazes after training on 9×9;
     - R4-001: MPNN-max reaches 99.80% on 100-node reachability.

     If G1 is above 0.9 on reachability, maze and shortest path, at most 3 families stay informative. Then neither V1 nor V1-null can reach "≥ 4", and the study is inconclusive by design.
  3. **A joint floor is scored as "equivalent", which counts toward V1-null.** Take G2 = T1 = 0.00 and G1 = 0.50. The family is informative, Δ = 0 with zero spread, so the 90% CI [0, 0] lies inside (−δ, δ). The family is "equivalent" and supports "the gain is recurrence and sharpness, not routing", even though neither arm gained anything.

  The same gate also governs V0 (T1 vs T0), V2 and V3.
- **Evidence.** Rule text as quoted. Claim rows R1-027, R4-025 and R4-001 with the quotes above. The three cases follow directly from the outcome table.
- **Fix.** Gate each comparison on the two arms being compared, never on a third arm and never on the best arm.
  - Before testing, require both arms to reach ≥ 0.95 in-distribution validation accuracy; otherwise mark the pair "not trained".
  - Mark the pair "floor" if both arms are below 0.10, and "ceiling" only if both are above 0.90.
  - A floor pair never counts as "equivalent".
  - Report G1 as a reference arm outside the gate.
  - Preregister what happens when fewer than 4 families qualify (report per family, with no overall verdict), and say so in §0.6.

### B2. Shortest path can be neither computed nor scored as specified
- **Where.**
  - PREREGISTRATION task table: "valid predecessor of every node".
  - SYNTHESIS §4 formulation: scores S_ij = … + β·A_ij; messages m_i = Σ_j α_ij W_V LN(h̃_j); Enc(X) is per node.
  - `ngs/tasks/shortest_path.py`: `answer` is an n×n boolean matrix.
- **What is wrong.**
  1. **Weights have no way in.** Edge weights have no input channel. A_ij enters only as a scalar bias times one learned β, and a message from j does not depend on the pair (i, j). Bellman–Ford needs dist_j + w_ji at the receiver, so the task is not expressible in the specified architecture unless weights are packed into node states in some unspecified way. R4-176, which the synthesis itself cites, is the evidence that edge vectors matter: a plain Transformer averages 42.34% OOD against 81.30% for the Relational Transformer.
  2. **"Exact match" is undefined, and ties are common.** The answer is a set of valid parents per node. Over 30 instances per size:
     - every instance at n ≥ 256 has nodes with ≥ 2 valid parents (30% of instances at n = 16, 87% at n = 64);
     - about 2.7% of non-source nodes have ≥ 2 valid parents.

     Scoring the whole set (N² binary outputs per graph) and scoring one pointer per node by set membership give different tasks and different floors. No scoring code exists in `ngs/` or `scripts/`.
  3. **The readout is unspecified.** A per-node readout R(LN(h_i)) cannot name another node unless it outputs that node's random ID or reads a pointer off the attention scores. Reading a pointer off the scores would favour arms whose scores are already sharp (G2).
  4. **k = 8 barely covers the needed neighbours.** Maximum in-degree is 8 at n = 256 and n = 1024, so G2 can attend to every in-neighbour only if a node never selects itself.
- **Evidence.** `.venv/bin/python -B -c …` over `shortest_path.make`: fraction of nodes with ≥ 2 valid parents 0.027 / 0.032 / 0.027 / 0.027 and P(instance has any) 0.30 / 0.87 / 1.00 / 1.00 at n = 16 / 64 / 256 / 1024; maximum in-degree 6 / 7 / 8 / 8.
- **Fix.**
  - Add one edge channel, identical across arms: a learned edge embedding e_ij = f(A_ij, w_ij), used both as a score bias and inside values (relational attention).
  - Define the output as one pointer per node, scored correct iff it lies in the valid set. Graph-level exact match then means every node is correct.
  - Use the same readout head for every arm: classify the predecessor's identifier, never argmax over attention scores.
  - Pin all of this in code with a test before the freeze. The alternative is to drop the family and say so.

### B3. A false sentence about the closest prior work (ReSSFormer) in §0.4
- **Where.** SYNTHESIS §0.4: "A 2025 model combines a recurrent reasoning unit with per-query top-k attention (R6-006, R6-007). Its baselines include no looped Transformer, and it tests no size extrapolation."
- **What is wrong.** ReSSFormer does test length extrapolation. Its baselines are all non-looped (that half of the sentence is correct).
- **Evidence.** Cached source `evidence/sources/R6/2510.01585.txt` (arXiv 2510.01585, §4.2), verbatim: "Models are trained on 4k tokens and tested with longer inputs. We compare ReSSFormer against GPT-2, Longformer, BigBird, and RoPE-Transformer … ReSSFormer sustains performance up to 8k tokens, while others degrade beyond 2k."
- **Fix.**
  - Rewrite the sentence: it tests 2× length extrapolation on long-context reasoning against non-looped, non-sharpened baselines (AUTHOR-CLAIM), not size extrapolation on algorithmic tasks.
  - Add a ledger row with this quote.
  - The "not found in our search" gap survives, but it narrows to: against a looped and an ASEntmax-sharpened baseline, on algorithmic size extrapolation, with matched steps. §2 "Open" should say exactly that.

## (c) MAJOR

### M1. The budget makes the primary metric also a test of long-horizon stability
- **Where.** PREREGISTRATION §Iteration budget, "Readout. Taken at the last executed step"; D3 "Why": "makes global arms prove they stay stable (V4)".
- **What is wrong.** For global arms, T(n) is far larger than they need and far beyond the trained loop counts.

  | Family | T(n_train) | T(n_max) | Ratio |
  |---|---|---|---|
  | Reachability | 11 | 56 | ×5 |
  | Maze | 79 | 737 | ×9 |
  | Recall | 72 | 1,152 | ×16 |
  | S5 | 24 | 768 | ×32 |

  Training samples T ~ U[T/2, T] only at n_train. A dense softmax loop iterated 737 times faces oversmoothing; the ledger has this as a theorem, covering state-dependent attention as well (R1-008: "graph attention mechanism cannot prevent oversmoothing"; R1-009: "accounts for asymmetric, state-dependent and time-varying aggregation operators"). Sparse top-k mixes less.

  So a G2 win at T(n) can come from drift and smoothing resistance rather than from routing reach. That is a real property, but it is not the stated question, "extrapolate in instance size". The question's own framing ("T1 solves the task in 10 steps and then drifts") is therefore scored as a size failure.

  V4 measures the same thing again, so V1 and V4 are not independent.
- **Fix.** Keep the primary metric, but preregister an interpretation rule. Report nAUC at T(n) alongside nAUC at the best step (upper bound) and at T(n_train). If G2 beats X at T(n) but not at the best step, the claim is "G2 is more stable over long horizons", not "G2 extrapolates further". Add a train-time stress test: sample some training runs out to 2·T(n_train), identically for every arm.

### M2. V3 (halting) is close to automatic, and its equivalence form penalises a halting gain
- **Where.** "V3: G3 equivalent to G2 … at ≤ 0.7 × G2's executed steps."
- **What is wrong.**
  - G2 always runs T(n) = 1.5·q99(D), so 0.7·T(n) = 1.05·q99(D). Any halting policy that stops once a *local* algorithm would be done passes the step test. For a global arm that needs about log n steps, the test is trivial.
  - If G2 drifts (M1) and G3 halts early, G3 is *better* than G2, and "equivalent" fails exactly when halting helps.
- **Fix.**
  - Make V3 non-inferiority: the 90% CI lower bound of nAUC(G3) − nAUC(G2) > −δ.
  - Compare G3's steps with G2's *earliest step reaching its final accuracy* (a diagnostic), and with the rule-based control. Do not compare against T(n).

### M3. The statistical machinery is asymmetric and partly undefined
- **Where.** §Statistics and outcomes, §Seeds, V1 / V1-null.
- **What is wrong.**
  1. **Superiority power is capped at 50% at a true effect of δ.** "Superior" requires the point estimate Δ̂ ≥ δ, so at true Δ = δ its power is 0.50 at any n. With the intersection–union test (both T1 and T1-sharp) it is about 0.25 per family, and V1 needs this on 4 or more families. Simulated with paired t, 100k reps (sup = power of "superior"):

     | σ | n seeds | TOST power at Δ = 0 | sup at δ | sup at 1.5δ | sup at 2δ |
     |---|---|---|---|---|---|
     | 0.04 | 7 | 0.79 | 0.49 | 0.94 | 1.00 |
     | 0.07 | 15 | 0.68 | 0.50 | 0.92 | 1.00 |
     | 0.10 | 15 | 0.20 | 0.40 | 0.75 | 0.95 |

     The power rule sizes for equivalence only. Say plainly that "superior" means a true effect of about ≥ 1.5δ.
  2. **V1 is corrected for multiplicity and V1-null is not.**
     - V1 gets Holm across families. V1-null ("equivalent *or* inferior to *at least one*" on ≥ 4 families) gets no correction, and its "at least one" is a union, which makes it easier.
     - Holm needs p-values, but the outcome classes are defined by CIs plus a point-estimate threshold. Which p-value enters Holm is undefined (the IUT p = max of two one-sided p's, against Δ ≤ 0 or against Δ ≤ δ?).
     - The number of tests m is set by the outcome-dependent gate (B1).
     - V2 ("≥ 3 informative families") has no correction stated.
  3. **The seed formula is mislabelled and unpinned.** "n_seeds = ⌈10.8 σ²/δ²⌉, i.e. power ≈ 0.8".
     - Normal approximation for a paired TOST at true Δ = 0: n = (z₀.₉₅ + z_{1−β/2})²·σ²/δ². Power 0.8 gives (1.645 + 1.282)² = **8.56**. 10.8 = (1.645 + 1.645)² is the **power 0.9** value.
     - Because small-n t-quantiles inflate the requirement, 10.8 happens to give an actual power of about 0.79–0.86 at n = 5–15 (table above). Exact n for 0.8 is 5 / 8 / 11 at σ = 0.03 / 0.04 / 0.05, against 4 / 7 / 11 from the rule.
     - The number is roughly right for the wrong reason. It is not a DERIVATIONS entry and has no pinning test, which breaks project rule 6.
  4. **The cap makes "underpowered" likely, and its consequence is unspecified.** At δ = 0.05 the cap of 15 is enough only for σ ≤ 0.059. R6-014 (AUTHOR-CLAIM) reports high OOD variance for looped Transformers. Whether an underpowered family still counts toward V1, V1-null and Holm is unspecified.
  5. **The pilot cannot reliably set σ.** Its size is unspecified, and its σ (G2 − T1, on reachability and maze only) is applied to all six families and to the G2 − T1-sharp comparison.
- **Fix.**
  - Replace "Δ ≥ δ" with a one-sided test of H0: Δ ≤ 0 at α, or state the effect size it is powered for.
  - Specify one p-value per family (IUT max) and apply Holm (or none) to V1 and V1-null alike.
  - Fix m before seeing the data (all 6 families; a non-informative family counts as not rejected).
  - Put the seed formula in DERIVATIONS with its exact t-based derivation and a test.
  - Fix the pilot size (for example 4 seeds) and use one n for every family.

### M4. T(n) is not reproducible from the preregistration, and the documented values disagree with the code
- **Where.**
  - PREREGISTRATION: "99th percentile over 200 seeded instances" (no seed given).
  - DERIVATIONS D3 "Values (`ngs.budget`, 100 instances)".
  - SYNTHESIS §5 table.
- **Evidence.** Re-run of `ngs.budget.budget` with the code defaults (samples = 200, seed = 0), against the documented values:

  | Family | n | Code | Documented |
  |---|---|---|---|
  | Reachability | 16 | 11 | 12 |
  | Reachability | 64 | 26 | 23 |
  | Reachability | 256 | 47 | 47 |
  | Reachability | 1024 | 56 | 52 |
  | Shortest path | 16 | 11 | 10 |
  | Maze | 9 | 79 | 73 |
  | Maze | 17 | 227 | 224 |
  | Maze | 33 | 737 | 737 |

  Across seeds 0–4 the values spread: reachability n = 1024: 56 / 56 / 61 / 61 / 67; maze side 33: 737 / 736 / 775 / 823 / 747; maze side 9: 79 / 77 / 80 / 86 / 85. The `0.99` quantile is hard-coded in `budget()` rather than read from `params.py`, and `test_budget_defaults_match_params` does not pin it, the sample count or the seed.
- **Fix.** Freeze the T(n) table per rung in the preregistration (generated by a script), pin it with a test, and pin `samples` and `seed`. SYNTHESIS §5 and D3 should quote the generated table, including recall (72 → 1,152, that is 4.5·n, not 1.5·n) and shortest path at 1024 (23).

### M5. "Routing is the single trained difference" is not true for T1-sharp, and G2 changes regime between training and test
- **Where.**
  - SYNTHESIS §0.6: "routing is the single trained difference between arms".
  - SYNTHESIS §12: "the design makes routing the single trained difference".
  - PREREGISTRATION T1-sharp = ASEntmax.
- **What is wrong.**
  1. **ASEntmax sees n and adds input-dependent parameters.** It rescales logits by (δ + β(log n)^γ), with β = softplus(X w_β) and γ = s·tanh(X w_γ), where w_β and w_γ ∈ ℝ^d are learned per head. T1-sharp therefore gets an **explicit instance-size signal (log n)** that T1 and G2 do not have, plus input-dependent parameters (2·d per head; negligible against ±5%, but not zero).

     Source: https://arxiv.org/html/2506.16640, §4.1, fetched this session through a summarising fetcher, so the wording should be re-checked against the PDF: "ASEntmax(z)=α-entmax((δ+β(log n)^γ)z), where β,γ,δ∈ℝ are head-specific scalars". The cached abstract (`evidence/sources/R6/2506.16640.abstract.txt`) confirms "a learnable temperature parameter".

     If T1-sharp beats G2, part of the edge may be the log n input. That is legitimate for the "sharpening" baseline, but it is a second difference and must be stated.
  2. **G2 is trained near-dense and tested very sparse.** With k = 8 fixed, the attended fraction is:
     - reachability, sorting, S5: 8/16 = 50% in training, 8/1024 = 0.8% (or 8/512) at test;
     - maze: 8/81 ≈ 10% in training;
     - recall: 8/48 ≈ 17% in training.

     G2 can learn strategies that need broad coverage at training size, then lose them at test. The shift in the routing operator itself is specific to G2. N ≤ 8 never occurs on the ladder, so G2 = T1 never happens exactly, but at N = 16 the two are near-identical, so the routing difference is barely trained on three families.
  3. **In-degree reaches or exceeds k at large n.** Reachability: maximum in-degree 9 at n = 256 and 10 at n = 1024 (50 instances each). For an OR over in-neighbours, G2 can miss a reachable parent.
- **Fix.**
  - Reword to: "between T1 and G2 only the routing rule differs; T1-sharp also receives log n through ASEntmax's temperature".
  - Optionally add the same log n temperature to T1 and G2 scores as an ablation.
  - Raise n_train for the three 16-node families so that N_train ≥ 4k, or state the regime shift as a known confound and keep k = 4 as the ablation that probes it.

### M6. V0, the brief's critical question, has no decision rule, and the iso-param T0 is under-specified
- **Where.**
  - "V0 … T1 vs T0 (iso-param), using the outcome classes above, family by family."
  - The T0 row: "L distinct blocks".
- **What is wrong.**
  1. **No overall rule.** No count of families and no aggregation is given, so V0 cannot return an overall answer.
  2. **L is unspecified for iso-param T0, and so are d, heads and d_ff** (d = 128 appears only in D2). If tuning picks width, ±5% matching is undefined.
  3. **Lookup tables dominate the parameter count.** Random IDs from [0, 4096) "embedded" imply a 4096 × d table: 524k parameters at d = 128, against about 197k for one block (12d²). A value vocabulary adds more. "Per stored parameter" is then mostly embedding parameters, and matching total parameters by shrinking T0's width changes its block capacity quadratically.
  4. **V0 mixes two things.** At test, T1 runs T(n) steps that grow with n while T0 is fixed at L. V0 therefore measures parameter efficiency together with growing test-time compute (as §0.1 already says of the literature).
- **Fix.**
  - Specify L (or a small preregistered set), d, heads and d_ff.
  - Match non-embedding parameters ±5% and report total parameters beside them.
  - Give V0 an aggregation rule like V1's.
  - Print each arm's inference-FLOP ratio at every rung next to V0.

### M7. (Downgraded to minor after reading R2: see (g).) The §12 cost hides an assumption and leaves out inputs
- **Where.** §12: "Tuning: ≈ 100 run-equivalents".
- **What is wrong.** 8 configurations × 6 families × 8 trials = 384 *trials*. That is ≈ 100 run-equivalents only if each trial costs 0.25 of a run. R2 (f) states this factor ("8 × 8 × 6 × 0.25 = 96"), but v0.3 does not. If tuning trials are full runs, the cost becomes:
  - (240 + 384) × 0.5 = 312 GPU-h;
  - (720 + 384) × 2 = 2,208 GPU-h;
  - ≈ $140–994.

  Also still missing: test-set size per rung, training length (steps or examples), pilot and reproduction runs. The headline arithmetic is correct: 8 × 6 × 5–15 = 240–720 runs; $75–740 given the inputs.
- **Fix.** Write the 0.25 factor into §12 as an ASSUMPTION, and preregister the test-set size per rung and the training budget.

### M8. Two citations go the wrong way in §0 and §12
1. **R5-092 is cited as a per-FLOP win.**
   - Where: SYNTHESIS §12 "Looping wins modestly per FLOP (R2-089, R5-092)".
   - R5-092 says the opposite: "at r=4 a 410M looped model performs on par with a 580M non-looped model, but incurs the training cost of a 1B non-looped one". That is a loss per training FLOP. §0.1 handles it correctly ("recurrence pays much less").
   - Fix: "modest win at best (R2-089); a loss in another setting (R5-092)".
2. **R4-176 is filed as evidence for hard selection.**
   - Where: §0.2, under "For hard, discrete selection".
   - The Relational Transformer adds **edge vectors** to soft attention. Its gain (42.34 → 81.30% OOD) is evidence for edge features (and supports B2), not for hard routing.
   - Fix: move it to its own line.

## (d) MINOR / wording
- **R4-185 is misparaphrased.** §0.1 says "One recurrence is worth r^0.46 unique blocks". The fitted law is (N_once + r^φ N_rec): r recurrences of a block are worth r^0.46 copies of it. The ledger claim text carries the same misreading.
- **AUTHOR-CLAIMs appear unlabelled.**
  - §1 table "OOD variance high and reduced by stochastic loop counts" (R6-014 and R6-015 are both AUTHOR-CLAIM).
  - §7 and the PREREGISTRATION shared recipe cite R6-015 as fact.
  - §2 "Established … attention is message passing (an identity)" rests on R4-070 and R1-099, both AUTHOR-CLAIM. Fine as an identity, but say "identity" and cite the derivation, not the claims.
- **NDR is missing its task.** §0.4 "100% length generalisation" should say "on compositional table lookup" (R6-012).
- **R1-098 and R4-173 are the same paper.** Add them to the duplicate-ID convention.
- **R1-166 is not evidence of absence.** It shows that more rounds degrade HGNNs. "Hyperedges: no positive evidence (R1-166)" should be "a negative datum (R1-166); no positive evidence found".
- **R5-131 is off by an order of magnitude.** It says "~1e-128"; recomputed: (C(384,8)/C(512,8))^128 = 1.09e-129. Harmless.
- **q10 count is stale.** The q10 "unknown / n/a" count is now 81, not 80 (matrix.csv, 121 rows).
- **IDs need drawing without replacement.** Random node and position IDs must be drawn *without replacement*. With replacement, n = 1024 from 4096 gives about 128 colliding pairs per instance.
- **β·A is undefined for sequence tasks.** Is A the ±2 window, and is it given to T1 and G2 too?
- **Maze ladder.** "9 → 33, ×√2" is non-integer; list the rungs. Note that T(n) is computed at percolation 0 and reused for 0.3, which is generous because cycles shorten d(s, g).
- **V4 is under-specified.** "Largest informative rung" is undefined (the gate is per family, not per rung), and V4 has no statistical procedure: seeds, CI, the definition of "bounded".
- **G0 drives no verdict.** It costs runs but decides nothing; either give it one (the brief's "standard GNN" comparison) or label it descriptive.
- **Position terms are missing from D2.** ⟨id_i, id_j⟩ costs 2N²·d_id. It is state-independent and can be cached once per instance; say so.
- **"Persistent nodes" is reinterpreted without saying so.** The design ties N to the instance (nodes = input elements). There is no persistent pool of latent nodes independent of the input, as the brief's "N persistent nodes" could be read. Say so beside the other dropped components.
- **The reachability band changes the label prior's spread with n.** Reachable-fraction SD is 0.16 / 0.14 / 0.09 / 0.04 at n = 16 / 64 / 256 / 1024, while the mean stays 0.55–0.60 and acceptance rates are 0.40–0.59. Not a bias in the mean, but larger instances are more homogeneous. Report the per-rung label base rate.
- **The ACT ponder-cost weight and the G3 rule-based control's thresholds are unspecified.**

## (e) Citation audit table

| Claim ID | Section | Supports? | Note |
|---|---|---|---|
| R4-080 | §0.1 | Y | Quote matches; AUTHOR-CLAIM labelled |
| R2-016 | §0.1 | Y | 2–3× parameter efficiency; "params only" is correct |
| R2-199 | §0.1 | Y | DERIVED; 5.6B / 4B ≈ 1.4× checks |
| R2-093 | §0.1 | Y | "parameter-matched" in the quote |
| R2-089 | §0.1, §12 | Y | 6.8–18.0%, strict matching |
| R5-092 | §0.1 / §12 | Y in §0.1, **N in §12** | A per-FLOP loss, not a win (M8) |
| R4-185 | §0.1 | partial | φ misparaphrased (d) |
| R4-001/002 | §0.2 | partial | Supports the numbers; max aggregation is per-feature selection; step-supervised (disclosed) |
| R4-176 | §0.2 | **N** (as hard selection) | Edge vectors, not hard routing (M8) |
| R6-010 | §0.2, §0.4 | Y | AUTHOR-CLAIM labelled in §0.2 |
| R6-011 | §0.2 | Y | 16 → 1600 nodes |
| R4-165 | §0.2 | Y | ~5 pp; analogy caveat present |
| R1-088 / R1-091 | §0.2, §1 | Y | Tuned baselines erase gaps |
| R2-017 | §0.3, §2, §12 | Y | One study; the synthesis says so |
| R6-008 | §0.4 | Y | Top-k selection, 2019 |
| R6-006/007 | §0.4 | **partial / N** | Top-k + recurrence is right; "tests no size extrapolation" is false (B3) |
| R1-067 | §0.4 | Y | |
| R6-012 | §0.4 | partial | Task qualifier missing |
| R6-013 | §0.4 | Y | Abstract: masked hard attention + "autonomous halting criterion" |
| R6-001 | §0.4, §2 | Y | THEOREM |
| R6-016 | §0.4, §3 | Y | "up to 1000×" on synthetic tasks; mechanism includes log n (M5) |
| R5-086 | §0.5 | Y | Aggregation memory-bound |
| R5-131 | §0.5, §2 | Y | Recomputed 1.09e-129 |
| R5-017/041/042 | §0.5 | Y | Long-context speedups |
| R1-027 / R1-029 | §1, §2 | Y | |
| R6-009 | §3, §4, §7 | Y | |
| R6-014 / R6-015 | §1, §7, prereg | Y, unlabelled | AUTHOR-CLAIM stated as fact |
| R2-036 | §6 | Y | 87.4 → 56.5 |
| R4-024 / R4-025 | §1, §12 | Y | Peak post hoc, disclosed |
| R2-193, R1-141, R4-148, R4-143 | §12 | Y | Licences match the quotes |
| R5-071/072 | §8 | Y | |
| R2-095 | §12 | Y | |
| R1-166 | §3 | partial | Negative datum, not absence of evidence |
| R5-133 | §3 | partial | Threshold N = k·d needs P_M = 2d²; state the assumption |
| R2-161 | §7, §11 | Y | |
| R1-098 / R4-173 | §2 | Y | Same source, double-listed |

All 111 IDs cited across the two drafts exist in `claims.csv` (0 missing). 13 of them are AUTHOR-CLAIM; three are used as fact (above).

## (f) What I checked and found sound
- **Tests.** `pytest -q`: **227 passed** in 1.07 s.
- **D2.** Re-run of `ngs.flops`. G2/T1 matmul at d = 128, k = 8 is 0.995 / 0.966 / 0.879 / 0.717 at N = 16 / 64 / 256 / 1024, matching the drafts; 0.709 at the 1,089-cell maze. G2 never exceeds T1, including non-matmul at 16× weight. The entmax total is 1.11× T1 at N = 1024 (2.64× with non-matmul weighted 16×), so "ASEntmax's extra non-matmul cost is reported" matters.
- **D3 solvers.**
  - BFS depth and fewest-hop Bellman–Ford rounds are correct.
  - The maze cell graph and labels are correct: a cell is on a grid shortest path iff it is on a cell shortest path.
  - D = d(s, g) is enough for a local algorithm on mazes. On a tree, off-path cells default to 0, and on-path cells see both waves within d(s, g) steps. With cycles, the midpoint broadcast also finishes in about d(s, g). The reachability default-0 argument holds as well.
  - "Sequence length" is the right local bound for odd–even transposition sort and for a left-to-right S5 scan with a ±2 window.
- **Outcome classes.** Mutually exclusive and exhaustive: "equivalent" implies |Δ̂| < δ. V1 and V1-null are exclusive per family, and overall, because 4 + 4 > 6. No within-family adjustment is needed for the intersection–union test.
- **Seed-rule numbers.** Its output is close to power 0.8 after the t-correction (M3.3 is about the label and the pinning, not the numbers).
- **Reachability rejection sampling.** It works (acceptance 0.40–0.59), mean out-degree is preserved (1.47–1.53), and the base rate is stable.
- **Brief coverage.**
  - All 12 requested outputs are present (§1–§12).
  - The critical question is answered in §0.1 (yes against fixed depth, via recurrence) and §0.2 (unknown against looped).
  - Hyperedges, cross-input memory and evolving node roles are disclosed as dropped in §3.
  - Every comparison arm the brief asks for is present (hypergraph justified out).
- **§12 headline arithmetic** (240–720 runs; $75–740 given its inputs) is internally consistent; M7 is about the missing tuning runs.

## (g) New vs already raised (after reading R1-opus.md, R2-opus.md, NEGATIVE-FINDINGS.md)
Read after (a)–(f) were written.

| Finding | Status |
|---|---|
| **B1** gate on the best looped arm (G2 and G1 included); joint floor counted as "equivalent" | **Partly raised, new in substance.** R2 B2 asked for a validity gate against floors and ceilings. v0.3's gate is the fix, and it is selected on the outcome: it erases large G2 wins, lets G1 force families out, and still turns a joint floor into "equivalent". No earlier review examined the adopted gate. |
| **B2** shortest path: no edge-weight channel; set-vs-pointer scoring undefined; ties at every n ≥ 256 | **New.** R2 M10 raised the distance value-extrapolation floor; v0.3 moved to predecessor labels, which created these problems. |
| **B3** "ReSSFormer tests no size extrapolation" is false (4k → 8k) | **New.** R1 M1 found ReSSFormer; the false scope sentence arrived in v0.2/v0.3. |
| **M1** long T(n) makes the primary metric also a stability and oversmoothing test (×5–×32 the trained steps) | **New.** D3 states the stability intent; no review raised the confound with the primary metric. |
| **M2** V3 is automatic (0.7·T(n) = 1.05·q99 D); equivalence penalises a halting gain | **New.** R2 B3 raised a different V3 asymmetry (an oracle T). |
| **M3** superiority power capped at 0.5 at Δ = δ; V1-null uncorrected; Holm p undefined; 10.8 is the z-coefficient for power 0.9; underpowered handling undefined | **Partly raised.** R2 B2 raised power and R2 M6 raised multiplicity in general; these specifics are new. |
| **M4** documented T(n) ≠ code; seed and sample count unpinned | **New.** |
| **M5** ASEntmax receives log n plus input-dependent parameters; G2 trained at k/N = 50%; in-degree > k | **New.** R2 M1 dealt with Gumbel and annealing only. R1 M3 raised G2's exploration problem, which is related but different. |
| **M6** V0 lacks an aggregate rule; L, d, width unspecified; ID tables dominate parameters | **Partly raised.** R2 M5 asked for V0 and a T0 spec. V0 was added, but its aggregate rule and L are still missing; the embedding dominance is new. |
| **M7** tuning cost | **Mostly already raised, my error corrected.** R2 (f) computed 8 × 8 × 6 × 0.25 = 96 run-equivalents. My first draft took the trials as full runs; it is now a minor wording point (state the 0.25). |
| **M8** R5-092 in §12 as a per-FLOP win; R4-176 filed as hard selection | **New.** R1 B1 moved R5-092 into §0.1 correctly; the §12 sentence repeats the old direction. R1 itself proposed listing R4-176 on the "for" side; I disagree, because it is edge vectors, not hard selection. |
| Minor: R5-133 threshold assumption | Already raised (R1 minor 6 / M-R5-133). |
| Minor: node roles | Already raised (R2 minor 10); v0.3 now discloses it. |
| Minor: R4-185 paraphrase, AUTHOR-CLAIM labelling of R6-014/015, NDR task, R1-098 = R4-173, IDs without replacement, β·A for sequences, V4 rung, G0 without a verdict, position-term cost, "persistent nodes" tied to input | New. |
