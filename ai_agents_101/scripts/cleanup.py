#!/usr/bin/env python3
"""
Cleanup script for AI Agents 101 repo.
Removes deprecated build scripts and handoff files.

Run with: python scripts/cleanup.py
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

# Files to remove
CLEANUP_FILES = [
    "build_coursenotes.sh",
    "build_slides.sh",
    "HANDOFF_2026-01-24_class_materials.md",
    "HANDOFF_2026-01-24_course_materials.md",
]

def main():
    print("Cleaning up deprecated files...")
    
    for filename in CLEANUP_FILES:
        filepath = ROOT_DIR / filename
        if filepath.exists():
            filepath.unlink()
            print(f"  Removed: {filename}")
        else:
            print(f"  Skipped (not found): {filename}")
    
    print("Done.")


if __name__ == "__main__":
    main()
