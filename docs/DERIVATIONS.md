# Derivations

Each entry: statement · derivation · assumptions · where implemented · pinning test.

## D1. Task-solver correctness (ground truth for every generator)
- **Statement.** Each generator in `ngs/tasks/` returns the exact answer computed by a classical algorithm: BFS for reachability, Dijkstra for non-negative-weighted shortest path, a dict lookup for associative recall, Python `sorted` for sorting, two BFS distance maps for mazes (a square is labelled iff d(start,v) + d(v,goal) = d(start,goal), i.e. the union of all shortest paths; with percolation 0 the maze is a spanning tree and this is the unique path), direct simulation for automata.
- **Assumptions.** Integer weights ≥ 1, so shortest paths are well defined; seeded `numpy.random.Generator` makes every instance reproducible from (task, n, seed).
- **Where.** `ngs/tasks/*.py`.
- **Pinning tests.** `tests/test_tasks.py`: each solver is cross-checked against an independent brute-force method on small instances (Floyd–Warshall for shortest path, transitive closure for reachability, bubble sort for sorting, a step-by-step re-simulation for automata, Floyd–Warshall over free squares for percolated mazes). `test_percolation_creates_cycles` pins that percolation > 0 adds free squares beyond the 2n²−1 of a perfect maze; both maze guards were mutation-checked red (2026-10-01).

## D2. Per-step FLOPs and the executed-vs-useful convention (review R1, B4)
- **Statement.** For N nodes, width d, MLP width d_ff, one block step costs matmul FLOPs = 8Nd² + 4N·d_ff·d + 2·P_s·d + 2·P_m·d, where P_s = scored pairs and P_m = mixed (aggregated) pairs. Dense (T0/T1): P_s = P_m = N². Masked (G0/G1): executed P_s = P_m = N² (dense masked kernel), useful P_s = P_m = E. Top-k (G2/G3): P_s = N² (selection needs every score), P_m = N·k, implemented as dense scores → top-k → gather-aggregate reusing the scores. Non-matmul FLOPs: 5·P_m for softmax plus N²·⌈log₂k⌉ for selection (approximate). 1 multiply-add = 2 FLOPs.
- **Derivation.** QKᵀ is an N×d by d×N product: 2N²d. AV over P_m pairs: 2P_m·d. Q, K, V, O projections: 4 × 2Nd². MLP: 2 × 2N·d·d_ff.
- **Consequences.** G2 executes exactly T1's FLOPs at k = N and saves 2N(N−k)d matmul FLOPs below it, while paying selection. With d = 128 and k = 8, G2/T1 matmul = 0.995 at N = 16, 0.966 at N = 64, 0.879 at N = 256, 0.717 at N = 1024 (output of `ngs.flops`). The v0.1 pipeline (top-k, then masked SDPA recomputing QKᵀ and a full AV) executes T1 + 2N²d and was wrong.
- **Assumptions.** Embedding, injection and readout FLOPs are excluded from the per-step count and reported separately. The selection term is an approximation; measured top-k cost on GPUs is reported separately (R5-081).
- **Where.** `ngs/flops.py`.
- **Pinning test.** `tests/test_flops.py` (k = N equals dense; aggregation saving equals 2N(N−k)d; selection counted; executed vs useful for the mask arm; the v0.1 pipeline exceeds dense). Mutation-checked 2026-10-01: aggregation reverted to N², free selection, and useful = executed each turn the suite red.

## D3. Task-derived iteration budget T(n) (review R2, B3 and M2)
- **Statement.** T(n) = max(4, ⌈1.5 × q₀.₉₉(D)⌉), where D is computed by the exact solver on 1000 instances of size n (seed 0) and equals the number of synchronous one-hop steps a local exact algorithm needs:
  - BFS depth from the source (reachability);
  - the maximum over nodes of the fewest hops on any shortest path, i.e. synchronous Bellman–Ford rounds (shortest path);
  - the cell-graph distance start → goal (maze);
  - sequence length, the steps of a local-window algorithm such as odd–even transposition sort or a left-to-right scan (sorting, S5, and 2·pairs + queries for recall).
- **Why.** A diameter-bound arm (G1) needs ~D steps (R4-179, R4-061), while global arms need fewer. Giving every arm the same T(n) ≥ D lets the most local arm finish, and makes global arms prove they stay stable (V4). The budget depends only on the task, never on a model, so no arm's pilot sets it. Reading out at the last step removes the oracle choice of step on test labels.
- **Values.** Generated, never typed: `docs/generated/budgets.md` (`scripts/build_budgets.py`; maze rungs above side 17 use 300 instances). Review R3 found the earlier hand-typed values (100 instances, unpinned seed) disagreed with the code; at n = 1024 reachability T(n) varied 56–61 across seeds.
- **Where.** `ngs/budget.py`.
- **Pinning tests.** `tests/test_budget.py`:
  - BFS depth on a path;
  - Bellman–Ford fewest-hop tie;
  - maze steps = path cells − 1;
  - coverage ≥ 97% of fresh instances;
  - growth with n;
  - defaults tied to `ngs/params.py`.
  
  Mutation-checked 2026-10-01: budget factor 0.5 and the hop count frozen each turn the suite red.
