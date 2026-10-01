# R4: Neural algorithmic reasoning, learned connectivity, benchmarks

Researcher R4 · retrieved 2026-10-01 · ledger `R4-reasoning-connectivity.csv` (R4-001 to R4-185) · matrix `R4-matrix.csv` (A4-01 to A4-24) · sources in `evidence/sources/R4/`.

## (a) Verdict first

1. **Time can replace depth, but recurrence explains the gains, not the graph.** Weight-tied recurrent nets extrapolate far past training size when they run more iterations: prefix sums 32 to 512 bits at 97.12%, mazes 9x9 to 59x59 at 97.30% (R4-024, R4-025), and Sudoku run at 2x the training steps (R4-118). Looped Transformers do the same: parity 20 to 40+ digits, and k layers looped L times come close to kL unique layers (R4-140, R4-080). The single param-matched test of a "brain-inspired" structure against a plain Transformer inside the same recurrent pipeline found a gap of about 5pp. The refinement loop supplied the gain (R4-165, R4-166).
2. **The Transformer-is-already-a-graph objection holds up.** Attention is message passing on a complete graph (R4-070). It needs only O(log n) depth for connectivity, whereas sparse message passing needs O(diameter) (R4-061, R4-066, R4-179). A looped Transformer with graph-attention heads simulates Dijkstra, BFS, DFS and SCC with a parameter count that does not depend on graph size (R4-173). Dense attention also wins the hardware lottery (R4-071, R4-109).
3. **The opposite also holds: plain dense attention extrapolates badly on algorithmic graph tasks.** On reachability at 100 nodes it scores 91.51%, against 99.80% for max-aggregation message passing (R4-002). A plain Transformer scores 42.34% against 81.30% for the edge-state Relational Transformer on CLRS (R4-176). Transformers learn degree heuristics or path-merging shortcuts unless the training distribution is controlled (R4-063, R4-067). The open question is therefore graph substrate vs **looped** Transformer at matched parameters and FLOPs. **We found no paper that runs that comparison** (section e).
4. **Learned topology is mostly static or supervised.** DNW, RigL, SET and CHT learn the wiring once, during training. PGN and NEE create edges at every step, but only with pointer supervision. RIMs and NPS select modules at every step with top-k, without learned edges (R4-086, R4-089, R4-017, R4-095, R4-098). Random wiring is competitive with learned wiring (R4-093).
5. **Recurrence does not add storage.** Knowledge capacity is about 2 bits per parameter for looped and non-looped models alike (R4-082, R4-184). On language-model loss, one recurrence is worth only r^0.46 unique blocks (R4-185). The paper's verdict should rest on computational capacity, not storage (matches the prereg).

## (b) C1–C13 coverage by the closest prior art

Y = present, P = partial, N = absent. The column "Best prior art" names the closest system.

| C | Component | Best prior art | Score | Claims | Gap |
|---|---|---|---|---|---|
| C1 | persistent node states | RRN, RIMs, Triplet-GMPNN | Y | R4-117, R4-095, R4-013 | ForgetNet argues history contradicts Markov algorithm steps (R4-060) |
| C2 | sparse directed graph | PGN pointers, SALSA sparse GNNs | P | R4-016, R4-040 | Sparse when the graph is given; learned sparse directed graphs only via supervised pointers |
| C3 | shared message fn M | RRN, CLRS processors | Y | R4-117, R4-013 | Learnability limits for standard MPNN messages (R4-053, R4-056) |
| C4 | shared update fn U | RRN, DT nets | Y | R4-117, R4-022 | Update spectrum matters for state tracking (R4-078) |
| C5 | recurrent evolution, T steps | DT-Recall, RRN, recurrent GNN theory | Y | R4-024, R4-118, R4-181 | Overthinking without recall (R4-026) |
| C6 | learned top-k routing / edge creation | PGN (supervised), RIMs top-k modules, NPS, NEE | P | R4-016, R4-017, R4-095, R4-098, R4-021 | No unsupervised per-step top-k edge creation evaluated on size extrapolation (section e) |
| C7 | hyperedges | Shared workspace hub; looped-Transformer hypergraph theory; HyperGNN theory | P | R4-100, R4-182, R4-183 | No learned hyperedges in trained NAR models (section e) |
| C8 | state-conditioned topology | PGN, NEE, RIMs, RSGN | P | R4-016, R4-021, R4-094, R4-107 | RSGN evidence is Low confidence and loses to a Transformer (R4-108) |
| C9 | persistent associative memory | Stack-augmented GNN; stack/tape RNNs | P | R4-054, R4-076 | R3 covers Hopfield-style memory |
| C10 | distributed readouts | RRN readout at every node and every step | Y | R4-117 | — |
| C11 | confidence / convergence signal | DT fixed-point analysis, EqR attractors | P | R4-034, R4-141, R4-133, R4-178 | A fixed point does not imply correctness, and limit cycles can still be correct (R4-034) |
| C12 | learned adaptive halting | NEGA termination network; looped TF adaptive steps | P | R4-004, R4-140, R4-028 | Needs ground-truth step counts (R4-140). A run-time penalty destroyed extrapolation (R4-028) |
| C13 | topology and node roles evolve during computation | NEE self-modifying mask, PGN | P | R4-021, R4-016 | DNW's "dynamic graph" is a training-time structure (R4-086, R4-088) |

