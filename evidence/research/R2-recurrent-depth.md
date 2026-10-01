# R2 — Recurrent depth, equilibrium, continuous depth, halting, routing

Researcher R2 · retrieved 2026-10-01 · ledger `R2-recurrent-depth.csv` (206 claims) · matrix `R2-matrix.csv` (25 approaches, A2-01…A2-25). Every number below cites a claim ID. Each claim row carries a verbatim quote, and every quote was machine-checked against the downloaded source text in `evidence/sources/R2/`.

## (a) Verdict first

1. **The strongest competitor already covers most of the hypothesis.** It is the stabilised weight-shared looped / recurrent-depth Transformer with input injection (Huginn, Parcae, Ouro; TRM on puzzles). Between them, these models already cover C1, C3, C4, C5, C11 and C12, with partial C6, C8 and C10. The parts that are new in the candidate are a sparse graph (C2), hard top-k edge creation (C6), hyperedges (C7), persistent memory (C9) and evolving topology (C13).
2. **Recurrence buys computation per stored parameter, not storage.** Looped and non-looped models both store about 2 bits per parameter (R2-017, R2-085). Looping gives 2–3× parameter efficiency at matched parameters (Ouro, R2-016; Parcae, R2-093, R2-094), but those comparisons are not FLOP-matched: Ouro spends about 1.4× the forward FLOPs of its 4B comparator (R2-199).
3. **At matched FLOPs, looping's advantage is small or negative.** Under triple matching (parameters, FLOPs, KV cache), looping saves 6.8–18% of training FLOPs (R2-089). With fresh data and single-epoch training, untied weights are more compute-efficient (R2-097). Post-trained looped LMs are less accurate than the non-looped model at matched test-time compute (R2-115). Autoregressive TRM gives no reliable gain at matched compute (R2-058, R2-059). Most prior gains conflate architecture with extra FLOPs (R2-090). The candidate must therefore win where looping itself barely wins.
4. **Extra iterations beyond the training horizon: yes on synthetic algorithmic tasks, mostly no at LM scale.** On algorithmic tasks with input injection, progressive training or a fixed-point objective, extrapolation works (mazes 9×9→201×201, R2-157; R2-064; R2-104). At LM scale, performance degrades past the trained depth (Ouro, R2-018), saturates (Parcae, R2-095), or gives marginal gains with non-settling dynamics (Huginn, R2-204, R2-106).
5. **On HRM and TRM, the gains come from the training loop, not the architecture.** A parameter-matched plain transformer lands within about 5 pp of HRM (R2-046). The outer refinement loop plus deep supervision drives the result (R2-048, R2-050), and the ARC score is largely per-task fitting (R2-051). TRM needs about 1000× augmentation; without it, it scores 0.00 under one replication protocol (R2-105).
6. **Halting saves compute but is fragile.** Convergence exits cut depth 38% at matched quality (R2-109), and ACT recovers 34% of compute in one setting (R2-114). However, ACT and PonderNet collapse to one loop on a looped LLM (R2-149), and simple confidence readouts match learned gates (R2-152). Top-k routing on GPUs needs static shapes, load balancing and custom kernels (R2-169, R2-172, R2-174, R2-175).

## (b) C1–C13 coverage by the closest prior art

Prior art columns:
- **LT**: looped / recurrent-depth Transformer (UT, Huginn, Ouro, Parcae).
- **MoR**: Mixture-of-Recursions.
- **TRM/HRM**: tiny or hierarchical recursive reasoning models.
- **LT+Mem**: looping plus memory tokens or memory banks.

Cell values: Y = yes, P = partial, N = no.

