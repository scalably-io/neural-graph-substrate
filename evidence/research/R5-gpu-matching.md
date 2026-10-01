# R5: GPU cost and compute matching (GPU · BENCH · ROUTE · THEORY · X)

Retrieved 2026-10-01. Ledger: `R5-gpu-matching.csv` (142 rows: 12 DERIVED, 0 ACCESS-FAILED). Matrix: `R5-matrix.csv` (19 approaches). A script checked every non-DERIVED quote as a whitespace-normalised substring of the saved source in `evidence/sources/R5/` (arXiv text, docs HTML→text, `gh_*.json`, and rendered Vast.ai snapshots). 0 misses. This dossier extends R1-131 and R1-135 and does not repeat them.

## (a) Verdict first

1. **At our graph sizes (N ≤ ~1k nodes), dense attention is the cheapest way to run a graph on a GPU, both in wall-clock and often in FLOPs.**
   - Gather/scatter aggregation is memory-bound. Measured: 2.35 DRAM bytes/op with a 6.87% L2 hit rate, against 0.01 bytes/op for the dense step (R5-086). Our estimate is about 0.08 FLOP/byte, roughly 1,900× below the A100 ridge (R5-128/129).
   - On small graphs, framework overhead dominates (R5-137).
   - A per-edge MLP costs more FLOPs than full attention below roughly 2k nodes at d=256, k=8 (R5-133, DERIVED).
2. **Learned top-k topology gets no kernel sparsity at our N.**
   - Block-sparse kernels skip only fully masked 128×128 tiles (R5-002/003).
   - N ≤ 128 is one tile. Random top-k at N=512 leaves about 1e-128 chance of an empty tile (R5-130/131).
   - Fast sparse attention (NSA, MoBA, Quest) wins only at 16k–1M tokens (R5-017/041/042).
   - Top-k selection itself took 11.6–26.9% of MaxK-GNN training time (R5-081).
3. **Halting saves FLOPs, not batched wall-clock.**
   - A batch waits for its slowest sample (R5-103).
   - Fewer FLOPs do not reduce time in the memory-bound regime (R5-105).
   - CALM's 3× was measured at batch size 1 (R5-101/102).
4. **Parameter sharing helps per stored parameter, not per training FLOP.**
   - A looped block is worth r^0.46 unique blocks. At r=4, 410M looped parameters match 580M non-looped in loss, but at the training cost of a 1B model (R5-091/092).
   - Truncated BPTT lowers this exponent further, to 0.38 (R5-093).
   - Counterpoint: a looped MoE matches a ~2× larger MoE at matched training compute (R5-096; preprint dated 2026-09-30).
5. **Standard FLOP tools under-count exactly what the graph arms do.**
   - torch FlopCounterMode, torch.profiler and fvcore count no scatter, gather or top-k (R5-049/053/126).
   - The tools disagree by a factor of 2 on how they count an FMA (R5-051/053).
   - Kaplan's 6N under-counts a T-loop by a factor of T (R5-132).
   - Matching therefore has to be analytic, with hand-written formulas, cross-checked by the counters.
6. **V5 (graph wall-clock ≤ 2× T1) is at high risk** unless G0–G3 are implemented as dense masked attention, which gives up any sparsity saving. Make that the default and treat a gather/scatter build as an ablation.

## Component coverage (C1–C13): is there an efficient GPU path?

Y = mature kernel exists, P = partial, N = none found.

| Component | Efficient path | Claims |
|---|---|---|
| C1 persistent node states, C5 T-step recurrence | P: activations grow with T; checkpointing costs +33% FLOPs; implicit/JFB gives O(1) memory but needs a fixed point | R5-030/033/034/097/134 |
| C2 sparse directed graph, C3/C4 shared M/U | P: gather/scatter is memory-bound; dense masked attention is fast but not sparse | R5-086/129/012 |
| C6/C8 learned top-k, state-conditioned edges | P: torch.topk/RTop-K/RadiK exist; fixed k keeps shapes static; thresholded edges cause recompiles | R5-081/082/059/061 |
| C7 hyperedges | N: no kernel evidence collected | none |
| C12 learned halting | P: unroll to T_max with masks; no batched wall-clock gain without re-batching | R5-103/104/141/057 |
| C9, C10, C11, C13 | not assessed (cost-neutral relative to the above) | none |