**No single system scores Y on C6, C8 and C13 together without supervision.** That combination is the candidate's distinctive bet.

## (c) Benchmark map for the program

"Matched?" means matched on parameters or FLOPs, as stated by the source.

| Task | Generator / repo (license) | Sizes in literature | GNN / recurrent best | Transformer best | Looped Transformer best | Matched? |
|---|---|---|---|---|---|---|
| Reachability / connectivity | CLRS BFS (google-deepmind/clrs, Apache-2.0, JAX) R4-142; SALSA-CLRS (Apache-2.0, PyG) R4-143; asaparov/learning_to_search (no license) R4-162 | 20→100 (R4-001); 16→1600 (R4-041); ≤41 vertices (R4-064) | MPNN-max 99.80% last-step at 100 (R4-001); RecGNN BFS 99.2% node accuracy at 1600 on ER, 55.6% on Delaunay (R4-041) | GAT-full 91.51% at 100 (R4-002); difficulty grows with size even with more parameters (R4-063) | Constructions only (R4-173, R4-066) | No |
| Shortest path | CLRS Bellman-Ford/Dijkstra; SALSA Dijkstra R4-040; Maze-Hard (R4-129) | 16→64; 16→1600; Maze-Hard 30x30 fixed | Provable extrapolation with sparsity regulariser (R4-052); TRM 85.3% Maze-Hard (R4-130) | Plain Transformer weak on CLRS (R4-176) | Dijkstra construction (R4-174) | No |
| Associative recall (MQAR) | HazyResearch/zoology (Apache-2.0) R4-148 | Sequence length and key-value count varied | not found in our search | Attention solves with dimension independent of length (R4-116); 70M attention beats 1.4B gated-conv (R4-114) | not found | No (by design) |
| Sorting | CLRS sorting; NEE | 16→64; length 8→100 | No-hint GNN 98.7% F1 (R4-045); MPNN 11.83% (R4-009) | NEE 8→100 near-perfect with mask supervision (R4-020); plain seq2seq degrades (R4-019) | R2 covers | No |
| Mazes (extrapolation) | easy-to-hard-data (MIT) R4-145; maze-dataset (LGPL-3.0) R4-147 | 9x9→59x59 and 201x201 | DT-Recall 97.30% at 59x59 (R4-025); CTM 39→99 by re-application (R4-112) | not found | not found | Depth-matched only |
| Prefix sums / parity | easy-to-hard-data; looped-TF tasks | 32→512 bits; 20→40+ | DT-Recall 97.12% at 512 (R4-024) | Next-token-prediction fails at max length +10 (R4-140) | Parity 20→40+ near-perfect (R4-140) | No |
| State tracking (S5, automata) | Chomsky suite (Apache-2.0) R4-144 | Train lengths 1–40, test 41–500 (R4-075) | LSTM solves regular tasks; stack/tape needed beyond (R4-076) | TC0 bound (R4-072, R4-077); shortcuts brittle (R4-074) | Escapes the bound in theory (R4-080); numbers not extracted | No |
| Program / algorithm execution (text) | CLRS-Text (in the clrs repo) R4-038 | Per-algorithm sizes for Gemma 2B | TransNAR +20pp OOD on several classes (R4-044) | Gemma 2B baseline (R4-038) | not found | No |
| Compositional reasoning | SCAN (BSD) R4-154; COGS (MIT) R4-155; CLUTRR (CC BY-NC) R4-156 | SCAN length ≤22 actions; COGS gen set | GAT on symbolic CLUTRR beats text models (R4-124) | COGS gen 16–35% (R4-123); SCAN length 20.8% for an RNN (R4-122) | Recurrent-depth TF extrapolates 5→10 hops (R4-084) | No |
| Sudoku | RRN (no license, reimplement) R4-150; Sudoku-Extreme via TRM/HRM repos R4-158 | 17–34 givens; 1K train / 423K test | RRN 96.6% at 64 steps (R4-118); TRM-MLP 87.4% (R4-131) | not found | TRM 74.7% (attention) (R4-130) | No (7M vs 27M) |
| ARC | ARC-AGI-1/2 (Apache-2.0) R4-157 | 400/400 public, 100 hidden (R4-121) | — | HRM-size Transformer within ~5pp of HRM (R4-165) | TRM 44.6% / 7.8% (R4-132); HRM verified 32% / 2% (R4-169) | Param-matched only in R4-165 |

