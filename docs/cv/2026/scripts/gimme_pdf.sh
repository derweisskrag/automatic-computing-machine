#!/bin/bash
# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Move to project root (assuming the script lives in /scripts)
PROJECT_ROOT="$SCRIPT_DIR/.."
cd "$PROJECT_ROOT" || exit 1

echo "📂 Working directory: $PWD"


pandoc "$PROJECT_ROOT/accompany_poland.md" \
  --standalone \
  --pdf-engine=xelatex \
  --include-before-body="$PROJECT_ROOT/title_page.tex" \
  --lua-filter="$PROJECT_ROOT/split_pages.lua" \
  -V geometry:margin=0.75in \
  -V mainfont="Times New Roman" \
  -o "$PROJECT_ROOT/accompany_letter_rust_job_Czechia.pdf"

# Now run pandoc safely with absolute paths
# pandoc "$PROJECT_ROOT/README.md" \
#   --standalone \
#   --pdf-engine=xelatex \
#   --include-before-body="$PROJECT_ROOT/title_page.tex" \
#   --lua-filter="$PROJECT_ROOT/split_pages.lua" \
#   -V geometry:margin=0.75in \
#   -V mainfont="Times New Roman" \
#   -o "$PROJECT_ROOT/rust_cv_sergei_ivanov_2026.pdf"

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

