# Review N2 (fresh-context Opus 5.5, adversarial), 2026-10-01

Target: `paper/paper.md` v0.1 (draft), Figure 1 `figures/coverage.svg`, `evidence/coverage.csv`, §7 vs `docs/PREREGISTRATION.md` v0.3.1.
Sources checked: the cached texts in `evidence/sources/` (read this session) plus live fetches of arxiv.org/html/2605.20670 and arxiv.org/html/2510.01585 this session.

## (a) Verdict

**FIX-THEN-SHIP.** The note's structure and caution are sound, but its account of LT2 leaves out the routing-free arms that do as well or better in LT2's own tables, and Figure 1's headline and subtitle are not true of the data as scored. All three blockers can be fixed from material already in the repo, without new research.

## (b) BLOCKERS

**B1. LT2 retrieval result presented as routing counter-evidence; the same table shows routing-free loops doing as well or better.**
- Where: §1 answer 2 ("a sparse and linear hybrid also extrapolates on retrieval where the dense loop scores 0.0"), §5 ("On retrieval, a sparse and linear hybrid trained at 2048 tokens scores 91.4 at 4096, where the dense loop scores 0.0 … the extrapolating arm mixes routing with linear attention"), §9 ("a sparse and linear hybrid extrapolating on retrieval (91.4 against 0.0)").
- What is wrong: LT2 Table 5, NIAH-Single-1 at 4096 (cached `evidence/sources/R7/2605.20670.txt`, Table 5 rows), reads:
  - non-looped Transformer 0.0;
  - Looped Transformer 0.0;
  - **Looped GDN 99.8** (no routing);
  - Looped Hybrid (GDN+DSA) 91.4;
  - **Looped Hybrid (Full+GDN) 93.5** (dense attention + GDN, no routing).

  So the 0.0 is a failure of dense attention to extrapolate in length, and it is not caused by looping: the non-looped Transformer also scores 0.0. A routing-free loop extrapolates best. On NIAH-2 and NIAH-3 at 4096, Full+GDN (81.0 / 63.7) also beats GDN+DSA (77.6 / 60.3). The authors attribute the effect to the recurrent mixer. Live fetch, arxiv.org/html/2605.20670 §3.7: "recurrent backbones extrapolate gracefully to 4096 while dense-attention ones do not." The note saying "mixes routing with linear attention" is true, but it is incomplete in the direction that inflates the counter-evidence. A reader who opens Table 5 will see this immediately.
- Fix:
  - Add ledger rows for Looped GDN (99.8), Full+GDN (93.5) and the non-looped Transformer (0.0) at NIAH-1 4096.
  - Rewrite §1 answer 2, §5 and §9 so the retrieval result counts as evidence for recurrent linear mixers, not for routing.
  - Remove the 91.4/0.0 figure from "the strongest case against us".
  - Also fix R7-012's claim text, which says LT2 attributes the result to the GDN+DSA loop; the authors attribute it to recurrent backbones.

**B2. The state-tracking result omits a fourth no-routing arm that also reaches 128.**
- Where: §1 answer 2 ("several cheaper looped mixers … double the largest state-tracking problem"), §5 ("three cheaper mixers reach 128 (R7-005, R7-006): learned top-k sparse attention, and also a linear-attention variant with only a local window and no routing").
- What is wrong: the same paragraph of LT2 that R7-006 quotes continues: "Looped Full+GDN does too, but only because half its block is already linear-time GDN" (live fetch of arxiv.org/html/2605.20670 confirmed this sentence; cached txt line ~1436). So four arms reach 128, and three of them contain GDN. The only arm that reaches 128 by top-k selection alone is Looped NSA. NSA is also not pure top-k: its rows have compressed-block and window branches (R7-002 quote: "KV cache + compressed blocks; ℐ t : top- w selected indices"). Looped Full+Window stays at 64, which rules out the window alone as the explanation.
- Fix:
  - List all four arms that reach 128.
  - Name NSA as the single arm that bears on routing, and describe it as NSA (compressed + selected + window branches), not as "learned top-k sparse attention".
  - Answer 2 then reads: one top-k arm and three GDN arms double n_max at trained size.

