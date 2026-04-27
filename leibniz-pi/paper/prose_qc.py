#!/usr/bin/env python3
"""Prose QC for leibniz-pi — delegates to seldon.paper.qc.

Run from project root:
    python paper/prose_qc.py
"""
import sys
from pathlib import Path

from seldon.paper.qc import load_qc_config, load_style_config, run_tier2, run_tier3, format_violations

SECTIONS_DIR = Path("paper/sections")
CONFIG_PATH = Path("paper/paper_qc_config.yaml")
STYLE_PATH = Path("paper/paper_style_config.yaml")
TARGET_PREFIXES = [f"{n:02d}" for n in range(1, 8)]


def main():
    qc_config = load_qc_config(CONFIG_PATH)
    style_config = load_style_config(STYLE_PATH)

    total_t2 = 0
    total_t3 = 0

    for fp in sorted(SECTIONS_DIR.glob("*.md")):
        if not any(fp.name.startswith(p) for p in TARGET_PREFIXES):
            continue
        text = fp.read_text()
        t2 = run_tier2(text, qc_config, fp.name)
        t3 = run_tier3(text, style_config, fp.name)
        if t2:
            print(format_violations(t2, f"Tier 2: {fp.name}"))
            total_t2 += len(t2)
        if t3:
            print(format_violations(t3, f"Tier 3: {fp.name}"))
            total_t3 += len(t3)

    print(f"\nTotal: {total_t2} Tier 2 violations, {total_t3} Tier 3 findings")
    sys.exit(1 if total_t2 > 0 else 0)


if __name__ == "__main__":
    main()
