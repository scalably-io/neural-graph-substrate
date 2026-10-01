# SR-2026-006 synthesis v0.4: is a self-routing recurrent neural graph a better substrate than a Transformer?

Status: DRAFT v0.3, 2026-10-01.
- **Evidence.** The merged ledger: `evidence/claims.csv` (891 claims) and `evidence/matrix.csv` (121 approaches), 0 rejected.
- **Review history.**
  - v0.2 answered fresh-context review round 1 (`docs/reviews/R1-opus.md`).
  - v0.3 answers round 2 (`docs/reviews/R2-opus.md`).
  - Every blocker and major in both rounds was accepted after re-verification. Reversals are in `docs/NEGATIVE-FINDINGS.md`.
- **Conventions.**
  - Every factual sentence cites claim IDs; **[ours]** marks our reasoning or design.
  - Literature comparisons are unmatched unless stated. Two IDs naming the same source count once: R2-017 = R4-184 and R4-165 = R2-046.

## 0. Verdict first

1. **Against a fixed-depth Transformer: yes, but the gain comes from recurrence, which a looped Transformer already has.**
   - Saunshi et al. report that k layers looped L times nearly match kL layers (R4-080, AUTHOR-CLAIM).
   - Ouro reports 2–3× parameter efficiency, matched on parameters only. At 4 loops it spends ~4× the per-token FLOPs of a non-looped model its own size (R2-016 note) and ~1.4× those of its 4B comparator (R2-199, DERIVED).
   - Parcae beats parameter-matched, not FLOP-matched, Transformers (R2-093).
   - Per FLOP, recurrence pays much less:
     - SMELT saves 6.8–18.0% of training FLOPs under strict parameter + FLOP + KV matching, a modest win for looping (R2-089).
     - At r = 4, a 410M looped model matches 580M in loss at a 1B model's training cost (R5-092).
     - One recurrence is worth r^0.46 unique blocks on LM loss (R4-185).
2. **Against a weight-shared looped Transformer: unknown, with one direct two-arm data point in favour of sparse routing.**
   - **Direct (found by the R7 sweep):** LT2 (May 2026) compares, inside the same weight-tied loop at the same parameter budget, a learned top-k sparse attention (NSA) with dense attention. On a state-tracking + recall task the sparse loop solves n_max = 128 vs 64 for the dense loop, at every loop count T (R7-005, R7-006, R7-007).
   - **Limits of LT2:**
     - trained at each size along a curriculum, not train-small/test-large (R7-004);
     - no sharpened-attention arm;
     - not FLOP-matched (the sparse arm uses fewer FLOPs);
     - routing is causal top-k over earlier tokens, not a graph over all nodes rebuilt each step.

   The remaining indirect evidence is unmatched and splits:
   - **For hard, discrete selection** (all step- or hint-supervised processors, unlike the proposed design):
     - a max-aggregation MPNN scores 99.80% on 100-node reachability vs 91.51% for full attention (R4-001/002);
     - Discrete NAR reports hard attention as important for size generalisation, 16 → 1600 nodes (R6-010, R6-011, AUTHOR-CLAIM).
   - **Against:**
     - in one recurrent pipeline, a plain Transformer came within ~5 points of HRM's brain-inspired hierarchy without hyperparameter optimisation (R4-165). HRM is hierarchical, not a graph, so this is analogy only;
     - tuned simple baselines erase reported architecture gaps (R1-088, R1-091).
   - **Related but not about selection:** the Relational Transformer, which adds edge-state features, scores 81.30% vs 42.34% for a plain Transformer OOD on CLRS (R4-176). This bears on edge features, which every arm in our design receives.
   - **A competing explanation to control for:** adding a causal convolution (pure locality) to TRM lifts A5 state-tracking accuracy at 4× the training length from 45.8% to 91.4% (R7-032, R7-033). Locality alone can look like "routing"; G1 (fixed local graph) is the control for it.
   - **Not on either list:**
     - R3-105 is oscillator dynamics, not routing;
     - R4-063 is about fixed-depth Transformers only.

   **[ours]** Our prior is a null, and it is a prior, not a verdict.
