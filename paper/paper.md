# Is the graph doing anything? A sourced survey of recurrent self-routing neural graphs as an alternative to layered networks

SR-2026-006 · Scalably research note · v0.5 · 2026-10-01 · Pavle Lazić (Scalably) · code and data: https://github.com/scalably-io/neural-graph-substrate · archived: https://doi.org/10.5281/zenodo.23091812

Built with AI, disclosed in full: the survey, evidence ledger, analysis and this note were produced by Claude Opus 5.5 agents (Anthropic), directed by Pavle Lazić, and reviewed by fresh-context Claude Opus 5.5 reviewers and by GPT-6 Astra (OpenAI) as a second model family. It has not yet been reviewed by human experts. No experiments were run; every number below is a value reported by a cited source or computed from one.

## 1. Summary

**Question.** Can a persistent recurrent graph of neural nodes, which shares one message and one update function, rewires itself from its own state at every step, and computes by evolving until it halts, give more reasoning capacity per stored parameter than a Transformer, because the same weights are reused in different graph configurations?

**Method.** A quote-per-claim evidence ledger of 962 citable claims from 6 research workstreams across twenty neural-network families, a 121-row matrix answering fourteen fixed questions per approach, 7 adversarial reviews by fresh-context AI reviewers from two model families, which were allowed to reverse our conclusions, and a dedicated prior-art search in Transformer vocabulary.

