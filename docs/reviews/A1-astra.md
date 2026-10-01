# A1 review by Astra (gpt-6-astra via Codex CLI, read-only), 2026-10-01

Extracted from the JSON event stream (agent_message items); the -o file held only the last message.

Review complete. The sandbox is read-only, so these are the contents for `docs/reviews/A1-astra.md`. Earlier reviews and `docs/NEGATIVE-FINDINGS.md` remained unopened.

All eight LT2 model rows and every displayed Table 2 value match their ledger quotes and cached source. I found no misplaced-number extraction in those cells. The problems concern omitted evidence, coverage scoring, and conclusions drawn from the evidence.

**1. Section 5 · Incomplete results presented as complete**

**Exact sentence:** “We report its results in full rather than select from them.”

**Problem:** Table 2 includes every model row but only six of the source’s fifteen numerical columns. It omits SQuAD, Natural Questions, DROP, and the six in-distribution retrieval columns. The omission matters: on DROP, the dense loop’s 28.1 trails four models, including non-looped Mamba-2. The selected knowledge columns make its standing look more consistently strong.

**Evidence:** R6-018–R6-025 contain all fifteen values per row. The cached LT2 source lists all six knowledge benchmarks and all nine retrieval columns at [`2605.20670.txt:1460`](evidence/sources/R7/2605.20670.txt:1460). The omitted DROP values include 28.1 for Looped Transformer, 29.7 for Looped Mamba-2, and 30.2 for Full+GDN.

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Restore all columns, preferably in two tables. Alternatively, explicitly label Table 2 a selection and report the omitted benchmarks sufficiently to support the task-dependent conclusion.

**2. Summary answer 4 / Figure 1 · ReSSFormer is undercounted**

**Exact sentence:** “Of the 13 components, no row among the 15 we scored (one of them a union of looped-Transformer papers) fully has more than 6, and none fully has C10, C13 (Figure 1).”

**Problem:** ReSSFormer receives only partial credit for C2, “a sparse directed graph,” although its described computation meets that definition. Correcting this alone raises its full-component count from six to seven. The headline faithfully counts the CSV but does not faithfully represent the source.

**Evidence:** `evidence/coverage.csv:4` assigns C2=P. R6-007 states: “For each query q i q_{i} , only the k k highest-scoring keys are selected for attention computation.” The cached ReSSFormer §3.3 explicitly constructs a graph with an edge weight **from** token \(x_i\) **to** token \(x_j\); §3.4 places sparse selection and graph construction inside each recurrent iteration. See [`2510.01585.txt:1`](evidence/sources/R6/2510.01585.txt:1), §§3.2–3.4.

**Severity:** BLOCKER  
**Confidence:** CONFIRMED  
**Suggested fix:** Give C2 full credit under the stated definition, or document a substantive additional criterion and apply it consistently. Regenerate the count, figure, and Summary.

**3. Sections 4.4 and 6 · A cited hypergraph model already combines learned connectivity with recurrent message routing**

**Exact sentence:** “Also not found: learned hyperedges or evolving node roles combined with recurrent routing.”

**Problem:** The set-to-hypergraph paper does more than recurrently predict an unused output graph. Its learned incidence weights control messages between nodes and hyperedges during subsequent recurrent refinement. The broad absence claim is contradicted by this cited source. It could remain defensible only under a narrower definition such as *hard top-k routing without topology supervision*.

**Evidence:** R1-164 identifies the recurrent hypergraph refiner. Its source explicitly produces a new incidence matrix each step, aggregates neighboring edge features weighted by those incidence probabilities, performs the reverse node-to-edge aggregation, and shares parameters between refinement steps. See [`2106.13919.txt:361`](evidence/sources/R1/2106.13919.txt:361), especially lines 372–402.

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Credit recurrent, learned incidence-weighted routing as published. State precisely which harder combination remains unverified, and update the corresponding coverage cells.

**4. Figure 1 / Table 1 · The promised cell-level evidence is incomplete**

**Exact sentence:** “Each mark rests on a cited claim whose quote supports it; a question mark means we found no such claim in our ledger.”

**Problem:** Forty-six “no” cells have no claim ID. Some populated IDs do not support the assigned property. Thus “no” and “not established” are not consistently distinguished, and the figure cannot support strong absence conclusions as currently documented.

