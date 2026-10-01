# Is the graph doing anything?

**A sourced survey of recurrent self-routing neural graphs as an alternative to layered networks.** Report SR-2026-006 by Pavle Lazić (Scalably). Research note `paper/paper.md`; Figure 1 `figures/coverage.svg`.

The question: can a persistent recurrent graph of neural nodes that rewires itself from its own state at every step give more reasoning capacity per stored parameter than a Transformer? The short answer: recurrence helps, a looped Transformer already has that, most parts of the design are published separately (no system in our scoring has more than seven of thirteen), and the one open question is narrow. We publish a preregistration-ready protocol for it, not results.

## Built with AI, on purpose

One founder directed AI agents (Anthropic's Claude) that searched primary sources, wrote a quote-per-claim evidence ledger, built the task generators, budget and compute models, and wrote the note from that ledger. Fresh-context Claude reviewers and OpenAI's GPT-6 Astra then attacked it; their reviews reversed several of our conclusions, and every reversal is recorded (`docs/NEGATIVE-FINDINGS.md`, `docs/reviews/`, `EXPERIMENTS.md`). No experiment was run and no human domain expert has reviewed it yet. That is what this repository is for: find where it breaks.

## Reproduce everything

```
python3 -m pip install -e ".[test]"
./scripts/reproduce.sh      # validates the ledger, runs the tests, regenerates budgets, the figure and the note
```

Every number in the note is filled by `paper/build_paper.py` (from claim quotes, claim text, derivations, the coverage table, protocol constants or counts); the build fails on a typed number, an unknown or inaccessible claim ID, a dash or a hype word.

## Where things are

| Path | What |
|---|---|
| `evidence/claims.csv` | The ledger: every claim with source URL, locator, verbatim quote, status and date, merged from `evidence/research/` by `scripts/validate_evidence.py`. Downloaded sources are not redistributed; every row is re-fetchable from its URL. |
| `evidence/matrix.csv` | 121 approaches, each answering fourteen fixed questions (partly filled; unknowns are marked). |
| `evidence/coverage.csv` | The data behind Figure 1, with the claim IDs each cell rests on. |
| `docs/QUESTION.md` | Why we did this and the questions we asked ourselves. |
| `docs/SYNTHESIS.md` | The longer internal synthesis the note was condensed from. |
| `docs/PREREGISTRATION.md` | The proposed experiment (draft, six open items), with `ngs/` (task generators with exact solvers, step budget, compute model, statistics). |
| `docs/DERIVATIONS.md` | Every formula with the test that pins it. |
| `docs/NEGATIVE-FINDINGS.md`, `docs/reviews/` | Our errors and the AI reviews that found them. |
| `docs/briefs/` | The exact briefs given to the AI research agents and reviewers. |

## Challenge a number

Open an issue with the claim ID, a better source, its locator and a verbatim quote.

## Licences

Code: Apache-2.0 (`LICENSE`). Text, data and figures: CC BY 4.0 (`LICENSE-CC-BY-4.0.txt`).

## Cite

See `CITATION.cff`. https://github.com/scalably-io/neural-graph-substrate