3. **Recurrence does not raise knowledge storage.** One controlled study, the Ouro physics-of-LMs probe, finds ~2 bits per parameter for looped and non-looped models alike (R2-017).
4. **The architecture and its mechanism are not new. Only a matched test is open.**
   - Per-query top-k attention dates from 2019 (R6-008).
   - A 2025 model combines a recurrent reasoning unit with per-query top-k attention (R6-006, R6-007). Its baselines include no looped Transformer, and its extrapolation test is LM context length (trained on 4k tokens, tested longer), not algorithmic instance size (review R3 B3; the v0.3 sentence "tests no size extrapolation" was false).
   - N2 uses one weight-shared recurrent layer with dynamic pathways (R1-067).
   - Hard attention inside a recurrent loop, for size generalisation, is published, though hint-supervised and over task-graph neighbours (R6-010).
   - The Neural Data Router gets 100% length generalisation with a weight-tied Transformer and sharp geometric attention (R6-012).
   - Masked hard attention plus iteration plus halting has a provably correct construction (R6-013).
   - Soft attention must disperse as items grow (R6-001, THEOREM). Sharpening fixes it without a graph: adaptive temperature (R6-002), Scalable-Softmax (R6-004), and ASEntmax, which beats fixed α-entmax and reaches up to 1000× length extrapolation (R6-016).

   - **The two-arm loop comparison exists:** LT2 (R7-001–R7-008) runs learned top-k sparse vs dense attention in the same weight-tied loop at equal parameters, trained at each size.

   **Not found in our search:** the same comparison **plus** a sharpened-attention (ASEntmax) looped arm and a fixed-local-graph arm, with top-k over **all** nodes rebuilt each step, at equal steps and no more FLOPs, on **train-small / test-large** size extrapolation. Coverage:
   - GNN vocabulary: R1 d1–d2, R2 d, R3 d, R4 e;
   - Transformer vocabulary: the R7 sweep (22 web, 40 arXiv-API and 16 Semantic Scholar queries; 12 of the 16 were rate-limited and logged as failures, not negatives) plus review rounds 1–3, all 2026-10-01.

   ChainGPT (ICLR 2026, recurrent depth + "state-guided sparse attention") could only be read as an abstract; its full text was ACCESS-FAILED. It is a residual risk to the novelty claim.

   **[ours]** A reviewer would call our study an extension of LT2, not a replication: it adds the sharpness control, a locality control, size extrapolation and compute matching.
5. **GPU cost [ours, to be measured].**
   - Training sizes are 16 nodes and 81 maze cells. Test sizes reach 1,024 nodes and 1,089 cells.
   - At these sizes, dense masked attention is the likely fastest implementation. Gather/scatter is memory-bound in large-graph measurements (R5-086). Random top-k leaves no empty 128×128 tile under uniform targets (R5-131, N = 512, k = 8).
   - At long context, sparse top-k attention does pay (R5-017, R5-041, R5-042), so GPU cost is no argument against the idea at LLM scale.
6. **Recommendation [ours]: one small study, reframed.**
   - **The question:** does hard, self-chosen routing add anything inside a looped model beyond recurrence and attention sharpness?
   - **What makes it worth running:**
     - the comparison was not found in our search;
     - routing is the single trained difference between arms;
     - the step budget comes from the task;
     - the outcomes are mutually exclusive and a null is publishable.
   - **Not recommended:** a new LM substrate.

## 1. SOTA map

14-question answers per approach are in `evidence/matrix.csv`. The matrix is only partly filled: of 121 rows, the number marked "unknown" or "n/a" per question is:

| q7 scaling | q8 stability | q9 capacity | q10 more iterations help | q11 GPU | q12 repos |
|---|---|---|---|---|---|
| 52 | 59 | 77 | 80 | 73 | 53 |

The full count is in E011. Question 10 is the brief's central one and the least covered.