**B3. Figure 1's subtitle is false for the data, and its title depends on incomplete scoring that the repo's own cached sources contradict.**
- Where: figure subtitle "Each mark rests on a cited claim whose quote supports it"; the §4.4 caption, same sentence; figure title "No system has more than 6 of 13"; §1 answer 4.
- What is wrong:
  - (i) Of the 51 N marks in `evidence/coverage.csv`, **46 carry no claim ID** (computed this session). "Does not" is an asserted absence with no cited quote, which is exactly what the subtitle denies.
  - (ii) ReSSFormer is scored from two ledger rows only. C1, C3, C4 and C9 are marked "?", yet the cited R6-006 quote itself names a "Recurrent Reasoning & **Memory** Unit". The full text is cached at `evidence/sources/R6/2510.01585.txt`. Live fetch, arxiv.org/html/2510.01585: "ReSSFormer reuses a recurrent block with memory aggregation; it replaces dense attention with token- and expert-sparse mechanisms; and it eliminates positional encoding by inducing latent token graphs from input content", and "M(t) is a step-specific memory embedding".
  - Scored from this text, ReSSFormer plausibly has C1, C4, C5, C6, C8 and C9 (memory, at least P), with C3 and C13 ("inducing latent token graphs") as candidates. That is at least 6 fully, and likely 7, which would break the title and answer 4.
  - §9 admits that "four systems [are scored] only from their own quoted rows", but a title stated as fact cannot rest on a scoring gap the authors already hold the text to close.
- Fix:
  - Score ReSSFormer (and the other "own rows only" systems) from their cached full texts, with new ledger rows.
  - Change the subtitle to "Y and P marks rest on a cited quote; N marks are our reading of the paper (IDs where available)", or add an ID to every N.
  - Recompute the title and answer 4 from the rescored data.
  - In §4.4, describe ReSSFormer as recurrent block + memory + top-k + content-induced token graph. It is closer to the candidate than the note currently says.

## (c) MAJOR

- **M1. §4.2 heading and §1 answer 1 understate the compute picture.** "Per unit of compute it is small": two of the three compute-relevant citations show a compute *loss*, not a small gain. R2-199 (our derivation) is 1.4× the forward compute for parity. R5-092 shows a looped 410M model costing the training compute of a 1B model to match a 580M one. Only R2-089 (SMELT, MoE middle-layer loops) shows a 6.8–18.0% saving. Fix: "per unit of compute it is small or negative".
- **M2. Not being compute-matched in LT2 favours the dense arm, not routing.** §1 answer 2 and §5 list "is not compute-matched" as a weakness of LT2 as counter-evidence. The winning arms are the subquadratic, cheaper ones (the note itself calls them "cheaper"). The mismatch therefore makes LT2's result *stronger*, not weaker. Say so, or drop that caveat. The other two caveats (no sharpened arm; train-at-size, not train-small/test-large) carry the argument.
- **M3. §1 answer 5 overstates how open the question is.** "Whether learned, unsupervised top-k routing … adds anything inside a weight-tied loop beyond recurrence and attention sharpness". Looped NSA versus the Looped Transformer (same loop, same backbone, R7-005/R7-006) is already a recurrence-held-fixed comparison, and the top-k arm wins at trained size. What remains open is "beyond sharpness and recurrent linear mixers, on train-small/test-large". Narrow answer 5 and the §6 "Not found" bullet accordingly.
- **M4. §4.4 reachability result: magnitude likely inflated by the metric.** "99.97% … against 91.51% … The gap is graph structure". This is last-step accuracy. GAT-full's last-step score *rises* with size (77.86% at 20 nodes, 91.51% at 100, from the R6-017 quote), which suggests base-rate effects in per-node reachability at larger, denser graphs. On mean-step accuracy in the same quote the gap is 92.34% vs 88.98% (about 3.4 points). Report both, or give the direction only.
- **M5. §7 omits a design fact a reader needs to interpret any graph-versus-attention result.** The shared recipe gives *every* arm, including the dense T1 and T1-sharp, a learned adjacency bias e_ij = β·A_ij + embed(w_ij) (PREREGISTRATION "Shared recipe"). So the "looped Transformer" is told the task graph. Together with §4.4's "the gap is graph structure", this changes what G1 versus T1 measures. State it in §7.
- **M6. Coverage cells whose quote does not support the mark** (detail in table (e)):
  - MoR C5 Y and C8 P (R2-022 is a few-shot accuracy quote);
  - MoR C13 P (R2-025 is about load imbalance);
  - HRM/TRM C4 Y (R2-039) and C5 Y (R2-034);
  - Discrete NAR C5 Y (R6-010 does not mention recurrence);
  - IterGNN C1, C3 and C4 Y (R1-022 is about adaptive iteration only);
  - Co-GNN C3 P (R1-061 shares the *action* network, not the message function).

  Several are probably true of the papers but are not supported *by the cited quote*, which is the figure's own standard. Separately, MoR C12 is "?" although learned per-token recursion depth is MoR's defining feature. LT2 related work, cached: "Mixture-of-Recursions learns dynamic per-token depths in a token-level routing framework". That cell should be P or Y.
