# CC Task: Leibniz-Pi Documentation Backfill via `seldon artifact update`

**Date:** 2026-03-16
**Project:** leibniz-pi (`~/Documents/GitHub/ai-demos/leibniz-pi/`)
**Goal:** Bring documentation completeness from 28% to 90%+ by backfilling documentation-category properties on all artifacts using `seldon artifact update`.

---

## Context

`seldon go` reports 13/45 artifacts fully documented (28%). The gap is documentation-category properties (as defined in `research.yaml`) that were not set during the initial bootstrap. The new `seldon artifact update` CLI command makes this feasible without Python REPL hacks.

**Important:** Run all commands from the leibniz-pi project directory:
```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
```

Seldon reads `seldon.yaml` from cwd to find the Neo4j database (`seldon-leibniz-pi`).

---

## Step 0: Get the Gap Report

Run `seldon docs check` from the project directory. This produces a per-artifact report of missing documentation properties. Use this output to drive all subsequent steps — do NOT guess which properties are missing.

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
seldon docs check
```

Capture the output. It tells you exactly which artifacts need which properties.

---

## Step 1: Backfill Script Artifacts (9 scripts, up to 6 doc properties each)

Documentation properties for Script: `description`, `inputs`, `outputs`, `parameters`, `usage`, `dependencies`.

For each Script artifact reported as incomplete by `seldon docs check`:

1. Read the actual script file (the `path` property tells you where it is)
2. Determine accurate values for each missing doc property by reading the code
3. Update via CLI:

```bash
seldon artifact update <id-or-prefix> \
  -p "description=<what it does, 1-2 sentences>" \
  -p "inputs=<input files or parameters>" \
  -p "outputs=<what it produces: results files, CSVs, etc.>" \
  -p "parameters=<configurable params and defaults, or N/A for libraries>" \
  -p "usage=<how to run: python3 script.py [args]>" \
  -p "dependencies=<required packages, data files>"
```

**Key scripts to expect** (from CLAUDE.md):
- `gp_leibniz_v3_wide.py`, `gp_leibniz_v3_hostile.py`, `gp_leibniz_v3_minimal.py`
- `gp_sensitivity_sweep.py`
- `entropy_leibniz_v3_wide.py`, `entropy_leibniz_v3_hostile.py`, `entropy_leibniz_v3_minimal.py`
- `entropy_stress_test.py`, `fitness_sensitivity_test.py`

Read each script file to get accurate info. Do NOT fabricate descriptions — read the code.

---

## Step 2: Backfill Result Artifacts (11 results, up to 2 doc properties each)

Documentation properties for Result: `interpretation`, `methodology_note`.

For each Result artifact reported as incomplete:

1. Check existing properties via `seldon artifact show <id-or-prefix>` — the `value`, `units`, and `description` are already set
2. Determine `interpretation` (what the value means in context) and `methodology_note` (how computed) from:
   - `RESEARCH_NOTES.md`
   - `v3_results_summary.md`
   - The generating script (follow `GENERATED_BY` relationship)
3. Update:

```bash
seldon artifact update <id-or-prefix> \
  -p "interpretation=<what this value means in context>" \
  -p "methodology_note=<brief computation method>"
```

---

## Step 3: Backfill DataFile Artifacts (5 data files, up to 4 doc properties each)

Documentation properties for DataFile: `format`, `schema_description`, `provenance_description`, `row_count`.

For each DataFile reported as incomplete:

1. Locate the file on disk (the `path` property tells you)
2. Inspect it: `head -5 <file>` for format/schema, `wc -l <file>` for row count
3. Update:

```bash
seldon artifact update <id-or-prefix> \
  -p "format=<CSV|JSON|JSONL|etc.>" \
  -p "schema_description=<columns/fields and their meanings>" \
  -p "provenance_description=<how produced>" \
  -p "row_count=<approximate number of records>"
```

---

## Step 4: Backfill PaperSection Artifacts (7 sections, 1 doc property each)

Documentation property for PaperSection: `file_path`.

```bash
seldon artifact update <id-or-prefix> -p "file_path=paper/sections/<filename>.md"
```

Check `paper/sections/` for actual filenames. If sections don't have files yet (not written), use `file_path=not yet created` — honest is better than fabricated.

---

## Step 5: Verify

Run `seldon docs check` again. Target: 90%+ documentation completeness (some artifacts may legitimately have N/A properties — that's fine if the value is explicitly set to "N/A" rather than missing).

Then run `seldon docs generate` to produce updated reference docs.

---

## Success Criteria

- `seldon docs check` reports 90%+ fully documented (up from 28%)
- All property values are accurate (derived from reading actual code/data, not fabricated)
- `seldon docs generate` produces clean reference docs
- No errors in JSONL event log from the updates

---

## What NOT to Do

- Do NOT fabricate property values. If you can't determine a value, set it to "N/A" or "Unknown — needs investigation" with a note.
- Do NOT modify the actual script/data files — only update Seldon artifact properties.
- Do NOT change artifact states (proposed/verified/etc.) — this task is documentation only.
- Do NOT create new artifacts — only update existing ones.
- Do NOT skip the initial `seldon docs check` — let the tool tell you what's missing rather than guessing.
- Do NOT run experiments or touch any running simulations.