| Family | What it shows for this question | Key IDs |
|---|---|---|
| Message passing | 1-WL ceiling at any depth; depth × width must grow with n; depth does not cure over-squashing; oversmoothing even with state-dependent attention | R1-002/003, R4-069, R1-013, R1-008/009 |
| Recurrent GNN | 1,000× size extrapolation with stabilisers; collapse after ~100 rounds without L2 state regularisation | R1-027, R1-029 |
| Dynamic / rewiring | Co-GNN per-layer state-conditioned topology; N2 recurrent + dynamic pathways; edges trade over-squashing for oversmoothing | R1-059, R1-067, R1-016 |
| Graph transformers | Gains over tuned MPNNs shrink | R1-088, R1-091 |
| Hypergraph / topological | No recurrent substrate with learned hyperedges found; more rounds degrade HGNNs | R1-104–106, R1-166 |
| NCA | Shared local update on a persistent graph; sample-pool stabilisation | R3-089, R3-087 |
| Looped Transformers | Input injection needed past the trained loop count; OOD variance high and reduced by stochastic loop counts; LM test-time recurrence degrades or saturates | R2-064/065, R6-014/015, R2-018, R2-095 |
| Sharp / sparse / hard attention | Top-k (2019); recurrent + top-k (2025); dispersion theorem; ASEntmax; NDR; hard attention in Discrete NAR; masked hard attention + halting construction | R6-008, R6-006/007, R6-001, R6-016, R6-012, R6-010, R6-013 |
| Recursive reasoning (HRM, TRM) | Refinement + deep supervision drive results; 1-step gradient costs 87.4 → 56.5% | R2-048, R2-036 |
| DEQ / Neural ODE | O(1)-memory implicit training but 3–4× slower; NFE growth | R5-034, R2-128, R2-137 |
| Hopfield | Attention = Hopfield retrieval within an input; sparse retrieval bound tighter | R3-002, R3-028 |
| Predictive coding / EqProp | Worse with depth; ~100× backprop compute | R3-054, R3-066 |
| Reservoir | Fixed random topology loses at equal trainable parameters | R3-081 |
| Halting | Convergence exits cut depth 38%; ACT can collapse; confidence ≈ learned gates | R2-109, R2-149, R2-152 |
| Routing (MoE / MoD / MoR) | Top-k over experts, tokens or depth, not edges; collapse without balancing | R2-160, R2-175, R2-161 |
| Learned connectivity / NAR | Wiring learned once (DNW, RigL); per-step edges only with supervision; DT-Recall prefix sums 32 → 512 at 97.12% (peak chosen post hoc); maze extrapolation mostly dead-end filling | R4-086, R4-089, R4-016, R4-024, R4-032/033 |
| Oscillatory | AKOrN: more test-time steps help, while extra self-attention steps hurt in-distribution accuracy; CTM synchrony readouts | R3-105, R3-099 |
| GPU measurement | FLOP counters count 0 for scatter / gather / top-k; non-matmul ≈ 16× matmul cost (A100) | R5-049, R5-011 |

## 2. Novelty map

| Status | Item | Evidence |
|---|---|---|
| **Established** | Attention is message passing on a complete graph with soft, state-conditioned routing (an identity) | R4-070, R1-099, R3-002 |
| Established | Recurrence does not add knowledge storage (one controlled study) | R2-017 |
| Established | Softmax dispersion with N (theorem); sharpening fixes | R6-001, R6-002, R6-016 |
| Established | Per-query top-k attention; recurrence + top-k as an architecture | R6-008, R6-006/007 |
| Established | Looped Transformers simulate graph algorithms (constructions) | R1-098, R4-173 |
| **Supported, with caveats** | Time replaces depth on local and sequence algorithmic tasks (one paper family; dead-end shortcut on mazes; LM recurrence saturates) | R2-157, R4-024, R4-032/033, R2-095 |
| Supported, with caveats | Recurrent GNNs extrapolate in size with stabilisers | R1-027, R1-029 |
| Supported, with caveats | Hard selection helps size generalisation (hint-supervised) | R6-010, R4-001/002 |
| **Partial** | Sparse routing does not pay on GPUs at small N | R5-131 (DERIVED), R5-086, R1-135 (AUTHOR-CLAIM) |
| Partial | Per-step edge creation with pointer supervision | R4-016, R4-021 |
| Partial | Halting from confidence / convergence vs learned gates | R2-109, R2-152, R2-149 |
| Partial | Hyperedges in looped models (constructions) | R4-182, R4-183 |
| **Partial (new, R7)** | Learned top-k sparse vs dense attention in the same weight-tied loop, equal parameters, trained at each size: sparse doubles n_max | R7-005, R7-006 |
| **Open** (not found in our search) | §0.4's extension: plus ASEntmax and fixed-local controls, top-k over all nodes, train-small/test-large, compute-matched | §0.4 |
| Open | Learned hyperedges as a compute substrate | R1 d3, R4 e2 |
| Open | Node roles that evolve during computation (brief component C13): no design found or proposed | — |

