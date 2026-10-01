# R3 — Dynamical systems, associative memory, local learning, NCA, oscillators, distributed readouts

Researcher R3 · retrieved 2026-10-01 · ledger `R3-dynamical-memory.csv` (164 rows: 163 citable + 1 ACCESS-FAILED) · matrix `R3-matrix.csv` (26 approaches, A3-01…A3-26). Sources cached in `evidence/sources/R3/`.

## (a) Verdict first

1. **Storage per parameter is fixed, whatever the architecture.** Language models store about 2 bits of knowledge per parameter. At 1000 exposures that ratio holds across architectures, even ones without MLP layers (R3-016, R3-017). For fading-memory systems, a dynamical system's total information-processing capacity is bounded by its number of independent state variables (R3-071, R3-072). Hopfield "exponential capacity" is counted per dimension or per neuron. The memories are still paid for, either as stored pattern rows or as hidden neurons (R3-001, R3-009, R3-162). Recurrence and topology can move capacity around. They cannot raise the storage ceiling. Associative memory layers help on *facts* (R3-022, R3-023), not on iterative computation.
2. **Associative recall sets a hard limit on persistent fixed-size state.** Recall needs state that grows with what must be recalled. Any recurrent model faces a lower bound (R3-036), and BaseConv's dimension must grow with sequence length (R3-033). Chain-of-thought (extra recurrent steps) does not close the gap. One attention layer does (R3-040, R3-041). A persistent node graph with a fixed total state inherits these limits unless it has a growing retrieval store (C9). Attention already provides one.
3. **Extra iterations help when training makes them help.** Weight-shared recurrence with input recall and progressive or deep supervision extrapolates far past the training horizon: 9×9→201×201 mazes and 32→512-bit prefix sums (R3-120, R3-121). AKOrN gains more from test-time steps than iterated self-attention (17→52% vs 14→34% OOD Sudoku, R3-105). The ARC Prize ablation of HRM is the opposite case:
   - HRM's bespoke recurrent architecture was within about 5pp of a parameter-matched transformer (R3-125, R3-126).
   - Training with refinement mattered more than inference refinement (R3-128).
   - Learned halting matched a fixed 16 loops within a few points (R3-129).
4. **Local and forward-only learning would be a handicap.** Predictive coding gets *worse* with depth while backprop gets better (R3-054). Iterating to convergence costs about 100× backprop (R3-066). Canonical PC suffers exponential signal decay on digital hardware (R3-058). The fixes (ePC, muPC) work by converging back to backprop's gradients (R3-059, R3-065).
5. **Fixed random topology (reservoirs) loses to trained models on quality.** At equal trainable parameters, transformers beat reservoirs on prediction quality (R3-081). Reservoirs only work near the edge of chaos (R3-074, R3-083). Under partial observation they diverge more often than BPTT-trained RNNs (R3-078).
6. **Closest prior art, overall:** the Continuous Thought Machine (A3-21) and AKOrN (A3-22) for internal ticks plus convergence and synchrony signals, the Energy Transformer (A3-03) for an iterated shared block with associative memory and an energy guarantee, and graph NCA (A3-17) for a shared M/U on a sparse persistent graph. None combines learned state-conditioned top-k edges (C6/C8) with persistent memory and distributed readouts.

## (b) C1–C13 coverage of the closest prior art (Y / P / N, claim_ids)

| Component | CTM (A3-21) | AKOrN (A3-22) | Energy Transformer (A3-03) | Graph NCA (A3-17) | Deep Thinking + recall (A3-24) |
|---|---|---|---|---|---|
| C1 persistent node states | Y R3-098, R3-161 | Y R3-103 | Y R3-011 | Y R3-089 | Y R3-160 |
| C2 sparse directed graph | N (dense synapse model) R3-098 | P (FC/conv/attention choice) R3-103 | N (dense attention) R3-011 | Y (arbitrary graph) R3-089 | P (local conv) R3-120 |
| C3 shared message fn M | P (shared synapse model; attention to input) R3-161 | P R3-103 | Y (one block) R3-011 | Y R3-089 | Y R3-160 |
| C4 shared update fn U | N (per-neuron private weights) R3-098 | unknown (not verified) | Y R3-011, R3-015 | Y R3-089 | Y R3-160 |
| C5 recurrent evolution over T | Y R3-099 | Y R3-159 | Y R3-011 | Y R3-089 | Y R3-121 |
| C6 learned top-k routing / edge creation | N | N | N | N | N |
| C7 hyperedges | N | N | N | N | N |
| C8 state-conditioned topology | P (synchrony-conditioned attention queries) R3-161 | P (if attentive connectivity) R3-103 | P (attention weights) R3-011 | N | N |
| C9 persistent associative memory | N | N | Y (Hopfield memories) R3-011, R3-015 | N | P (input recall only) R3-160 |
| C10 distributed readouts | Y (synchrony across many neuron pairs, per-tick) R3-099, R3-161 | N | N | N | N |
| C11 confidence / convergence signal | Y (certainty) R3-099 | Y (energy) R3-106 | Y (energy, guaranteed fixed point) R3-012 | N | N |
| C12 learned adaptive halting | P (certainty-based stop, not a learned halt unit) R3-111 | N | P (stop at fixed point) R3-011 | N | N |
| C13 topology and roles evolve during computation | N | N | N | N | N |

C6, C7 and C13 are covered by no R3-family system. R1 (DYN) and R2 (ROUTE) own the closest evidence for those.

## (c) Evidence against the hypothesis (first-class)

