#!/usr/bin/env python3
"""
Build script for AI Agents 101 course materials.

Usage:
    python scripts/build_materials.py --all          # Everything
    python scripts/build_materials.py --slides       # Diagrams + slides PDF
    python scripts/build_materials.py --notes        # Compile chapters + PDF
    python scripts/build_materials.py --handouts     # Handout, exercises, guide → PDFs
    python scripts/build_materials.py --diagrams     # Just render diagrams

Dependencies:
    npm install -g @mermaid-js/mermaid-cli   # mmdc
    npm install -g @marp-team/marp-cli       # marp
    npm install -g md-to-pdf                 # markdown to PDF
"""

import argparse
import subprocess
import sys
from pathlib import Path


# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
CHAPTERS_DIR = ROOT_DIR / "chapters"
DIAGRAMS_DIR = ROOT_DIR / "diagrams"
IMG_DIR = ROOT_DIR / "img"

# Source files
SLIDES_MD = ROOT_DIR / "slides.md"
COURSE_NOTES_MD = ROOT_DIR / "course_notes.md"
STUDENT_HANDOUT_MD = ROOT_DIR / "student_handout.md"
EXERCISES_MD = ROOT_DIR / "exercises.md"
FACILITATOR_GUIDE_MD = ROOT_DIR / "facilitator_guide.md"


def check_command(cmd: str) -> bool:
    """Check if a command is available."""
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_dependencies(need_mmdc=False, need_marp=False, need_md2pdf=False):
    """Check required dependencies and exit with helpful message if missing."""
    missing = []
    
    if need_mmdc and not check_command("mmdc"):
        missing.append("mmdc (npm install -g @mermaid-js/mermaid-cli)")
    
    if need_marp and not check_command("marp"):
        missing.append("marp (npm install -g @marp-team/marp-cli)")
    
    if need_md2pdf and not check_command("md-to-pdf"):
        missing.append("md-to-pdf (npm install -g md-to-pdf)")
    
    if missing:
        print("Missing dependencies:")
        for dep in missing:
            print(f"  - {dep}")
        sys.exit(1)


def render_diagrams():
    """Render Mermaid diagrams to PNG."""
    print("\n=== Rendering Mermaid diagrams ===")
    
    IMG_DIR.mkdir(exist_ok=True)
    
    mmd_files = list(DIAGRAMS_DIR.glob("*.mmd"))
    if not mmd_files:
        print("  No .mmd files found in diagrams/")
        return
    
    for mmd_file in mmd_files:
        output_file = IMG_DIR / f"{mmd_file.stem}.png"
        print(f"  {mmd_file.name} → {output_file.name}")
        subprocess.run([
            "mmdc",
            "-i", str(mmd_file),
            "-o", str(output_file),
            "-b", "transparent",
            "-w", "1200",
            "-H", "800"
        ], check=True)
    
    print(f"  Done: {len(mmd_files)} diagrams rendered")


def build_slides():
    """Build slides PDF with Marp."""
    print("\n=== Building slides ===")
    
    output_pdf = SLIDES_MD.with_suffix(".pdf")
    print(f"  {SLIDES_MD.name} → {output_pdf.name}")
    
    subprocess.run([
        "marp",
        str(SLIDES_MD),
        "--pdf",
        "-o", str(output_pdf),
        "--allow-local-files"
    ], check=True)
    
    print(f"  Done: {output_pdf.name}")


def compile_chapters():
    """Compile chapter files into course_notes.md."""
    print("\n=== Compiling course notes ===")
    
    chapter_files = sorted(CHAPTERS_DIR.glob("*.md"))
    if not chapter_files:
        print("  No chapter files found")
        return
    
    content_parts = []
    for chapter_file in chapter_files:
        print(f"  Adding: {chapter_file.name}")
        content_parts.append(chapter_file.read_text())
    
    # Join with separator
    full_content = "\n\n---\n\n".join(content_parts)
    
    # Remove trailing separator if present
    full_content = full_content.rstrip("\n-")
    
    COURSE_NOTES_MD.write_text(full_content)
    
    word_count = len(full_content.split())
    print(f"  Done: {COURSE_NOTES_MD.name} ({word_count} words)")


def markdown_to_pdf(md_file: Path):
    """Convert a markdown file to PDF using md-to-pdf."""
    if not md_file.exists():
        print(f"  Warning: {md_file.name} not found, skipping")
        return
    
    print(f"  {md_file.name} → {md_file.stem}.pdf")
    
    subprocess.run([
        "md-to-pdf",
        str(md_file),
        "--config-file", str(SCRIPT_DIR / "pdf-config.json")
    ], check=True, cwd=ROOT_DIR)


def build_handouts():
    """Convert handout materials to PDF."""
    print("\n=== Building handout PDFs ===")
    
    handout_files = [
        STUDENT_HANDOUT_MD,
        EXERCISES_MD,
        FACILITATOR_GUIDE_MD,
    ]
    
    for md_file in handout_files:
        markdown_to_pdf(md_file)
    
    print("  Done")


def build_notes_pdf():
    """Convert course notes to PDF."""
    print("\n=== Building course notes PDF ===")
    markdown_to_pdf(COURSE_NOTES_MD)
    print("  Done")


def main():
    parser = argparse.ArgumentParser(
        description="Build AI Agents 101 course materials",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/build_materials.py --all
    python scripts/build_materials.py --slides
    python scripts/build_materials.py --notes
    python scripts/build_materials.py --handouts
    python scripts/build_materials.py --diagrams
        """
    )
    
    parser.add_argument("--all", action="store_true", help="Build everything")
    parser.add_argument("--slides", action="store_true", help="Render diagrams + build slides PDF")
    parser.add_argument("--notes", action="store_true", help="Compile chapters + build notes PDF")
    parser.add_argument("--handouts", action="store_true", help="Build handout PDFs (student, exercises, facilitator)")
    parser.add_argument("--diagrams", action="store_true", help="Just render Mermaid diagrams")
    
    args = parser.parse_args()
    
    # Default to --all if no flags specified
    if not any([args.all, args.slides, args.notes, args.handouts, args.diagrams]):
        args.all = True
    
    # Determine what we need
    need_mmdc = args.all or args.slides or args.diagrams
    need_marp = args.all or args.slides
    need_md2pdf = args.all or args.notes or args.handouts
    
    # Check dependencies
    check_dependencies(need_mmdc=need_mmdc, need_marp=need_marp, need_md2pdf=need_md2pdf)
    
    print("=" * 50)
    print("Building AI Agents 101 Materials")
    print("=" * 50)
    
    # Execute requested builds
    if args.all or args.diagrams or args.slides:
        render_diagrams()
    
    if args.all or args.slides:
        build_slides()
    
    if args.all or args.notes:
        compile_chapters()
        build_notes_pdf()
    
    if args.all or args.handouts:
        build_handouts()
    
    print("\n" + "=" * 50)
    print("Build complete")
    print("=" * 50)


if __name__ == "__main__":
    main()