## 3. Design for the first study [ours]

Full specification: `docs/PREREGISTRATION.md` v0.3.

- **Arms.** T0 (iso-param; iso-FLOP reported), T1, T1-sharp (ASEntmax), G0, G1, G2 (k = 8), G3 (learned halting + rule control).
- **One shared recipe for every looped arm:**
  - stochastic loop counts (R6-015);
  - deep supervision;
  - the Parcae-style stable transition (R6-009);
  - input injection;
  - a learned β·A bias;
  - the same tuning budget.
- **G2 differs from T1 only in its routing rule.** Gumbel noise and k annealing are ablations, not part of the headline (review R2 M1).
- **Positions.** Random identifiers, fixed a priori, the same for all arms.

**Hypothesis under test, revised twice.** Hard, unsupervised top-k routing over all nodes inside a weight-tied loop extrapolates further than dense and ASEntmax attention in the same loop.
- What is established:
  - soft attention disperses (R6-001);
  - sharpening helps (R6-016);
  - hard attention helps when supervised (R6-010).
- Untested: whether **learned hard routing beats strong sharpening** without supervision.

**Not in the first study:**
- **Hyperedges:** no positive evidence (R1-166).
- **Cross-input persistent memory:** the brief asks for it, but no evidence motivates it for these tasks. R3-002 covers only within-input retrieval, so this is a scope choice, not a finding.
- **Evolving node roles (C13):** no concrete mechanism proposed. This is stated as a gap.
- **Per-edge MLP messages:** more FLOPs than attention below N = k·d (R5-133).
- **Local learning rules:** R3-054, R3-066.

## 4. Mathematical formulation

Instance with N nodes, inputs X, optional adjacency A, state H^t ∈ ℝ^{N×d}, H^0 = 0.

1. **Transition and input injection:**
   H̃^t = Ā ⊙ H^t + B̄·Enc(X)
   Ā = exp(Δ·Λ), with Λ negative diagonal, so ρ(Ā) < 1 (R6-009).
2. **Scores:**
   S_ij = ⟨W_Q LN(h̃_i), W_K LN(h̃_j)⟩/√d_h + β·A_ij + ⟨id_i, id_j⟩-based position terms (the same for all arms).
3. **Routing:**
   - T1: softmax over j.
   - T1-sharp: ASEntmax over j.
   - G1: softmax over A-neighbours.
   - G2: softmax over TopK_j(S_ij, 8).
4. **Messages:** m_i = Σ_j α_ij W_V LN(h̃_j). For G2, a gather over the selected j that reuses S (D2).
5. **Update:**
   H^{t+1} = H̃^t + W_O m + MLP(LN(H̃^t + W_O m))
6. **Readout and loss:**
   ŷ_i^t = R(LN(h_i^{t+1})), with loss Σ_{t ∈ sampled steps} w_t Σ_i ℓ(ŷ_i^t, y_i).
   Evaluation reads out at the last step only.
7. **Halting (G3):** p_t = σ(w·pool(H^t)), ACT-style, with a minimum of 2 steps and a maximum of T(n).

