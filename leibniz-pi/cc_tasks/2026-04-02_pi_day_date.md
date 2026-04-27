# CC Task: Update Paper Date to Pi Day

**Date:** 2026-04-02
**Purpose:** Change the paper date from "March 2026" to "March 14, 2026" (Pi Day) in frontmatter.yml.

---

## Pre-Flight

1. Read `paper/frontmatter.yml`
2. Confirm the current `date:` field value

---

## Steps

### Step 1: Update the date field

In `paper/frontmatter.yml`, change:

```yaml
date: "March 2026"
```

to:

```yaml
date: "March 14, 2026"
```

That's it. One line.

---

## Post-Flight

```bash
seldon paper sync
seldon paper build --no-render
seldon verify --fix
```

---

## Do NOT

- Do not modify any other field in frontmatter.yml
- Do not modify any section files
- Do not modify any existing CC task files