- **The gain is recurrence plus supervision, not the substrate.** In the ARC Prize HRM ablation, a ~27M transformer (parameter-matched) came within about 5pp, and the hierarchical architecture had minimal impact (R3-125, R3-126). Training with refinement improves even single-loop inference by more than 15pp, while extra inference loops matter less (R3-128). Learned ACT is roughly equal to a fixed 16 loops (R3-129). About 9 points of the headline drop away on the hidden set (41% claimed vs 32% verified, R3-130), and much of the score is memorisation of the evaluation tasks (R3-131).
- **Storage per parameter cannot be raised:** R3-016–R3-019 (2 bits/param across architectures), R3-071–R3-072 (capacity ≤ number of state variables), R3-009/R3-010 (dense-memory capacity is paid for in hidden units).
- **Fixed-state recall bounds:** R3-033, R3-036, R3-039, R3-040, R3-045 (more than d_dot associations means retrieval error).
- **Recurrent models are optimisation-brittle on recall:** success only inside a narrow learning-rate window, while Transformers are robust (R3-042).
- **Iterating beyond the horizon fails without specific fixes:** overthinking (R3-118, R3-112), NCA patterns explode or decay (R3-085), iterated self-attention *loses* ID accuracy with more steps (R3-105).
- **Iterative energy inference is unstable and costly:** EBT step hyperparameters cause unstable training, and both training and inference cost more (R3-030). CTM training time is extended and parameters grow (R3-101).
- **Local learning is a handicap on GPUs:** R3-054, R3-057, R3-058, R3-066, R3-068. EP sat 0.6% behind BPTT on CIFAR-10, and only after fixing its gradient bias (R3-060, R3-061).
- **Hardware:** sparse message passing wastes GPU work. Redundant operator computation is 92.4% of GNN operators (R3-155). Naive delta-rule recurrence is not sequence-parallel (R3-048).
- **Attention already is associative-memory retrieval** (R3-002). Data-dependent mixing is what solves MQAR (R3-034). This supports the "Transformer is already a dynamic graph" objection.
- **Distributed readouts can hurt:** naive intermediate classifiers degrade the backbone (R3-115).

Evidence *for* parts of the hypothesis: R3-120/121/153 (time replaces depth on local algorithmic tasks), R3-105 (oscillator dynamics extrapolate better than looped self-attention at matched step increase), R3-087/R3-123 (sample-pool and deep-supervision tricks stabilise long rollouts), R3-012/R3-107/R3-109/R3-110 (energy and oscillatory parameterisations that guarantee stability or mitigate oversmoothing).

## (d) Unexplored ("not found in our search")

- A recurrent graph with **learned state-conditioned top-k edges plus persistent associative memory**, compared with a **parameter- and FLOP-matched looped Transformer** on algorithmic extrapolation. Not found in our search. Query 2026-10-01: "arxiv 2026 recurrent graph neural network learned top-k edges persistent node states associative memory halting reasoning extrapolation vs looped transformer". The results contained no matching paper.
- **Predictive coding or equilibrium propagation training of transformer-scale language models.** Not found in our search. Query 2026-10-01: "predictive coding transformer language model 2025 2026 arxiv scaling local learning". The results were unrelated (CPC world models, scaling-law papers).
- MQAR measured on **persistent-state graph substrates** at matched total state size (only SSM, convolution and attention families appear in R3-031–R3-044). Not found in our search (same 2026-10-01 queries).
- Readout from synchrony (CTM) or energy (AKOrN) used as a **halting signal** compared with learned ACT at matched compute. Not found in our search.
- NCA vs a looped Transformer at matched parameters and FLOPs on ARC or mazes. The ARC-NCA comparisons are against LLMs and unmatched (R3-092).

## (e) Reproduce first

1. **Deep-thinking nets** (`aks2203/deep-thinking`, MIT, R3-145): the cleanest time-replaces-depth baseline, and the recipe (recall + progressive loss) for T1/G1.
2. **Zoology MQAR** (`HazyResearch/zoology`, Apache-2.0, PyTorch, R3-134): the associative-recall family, plus state-size sweeps.
3. **AKOrN Sudoku** (`autonomousvision/akorn`, no SPDX license detected, R3-142): the only R3 result directly against iterated self-attention (R3-105). Check licence before reuse.
4. **CTM mazes** (`SakanaAI/continuous-thought-machines`, Apache-2.0, R3-140): rerun against a matched looped transformer.
5. **ARC Prize HRM ablation protocol** (R3-125–R3-129): reuse its design (swap the substrate, hold the pipeline constant) for V1.
6. **Growing NCA sample pool** (`google-research/self-organising-systems`, Apache-2.0): stabilisation trick for G1–G3.

## (f) Unconfirmed leads (not in CSV)

- Song et al. 2024, *Inferring neural activity before plasticity* (prospective configuration): not checked.
- NoProp (arXiv 2503.24322): not checked.
- Echo State Transformer (arXiv 2507.02917): downloaded, not read.
- Reservoir Attention Network (arXiv 2606.15678): seen in search, not read.
- Rotating Features (2306.00600) / Complex AutoEncoder (2204.02075), synchrony-based binding: not checked.
- Differentiable Logic Cellular Automata (Google, 2025): not located at a primary URL.
- Bertschinger & Natschläger 2004, *Neural Computation* journal version: paywalled. We used the NeurIPS 2004 companion paper instead (R3-074).
- Lead ID 2405.06135 was wrong (it is an unrelated statistics paper). Memory Mosaics is 2405.06394 (R3-158).

## (g) Failed sources

- Jaeger 2002 STM echo-state tech report: the PDF text is unextractable (font encoding). Recorded as R3-164 ACCESS-FAILED.
- The muPC (2505.13124) Limitations section came out garbled in pdftotext. Only the abstract was used.
- Not a failed source but a caveat: CODE rows quote the GitHub REST API JSON (license/language/pushed_at), saved in `sources/R3/gh_*.txt`. Framework is stated only where a README line was quoted.