**Evidence:** Inspection of [`coverage.csv:2`](evidence/coverage.csv:2) through line 16 found 46 N cells with empty evidence fields. The looped-family C2=N cites R2-001, whose quote concerns Universal Transformers being Turing-complete under assumptions—not whether their graph is sparse.

The figure further broadens the bounded claim to “No system has more than 6 of 13” and “Fully present in no system,” despite its unknown cells: [`coverage.svg:3`](figures/coverage.svg:3).

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Supply source-backed negative classifications or change them to unknown. Qualify figure claims as properties established by this scoring exercise, not universal architectural absences.

**5. Figure 1 / Method · AUTHOR-CLAIM status disappears in coverage assertions**

**Exact sentence:** “Author claims are attributed, never stated as fact.”

**Problem:** The coverage table converts AUTHOR-CLAIM evidence into categorical or partial architectural assertions without preserving attribution. This violates the note’s stated evidence policy, even where the underlying architectural claim may ultimately be correct.

**Evidence:** `coverage.csv` uses AUTHOR-CLAIM R1-061 for Co-GNN C3, R6-010 for Discrete NAR C5/C6/C8, and R3-111 for CTM C12. R3-111 says, “The CTM can also leverage adaptive compute…”; the displayed cell simply says “partly.” Neither Table 1 nor its caption distinguishes author assertions from independently established design facts.

**Severity:** OPTIONAL  
**Confidence:** CONFIRMED  
**Suggested fix:** Preserve attribution/status in the figure’s evidence annotations, or reclassify individual claims only after documenting architectural verification.

**6. Section 2 · A fixed-depth comparison cannot identify recurrence as the sole cause**

**Exact sentence:** “Beating a fixed-depth Transformer would show only that recurrence helps.”

**Problem:** A recurrent learned-graph model differs from that baseline in recurrence, connectivity, and potentially other mechanisms. A win establishes the performance of the combined design; it does not isolate recurrence. This sentence also discounts the owner’s explicitly requested comparison without sufficient justification.

**Evidence:** [`BRIEF.md:21`](docs/BRIEF.md:21) asks whether the proposed architecture beats a conventional fixed-depth Transformer per stored parameter. The protocol itself separates T1-versus-T0 recurrence testing from G2-versus-T1 routing testing: [`PREREGISTRATION.md:102`](docs/PREREGISTRATION.md:102).

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** “Beating a fixed-depth Transformer would answer the brief’s performance question, but would not establish whether routing adds value beyond recurrence.”

**7. Section 4.4 · The dispersion theorem is broadened beyond its supported subject**

**Exact sentence:** “Soft attention provably disperses as the number of items grows (R6-001).”

**Problem:** The cached evidence concerns **softmax**, not every differentiable or “soft” attention mechanism. The next cited work explicitly describes dynamically sparse entmax attention avoiding the problem. The broader wording misstates what has been established.

**Evidence:** R6-001’s cached abstract attributes the limitation to “the softmax function”: [`2410.01104.abstract.txt:1`](evidence/sources/R6/2410.01104.abstract.txt:1). R6-016’s abstract states that dynamically sparse attention can avoid these issues through exact zeros.

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Say “The cited paper proves a dispersion limitation for softmax attention.” Since only the abstract is cached, avoid asserting the theorem’s unstated assumptions or universal scope.

**8. Section 4.4 · “Without any graph” obscures the actual distinction**

**Exact sentence:** “Sharper attention functions mitigate this without any graph: one reports up to 1000 times length extrapolation on synthetic tasks (R6-016), and a weight-tied Transformer with sharp, selective attention reaches 100% length generalisation on a lookup task (R6-012).”

**Problem:** The note already treats attention as graph message passing. ASEntmax creates content-dependent sparse support, while NDR’s authors explicitly describe their mechanism as neural routing. These are valuable controls, but “without any graph” makes them sound categorically unrelated to the hypothesis.

**Evidence:** R6-016 describes “dynamically sparse attention mechanisms” assigning exact zeros. R6-012’s cached abstract says its patterns are interpretable “as an intuitive form of neural routing”: [`2110.07732.abstract.txt:1`](evidence/sources/R6/2110.07732.abstract.txt:1). Section 2 invokes R4-070’s attention-as-message-passing interpretation.

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Distinguish hard top-k selection, sparse attention normalization, and an explicit graph data structure. Replace “without any graph” with the specific architectural distinction intended.

