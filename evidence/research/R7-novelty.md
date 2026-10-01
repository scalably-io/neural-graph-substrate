# R7 — Novelty sweep in Transformer vocabulary (2026-10-01)

Claims: `R7-novelty.csv` (R7-001…R7-051, validator 0 rejects). Downloads: `evidence/sources/R7/`.

## (a) Verdict: partially found

**Our full comparison was not found in our search, but half of it has been published.** That half is a weight-tied loop with learned top-k sparse attention against a dense looped Transformer, at equal loop count and parameters. It appears in **LT2: Linear-Time Looped Transformers (arXiv 2605.20670, May 2026)**:

- On a synthetic state-tracking + recall task, the dense Looped Transformer plateaus at n_max = 64 at every T (R7-005).
- Looped NSA, which uses learned top-w block selection, reaches n_max = 128 "at the same parameter budget" (R7-006, R7-007).

**The gap.** LT2 does not run our three-arm, extrapolation test:

1. **No size extrapolation.** n_max is the largest curriculum stage the model is trained on and then solves (R7-004). LT2's only length-extrapolation result is NIAH 2048 → 4096. There the sparse arm is a GDN + DSA hybrid, so linear attention confounds it (R7-010, R7-011, R7-012).
2. **No sharpened-attention arm.** There is no entmax, ASEntmax or temperature arm.
3. **No FLOP matching.** The sparse arms spend fewer attention FLOPs, so the arms are not matched on FLOPs.
4. **Different routing.** Routing is causal block or token top-w over the prefix. It is not a per-step graph over all nodes on a non-causal algorithmic instance. We did not confirm whether DSA's indexer gets an auxiliary loss in LT2.

**What a reviewer would say.** A reviewer would not call our study a replication of LT2. They would expect us to:

- cite LT2 as prior evidence that learned sparse routing inside a loop can beat dense looping in-distribution;
- reframe our contribution as the size-extrapolation, sharpened-baseline, FLOP-capped test.

The §0.4 sentence in SYNTHESIS.md therefore needs one qualifier: "a two-arm, in-distribution version exists (LT2, R7-006)".

## (b) Closest works, scored

✓ = yes; ✗ = no; ~ = partial; ? = not stated in the text we read. Ledger rows that were already present are cited by ID and were not re-added.

| # | Work | Weight-tied loop | Learned top-k over all tokens | Unsupervised routing | Size/length extrapolation | Dense looped baseline | Sharpened baseline | Param-matched | FLOP-matched |
|---|---|---|---|---|---|---|---|---|---|
| 1 | LT2 (2605.20670) R7-001…012 | ✓ | ✓ causal top-w (NSA/DSA) | NSA ✓ / DSA ? | ~ (NIAH 2×, hybrid only) | ✓ | ✗ | ✓ | ✗ (sparse uses fewer) |
| 2 | ReSSFormer (2510.01585) R6-006/007 | ✓ recurrent unit | ✓ per-query top-k | ✓ | ✗ | ✗ | ✗ | ? | ? |
| 3 | Discrete NAR (2402.11628) R6-010/011 | ✓ recurrent processor | ✗ (hard attention over task-graph neighbours) | ✗ (hint-supervised) | ✓ 16 → 1600 nodes | ✗ | ✗ | ? | ? |
| 4 | Neural Data Router (2110.07732) R6-012 | ✓ | ✗ (geometric attention = sharpened) | ✓ | ✓ length | ✓ (UT-style) | ~ (it is the sharpened arm) | ? | ? |
| 5 | ASEntmax (2506.16640) R6-003/016 | ✗ | ✗ (adaptive entmax) | ✓ | ✓ up to 1000× | ✗ | ✓ | ? | ? |
| 6 | WISE (2609.27373) R7-016…018 | ✓ | ~ (training-free block working set) | n/a | ✗ | ✓ (vs itself, full attention) | ✗ | ✓ | n/a |
| 7 | Graph Machine (2608.06834) R7-026…029 | ? (layers; tying not seen) | ✗ (soft, sharpened edges; top-s only simulated) | ✓ | ✗ (fixed Sudoku) | ✗ | ~ (learned edge sharpener) | ✗ | ✗ |
| 8 | MoSA (2505.00315) R7-019…021 | ✗ | ✓ (expert-choice top-k) | ✓ | ✗ | ✗ | ✗ | ~ | ✓ isoFLOP |
| 9 | UT for Circuit Computations (2608.31067) R6-013 | ✓ | ✗ (masked hard attention, constructed) | ✗ | ✓ length | ? | ✗ | ? | ? |
| 10 | Wu et al., "Shared Weights, Selected Computations" (2609.39892) R7-013…015 | ✓ | ✗ (dense; analysis) | n/a | appendix depth extrapolation | n/a | ✗ | n/a | n/a |

**The three closest:**

