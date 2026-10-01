<role>You are a senior ML-systems engineer (GPU kernels, sparse/irregular workloads, compute accounting), building a citation-grade evidence ledger for an open research paper.</role>
{COMMON}
<context>Project . (SR-2026-006). Read evidence/SCHEMA.md, docs/PREREGISTRATION.md and, if present, the dossiers evidence/research/R1–R4-*.md (do not edit them). The experiments compare matched arms (fixed-depth Transformer, looped Transformer, GNN, recurrent GNN, recurrent learned-topology graph with top-k routing and halting) on rented single GPUs (Vast.ai, RTX 4090/5090/A100/H100 class). Your job: what each arm actually costs on a GPU, and how to measure and match cost honestly.</context>
<task>
Families: GPU, BENCH, ROUTE, THEORY.
1. Irregular graph compute on GPUs: measured efficiency of scatter/gather message passing (PyTorch Geometric, DGL, torch_scatter / torch.sparse, JAX segment_sum / jraph) vs dense matmul attention at equal FLOPs; arithmetic intensity and memory-bandwidth bounds; the cost of dynamic top-k edge selection per iteration (topk, sorting, gather) and of changing sparsity patterns (no static kernel reuse, recompilation, torch.compile / CUDA-graph limits with data-dependent shapes).
2. Kernels that make dynamic sparse routing efficient: block-sparse / FlexAttention-style masked attention, Triton kernels for MoE dispatch (grouped GEMM, megablocks-style), sparse attention kernels with top-k selection (2024–2026), padding/capacity-factor overheads. Measured speedups and their conditions.
3. Recurrence costs: activation memory for BPTT over T iterations, gradient checkpointing, truncated backprop / one-step gradients, implicit-differentiation memory; reported wall-clock of looped vs unlooped models at matched FLOPs.
4. Compute accounting practice: how papers count FLOPs for recurrent / looped / MoE / sparse models, tools (fvcore, torch.utils.flop_counter, calflops, DeepSpeed profiler) and their known blind spots (scatter ops, sparse ops, data-dependent iteration counts); how to measure memory traffic (Nsight Compute dram__bytes, roofline). Papers criticising unmatched compute comparisons.
5. Parameter-sharing scaling: scaling laws or compute-optimal results for models with shared / recursive weights, and evidence on whether parameter reuse trades off against training FLOPs.
6. Current Vast.ai on-demand price ranges for RTX 4090, RTX 5090, A100 80GB, H100 (from vast.ai's own pages), dated.
</task>
<output_format>
File 1: evidence/research/R5-gpu-matching.csv — claim_id R5-001…, branch ∈ {GPU, BENCH, ROUTE, THEORY, X}.
File 2: evidence/research/R5-matrix.csv — approach_id A5-01…, one row per implementation approach (kernel / library / method), all 14 questions where applicable ("n/a" is allowed for questions that do not apply, e.g. q4 for a kernel).
File 3: evidence/research/R5-gpu-matching.md — (a) verdict-first summary ≤10 lines; (b) recommended implementation stack for each arm with expected bottleneck; (c) the measurement protocol (params, train FLOPs, inference FLOPs, bytes moved, latency, iterations) with tools and their blind spots; (d) failure evidence (where graph/dynamic routing loses on GPUs); (e) unconfirmed leads; (f) failed sources.
Write the CSVs incrementally. Target: 80–150 claim rows. Self-check: validator 0 REJECT for R5, 3 quotes re-read. Return to me ≤15 lines: counts, the 3 most decision-relevant findings, the recommended stack. Return findings to me; don't address the user.
</output_format>
