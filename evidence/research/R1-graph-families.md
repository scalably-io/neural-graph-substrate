# R1 — Graph families (MPNN · RGNN · DYN · GT · HYP · TOP · THEORY · GPU)

Retrieved 2026-10-01. Ledger: `R1-graph-families.csv` (178 rows, 1 ACCESS-FAILED). Matrix: `R1-matrix.csv` (27 approaches). Every quote was machine-checked as a substring of the source's extracted text (`evidence/sources/R1/<arxiv-id>.txt`, `gh_*.json`).

## (a) Verdict first

1. **No graph-family method we found combines the candidate's core loop**, meaning weight-tied recurrence + state-conditioned edge creation + learned halting, and none is compared against a **parameter- and FLOP-matched looped transformer**. The closest are N2 (shared recurrent layer + dynamic pathways, R1-067/068), Co-GNN (state-conditioned per-node topology, R1-059) and IterGNN (recurrent + learned termination, R1-022).
2. **Iterating longer than training can help on graphs, but only with explicit stabilisers.** IterGNN reaches 100% shortest path on 5000-node graphs after training on 4–33 nodes (R1-023). A recurrent GNN extrapolates 1,000× in size (R1-027). Without L2 state regularisation it collapses after ~100 rounds (R1-029). Recurrence is "necessary but not sufficient" (R1-028).
3. **The theory predicts that iteration cannot fix the topology:** depth/iterations do not mitigate over-squashing, which vanishing gradients dominate instead (R1-013). Topology, measured by commute time, dominates (R1-015). State-dependent, time-varying attention still oversmooths exponentially (R1-008/009). A recurrent substrate therefore needs the C6/C8 topology component to be real, and that component is exactly what remains unbenchmarked at matched compute.
4. **The objection holds up in the evidence.** Transformers are MPNNs on complete graphs that "win the hardware lottery" (R1-099). Log depth suffices for connectivity (R1-092). Transformers beat GNNs on connectivity and shortest path (R1-093). MPNNs, even with virtual nodes, fail a short-range bottleneck task that transformers solve (R1-096/097). A looped transformer simulates Dijkstra/BFS/DFS with size-independent parameters (R1-098).
5. **The reported graph-transformer advantages are fragile.** Tuned GCN beats GPS on Peptides (R1-088), and the LRGB gap vanishes on several datasets (R1-089). Classic GNNs match or beat GTs on 17 of 18 node datasets (R1-091). Every comparison needs our own tuning budget per arm.
6. **The GPU reality is against sparse graphs.** Sparse aggregation hits about 37% cache (R1-131), kernels are memory-bound, and FLOP reductions often do not become wall-clock gains (R1-135). V5 (≤2× T1 wall-clock) is at real risk.

## (b) C1–C13 coverage of the closest prior art

Y = yes, P = partial, N = no. Claim IDs in brackets.

| Component | N2 (2024) | Co-GNN (2023) | IterGNN (2020) | Recurrent GNN, Grötschla (2022) | DGCNN (2018) | MAVN (2026) |
|---|---|---|---|---|---|---|
| C1 persistent node states | Y [067] | P, per layer [059] | Y [022] | Y [027,030] | N | N |
| C2 sparse directed graph | P, pseudo-node pathways [067] | P, directionality via actions [060] | P, input graph | P, input graph | Y, kNN directed [054] | P [069] |
| C3 shared message fn | Y, one recurrent layer [067,068] | P, action net shared across layers [061] | Y [022] | Y [030] | N | N |
| C4 shared update fn | Y [067] | N | Y [022] | Y [030] | N | N |
| C5 recurrent evolution over T | Y [067] | N | Y [022,023] | Y [027,029] | N | N |
| C6 learned top-k routing / edge creation | P [067] | P, gating of existing edges only [059] | N | N | P, kNN top-k, not learned by a loss [054,055] | Y, learned node–VN connections [070] |
| C7 hyperedges | N | N | N | N | N | P, virtual hubs [069] |
| C8 state-conditioned topology | Y [067] | Y [059] | N | N | Y [054] | Y [069] |
| C9 persistent associative memory | N | N | N | N | N | N |
| C10 distributed readouts | N | N | N | N | N | N |
| C11 confidence / convergence signal | N | N | Y, confidence score [022] | N | N | N |
| C12 learned adaptive halting | N | N | P, global, not per node [022] | N | N | N |
| C13 topology and roles evolve during computation | P [067] | P, per-layer roles listen/broadcast [059] | N | N | P [054] | P [069] |