| Component | LT | MoR | TRM/HRM | LT+Mem | Note |
|---|---|---|---|---|---|
| C1 persistent node states h_i | Y (R2-001, R2-007) | P (R2-022) | Y (R2-031, R2-043) | Y (R2-113) | In all of these, "nodes" are tokens or cells, not free latent nodes |
| C2 sparse directed graph | N (R2-001) | P (R2-025) | N (R2-038) | N | Attention is dense; only MoD/MoR prune token subsets (R2-175) |
| C3 shared message function M | Y (R2-001) | Y (R2-026) | Y (R2-039) | Y (R2-113) | Attention is a shared, state-conditioned message function |
| C4 shared update function U | Y (R2-001, R2-006) | Y (R2-026) | Y (R2-039) | Y | |
| C5 recurrent evolution over T steps | Y (R2-007, R2-018) | Y (R2-022) | Y (R2-034) | Y (R2-111) | |
| C6 learned top-k routing / edge creation | N | P, over depth not edges (R2-025) | N | N | MoE (R2-160) and MoD (R2-175) do top-k over experts or tokens, never over node-to-node edges |
| C7 hyperedges | N | N | N | N | Not found in our search |
| C8 state-conditioned topology | P, soft attention (R2-001) | P, router (R2-022) | N | N | |
| C9 persistent associative memory | N | N | N | P, learned slots, not persistent across inputs (R2-111, R2-113) | |
| C10 distributed readouts | P, per-step LM heads (R2-020) | N | P, deep supervision (R2-048) | N | Readouts are spread over depth, not over graph regions |
| C11 confidence / convergence signal | Y (R2-013, R2-109) | N | Y, Q head (R2-032) | N | DEQ solver tolerance as well (R2-123) |
| C12 learned adaptive halting | Y (R2-003, R2-020) | Y, per token (R2-022) | Y (R2-032, R2-044) | Y (R2-114) | Fragile (R2-142, R2-149) |
| C13 topology and node roles evolve | P (R2-001) | P (R2-025) | N | N | Only soft attention or token-subset changes |

## (c) Failure evidence against the hypothesis

**"A looped transformer already does this."**
- R2-046, R2-047: a parameter-matched transformer is within about 5 pp of HRM.
- R2-069, R2-070: k×L looping nearly matches a kL-layer model.
- R2-093, R2-016: parameter-efficiency gains already exist without any graph.

**No gain once FLOPs are matched.**
- R2-097: untied weights beat tied weights at matched compute (single epoch).
- R2-115, R2-117: looped post-trained models lose to the non-looped one at matched compute.
- R2-058, R2-059: untied depth gives the best generalisation per block evaluation.
- R2-089: only 6.8–18% savings even with careful matching.
- R2-206: a looped model has less non-recurrent capacity at matched FLOPs.
- R2-181, R2-179: UTs are compute-inefficient for language modelling.

**Capacity is bounded by stored parameters.**
- R2-017, R2-085, R2-086: about 2 bits per parameter, looped or not.
- R2-070: looped models have worse perplexity and memorisation than the iso-FLOP model.
- R2-111: looping helps math, while memory is needed for commonsense.

**Extra iterations do not help, or hurt.**
- R2-018, R2-019: Ouro degrades past T=4.
- R2-095: loss saturates with test-time loops.
- R2-204: Huginn's gains are marginal.
- R2-106, R2-107: whether more depth helps depends on the training objective.
- R2-100: retrofit extrapolation stops at about 1.5× the supervised depth.
- R2-156, R2-155: overthinking.
- R2-050: inference loops matter less than training loops.
- R2-103: truncation-based evaluation overstates the contribution of depth.

**Instability.**
- R2-008, R2-009: collapse in the first large Huginn runs.
- R2-092: residual explosion in looped models.
- R2-065: divergence without input injection.
- R2-041: HRM diverges on small data.
- R2-126, R2-127, R2-130: DEQ instability and growing iteration counts.
- R2-137, R2-138: Neural ODE NFE growth.
- R2-142, R2-144, R2-149, R2-020: halting collapses.
- R2-161, R2-165: router collapse and loss divergence.

**Convergence ≠ correctness.**
- R2-053, R2-054: multiple fixed points; HRM fails on a single unknown cell.
- R2-057: TRM gets trapped in bad latent basins.
- R2-014: Huginn shows orbits and sliders, not fixed points.

**GPU-hostile.**
- R2-128: DEQ is 3–4× slower than explicit networks.
- R2-125: MDEQ is slower than explicit networks.
- R2-169: top-k routing forces a choice between dropping tokens and padding.
- R2-172: all-to-all dispatch takes up to 60% of training time.
- R2-174: naive per-expert loops are 17.7× slower.
- R2-177: top-k is non-causal.
- R2-178 (low confidence): routers over graphs and depth show the same collapse signature as attention.

**Evidence in favour of recurrence itself, which supports the T1 arm rather than the graph.**
- R2-157, R2-158: easy-to-hard extrapolation.
- R2-073, R2-074, R2-077: log-depth loops solve problems that fixed depth cannot.
- R2-101: depth extrapolation on multi-hop knowledge composition.
- R2-112: the iso-FLOP win on math.
- R2-132: path independence predicts upward generalisation.

## (d) Unexplored ("not found in our search", all searches run 2026-10-01)