1. **LT2**: shares the arms and the loop, but lacks extrapolation, the sharpened arm and FLOP matching.
2. **ReSSFormer**: has the recurrence and top-k, but no looped baseline and no extrapolation.
3. **Discrete NAR**: has hard selection in a loop and size extrapolation, but its routing is supervised, over given edges, with no Transformer baselines.

**Context rows.** Several rows explain why the sharpened arm is mandatory:

- R7-039: layer norm after attention also fixes dispersion.
- R7-041: entmax kernels length-generalize.
- R7-037/038: theory says k-sparse dependence suffices for length generalization.
- R7-035: UT authors suspect dense-softmax noise.

Other rows bear on the step budget or the competing explanations:

- R7-014: dense loops already route implicitly, so one loop is not one hop.
- R7-032/033: a causal-conv locality prior alone takes TRM from 45.8% to 91.4% at 4× length. A reviewer may name this as a competing explanation.

## (c) Query log (all 2026-10-01)

**WebSearch, 22 queries.** Each line gives the query, then the notable hits.

1. looped transformer top-k attention length generalization: 2409.15647, 2609.33144, 2608.31067, 2604.15259
2. universal transformer sparse attention size generalization algorithmic tasks 2025: SUT 2310.07096, 2506.16640, 2605.31423
3. weight-tied transformer hard attention extrapolation graph algorithms arXiv: 2601.05770, 2603.17063
4. "looped transformer" entmax OR sparsemax length extrapolation: 2506.16640, 2603.23998, 2606.29983 (no looped + entmax paper)
5. "dynamic sparse attention" algorithmic reasoning length generalization: 2510.17196, 2601.22766, 2506.08889
6. recurrent depth transformer learned sparse graph per step routing tokens extrapolation: MoR, 2607.14427, 2603.21676, 2605.05222, 2608.15062
7. "top-k attention" looped OR recurrent transformer CLRS size generalization: 2607.15456, 2106.06899, 2604.01577
8. neural algorithmic reasoning transformer sparse attention OOD larger graphs 2025: 2402.11628, 2510.01585, 2406.09308, 2506.20575
9. "selective attention" OR "gated attention" length extrapolation 2025: 2410.02703, 2505.06708, FoX
10. attention as dynamic graph rewiring looped transformer length generalization learned adjacency: 2609.33144, Graph-aware isomorphic attention (AIP)
11. "k-NN attention" OR "kNN attention" generalization theory top-k: KVT, kNN Attention Demystified (ICLR 2025), 2512.07647
12. routing transformer clustered attention recurrent UT algorithmic extrapolation: 2003.05997, 2609.19521
13. "The Role of Sparsity for Length Generalization in Transformers": 2502.16792
14. recurrent transformers dynamic halt ListOps length generalization: 2402.00976
15. openreview ICLR 2026 looped transformer sparse attention graph algorithm larger graphs: 2402.01107, 2608.18230, 2602.19143
16. tiny recursive model OR HRM sparse attention maze larger grids extrapolation: 2605.20784, 2602.12078 (no sparse-routing arm)
17. "mixture of sparse attention" expert-choice routing: 2505.00315
18. looped transformer graph connectivity shortest path larger graphs learned attention: 2402.01107, 2502.08794
19. looped transformer attention temperature sharpening extrapolation dispersion: 2606.29983, Awesome-Loop-Models catalogue
20. "looped" transformer "sparse attention" sudoku OR maze OR graph 2026: 2604.15259, 2606.18206, 2604.21254, **2608.06834**
21. transformer learns graph each layer top-k neighbours "learned adjacency" extrapolation: 2510.25542, 2510.19753
22. ICML 2026 / NeurIPS 2025 / CLRS sparse top-k (3 queries): 2603.02238, MoSA, 2606.06467, 2508.06016
- Also searched: "ChainGPT" Dual-Reasoning…, and "MoDr" Mixture-of-Depth-Recurrent.

**arXiv API (export.arxiv.org), 40 abstract queries.** Hits by query:

