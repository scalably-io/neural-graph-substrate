<hard_constraints>
1. Read-only on the web: no messages, emails, form submissions, sign-ups, account creation, issues/PRs/comments on GitHub. Never contact anyone.
2. Write ONLY to your three output files, plus downloads into evidence/sources/<your prefix>/. Touch nothing else in the repo or on this machine.
3. Do the work yourself. Do not use the Agent tool, do not spawn subagents.
4. Today is 2026-10-01. Your training memory is stale and incomplete for 2025–2026. Never state a number, a result, a venue or a repo fact from memory. Every claim needs: URL + exact locator (section/table/figure/theorem/equation or repo file path) + a verbatim quote of 40 words or fewer that contains the number if the claim is numeric. No quote → the claim does not go in.
5. Papers you "remember" are LEADS, not facts. Confirm each one exists at a primary URL (arXiv abs/html, OpenReview, proceedings, official repo) before writing a row about it. A lead you cannot confirm goes in the dossier under "unconfirmed leads", never in the CSV.
6. Status exact (evidence/SCHEMA.md): REPORTED · THEOREM · DESIGN · AUTHOR-CLAIM · CODE · DERIVED (formula in notes) · ACCESS-FAILED. Novelty or "state of the art" assertions by authors are AUTHOR-CLAIM.
7. Results must say what they are compared against and whether the comparison is matched on parameters, FLOPs, or neither (notes column). An unmatched comparison is still recorded, labelled unmatched.
8. Be adversarial. You are looking at least as hard for evidence that the target hypothesis FAILS (instability, no gain from extra iterations, no gain over a weight-shared transformer, GPU-hostile, capacity bounded by parameters) as for evidence that it works. Record negative results and failed replications as first-class rows.
</hard_constraints>

<target_hypothesis>
Replace a feed-forward layer stack with a persistent recurrent graph of N neural nodes with latent states h_i, a sparse directed graph, a shared message function M and update function U, evolved for T steps until convergence or a learned halt; learned state-conditioned top-k routing / edge creation; optional hyperedges; persistent associative memory; readouts attached to many graph regions; confidence/convergence signals. Claim under test: time (recurrent iterations) can replace depth, topology becomes part of the computation, and this yields more reasoning/computational capacity per stored parameter than a fixed-depth Transformer.

The obvious objection you must collect evidence on, for or against: a Transformer is already a fully connected graph whose attention is state-conditioned dynamic routing, and a weight-shared looped / universal / recurrent-depth Transformer already reuses the same weights over time. The candidate must beat THAT, not only a fixed-depth Transformer. Also separate "computational capacity per parameter" (what recurrence can add) from "knowledge storage per parameter" (which recurrence cannot add).
</target_hypothesis>

<per_approach_questions>
For every relevant approach answer, in the matrix CSV: q1 exact computational graph · q2 edges fixed or learned · q3 topology changes during inference · q4 node state persists across iterations · q5 weights shared across iterations/nodes · q6 training (BPTT, truncated BPTT, implicit differentiation, equilibrium learning, local losses, deep supervision…) · q7 scaling in nodes, edges, state dim, iterations · q8 stability problems (exploding/vanishing, oversmoothing, oversquashing, collapse, chaos) and the fixes used · q9 memory capacity / parameter efficiency · q10 do extra inference iterations improve capability (and beyond the training horizon?) · q11 GPU efficiency + PyTorch/JAX/Triton compatibility · q12 official repos (URL, license, framework, last activity) · q13 best benchmark results vs Transformer/GNN baselines, with matching stated · q14 what remains genuinely unexplored.
</per_approach_questions>

Tools: WebSearch, WebFetch. Prefer arXiv HTML (`https://arxiv.org/html/<id>`) or abs pages; OpenReview forum pages for venue/decision. PDFs: `curl -sL -o <path>.pdf <url>` then `/opt/homebrew/bin/pdftotext -layout <file> -`; search with /usr/bin/grep (plain grep is ugrep here). Repos: `gh api repos/<owner>/<repo>` and `gh api repos/<owner>/<repo>/license` (read-only), or raw.githubusercontent.com.
CSV files: write with Python's csv module; headers exactly as in evidence/SCHEMA.md; retrieved = 2026-10-01. Before you finish, run `python3 scripts/validate_evidence.py` (report-only) and fix every REJECT for your prefix.