## (b) Recommended stack per arm (PyTorch 2.x + Triton; single GPU)

Rule for every arm: use fixed shapes. Pad every instance to N_max. Use fixed k per node, so E = N·k. Unroll to a fixed T_max. This keeps torch.compile and CUDA graphs usable (R5-057–061) and gives the same shape every step.

| Arm | Implementation | Expected bottleneck |
|---|---|---|
| T0 fixed-depth Transformer | `F.scaled_dot_product_attention` (FlashAttention backend) in bf16, torch.compile | At small N: kernel-launch and framework overhead (R5-137). FLOPs dominated by MLPs. |
| T1 looped Transformer | Same block × T with input re-injection. Full BPTT, with `torch.utils.checkpoint` per iteration if memory requires it. CUDA graphs over the fixed-T unroll. | Activation memory O(T) (R5-023). Checkpointing adds +33% FLOPs (R5-134). Launch overhead × T. |
| G0 GNN, fixed depth | **Primary:** dense masked attention/aggregation over the task adjacency (SDPA with a boolean mask, or FlexAttention mask_mod). **Ablation:** PyG MessagePassing with torch_scatter. | Dense: N² work, but tensor-core speed. Scatter: memory-bound (R5-086), nondeterministic atomics (R5-062). |
| G1 recurrent GNN, fixed topology | G0 weight-tied over T. Static mask/edge_index, so CUDA graphs work. | Same as T1 plus G0. |
| G2 learned top-k topology | Per iteration: scores S = q·kᵀ (N×N, dense matmul), `torch.topk(S, k)`, boolean mask, then masked softmax messaging via SDPA/FlexAttention. Gradient flows through the selected scores. Rebuild the mask each iteration; do not rebuild a BlockMask unless N > 128 and it has been measured. | N² scoring every iteration plus top-k (non-matmul, up to 16× costlier per FLOP; R5-011). Top-k ≈ 12–27% of time in an analogous GNN (R5-081). No sparsity savings (R5-131). |
| G3 = G2 + halting | Unroll to T_max with per-node/per-instance halting masks (ACT/PonderNet-style). Avoid `.item()` and while-loops (R5-057, R5-141). Report executed iterations. | Batched wall-clock equals T_max (R5-103). Savings appear only in FLOPs and in batch-size-1 latency. |

If a sparse gather/scatter G2 is wanted: build `edge_index` from top-k (fixed E = N·k) and aggregate with torch_scatter or `index_add_`. Expect it to lose to the dense path below ~2k nodes (R5-133, DERIVED). It is worth running only as a V5 sensitivity check.

**Hardware.**
- An RTX 4090 or 5090 is enough for every arm at these sizes. The 2026-10-01 Vast.ai medians are $0.45/hr (RTX 4090) and $0.60/hr (RTX 5090), against $2.27/hr for H100 SXM (R5-071/072/075).
- Prices are marketplace offers that update hourly (R5-077), so budget on the median (R5-135).
- Run every arm of a comparison on the same SKU, in the same session. GraphGPS saw run-time drift across mixed GPUs (R5-108).

## (c) Measurement protocol, with tools and blind spots