- `"looped transformer" AND sparse`: **2605.20670 (LT2)**, 2609.27373, 2609.29812, 2609.35751, 2609.01343
- `"looped transformer" AND "top-k"`: 0 hits
- `"looped transformer" AND "hard attention"`: 0 hits
- `"looped transformer" AND graph AND generalization`: 2609.33144, 2501.10688, **2609.39892**
- `"universal transformer" AND sparse`: 2310.07096, 2604.25930, 2605.31423
- `"universal transformer" AND "length generalization"`: 0 hits
- `"recurrent depth" AND attention AND extrapolat*`: 0 hits
- `"weight-tied" AND attention AND "length generalization"`: 0 hits
- `"top-k attention" AND generalization`: 2602.01219, 2601.22766, 2512.07647
- `"top-k" AND attention AND "length generalization"`: 2410.01651, 2504.16795
- `entmax AND "length generalization"`: 2601.22766
- `sparsemax AND extrapolation`: 0 hits
- `"hard attention" AND "length generalization"`: 2608.31067, 2511.20038, 2602.07599
- `"hard attention" AND "size generalization"`: 0 hits
- `"neural algorithmic reasoning" AND transformer AND attention`: 0 hits
- `"neural algorithmic reasoning" AND sparse`: 1 irrelevant hit
- `"learned graph" AND transformer AND iterative`: 2406.04090
- `"dynamic graph" AND "looped"`: no relevant hits
- `"recurrent" AND "top-k attention"`: 0 hits
- `"latent graph" AND "algorithmic reasoning"`: 0 hits
- `"depth-recurrent" AND graph`: 2603.21676
- `"looped" AND "attention" AND "maze"`: no relevant hits
- `"recurrent transformer" AND "size generalization"`: 0 hits
- `"pointer" AND "looped transformer"`: 2605.30757
- `"routing" AND "universal transformer"`: 2604.25930
- `"relational transformer" AND recurrent AND CLRS`: 0 hits
- `"graph transformer" AND CLRS AND attention`: 0 hits
- `"recurrent memory transformer" AND algorithmic`: no relevant hits
- Second batch:
  - `recurrent AND "hard attention" AND algorithm`: 0 hits
  - `"top-k" AND recurrent AND extrapolat`: 0 hits
  - `"weight sharing" AND "sparse attention" AND reasoning`: 0 hits
  - `k-nearest graph each layer recompute`: 0 hits
  - `"latent graph" AND transformer AND recurrent`: 2601.09775
  - `looped AND sparse AND routing`: 2606.04438, 2609.35751
  - `recursive AND "sparse attention" AND reasoning`: 2510.01585
  - `"neural execution" attention mask`: 0 hits
  - `attention dispersion/dilution AND length`: 2607.18759
  - `sharpen AND attention AND "length generalization"`: 2510.27015
- Plus the remaining queries in the same families. The raw JSON is kept in `/tmp/r7` only and was not saved to the repo.

**Semantic Scholar API, 16 query attempts.** Most returned 0 because of rate limiting (HTTP 429), so treat these as failed, not as negatives. Two succeeded:

- "looped transformer sparse attention length generalization": 2510.17196, 2510.00258, 2504.02827, 2605.18797, 2502.16792
- "entmax looped transformer": loop-model papers only; none combines loops with entmax.

**Catalogue sweep.** We cloned the `huskydoge/Awesome-Loop-Models` repository (250 paper YAMLs, built 2026-10-01). We grepped it for top-k, sparse attention, hard attention, entmax, sparsemax, kNN, learned graph, dynamic graph, rewiring, adjacency, argmax, Gumbel and routing:

- The only token-routing loop papers are LT2, WISE, FlashLoop and ChainGPT.
- Every other routing hit is MoE or depth routing (MoR, LoopMoE, Foil, MoDr, T-LoopFormer).

**Already in the ledger, so not re-added.** These came up in the searches above: 2609.33144, 2603.21676, 2501.10688, 2310.07096, 2603.23998, 2607.14427, 2406.09308, 2402.01107, 2412.04703, 2510.04871, 2512.11847, 2607.16051, 2510.19753.

## (d) Unconfirmed leads (not read at primary full text)

- **ChainGPT (ICLR 2026).** Its "state-guided sparse attention" is described only in the abstract (R7-024). Secondary summaries say it uses a sliding window plus periodic anchors, which would be a fixed pattern, not learned top-k. Full text was blocked (R7-025).
- **FlashLoop (2609.29812).** "Loop-aware sparse attention", for efficiency. Not read.
- **Fully Looped Transformer (2605.18797)** and **Hyperloop (2604.21254).** Hyperloop's text had no sparse/top-k hits; 2605.18797 was not downloaded.
- **Hierarchical sparse attention length generalization (2510.17196); kNN Attention Demystified (ICLR 2025); A Formal Framework for Length Generalization (2410.02140).** 2410.02140 is downloaded but was not mined.
- **MoDr (ICLR 2026).** Routes between LoRA branches of a Huginn loop, not over tokens; out of scope.
- **LT2.** Whether the "Looped NSA" arm in §3.6 is pure NSA or a hybrid. The text lists Looped NSA separately from Looped GDN+NSA, which suggests it is pure. Seed count is not stated in the sentence we read.

## (e) Failed sources

- **OpenReview** (forum, `/pdf?id=`, `api2.openreview.net`) for kdZbxizwGK, ChainGPT: a browser-verification challenge (HTTP 403, ChallengeRequiredError). We did not attempt to solve the challenge. We used the ML Anthology mirror of the abstract instead.
- **Semantic Scholar Graph API:** repeated HTTP 429 rate limits. 12 of 16 query attempts returned empty.
- **HTML extraction** dropped some inline math, so the "top-k" and "×" symbols appear as "top-" in quotes from 2601.22766, 2602.01219 and 2410.01651. Noted per row.
