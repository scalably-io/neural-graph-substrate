#!/usr/bin/env bash
# Rebuild every generated number, table, figure and the note from the evidence ledger. Exit non-zero on any failure.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/validate_evidence.py          # ledger schema, quotes present, numbers in quotes
python3 -m pytest -q                          # task solvers, budget, compute model, statistics, coverage, guards
python3 scripts/build_budgets.py > /dev/null  # docs/generated/budgets.md (about two minutes)
python3 scripts/build_charts.py               # figures/coverage.svg
python3 paper/build_paper.py                  # paper/paper.md from the ledger (structural guards)
echo "reproduce: OK"
