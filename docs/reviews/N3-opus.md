# Review N3 (Opus 5.5, fresh context, adversarial), 2026-10-01

Target: `paper/paper.md` (generated, v0.1 draft). Priority: Section 1, Section 5 + Table 2, Figure 1 + Section 4.4, Section 9, and Section 7 against `docs/PREREGISTRATION.md`.
Evidence used: `evidence/claims.csv`, `evidence/coverage.csv`, cached LT2 text `evidence/sources/R7/2605.20670.txt` (cited below as "LT2 txt" with line numbers), `evidence/sources/R1/1910.10593.txt`, `evidence/sources/R6/*.abstract.txt`. No web fetch was needed. Every quote below comes from those cached files.

## (a) Verdict

**FIX-THEN-SHIP.** The note's structure and hedging are sound and Table 2 reproduces LT2's Table 5 correctly. But the LT2 reading in the Summary, Section 5, Section 9 and protocol item 6 is selective in one direction: it calls dense attention "the weakest mixer" and shows pure linear recurrence's best column. Section 4.4 also misreads a source table in a way that reverses a comparison. A domain expert would quote all three of these first.

## (b) BLOCKERS

### B1. "Dense attention is the weakest mixer inside a loop" is not what LT2 finds
- **Where.** §1 answer 2: "The closest study (LT2) finds that dense attention is the weakest mixer inside a loop." §5: "So LT2 shows that dense attention is the weak mixer inside a loop". §9: "LT2 shows that our main comparator, the dense looped Transformer, is the weakest looped mixer on both of its tests." The same wording is in PREREGISTRATION open item 6.
- **What is wrong.** LT2 finds the dense loop weakest on two measures only: NIAH retrieval past the training length, and the curriculum stage metric. On its other evaluations the dense loop is the quality reference that the subquadratic arms at best *match*:
  - **Same Table 5.** In the knowledge-recall columns, the Looped Transformer scores SWDE 52.8 / FDA 61.7, against 34.9 / 30.6 for Looped GDN and 33.9 / 25.8 for Looped Mamba-2 (rows R6-021/022/023; the quotes are in the ledger). At 1024 and 2048 tokens it scores 100.0 on NIAH-1 and NIAH-2.
  - **Authors' framing.** LT2 txt l.274: "LT2-hybrid (GDN+DSA) … matching the standard looped transformer's quality". l.590: "at the smaller 0.6B scale, looped GDN still slightly trails the Looped Transformer".
  - **"Both of its tests".** LT2 has more than two evaluations: language modelling, the knowledge suite, NIAH, the curriculum and efficiency.
- **Fix.** Scope every instance: "inside a loop, dense attention is the weakest mixer at retrieval beyond the training length (Table 2) and on LT2's state-tracking curriculum; on in-length knowledge recall and language modelling it is LT2's reference, which the cheaper mixers at best match." This scoping does not weaken the note's argument: the reason to add a linear-recurrence control still stands.

