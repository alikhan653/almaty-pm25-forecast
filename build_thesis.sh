#!/usr/bin/env bash
# Build the complete thesis.
# Usage:
#   bash build_thesis.sh           → Word (.docx) via pandoc
#   bash build_thesis.sh --pdf     → PDF via XeLaTeX
#   bash build_thesis.sh --both    → Word + PDF

set -e

MODE="${1:-}"
THESIS_DIR="$(cd "$(dirname "$0")/thesis" && pwd)"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Word build ────────────────────────────────────────────────
build_docx() {
  OUT="$THESIS_DIR/THESIS_Alikhan_Almaty_PM25.docx"
  REF="$THESIS_DIR/reference.docx"

  FILES=(
    "$THESIS_DIR/abstract.md"
    "$THESIS_DIR/introduction.md"
    "$THESIS_DIR/chapter_1_review.md"
    "$THESIS_DIR/chapter_2_methodology.md"
    "$THESIS_DIR/chapter_3_implementation.md"
    "$THESIS_DIR/chapter_4_discussion.md"
    "$THESIS_DIR/conclusion.md"
  )

  if ! command -v pandoc &>/dev/null; then
    echo "ERROR: pandoc not found. Install: brew install pandoc"; exit 1
  fi

  echo "Building Word document..."
  REF_ARG=""
  [ -f "$REF" ] && REF_ARG="--reference-doc=$REF"

  pandoc "${FILES[@]}" \
    --from markdown \
    --to docx \
    $REF_ARG \
    --output="$OUT" \
    --toc \
    --toc-depth=3 \
    --number-sections

  echo "✓ Word: $OUT"
  open "$OUT"
}

# ── PDF build via XeLaTeX ─────────────────────────────────────
build_pdf() {
  # XeLaTeX may be at /Library/TeX/texbin after MacTeX install
  export PATH="/Library/TeX/texbin:$PATH"

  if ! command -v xelatex &>/dev/null; then
    echo "ERROR: xelatex not found."
    echo "Install: brew install --cask mactex-no-gui"
    echo "Then restart terminal or run: export PATH=/Library/TeX/texbin:\$PATH"
    exit 1
  fi

  # Regenerate tex/ files from current markdown
  echo "Converting markdown → LaTeX..."
  mkdir -p "$THESIS_DIR/tex"
  for f in abstract introduction chapter_1_review chapter_2_methodology \
            chapter_3_implementation chapter_4_discussion conclusion; do
    if [ -f "$THESIS_DIR/${f}.md" ]; then
      pandoc "$THESIS_DIR/${f}.md" \
        --from markdown --to latex \
        --output "$THESIS_DIR/tex/${f}.tex" \
        --wrap=none
      # Remove duplicate top-level heading (main.tex provides \chapter{})
      sed -i '' '1{/^\\section{/d;}' "$THESIS_DIR/tex/${f}.tex"
    fi
  done

  echo "Compiling XeLaTeX (3 passes)..."
  cd "$THESIS_DIR"
  xelatex -interaction=nonstopmode main.tex 2>&1 | grep -E "^(! |LaTeX Warning:|Error)" || true
  biber main 2>&1 | grep -v "^INFO" || true
  xelatex -interaction=nonstopmode main.tex > /dev/null
  xelatex -interaction=nonstopmode main.tex > /dev/null

  echo "✓ PDF: $THESIS_DIR/main.pdf"
  open "$THESIS_DIR/main.pdf"
}

# ── Dispatch ──────────────────────────────────────────────────
case "$MODE" in
  --pdf)  build_pdf ;;
  --both) build_docx; build_pdf ;;
  *)      build_docx ;;  # default: Word only
esac