- **M7. "15 closest published systems" includes a union row.** "Looped Transformer family (union of several papers)" is not a system, and it reaches 6 only by pooling papers. Exclude it from the "no system has more than N" count, or say "no single paper".

## (d) MINOR

- §1 answer 1 and §4.2: "looped language models report 2 to 3 times" is one paper (Ouro). Write "Ouro reports".
- §4.1: "collapses after about 100 rounds" — the R1-029 quote says "accuracy declines rapidly". Use the source's wording.
- §4.1: "an outer refinement loop drove most of the gain (R2-048)" is the ARC Prize analysis's interpretation. Attribute it. The R2-048 quote gives +13pp and "doubles", not "most of the gain".
- §4.1: "parameter-matched" for R4-165 comes from the row's notes; the quote does not contain it. Add the parameter statement to the quote, or attribute it.
- §4.1: R1-027 ("1000 times larger") does not name the task. A reader will ask which one.
- §4.5: R5-049's quote supports only the general rule (unregistered operators add zero). That scatter, gather and top-k are unregistered is our grep, recorded in the notes. Label it "our reading of the file at commit 958e982".
- R2-199 and R5-131 are DERIVED but have no entry in `docs/DERIVATIONS.md`, which project rule 6 requires. R2-199's quote (a radar-plot caption) supports nothing in its claim.
- §5: "cheaper" for the LT2 mixers is unsourced at n ≤ 256. Subquadratic asymptotically, yes; cheaper at those sizes, not shown.
- §7: "Every looped arm runs the same number of steps" — G3 runs at most T(n). Also, "preregistration-ready" sits awkwardly with a DRAFT that has five open questions. Use "draft protocol".
- §3: "twenty neural-network families" — the ledger has 23 branch codes, 19 of them family codes. Generate the number.
- GNCA C2 Y: R3-089 says "arbitrary graphs", which is neither necessarily sparse nor directed. P is safer.
- Lead, unverified (not checked this session beyond its presence in the ledger, 1 row): negative-eigenvalue linear RNNs and state tracking (arXiv 2411.12537) is the natural mechanism for why the GDN arms win at LT2 state tracking. Citing it in §5 would make B2's reframing concrete.

## (e) Audit tables

### Citation audit (prose IDs)

