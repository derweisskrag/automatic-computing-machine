#!/bin/bash
# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Move to project root (assuming the script lives in /scripts)
PROJECT_ROOT="$SCRIPT_DIR/.."
cd "$PROJECT_ROOT" || exit 1

echo "📂 Working directory: $PWD"

# Now run pandoc safely with absolute paths
pandoc "$PROJECT_ROOT/essay.md" \
  --standalone \
  --pdf-engine=xelatex \
  --citeproc \
  --include-before-body="$PROJECT_ROOT/title_page_essay.tex" \
  --lua-filter="$PROJECT_ROOT/split_pages.lua" \
  -o "$PROJECT_ROOT/sergei_ivanov_loputoo_essay_tagasiside.pdf"

# pandoc "$PROJECT_ROOT/README.md" \
#   --standalone \
#   --from markdown+raw_tex \
#   --citeproc \
#   --bibliography="$PROJECT_ROOT/books.bib" \
#   --pdf-engine=xelatex \
#   --include-before-body="$PROJECT_ROOT/title_page.tex" \
#   --lua-filter="$PROJECT_ROOT/split_pages.lua" \
#   -V geometry:margin=1in \
#   -V mainfont="Times New Roman" \
#   -o "$PROJECT_ROOT/output.pdf"