**Benchmark pitfalls to design against:**
- Maze sets with no cycles admit a deadend-filling shortcut (R4-032, R4-035).
- Reachability sets admit a degree heuristic beyond model capacity (R4-067), and naive graph distributions defeat search learning (R4-064).
- Automata admit brittle shortcuts (R4-074). SimpleLogic-style generators leak statistical features (R4-125).
- ARC and HRM pipelines use transductive puzzle-ID training and test-time voting (R4-168, R4-170).
- SATNet's visual Sudoku result leaked labels; it scores 0% without them (R4-172).
- Pretrained LMs have seen CLRS implementations (R4-039).
- The COGS generalisation set was corrected after release (R4-155).
- COGS seed variance is ±6–8%, so 3 seeds may be underpowered (R4-123).
- Node-level metrics hide graph-level failure (R4-043).

## (d) Evidence against the hypothesis

- **Looped Transformers already deliver time-as-depth.** k layers looped L times come close to kL layers (R4-080). Recurrent-depth Transformers extrapolate in hop depth (R4-084). Looped Transformers provably simulate graph and hypergraph algorithms with constant parameters (R4-173, R4-182).
- **Structure adds little once recurrence is present.** A Transformer comes within ~5pp of HRM at matched parameters; refinement loops account for the gain (R4-165, R4-166). The gain is mostly a training-time effect (R4-167). On ARC, most of TRM's accuracy arrives at the first recursion step (R4-171).
- **Iteration budget on connectivity.** Attention reaches diameter 3^L in L layers, while message passing needs T ≥ diameter: 63 vs 4 on a 64-node path (R4-179, DERIVED).
- **Extra iterations do not fix non-size shifts.** DT-Net outputs freeze under percolation (R4-033). Training diversity does not improve extrapolation (R4-034). Looped-Transformer mechanisms degrade at greater depths and errors compound (R4-085). Chess saturates at ~83% (R4-027).
- **Stability.** Overthinking appears without recall (R4-026). Limit cycles occur (R4-034). HRM has no guarantee of reaching a fixed point (R4-133, R4-178). Implicit solvers are sensitive to Broyden settings (R4-036).
- **Message-passing limits.** depth × width must grow polynomially in n for many tasks (R4-069). Standard MPNNs provably cannot learn many algorithms (R4-053). Recurrent GNNs are capped at 1-WL without random features (R4-083). Local-structure shift yields "bad" minima (R4-057).
- **Learned topology is weak evidence.** Random wiring is competitive (R4-093). The 2026 brain-like sparse substrate (RSGN) loses to a Transformer on accuracy (R4-108). Dynamic sparse training is static at inference (R4-089).
- **GPU cost.** Dense attention wins the hardware lottery (R4-071, R4-109). Conditional compute trains 1.5–2x slower even when MAC-matched (R4-139). Topology learning itself can cost O(N·d^3) (R4-106). Triplet messages are cubic per step (R4-013).
- **Capacity is bounded by parameters for storage.** About 2 bits per parameter regardless of looping (R4-082, R4-184). Recurrence is worth r^0.46 unique blocks on LM loss (R4-185). Looped models memorise worse at iso-FLOP (R4-081).
- **Matching criticism.** A parameter-only match misleads for shared-weight models (R4-134), and rankings flip between parameters, FLOPs and throughput (R4-135). BPTT activation memory is not reduced by weight sharing (R4-136).

## (e) Unexplored: not found in our search (all searches run 2026-10-01)

