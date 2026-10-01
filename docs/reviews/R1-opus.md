# R1 adversarial review: SYNTHESIS.md v0.1 (Opus, fresh context, 2026-10-01)

## (a) Verdict

**MAJOR-REWORK (scoped to §0.2, §3–§4 and §12).** Citation fidelity is mostly good and the SOTA map survives. But the verdict's central "leans against" rests on evidence that does not test the graph. The headline design is not one variable: the iteration budget, softmax sharpness and FLOP accounting all differ between arms. The mechanism the study is built around (H*) is already a published theorem with a cheaper fix the design does not control for. As written, a G2 win would not mean "the graph", and a null could not be established with the stated statistics.

---

## (b) BLOCKERS

### B1. §0.2: the "leans against" evidence is about looped vs untied Transformers, not graph vs looped Transformer. Opposing evidence is left out of the verdict.
- **Sentence:** "Against a weight-shared looped Transformer at matched compute: unknown, and the evidence leans against." The supporting bullets are R2-089, R2-097, R4-185 and R5-092.
- **What is wrong:**
  - **The evidence does not test the claim.** All four bullets compare *looped* against *non-looped / untied* Transformers on LM pretraining loss. None contains a graph, top-k routing or an algorithmic task.
    - They bear on "does recurrence pay at matched FLOPs" (§0.1's question).
    - They do not bear on "graph vs looped Transformer" (§0.2's question).
    - R4-185's own note: "Language-modelling validation loss … (storage-dominated objective)".
  - **R2-089 is a win for looping, presented as evidence against it.** SMELT *saves* 6.8–18% of training FLOPs under strict matching. Quote: "SMELT's loss drops faster with compute, saving 6.8–18.0% of training FLOPs". "Wins little" is a fair gloss. Counting it as evidence against is not.
  - **Evidence favouring sparse or graph structure over dense attention is absent from §0.** Some of it sits in §1/§3 as "motivation", and none of it is weighed in the verdict. R4's own dossier verdict point 3 says "The opposite also holds".
    - R4-002: GAT-full (Transformer-like) reaches 91.51% vs MPNN-max 99.80% on 100-node reachability.
    - R4-176: plain Transformer 42.34% vs edge-state Relational Transformer 81.30% on CLRS OOD.
    - R3-105: Kuramoto steps 17→52% vs iterated self-attention 14→34%, "and hurt ID accuracy".
    - R4-063: fixed-depth Transformers' search difficulty "is not resolved even as the number of parameters is increased".
  - **Both sides are unmatched.** All of the above is unmatched (notes say so). But so is most of the "against" side with respect to the actual question.
- **Fix:**
  - Rewrite §0.2 as "**unknown; no direct evidence either way**".
  - Move R2-089/R2-097/R4-185/R5-092 into §0.1 as "recurrence pays per parameter, much less per FLOP".
  - Add a two-sided list of indirect, unmatched evidence on dense vs sparse/edge-structured attention: R4-002, R4-176, R3-105 and R4-063 on one side; R4-165, R1-088 and R1-091 on the other.
  - Keep "our prior: null" as **[ours]**, not as an evidence verdict.

### B2. §3/§4/§12: H* is not new. Softmax dispersion with growing N is a published theorem, and cheaper fixes exist that the design does not control for. "Clean either way" is therefore false.
- **Sentences:**
  - §3: "We additionally hypothesise that soft attention disperses as N grows past the training size, while top-k does not. This is not in our ledger and must be tested, not cited."
  - §12: "The design isolates the graph as one variable (k), so the answer is clean either way."
- **Evidence (fetched this session):**
  - Veličković, Perivolaropoulos, Barbero, Pascanu, *Softmax is not Enough (for Sharp Size Generalisation)*, https://arxiv.org/abs/2410.01104: "even for tasks as simple as finding the maximum key, any learned circuitry must disperse as the number of items grows at test time … prove this phenomenon theoretically, and propose adaptive temperature".
  - Vasylenko et al., *Long-Context Generalization with Sparse Attention* (ICLR 2026), https://arxiv.org/abs/2506.16640: "as sequence length increases, non-informative tokens accumulate attention probability mass, leading to dispersion … achieving up to 1000× length extrapolation on synthetic benchmarks".
  - Nakanishi, *Scalable-Softmax*, https://arxiv.org/abs/2501.19399: "causing the attention distribution to flatten as the context size grows … potentially limits its length generalization."
  - Hashemi et al., *Tropical Attention*, https://arxiv.org/abs/2505.17190: "stronger out-of-distribution generalization in both length and value … compared to Softmax-based and recurrent attention baselines" (a max-plus kernel, i.e. the §9 ablation-2 "max aggregation" idea).
  - None of these four is in claims.csv (grep: 0 hits).
- **Why it blocks:** if G2 beats T1, the most economical explanation is "sharper attention", which adaptive temperature / SSMax / α-entmax gives a looped Transformer **without any graph**. The headline then shows "softmax dispersion", which is already known, not "topology as computation".
- **Fix:**
  - Add the four papers to the ledger.
  - Restate H* as a known result to be *confirmed in the looped setting*.
  - Add a **T1-sharp arm**: T1 + SSMax or adaptive temperature, or α-entmax. V1/V2 then require G2 > max(T1, T1-sharp).
  - Only then does a G2 win say something about discrete selection, rather than about sharpness.

### B3. §3/§4/§8: k and the iteration budget are confounded. The ledger's own R4-179 says so, and the synthesis never cites it.
- **Sentence (§3):** "Design principle: make 'graph vs looped Transformer' a single variable." Combined with prereg: "T1 and G1–G3 get the same iteration budget T_max", and V4: "T_test = 4 × T_train".
- **Evidence:**
  - **R4-179 (DERIVED, verified below):** "for a 64-node path graph that is 63 message-passing steps vs 4 attention layers/loops". Its note says "matching 'iterations' across G1-G3 and T1 is not compute-neutral on reachability".
  - **R4-061 (THEOREM):** "logarithmic depth is necessary and sufficient for tasks like graph connectivity".
  - **R4-025:** DT-Recall needed "984 test iterations" for 59×59 mazes after training with ≤30.
- **What is wrong:**
  - Neighbourhood size changes how many steps a task needs: O(diameter) for G1 vs O(log n) for T1, with G2 in between depending on whether it learns long edges.
  - With one fixed T_max and a 4×-only test-time multiplier, a ladder of 16→1024 nodes (64×) or 9×9→59×59 mazes is **decided by the iteration budget, not inductive bias**. G1 on paths/mazes is guaranteed to fail.
  - G2 can "win" simply by learning shortcut edges, which is pointer doubling, i.e. what T1 already does.
- **Fix:**
  - Cite R4-179/R4-061 in §3.
  - Make T a stated function of instance size, T(n): diameter-scaled for local arms and log-scaled for global ones. Or give every arm T(n) = c·n and let halting cut it.
  - Report n* against *executed* iterations.
  - Drop "4× T_train" as a universal V4 rule, or apply it per arm on the T(n) scale.

### B4. §4: "G2 therefore costs at most T1's FLOPs per step" is false for the implementation actually specified in §7. Under the prereg's V1 condition this makes a G2 win impossible.
- **Sentences:**
  - §4: "G2 therefore costs at most T1's FLOPs per step (it saves 2N(N−k)d in aggregation and pays a top-k) … The arms are FLOP-comparable by construction."
  - §7: "G2 computes dense scores, `torch.topk`, then a boolean mask into SDPA or FlexAttention."
- **What is wrong:** the §7 pipeline computes QKᵀ (2N²d) for `topk`, then SDPA recomputes QKᵀ (2N²d) and does the full masked AV (2N²d).
  - Masked flash attention skips nothing, because R5-131 shows no tile is empty.
  - Executed FLOPs are therefore T1 + 2N²d + top-k. Top-k is a non-matmul op at 16× the matmul cost (R5-011), measured at 11.6–26.9% of training time in MaxK-GNN (R5-081).
  - The "saves 2N(N−k)d" is the FLOP count of a gather/scatter implementation that §7 relegates to an ablation.
  - **Prereg V1 requires the graph arm at "≤ T1's inference FLOPs".** With executed FLOPs, G2 can never satisfy V1. With analytic sparse FLOPs, the count describes code that is not run.
- **Also wrong:** "FLOP-comparable by construction" does not hold for G0/G1. Their per-step cost is ~2|E|d plus projections, far below T1's 4N²d. Combined with B3, they need far more steps.
- **Fix:**
  - Define one FLOP convention in DERIVATIONS D2: "useful FLOPs" (sparse-analytic) or "executed FLOPs". Use it in V1, and report the other beside it.
  - Fuse scoring with SDPA via FlexAttention `score_mod` top-k, or count the double scoring.
  - Delete "by construction".

---

## (c) MAJOR

### M1. §0.5 / §1 / §2 / §12: novelty is overstated, and the N2 claim contradicts its own source.
- **Sentences:**
  - §0.5: "Prior art with state-conditioned topology is not recurrent (Co-GNN R1-059; N2 R1-067 partial)".
  - §1: "none is weight-tied, iterated and halting".
  - §12: "The gap was confirmed absent by four independent searches."
- **N2 is recurrent:**
  - R1-067 quote: "N2 incorporates a recurrent layer to parameterize the displacements of graph nodes and pseudo nodes".
  - Source 2410.23686.txt l.587–588: "N2 updates the states of the embedded nodes recursively with a single recurrent layer … the associated parameters are shared across steps."
  - matrix A1-16 marks it "Yes (recurrent) / Yes: single shared recurrent layer".
- **G2's routing is old.** Per-query top-k attention is Explicit Sparse Transformer, https://arxiv.org/abs/1912.11637: "improve the concentration of attention on the global context through an explicit selection of the most relevant segments".
- **A recurrent + top-k combination exists.** *ReSSFormer* (Oct 2025), https://arxiv.org/abs/2510.01585, abstract: "Recurrent Reasoning & Memory Unit (R2MU) for iterative reasoning with bounded depth, Adaptive Sparse Attention Module (ASAM) for efficient and focused context selection, and Self-Organizing Encoder Structure (SOES)". Body: "For each query qᵢ, only the k highest-scoring keys are selected". Its baselines include no looped or Universal Transformer, and its tasks are NLP/QA. So the *matched-comparison* slot survives. Quality not assessed (two authors, arXiv).
- **The searches were thin.**
  - The "four independent searches" were each one or two long queries on the same day (R1 d1–d2, R2 d, R3 d, R4 e).
  - They were phrased in GNN vocabulary ("recurrent graph neural network … edges"), never in Transformer vocabulary ("looped / universal transformer + top-k / sparse / hard attention").
  - "Confirmed absent" violates CLAUDE.md rule 7.
- **Fix:**
  - Reword the open slot: the candidate's G2 ≈ **a looped Transformer with per-query top-k attention**. What is open is *the matched, size-extrapolation comparison* and the analysis of whether selection computes, not the architecture.
  - Add N2, ReSSFormer and Explicit Sparse Transformer to "Partial".
  - Run Transformer-vocabulary searches.
  - Replace "confirmed absent" with "not found in our search (queries, date)".

### M2. §4: positional information, and how T1 receives the task graph, are unspecified.
- **Sentence:** "S^t_ij = ⟨…⟩/√d_h + β·A_ij. Task structure is a bias, not a hard constraint, except in G0/G1."
- **Problem 1: who gets β·A?**
  - If T1 gets β·A, T1 is a graph-biased Transformer, and ablation 3 ("β on/off in G2") must also be run on T1.
  - If T1 does not, T1 vs G2 differ in k **and** in access to A. That is two variables.
- **Problem 2: sequence tasks have no position signal.** For sorting, MQAR and S5 (and maze cells) there is no A and no positional encoding in §4 (H⁰ = 0; Enc(X) only).
  - Attention without position is permutation-equivariant, so S5 and sorting are impossible.
  - The choice of positional encoding is a dominant factor in length extrapolation. It interacts with top-k, since local windows behave like relative position.
- **Fix:** specify the PE (identical across arms, extrapolation-safe) and state the A-access rule for every arm.

### M3. §4 step 4: the top-k gradient path is an optimisation confound, not an inductive bias.
- **Sentence:** "Gradients flow through the selected scores; selection itself is non-differentiable, as in MoE top-k."
- **Problem:** unselected pairs get zero gradient, so G2 cannot learn to pick an edge it never picks (an exploration problem). MoE needs noise and balancing losses for exactly this reason (R2-161 quote: "always produces large weights for the same few experts"). T1 gets dense gradients.
- **Fix:** add a k-annealing schedule (k from N down to k), Gumbel/noisy top-k, or straight-through, as a preregistered part of G2. Report selection entropy per step.

### M4. §4 step 1 / §6: the Parcae stability fix is applied to the wrong matrix.
- **Sentence:** "Z^t = H^t + P·Enc(X). P is constrained to spectral norm ≤ 1 (… R2-092 …)".
- **What the source says:** Parcae's "injection parameters" are **A**, the state transition in h_{t+1}=A·h_t + B·e. Source 2604.12946.txt l.84–90: "divergence conditions on the residual stream based on the spectral norm of A … parametrizes A as a negative diagonal matrix, constraining the spectral norm to prevent residual explosion". l.209: "Discrete LTI systems requires ρ(A) < 1".
- **Problem:** the §4 update has A = I (ρ = 1), which is the marginally stable case. P is the B analogue, which Parcae *normalises*, not constrains.
- **Fix:** H^{t+1} = Ā·H^t + B̄·Enc(X) + f(·), with Ā a ZOH-discretised negative diagonal, as in Parcae. Or justify A = I with R1-029's L2 state penalty.

### M5. §3/§4 step 7 vs PREREGISTRATION and BRIEF: halting is silently changed.
- **What changed:** the prereg defines "G3 = G2 + learned adaptive halting", and the brief asks for "learned adaptive halting". The synthesis makes G3 a fixed confidence/convergence rule and demotes learning to "an ablation only".
- **Assessment:** the reason is defensible (R2-152, R2-149), but it must be a dated prereg amendment, and §12 should tell Pavle that the brief's component was replaced.

### M6. §3: T0/G0 matching is undefined.
- **Problem:** "L distinct blocks, no loop" does not say whether parameters are L× T1's or width-reduced to match (prereg: ±5%). Saunshi's protocol (R4-080 note) reports both iso-param and iso-FLOP baselines. Pick one and state it, or run both.

### M7. §0.4 / §12: the GPU regime argument is misapplied.
- **Problem 1: the benchmark leaves the "N ≤ ~1k" regime.** 59×59 mazes = 3,481 nodes; reachability goes to n = 1024; DT-Recall's 201×201 is 40k nodes.
  - R5-133 simplifies to **N* = k·d** (with P_M = 2d²). For d=256, k=8, per-edge messages become *cheaper* than dense attention above 2,048 nodes, which includes the maze rung.
- **Problem 2: the cited claims do not support "dense masked attention is the fastest".**
  - R5-086 is a GCN on Reddit (232k nodes, V100).
  - R5-137 is an AUTHOR-CLAIM about framework overhead.
  - Neither benchmarks masked SDPA against gather at N ≤ 1k. This is an inference and should be labelled **[ours]**, to be measured.
- **Problem 3: §12 argues the wrong direction for LLMs.** "GPUs do not reward sparsity at these sizes (R5-131)" is used against the *LLM* substrate. LLM contexts are 4k–1M, where the R5-133 crossover flips and block-sparse top-k attention is a shipping practice (MoBA, R5-118; Quest, R5-119, both in the ledger). Drop that bullet or restate it correctly.

### M8. §0.3: two of the storage/capacity bounds are misapplied.
- **R3-071 (Dambre):** bounds *information-processing capacity* (memory of input history in a driven dynamical system). Quote: "bounded by the number of linearly independent state variables". It says nothing about parametric knowledge.
- **R3-036 / R3-040:** bound *fixed-size* recurrent state. The candidate's state is N×d and grows with the input, like attention's KV, so these bounds do not bind on it.
- **Fix:** §0.3 should rest on R2-017/R4-184 (direct, param-matched) and drop or relabel the rest.

### M9. §10 / §12: the statistics cannot establish the null that §12 plans to publish.
- **Problem 1: the interval is huge at 3 seeds.** The prereg uses a "seed-level 95% interval" at 3 seeds, so t(2) = 4.30 and the interval is roughly ±2.5 SD.
- **Problem 2: "tight interval" is not achievable.** §12's "If G2 equals T1 there, with a tight interval" cannot be met.
- **Problem 3: no equivalence test.** "T1 matches G2 within seed noise" is not an equivalence test.
- **Problem 4: n\* is too coarse.** It sits on a 3–4-rung ladder, so ties are the default.
- **Fix:**
  - Preregister an equivalence margin (TOST) on a continuous metric, e.g. accuracy-vs-n AUC or a fitted n\*.
  - Use ≥ 5 seeds on the pilot families.
  - Use a denser ladder.

### M10. §12: the cost estimate undercounts its own plan, and the dollar range is miscomputed.
- **Undercount:** "6 families × 6 arms × 3 seeds ≈ 108 runs".
  - §9 headline already has k ∈ {2,4,8,16} for G2. That is 9 arm-configs, or 162 runs before ablations 2–8.
  - The B2 T1-sharp arm adds more.
  - The prereg's per-arm tuning budget multiplies everything.
  - COGS needs more seeds (R4-123).
  - Maze evaluation at ~1,000 iterations with dense attention at N = 3,481 is not free.
- **Arithmetic:** 100–500 GPU-h × $0.45 = **$45–225**, not $50–300. $300 needs the 5090 median.
- **Fix:** derive the run count from §9 × tuning trials × seeds, then price it.

### M11. §1: "Full 14-question answers per approach are in matrix.csv" is overstated.
- **Counts:** of 121 rows, these are "unknown" or empty:
  - q11 GPU: 71
  - q10 more-iterations-help: 61
  - q9 capacity: 58
  - q8 stability: 53
  - q12 repos: 50
  - q7 scaling: 49
- **Why it matters:** the brief asked for all 14 per approach. Say "partially filled; unknowns marked", and give the counts.

### M12. §11 #2 / §12 gate: the T1 reproduction does not validate T1 on the study's tasks.
- **Problem:** `Leiay/looped_transformer` (R2-064) is in-context *linear regression*. Its note says "Linear-regression ICL task".
- **Fix:** reproduce Fan et al. 2409.15647 (R4-140, parity 20→40+ with adaptive loops) as the algorithmic T1 check, plus Saunshi's k×L protocol.

---

## (d) MINOR / wording

1. **§0.1, R4-080 status.** R4-080 is AUTHOR-CLAIM but is stated as fact ("nearly match"). Attribute it: "Saunshi et al. report …".
2. **§0.1, R2-016 / R2-093.** These are parameter-matched only, and Ouro spends ~4× FLOPs/token (R2-016 note). Print the mismatch beside the number (rule 2).
3. **§0.1, R4-165.** Add "without any hyperparameter optimization", which cuts toward a smaller gap. HRM is a *hierarchical* recurrent model, not a graph. Its relevance to "graph vs Transformer" is by analogy only.
4. **§0.4 and elsewhere: AUTHOR-CLAIMs used as fact.** R5-103 and R5-137 are AUTHOR-CLAIM; R4-005 is correctly flagged in §3.
5. **§12, R3-016.** R3-016 is generic LM storage. Cite R2-017/R4-184 for "storage cannot rise *with recurrence*".
6. **§0.4 / §4, R5-131 assumptions.** State them where it is used: uniform, independent targets with replacement; N = 512, k = 8, BS = 128.
   - Learned top-k biased by β·A on raster-ordered grids/mazes will be local, and could empty tiles.
   - At the training size (n = 16) the whole problem is one tile.
7. **R5-133 citation and conditions.**
   - The note reads Kaplan's "2 n_layer n_ctx d_attn" as "QK and AV each". In the source (2001.08361 Table 1) it is a single "Attention: Mask" term. 4N²d is right from first principles, so cite it as such.
   - State d = 256, k = 8, P_M = 2d² wherever "~2k nodes" appears (§0.4, §3).
8. **§6, R1-101.** It proves rank collapse without skips/MLPs. It says nothing about pre-norm.
9. **§0.2, R5-092.** The citation is fine, but it is evidence about recurrence per FLOP, not about the graph (see B1).
10. **§2 "Solved: sparse / dynamic routing does not pay on GPUs at small N".** One of its four IDs is DERIVED and two are AUTHOR-CLAIM. "Solved" is too strong; use "Supported (derived + indirect)".
11. **§12 gate: "≈ 1 day, < $20 assumed".** Label it ASSUMPTION, as the run-count estimate is.

---

## (e) Citation audit (36 IDs)

| Claim ID | Section | Supports? | Note |
|---|---|---|---|
| R4-080 | §0.1 | partial | AUTHOR-CLAIM stated as fact |
| R2-016 | §0.1 | Y | per-param only; FLOP mismatch not printed |
| R2-093 | §0.1 | Y | param-matched, not FLOP-matched |
| R4-165 | §0.1, §12 | partial | ~5pp correct; "without HPO" dropped; hierarchy ≠ graph |
| R3-125 | §0.1 | Y | |
| R3-128 | §0.1 | Y | |
| R4-166 | §0.1 | Y | |
| R2-089 | §0.2 | partial (wrong direction) | a looping win; does not test the graph |
| R2-097 | §0.2, §12 | partial | LM, tied vs untied; not graph vs looped |
| R4-185 | §0.2 | partial | LM loss; not graph vs looped |
| R5-092 | §0.2 | partial | number correct; same issue |
| R5-096 | §0.2 | Y | |
| R2-116 | §0.2 | Y | |
| R2-115 | §0.2 | Y | |
| R3-016 | §0.3, §12 | partial | generic LM; not about recurrence |
| R2-017 / R4-184 | §0.3 | Y | |
| R3-071 | §0.3 | N | input-memory IPC, not parametric storage |
| R3-036 / R3-040 | §0.3 | N (misapplied) | fixed-size state; candidate state grows with N |
| R3-002 | §0.3 | Y | |
| R5-086 | §0.4, §1 | partial | GCN/Reddit 232k nodes; does not show "dense masked fastest at N≤1k" |
| R5-137 | §0.4 | partial | AUTHOR-CLAIM; framework overhead, not dense vs sparse |
| R5-131 | §0.4 | Y (arith.) | assumptions not stated in synthesis |
| R5-133 | §0.4, §3 | Y (arith.) | conditional on d, k; Kaplan citation misread |
| R5-103 | §0.4 | partial | AUTHOR-CLAIM; early-exit setting |
| R4-016 / R4-021 | §0.5 | Y | |
| R4-095 | §0.5 | Y | |
| R1-059 | §0.5 | Y | |
| R1-067 | §0.5, §1 | N | source says N2 *is* weight-shared recurrent |
| R5-071 | §0.6 | Y | $0.45 median |
| R4-001 / R4-002 | §3 | Y | unmatched (noted in ledger, not in synthesis) |
| R3-028 | §3 | Y | |
| R2-092 | §4, §6 | N (wrong target) | Parcae constrains A (state), not the input injection |
| R2-036 | §5 | Y | 87.4→56.5% |
| R5-134 | §5 | Y | 4/3 |
| R4-123 | §5 | Y | |
| R4-024 / R4-025 | §8 | Y | DT numbers exact; peak chosen post hoc (ledger note) |
| R2-152 / R2-149 / R2-109 | §1, §4 | Y | |
| R1-029 / R1-027 / R1-023 | §1, §6 | Y | unmatched |
| R4-033 / R4-032 | §5, §10 | Y | R4-033 is AUTHOR-CLAIM, used as a pitfall (OK) |
| R1-101 | §6 | partial | no pre-norm claim |
| R2-193 / R2-195 / R1-141 / R1-143 | §11 | Y | licences match |

Tally: Y 24 · partial 13 · N 4. The N rows (R3-071, R3-036/040, R1-067, R2-092) are each load-bearing in one sentence.

---

## (f) What I checked and found sound

- **Re-derivations.**
  - R4-179: diameter of a 64-path = 63; ⌈log₃ 63⌉ = 4 (3⁴ = 81 ≥ 63). Correct. Caveat: 3^L is a construction bound for the Disentangled Transformer (R4-066), not a guarantee for a learned T1. On ER graphs the diameter is ~log n, so the asymmetry is worst on paths and mazes.
  - R5-131: 0.75^1024 = 10^(−127.9). Correct. At N = 1024: 0.875^1024 ≈ 10^(−59), so the conclusion holds across the ≤1k range under its stated assumptions.
  - R5-133: 131,072·8/512 = 2,048. Correct. In general N* = k·d.
- **Numbers.** Every number I sampled matches its quote exactly: 99.80/91.51, 97.12, 97.30, 6.8–18%, r^0.46, 410M/580M/1B, +3.4, 87.4→56.5, ±6–8%, 38%, $0.45/$0.60.
- **Structure.** All 12 requested outputs are present and in brief order.
- **Critical question.** It is answered directly: yes vs fixed-depth, attributed to recurrence.
- **Design choices that survive.**
  - The looped-Transformer comparator (prereg) is the right one.
  - The storage-vs-computation split is correctly grounded in R2-017/R4-184.
  - The nesting T1 = G2 at k = N is a good design idea once B2–B4 are fixed.
  - The shortcut and pitfall controls in §5/§8 (percolation, balanced lookahead, graph-level exact match) are well sourced.
  - The analytic-FLOP + `FlopCounterMode`-cross-check rule (R5-049) is correct.
- **Scope decisions.** Excluding hyperedges and persistent memory from v1 is justified, and the brief's "if justified" clause is respected.
- **Literature search.** Beyond the ReSSFormer lead (M1), I found no paper running a recurrent learned-topology graph against a matched looped Transformer on size extrapolation. Searches: "looped transformer top-k sparse attention length generalization algorithmic 2025" and "recurrent graph neural network learned dynamic topology versus looped transformer size extrapolation 2026 arXiv". The matched-comparison slot looks open. The *architecture* slot does not.
