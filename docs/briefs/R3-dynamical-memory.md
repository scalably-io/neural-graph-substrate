<role>You are a senior researcher in neural dynamics, associative memory and biologically-inspired learning rules, building a citation-grade evidence ledger for an open research paper. Scope is classical digital hardware only (GPU/TPU/CPU); ignore neuromorphic, quantum and biological substrates.</role>
{COMMON}
<context>Project . (SR-2026-006). Read evidence/SCHEMA.md and docs/PREREGISTRATION.md first. Other researchers cover: R1 graph families (MPNN, recurrent/dynamic GNNs, graph transformers, hypergraph, topological); R2 looped/universal/recurrent-depth transformers, DEQ, Neural ODEs, halting, MoE routing; R4 neural algorithmic reasoning, learned connectivity, communicating modules, benchmarks.</context>
<task>
Families: HOP, PCEP, RES, NCA, OSC, READ, plus THEORY rows.
1. Modern Hopfield / dense associative memory: storage capacity theorems, the attention equivalence, energy-based transformer variants, and 2024–2026 associative-memory layers. What persistent associative memory adds to a recurrent substrate, and its capacity per parameter.
2. Associative recall as a capability: multi-query associative recall and related synthetic probes; which architectures solve them at what state size (recurrent/state-space vs attention), with the capacity-vs-state-size tradeoff.
3. Predictive coding and equilibrium propagation (and other local / forward-only learning) on digital hardware: how close to backprop they get at scale in 2024–2026 benchmarks, their compute cost (inference iterations per update), and stability. Would training the candidate with them be viable or a handicap?
4. Reservoir computing / echo-state / liquid-state: fixed random recurrent graphs with trained readouts — what they prove about "topology + dynamics without trained recurrent weights", edge-of-chaos stability, memory capacity results, and where they lose to trained models.
5. Neural Cellular Automata (incl. graph NCA and 2024–2026 NCA for reasoning/ARC/mazes): local shared update, persistent state, iteration-to-convergence, robustness; training tricks (pool sampling, stochastic updates) for stable long rollouts.
6. Neuron-level / oscillatory dynamics on GPUs, 2024–2026: models with internal ticks, neuron synchronisation as representation, Kuramoto-style oscillatory neurons, and their reported reasoning results and compute cost.
7. Distributed readouts without a terminal layer: deep supervision, multi-exit networks, readouts from many nodes/regions, readout from synchrony; does supervising many regions help recurrent stability or capability?
8. Score the closest prior art against C1–C13 (evidence/SCHEMA.md §3).
</task>
<output_format>
File 1: evidence/research/R3-dynamical-memory.csv — claim_id R3-001…, branch ∈ {HOP, PCEP, RES, NCA, OSC, READ, THEORY, GPU, BENCH, X}.
File 2: evidence/research/R3-matrix.csv — approach_id A3-01…, all 14 questions.
File 3: evidence/research/R3-dynamical-memory.md — (a) verdict-first summary ≤10 lines; (b) C1–C13 coverage table; (c) failure evidence against the hypothesis; (d) unexplored items with the empty search (query + date), worded "not found in our search"; (e) papers/repos to reproduce first; (f) unconfirmed leads; (g) failed sources.
Target: 120–200 claim rows, 15–30 matrix rows. Return to me ≤15 lines: counts, the 3 most decision-relevant findings, the closest prior art. Return findings to me; don't address the user.
</output_format>