**Answers.**
1. Against a fixed-depth Transformer, per stored parameter: recurrence helps (looped language models report 2 to 3 times parameter efficiency against other teams' models trained on different data, R2-016; a controlled study puts looping a block r times at about r to the power 0.46 distinct blocks, R4-185), but no cited evidence tests whether the graph adds to that, and a weight-shared looped Transformer already has it.
2. Against a looped Transformer: open. The closest study (LT2) compares dense, sparse, recurrent and hybrid mixers inside the same loop; which one wins depends on the task (Table 2), and no comparison in it isolates routing.
3. One controlled study finds recurrence does not raise knowledge storage: about 2 bits per parameter, looped or not.
4. Most components of the design are published, but separately. In our scoring of 15 rows (one of them a union of looped-Transformer papers), no row fully has more than 7 of the 13 components, and none fully has C10, C13 (Figure 1). These are results of our scoring, not proofs of absence. The full combination was not found in our search.
5. What remains open is narrow. LT2 already compares looped top-k, recurrent and dense mixers on retrieval beyond the training length and, across loop counts, on a curriculum trained at each size. Still open is whether learned, unsupervised top-k routing over all nodes beats a sharpened looped Transformer and looped recurrent controls on instance-size extrapolation in algorithmic problems. We publish a protocol to test it (Section 7) rather than results.

**What would change these answers.** A matched experiment in which learned routing beats a dense looped Transformer, a sharpened one, and looped recurrent and hybrid controls on size extrapolation would revise answer 2; a published version of that experiment would close answer 5.

## 2. The question and its scope

The brief asked for graph-native architectures on ordinary digital hardware only (GPU, TPU, CPU): no quantum, biological or neuromorphic substrates, and no agent systems. The candidate has 13 components, labelled C1 to C13 in Figure 1: persistent node states, a sparse directed graph, a shared message function, a shared update function, recurrent evolution over many steps, learned top-k routing or edge creation, hyperedges, topology conditioned on the current state, persistent associative memory, readouts attached to many graph regions, a confidence or convergence signal, learned adaptive halting, and topology and node roles that evolve during computation.

We separate two kinds of capacity, because the evidence treats them differently. Computational capacity is the size or difficulty of problem a model can solve; recurrence can plausibly raise it. Knowledge storage is what a model memorises; one controlled study finds recurrence does not raise it (Section 4.3).

We added one comparator the brief did not list: the weight-shared looped Transformer. Self-attention can be written as message passing on a complete token graph whose weights depend on the current state, as Joshi argues (R4-070, an author claim; R1-099 is the same paper), and a looped Transformer already reuses one set of weights over time. Beating a fixed-depth Transformer would answer the brief's performance question, but would not show whether routing adds anything beyond recurrence.

## 3. Method

**Evidence ledger.** Every row holds one claim, the source URL, a locator, a verbatim quote that contains the number when there is one, a status, and the date read. Quotes aim at forty words or fewer; the validator allows up to sixty, and 7 rows exceed forty. Rows enter the ledger only through a validator that rejects missing quotes, malformed IDs and reported numbers absent from their quote. The ledger holds 962 citable claims (358 reported results, 103 theorems, 174 design facts, 208 author claims, 107 repository facts, 12 of our own derivations) and 3 sources we could not access, which are kept but never cited. Author claims are attributed, never stated as fact.

**Approach matrix.** 121 approaches, each answering the brief's fourteen questions (computational graph, learned edges, topology at inference, persistent state, weight sharing, training, scaling, stability, capacity, whether more iterations help, GPU fit, repositories, best results, open problems). The matrix is only partly filled: for whether extra iterations help, 62 rows say unknown and 19 say not applicable.

**Review.** Three fresh-context Claude reviewers, not told our reasoning, attacked the survey and the experimental design and found 11 blocking errors; three more attacked drafts of this note; GPT-6 Astra then reviewed it as a second model family. Every finding was re-derived or re-fetched before we accepted it; the record is public (Section 8).

**Prior-art search.** The first workstreams searched mostly in graph-network vocabulary; the last searched in Transformer vocabulary and found the closest prior work (Section 5) that the earlier searches had missed. Rows added by the orchestrator while verifying reviewer findings are kept in their own file.

## 4. What the evidence says

### 4.1 Time can replace depth, and a looped Transformer already does it

Weight-tied recurrence extrapolates on algorithmic tasks when the input is fed back at every step and training does not tie behaviour to one iteration count: a recurrent network trained on 32-bit prefix sums reaches a peak of 97.12% on 512-bit strings, the best over test iterations, chosen after the fact (R4-024), and a recurrent graph network extrapolates to graphs 1000 times larger than in training (R1-027). Without a stabiliser it collapses after about 100 rounds (R1-029). Saunshi and colleagues report that k layers looped L times nearly match kL distinct layers (R4-080, an author claim). In the one parameter-matched test of a brain-inspired recurrent structure we found, a plain Transformer in the same recurrent pipeline came within about 5 points of it, without hyperparameter optimisation (R4-165): the hierarchical structure added at most that much, and an outer refinement loop drove most of the gain (R2-048).

### 4.2 Per parameter the gain is large; per unit of compute it is small or negative

Looped language models report 2 to 3 times parameter efficiency (R2-016), measured per stored parameter rather than per unit of compute; by our derivation the smaller looped model spends about 1.4 times the forward compute of its comparator, ignoring attention and early exit (R2-199). One study that loops the middle layers of a mixture-of-experts model, with parameters, compute per token and cache all matched, saves 6.8 to 18.0% of training compute (R2-089). An iso-depth study finds a looped model with 410M parameters at r = 4 matches a 580M model in loss but costs the training compute of a 1B model (R5-092), and looping a block r times is worth about r to the power 0.46 distinct blocks in language-model loss, where an exponent of one would mean full equivalence (R4-185). At language-model scale, extra test-time loops degrade after the trained depth of 4 (R2-018) or saturate (R2-095).

### 4.3 Recurrence does not add stored knowledge

A controlled study finds about 2 bits of knowledge per parameter for looped and non-looped models alike (R2-017). If that holds beyond looped Transformers, a recurrent graph would gain computation, not stored knowledge; the design's persistent associative memory (C9) is a separate question this evidence does not settle.

### 4.4 Routing: what is already published

Every routing ingredient of the design exists separately (Figure 1, Table 1).

- Per-query top-k attention dates from at least 2019 (R6-008). A 2025 model combines a recurrent reasoning unit with per-query top-k attention (R6-006, R6-007).
- A recurrent graph network with one weight-shared layer and dynamic pathways exists (R1-067), and per-node, state-conditioned roles (listen, broadcast, isolate) exist in a non-recurrent graph network (R1-059).
- Hard attention inside a recurrent processor is reported as important for size generalisation, tested on graphs of 16 to 1600 nodes (R6-010, an author claim; R6-011); it is trained with supervision on the algorithm's state transitions (R4-048, an author claim).
- The cited paper proves a dispersion limitation for softmax attention as the number of items grows (R6-001, read from the abstract). Sparser or sharper normalisations and selective attention mitigate it without hard top-k selection: one reports up to 1000 times length extrapolation on synthetic tasks (R6-016), and a weight-tied Transformer whose sharp, selective attention its authors describe as a form of neural routing reaches 100% length generalisation on a lookup task (R6-012).
- Restricting attention to the task's own edges helps, when supervised step by step: soft attention on the input graph reaches 99.97% last-step reachability at test size, against 91.51% for attention over the complete graph (92.34% against 88.98% averaged over steps), and max aggregation on the same edges reaches 99.80% (R6-017, R4-001, R4-002). The gap is graph structure, not discrete selection.
- Learned hyperedges exist (R1-109), and one recurrent model builds a new incidence matrix at every step from its current state and passes messages weighted by it, with parameters shared across steps (R1-164, R6-034, R6-035, R6-036): learned, state-conditioned hypergraph routing inside a loop is published, though without hard top-k selection.

Two results bear on whether routing, rather than something simpler, explains gains. First, pure locality: adding one causal convolution lifts a recursive model's state-tracking accuracy at length 128 from 45.8% to 91.4% (R7-032, R7-033). Second, relational attention with evolving edge states: a Transformer with them scores 81.30% against 42.34% without them on algorithm execution (R4-176). Neither is hard top-k routing, but the second is close to the brief's stateful relational computation.

![Figure 1. The components of the proposed design (columns) in the closest published systems (rows). Filled and ringed marks rest on a cited claim (some of them author claims, flagged in `evidence/coverage.csv`); grey dots come from the researchers' coverage tables and are not individually sourced; a question mark means we found no supporting claim. The counts are results of this scoring, not proofs of absence.](../figures/coverage.svg)

Table 1. The data behind Figure 1 (claim IDs per cell are in `evidence/coverage.csv`).

| system | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Looped Transformer family (union of several papers) | not established | no | yes | yes | yes | no | no | not established | no | not established | yes | yes | not established |
| LT2 looped sparse attention (2026) | not established | partly | yes | yes | yes | yes | not established | partly | not established | not established | not established | not established | not established |
| ReSSFormer (2025) | yes | yes | yes | yes | yes | yes | not established | yes | partly | not established | not established | not established | partly |
| Mixture-of-Recursions | not established | not established | not established | not established | yes | partly | no | partly | no | no | no | not established | partly |
| HRM / TRM recursive reasoning | not established | no | not established | yes | yes | no | no | no | no | not established | partly | yes | no |
| N2 recurrent graph network (2024) | yes | partly | yes | yes | yes | partly | no | partly | no | no | no | no | partly |
| Co-GNN | partly | partly | partly | no | no | partly | no | yes | no | no | no | no | partly |
| IterGNN | not established | not established | not established | not established | yes | no | no | no | no | no | partly | yes | no |
| Discrete NAR (2024) | not established | partly | not established | not established | yes | partly | not established | partly | not established | not established | not established | not established | not established |
| Pointer Graph Networks / NEE | not established | partly | not established | not established | not established | partly | not established | partly | not established | not established | not established | not established | partly |
| Continuous Thought Machine | yes | no | partly | no | yes | no | no | partly | no | partly | yes | partly | no |
| Energy Transformer | yes | no | yes | yes | yes | no | no | partly | yes | no | yes | not established | no |
| Graph Neural Cellular Automata | yes | yes | yes | yes | yes | no | no | no | no | no | no | no | no |
| Set-to-hypergraph recurrent refiner | yes | not established | yes | yes | yes | not established | yes | yes | not established | not established | not established | not established | partly |
| DyHSL learned hypergraph | not established | not established | not established | not established | not established | not established | yes | not established | not established | not established | not established | not established | not established |

### 4.5 On GPUs, an efficiency gain at these sizes is unshown

At the sizes algorithmic benchmarks use, we infer (without a measurement at these sizes) that dense masked attention is the fastest implementation: gather and scatter message passing is memory-bound in large-graph measurements (R5-086), and randomly placed top-k edges leave essentially no empty tile for block-sparse kernels to skip (R5-131, our derivation under stated assumptions). PyTorch's built-in FLOP counter counts nothing for scatter, gather or top-k (R5-049). At long context, block- or page-structured top-k attention does pay (R5-017, R5-041, R5-042); unstructured per-node top-k, as in this design, is not shown to. Our hypothesis, not a result: at these sizes the case for the design rests on inductive bias rather than efficiency, unless a measurement with learned, local edge patterns shows otherwise (the tile calculation assumes random targets).

## 5. The closest prior work

LT2 (arXiv 2605.20670) compares dense, sparse (learned top-k), recurrent and hybrid mixers inside the same weight-tied loop, at what the authors describe as the same parameter budget (R7-007, an author claim). We report its long-context results in full (Table 2 and Table 3). The source states its model size and hybrid ratio inconsistently (the caption and the table header give different model sizes, and the setup and the caption give different ratios of mixer to attention layers; R6-037, R6-038, R6-039), so we rely only on its reported scores.

- **A curriculum trained at each size**, sweeping the loop count (R7-004): the dense loop's best is a largest solved size of 64, while four other mixers reach 128 at their best loop count (R7-005, R7-006, R6-028); two of those four have no routing, and one of them reaches it only at eight loops (R6-032). The authors read this as looping helping cheaper mixers more than full attention (R6-027, an author claim).
- **Language-model evaluation** (Table 2 and Table 3): on most knowledge benchmarks the dense loop scores at or near the top, though not on all of them, and the authors present the routed hybrid as tracking it closely (R7-012, an author claim); on retrieval beyond the training length, dense attention scores zero, looped or not, while recurrent and hybrid mixers do not, and the authors attribute extrapolation to recurrent backbones (R6-026, an author claim).

Table 2. LT2's knowledge benchmarks at the training length, every model row and every column (R6-018 to R6-025).

| model (looped = weights shared over four steps) | mixer | SWDE | SQuAD | FDA | TQA | NQ | DROP | claim |
|---|---|---|---|---|---|---|---|---|
| Transformer | dense attention | 48.9 | 46.6 | 58.4 | 67.5 | 31.7 | 26.4 | R6-018 |
| GDN | gated linear recurrence (no routing) | 32.7 | 40.0 | 28.3 | 63.5 | 25.7 | 24.5 | R6-019 |
| Mamba-2 | state-space recurrence (no routing) | 30.7 | 39.1 | 23.7 | 64.3 | 25.1 | 28.5 | R6-020 |
| Looped Transformer | dense attention | 52.8 | 49.4 | 61.7 | 68.2 | 33.6 | 28.1 | R6-021 |
| Looped GDN | gated linear recurrence (no routing) | 34.9 | 41.8 | 30.6 | 64.7 | 27.0 | 25.9 | R6-022 |
| Looped Mamba-2 | state-space recurrence (no routing) | 33.9 | 40.5 | 25.8 | 65.1 | 26.8 | 29.7 | R6-023 |
| Looped Hybrid (GDN+DSA) | linear recurrence + learned sparse top-k attention (routing) | 51.6 | 48.0 | 60.4 | 66.9 | 33.0 | 28.4 | R6-024 |
| Looped Hybrid (Full+GDN) | full attention + linear recurrence (no routing) | 53.1 | 48.9 | 62.0 | 67.8 | 34.0 | 30.2 | R6-025 |

Table 3. LT2's retrieval tests at three lengths, every model row (R6-018 to R6-025); models were trained at 2048 tokens, so the 4096 columns test extrapolation.

| model | test 1, shorter | test 1, trained length | test 1, longer | test 2, shorter | test 2, trained | test 2, longer | test 3, shorter | test 3, trained | test 3, longer | claim |
|---|---|---|---|---|---|---|---|---|---|---|
| Transformer | 100.0 | 100.0 | 0.0 | 92.2 | 100.0 | 0.0 | 98.6 | 99.4 | 0.0 | R6-018 |
| GDN | 100.0 | 100.0 | 99.8 | 100.0 | 93.8 | 49.8 | 83.8 | 68.4 | 34.2 | R6-019 |
| Mamba-2 | 100.0 | 99.6 | 62.0 | 100.0 | 53.8 | 11.8 | 95.8 | 87.4 | 13.4 | R6-020 |
| Looped Transformer | 100.0 | 100.0 | 0.0 | 94.6 | 100.0 | 0.0 | 99.2 | 99.8 | 0.0 | R6-021 |
| Looped GDN | 100.0 | 100.0 | 99.8 | 100.0 | 96.4 | 53.2 | 85.6 | 71.0 | 35.8 | R6-022 |
| Looped Mamba-2 | 100.0 | 100.0 | 65.7 | 100.0 | 57.1 | 13.5 | 96.2 | 88.1 | 16.2 | R6-023 |
| Looped Hybrid (GDN+DSA) | 100.0 | 100.0 | 91.4 | 100.0 | 100.0 | 77.6 | 100.0 | 99.6 | 60.3 | R6-024 |
| Looped Hybrid (Full+GDN) | 100.0 | 100.0 | 93.5 | 100.0 | 100.0 | 81.0 | 99.8 | 99.8 | 63.7 | R6-025 |

Which mixer is best depends on the task, and none of LT2's comparisons varies routing alone. We found LT2 only when we searched in Transformer vocabulary. A study of the open question would extend it, and should include looped recurrent and hybrid mixers as controls alongside the dense and sharpened ones.

## 6. Novelty map

- **Established:** attention as soft, state-dependent message passing; softmax dispersion as the number of items grows, and sharper attention functions that mitigate it; per-query top-k attention, and recurrence combined with it; time replacing depth on algorithmic tasks, with stabilisers.
- **Reported by one controlled study:** recurrence adds computation but not stored knowledge.
- **Partly explored:** state-conditioned per-node roles and topology, per layer; edge creation with step supervision; hard selection for size generalisation, supervised; learned, state-conditioned hypergraph routing inside a recurrent loop; cheaper mixers, including top-k sparse attention, compared with dense attention inside a loop (LT2).
- **Not found in our search:** learned, unsupervised top-k routing over all nodes inside a weight-tied loop, compared with a dense and a sharpened looped Transformer, looped recurrent and hybrid controls, and a fixed local graph, at equal steps and no more matrix-multiply compute per step, on train-small, test-large problems. Also not found: hard top-k selection over learned hyperedges, or evolving node roles, inside a recurrent loop.

## 7. A protocol for the open question

We publish, but did not run, a preregistration-ready protocol (`docs/PREREGISTRATION.md`, with code in `ngs/`).

- **Arms.** A fixed-depth Transformer; a looped Transformer; a looped Transformer with sharpened attention; a fixed-depth and a looped graph network on the task's own edges; the candidate, a looped model whose every node attends to its top 8 nodes by current state; and the candidate with learned halting. All looped arms share one training recipe and receive the task's edges as a learned score bias; they differ in the attention or routing operator, plus a halting head in the last arm. After LT2, looped recurrent and hybrid controls must be added (open item six of the protocol).
- **Tasks.** Six families with exact solvers and train-small, test-large ladders: reachability, shortest path, mazes with and without cycles, sorting, associative recall and state tracking.
- **Budget.** Every looped arm runs the same number of steps, derived from the task alone: 1.5 times the steps a one-hop exact algorithm needs at the ninety-ninth percentile (reachability: from 12 steps at 16 nodes to 56 steps at 1024 nodes; mazes: from 81 steps at 9 cells per side to 737 steps at 33 cells per side). Answers are read at the last step.
- **Matching.** Stored parameters within 5%; the candidate never executes more matrix-multiply compute per step than the dense loop.
- **Statistics.** Paired seeds, between 5 and 15 per arm from a power rule; four mutually exclusive outcomes per comparison (superior, inferior, equivalent within 0.05 of normalised area under the accuracy curve, inconclusive); comparisons where both arms are at floor or both at ceiling do not count.
- **Before freezing,** six design questions remain open and are listed in the protocol.

## 8. Negative findings, including our own errors

The project log records 42 reversals and errors, each with its evidence. The most consequential:

- Our first draft said the evidence leaned against the design; its citations compared looped with non-looped Transformers, not graph with looped. We now say the question is open.
- We first believed the mechanism we wanted to test (soft attention spreading thin as problems grow) was ours to test; it is a published theorem with cheaper fixes.
- We first claimed the architecture was a new combination; recurrence with top-k attention, recurrent graph networks with dynamic pathways, hard attention in a loop, and sparse versus dense attention in a loop are all published.
- Our first experimental design would have credited the candidate with cheaper per-step compute as if it were inductive bias, could have produced a null result from floor effects alone, and chose the stopping step using test labels. Reviewers caught each; the published protocol fixes them.

## 9. Limitations and the strongest case against this note

- No experiment was run. Every verdict about routing is about the literature, not about a model we trained.
- Our searches were bounded: one day, a fixed set of queries per workstream, and one search engine rate-limited for much of the prior-art sweep. "Not found in our search" is not "does not exist". One closely related paper could be read only as an abstract, and 14 of the claims this note cites use an abstract as their locator, including the dispersion theorem and the sharpened-attention results the protocol's main control relies on.
- Figure 1 is our scoring: its grey "does not" marks are not individually sourced, cells we could not support are marked not established, and a fuller reading could raise counts. A second-model review raised one system's count after reading its full text.
- The reviewers were AI models (Claude and GPT-6). Human experts in looped Transformers or neural algorithmic reasoning may weigh the evidence differently.
- The strongest case against us: in LT2 the dense looped Transformer, our main comparator, loses on retrieval beyond the training length and on its curriculum, so a recurrent graph could beat it for reasons unrelated to routing, and a reader could take that as support for the design. Equally, if routing survives the sharpened-attention and recurrent controls on train-small, test-large problems, the design's core bet is right and this note is too cautious.

## 10. Reproduce and contribute

The ledger, matrix, coverage table, validator, task generators, step-budget and compute models, and the build of this note are in the project repository. Every number in this note is filled by `paper/build_paper.py`, never typed: reported results come from claim quotes (cross-checked against each claim's value), and the rest from claim text, our derivations, the coverage table, protocol constants or inventory counts. The build's checks are structural (it fails on a typed number, an unknown or inaccessible claim ID, a dash or a hype word); they do not verify meaning, which is what the reviews were for. To challenge a number, find its claim ID in Appendix A and check the quote against the source.

Code under Apache-2.0; text, data and figures under CC BY 4.0.

## Appendix A. Cited evidence

| ID | status | claim | verbatim quote | source |
|---|---|---|---|---|
| R1-027 | REPORTED | Recurrent GNNs (RecGRU-E) trained on size-10 graphs extrapolate to graphs 1,000 times larger | The RecGRU-E outperforms IterGNN and can extrapolate well to graphs that are 1,000 times larger than the graphs encountered during training. | https://arxiv.org/abs/2212.04934 |
| R1-029 | REPORTED | Without L2 state regularization, accuracy declines rapidly after ~100 rounds; with it, stable up to 10,000 rounds (graphs of size 10) | both versions output correct predictions until approximately 100 layers. Afterwards, the models trained with L2 regularization still stay stable while accuracy declines rapidly without regularization. | https://arxiv.org/abs/2212.04934 |
| R1-059 | DESIGN | Co-GNN: each node chooses per layer to listen/broadcast/both/isolate via an action network given its state and neighbors | an action network π predicts, for each node v, a probability (ℓ) distribution pv ∈ R4 over the actions {S, L, B, I} that v can take, given its state and the state of its neighbors Nv | https://arxiv.org/abs/2310.01267 |
| R1-067 | DESIGN | N2: a single shared recurrent layer moves graph nodes and pseudo nodes in a common space, building dynamic pathways at linear complexity | N2 incorporates a recurrent layer to parameterize the displacements of graph nodes and pseudo nodes in the common space. | https://arxiv.org/abs/2410.23686 |
| R1-099 | AUTHOR-CLAIM | Transformers are message-passing GNNs on fully connected token graphs that win the hardware lottery via dense matmuls | Transformers are implemented via dense matrix operations that are significantly more efficient on modern hardware than sparse message passing. This leads to the perspective that Transformers are GNNs currently winning the hardware lottery. | https://arxiv.org/abs/2506.22084 |
| R1-109 | DESIGN | DyHSL learns hypergraph structure by low-rank decomposition, contrasted with DHGNN kNN/K-means hyperedge construction | Compared to DHGNN that builds hypergraphs using kNN and K-Means algorithm to cluster node features, our DyHSL explicitly learns the structure of the hypergraph based on low rank matrix decomposition | https://arxiv.org/abs/2309.12028 |
| R1-164 | DESIGN | Set-to-hypergraph model uses a recurrent network that iteratively refines edge and node features to predict the incidence matrix (learned hyperedges) | We propose a simple recurrent neural network that refines the edge and node features, based on wich it predicts the incidence matrix while preserving the permutatio | https://arxiv.org/abs/2106.13919 |
| R2-016 | REPORTED | Ouro LoopLM 1.4B and 2.6B trained on 7.7T tokens match 4B and 8B standard transformers, 2-3x parameter efficiency | we demonstrate that 1.4B and 2.6B parameter LoopLMs match 4B and 8B standard transformers on most benchmarks, yielding 2-3× parameter-efficiency gains | https://arxiv.org/abs/2510.25741 |
| R2-017 | REPORTED | Ouro controlled study: recurrence does not increase raw knowledge storage, ~2 bits/parameter for looped and non-looped | we find recurrence does not increase raw knowledge storage (approximately 2 bits per parameter for looped and non-looped models) but dramatically enhances knowledge manipulation capabilities | https://arxiv.org/abs/2510.25741 |
| R2-018 | REPORTED | Ouro performance peaks at trained depth T=4 and degrades when extrapolating to T=5..8 | Performance peaks at the trained depth (T = 4) and then degrades. | https://arxiv.org/abs/2510.25741 |
| R2-048 | REPORTED | ARC Prize: outer refinement loop drives performance: +13pp from 1 to 2 loops; 1->8 refinement loops doubles public eval score | from no refinement (1 loop) to just 1 refinement, performance jumps by +13pp. From 1 to 8 refinement loops, the Public Evaluation set performance doubles. | https://arcprize.org/blog/hrm-analysis |
| R2-089 | REPORTED | SMELT: looping MoE middle layers twice with per-token FLOPs, total params and KV cache all matched saves 6.8-18.0% training FLOPs on compute-optimal frontier | SMELT’s loss drops faster with compute, saving 6.8–18.0% of training FLOPs on the compute-optimal frontier. | https://arxiv.org/abs/2609.01343 |
| R2-095 | REPORTED | Parcae: test-time looping follows a saturating exponential decay L(T)=L_inf + Z e^{-zT} | We find that the test-time scaling curves are well-described by a saturating exponential decay of the form: L(T ) = L∞ + Ze−z·T . | https://arxiv.org/abs/2604.12946 |
| R2-199 | DERIVED | Ouro 1.4B at 4 recurrent steps spends ~5.6B-dense-equivalent forward FLOPs/token, so matching a 4B dense model is a parameter win but not a FLOP win | Radar plots comparing the Ouro 1.4B and 2.6B models, both with 4 recurrent steps (red), against individual transformer baselines. | https://arxiv.org/abs/2510.25741 |
| R4-001 | REPORTED | Neural execution of graph algorithms: an MPNN with max aggregator, trained on 20-node graphs, predicts reachability (BFS) at 100 nodes with 99.80% last-step accuracy. | MPNN-max (Gilmer et al., 2017) 100.0% / 100.0% 100.0% / 100.0% 99.92% / 99.80% | https://arxiv.org/abs/1910.10593 |
| R4-002 | REPORTED | Same table: fully-connected attention (GAT-full, labelled Vaswani et al. 2017) reaches only 91.51% last-step reachability accuracy at 100 nodes vs MPNN-max 99.80%, trained at 20 nodes. | GAT-full* (Vaswani et al., 2017) 78.40% / 77.86% 85.76% / 91.83% 88.98% / 91.51% | https://arxiv.org/abs/1910.10593 |
| R4-024 | REPORTED | DT-Recall with progressive loss, trained on 32-bit prefix sums with at most 30 recurrent iterations, solves 512-bit strings at 97.12% peak accuracy (237 test iterations); plain DT gets 11.26%, FF 0.00%. | DT-Recall 1.0 237 97.12 ± 1.88 | https://arxiv.org/abs/2202.05826 |
| R4-048 | AUTHOR-CLAIM | Discrete NAR forces execution through finite predefined discrete states; with state-transition supervision it achieves perfect test scores and provable correctness for any test size. | Trained with supervision on the algorithm’s state transitions, such models are able to perfectly align with the original algorithm. To show this, we evaluate our approach on multiple algorithmic problems and achieve perfect test scores | https://arxiv.org/abs/2402.11628 |
| R4-070 | AUTHOR-CLAIM | Joshi 2025: Transformers are message-passing GNNs on fully connected token graphs, with attention giving relative importance of all tokens. | We show how Transformers can be viewed as message passing GNNs operating on fully connected graphs of tokens, where the self-attention mechanism capture the relative importance of all tokens w.r.t. each-other | https://arxiv.org/abs/2506.22084 |
| R4-080 | AUTHOR-CLAIM | Saunshi et al. 2025: a k-layer Transformer looped L times nearly matches a kL-layer non-looped model on addition, p-hop induction and math, and beats a k-layer model. | a k-layer transformer looped L times nearly matches the performance of a kL-layer non-looped model, and is significantly better than a k-layer model. | https://arxiv.org/abs/2502.17416 |
| R4-165 | REPORTED | ARC Prize analysis of HRM: a regular Transformer with the same ~27M parameters and the same pipeline comes within ~5pp of HRM without hyperparameter tuning. | a regular transformer comes within ~5pp of the HRM model without any hyperparameter optimization. | https://arcprize.org/blog/hrm-analysis |
| R4-176 | REPORTED | On 8 core CLRS algorithms a standard Transformer (re-tuned) averages 42.34% OOD vs 81.30% for the Relational Transformer that adds edge vectors. | Average 42.34% 81.30% | https://arxiv.org/abs/2210.05062 |
| R4-185 | REPORTED | Iso-depth scaling law for looped LMs: looping a block r times is worth about r^0.46 unique blocks in validation loss (phi = 1 would be full equivalence, phi = 0 no capacity gain) | we fit a joint scaling law L = E + A (Nonce + rφ Nrec )−α + B D−β and measure a recurrence-equivalence exponent φ = 0.46. | https://arxiv.org/abs/2604.21106 |
| R5-017 | REPORTED | NSA (trainable blockwise top-k sparse attention, Triton) reaches up to 9.0x forward and 6.0x backward speedup over FlashAttention-2 at 64k context | our NSA achieves progressively greater speedups as context length increases, up to 9.0× forward and 6.0× backward speedup at 64k context-length. | https://arxiv.org/abs/2502.11089 |
| R5-041 | REPORTED | MoBA reaches up to 6.5x speedup prefilling 1M tokens vs FlashAttention full attention | In particular, it achieves a speedup ratio of up to 6.5x when prefilling 1M tokens. | https://arxiv.org/abs/2502.13189 |
| R5-042 | REPORTED | Quest (query-aware top-k KV page selection): up to 7.03x self-attention speedup, 2.23x end-to-end decode latency vs FlashInfer | We show that Quest can achieve up to 7.03× self-attention speedup, which reduces inference latency by 2.23× while performing well on tasks with long dependencies with negligible accuracy loss. | https://arxiv.org/abs/2406.10774 |
| R5-049 | CODE | torch.utils.flop_counter: operators without a registered formula (and no decomposition) add zero FLOPs | Counts are produced by formulas in ``flop_registry``. Operators without a formula may be decomposed into registered operators; otherwise they add zero FLOPs. | https://github.com/pytorch/pytorch/blob/main/torch/utils/flop_counter.py |
| R5-086 | REPORTED | GCN on GPU: aggregation is memory-bound (L2 hit 6.87%, 2.35 DRAM bytes/op) while combination is compute-bound (L2 hit 82.5%, 0.01 DRAM bytes/op, 90% unit utilisation) | The irregularity also leads to low L2 Cache Hit Rate (6.87%) and high DRAM Byte per Operation (2.35). In contrary, the Combination phase achieves 90% Computation Unit Utilization and 2.49 Executed IPC. | https://arxiv.org/abs/2001.10160 |
| R5-092 | REPORTED | At r=4 a 410M looped model matches a 580M non-looped model in loss but costs the training compute of a 1B non-looped model | For example, at r=4 a 410M looped model performs on par with a 580M non-looped model, but incurs the training cost of a 1B non-looped one. | https://arxiv.org/abs/2604.21106 |
| R5-131 | DERIVED | Random top-k edges leave essentially no empty 128x128 tiles: at N=512, k=8 the probability a given tile is empty is ~1e-128, so block-sparse kernels degrade to dense for unstructured learned graphs | The BlockMask unlocks the opportunity to save the work for fully-masked score matrix blocks without loading a large elementwise attention mask. | https://arxiv.org/abs/2412.05496 |
| R6-001 | THEOREM | Softmax is not Enough: any learned softmax circuitry must disperse as the number of items grows at test time, even for finding the maximum key; proven theoretically | even for tasks as simple as finding the maximum key, any learned circuitry must disperse as the number of items grows at test time | https://arxiv.org/abs/2410.01104 |
| R6-006 | DESIGN | ReSSFormer combines a recurrent reasoning unit with bounded depth and an adaptive sparse attention module | Recurrent Reasoning & Memory Unit (R2MU) for iterative reasoning with bounded depth, Adaptive Sparse Attention Module (ASAM) for efficient and focused context selection | https://arxiv.org/abs/2510.01585 |
| R6-007 | DESIGN | ReSSFormer's sparse attention selects, for each query, only the k highest-scoring keys (hard top-k routing) | For each query q i q_{i} , only the k k highest-scoring keys are selected for attention computation | https://arxiv.org/html/2510.01585 |
| R6-008 | DESIGN | Explicit Sparse Transformer: explicit top-k selection of the most relevant segments in self-attention (2019) | improve the concentration of attention on the global context through an explicit selection of the most relevant segments | https://arxiv.org/abs/1912.11637 |
| R6-010 | AUTHOR-CLAIM | Discrete NAR enforces hard attention in its recurrent processor and reports it as important for size generalisation, overcoming attention-weight annealing on arbitrarily large graphs | we enforce attention to be hard attention. We found this property important not only for interpretability but also for size generalization, as hard attention allows us to overcome the annealing of the attention weights for arbitrarily large graphs | https://arxiv.org/html/2402.11628 |
| R6-011 | DESIGN | Discrete NAR trains on SALSA-CLRS graphs of at most 16 nodes and tests on sparse graphs of 16 to 1600 nodes | The test set consists of sparse graphs of sizes from 16 to 1600 nodes | https://arxiv.org/html/2402.11628 |
| R6-012 | REPORTED | Neural Data Router (weight-tied Transformer with copy gate and geometric attention) reaches 100% length generalisation on compositional table lookup | achieves 100% length generalization accuracy on the classic compositional table lookup task | https://arxiv.org/abs/2110.07732 |
| R6-016 | REPORTED | ASEntmax (alpha-entmax with adaptive scalable temperature) outperforms softmax, scalable softmax and fixed-temperature alpha-entmax, reaching up to 1000x length extrapolation | substantially outperforms softmax, scalable softmax, and fixed-temperature $\alpha$-entmax baselines, achieving up to 1000$\times$ length extrapolation on synthetic benchmarks | https://arxiv.org/abs/2506.16640 |
| R6-017 | REPORTED | Neural execution of graph algorithms: soft attention restricted to the input graph (GAT*) reaches 99.97% last-step reachability at 100 nodes (trained at 20), vs 91.51% for attention over the complete graph (GAT-full) | GAT* (Veličković et al., 2018) GAT-full* (Vaswani et al., 2017) 93.28% / 99.86% 78.40% / 77.86% 93.97% / 100.0% 85.76% / 91.83% 92.34% / 99.97% 88.98% / 91.51% | https://arxiv.org/abs/1910.10593 |
| R6-018 | REPORTED | LT2 Table 5, Transformer (dense attention): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 0.0 / 0.0 / 0.0 | Transformer 48.9 46.6 58.4 67.5 31.7 26.4 100.0 100.0 0.0 92.2 100.0 0.0 98.6 99.4 0.0 | https://arxiv.org/html/2605.20670 |
| R6-019 | REPORTED | LT2 Table 5, GDN (gated linear recurrence (no routing)): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 99.8 / 49.8 / 34.2 | GDN 32.7 40.0 28.3 63.5 25.7 24.5 100.0 100.0 99.8 100.0 93.8 49.8 83.8 68.4 34.2 | https://arxiv.org/html/2605.20670 |
| R6-020 | REPORTED | LT2 Table 5, Mamba-2 (state-space recurrence (no routing)): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 62.0 / 11.8 / 13.4 | Mamba-2 30.7 39.1 23.7 64.3 25.1 28.5 100.0 99.6 62.0 100.0 53.8 11.8 95.8 87.4 13.4 | https://arxiv.org/html/2605.20670 |
| R6-021 | REPORTED | LT2 Table 5, Looped Transformer (dense attention): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 0.0 / 0.0 / 0.0 | Looped Transformer 52.8 49.4 61.7 68.2 33.6 28.1 100.0 100.0 0.0 94.6 100.0 0.0 99.2 99.8 0.0 | https://arxiv.org/html/2605.20670 |
| R6-022 | REPORTED | LT2 Table 5, Looped GDN (gated linear recurrence (no routing)): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 99.8 / 53.2 / 35.8 | Looped GDN 34.9 41.8 30.6 64.7 27.0 25.9 100.0 100.0 99.8 100.0 96.4 53.2 85.6 71.0 35.8 | https://arxiv.org/html/2605.20670 |
| R6-023 | REPORTED | LT2 Table 5, Looped Mamba-2 (state-space recurrence (no routing)): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 65.7 / 13.5 / 16.2 | Looped Mamba-2 33.9 40.5 25.8 65.1 26.8 29.7 100.0 100.0 65.7 100.0 57.1 13.5 96.2 88.1 16.2 | https://arxiv.org/html/2605.20670 |
| R6-024 | REPORTED | LT2 Table 5, Looped Hybrid (GDN+DSA) (linear recurrence + learned sparse top-k attention (routing)): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 91.4 / 77.6 / 60.3 | Looped Hybrid (GDN+DSA) 51.6 48.0 60.4 66.9 33.0 28.4 100.0 100.0 91.4 100.0 100.0 77.6 100.0 99.6 60.3 | https://arxiv.org/html/2605.20670 |
| R6-025 | REPORTED | LT2 Table 5, Looped Hybrid (Full+GDN) (full attention + linear recurrence (no routing)): NIAH-Single-1/2/3 at 4096 tokens after pre-training at 2048 = 93.5 / 81.0 / 63.7 | Looped Hybrid (Full+GDN) 53.1 48.9 62.0 67.8 34.0 30.2 100.0 100.0 93.5 100.0 100.0 81.0 99.8 99.8 63.7 | https://arxiv.org/html/2605.20670 |
| R6-026 | AUTHOR-CLAIM | LT2 authors: looped variants retain their base mixer's NIAH behaviour; recurrent backbones extrapolate to 4096 while dense-attention ones do not | they retain the qualitative NIAH behavior of their base versions – recurrent backbones extrapolate gracefully to 4096 while dense-attention ones do not | https://arxiv.org/html/2605.20670 |
| R6-027 | AUTHOR-CLAIM | LT2 authors: looping helps subquadratic mixers more than full attention on the state-tracking + recall curriculum | The striking pattern is that looping helps subquadratic mixers more than it helps full attention | https://arxiv.org/html/2605.20670 |
| R6-028 | AUTHOR-CLAIM | LT2: Looped Full+GDN (no routing) also reaches stage 5 (n_max = 128), attributed by the authors to its linear-time GDN half | Looped Full+GDN does too, but only because half its block is already linear-time GDN | https://arxiv.org/html/2605.20670 |
| R6-032 | REPORTED | LT2 curriculum: Looped GDN+Window solves only stage 3 at loop counts up to 4 and reaches stage 5 only at 8 loops; the n_max = 128 results are best-over-T | Looped GDN+Window is the most dramatic: stage 3 at T ≤ 4 , stage 5 at T = 8 . | https://arxiv.org/html/2605.20670 |
| R6-034 | DESIGN | Set-to-hypergraph model produces a new incidence matrix at every step from the previous step's edge and node vectors | we produce a new incidence matrix for step t based on the edge and node vectors from the previous step | https://arxiv.org/abs/2106.13919 |
| R6-035 | DESIGN | Set-to-hypergraph model shares parameters between refinement steps, making it recurrent | By sharing the parameters between different refinement steps, we naturally obtain a recurrent model. | https://arxiv.org/abs/2106.13919 |
| R6-036 | DESIGN | Set-to-hypergraph model aggregates neighbouring edges weighted by the learned incidence probabilities, akin to message passing | This aggregation works akin to message passing in graph neural networks | https://arxiv.org/abs/2106.13919 |
| R6-037 | DESIGN | LT2 setup prose: hybrids interleave the mixer with full attention in a fixed 4:1 ratio | hybrids interleave that mixer with full attention in a fixed 4 : 1 ratio | https://arxiv.org/html/2605.20670 |
| R6-038 | DESIGN | LT2 Table 5 caption: hybrid models interleave with full attention in a 1:1 ratio, evaluated at 1.3B parameters | hybrid models interleave with full attention in a 1 : 1 ratio | https://arxiv.org/html/2605.20670 |
| R6-039 | DESIGN | LT2 Table 5 header labels the models 1.5B, while its caption says 1.3B | underline marks the second best. Model (1.5B) | https://arxiv.org/html/2605.20670 |
| R7-004 | DESIGN | LT2 synthetic state-tracking+recall task grows n=m along a curriculum and reports the largest stage solved (n_max), i.e. trained-at-size performance, not train-small/test-large extrapolation | We tie n = m and grow them together along the curriculum { 8 , 16 , 32 , 64 , 128 , 256 } ; a model advances once eval accuracy reaches 0.90 within a 100 k-step budget. | https://arxiv.org/abs/2605.20670 |
| R7-005 | REPORTED | On LT2 state-tracking+recall, the dense Looped Transformer plateaus at n_max=64 at every loop count T | Looped Transformer and Looped Full+Window plateau at stage 4 ( n max = 64 ) and never reach stage 5 at any T . | https://arxiv.org/abs/2605.20670 |
| R7-006 | REPORTED | On LT2 state-tracking+recall, Looped NSA (learned top-k sparse attention in a loop) reaches n_max=128, double the dense looped Transformer | three subquadratic variants — Looped NSA, Looped GDN+Window, and Looped GDN+NSA — all reach stage 5 ( n max = 128 ) | https://arxiv.org/abs/2605.20670 |
| R7-007 | AUTHOR-CLAIM | LT2 compares sparse and dense looped arms at the same parameter budget | a doubling of n max over the global-attention baseline at the same parameter budget. | https://arxiv.org/abs/2605.20670 |
| R7-012 | AUTHOR-CLAIM | LT2 attributes better NIAH extrapolation to the GDN+DSA loop despite it having no quadratic component | Looped Hybrid (GDN+DSA) tracks the Looped Transformer closely on the knowledge suite despite containing no quadratic component, and additionally extrapolates substantially better at NIAH-4096. | https://arxiv.org/abs/2605.20670 |
| R7-032 | REPORTED | Plain TRM fails to extrapolate on A5 state tracking: 45.8% at length 128 after training on up to 32 updates | plain TRM fails to extrapolate: at length 128, TRM and TRM with ACT enabled both obtain 45.8 % ± 3.9 % on A 5 | https://arxiv.org/abs/2606.18206 |
| R7-033 | REPORTED | Adding a causal 1D convolution to TRM raises A5 length-128 accuracy to 91.4% | Adding a causal 1D convolution layer substantially improves length generalization, reaching 91.4 % ± 2.3 % on A 5 | https://arxiv.org/abs/2606.18206 |