**9. Section 4.4 · The relational-transformer result is reduced to an input-feature explanation**

**Exact sentence:** “Second, edge features: a Transformer given edge states scores 81.30% against 42.34% without them on algorithm execution (R4-176).”

**Problem:** The numbers are correct, but “edge features” understates the tested mechanism. The stronger model uses relational attention and dynamically updated edge representations. This is relevant to the owner’s stateful relational-computation hypothesis, rather than merely showing that supplying extra input features helps.

**Evidence:** R4-176’s source says the ablation disables “edge vectors and features” and relational attention. A separate ablation retaining relational attention but disabling edge updates drops accuracy from 81.30% to 53.99%: [`2210.05062.r.txt:581`](evidence/sources/R4/2210.05062.r.txt:581), particularly lines 601–605.

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Describe the result as evidence for relational attention with evolving edge states. Preserve the distinction from hard top-k routing without presenting it as a simple static-feature effect.

**10. Section 4.5 · An implementation hypothesis becomes an efficiency verdict**

**Exact sentence:** “The case for the design therefore has to rest on inductive bias, not efficiency.”

**Problem:** Neither large-graph memory-bound measurements nor a random-edge tile-occupancy calculation establishes that the proposed architecture cannot improve efficiency. They constrain particular implementations and distributions. The section admits no measurement at the relevant sizes, but its heading and conclusion discard that qualification.

**Evidence:** R5-086 measures a particular GCN aggregation workload. R5-131 is DERIVED under uniformly random target assumptions; its notes explicitly say learned locality or clustering would change the result. The protocol requires selection/entmax calibration before compute statements: [`PREREGISTRATION.md:76`](docs/PREREGISTRATION.md:76).

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Label the performance prediction **HYPOTHESIS**. Say an efficiency benefit at these sizes has not been demonstrated and requires measurement; qualify the section heading likewise.

**11. Section 6 / proposed test · “No more compute” exceeds the protocol’s guarantee**

**Exact sentence:** “Not found in our search: learned, unsupervised top-k routing over all nodes inside a weight-tied loop, compared with both a dense and a sharpened looped Transformer and a fixed local graph, at equal steps and no more compute, on train-small, test-large problems.”

**Problem:** The protocol guarantees no more **matrix-multiply** compute than T1, not no more total compute than all comparators. Selection, normalization, memory movement, and training costs remain additional measurements. The purported open experiment and the published protocol therefore have different compute criteria.

**Evidence:** [`PREREGISTRATION.md:74`](docs/PREREGISTRATION.md:74) restricts the guarantee to matmul FLOPs versus T1. Lines 75–77 treat other costs as reported quantities and put FLOP matching in a secondary analysis. Section 7 itself correctly uses “matrix-multiply compute.”

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Use the narrower matmul guarantee consistently, or make a measured total-compute constraint part of the deciding experiment.

**12. Summary · The stated evidence needed to close answer 5 omits required controls**

**Exact sentence:** “A matched experiment in which learned routing beats both a dense and a sharpened looped Transformer on size extrapolation would revise answer 2; a published version of that experiment would close answer 5.”

**Problem:** Answer 5 explicitly includes looped recurrent controls, and Section 5 explains why they matter. The stated closing condition omits them. Such an experiment would provide useful evidence but would not close the question as formulated.

**Evidence:** Summary answer 5 names “looped recurrent controls.” [`PREREGISTRATION.md:121`](docs/PREREGISTRATION.md:121) says that without recurrent/hybrid controls, a win could reflect a different mixer outperforming a dense loop rather than routing.

**Severity:** MAJOR  
**Confidence:** CONFIRMED  
**Suggested fix:** Include the required recurrent and hybrid controls in the closing condition, along with the final matching criteria.

**13. Method · The forty-word quote invariant is false**

**Exact sentence:** “Every row holds one claim, the source URL, a locator, a verbatim quote of forty words or fewer that contains the number when there is one, a status, and the date read.”

