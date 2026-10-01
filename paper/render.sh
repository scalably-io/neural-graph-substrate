#!/usr/bin/env bash
# Render paper/paper.md to a self-contained HTML and a PDF in paper/out/ (pandoc + headless Chrome).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
pandoc paper.md -f markdown-implicit_figures -o out/paper.html --standalone --embed-resources --css style.css \
  --metadata pagetitle="Is the graph doing anything?" --resource-path=.:..
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
rm -f out/paper.pdf
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/out/paper.pdf" "file://$PWD/out/paper.html" 2>/dev/null || true
test -s out/paper.pdf   # Chrome's exit code is unreliable here; the artifact is the check
echo "rendered out/paper.html and out/paper.pdf"
