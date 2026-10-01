# N1 review: public note `paper/paper.md` (SR-2026-006 v0.1 draft)

Reviewer: fresh-context Claude Opus 5.5, adversarial. Date 2026-10-01.
Sections (a) to (e) were written before reading R1-opus.md, R2-opus.md, R3-opus.md or NEGATIVE-FINDINGS.md. Section (f) was added afterwards.
Every external quote below was fetched in this session. Anything not fetched is labelled "lead, unverified".

## (a) Verdict

**FIX-THEN-SHIP.** The note is honest in structure and well sourced. Even so, six substantive errors would be caught within minutes by a looped-Transformer or NAR expert:
- one misread scaling law;
- a false "does not test extrapolation" about the closest prior work;
- a "discrete selection helps" claim that the same table refutes;
- a figure caption ("scored only from quoted evidence") that many of its own cells do not meet;
- novelty statements that contradict the note's own Table 1 and ledger;
- two unattributed author claims.

All six can be fixed with text and re-scoring. No new research is needed.

## (b) BLOCKERS

### B1. §4.2: the recurrence-equivalence exponent is misread
- **Sentence:** "and one extra loop is worth r to the power 0.46 distinct blocks (R4-185)."
- **What is wrong:** φ describes the whole loop, not one extra iteration. Looping a block r times is worth r^φ distinct blocks. At r = 4 that is about 1.9 blocks for four iterations. The note's reading would make each added loop worth more than one distinct block whenever r > 1, which is the opposite of the paper's finding of diminishing returns.
- **Evidence:**
  - R4-185 quote: "L = E + A (Nonce + rφ Nrec )−α".
  - Fetched https://arxiv.org/abs/2604.21106: "φ tells us whether looping a block r times is equivalent in validation loss to r unique blocks of a non-looped model (full equivalence, φ=1) or to a single block run repeatedly with no capacity gain (φ=0)."
  - The ledger's own claim text ("one recurrence is worth r^0.46 unique blocks") carries the same error, so fix the ledger row too.
- **Fix:** "looping a block r times is worth about r^0.46 distinct blocks in language-model loss (φ = 0.46; φ = 1 would be full equivalence) (R4-185)."

