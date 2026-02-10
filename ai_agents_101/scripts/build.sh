#!/bin/bash
# Build script for AI Agents 101 course materials (Quarto)
#
# Usage:
#   ./scripts/build.sh              # Build everything
#   ./scripts/build.sh diagrams     # Just render Mermaid diagrams
#   ./scripts/build.sh book         # Course notes (PDF book)
#   ./scripts/build.sh slides       # Slide deck (revealjs HTML)
#   ./scripts/build.sh handouts     # Student handout, exercises, facilitator guide → PDFs
#   ./scripts/build.sh all          # Everything
#   ./scripts/build.sh clean        # Remove scattered build artifacts
#
# Dependencies:
#   - quarto (https://quarto.org)
#   - npm install -g @mermaid-js/mermaid-cli   (for diagrams)
#
# NOTE: Standalone files (slides, handouts) must be rendered OUTSIDE the
# book project tree, because Quarto forces the book's format config on
# everything in the project directory. The workaround is to copy files
# to a temp dir, render there, and move output back.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

# Render a standalone file outside the book project tree.
# Usage: render_standalone <source_file> <format> <output_dir>
render_standalone() {
    local src="$1"
    local fmt="$2"
    local outdir="$3"
    local name=$(basename "$src" | sed 's/\.[^.]*$//')

    # Create temp dir and copy source + dependencies
    local tmpdir=$(mktemp -d)
    cp "$src" "$tmpdir/"
    # Copy img/ so image references work
    [ -d img ] && cp -r img "$tmpdir/"

    # Render in temp dir (no _quarto.yml = no book interference)
    (cd "$tmpdir" && quarto render "$(basename "$src")" --to "$fmt")

    # Move output back
    local ext="$fmt"
    [ "$fmt" = "revealjs" ] && ext="html"
    if [ -f "$tmpdir/${name}.${ext}" ]; then
        mv "$tmpdir/${name}.${ext}" "$outdir/"
        echo "  → ${outdir}/${name}.${ext}"
    fi
    # For revealjs, also grab the _files support dir
    if [ "$fmt" = "revealjs" ] && [ -d "$tmpdir/${name}_files" ]; then
        rm -rf "${outdir}/${name}_files"
        mv "$tmpdir/${name}_files" "$outdir/"
    fi

    rm -rf "$tmpdir"
}

build_diagrams() {
    echo "=== Rendering Mermaid diagrams ==="
    mkdir -p img
    for mmd in diagrams/*.mmd; do
        [ -f "$mmd" ] || continue
        name=$(basename "$mmd" .mmd)
        echo "  $name.mmd → $name.png"
        mmdc -i "$mmd" -o "img/$name.png" -b transparent -w 1200 -H 800
    done
    echo "  Done"
}

build_book() {
    echo "=== Building course notes PDF (Quarto book) ==="
    # This uses _quarto.yml book project — renders to pdf/ (output-dir)
    quarto render --to pdf
    echo "  Done → pdf/AI-Agents-101_course-companion.pdf"
}

build_slides() {
    echo "=== Building slides (revealjs) ==="
    mkdir -p slides
    echo "  slides/slides.qmd → revealjs"
    # Slides need ../img/ refs rewritten to img/ for temp dir rendering
    local tmpqmd=$(mktemp -d)
    sed 's|\.\./img/|img/|g' slides/slides.qmd > "$tmpqmd/slides.qmd"
    [ -d img ] && cp -r img "$tmpqmd/"
    (cd "$tmpqmd" && quarto render slides.qmd --to revealjs)
    [ -f "$tmpqmd/slides.html" ] && mv "$tmpqmd/slides.html" slides/
    [ -d "$tmpqmd/slides_files" ] && rm -rf slides/slides_files && mv "$tmpqmd/slides_files" slides/
    rm -rf "$tmpqmd"
    echo "  Done → slides/slides.html"
}

build_handouts() {
    echo "=== Building handout PDFs ==="
    mkdir -p pdf
    for md in docs/student_handout.md docs/exercises.md docs/facilitator_guide.md; do
        [ -f "$md" ] || continue
        name=$(basename "$md" .md)
        echo "  $md → pdf/${name}.pdf"
        render_standalone "$md" pdf pdf
    done
    echo "  Done → pdf/"
}

clean_artifacts() {
    echo "=== Cleaning scattered build artifacts ==="
    # PDFs that escaped to root
    rm -f exercises.pdf facilitator_guide.pdf student_handout.pdf
    # Quarto scatter in docs
    rm -rf docs/*_files
    rm -f docs/*.html docs/course_companion/*.html
    # Legacy PDF name
    rm -f pdf/AI-Agents-101.pdf
    echo "  Done"
}

# Default to all if no argument
TARGET="${1:-all}"

echo "=================================================="
echo "Building AI Agents 101 Materials"
echo "=================================================="

case "$TARGET" in
    diagrams)
        build_diagrams
        ;;
    book)
        build_diagrams
        build_book
        ;;
    slides)
        build_diagrams
        build_slides
        ;;
    handouts)
        build_handouts
        ;;
    clean)
        clean_artifacts
        ;;
    all)
        build_diagrams
        build_book
        build_slides
        build_handouts
        clean_artifacts
        ;;
    *)
        echo "Unknown target: $TARGET"
        echo "Usage: $0 [diagrams|book|slides|handouts|clean|all]"
        exit 1
        ;;
esac

echo ""
echo "=================================================="
echo "Build complete"
echo "=================================================="
