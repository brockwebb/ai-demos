# CC Task: Epistemic Hedge on Novelty Claim (Section 02)

**Date:** 2026-04-02
**Source:** Editorial review
**Scope:** Single sentence fix in Background section.

---

## Pre-Flight

Read `paper/sections/02_background.md` before editing.

---

## Fix

In `paper/sections/02_background.md`, in subsection "Fitness Design for Convergent Processes", replace:

```
Prior symbolic regression work does not address fitness design for this objective class.
```

With:

```
To our knowledge, prior symbolic regression work does not address fitness design for this objective class.
```

---

## Do NOT

- Do not change anything else in this file
- Do not modify existing CC task files

---

## Post-Flight

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```
