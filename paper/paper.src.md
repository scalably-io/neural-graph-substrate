# Is the graph doing anything? A sourced survey of recurrent self-routing neural graphs as an alternative to layered networks

SR-2026-006 · Scalably research note · {{version}} · {{date}} · Pavle Lazić (Scalably)

Built with AI, disclosed in full: the survey, evidence ledger, analysis and this note were produced by Claude Opus 5.5 agents (Anthropic), directed by Pavle Lazić, and reviewed by fresh-context Claude Opus 5.5 reviewers and by GPT-6 Astra (OpenAI) as a second model family. It has not yet been reviewed by human experts. No experiments were run; every number below is a value reported by a cited source or computed from one.

## 1. Summary

**Question.** Can a persistent recurrent graph of neural nodes, which shares one message and one update function, rewires itself from its own state at every step, and computes by evolving until it halts, give more reasoning capacity per stored parameter than a Transformer, because the same weights are reused in different graph configurations?

**Method.** A quote-per-claim evidence ledger of {{n_claims}} citable claims from {{n_workstreams}} research workstreams across twenty neural-network families, a {{n_approaches}}-row matrix answering fourteen fixed questions per approach, {{n_reviews}} rounds of adversarial review by fresh-context AI reviewers that were allowed to reverse our conclusions, and a dedicated prior-art search in Transformer vocabulary.