Other graph-first single-component matches:
- C9: gLSTM's associative memory inside node state [046].
- C5+C7 with learned hyperedges: the recurrent set-to-hypergraph refiner [164,165], which predicts structure and is not used as a compute substrate.
- C12: theory on per-vertex halting RGNNs [118,119].

## (c) Failure evidence against the hypothesis

- **The expressivity ceiling does not move with iterations.** MPNNs are capped at 1-WL whatever their depth [002,003]. Converging RGNNs express exactly graded modal µ-calculus, which is still bisimulation-invariant [118]. Stabilising set-aggregation RGNNs cannot compose opposite-polarity fixed points [120].
- **Capacity is bounded by state width.** Depth × width must exceed poly(n) [004,005]. Two-Radius needs width that grows with n [097]. Capacity over-squashing saturates node storage [047]. Time cannot substitute for per-node width.
- **Iteration does not cure the bottleneck.** Depth cannot fix over-squashing [013]. GNNs vanish gradients after a few layers [042]. Shared contractive layers converge to a unique fixed point, so iterations beyond convergence add nothing [044].
- **Dynamic routing does not stop collapse.** State-dependent, time-varying attention oversmooths exponentially [008,009]. Pure attention collapses to rank 1 [101]. Adding edges trades over-squashing for oversmoothing [016,126].
- **Instability past the training horizon.** Accuracy collapses after ~100 rounds without state regularisation [029]. Maze RNN/implicit extrapolators fail on several axes and show limit cycles [034]. More diverse data did not improve extrapolation [035]. Adding hypergraph message-passing rounds degrades HGNNs [166]. Co-GNN optimisation gets hard as layers grow [062].
- **Transformers win the global tasks.** See R1-092, 093, 094, 096 and 098. Transformers share over-squashing [102], so the pathology is not unique to graphs, but it gives graphs no advantage either.
- **Baselines catch up once tuned.** See R1-088, 089 and 091.
- **Hardware.** See R1-099 (dense wins), 129 (per-edge message tensors cost memory), 131, 133 and 135. TDL adds cost [116].
- **Positive theory relies on impractical assumptions.** Exact algorithm learnability needs bounded degree and infinite-width ensembles [124].

## (d) What is genuinely unexplored

Each item is "not found in our search". All searches were run on 2026-10-01.

1. A weight-tied recurrent GNN with **state-conditioned edge creation plus learned per-node halting**, evaluated beyond the training horizon. Query: `recurrent graph neural network learned state-conditioned edge creation adaptive halting persistent node state replace transformer parameter-matched looped transformer comparison`. It returned only halting/convergence theory (2604.25551) and Grötschla 2022.
2. A **parameter- and FLOP-matched comparison of a looped transformer against a recurrent GNN** on algorithmic size extrapolation. Query: `"looped transformer" vs "recurrent GNN" parameter-matched graph algorithm extrapolation comparison`. It returned looped-transformer simulation theory (2402.01107) and looped-LM pages, but no head-to-head.
3. A **recurrent computation substrate with learned hyperedges** used for computation rather than structure prediction. Query: `recurrent hypergraph neural network learned hyperedges iterative message passing until convergence`. It returned set-to-hypergraph prediction (2106.13919) and IHNN on fixed hypergraphs (2508.14101).
4. **Test-time iteration scaling** (more rounds at inference than in training) for GNNs in 2024–2026. Query: `graph neural network "test-time compute" more message passing iterations at inference 2025`. It returned 2601.23207, which iterates a learned local rule at inference but under NTK/ensemble assumptions; we found no compute-scaling study.
5. A **weight-tied, iterated Co-GNN or DGCNN-style kNN rewiring**. It is covered by query 1 and by `graph neural network learned dynamic topology nodes choose edges top-k state-dependent rewiring during message passing 2025`. That search returned per-layer rewiring (GraphTorque, TRIGON, GraphTOP), all fixed-depth.
6. **Distributed readouts (C10) and convergence-confidence signals (C11) in graph substrates.** Only IterGNN's global confidence appeared; we ran no dedicated query beyond queries 1 and 4, so treat this item as weakly searched. R3 covers distributed readouts.