| ID | where | supports? | note |
|---|---|---|---|
| R2-016 | §1, §4.2 | yes | one model family; "report" attributed |
| R2-017 | §1, §4.3 | yes | |
| R7-004/005/006 | §1, §5 | yes, incomplete | omits Full+GDN reaching 128 (B2) |
| R7-007 | §5 | yes, attributed | |
| R7-010/011 | §1, §5, §9 | numbers yes, framing no | Looped GDN 99.8, Full+GDN 93.5 omitted (B1) |
| R4-070, R1-099 | §2 | yes, attributed | |
| R4-024 | §4.1 | yes | post-hoc peak stated, good |
| R1-027 | §4.1 | yes | task unnamed |
| R1-029 | §4.1 | direction yes, wording strong | "collapses" vs "declines rapidly" |
| R4-080 | §4.1 | yes, attributed | |
| R4-165 | §4.1 | yes; "parameter-matched" is from notes, not the quote | |
| R2-048 | §4.1 | partly | "most of the gain" is interpretation |
| R2-199 | §4.2 | DERIVED; quote irrelevant; no DERIVATIONS entry | |
| R2-089 | §4.2 | yes; matching stated from notes | |
| R5-092 | §4.2 | yes | supports M1 (compute loss) |
| R4-185 | §4.2 | yes | |
| R2-018, R2-095 | §4.2 | yes | |
| R6-008 | §4.4 | yes ("explicit selection") | |
| R6-006, R6-007 | §4.4 | yes, but undersells ReSSFormer (B3) | |
| R1-067, R1-059 | §4.4 | yes | |
| R6-010 (AC), R6-011, R4-048 (AC) | §4.4 | yes, attributed | |
| R6-001 | §4.4 | yes | |
| R6-016, R6-012 | §4.4 | yes; "sharp" for NDR is our gloss | |
| R6-017, R4-001, R4-002 | §4.4 | numbers yes; magnitude metric-dependent (M4) | |
| R1-164, R1-109 | §4.4 | yes | |
| R7-032, R7-033 | §4.4 | yes | |
| R4-176 | §4.4 | yes; not param-matched (notes) | unstated in prose |
| R5-086 | §4.5 | yes (GCN, large graphs; labelled inference) | |
| R5-131 | §4.5 | DERIVED; formula checks (0.75^1024 ≈ 1e-128) | no DERIVATIONS entry |
| R5-049 | §4.5 | general rule only | specifics are our grep |
| R5-017, R5-041, R5-042 | §4.5 | yes | |

### Coverage-cell audit (Y and P cells)

| system | cell | ids | verdict |
|---|---|---|---|
| LT family | C1 Y | R2-001; R2-007 | weak (shared block / recurrence; persistence implied) |
| LT family | C3, C4 Y | R2-001 | ok |
| LT family | C5 Y | R2-007; R2-018 | ok |
| LT family | C11 Y | R2-013 | ok (KL convergence halt) |
| LT family | C12 Y | R2-003 (AC); R2-020 (AC) | ok as existence; both author claims |
| LT2 | C1, C3, C4, C5 Y | R7-003 | ok |
| LT2 | C2 P, C6 Y, C8 Y | R7-002 | quote is a table fragment; "learned" rests on notes; ok-ish |
| ReSSFormer | C2 P, C6 Y, C8 Y | R6-007 | ok |
| ReSSFormer | C5 Y | R6-006 | ok; same quote names a Memory Unit, yet C9 is "?" (B3) |
| MoR | C5 Y, C8 P | R2-022 | **not supported by quote** |
| MoR | C6 P | R2-025 | ok (routing exists) |
| MoR | C13 P | R2-025 | **not supported** |
| MoR | C12 ? | none | should be P/Y (per-token depth) |
| HRM/TRM | C4 Y | R2-039 | **weak** (layer count, not sharing) |
| HRM/TRM | C5 Y | R2-034 | **weak** (param count, no recursion in quote) |
| HRM/TRM | C11 P, C12 Y | R2-032; R2-044 | ok |
| N2 | C1, C3, C4, C5 Y; C2, C6, C8, C13 P | R1-067; R1-068 | ok |
| Co-GNN | C1 P, C6 P, C8 Y, C13 P | R1-059 | ok |
| Co-GNN | C2 P | R1-060 (AC) | ok-ish |
| Co-GNN | C3 P | R1-061 | **mismatch** (action network, not message function) |
| IterGNN | C1, C3, C4 Y | R1-022 | **weak** |
| IterGNN | C5 Y; C11, C12 Y | R1-022; R1-023 | ok |
| Discrete NAR | C2 P | R6-011 | ok |
| Discrete NAR | C5 Y | R6-010 | **quote lacks recurrence** |
| Discrete NAR | C6, C8 P | R6-010 | ok |
| PGN/NEE | C2, C6, C8, C13 P | R4-016; R4-021 | ok |
| CTM | C1, C5, C11 Y; C3, C8, C10 P | R3-098; R3-099; R3-161 | ok |
| CTM | C12 P | R3-111 (AC) | ok, author claim |
| Energy Tr. | C1, C3, C4, C5, C9, C11 Y; C8 P | R3-011; R3-012; R3-015 | ok |
| GNCA | C1–C5 Y | R3-089 | C2 should be P |
| Set-to-hypergraph | C5, C7 Y | R1-164 | ok |
| DyHSL | C7 Y | R1-109 | ok |

