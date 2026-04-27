# CC Task: Tier 2 Prose QC Pass

**Date:** 2026-03-24
**Scope:** Find and fix all Tier 2 prose quality violations across paper sections 01-07.
**Config:** Rules defined in `paper/paper_qc_config.yaml`

---

## Pre-Flight

1. Read `paper/paper_qc_config.yaml` for the full rule set.
2. Read `paper/paper_style_config.yaml` for banned words/phrases (Tier 3, report only, do not fix unless obvious).
3. Read `paper/conventions.md` for style guidance.

---

## Step 1: Build and Run a QC Scanner

Write a Python script `paper/prose_qc.py` that:

1. Reads all `.md` files in `paper/sections/` (00 through 09).
2. Parses each file into paragraphs and sentences (split on `. `, `? `, `! ` while handling abbreviations and decimal numbers).
3. For each sentence, checks:
   - **Word count > 35** → flag with file, line number, word count, and the sentence text.
   - **Contains em dash (—)** → flag.
   - **Passive voice** → simple heuristic: flag sentences matching `(was|were|is|are|been|be|being) + past_participle_pattern`. This is approximate; false positives are OK to flag for review.
   - **Ambiguous pronoun** → flag sentences starting with "This " or "It " followed by a verb (no noun antecedent). Heuristic: "This + verb" or "It + verb" at sentence start.
   - **Semicolons in sentences > 20 words** → flag.
4. For each paragraph, checks:
   - **Fewer than 2 sentences** → flag (except in abstract, definitions, or math blocks).
   - **More than 8 sentences** → flag.
5. For banned words/phrases from `paper_style_config.yaml`:
   - Report occurrences with file and line number. Do not auto-fix; report only.
6. Output: print a structured report grouped by file, with violation type, line number, and the offending text. Also write the report to `paper/prose_qc_report.md`.

Run the script. Paste the full output.

---

## Step 2: Fix Tier 2 Violations

For each violation found, apply the fix. Work file by file, reading the current state before each edit.

### Sentence length (> 35 words)
- Split into two sentences at the most natural break point (usually a conjunction, relative clause, or parenthetical).
- Preserve meaning exactly. Do not add or remove content.
- If the sentence cannot be split without losing clarity, note it as an exception with a brief justification.

### Em dashes (—)
- Replace with comma, colon, semicolon, or restructure into two sentences.
- Choose the punctuation that best fits the logical relationship.

### Passive voice
- Rewrite in active voice using "we" as the subject where appropriate.
- If passive is genuinely better (actor irrelevant or unknown), leave it and note the exception.

### Ambiguous pronouns
- Replace "This" with "This [noun]" (e.g., "This result", "This pattern", "This constraint").
- Replace "It" with the specific referent.

### Semicolons in long sentences
- Split into two sentences at the semicolon.

### Single-sentence paragraphs
- Merge with adjacent paragraph if logically connected, or add a supporting sentence.
- Exception: standalone definitions or transitional sentences between sections.

### Banned words (Tier 3, report only)
- Do NOT auto-fix. Just list them in the report. Brock will review.

---

## Step 3: Re-Run QC

After all fixes, re-run `paper/prose_qc.py`. The report should show 0 Tier 2 violations (or a small number of justified exceptions).

---

## Post-Flight

1. Run `python paper/check_glossary.py` for glossary/terminology compliance.
2. Run `seldon paper sync`.
3. Run `seldon paper build --no-render` to verify no broken references.
4. Report: total violations found, total fixed, any remaining exceptions with justification, and the Tier 3 (banned word) list for Brock's review.

## Do NOT

- Do not change the meaning of any sentence.
- Do not alter Seldon result references `{{result:...:value}}`.
- Do not modify math blocks or tables.
- Do not modify section 00 (abstract, not yet written) or section 08 (references) or section 09 (appendix).
- Do not fix Tier 3 violations without explicit approval.
- Read current file state before every edit.
