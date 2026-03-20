# CC Task: Paper Foundations Audit + Repo Housekeeping

**Date:** 2026-03-17
**Priority:** HIGH — prerequisite to further paper editing
**Project:** leibniz-pi (`/Users/brock/Documents/GitHub/ai-demos/leibniz-pi`)
**Database:** `seldon-leibniz-pi`

---

## IMPORTANT: Read CLAUDE.md first

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
cat CLAUDE.md
```

Then orient via Seldon:
```bash
seldon go --brief
```

Follow the workflows documented there. This task is an audit and cleanup.
Everything you touch must be 100% correct. If you only get 25% done, that 25% must be right.

**Do NOT fix anything silently. Report findings first. Human decides what to fix.**

---

## Part A: Glossary Validation

### A1. Run check_glossary.py

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py 2>&1
```

Capture the full output: keyword index + any banned synonym violations.

### A2. Audit glossary completeness

Read every file in `paper/sections/`. For each section, identify:

1. **Technical terms used that are NOT in `paper/glossary.md`** — these are gaps.
   Look for: named concepts, defined quantities, coined terms, method names,
   parameter names that appear repeatedly across sections.

2. **Inconsistent term usage** — places where the glossary defines a term one way
   but a section uses it differently, or uses a near-synonym that isn't in the
   banned list.

3. **Terms in glossary whose definitions may be wrong** — compare the glossary
   definition against how the abstract and conclusion actually use the term
   (those are the authoritative sections the human has edited).

**Report as a structured list. Do NOT modify the glossary without human approval.**

### A3. Audit evidence_map.md

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon result list
```

Compare results in `paper/evidence_map.md` against:
- What's in the graph (seldon result list)
- What's referenced in section files (grep for `{{result:`)
- What's actually claimed in the text

Flag discrepancies. Also scan sections for literal numbers that should be
`{{result:...}}` references. Exempt: GP engine parameters (P_CROSS, TOURNAMENT_K, etc.),
mathematical constants (π/4, log₂(10)), and table data that summarizes multiple runs
where individual results aren't separately registered.

**Report findings. Do NOT change references without human approval.**

---

## Part B: Repo Housekeeping

The repo has accumulated organizational debt. Files are in inconsistent locations
and naming conventions have drifted.

### B1. Rename old CC tasks to current convention

Old convention: `CC_TASK_*.md`
Current convention: `YYYY-MM-DD_slug.md`

These files in `cc_tasks/` need renaming. They are historical (completed tasks).
Rename them with a `historical_` prefix since we don't know their exact dates:

```
CC_TASK_capture_design_motivation.md  → historical_capture_design_motivation.md
CC_TASK_entropy_fitness_sensitivity.md → historical_entropy_fitness_sensitivity.md
CC_TASK_entropy_stress.md             → historical_entropy_stress.md
CC_TASK_fitness_motivation_framing.md → historical_fitness_motivation_framing.md
CC_TASK_fix_scaling_heatmap.md        → historical_fix_scaling_heatmap.md
CC_TASK_gp_scaling_column.md          → historical_gp_scaling_column.md
CC_TASK_gp_scaling_extended.md        → historical_gp_scaling_extended.md
CC_TASK_gp_sensitivity.md             → historical_gp_sensitivity.md
CC_TASK_gradient_fitness.md           → historical_gradient_fitness.md
CC_TASK_paper_naming_fixes.md         → historical_paper_naming_fixes.md
CC_TASK_paper_skeleton.md             → historical_paper_skeleton.md
CC_TASK_parsimony_test.md             → historical_parsimony_test.md
CC_TASK_rename_entropy.md             → historical_rename_entropy.md
CC_TASK_scaling_heatmap.md            → historical_scaling_heatmap.md
CC_TASK_seldon_dogfood_leibniz.md     → historical_seldon_dogfood_leibniz.md
CC_TASK_seldon_dogfood_leibniz2.md    → historical_seldon_dogfood_leibniz2.md
CC_TASK_v3_clean_rerun.md             → historical_v3_clean_rerun.md
CC_TASK_v3_minimal.md                 → historical_v3_minimal.md
CC_TASK_v3_variants.md                → historical_v3_variants.md
```

Also remove `NOTE_run_paper_sync_after_edits.md` — superseded by CLAUDE.md.

### B2. Move misplaced root files

These files are at the repo root but belong in specific directories:

```
HANDOFF-3-15-2026--0830.md → handoffs/2026-03-15_initial_handoff.md
```

These research note supplements should be consolidated or moved to `docs/`:
```
RESEARCH_NOTES_SUPP_applicability.md      → docs/research_notes_supp_applicability.md
RESEARCH_NOTES_SUPP_complexity_ceiling.md  → docs/research_notes_supp_complexity_ceiling.md
RESEARCH_NOTES_SUPP_core_finding.md        → docs/research_notes_supp_core_finding.md
RESEARCH_NOTES_SUPP_design_motivation.md   → docs/research_notes_supp_design_motivation.md
RESEARCH_NOTES_SUPP_future_work.md         → docs/research_notes_supp_future_work.md
RESEARCH_NOTES_SUPP_pi_entropy_connection.md → docs/research_notes_supp_pi_entropy_connection.md
```

These utility/scratch files should go to a sensible location:
```
seldon_bootstrap.py      → .seldon/bootstrap.py  (or docs/ if it's documentation)
seldon_dogfood_notes.md  → docs/seldon_dogfood_notes.md
create_v3_variants.sh    → (check if still needed; if historical, move to EDA/ or docs/)
medium_draft_final.md    → docs/medium_draft_final.md  (or paper/ if it's paper-related)
v3_results_summary.md    → docs/v3_results_summary.md
```

**Before moving:** Read each file's first 10 lines to confirm the destination is correct.
The `RESEARCH_NOTES.md` at root is fine — it's the primary research notes file referenced
by CLAUDE.md. Leave it.

### B3. Verify .gitignore

Check `.gitignore` to make sure `cc_tasks/` and `handoffs/` are listed (they should be
gitignored per Seldon convention, but verify for this project).

---

## Part C: Register and Sync

### C1. Register foundation files in graph

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi

seldon artifact create LabNotebookEntry \
  -p summary="Controlled vocabulary and term definitions for paper" \
  -p name=glossary \
  --actor human --authority accepted

seldon artifact create LabNotebookEntry \
  -p summary="Results-to-claims provenance mapping for paper" \
  -p name=evidence_map \
  --actor human --authority accepted
```

### C2. Run full sync cycle

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py 2>&1
seldon paper sync
seldon paper build --no-render
```

Report all output.

---

## Part D: Summary Report

Produce a structured report with these sections:

1. **Glossary violations** — banned synonyms found in sections (file:line:phrase)
2. **Missing glossary terms** — technical terms used in sections but not defined
3. **Inconsistent term usage** — definition vs actual usage discrepancies
4. **Evidence map discrepancies** — graph vs map vs section references
5. **Literal numbers that should be references** — (file:line:number)
6. **Files moved** — what went where during housekeeping
7. **Sync status** — which sections changed
8. **Build status** — pass/fail

---

## What NOT to do

- Do NOT rewrite any section prose
- Do NOT add terms to the glossary without human approval
- Do NOT change `{{result:...}}` references without human approval
- Do NOT modify `conventions.md`
- Do NOT create new Result artifacts
- Do NOT delete any files (move only)
- Do NOT run `seldon paper build` with rendering (use `--no-render` only)

This is an audit, housekeeping, and registration task. The human will review the
report and give specific instructions for any content changes.
