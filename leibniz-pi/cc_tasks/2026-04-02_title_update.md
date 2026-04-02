# CC Task: Title Update

**Date:** 2026-04-02
**Source:** Editorial discussion
**Scope:** Update paper title in frontmatter. Nothing else.

---

## Pre-Flight

Read `paper/frontmatter.yml` before editing.

---

## Fix

In `paper/frontmatter.yml`, replace the title line:

```
title: "The Evaluation Horizon Trap: Why Search Space Structure Dominates Fitness Design"
```

With:

```
title: "The Evaluation Horizon Trap: Why Search Space Structure Dominates Solution Discoverability"
```

No other changes to frontmatter.yml.

---

## Do NOT

- Do not change anything else in frontmatter.yml
- Do not modify any section files (prose QC fixes are in a separate task)
- Do not modify existing CC task files

---

## Post-Flight

```bash
seldon paper sync
seldon paper build --no-render
```