### B2. Summary answer 2 and §5: LT2 is misdescribed, and the description shades it against the strongest counter-evidence
Four separate errors:
1. **"it does not test extrapolation" is false.**
   - LT2 tests length extrapolation on needle-in-a-haystack retrieval: models trained at 2048 tokens are tested at 4096.
   - Our own ledger: R7-010 "Looped Transformer … 100.0 100.0 0.0" and R7-011 "Looped Hybrid (GDN+DSA) … 100.0 100.0 91.4". R7-012 is an author claim that the hybrid "extrapolates substantially better at NIAH-4096".
   - Fetched Table 5 (https://arxiv.org/html/2605.20670) for NIAH-Single-1/2/3 at 4096: Looped Transformer "0.0 … 0.0 … 0.0"; Looped Hybrid (GDN+DSA) "91.4 … 77.6 … 60.3". The paper text says models "pre-trained at 2048 must extrapolate to 4096".
   - What is true: the state-tracking curriculum result is trained at size (R7-004), and the length extrapolation is on retrieval, not algorithmic size. Say exactly that.
2. **"at every loop count" is unsupported for the sparse arm.**
   - R7-005's "at any T" refers only to the dense plateau.
   - R7-006 says only that three variants "all reach stage 5". The fetched text adds: "Looped GDN+Window is the most dramatic: stage 3 at T≤4, stage 5 at T=8."
3. **"favours learned sparse routing" omits that a non-routing arm matches it.**
   - R7-006's own quote lists "Looped NSA, Looped GDN+Window, and Looped GDN+NSA". GDN+Window is gated linear attention plus a local window, with no top-k selection, and it also reaches 128.
   - The extrapolating NIAH arm is a linear-attention + top-k hybrid, not pure routing.
   - So LT2 shows that subquadratic mixers, including at least one with no routing, beat the dense loop. It does not isolate routing. This matters for the note's own locality point (R7-032/033).
4. **"One direct two-arm result" is wrong.** LT2 has at least five looped arms on this task (R7-005, R7-006).

Also, §5 cites R7-007 ("at the same parameter budget") without attribution. See B6.

- **Fix, Summary 2:** "Open. LT2 finds that several subquadratic looped mixers, including learned top-k sparse attention and also a linear-attention-plus-window variant without routing, double the largest trained-at-size state-tracking problem solved by a dense loop (128 vs 64). A sparse/linear hybrid also length-extrapolates on retrieval where the dense loop scores 0. It has no sharpened-attention control, is not compute-matched, and does not isolate routing."
- **Fix, §9 strongest case:** name the NIAH extrapolation result explicitly. It is the strongest counter-evidence in the ledger, and the note currently says it does not exist.

### B3. §4.4: "Discrete selection helps when supervised" is refuted by the same table
- **Sentence:** "Discrete selection helps when supervised: a max-aggregation network scores 99.80% on reachability at test size against 91.51% for full attention (R4-001, R4-002)."
- **What is wrong:**
  - GAT-full attends over the complete graph, while MPNN-max uses the task's edges, so the comparison confounds graph structure with the aggregator.
  - The same Table 1 has soft attention on the task's edges (GAT*), and it scores higher than max at 100 nodes.
- **Evidence:** fetched https://arxiv.org/abs/1910.10593 (PDF Table 1):
  - Caption: "GAT* correspond to the best GAT setup as per Section 3 (GAT-full using the full graph)."
  - Rows: "GAT* (Veličković et al., 2018) 93.28% / 99.86% 93.97% / 100.0% 92.34% / 99.97%" and "MPNN-max … 99.92% / 99.80%".
- **Fix:** "Restricting attention to the task's own edges helps when supervised: soft attention on the input graph reaches 99.97% last-step reachability at 100 nodes (trained at 20), against 91.51% for attention over the complete graph. Max aggregation on the same edges reaches 99.80% (R4-001, R4-002, plus a new ledger row for GAT*)." This actually supports the given-graph arms (G0/G1), not learned routing. Say so.

### B4. Figure 1 caption and Summary answer 4: "Scored only from quoted evidence" is not true for many cells
Many Y/P cells cite a claim whose quote says nothing about the component (full list in (e)). Examples:
- **Mixture-of-Recursions C3 and C4 = Y** cite R2-026. That is an author claim about a Pareto frontier ("MoR forms a new Pareto frontier: at equal training FLOPs…"), with no mention of weight sharing.
- **MoR C12 = Y** cites R2-022, a few-shot accuracy result ("surpasses the vanilla baseline … (43.1% vs. 42.3%)").
- **Looped Transformer C8 and C13 = P** cite R2-001, which is about Turing completeness. **C10 = P** cites R2-020, about collapsing adaptive exits, not distributed readouts.
- **Looped Transformer C11 = Y** cites R2-109 (arXiv 2607.14427). That is a fifth system, not UT, Huginn, Ouro or Parcae as the row label says.
- **HRM/TRM C10 = P** cites R2-048 (outer refinement loop), which is not readouts across regions.
- **Discrete NAR C1 = Y** cites R6-010 (hard attention). The quote says nothing about persistent node states.

The "Looped Transformer (UT, Huginn, Ouro, Parcae)" row also pools features from at least five papers. It is a family composite, not a system. That makes "No system has more than 6 of 13" partly an artifact: pooling raises a family's count, and splitting it would change which row reaches 6.

- **Fix, two options:**
  - (a) Re-score every cell from a claim whose quote names the component, add ledger rows where needed, and split or relabel the composite row as "family (union of N papers)".
  - (b) Change the caption to "scored by the researchers from their dossiers; the claim IDs are the nearest supporting rows, not always proof of the component", and soften Summary 4.
  - Option (a) is preferable for a note that sells provenance.

### B5. Summary 4, §6 and the figure title: novelty and absence statements contradict the note's own table and ledger
1. **"The architecture is not new."**
   - The note's own §6 lists "Not found in our search: learned, unsupervised top-k routing over all nodes inside a weight-tied loop … learned hyperedges … any mechanism by which node roles evolve". The Summary also says C7 and C13 are fully present in no system.
   - The correct claim is narrower: "most of its components are published separately; the specific combination is not found in our search, and most of its parts are prior art". "Not new" asserts that a combination exists, which the note says it did not find.
2. **"any mechanism by which node roles evolve during computation" (§6, not found).**
   - Table 1 scores C13 as "partly" for Co-GNN, N2, MoR, PGN/NEE and looped Transformers.
   - R1-059 (Co-GNN): "an action network π predicts, for each node v, a probability … distribution … over the actions {S, L, B, I} … given its state and the state of its neighbors". Per-node, per-layer, state-conditioned listen/broadcast/isolate roles are evolving node roles.
3. **"learned hyperedges used as a computing substrate" (not found), and "no system fully has C7".** The ledger contains learned and iteratively refined hyperedges:
   - R1-109 (DyHSL "explicitly learns the structure of the hypergraph");
   - R1-164 ("a simple recurrent neural network that refines the edge and node features, based on wich it predicts the incidence matrix");
   - R1-108 (LFH, implicit hyperedges);
   - matrix row A1-23, "Learned hyperedges".

   Figure 1 includes no hypergraph system, so "no system fully has C7" follows from row selection, not from the literature.
- **Fix:**
  - Summary 4: "Most components are published, but separately. No system in our table has more than 6 of 13, and the full combination was not found in our search."
  - §6: change the C13 line to "per-node, state-conditioned roles exist (Co-GNN, R1-059), but not inside a weight-tied loop with routing". Change the hyperedge line to "learned hyperedges exist (R1-108, R1-109, R1-164) but not combined with recurrent routing", or add a hypergraph row to Figure 1 and re-derive `never_y`.

### B6. §2 and §5: author claims stated as fact, against the note's own rule in §3 ("Author claims are attributed, never stated as fact")
- **§2:** "A Transformer already is message passing on a complete graph whose attention routes information by current state (R4-070, an author claim; R1-099)."
  - R1-099 is also AUTHOR-CLAIM and is not attributed.
  - R1-099 and R4-070 are the same paper (arXiv 2506.22084), cited as if they were two sources.
  - The sentence asserts the claim in the note's own voice.
- **§5:** "inside the same weight-tied loop and at the same parameter budget … (R7-005, R7-006, R7-007)". The parameter match rests only on R7-007, an AUTHOR-CLAIM, and it is not attributed. The Summary carries the same claim implicitly.
- **Fix:**
  - §2: "Self-attention can be written as message passing on a complete token graph (Joshi 2025, R4-070; the same paper, R1-099)", or cite the identity directly.
  - §5: "at what the authors describe as the same parameter budget (R7-007, an author claim)".

## (c) MAJOR

**M1. Summary answer 1 over-answers.**
- "Against a fixed-depth Transformer, per stored parameter: yes" answers a question about the proposed graph, but no cited evidence tests a graph.
- R2-016 and R4-080 are looped Transformers. R4-080 is an author claim, yet answer 1 states it as fact.
- Fix: "Recurrence does, per stored parameter (looped language models report 2 to 3 times, R2-016). There is no evidence that the graph adds to it, and a looped Transformer already has this gain."

**M2. §4.1: "the training loop, not the structure, supplied the gain" misnames what was shown and drops the residual gap.**
- Fetched https://arcprize.org/blog/hrm-analysis: "The 'hierarchical' architecture had minimal performance impact when compared to a similarly sized transformer", and "The under-documented 'outer loop' refinement process drove substantial performance gains".
- It is the outer refinement loop plus augmentation, not "the training loop".
- HRM still leads by about 5 points, so "not the structure" is too strong.
- Fix: "the hierarchical structure added about 5 points at most; the outer refinement loop drove most of the gain (R4-165, R2-048)."

**M3. §4.4: "Sharpening fixes this" overstates.**
- Fetched https://arxiv.org/abs/2410.01104: the authors "propose adaptive temperature as an ad-hoc technique for improving the sharpness of softmax at inference time".
- ASEntmax is not softmax. Its "up to 1000×" is on synthetic tasks (R6-016).
- Fix: "Sharper attention functions mitigate it without any graph: …"

**M4. §4.1: R4-024's 97.12% is a peak over test-time iterations, chosen after the fact.**
- The ledger note on R4-024 says so. That is the same oracle stopping step the note's §8 calls an error in its own design.
- "Solves 512-bit strings at 97.12%" hides this.
- Fix: "reaches a peak of 97.12% (best over test iterations) on 512-bit strings".

**M5. §4.5: the long-context counter-examples are block-structured.**
- NSA is blockwise top-k (R5-017 claim: "trainable blockwise top-k"), MoBA selects blocks, and Quest selects KV pages.
- They pay off because selection is coarse and contiguous. That is the opposite of the unstructured per-node top-k that R5-131 shows yields no empty tiles.
- "The picture reverses, and sparse top-k attention does pay" invites the wrong inference.
- Fix: "block- or page-structured top-k attention does pay at long context (…); unstructured per-node top-k is not shown to."
- Also mark "dense masked attention is likely the fastest" as our inference: no cited measurement compares them at these sizes.

**M6. §4.2: "but matched on parameters only" is the wrong description of R2-016.**
- The comparison is at unequal parameters (1.4B vs 4B). The 2 to 3 times is a per-parameter efficiency, not a parameter-matched result.
- "About 1.4 times" holds only for 1.4B vs 4B (R2-199: 5.6/4). For 2.6B × 4 vs 8B it is about 1.3×. R2-199 also ignores attention terms and early exit (its own note).
- Fix: "measured per stored parameter, not per unit of compute; by our derivation the 1.4B model spends about 1.4 times the forward compute of its 4B comparator, ignoring attention and early exit (R2-199)."

**M7. §4.2: "looping saves 6.8 to 18.0%" generalises one study.**
- R2-089 (SMELT) loops the middle layers of an MoE model twice.
- Fix: "One study looping the middle layers of a mixture-of-experts model, with parameters, per-token compute and KV cache all matched, saves …"

**M8. Storage: one study is turned into a law.**
- §2 says "recurrence cannot raise it" and §6 says "Established: recurrence adds computation but not storage". Both rest on R2-017 alone (Ouro; per the prereg, R4-184 is the same study).
- "Whatever the graph adds, it adds computation, not memory" extrapolates from looped Transformers to a design that includes C9, persistent associative memory.
- Fix: "One controlled study finds …", and move this item from "Established" to "reported".

**M9. §3: "81 rows say unknown" is mislabelled.**
- `build_paper.py` counts values starting with "unknown" or "n/a". By my count, 62 rows say unknown and the rest say n/a or N/A.
- Fix: "62 say unknown and 19 say not applicable", or relabel the placeholder.

**M10. §7: "All looped arms share one recipe, so routing is the single trained difference" is not true per the protocol.**
- PREREGISTRATION "Open before freeze" item 1: "ASEntmax adds learned parameters and an explicit log n size signal to T1-sharp".
- G3 adds a halting head and a ponder cost. G1 uses the task adjacency mask.
- Fix: "All looped arms share one training recipe; they differ only in the attention or routing operator (and, for the halting arm, a halting head)."

**M11. §4.4, Discrete NAR: "its routing is supervised and follows the task's own edges" cites no claim.**
- R6-010 and R6-011 say neither. "Trained on graphs of 16 nodes" is "at most 16" in the claim text, and the number is not in R6-011's quote, which covers the test set only.
- Fix: add a ledger row with a quote, or hedge.

## (d) MINOR / wording

1. **§4.4 "Per-query top-k attention was introduced in 2019 (R6-008)":** an unchecked priority claim. Lead, unverified: earlier sparse top-k memory reads, such as Rae et al. 2016 (Sparse Access Memory, arXiv 1610.09027) and Sparse Attentive Backtracking (2018). The SAM abstract I fetched does not itself say "top-k". Say "was published by 2019".
2. **§1 "twenty neural-network families":** typed, not generated. The matrix has 23 family codes. Generate it, or say "the brief's families".
3. **§1 "121-row matrix answering fourteen fixed questions":** add "partly" (as §3 does), because the Summary is often read alone.
4. **§4.1 R1-029 "collapses":** the source says "accuracy declines rapidly". Also give the scale (graphs of size 10).
5. **§4.4 R4-176:** add "out of distribution, on 8 CLRS algorithms".
6. **§4.4 R1-067 "state-conditioned pathways":** the quote says "displacements of graph nodes and pseudo nodes"; "state-conditioned" is our reading. Say "dynamic pathways (its authors' term)".
7. **§4.5 R5-131 "under stated assumptions":** the assumption (uniformly random targets) is not stated in the note. State it in one clause.
8. **§4.5 R5-049 "Standard FLOP counters":** one counter (PyTorch's) was checked. Say "PyTorch's FLOP counter".
9. **§7 tasks: "mazes with and without cycles":** cyclic mazes (percolation 0.3) are a test-only structure shift, not a train-small/test-large ladder. Say so.
10. **§7 budget:** reachability peaks at 57 steps (724 nodes), not at 1024. "From 12 to 56" is literally true but reads as monotone. Also, the prereg is a DRAFT awaiting approval. "Preregistration-ready" is fine, but add "not yet frozen".
11. **§9 "the design's core bet is right":** too strong. LT2 surviving the controls would support routing inside a loop, not the 13-component design.
12. **§10 "Every number in this note is filled by build_paper.py":** "twenty" and "fourteen" are typed numbers in words. The build check evidently only catches digits.
13. **AI disclosure:** adequate and prominent. Add one clause: "quotes and source readings were made by AI agents and have not been checked by a human."
14. **Missing but in the ledger:** R7-013 (arXiv 2609.39892, looped Transformers on graph walks: "the hidden state can control shared computation, with attention routing as a causal pathway", an author claim). It belongs in §5 or the novelty map. The sparse UT / MoEUT family (R2-180) is closer to the design than Graph Neural Cellular Automata and is absent from Figure 1.
15. **Table 1:** "not established" vs "no" is explained only in the SVG footnote. Add one line under Table 1.

## (e) Audit tables

### Citation audit (every claim ID in the prose, §1 to §9)

| ID | § | supports? | note |
|---|---|---|---|
| R4-070 | 2 | partial | AUTHOR-CLAIM, attributed, but the sentence then asserts it as fact |
| R1-099 | 2 | partial | AUTHOR-CLAIM, unattributed; same paper as R4-070 (B6) |
| R4-024 | 4.1 | partial | numbers exact; "peak" over test iterations omitted (M4) |
| R1-027 | 4.1 | Y | "1,000 times larger" |
| R1-029 | 4.1 | Y | "declines rapidly" softened to "collapses"; graph size 10 omitted |
| R4-080 | 4.1 | Y | attributed |
| R4-165 | 4.1 | partial | the 5-point gap is right; "training loop, not structure" needs R2-048 and is overstated (M2) |
| R2-016 | 4.2 | partial | "matched on parameters only" mis-describes it (M6) |
| R2-199 | 4.2 | partial | DERIVED; 1.4× for 1.4B only; ignores attention (M6) |
| R2-089 | 4.2 | partial | one MoE study generalised (M7) |
| R5-092 | 4.2 | Y | exact |
| R4-185 | 4.2 | **N** | φ misread (B1) |
| R2-018 | 4.2 | Y | |
| R2-095 | 4.2 | Y | |
| R2-017 | 1, 4.3 | Y | one study; "cannot" (§2) and "established" (§6) too strong (M8) |
| R6-008 | 4.4 | partial | "introduced" is a priority claim (d1) |
| R6-006 / R6-007 | 4.4 | Y | |
| R1-067 | 4.4 | partial | "state-conditioned" is our gloss (d6) |
| R6-010 | 4.4 | Y | attributed |
| R6-011 | 4.4 | partial | training size not in the quote; "supervised, task edges" uncited (M11) |
| R6-001 | 4.4 | Y | theorem |
| R6-016 | 4.4 | partial | "fixes" too strong (M3) |
| R6-012 | 4.4 | Y | |
| R4-001 / R4-002 | 4.4 | **N** for the inference | numbers exact; the conclusion is refuted by GAT* in the same table (B3) |
| R7-032 / R7-033 | 4.4 | Y | |
| R4-176 | 4.4 | Y | add OOD and CLRS-8 |
| R5-086 | 4.5 | Y | GCN aggregation, memory-bound |
| R5-131 | 4.5 | Y (DERIVED) | the assumption should be stated in text |
| R5-049 | 4.5 | partial | one counter, not "standard counters" |
| R5-017 / R5-041 / R5-042 | 4.5 | partial | all block- or page-structured (M5) |
| R7-004 | 5 | Y | the curriculum result is trained at size; but the NIAH extrapolation exists (B2) |
| R7-005 | 1, 5 | Y | "at any T" is for the dense arm only |
| R7-006 | 1, 5 | partial | lists GDN+Window (no routing) too; does not say "every T" (B2) |
| R7-007 | 5 | partial | AUTHOR-CLAIM, unattributed (B6) |

### Coverage-cell audit (34 cells)

| system | comp | cell | verdict | note |
|---|---|---|---|---|
| Looped T (composite) | C1 | Y (R2-001, R2-007) | OK | |
| Looped T | C4 | Y (R2-001, R2-006) | OK | R2-006 (truncated backprop) is irrelevant |
| Looped T | C8 | P (R2-001) | **unsupported** | Turing-completeness quote |
| Looped T | C10 | P (R2-020) | **unsupported** | collapsing-exit quote, not readouts |
| Looped T | C11 | Y (R2-013, R2-109) | OK, but | R2-109 is a fifth system outside the row label |
| Looped T | C12 | Y (R2-003, R2-020) | OK | UT ACT; R2-003 is an author claim |
| Looped T | C13 | P (R2-001) | **unsupported** | |
| LT2 | C2 | P (R7-002) | OK | causal top-w |
| LT2 | C6 | Y (R7-002) | OK | |
| LT2 | C8 | Y (R7-002) | OK | consistent with top-k changing edges |
| LT2 | C11–C13 | ? | OK | "?" rule applied consistently |
| ReSSFormer | C5 | Y (R6-006) | OK | "recurrent … bounded depth" |
| ReSSFormer | C8 | Y (R6-007) | OK | |
| MoR | C1 | P (R2-022) | **unsupported** | accuracy quote |
| MoR | C2 | P (R2-025) | **unsupported** | load-imbalance quote |
| MoR | C3 / C4 | Y (R2-026) | **unsupported** | Pareto author claim; sharing is true of MoR but not shown by the quote |
| MoR | C6 | P (R2-025) | OK | router choice, reasonable P |
| MoR | C12 | Y (R2-022) | **unsupported by the quote** | the router-chosen depth is plausibly Y, but cite R2-022's design rows, not an accuracy number |
| HRM/TRM | C1 | Y (R2-031, R2-043) | weak | memory-footprint quotes |
| HRM/TRM | C2 | N (R2-038) | OK | dense mixer |
| HRM/TRM | C3 | Y (R2-039) | weak | "2 layers" quote does not show sharing |
| HRM/TRM | C10 | P (R2-048) | **unsupported** | outer refinement loop, not readouts |
| HRM/TRM | C11 | Y (R2-032) | generous | Q-halting head; P more apt |
| N2 | C8 | Y (R1-067) | generous | displacement quote; P more apt |
| Co-GNN | C13 | P (R1-059) | OK | and contradicts §6 "no mechanism" (B5) |
| Co-GNN | C8 | Y (R1-059) | OK | |
| IterGNN | C12 | P (R1-022) | **understated** | "adaptively adjust the number of iterations … without any supervision of the stopping condition" is learned halting: Y |
| IterGNN | C2 | P (R1-022) | weak | input graph; the quote is about halting |
| Discrete NAR | C1 | Y (R6-010) | **unsupported** | hard-attention quote |
| Discrete NAR | C3 / C4 | ? | OK by rule | likely Y on fuller reading |
| PGN/NEE | C5 | ? | understated | PGN iterates per operation; 0/13 undersells it |
| CTM | C4 | N (R3-098) | OK | per-neuron private weights |
| CTM | C10 | Y (R3-099, R3-161) | generous | synchronisation readout; P more apt |
| Energy T | C9 | Y (R3-011, R3-015) | OK | Hopfield module |
| Energy T | C12 | P (R3-011) | generous | a fixed-point stop is not learned halting |
| GNCA | C2 | Y (R3-089) | OK | "arbitrary graphs" |

**Title check.** The counts are right as scored: the maximum Y count is 6 (Looped T composite, LT2, HRM/TRM, Energy T), and C7 and C13 have no Y. But:
- re-scoring the unsupported cells changes MoR and the composite;
- correcting IterGNN C12 raises IterGNN to 6;
- the C7 claim depends on excluding the hypergraph systems in the ledger (B5);
- "?" vs "N" is used consistently with the footnote rule ("?" for rows scored only from their own quoted rows).

## (f) Overlap with earlier rounds (read after (a) to (e))

- **B1 (φ) repeats R3 (d).** R3 flagged "R4-185 is misparaphrased" as minor, but it survived into the public note and the ledger claim text. Raised to blocker here because the note is public and the error inverts the finding's direction.
- **M4 (DT-Recall peak) repeats R1 (e), R2 B3 and R3 (e).** All three said the peak was post hoc and "disclosed". The disclosure did not reach the note.
- **M10 (single trained difference) repeats R3 M5.** It was accepted in the prereg's "Open before freeze" list, but the note's sentence was not updated.
- **B6 (R4-070 / R1-099 author claims) partly repeats R3 (d).**
- **B5 / §6 node roles and hyperedges** relate to R2 (d10) and R3 (f) ("disclosed as dropped"). The new point is that the note now claims absence, which its own table and ledger contradict.
- **B3** extends R2 (e) ("GAT-full is also step-supervised"). The GAT* row that refutes the inference is **new**.
- **M2** relates to R1 (B1), which cites R4-165 on the other side; the misnaming of the loop is **new**.

**New in N1:** B2 (LT2 does test extrapolation; GDN+Window matches without routing), B3's GAT* refutation, B4 (coverage cells not supported by their quotes; composite row), B5 (internal contradictions), M3, M5, M6, M7, M8, M9, M11.

**Counts checked:** 11 blockers across R1 to R3 (4 + 4 + 3) and 28 dated NEGATIVE-FINDINGS rows both match the note.