**Answers.**
1. Against a fixed-depth Transformer, per stored parameter: recurrence helps (looped language models report {{ouro_lo}} to {{ouro_hi}} times parameter efficiency against other teams' models trained on different data, R2-016; a controlled study puts looping a block r times at about r to the power {{phi}} distinct blocks, R4-185), but no cited evidence tests whether the graph adds to that, and a weight-shared looped Transformer already has it.
2. Against a looped Transformer: open. The closest study (LT2) compares dense, sparse, recurrent and hybrid mixers inside the same loop; which one wins depends on the task (Table 2), and no comparison in it isolates routing.
3. One controlled study finds recurrence does not raise knowledge storage: about {{bits}} bits per parameter, looped or not.
4. Most components of the design are published, but separately. In our scoring of {{n_systems}} rows (one of them a union of looped-Transformer papers), no row fully has more than {{best_y}} of the {{n_components}} components, and none fully has {{never_y}} (Figure 1). These are results of our scoring, not proofs of absence. The full combination was not found in our search.
5. What remains open is narrow. LT2 already compares looped top-k, recurrent and dense mixers on retrieval beyond the training length and, across loop counts, on a curriculum trained at each size. Still open is whether learned, unsupervised top-k routing over all nodes beats a sharpened looped Transformer and looped recurrent controls on instance-size extrapolation in algorithmic problems. We publish a protocol to test it (Section 7) rather than results.

**What would change these answers.** A matched experiment in which learned routing beats a dense looped Transformer, a sharpened one, and looped recurrent and hybrid controls on size extrapolation would revise answer 2; a published version of that experiment would close answer 5.

## 2. The question and its scope

The brief asked for graph-native architectures on ordinary digital hardware only (GPU, TPU, CPU): no quantum, biological or neuromorphic substrates, and no agent systems. The candidate has {{n_components}} components, labelled C1 to C13 in Figure 1: persistent node states, a sparse directed graph, a shared message function, a shared update function, recurrent evolution over many steps, learned top-k routing or edge creation, hyperedges, topology conditioned on the current state, persistent associative memory, readouts attached to many graph regions, a confidence or convergence signal, learned adaptive halting, and topology and node roles that evolve during computation.

We separate two kinds of capacity, because the evidence treats them differently. Computational capacity is the size or difficulty of problem a model can solve; recurrence can plausibly raise it. Knowledge storage is what a model memorises; one controlled study finds recurrence does not raise it (Section 4.3).

We added one comparator the brief did not list: the weight-shared looped Transformer. Self-attention can be written as message passing on a complete token graph whose weights depend on the current state, as Joshi argues (R4-070, an author claim; R1-099 is the same paper), and a looped Transformer already reuses one set of weights over time. Beating a fixed-depth Transformer would answer the brief's performance question, but would not show whether routing adds anything beyond recurrence.

## 3. Method

**Evidence ledger.** Every row holds one claim, the source URL, a locator, a verbatim quote that contains the number when there is one, a status, and the date read. Quotes aim at forty words or fewer; the validator allows up to sixty, and {{n_long_quotes}} rows exceed forty. Rows enter the ledger only through a validator that rejects missing quotes, malformed IDs and reported numbers absent from their quote. The ledger holds {{n_claims}} citable claims ({{n_reported}} reported results, {{n_theorem}} theorems, {{n_design}} design facts, {{n_author}} author claims, {{n_code}} repository facts, {{n_derived}} of our own derivations) and {{n_failed}} sources we could not access, which are kept but never cited. Author claims are attributed, never stated as fact.

**Approach matrix.** {{n_approaches}} approaches, each answering the brief's fourteen questions (computational graph, learned edges, topology at inference, persistent state, weight sharing, training, scaling, stability, capacity, whether more iterations help, GPU fit, repositories, best results, open problems). The matrix is only partly filled: for whether extra iterations help, {{q10_unknown}} rows say unknown and {{q10_na}} say not applicable.

**Review.** Three fresh-context Claude reviewers, not told our reasoning, attacked the survey and the experimental design and found {{n_blockers}} blocking errors; three more attacked drafts of this note; GPT-6 Astra then reviewed it as a second model family. Every finding was re-derived or re-fetched before we accepted it; the record is public (Section 8).

**Prior-art search.** The first workstreams searched mostly in graph-network vocabulary; the last searched in Transformer vocabulary and found the closest prior work (Section 5) that the earlier searches had missed. Rows added by the orchestrator while verifying reviewer findings are kept in their own file.

## 4. What the evidence says

### 4.1 Time can replace depth, and a looped Transformer already does it

Weight-tied recurrence extrapolates on algorithmic tasks when the input is fed back at every step and training does not tie behaviour to one iteration count: a recurrent network trained on {{dt_from}}-bit prefix sums reaches a peak of {{dt_acc}}% on {{dt_to}}-bit strings, the best over test iterations, chosen after the fact (R4-024), and a recurrent graph network extrapolates to graphs {{rgnn_x}} times larger than in training (R1-027). Without a stabiliser it collapses after about {{rgnn_collapse}} rounds (R1-029). Saunshi and colleagues report that k layers looped L times nearly match kL distinct layers (R4-080, an author claim). In the one parameter-matched test of a brain-inspired recurrent structure we found, a plain Transformer in the same recurrent pipeline came within about {{hrm_gap}} points of it, without hyperparameter optimisation (R4-165): the hierarchical structure added at most that much, and an outer refinement loop drove most of the gain (R2-048).

### 4.2 Per parameter the gain is large; per unit of compute it is small or negative

Looped language models report {{ouro_lo}} to {{ouro_hi}} times parameter efficiency (R2-016), measured per stored parameter rather than per unit of compute; by our derivation the smaller looped model spends about {{ouro_vs4b}} times the forward compute of its comparator, ignoring attention and early exit (R2-199). One study that loops the middle layers of a mixture-of-experts model, with parameters, compute per token and cache all matched, saves {{smelt_lo}} to {{smelt_hi}}% of training compute (R2-089). An iso-depth study finds a looped model with {{loop_small}}M parameters at r = {{loop_r}} matches a {{loop_match}}M model in loss but costs the training compute of a {{loop_cost}}B model (R5-092), and looping a block r times is worth about r to the power {{phi}} distinct blocks in language-model loss, where an exponent of one would mean full equivalence (R4-185). At language-model scale, extra test-time loops degrade after the trained depth of {{ouro_peak}} (R2-018) or saturate (R2-095).

### 4.3 Recurrence does not add stored knowledge

A controlled study finds about {{bits}} bits of knowledge per parameter for looped and non-looped models alike (R2-017). If that holds beyond looped Transformers, a recurrent graph would gain computation, not stored knowledge; the design's persistent associative memory (C9) is a separate question this evidence does not settle.

### 4.4 Routing: what is already published

Every routing ingredient of the design exists separately (Figure 1, Table 1).

- Per-query top-k attention dates from at least 2019 (R6-008). A 2025 model combines a recurrent reasoning unit with per-query top-k attention (R6-006, R6-007).
- A recurrent graph network with one weight-shared layer and dynamic pathways exists (R1-067), and per-node, state-conditioned roles (listen, broadcast, isolate) exist in a non-recurrent graph network (R1-059).
- Hard attention inside a recurrent processor is reported as important for size generalisation, tested on graphs of {{dnar_lo}} to {{dnar_hi}} nodes (R6-010, an author claim; R6-011); it is trained with supervision on the algorithm's state transitions (R4-048, an author claim).
- The cited paper proves a dispersion limitation for softmax attention as the number of items grows (R6-001, read from the abstract). Sparser or sharper normalisations and selective attention mitigate it without hard top-k selection: one reports up to {{asent}} times length extrapolation on synthetic tasks (R6-016), and a weight-tied Transformer whose sharp, selective attention its authors describe as a form of neural routing reaches {{ndr}}% length generalisation on a lookup task (R6-012).
- Restricting attention to the task's own edges helps, when supervised step by step: soft attention on the input graph reaches {{gat_star}}% last-step reachability at test size, against {{gat_full}}% for attention over the complete graph ({{gat_star_mean}}% against {{gat_full_mean}}% averaged over steps), and max aggregation on the same edges reaches {{mpnn_max}}% (R6-017, R4-001, R4-002). The gap is graph structure, not discrete selection.
- Learned hyperedges exist (R1-109), and one recurrent model builds a new incidence matrix at every step from its current state and passes messages weighted by it, with parameters shared across steps (R1-164, R6-034, R6-035, R6-036): learned, state-conditioned hypergraph routing inside a loop is published, though without hard top-k selection.

Two results bear on whether routing, rather than something simpler, explains gains. First, pure locality: adding one causal convolution lifts a recursive model's state-tracking accuracy at length {{trm_len}} from {{trm_plain}}% to {{trm_conv}}% (R7-032, R7-033). Second, relational attention with evolving edge states: a Transformer with them scores {{rt_edge}}% against {{rt_plain}}% without them on algorithm execution (R4-176). Neither is hard top-k routing, but the second is close to the brief's stateful relational computation.

![Figure 1. The components of the proposed design (columns) in the closest published systems (rows). Filled and ringed marks rest on a cited claim (some of them author claims, flagged in `evidence/coverage.csv`); grey dots come from the researchers' coverage tables and are not individually sourced; a question mark means we found no supporting claim. The counts are results of this scoring, not proofs of absence.](../figures/coverage.svg)

Table 1. The data behind Figure 1 (claim IDs per cell are in `evidence/coverage.csv`).

{{T_coverage}}

### 4.5 On GPUs, an efficiency gain at these sizes is unshown

At the sizes algorithmic benchmarks use, we infer (without a measurement at these sizes) that dense masked attention is the fastest implementation: gather and scatter message passing is memory-bound in large-graph measurements (R5-086), and randomly placed top-k edges leave essentially no empty tile for block-sparse kernels to skip (R5-131, our derivation under stated assumptions). PyTorch's built-in FLOP counter counts nothing for scatter, gather or top-k (R5-049). At long context, block- or page-structured top-k attention does pay (R5-017, R5-041, R5-042); unstructured per-node top-k, as in this design, is not shown to. Our hypothesis, not a result: at these sizes the case for the design rests on inductive bias rather than efficiency, unless a measurement with learned, local edge patterns shows otherwise (the tile calculation assumes random targets).

## 5. The closest prior work

LT2 (arXiv 2605.20670) compares dense, sparse (learned top-k), recurrent and hybrid mixers inside the same weight-tied loop, at what the authors describe as the same parameter budget (R7-007, an author claim). We report its long-context results in full (Table 2 and Table 3). The source states its model size and hybrid ratio inconsistently (the caption and the table header give different model sizes, and the setup and the caption give different ratios of mixer to attention layers; R6-037, R6-038, R6-039), so we rely only on its reported scores.

- **A curriculum trained at each size**, sweeping the loop count (R7-004): the dense loop's best is a largest solved size of {{lt2_dense}}, while four other mixers reach {{lt2_sparse}} at their best loop count (R7-005, R7-006, R6-028); two of those four have no routing, and one of them reaches it only at eight loops (R6-032). The authors read this as looping helping cheaper mixers more than full attention (R6-027, an author claim).
- **Language-model evaluation** (Table 2 and Table 3): on most knowledge benchmarks the dense loop scores at or near the top, though not on all of them, and the authors present the routed hybrid as tracking it closely (R7-012, an author claim); on retrieval beyond the training length, dense attention scores zero, looped or not, while recurrent and hybrid mixers do not, and the authors attribute extrapolation to recurrent backbones (R6-026, an author claim).

Table 2. LT2's knowledge benchmarks at the training length, every model row and every column (R6-018 to R6-025).

{{T_lt2_know}}

Table 3. LT2's retrieval tests at three lengths, every model row (R6-018 to R6-025); models were trained at {{niah_train}} tokens, so the {{niah_test}} columns test extrapolation.

{{T_lt2_ret}}

Which mixer is best depends on the task, and none of LT2's comparisons varies routing alone. We found LT2 only when we searched in Transformer vocabulary. A study of the open question would extend it, and should include looped recurrent and hybrid mixers as controls alongside the dense and sharpened ones.

## 6. Novelty map

- **Established:** attention as soft, state-dependent message passing; softmax dispersion as the number of items grows, and sharper attention functions that mitigate it; per-query top-k attention, and recurrence combined with it; time replacing depth on algorithmic tasks, with stabilisers.
- **Reported by one controlled study:** recurrence adds computation but not stored knowledge.
- **Partly explored:** state-conditioned per-node roles and topology, per layer; edge creation with step supervision; hard selection for size generalisation, supervised; learned, state-conditioned hypergraph routing inside a recurrent loop; cheaper mixers, including top-k sparse attention, compared with dense attention inside a loop (LT2).
- **Not found in our search:** learned, unsupervised top-k routing over all nodes inside a weight-tied loop, compared with a dense and a sharpened looped Transformer, looped recurrent and hybrid controls, and a fixed local graph, at equal steps and no more matrix-multiply compute per step, on train-small, test-large problems. Also not found: hard top-k selection over learned hyperedges, or evolving node roles, inside a recurrent loop.

## 7. A protocol for the open question

We publish, but did not run, a preregistration-ready protocol (`docs/PREREGISTRATION.md`, with code in `ngs/`).

- **Arms.** A fixed-depth Transformer; a looped Transformer; a looped Transformer with sharpened attention; a fixed-depth and a looped graph network on the task's own edges; the candidate, a looped model whose every node attends to its top {{k}} nodes by current state; and the candidate with learned halting. All looped arms share one training recipe and receive the task's edges as a learned score bias; they differ in the attention or routing operator, plus a halting head in the last arm. After LT2, looped recurrent and hybrid controls must be added (open item six of the protocol).
- **Tasks.** Six families with exact solvers and train-small, test-large ladders: reachability, shortest path, mazes with and without cycles, sorting, associative recall and state tracking.
- **Budget.** Every looped arm runs the same number of steps, derived from the task alone: {{budget_factor}} times the steps a one-hop exact algorithm needs at the ninety-ninth percentile (reachability: from {{reach_first}} to {{reach_last}}; mazes: from {{maze_first}} to {{maze_last}}). Answers are read at the last step.
- **Matching.** Stored parameters within {{param_tol}}%; the candidate never executes more matrix-multiply compute per step than the dense loop.
- **Statistics.** Paired seeds, between {{seeds_lo}} and {{seeds_hi}} per arm from a power rule; four mutually exclusive outcomes per comparison (superior, inferior, equivalent within {{delta}} of normalised area under the accuracy curve, inconclusive); comparisons where both arms are at floor or both at ceiling do not count.
- **Before freezing,** six design questions remain open and are listed in the protocol.

## 8. Negative findings, including our own errors

The project log records {{n_negative}} reversals and errors, each with its evidence. The most consequential:

- Our first draft said the evidence leaned against the design; its citations compared looped with non-looped Transformers, not graph with looped. We now say the question is open.
- We first believed the mechanism we wanted to test (soft attention spreading thin as problems grow) was ours to test; it is a published theorem with cheaper fixes.
- We first claimed the architecture was a new combination; recurrence with top-k attention, recurrent graph networks with dynamic pathways, hard attention in a loop, and sparse versus dense attention in a loop are all published.
- Our first experimental design would have credited the candidate with cheaper per-step compute as if it were inductive bias, could have produced a null result from floor effects alone, and chose the stopping step using test labels. Reviewers caught each; the published protocol fixes them.

## 9. Limitations and the strongest case against this note

- No experiment was run. Every verdict about routing is about the literature, not about a model we trained.
- Our searches were bounded: one day, a fixed set of queries per workstream, and one search engine rate-limited for much of the prior-art sweep. "Not found in our search" is not "does not exist". One closely related paper could be read only as an abstract, and {{n_abstract_only}} of the claims this note cites use an abstract as their locator, including the dispersion theorem and the sharpened-attention results the protocol's main control relies on.
- Figure 1 is our scoring: its grey "does not" marks are not individually sourced, cells we could not support are marked not established, and a fuller reading could raise counts. A second-model review raised one system's count after reading its full text.
- The reviewers were AI models (Claude and GPT-6). Human experts in looped Transformers or neural algorithmic reasoning may weigh the evidence differently.
- The strongest case against us: in LT2 the dense looped Transformer, our main comparator, loses on retrieval beyond the training length and on its curriculum, so a recurrent graph could beat it for reasons unrelated to routing, and a reader could take that as support for the design. Equally, if routing survives the sharpened-attention and recurrent controls on train-small, test-large problems, the design's core bet is right and this note is too cautious.

## 10. Reproduce and contribute

The ledger, matrix, coverage table, validator, task generators, step-budget and compute models, and the build of this note are in the project repository. Every number in this note is filled by `paper/build_paper.py`, never typed: reported results come from claim quotes (cross-checked against each claim's value), and the rest from claim text, our derivations, the coverage table, protocol constants or inventory counts. The build's checks are structural (it fails on a typed number, an unknown or inaccessible claim ID, a dash or a hype word); they do not verify meaning, which is what the reviews were for. To challenge a number, find its claim ID in Appendix A and check the quote against the source.

Code under Apache-2.0; text, data and figures under CC BY 4.0.

## Appendix A. Cited evidence

{{T_evidence}}