| Quantity | How | Blind spot / mitigation |
|---|---|---|
| Stored params | `sum(p.numel())` over unique tensors, embeddings and readouts included (Chinchilla convention, R5-090). Also report parameter uses per forward pass. | Kaplan excludes embeddings (R5-088): state the convention. Sharing cuts params, not FLOPs or activations (R5-022/023). |
| Inference FLOPs / instance | **Analytic formulas per arm** (MAC = 2 FLOPs), reported as matmul FLOPs and non-matmul FLOPs (scatter adds, softmax, top-k scoring/selection) separately. Cross-check with `torch.utils.flop_counter.FlopCounterMode`. | The counter gives 0 for unregistered ops (scatter, gather, topk; R5-049). It does not see masking or early exits (R5-050). fvcore uses 1 FMA = 1 flop (R5-053) and cannot see control flow (R5-054). torch.profiler `with_flops` covers matmul and conv only (R5-126). Non-matmul FLOPs cost about 16× a matmul FLOP on A100 (R5-011), so ±10% FLOP matching must be stated on matmul FLOPs and on total FLOPs. |
| Training FLOPs | fwd + 2×fwd (bwd) + recompute (checkpointing +1 fwd), × steps, including the HP search budget. For one-step/JFB gradients, count the backward over the steps actually differentiated. | DeepSpeed hard-codes bwd = 2×fwd (R5-055). 6N under-counts loops by T (R5-132). |
| Bytes moved | (1) Analytic minimum: parameters + states read and written per iteration. (2) If counters are available: `ncu --metrics dram__bytes.sum,lts__t_bytes.sum --cache-control none --replay-mode application` on 3–5 iterations. | ncu flushes caches and locks clocks by default (R5-123), which inflates DRAM bytes for L2-resident small graphs. Replays (R5-124). Counters need SYS_ADMIN/PERFMON in containers (R5-125); Vast.ai support is unverified. Fallback: analytic + roofline position (ridge ≈153 FLOP/byte on A100, R5-128). |
| Latency | CUDA events after warm-up and `torch.cuda.synchronize()`; median of ≥50 reps; batch size 1 and the eval batch; compile on/off stated; compile time reported separately. Never time under ncu. | Overhead-bound regime (R5-137): report with and without CUDA graphs. Halting only pays off at batch size 1 (R5-101/103). |
| Iterations | T_train, T_test, T_max; mean, distribution and max of executed iterations under G3. | The FLOPs counted must be the executed ones. Batched wall-clock follows the max. |
| Peak memory | `torch.cuda.max_memory_allocated()` per train step. | State whether checkpointing, truncation or JFB was used; they trade loop quality for memory (R5-093/140). |
| Determinism | `torch.use_deterministic_algorithms(True)` where possible; otherwise record that atomics were used. | `index_add_`/scatter on CUDA is nondeterministic (R5-062/063). |

Report all cost indicators side by side, never just one (R5-020/021/025). A system-comparison pitfall to avoid is changing the math between arms, as with bias or backward kernels dropped in one system and kept in its baseline (R5-136).

## (d) Failure evidence: where graph or dynamic routing loses on GPUs

- **FLOP reduction ≠ speed.**
  - FLOP-reducing attention showed no wall-clock gain (R5-007).
  - Reformer runs at 0.5× and BigBird at about 1× vanilla speed at 1K (R5-099/100).
  - Many sparse attention methods fall short of their theoretical gains (R5-014).
  - Sparse models cut FLOPs by orders of magnitude without matching speed-ups (R5-024).
  - Structured matrices lose to dense matmul (R5-010).
- **Sparse kernels underperform.**
  - At DNN sparsity levels, library sparse kernels lose to dense (R5-026/027).
  - The best SpMM kernels reach 27% of FP32 peak (R5-028), against 73% for dense FlashAttention-2 (R5-012).
- **Irregular access.**
  - Token-granular selection rules out FlashAttention-style kernels (R5-015/016).
  - The GCN aggregation L2 hit rate is 6.9%, against 56.2% for classic graph processing on the same graph (R5-087).
  - SpMM is more than 83.6% of GNN training time (R5-138).
