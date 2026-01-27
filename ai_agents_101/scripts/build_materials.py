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
import re
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
SLIDES_FULL_MD = ROOT_DIR / "slides_full.md"  # Combined with glossary backup
COURSE_NOTES_MD = ROOT_DIR / "course_notes.md"
STUDENT_HANDOUT_MD = ROOT_DIR / "student_handout.md"
EXERCISES_MD = ROOT_DIR / "exercises.md"
FACILITATOR_GUIDE_MD = ROOT_DIR / "facilitator_guide.md"

# Chapter files (explicit for clarity)
EXTENDED_GLOSSARY_MD = CHAPTERS_DIR / "12_extended_glossary.md"


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


def extract_glossary_slides() -> str:
    """
    Extract [SLIDE] tagged terms from extended glossary and format as Marp slides.
    
    Returns backup slides section for appending to slide deck.
    """
    if not EXTENDED_GLOSSARY_MD.exists():
        print(f"  Warning: {EXTENDED_GLOSSARY_MD.name} not found, skipping glossary slides")
        return ""
    
    content = EXTENDED_GLOSSARY_MD.read_text()
    
    # Find all ### headings with [SLIDE] tag
    # Pattern: ### Term Name **[SLIDE]** followed by content until next ### or ---
    pattern = r'### ([^\n]+?)\s*\*\*\[SLIDE\]\*\*\n(.*?)(?=\n---|\n### |\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        print("  No [SLIDE] tagged terms found in glossary")
        return ""
    
    print(f"  Found {len(matches)} glossary terms marked for slides")
    
    # Build backup slides section
    slides = []
    slides.append("\n---\n")
    slides.append("<!-- Backup Slides: Selected Glossary Terms -->\n")
    slides.append("# Backup: Key Terms Reference\n")
    slides.append("\n*Reference slides for selected vocabulary*\n")
    
    for term_name, term_content in matches:
        term_name = term_name.strip()
        term_content = term_content.strip()
        
        # Extract just the definition (first paragraph/line after the heading)
        # Stop at **Source:** or **Note:** or **Why it matters:**
        definition_match = re.match(r'^([^\n]+(?:\n(?![*\n]).[^\n]*)*)', term_content)
        definition = definition_match.group(1).strip() if definition_match else term_content[:500]
        
        # Extract source if present
        source_match = re.search(r'\*\*Source:\*\*[^\n]*\n([^\n]+)', term_content)
        source = source_match.group(1).strip() if source_match else ""
        
        # Extract "Why it's a misnomer" or "Why it matters" or key note
        note_match = re.search(r'\*\*(?:Why it\'s a misnomer|Why it matters|Critical implication|Note):\*\*([^\n]+)', term_content)
        note = note_match.group(1).strip() if note_match else ""
        
        # Format slide
        slide = f"\n---\n\n# {term_name}\n\n"
        slide += f"{definition}\n"
        
        if note:
            slide += f"\n**Key point:** {note}\n"
        
        if source:
            slide += f"\n<small>{source}</small>\n"
        
        slides.append(slide)
    
    return "".join(slides)


def build_slides():
    """Build slides PDF with Marp, including glossary backup slides."""
    print("\n=== Building slides ===")
    
    # Read base slides
    base_slides = SLIDES_MD.read_text()
    
    # Extract glossary slides
    glossary_slides = extract_glossary_slides()
    
    # Combine: insert glossary backup after "# Questions?" slide
    if glossary_slides:
        # Find the Questions slide and append glossary after it
        if "# Questions?" in base_slides:
            combined = base_slides.replace(
                "# Questions?",
                "# Questions?\n" + glossary_slides
            )
        else:
            # Fallback: just append at end
            combined = base_slides + glossary_slides
        
        # Write combined version
        SLIDES_FULL_MD.write_text(combined)
        print(f"  Created {SLIDES_FULL_MD.name} with glossary backup slides")
        source_file = SLIDES_FULL_MD
    else:
        source_file = SLIDES_MD
    
    # Build PDF
    output_pdf = SLIDES_MD.with_suffix(".pdf")
    print(f"  {source_file.name} → {output_pdf.name}")
    
    subprocess.run([
        "marp",
        str(source_file),
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
    
    # List chapters for visibility
    print("  Chapters to compile:")
    for cf in chapter_files:
        print(f"    - {cf.name}")
    
    content_parts = []
    for chapter_file in chapter_files:
        content_parts.append(chapter_file.read_text())
    
    # Join with separator
    full_content = "\n\n---\n\n".join(content_parts)
    
    # Remove trailing separator if present
    full_content = full_content.rstrip("\n-")
    
    COURSE_NOTES_MD.write_text(full_content)
    
    word_count = len(full_content.split())
    print(f"  Done: {COURSE_NOTES_MD.name} ({word_count} words, {len(chapter_files)} chapters)")


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