"?" vs "N": inconsistent. 46 of 51 N cells have no ID while "?" means "no claim", so the two classes carry the same evidential weight. Either cite N cells or merge them into a labelled "our reading" class.

Chart title is true of the CSV as scored (max fully present = 6: LT family, LT2, IterGNN, Energy Transformer). "Fully present in no system: C10, C13" is true. The subtitle is false (B3), and the title is fragile (B3, M7).

§7 versus PREREGISTRATION: arms, tasks, budget numbers (reachability 16→12 … 1024→56; maze 9→81 … 33→737, from `docs/generated/budgets.md`), ±5% matching, the D2 per-step FLOP rule, outcome classes, the validity gate, 5–15 seeds, and the five open questions all match. Omissions: the adjacency bias in every arm (M5), G3's "at most", and the max(4, ·) floor (immaterial).

## (f) Repeats of earlier rounds (read after (a)–(e) were written)

Read after writing (a) to (e): N1-opus.md, R1/R2/R3-opus.md, NEGATIVE-FINDINGS.md.

| N2 finding | relation to earlier rounds |
|---|---|
| B1 (Looped GDN 99.8, Full+GDN 93.5, non-looped Transformer 0.0 at NIAH-4096) | **New, and partly caused by N1.** N1 B2 found that LT2 tests extrapolation and that GDN+Window matches without routing. N1's suggested fix then *installed* the 91.4/0.0 figure as "the strongest counter-evidence". Neither N1 nor NEGATIVE-FINDINGS row 33 read the rest of Table 5, which attributes the effect to recurrent mixers. |
| B2 (Full+GDN also reaches 128; NSA is the only routing-only arm and is not pure top-k) | **New.** It extends N1 B2.3. |
| B3(i) (46/51 N marks have no ID while the subtitle says every mark rests on a quote) | **Repeat in a new form** of N1 B4. Y/P cells were rescored; the caption claim still overreaches through the N class. |
| B3(ii) (ReSSFormer underscored; cached text supports C1/C4/C9, maybe 7 full marks) | **New.** R1 M1 found ReSSFormer and R3 B3 fixed a scope sentence, but its coverage cells were never rescored from the cached full text. |
| M1 (compute: small or negative) | Partly a repeat of N1 M6 (it fixed the "1.4×" wording, not the heading). |
| M2, M3, M5 | New. |
| M4 (last-step base-rate inflation) | New. N1 B3 introduced the GAT* 99.97 vs 91.51 framing; R3 flagged base-rate only for our own generator. |
| M6 (cells not supported by their quote; MoR C12 "?") | Residual repeat of N1 B4: a different set of cells after rescoring. |
| M7 (composite row) | Repeat of N1 B4; the row was relabelled but is still counted as a "system". |
| Minor R2-048 attribution | Partly a repeat of N1 M2 (fixed "training loop"; "most of the gain" is still unattributed). |

Pattern: each round fixes the sentence it was shown, and the fix adds a new selective number from the same source. For LT2, the durable fix is to ledger the *whole* of Table 5 (NIAH columns) and Figure 9 (all arms) and generate the §5 paragraph from them.