- **Selection cost.** Top-k takes 12–27% of MaxK-GNN training time (R5-081). Sort-based top-k takes 28.9% of serving time (R5-084). A naive score-then-top-k materialises N² scores (R5-098).
- **Dynamic shapes.** Every unique shape triggers a CUDA-graph re-record (R5-059). Data-dependent ops break compilation (R5-061). Static compilers force a capacity factor (R5-039).
- **Halting.** The slowest sample sets batch latency (R5-103). FLOP savings do not become time savings when memory-bound (R5-105). Re-batching stalls the GPU (R5-106).
- **Sharing vs compute.** A looped model pays a 1B-model training cost for 580M-equivalent loss (R5-092). Adding parameters beats adding FLOPs per example in MoE pretraining (R5-045). Routing gains diminish with scale (R5-043).

## Unexplored (not found in our searches, 2026-10-01)

1. A wall-clock and bytes comparison of gather/scatter message passing against dense masked attention at matched FLOPs for N = 64–1024. Searched: `GNN dense adjacency vs sparse message passing small graphs GPU faster benchmark batched dense matmul molecules`. Results were only large-graph systems: TC-GNN, GNNBench, MaxK-GNN.
2. The cost of per-iteration learned top-k edge selection inside a recurrent graph. Searched: `GPU top-k selection kernel performance radix top-k benchmark arXiv 2024 2025`. Results were only LLM/MaxK-GNN contexts.
3. A FLOP counter that accounts for scatter, top-k and executed halting iterations: none found among torch, fvcore, DeepSpeed and calflops.
4. Scaling laws for recurrence in a graph substrate, or measured on algorithmic extrapolation rather than pretraining loss. Searched: `scaling laws parameter sharing looped transformer compute-optimal recursive weights arXiv 2025`.

## (e) Unconfirmed leads (kept out of the CSV)

- Venues from memory or snippets only: FlashAttention-2 at ICLR 2024 and FlexAttention at MLSys 2025.
- H100 SXM peak BF16 throughput, needed for the H100 ridge point. We did not fetch a vendor datasheet.
- RTX 4090 memory bandwidth. It is absent from the Vast.ai page.
- Whether Vast.ai containers grant CAP_SYS_ADMIN or CAP_PERFMON for Nsight Compute.
- Whether FlexAttention still requires lengths that are multiples of 128 in PyTorch 2.14. R5-069 is dated 2024-08.
- DeepSeek-V3.2 DSA/lightning-indexer primary paper. It is seen only through StreamIndex (R5-098) and the search snippet for 2512.03494 (downloaded, not used).
- Downloaded but not used: gSuite (2210.11601), Architectural Implications of GNNs (2009.00804), Huang et al. (2211.03021, which supports the "PyG wins only on small graphs" snippet; not quoted).
- Seen in search, not read: LoopCoder-v2 (2606.18023), DeepLoop (2607.13491), Guess-Verify-Refine top-k (2604.22312, downloaded, not used), UNIQUE top-k (2605.27740).
- MegaBlocks padding/token-drop numbers, Switch capacity factor, MoD and MoR wall-clock: already in R2 (R2-164, 169–176). Not duplicated.

## (f) Failed sources and process notes

- **Vast.ai.** The static HTML for vast.ai/pricing and the GPU pages contains no prices because they render client-side. We rendered the public page read-only in a headless browser and saved the snapshots as `sources/R5/vast_*_rendered_*.yml`. The cards do not say whether a price is on-demand or interruptible; R5-071–076 note this. A100 SXM4's "from $0.31" sits below the A100 PCIE floor and is probably an outlier, so plan on the median.
- **Stray files.** The headless browser also wrote 9 snapshot and console files to `the browser tool's cache directory` (timestamps 2026-10-01T17:00–17:01Z), outside the allowed write paths. Two were copied into `sources/R5/`. The originals were left in place, not deleted; flag them for cleanup.
- **PyTorch docs.** `docs.pytorch.org/docs/stable/...` returns redirect stubs. Pages were read from the `/docs/2.14/` paths, including the `user_guide/torch_compiler/` subpaths.
- **PDF extraction.** pdftotext dropped the √ in Chen et al. (R5-030 quotes around it) and the underscores in Nsight metric names (R5-046). R5-019 and R5-081 quote table cells whose column mapping we inferred; their confidence is Medium.