**Problem:** Seven ledger quotations exceed forty whitespace-delimited words. This is an inaccurate reproducibility claim, independently of whether the scientific claims are correct.

**Evidence:** Direct counting in `evidence/claims.csv` gives R4-026: 44; R4-031: 46; R4-091: 42; R4-096: 45; R4-112: 42; R4-173: 44; R6-004: 56.

**Severity:** OPTIONAL  
**Confidence:** CONFIRMED  
**Suggested fix:** Bring the quotations within the stated limit or describe the actual policy and exceptions accurately.

**14. Sections 3 and 10 · Numerical provenance is overstated**

**Exact sentence:** “Every number in this note is filled by `paper/build_paper.py` from the ledger; the build fails on a typed number, an unknown or inaccessible claim ID, a dash or a hype word.”

**Problem:** The builder also draws numbers from coverage data, generated budgets, parameter configuration, and document counts. Some source-related numbers come from claim prose or derivation notes rather than quotations. Derived outputs need not occur in source quotes. The pipeline offers useful checks, but the stated provenance is stronger than its implementation.

**Evidence:** [`build_paper.py:4`](paper/build_paper.py:4) documents these multiple origins; lines 30–32 extract numbers from claim prose; line 66 reads derivation notes; lines 88–97 read generated budgets and parameters. R5-131’s numerical probability is absent from its quote because it is the project’s derivation.

**Severity:** OPTIONAL  
**Confidence:** CONFIRMED  
**Suggested fix:** Document separate provenance categories: quoted results, contextual claim fields, derivations, protocol constants, and inventory counts. Describe the guards as structural checks rather than semantic verification.

**15. Limitations · Abstract citations are counted as abstract-only access**

**Exact sentence:** “One closely related paper could be read only as an abstract, and 14 of the claims this note cites were read from abstracts only, including the dispersion theorem and the sharpened-attention results the protocol's main control relies on.”

**Problem:** The count of fourteen measures locators beginning with “Abstract,” not whether full text was available or consulted. It includes “Abstract; Section 1.” This cannot establish the claimed reading limitation.

**Evidence:** [`build_paper.py:130`](paper/build_paper.py:130) computes the count solely from the locator prefix. Included claims have cached full texts, including R6-006/ReSSFormer, R4-080/Saunshi, and R2-089/SMELT. R1-067’s locator is “Abstract; Section 1.”

**Severity:** OPTIONAL  
**Confidence:** CONFIRMED  
**Suggested fix:** Say “fourteen cited claims use abstract locators,” or calculate actual abstract-only access from explicit provenance metadata.

**16. Section 5 · Material inconsistencies in LT2’s source metadata deserve disclosure**

**Exact sentence:** “LT2 (arXiv 2605.20670) compares dense, sparse (learned top-k), recurrent and hybrid mixers inside the same weight-tied loop, at what the authors describe as the same parameter budget (R7-007, an author claim).”

**Problem:** Attribution of the matching claim is appropriate, but the source has unresolved inconsistencies concerning model size and hybrid composition. These do not invalidate the transcribed scores; they limit confidence in precise architectural and matching interpretations.

**Evidence:** In [`2605.20670.txt:1460`](evidence/sources/R7/2605.20670.txt:1460), the prose says 1.3B models and a 4:1 hybrid ratio. The Table 5 caption at line 1469 says 1.3B and 1:1. Its header at line 1473 says “Model (1.5B).”

**Severity:** OPTIONAL  
**Confidence:** CONFIRMED  
**Suggested fix:** Add a brief source-quality caveat. Retain attributed budget claims and refrain from resolving the conflicting specifications without additional evidence.

The five Summary answers consequently stand as follows:

| Answer | Assessment |
|---|---|
| 1 | Broadly supported for recurrence’s parameter-efficiency benefits; causal attribution for the complete graph design remains untested. |
| 2 | “Open” is justified. The LT2 numbers support task-dependent outcomes, subject to the table and source caveats above. |
| 3 | Supported as a result of the cited controlled study—not a universal storage-capacity law. |
| 4 | Requires correction: the six-component maximum is not defensible under the stated definitions. |
| 5 | A defensible proposed research question, but its closure conditions and compute constraint need alignment with the protocol. |

Novelty relative to earlier reviews was not assessed.

**Verdict: FIX**