### B2. The Summary and §5 use pure linear recurrence's best column, and the "match or beat" sentence is true only for hybrids
- **Where.** §1 answer 2: "the looped dense model scores 0.0 while a looped linear recurrence with no routing scores 99.8 (Table 2)". §5 bullet: "the looped linear recurrence without routing scores 99.8; the hybrid with routing 91.4". §5: "mixers without routing match or beat the routed ones on both tests." Protocol item 6: "recurrent mixers without routing matched or beat the routed ones".
- **What is wrong.** 99.8 is NIAH-Single-1. On NIAH-Single-2 and 3, the routed hybrid beats the pure looped linear recurrence by about 24 points: **77.6 vs 53.2 and 60.3 vs 35.8** (R6-024 vs R6-022, the note's own Table 2). Looped GDN+DSA vs Looped GDN is the closest thing LT2 has to a routing ablation, since it adds top-k attention to the same recurrence. It *helps* on 2 of 3 retrieval tests. The no-routing arm that beats the routed one on all three is the **full-attention + GDN hybrid** (93.5/81.0/63.7), i.e. dense attention paired with a recurrence. The same holds on the curriculum. LT2 txt l.1434-1436 lists exactly three subquadratic arms reaching stage 5 (NSA, GDN+Window, GDN+NSA), plus Full+GDN. Pure looped GDN is not among them; that it was tested and stalled lower is inferred from the exhaustive list and the Figure 9 caption "Pure mixers above the white line", since the figure image was not read. So the non-routing arms that match routing are **hybrids**, not "a looped linear recurrence".
- **Why it matters.** (i) A reader checking Table 2 sees the Summary chose the one column where pure GDN wins. (ii) The protocol's new arm (item 6: "gated delta / state-space mixer") is the *pure* recurrence, which in LT2 lost to routing on NIAH-2/3 and apparently on the curriculum. The control that actually neutralised routing in LT2 was a hybrid: Full+GDN, or GDN+Window.
- **Fix.** In §1 report all three tests, or say "on the first of three retrieval tests". Rewrite the §5 conclusion as: "adding top-k attention to a looped linear recurrence helps on two of three retrieval tests, but adding full attention instead helps as much or more; routing is therefore not isolated from 'any attention added to a recurrence'." Add a hybrid control (Full+GDN-style, or recurrence + local window) to protocol item 6, next to or instead of the pure recurrence.

### B3. §4.4 misreads the reachability table, and the parenthetical reverses the comparison
- **Where.** §4.4: "soft attention on the input graph reaches 99.97% last-step reachability at test size, against 91.51% for attention over the complete graph (85.76% against 91.83% averaged over steps)".
- **What is wrong.** The source table header (1910.10593 txt l.687-690) reads "Reachability (mean step accuracy / last-step accuracy) 20 nodes 50 nodes 100 nodes". R4-002's quote gives GAT-full's row as "78.40% / 77.86% 85.76% / 91.83% 88.98% / 91.51%". So **85.76 / 91.83 is GAT-full's own mean-step / last-step pair at 50 nodes**. It is not input-graph vs complete-graph averaged over steps. As written, the parenthetical tells the reader the complete graph wins on mean-step accuracy. The source says the opposite: at 100 nodes, GAT* 92.34% vs GAT-full 88.98% mean-step (R6-017 quote "92.34% / 99.97% 88.98% / 91.51%").
- **Fix.** "(92.34% against 88.98% averaged over steps)". Also add a build assert that pulls these from the quote positions instead of a typed pair. The build claims to reject typed numbers, so check why this one passed: the numbers appear in a quote, but the wrong pair was chosen.

## (c) MAJOR

**M1. The LT2 curriculum result is reported without its two confounds: best-over-T selection and a 100k-step trainability budget.**
- **Where.** §1 answer 2 ("double the largest state-tracking problem … (128 vs 64)") and the §5 bullet.
- **Best over T.** The comparison is best over loop counts for the cheap arms against "at any T" for the dense arm. LT2 txt l.1437-1438: "Looped GDN+Window is the most dramatic: stage 3 at T ≤ 4, stage 5 at T = 8". So at LT2's default T = 4 (the T of Table 2), one of the two no-routing winners solves only n = 32, *below* the dense loop's 64.
- **Training budget.** n_max is "the largest n solved" within "a 100 k-step budget" at a 0.90 threshold (R7-004). It measures learnability within a budget, not capacity. LT2's own stability section reports that the full-attention loop has gradient spikes that sparse loops lack (txt l.1352: "none of them shows the sharp spikes that occasionally appear in the full-attention loop"). An expert will ask whether dense's plateau is optimisation, not expressivity.
- **Fix.** Add "at the best loop count up to 8, within LT2's 100k-step-per-stage budget" to the 128-vs-64 sentence.

**M2. §5's compute sentence is uncited and reads backwards.**
- **Where.** "The dense arm also uses the most compute, so the missing compute matching works against it, not for it."
- **Direction.** If the dense arm got the most compute, the missing matching works *for* the dense arm, which makes its loss *more* robust. As written it says the opposite, or at best is ambiguous.
- **Support.** "Most compute" has no claim ID. In the curriculum (4-layer, 256-wide, sequences of a few hundred tokens), attention is a small share of FLOPs. NSA runs three branches (compressed, selected, window), so dense is not obviously the costliest.
- **Parameters.** "Same parameter budget" is looser than R7-007 suggests. LT2 txt l.2922: "the exact parameter count varies slightly across variants (e.g. DSA layers are heavier than dense Transformer blocks)". The routed arm has *more* parameters, not equal.
- **Fix.** Either cite a FLOP number, or write: "LT2 matches neither compute nor exactly parameters; its DSA layers are heavier than dense blocks."

**M3. Figure 1 / Table 1: several "yes" cells in the 6-of-13 rows are not supported by their quote, contradicting the caption "Each mark rests on a cited claim whose quote supports it".** The headline count "no system fully has more than 6" survives, because every correction lowers counts, so this is not a blocker.
- **Looped Transformer family, C1/C3/C4 = Y on R2-001.** The quote is "under certain assumptions UTs can be shown to be Turing-complete". It says nothing about node states or a shared message or update function. Use a quote about weight-tied blocks, e.g. R7-003 or a UT design row.
- **IterGNN, C11 = Y (and C12 = Y) on R1-022.** R1-022's own ledger note says "C11/C12 partial: global, not per-node". The quote mentions adaptive iteration, not a confidence signal; the source does have one, at 2010.13547 txt l.258 "calculates a confidence score". IterGNN C1/C3/C4 = Y also rest on a quote that says only "adaptively adjust the number of iterations". Either re-quote or follow the ledger note's P.
- **C9 standard is inconsistent.** Energy Transformer C9 = Y (a Hopfield module whose patterns are stored in weights; R3-011's quote does not mention memory). ReSSFormer C9 = P, on the grounds that its memory is "not persistent across inputs or associative" (R6-031 note). By ET's standard, any Transformer FFN key-value memory would qualify. Pick one rule.
- **LT2 C1 and C8 = Y on R7-002/003.** The quotes establish weight sharing and "top-w selected indices". They do not establish persistent node states or that selection is conditioned on the *current loop state*. That is plausible (queries change per loop) but inferred.
- **"C5 recurrent evolution over many steps".** It is marked Y for LT2 (T = 4) and ReSSFormer ("bounded depth"). Either define "many" or mark P.
- **"15 systems".** The first row is a union of papers, not a system. Say "15 rows (one a union of looped-Transformer papers)".

**M4. §9 understates abstract-only evidence.** "One closely related paper could be read only as an abstract." In fact R6-001 (the dispersion theorem), R6-008 (top-k since 2019), R6-012 (NDR) and R6-016 (ASEntmax, the basis of the T1-sharp arm and the "1000 times" figure) are all cited from abstracts: `evidence/sources/R6/` holds only `*.abstract.txt` for them, and their ledger locator is "Abstract". So are R6-004/005/013/014/015. The sharpened-attention side of the note, i.e. the main control, rests on abstracts. Fix: "Nine claims, including the dispersion theorem and the sharpened-attention results the protocol's control relies on, were read from abstracts only."

**M5. Answer 5 / §6 should acknowledge that LT2 Table 5 is already a train-short / test-long comparison of routed, recurrent and dense loops.** It is length extrapolation at language-model scale (2048 → 4096), not instance-size extrapolation on algorithmic tasks, but a hostile reader will say "train-small, test-large" was done. Also, "at fixed recurrence" in answer 5 is inaccurate for the curriculum, which sweeps T (Figure 9 "wrt. loop count T"). Fix: "LT2 compares … at T = 4 on retrieval extrapolation and across T on a trained-at-size curriculum; still open is … on instance-size extrapolation in algorithmic problems."

**M6. Answer 1 drops the mismatch that its own ledger records.** "recurrence helps (looped language models report 2 to 3 times parameter efficiency, R2-016)". R2-016's note: "baselines are external SOTA models with different data". Per CLAUDE.md rule 2 the mismatch must be printed beside the number. Fix: add "against external models trained on different data". Optionally cite R4-185 (r^0.46), which is controlled.

## (d) MINOR

- **m1.** §4.4 "Per-query top-k attention dates from at least 2019 (R6-008)". The quote, the only text cached (abstract), says "explicit selection of the most relevant segments". It says neither "top-k" nor "per-query". True of the paper as I recall it (inferred, not verified this session); re-quote from the full text.
- **m2.** §4.4 "a weight-tied Transformer with sharp, selective attention reaches 100% … (R6-012)". The NDR abstract says "copy gate and geometric attention", not weight-tied or sharp. "Sharp" is our characterisation; attribute it as such.
- **m3.** §9 "Figure 1 scores four systems only from their own quoted rows". `coverage.csv` basis shows five row-scored systems: LT2 (R7 rows), ReSSFormer and Discrete NAR (R6 rows), and set-to-hypergraph and DyHSL (R1 rows).
- **m4.** LT2 is internally inconsistent on the hybrid ratio. Table 5 caption: "hybrid models interleave with full attention in a 1 : 1 ratio" (txt l.1469). §3.7 text: "a fixed 4 : 1 ratio" (l.1460). §3.1: "hybrid ratio is 1:4" (l.583). The caption also implies GDN+DSA contains full attention, which §3.1 denies. Table 2 should note the ratio is ambiguous in the source, since the routed-vs-unrouted reading depends on what each hybrid contains.
- **m5.** §7 budget: "1.5 times the steps … at the ninety-ninth percentile" omits the max(4, ·) floor in the prereg rule.
- **m6.** §6 "at equal steps and no more compute" vs §7 "no more matrix-multiply compute". The prereg matches matmul FLOPs only; top-k selection and entmax are non-matmul. Use the §7 wording in §6.
- **m7.** Table 2 header "retrieval test 1/2/3": name them NIAH-Single-1/2/3 so readers can find them in LT2.
- **m8.** §1 Method "954 claims from 6 research workstreams". The ledger has 7 prefixes (R1 to R7); R6 is the orchestrator file per §3. Say "6 workstreams plus orchestrator verification rows".
- **m9.** Single runs: LT2 reports "All runs use seed 777 for the trainer and seed 42 for model initialization" (txt l.2971-2972). Every LT2 number in Table 2 and the curriculum is therefore a single seed. Say so once in §5.

## (e) Repeats of earlier rounds

Written after (a) to (d), from reading `docs/reviews/N1-opus.md`, `N2-opus.md` and `docs/NEGATIVE-FINDINGS.md`.

| Finding | Status |
|---|---|
| B1 ("dense is the weakest mixer") | **New, and caused by N2's fix.** N2 B1 correctly showed that routing-free loops match routing on NIAH. The rewrite then over-generalised this into "dense is weakest". Neither the note nor N2 read Table 5's knowledge columns or LT2 §3.1. |
| B2 (pure GDN's best column; "match or beat" holds only for hybrids) | **Partly a repeat of N2 B1/B2,** which noted that Full+GDN beats GDN+DSA. **New:** pure looped GDN *loses* to routed GDN+DSA on NIAH-2/3 by about 24 points, and the protocol's new item 6 adds the pure recurrence, not the hybrid that actually matched routing. This is the fourth round of the pattern N2 named ("each fix adds a new selective number from the same source"). |
| B3 (85.76/91.83 mislabelled as an averaged-over-steps comparison) | **New, and fix-induced.** N2 M4 gave the correct pair (92.34 vs 88.98 mean-step at 100 nodes). The applied fix took GAT-full's own 50-node pair instead. |
| M1 (best-over-T; 100k-step trainability) | Best-over-T partly repeats N1 B2.2 (which was about the sparse arm). The GDN+Window T ≤ 4 detail and the trainability confound are new. |
| M2 (compute sentence backwards, uncited; DSA heavier) | **A repeat of N2 M2 whose fix was garbled:** the intended point, "the mismatch favours dense", came out reversed. The DSA-parameter quote is new. |
| M3 (unsupported Y cells) | **A residual repeat of N1 B4 / N2 M6** (IterGNN C1/C3/C4; the union row = N2 M7). **New:** IterGNN C11 contradicts R1-022's own ledger note; the C9 rule is inconsistent between ET and ReSSFormer (N1 and N2 both passed ET C9 as OK); LT2 C1/C8 are inferred; "many steps" is undefined. |
| M4 (abstract-only evidence understated) | New. |
| M5 (LT2 Table 5 is already train-short/test-long; "fixed recurrence") | Related to N2 M3, which pushed in the narrowing direction; the "fixed recurrence" inaccuracy is new. |
| M6 (R2-016 mismatch dropped from answer 1) | Partly a repeat of N1 M6 (which fixed §4.2 but not the Summary). |
| m1 (R6-008 priority/quote) | Repeat of N1 minor 1 (still not re-quoted). |
| m5 (max(4, ·) floor) | Repeat of N2 (marked immaterial there). |
| m2, m3, m4, m6, m7, m8, m9 | New. |

**Recommendation that would stop the cycle.** As N2 also recommended: generate §1 answer 2, §5 and protocol item 6 from the *full* ledgered Table 5 (all 15 columns) plus a ledgered row per Figure 9 arm and T. Then add a build assert that any LT2 number quoted in prose has its sibling columns in the same sentence or in Table 2.