**Cost** (D2, `ngs/flops.py`).
- Matmul per step = 8Nd² + 4N·d_ff·d + 2·P_s·d + 2·P_m·d.
- G2/T1 matmul at d = 128: 0.995 (N = 16), 0.879 (N = 256), 0.717 (N = 1024).
- ASEntmax adds non-matmul bisection cost.
- Selection and entmax constants are calibrated on the rented GPU before any compute claim.

## 5. Iteration budget (D3)

Every looped arm runs the same T(n) = ⌈1.5 × q₀.₉₉(D)⌉, where D is the steps a local exact algorithm needs, computed from the task alone:

Values are generated into `docs/generated/budgets.md` (1000 instances, seed 0), never typed. Endpoints:

| Family | T(n) |
|---|---|
| Reachability | 12 → 56 at n = 16 → 1024 |
| Shortest path | 9 → 23 at n = 16 → 1024 |
| Maze | 81 → 737 at sides 9 → 33 |
| Sorting / S5 | 1.5·n |
| Recall | 72 → 1152 at 16 → 256 pairs |

Readout is at the last step; best-over-steps is reported only as an upper bound. This replaces v0.2's fixed FLOP grid, which floored every arm at n ≥ 256 (review R2 B1, reproduced: T1 could afford 0.76 steps at n = 256 and 0.11 at n = 1024 with c = 1).

## 6. Training strategy and statistics

- **Gradient.** Full BPTT, no 1-step gradient (R2-036). Checkpointing if memory binds (+33% FLOPs, R5-134).
- **Data controls:**
  - reachability band-sampled to 20–80% reachable (the plain generator gave only-the-source instances in 9–11 of 50 at each size);
  - shortest path labelled by valid predecessors, since distances outgrow the training range (review R2 M10);
  - mazes on the cell graph, with cycles as a separate structure-shift test (R4-033).
- **Statistics:**
  - paired seeds;
  - n_seeds from a pilot power rule (5 to 15);
  - mutually exclusive outcomes (superior / inferior / equivalent / inconclusive) with a validity gate against floor and ceiling;
  - an intersection–union test against both T1 and T1-sharp;
  - Holm correction across families;
  - no interim stopping.

## 7. Stability techniques

| Technique | Failure addressed | IDs |
|---|---|---|
| Input injection | divergence past the trained loop count | R2-065, R2-156 |
| Negative-diagonal transition | residual explosion | R6-009 |
| Stochastic loop counts | OOD variance, step-count overfitting | R6-015 |
| Progressive / sampled-step loss | iteration-specific behaviour | R3-119 |
| Residual + MLP around attention | rank collapse | R1-101 |
| EMA of weights | collapse on small data | R2-041 |
| Bounded halting | ACT collapse | R2-149 |
| Gumbel / annealing (G2 ablation only) | router collapse; supported only for noise + balancing, not annealing | R2-161 |

Residual risks: convergence ≠ correctness (R2-053, R4-034); orbits (R2-014).

## 8. GPU implementation

- **Stack.** PyTorch, bf16, fixed shapes.
- **Attention kernels.**
  - T1: SDPA. Additive N² biases (β·A, position terms) fall back from FlashAttention to a materialised-bias kernel; the same applies to every arm.
  - T1-sharp: entmax over dense scores.
  - G1: masked SDPA.
  - G2: dense QKᵀ, top-k, gather.
- **FLOPs.** From `ngs/flops.py`, cross-checked with `FlopCounterMode` (blind to scatter / top-k, R5-049).
- **Hardware.** Same SKU, same session (R5-108). RTX 4090 / 5090 medians: $0.45 / $0.60 per hour (R5-071/072).

## 9. Benchmark suite

Details in PREREGISTRATION. Six families, all with a ×√2 ladder and graph- or sequence-level exact match:
- reachability and shortest path, 16 → 1024 nodes;
- mazes, 9 → 33 cells per side (cell graph), percolation 0 and 0.3;
- sorting and recall, 16 → 256;
- S5, 16 → 512.

COGS / SCAN come next; language only if V1 is supported.

## 10. Ablations (secondary, costed separately)

