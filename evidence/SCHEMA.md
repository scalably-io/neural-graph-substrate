# Evidence schema

Two kinds of researcher output, both merged only by `scripts/validate_evidence.py`.

## 1. Claims — `evidence/research/R<n>-*.csv` → merged `evidence/claims.csv`

`claim_id,branch,claim,value,unit,status,source_url,locator,quote,source_date,retrieved,confidence,notes`

| field | rule |
|---|---|
| claim_id | `R<n>-<nnn>` |
| branch | family code, see below |
| status | REPORTED · THEOREM · DESIGN · AUTHOR-CLAIM · CODE · DERIVED · REPRODUCED · ACCESS-FAILED |
| locator | section / table / figure / theorem / equation / file path in repo, enough to find the quote in under a minute |
| quote | verbatim from the source, ≤40 words, and it must contain the number when `value` is a number. Empty ⇒ unusable (except ACCESS-FAILED) |
| source_date | publication or commit date (ISO, `YYYY` or `YYYY-MM` allowed) |
| retrieved | ISO date the researcher read it |
| confidence | High / Medium / Low |
| notes | DERIVED rows: the formula. REPORTED rows: the baseline it is compared against and whether the comparison is param- or FLOP-matched |

Status meanings:
- **REPORTED**: an empirical number the authors report (we have not reproduced it).
- **THEOREM**: a proved statement (theorem/proposition number in locator).
- **DESIGN**: an architectural fact (what is shared, what is recurrent, what the graph is).
- **AUTHOR-CLAIM**: a qualitative claim by the authors ("first to", "stable", "scales"). Never cited as fact, only as "the authors state".
- **CODE**: a fact read from an official repository (license, framework, kernel, last commit).
- **DERIVED**: our computation; formula in notes.
- **REPRODUCED**: we ran it (orchestrator only, with an EXPERIMENTS.md ID in notes).
- **ACCESS-FAILED**: kept in the ledger, never citable.

Family codes (`branch`):
MPNN · RGNN (recurrent / implicit GNN) · DYN (dynamic, adaptive, rewiring, latent-graph) · GT (graph transformer) · HYP (hypergraph) · TOP (simplicial / cellular / topological) · NCA · LOOP (universal / looped / recurrent-depth transformers, recursive reasoning models) · DEQ · ODE · HOP (Hopfield / associative memory) · PCEP (predictive coding, equilibrium propagation, local learning) · RES (reservoir / liquid state) · HALT (adaptive computation) · ROUTE (conditional computation, MoE, mixture-of-depths, top-k routing) · CONN (learned connectivity, topology learning, communicating modules) · NAR (neural algorithmic reasoning) · READ (distributed readouts, deep supervision, multi-exit) · OSC (oscillatory / synchrony / neuron-level temporal dynamics) · THEORY (expressivity and capacity results across families) · BENCH · GPU (implementation and hardware efficiency) · X (common)

## 2. Approach matrix — `evidence/research/R<n>-matrix.csv` → merged `evidence/matrix.csv`

`approach_id,family,name,primary_ref,year_venue,q1_graph,q2_edges,q3_topology_at_inference,q4_state_persists,q5_weight_sharing,q6_training,q7_scaling,q8_stability,q9_capacity,q10_more_iterations_help,q11_gpu,q12_repos,q13_best_results,q14_unexplored,claim_ids`

One row per approach. Cells ≤40 words, `unknown` allowed (never guessed). `claim_ids` is a `;`-separated list; every ID must exist in the same researcher's claims CSV, and every non-`unknown` cell must be supported by at least one listed claim. Approach IDs: `A<n>-<nn>` with n = researcher number.

## 3. Candidate-component coverage (in each dossier `R<n>-*.md`)

Closest prior art scored against the candidate's components (Y / P = partial / N, with claim_ids):
C1 persistent node states h_i · C2 sparse directed graph · C3 shared message fn M · C4 shared update fn U · C5 recurrent evolution over T steps · C6 learned top-k routing / edge creation · C7 hyperedges · C8 state-conditioned topology · C9 persistent associative memory · C10 distributed readouts · C11 confidence / convergence signal · C12 learned adaptive halting · C13 topology and node roles evolve during computation.