| Gap | Query | Result |
|---|---|---|
| Recurrent graph with learned top-k edge creation each iteration vs a looped Transformer at matched parameters and FLOPs, on size extrapolation | `recurrent graph neural network learned top-k edge creation per iteration size extrapolation compared looped transformer matched parameters FLOPs` | not found in our search |
| Learned hyperedges in a trained neural algorithmic reasoner with OOD-size results | `hypergraph neural algorithmic reasoning hyperedges CLRS size generalization` | not found in our search; only constructions and theory (R4-182, R4-183) |
| Unsupervised (no-hint) pointer or edge creation combined with adaptive halting, evaluated on maze extrapolation | `unsupervised pointer graph network learned edges without hint supervision adaptive halting maze extrapolation` | not found in our search |
| Knowledge-storage probe for graph-substrate (non-Transformer) recurrent models | `knowledge capacity bits per parameter looped transformer weight-shared recurrent depth memorization scaling law` | Found for looped LMs only (R4-184); not found in our search for graph substrates |

A further gap within our corpus, not separately searched: no paper reported here sets an MQAR result for a recurrent GNN or a looped Transformer.

## (f) Reproduce first

1. **SALSA-CLRS** (PyTorch + PyG, Apache-2.0). Covers reachability and shortest path on a ladder of 5x to 100x (R4-143, R4-180). Add an exact-match graph-level metric.
2. **CLRS** (JAX). Supplies the Triplet-GMPNN reference number 74.14% (R4-011). Re-running it costs a JAX stack; we could cite the number instead.
3. **deep-thinking + easy-to-hard-data** (MIT). DT-Recall on prefix sums and mazes is the reference for V4 (R4-024, R4-025, R4-145, R4-146).
4. **maze-dataset** (LGPL-3.0). Supplies percolation and deadend-start variants that close the deadend-filling shortcut (R4-147, R4-035).
5. **zoology MQAR** (Apache-2.0), including `ar_extrapolate.py` (R4-148).
6. **Chomsky suite** (Apache-2.0) for state tracking and automata (R4-144). Add an S5 permutation-composition task (R4-079).
7. **asaparov/learning_to_search**: a reachability generator with balanced lookahead (R4-162). It has no license, so we would regenerate the data with our own code.
8. **RRN Sudoku**: reimplement (unlicensed). It is the closest C1/C3/C4/C5/C10 baseline (R4-117).

**Recommended matching practice:**
- Report the iso-parameter and iso-FLOP baselines together (R4-080, R4-138).
- Report throughput and peak memory as well (R4-134 to R4-136).

## (g) Unconfirmed leads (not in the CSV)

- **Adaptive recurrent vision / AdRNN** (NeurIPS 2023): seen only as pages.ucsd.edu/~desa/extrapolation_rnns_neurips_2023.pdf in search results. No arXiv ID confirmed (the arXiv API returned 503).
- **Ren & Liu (2026), "HRM is a structured guesser"; Miyanishi & Morimura (2026)**: cited inside 2609.22197 and not located.
- **Confirmed on arXiv but not read** (so no rows): 2211.00692 (OOD generalisation of NAR), 2409.06953 (multiple correct solutions), 2509.15239 (KNARsack), 2505.24067 (primal-dual NAR), 2606.18164 (state-tracking learning dynamics), 2511.08028 (graph-transformer insights), 2407.00379 (GraphArena), 2507.05362 (shortest-path CoT bias), 2302.04496 (dual algorithmic reasoning), 2306.15632 (asynchronous alignment), 2301.13196 (looped TF as computers; R2).
- **SATNet critique venue**: NeurIPS 2020 per a proceedings review page in search results, not opened.
- **Overlap with R2**: Ouro (R4-184), the iso-depth law (R4-185), looped length generalisation (R4-140) and TRM/HRM (A4-24) overlap with R2's scope. Recorded here because they decide the capacity-vs-storage split and the benchmark map; dedupe at merge.

## (h) Failed sources

- **arXiv export API:** the `http://` endpoint returned an empty body. Batch 4 returned HTTP 503. Both papers were confirmed instead from the arXiv PDF headers (2501.10688, 2303.05490).
- **2509.22343:** the first download returned HTML. Re-downloaded as v1 (PDF).
- **arcprize.org/blog/hrm-analysis:** the WebFetch summary paraphrased the page. All quotes were instead taken from the curl'd HTML (`sources/R4/arcprize_hrm_analysis.txt`).
- **maze-dataset README:** an HTML header made it unparseable. The quote comes from the GitHub API description.
- **Self-check:** the validator shows 0 REJECT for R4 (185 claims, 24 matrix rows). Every arXiv and blog quote was checked by normalised substring match against the downloaded text, and the 3 mismatches were fixed. A manual spot check of R4-061, R4-083 and R4-093 corrected one locator (R4-061).