- Gumbel noise and k annealing in G2.
- k = 4.
- Fixed 1.5-entmax and Scalable-Softmax as T1-sharp variants.
- Max aggregation (R4-001; max-plus attention, R6-005).
- β·A off in all looped arms.
- Injection off.
- Ā = I + L2 state penalty.
- Deep supervision at the last step only.
- Memory slots (C9), hyperedges (C7): only after a routing effect.

## 11. Failure modes

- G2 equivalent or inferior to T1 or T1-sharp on ≥ 4 informative families: the gain is recurrence and sharpness, not routing (our prior).
- Families at floor or ceiling make the study uninformative there. The validity gate reports this rather than counting it as a null.
- G2 wins only by learning the long-range shortcut edges that T1 already has.
- G2's selection collapses to a fixed or degree-based pattern (R2-161).
- Steps beyond need degrade or orbit (R2-018, R2-014, R4-034).
- Size gains without structure gains (R4-033).
- Wall-clock fails V5 even though G2 executes fewer matmul FLOPs (R5-081).
- OOD variance swamps effects (R6-014). The power rule reports "underpowered" rather than a null.

## 12. Reproduce first, then the verdict

**Reproduce first** (validates arms on our harness):

| # | What | Why | Licence |
|---|---|---|---|
| 1 | DT-Recall prefix sums / mazes | time replaces depth (R4-024/025) | MIT (R2-193) |
| 2 | Fan et al. looped Transformer length generalisation (parity 20 → 40+, R4-140) | the T1 arm on algorithmic tasks | to check |
| 3 | ASEntmax (R6-016) | the T1-sharp arm | to check |
| 4 | Discrete NAR (R6-010/011) | hard attention on the 16 → 1600 ladder | to check |
| 5 | Grötschla recurrent GNN; zoology MQAR; SALSA-CLRS | the G1 arm; recall family; graph ladder | Apache-2.0 (R1-141, R4-148, R4-143) |

**Verdict [ours].**
- **New LM substrate: no.**
  - Recurrence cannot raise storage (R2-017).
  - Looping wins only modestly per FLOP under strict matching (R2-089), and loses per training FLOP in an iso-depth study (R5-092).
  - LM test-time recurrence saturates (R2-095).
  - The architecture already exists (R6-006/007).
- **Focused paper: yes, reframed and smaller than the brief imagined.**
  - **The question:** "does learned hard routing add anything beyond recurrence and sharpness?"
  - **Positioned as:** an extension of LT2 (R7-005/006), which already shows sparse > dense in a loop at equal parameters on in-distribution capacity. Our contribution is the controls LT2 lacks: sharpening, locality, size extrapolation, compute matching.
  - **Why it is worth it:** the comparison was not found, the design makes routing the single trained difference, and every outcome is publishable.
  - **What it is not:** "a new computational substrate". The paper should say so plainly.
- **Cost (ASSUMPTION until the pilot measures it).**
  - **Headline runs:** 8 configurations (T0 iso-param, T0 iso-FLOP, T1, T1-sharp, G0, G1, G2, G3) × 6 families × 5–15 seeds (power rule) = 240–720 runs.
  - **Tuning:** ≈ 100 run-equivalents.
  - **Hours:** at an assumed 0.5–2 GPU-hours each, ≈ 170–1,640 GPU-hours.
  - **Price:** ≈ $75–740 at $0.45 per hour.
  - Ablations are extra (≈ 300–900 runs) and optional.
  - The pilot's first job is to replace these assumptions with measured per-run cost, starting with the 33×33 maze rung (1,089 nodes × 737 steps).
- **Gates before spending**, all before the freeze:
  1. Transformer-vocabulary novelty sweep: done (R7, 2026-10-01). It found LT2; the study is repositioned as its extension. ChainGPT's full text remains unread.
  2. Reproductions #1–#3. Cost unknown; the pilot measures it.
  3. EXPLORATORY pilot for σ and cost, on separate seeds.
  4. Pavle approves and `prereg-v1` is tagged.

  No interim stopping after the freeze.
