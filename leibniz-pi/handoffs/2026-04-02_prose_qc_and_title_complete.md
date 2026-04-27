# Handoff: Prose QC, Title, and Table Captions Complete

**Date:** 2026-04-02
**From:** Claude Desktop (prose QC + editorial session)
**To:** Next Claude thread (final PDF verification + remaining edits)

---

## Status: All prose QC fixes, title update, epistemic hedge, and table caption restructuring complete. Final PDF render and visual verification remain.

---

## What Was Accomplished This Session

### Prose QC Run
- Replicated `prose_qc.py` and `check_glossary.py` checks locally (scripts require Seldon on user's machine)
- Found 19 Tier 2 violations, 29 Tier 3 warnings across sections 01-07
- No banned words, no banned phrases, no clichés, no em dashes — editorial pass was clean

### Prose QC Fixes (CC Task: `2026-04-02_prose_qc_tier2_fixes.md`)
- **Section 01 intro rewrite:** Merged three staccato fragments ("Training runs end. Test sets have boundaries. Context windows close.") into one comma-list sentence. Merged two ambiguous-pronoun sentences into one compound sentence. CC made a slightly different (better) edit: "The constraint is structural, arising from how we build and test all of them" instead of the semicolon version specified.
- **Section 01:** Split over-length LLM confabulation sentence (31 words → two sentences)
- **Section 03:** Split diversity injection sentence (32 words → two sentences)
- **Section 05:** Split wrong-limit attractor sentence, population scaling sentence; fixed ambiguous pronoun "It" → "The threshold"
- **Section 06:** Split road-map sentence, gradient-based selection sentence, Sastry population-sizing sentence, population range sentence (41 words → two sentences), confabulation analogy sentence (40 words → two sentences)
- **Section 07 staccato left intentional** — "The fitness was never the bottleneck. The search space was." works as emphasis in the conclusion

### Title Update (CC Task: `2026-04-02_title_update.md`)
- Old: "The Evaluation Horizon Trap: Why Search Space Structure Dominates Fitness Design"
- New: "The Evaluation Horizon Trap: Why Search Space Structure Dominates Solution Discoverability"
- "Solution Discoverability" replaces "Fitness Design" — reframes from GP-internal comparison to general finding about finding answers

### Epistemic Hedge (CC Task: `2026-04-02_epistemic_hedge_section02.md`)
- Section 02, "Fitness Design for Convergent Processes" subsection
- Added "To our knowledge," before "prior symbolic regression work does not address fitness design for this objective class"
- Scanned all sections for other unhedged absolute claims — none found. Results-section "none achieved" claims are all backed by data tables.

### Table Caption Restructuring (CC Task: `2026-04-02_table_captions_pandoc_native.md`)
- Converted all 8 table captions (Tables 1-8) from bold-paragraph style to Pandoc native `: ` caption syntax
- Moves captions inside the longtable environment so LaTeX cannot separate caption from table body at page breaks
- Covers Section 04 (Tables 1-2) and Section 05 (Tables 3-8)
- May need `\captionsetup[table]{position=above}` in frontmatter.yml if Pandoc renders captions below tables

### Font Decision
- Palatino is the intentional font choice. Not a bug. Brock decided it looks better than Source Sans Pro. Remove from "known issues" in future handoffs.

---

## What Still Needs Doing

### High priority

| Task | Notes |
|------|-------|
| Final PDF render + visual verification | Render and check: table captions bound to tables, abstract formatting, Census disclaimer, section numbering, figures, bibliography. Palatino is correct. |
| Verify table caption fix | The Pandoc native caption syntax should bind captions to tables. Confirm no caption/table separation at page breaks. If captions render below tables, add `\captionsetup[table]{position=above}` to frontmatter.yml |

### Medium priority

| Task | Notes |
|------|-------|
| Final `prose_qc.py` run on user's machine | CC ran post-flight but confirm 0 new Tier 2 violations in sections 01, 03, 05, 06. Section 07 staccato flags are accepted. |

### Low priority

| Task | Notes |
|------|-------|
| Medium article | Summary linking to preprint. Not started. Deprioritized. |
| Seldon DataFile registration | 20+ DataFile artifacts in proposed state. Not blocking. |
| Heatmap figure cleanup | `fig1_scaling_heatmap.{png,pdf}` still in `paper/figures/` but unreferenced. Can delete or leave. |

---

## Section Status

| Section | Status |
|---------|--------|
| 00 Abstract | Done |
| 01 Introduction | Done — staccato fixed, LLM sentence split |
| 02 Background | Done — epistemic hedge added |
| 03 Methods | Done — diversity injection sentence split |
| 04 Experimental Design | Done — table captions restructured |
| 05 Results | Done — 3 sentence splits, 1 pronoun fix, table captions restructured |
| 06 Discussion | Done — 6 sentence splits |
| 07 Conclusion | Done — staccato intentional, no changes |
| 08 References | Done |
| 09 Appendix | Done |

---

## CC Tasks Created This Session

| Task | Status |
|------|--------|
| `2026-04-02_prose_qc_tier2_fixes.md` | Complete |
| `2026-04-02_title_update.md` | Complete |
| `2026-04-02_epistemic_hedge_section02.md` | Complete |
| `2026-04-02_table_captions_pandoc_native.md` | Complete |

Note: A duplicate task `2026-04-02_title_and_prose_qc_fixes.md` was created in error (contained title change + duplicate prose fixes). Brock deleted it manually.

---

## Key Decisions Made This Session

1. **Intro staccato → merged.** "Training runs end. Test sets have boundaries. Context windows close." merged into comma-list. Staccato in Section 07 conclusion kept intentional.
2. **Title changed.** "Fitness Design" → "Solution Discoverability" to avoid sounding like a GP methods paper.
3. **Palatino is correct.** Not a font rendering bug. Intentional choice.
4. **Table captions → Pandoc native.** Prevents page-break orphaning between caption and table body.
5. **No other unhedged absolute claims found.** Only the Section 02 claim needed hedging.

---

## Key Principles (Unchanged)

- All implementation through CC task files in `cc_tasks/`
- Never overwrite existing CC task files (write new ones instead)
- After any edit: `check_glossary.py` → `seldon paper sync` → `seldon paper build --no-render` → `quarto render paper/paper.qmd --to pdf`
- No em dashes (use commas). "Log-precision fitness." "Discovery." "Coverage." "We" throughout.
- Paper is about structural limits of finite evaluation, not about GP.

---

## Key Files

| File | Contents |
|------|---------|
| `paper/frontmatter.yml` | YAML frontmatter — title updated, Palatino intentional |
| `paper/sections/*.md` | All paper sections (10 files, 00-09) |
| `paper/figures/*.{pdf,png}` | Publication figures (Fig 1-3 active, heatmap files orphaned) |
| `paper/_quarto.yml` | Quarto build config |

---

## Do NOT

- Do not rerun any experiments
- Do not modify existing CC task files
- Do not hardcode values
- Do not use "entropy fitness" — use "log-precision fitness"
- Do not frame the paper as being about GP
- Do not use em dashes
- Do not re-add crystallization, design provenance, or "domain knowledge encoding" language
- Do not change the font — Palatino is intentional