## (e) What to reproduce first

1. **Grötschla et al. recurrent GNN** (`floriangroetschla/Recurrent-GNNs-for-algorithm-learning`, Apache-2.0) [141]. It is the cleanest G1 arm and tests V4 directly (12 training rounds → 120+ test rounds, regulariser on/off). It is small and has a permissive licence.
2. **Co-GNN** (`benfinkelshtein/CoGNN`, MIT) [143]. It is the basis for the G2 state-conditioned topology arm. Make it weight-tied and iterate it, which is the unexplored item d5.
3. **IterGNN termination module**. The paper is NeurIPS 2020 [022–024]; we did not locate an official repo (see f). It is the closest G3 halting design, and its 5000-node shortest-path result is the extrapolation bar to beat.
4. **Tönshoff LRGB tuning protocol** (`toenshoff/LRGB`, MIT) [146] and **tunedGNN** (MIT) [147]. They set the per-arm tuning budget so that we do not reproduce the "overstated gap" error.
5. **GraphGPS** (MIT) [140]. It is the standard local+global baseline, if a GT arm is added.
6. **N2** (`sunjss/N2`) [159]. It is the closest architecture, but GitHub detected no licence file; we can use it for reading and reproduction only, and should check the licence before reusing any code.
7. **A-DGN** [148], as the stabiliser option for long iteration. GitHub detected no licence file.

## (f) Unconfirmed leads (kept out of the CSV)

- The official IterGNN repository. The guessed path `vthost/IterGNN` returns 404, and the paper's extracted text cites only `weihua916/powerful-gnns`.
- The Co-GNN venue (ICML 2024 per search results). OpenReview was blocked (R1-178).
- These venues are taken from search snippets only: Exphormer (ICML 2023), Grötschla (AAAI workshop?), AMP, DRew (ICML 2023?) and HGNN (AAAI 2019).
- "Halting Recurrent GNNs and the Graded µ-Calculus" (KR 2025), which a search snippet mentions; the primary source was not read.
- 2025–2026 dynamic rewiring papers found but not read: GraphTorque (OpenReview `43YE7hqSQJ`), TRIGON (arXiv 2508.19071), GraphTOP, Cluster Attention (2604.07492), S³GNN (2605.23467) and Kormann et al., "Position: Don't be afraid of oversmoothing and over-squashing" (2601.07419, cited inside 2505.15547).
- Search-snippet claims that a looped transformer matches a 12-layer transformer with 1/12 of the parameters, and that a "Recurrent Looped Transformer" scores 60.8% parity at matched parameters. These are R2 territory and unverified.
- Faber & Wattenhofer, asynchronous neural networks for graphs (arXiv 2205.12245), and DHGNN (IJCAI 2019): not read.

## (g) Failed sources

- The OpenReview forum `T0FuEDnODP` (Co-GNN) returned a browser-verification wall to both curl and WebFetch (R1-178).
- Two arXiv IDs from memory were wrong. 2212.06737 is a quantum-states paper and 2206.12001 is a combinatorics paper. The correct ED-HNN ID is 2207.06680.
- GitHub API 404 for the guessed repos `vthost/IterGNN`, `microsoft/tc-gnn` (the official repo is `YukeWang96/TC-GNN_ATC23`) and `yixinliu233/ProteinRNN` (an irrelevant guess).
- Table extraction is unreliable for multi-column PDFs. R1-094 and R1-177 quote table cells whose column mapping we inferred, so they are marked Low/Medium confidence.