| Gap | Search query |
|---|---|
| Looped transformer vs recurrent GNN or graph substrate on algorithmic extrapolation at matched parameters **and** FLOPs | "looped transformer versus recurrent graph neural network matched parameters matched FLOPs algorithmic extrapolation comparison" |
| Weight-shared recurrence with learned sparse top-k node-to-node edges, state-conditioned topology and adaptive halting together | "weight-shared recurrent model learned sparse top-k edges between latent nodes state-conditioned topology adaptive halting reasoning" |
| Evidence that continuous depth (Neural ODE) gives reasoning or algorithmic gains over discrete recurrence | "neural ODE continuous depth reasoning algorithmic extrapolation gains over discrete recurrence" (results were generic ODE extrapolation in time, not reasoning) |
| Hyperedges inside any looped or recurrent-depth model | Same searches; no hit |
| Persistent associative memory across inputs combined with depth recurrence | "looped transformer knowledge storage memorization bits per parameter…" returned only in-model learned memory banks or tokens (R2-111, R2-113) |
| Halting signals defined per graph region rather than per token or per sequence | Same halting searches; no hit |
| GPU kernels for per-node sparse top-k message passing inside a recurrent loop | Searched MoE dispatch / grouped GEMM only; no recurrent-graph kernel found |

## (e) Reproduce first

1. **T1 arm.**
   - Base: a looped transformer with input injection, from `Leiay/looped_transformer` (MIT; R2-195) and the Saunshi k×L protocol (R2-069).
   - Add Parcae-style spectral constraint on the injection (R2-092).
   - Add a terminal fixed-point objective (R2-107).
   - Rationale: this is the comparator that must be beaten.
2. **DT-Recall** (`aks2203/deep-thinking`, MIT; R2-193) on prefix sums and mazes. Its tasks overlap the preregistered families and have a known extrapolation ladder (R2-157).
3. **TRM** (`SamsungSAILMontreal/TinyRecursiveModels`, MIT, archived; R2-189) on Sudoku and mazes.
   - Run with and without augmentation, because of R2-105.
   - Include its 1-step-gradient ablation (R2-036).
4. **Halting baselines:** the KL convergence exit (R2-013, R2-109) and confidence readouts (R2-152). Learned gates go in only if they beat these.
5. **Routing cost baseline:** a MegaBlocks or Triton grouped-GEMM top-k dispatch (R2-170, R2-173). The aim is to measure the wall-clock cost of top-k edges before claiming V5.

## (f) Unconfirmed leads (not in the CSV)

- "Frey et al. 2026b", cited by Loopie (R2-206) for matched-FLOP capacity loss. Not located.
- "Recurrent Looped Transformer" and "Towards Looped Models Done Right: Part I". Seen only as alphaxiv listings (the parity 40→256-bit claim comes from a search snippet). No arXiv ID confirmed.
- Kohli et al. 2026 (looped transformer overthinking and implicit composition, cited in R2-099's source) and Jerad et al. 2026 (looping recognises context-free languages, cited in 2605.30523). Not fetched.
- Seen as URLs but not read:
  - 2604.11791 (mechanistic analysis of looped reasoning LMs)
  - 2604.01577 (fast–slow latent recurrence)
  - 2607.08775 (HALO)
  - 2606.18023 (LoopCoder-v2)
  - 2606.18208 (Looped World Models)
  - 2609.40305 (Looped Diffusion Transformer)
  - 2608.15062 (Gated Recurrent Transformers; downloaded, not ledgered)
- "SMELT 0.1B–54B" range from a search snippet. The paper text confirms "up to 54B" (R2-202); the 0.1B lower bound was not verified.
- Venue claims seen only in repo titles or headers: MoR at NeurIPS 2025 and Huginn at NeurIPS 2025. The matrix records both as arXiv.
- TRM's ARC numbers on the semi-private set. Only HRM's (R2-045) were independently verified.

## (g) Failed sources

- `gh api repos/ByteDance-Seed/Ouro`: 404. This was a guessed name; the paper only cites the project page ouro-llm.github.io (R2-203).
- `gh api repos/ytfan/looped_transformer`: 404 (guessed). The correct repo `UW-Madison-Lee-Lab/looped-tf` was found in the paper.
- TRM v1 PDF: the GitHub link is truncated in the extracted text, so the repo attribution is Medium confidence (R2-189).
- MegaBlocks arXiv text: the repo is not cited, so the `databricks/megablocks` attribution is Medium confidence (R2-192).
- 2202.08906 (ST-MoE): pdftotext's reading order puts the appendix first. Quotes were still found and verified; locators are by section name.
