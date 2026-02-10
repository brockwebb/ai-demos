#!/usr/bin/env python3
"""
Build script for AI Agents 101 course materials (Quarto).

Usage:
    python scripts/build.py              # Build everything
    python scripts/build.py diagrams     # Render Mermaid diagrams to PNG
    python scripts/build.py book         # Course companion PDF (Quarto book)
    python scripts/build.py slides       # Slide deck PDF (Beamer) + revealjs HTML
    python scripts/build.py handouts     # Student handout, exercises, facilitator guide PDFs
    python scripts/build.py all          # Everything
    python scripts/build.py clean        # Remove scattered build artifacts

Dependencies:
    - quarto (https://quarto.org)
    - npm install -g @mermaid-js/mermaid-cli  (for diagrams)
    - LaTeX with beamer package (for slides PDF)

NOTE: Standalone files (slides, handouts) must be rendered OUTSIDE the
book project tree, because Quarto forces the book's format config on
everything in the project directory. Workaround: copy to temp dir, render, move back.
"""

import subprocess
import sys
import shutil
import tempfile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "pdf"
IMG_DIR = ROOT / "img"
DIAGRAMS_DIR = ROOT / "diagrams"
SLIDES_DIR = ROOT / "slides"
DOCS_DIR = ROOT / "docs"


def run(cmd: list[str], cwd: Path | None = None, check: bool = True):
    """Run a subprocess, printing the command."""
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"    STDERR: {result.stderr.strip()}")
        if check:
            sys.exit(result.returncode)
    return result


def render_standalone(src: Path, fmt: str, output_dir: Path, output_name: str | None = None):
    """
    Render a standalone Quarto file outside the book project tree.
    Copies source + img/ to a temp dir so _quarto.yml doesn't interfere.
    """
    name = output_name or src.stem
    ext = "html" if fmt == "revealjs" else fmt

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Copy source file
        src_content = src.read_text()
        # Rewrite ../img/ paths to img/ (for files in subdirectories)
        src_content = src_content.replace("../img/", "img/")
        (tmp / src.name).write_text(src_content)

        # Copy images so references work
        if IMG_DIR.exists():
            shutil.copytree(IMG_DIR, tmp / "img")

        # Render
        run(["quarto", "render", src.name, "--to", fmt], cwd=tmp)

        # Move output
        output_file = tmp / f"{src.stem}.{ext}"
        if output_file.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            dest = output_dir / f"{name}.{ext}"
            shutil.move(str(output_file), str(dest))
            print(f"  → {dest.relative_to(ROOT)}")
        else:
            print(f"  ✗ Expected {output_file.name} not found in temp dir")


# ── Build targets ──────────────────────────────────────────────────

def build_diagrams():
    print("=== Rendering Mermaid diagrams ===")
    IMG_DIR.mkdir(exist_ok=True)
    mmd_files = sorted(DIAGRAMS_DIR.glob("*.mmd"))
    if not mmd_files:
        print("  No .mmd files found")
        return
    for mmd in mmd_files:
        png = IMG_DIR / f"{mmd.stem}.png"
        print(f"  {mmd.name} → {png.name}")
        run(["mmdc", "-i", str(mmd), "-o", str(png),
             "-b", "transparent", "-w", "1200", "-H", "800"])
    print(f"  Done — {len(mmd_files)} diagrams")


def build_book():
    print("=== Building course companion PDF (Quarto book) ===")
    run(["quarto", "render", "--to", "pdf"])
    print("  Done → pdf/AI-Agents-101_course-companion.pdf")


def build_slides():
    print("=== Building slides ===")
    PDF_DIR.mkdir(exist_ok=True)
    SLIDES_DIR.mkdir(exist_ok=True)

    slides_qmd = SLIDES_DIR / "slides.qmd"
    if not slides_qmd.exists():
        print(f"  ✗ {slides_qmd} not found")
        return

    # Beamer PDF for download
    print("  slides.qmd → Beamer PDF")
    render_standalone(slides_qmd, "beamer", PDF_DIR, output_name="slides")

    # Revealjs HTML for presenting (local use only, not linked from README)
    print("  slides.qmd → revealjs HTML")
    render_standalone(slides_qmd, "revealjs", SLIDES_DIR, output_name="slides")

    # Copy support files for revealjs if they exist
    # (render_standalone handles the main file; _files dir stays in temp)

    print("  Done → pdf/slides.pdf + slides/slides.html")


def build_handouts():
    print("=== Building handout PDFs ===")
    PDF_DIR.mkdir(exist_ok=True)
    handouts = [
        DOCS_DIR / "student_handout.md",
        DOCS_DIR / "exercises.md",
        DOCS_DIR / "facilitator_guide.md",
    ]
    for md in handouts:
        if not md.exists():
            print(f"  ✗ {md.relative_to(ROOT)} not found, skipping")
            continue
        print(f"  {md.relative_to(ROOT)} → pdf/{md.stem}.pdf")
        render_standalone(md, "pdf", PDF_DIR)
    print("  Done → pdf/")


def clean_artifacts():
    print("=== Cleaning scattered build artifacts ===")
    # PDFs that escaped to root
    for stray in ["exercises.pdf", "facilitator_guide.pdf", "student_handout.pdf"]:
        p = ROOT / stray
        if p.exists():
            p.unlink()
            print(f"  Removed {stray}")

    # Quarto scatter in docs
    for d in DOCS_DIR.glob("*_files"):
        shutil.rmtree(d)
        print(f"  Removed {d.relative_to(ROOT)}")
    for html in list(DOCS_DIR.glob("*.html")) + list((DOCS_DIR / "course_companion").glob("*.html")):
        html.unlink()
        print(f"  Removed {html.relative_to(ROOT)}")

    # Legacy PDF name
    legacy = PDF_DIR / "AI-Agents-101.pdf"
    if legacy.exists():
        legacy.unlink()
        print("  Removed pdf/AI-Agents-101.pdf")

    print("  Done")


# ── CLI ────────────────────────────────────────────────────────────

TARGETS = {
    "diagrams": lambda: build_diagrams(),
    "book": lambda: (build_diagrams(), build_book()),
    "slides": lambda: (build_diagrams(), build_slides()),
    "handouts": lambda: build_handouts(),
    "clean": lambda: clean_artifacts(),
    "all": lambda: (build_diagrams(), build_book(), build_slides(), build_handouts(), clean_artifacts()),
}

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target in ("-h", "--help"):
        print(__doc__)
        return

    if target not in TARGETS:
        print(f"Unknown target: {target}")
        print(f"Usage: python {sys.argv[0]} [{' | '.join(TARGETS)}]")
        sys.exit(1)

    print("=" * 50)
    print("Building AI Agents 101 Materials")
    print("=" * 50)

    TARGETS[target]()

    print()
    print("=" * 50)
    print("Build complete")
    print("=" * 50)


if __name__ == "__main__":
    main()
