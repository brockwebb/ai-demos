# Handoff: Paper Authoring Infrastructure Ready — Start Writing

**Date:** 2026-03-15
**From:** Seldon design thread (Claude Desktop)
**To:** Leibniz-pi paper writing thread (Claude Code or Desktop)

---

## What's New

Seldon now has `seldon paper audit` and `seldon paper build` commands. 215 tests passing. The paper authoring infrastructure is live and ready to use on this project.

### What This Means for Paper Writing

You no longer write literal numbers in prose. You write references like `{{result:entropy_minimal_5_5:value}}` and the build step resolves them from the Seldon graph. If a result is stale, missing, or unverified, the build fails and tells you exactly what's wrong.

You also have automated prose quality checking. `seldon paper audit` scans markdown for convention violations — sentence length, banned words, clichés, em dashes, hedge stacking, and more.

---

## How to Use It

### Step 0: Setup (once)

The paper directory needs a `sections/` subdirectory. Section files go there, numbered for assembly order.

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
mkdir -p paper/sections
```

Copy conventions from template (already done — `paper/paper_qc_config.yaml` and `paper/paper_style_config.yaml` are in place). Write `paper/conventions.md` from the Seldon template:

```bash
cp ~/Documents/GitHub/seldon/templates/paper/conventions.md paper/conventions.md
```

Then add leibniz-pi-specific rules to the bottom of `paper/conventions.md`.

### Step 1: Read Before Writing

Before writing any prose, read:
- `paper/conventions.md` — the writing rules
- `paper/paper_style_config.yaml` — the banned words and clichés list

These encode all the quality standards. Following them during writing is faster than fixing violations after.

### Step 2: Write Sections

Create section files in `paper/sections/` with numeric prefixes:

```
paper/sections/
├── 00_abstract.md
├── 01_introduction.md
├── 02_background.md
├── 03_methods.md
├── 04_results.md
├── 05_discussion.md
├── 06_conclusion.md
└── 07_references.md
```

In every section, use reference syntax for research numbers:

```markdown
The entropy fitness discovered the Leibniz series in
{{result:entropy_minimal_5_5:value}}/5 seeds within
{{result:entropy_minimal_runtime:value}} seconds.
```

**Never write a literal number for a research result.** The reference resolves from the graph at build time. If the result changes, every citation updates automatically.

### Step 3: Check Prose Quality

After writing or editing a section:

```bash
seldon paper audit paper/sections/03_methods.md
```

Or check all sections:

```bash
seldon paper audit paper/sections/*.md
```

This reports Tier 2 violations (sentence too long, missing paragraph structure, em dashes) and Tier 3 findings (banned words, clichés, repetition). Fix Tier 2 issues. Review Tier 3 findings — they're informational.

### Step 4: Build

When sections are ready to assemble:

```bash
# Resolve references + QC, but don't render PDF yet
seldon paper build --no-render

# Full build including Quarto render
seldon paper build

# Quick build, skip prose/style checks
seldon paper build --skip-qc
```

The build will **fail and tell you why** if:
- A `{{result:NAME:value}}` references a result that doesn't exist in the graph
- A referenced result is in `stale` state (needs re-verification)
- A referenced result is still `proposed` (not yet verified)
- A `{{cite:NAME:bibtex_key}}` has no matching entry in `paper/references.bib`
- A `{{figure:NAME:path}}` points to a file that doesn't exist

### Step 5: Iterate

The workflow is: write → audit → fix → build → review output → repeat.

The human reviews **argument quality, voice, and scientific validity**. The system handles **fact-checking, convention compliance, and structural integrity**.

---

## Available Results in the Graph

Run `seldon result list` from the project directory for the current inventory. As of the last dogfood session, 11 verified results are registered. Key ones:

```
entropy_minimal_5_5          — 1.0 (discovery rate, 5 seeds)
entropy_minimal_runtime      — 369.9 (seconds)
info_rate_3_32               — 3.32 (bits/decade)
wrong_limit_ti_15_93         — 15.93 (bits at T=10000)
gp_pop2000_5_5               — 1.0 (GP discovery rate at pop=2000)
```

For full provenance on any result: `seldon result trace <name>`

---

## Available Seldon Commands

```bash
seldon briefing                          # Session start — open tasks, stale results
seldon closeout                          # Session end — structured handoff
seldon result list                       # All results with state
seldon result trace <name>               # Full provenance chain
seldon paper audit [FILES...]            # Tier 2+3 prose/style checks
seldon paper audit --tier 2 [FILES...]   # Prose rules only
seldon paper audit --tier 3 [FILES...]   # Style only
seldon paper build                       # Full build pipeline
seldon paper build --no-render           # Resolve + QC without Quarto
seldon paper build --skip-qc             # Skip Tier 2+3, Tier 1 always runs
seldon paper build --strict              # Tier 2 warnings become errors
seldon status                            # Graph stats
seldon task list --open                  # Open research tasks
```

---

## What's NOT Built Yet (Don't Try to Use)

- `seldon argument` commands (argument skeleton tracking — Phase 4)
- `seldon claim` commands (paragraph-level claim inventory — Phase 4)
- `seldon paper init` (scaffolding — manual setup for now)
- `seldon paper claim-inventory` or `seldon paper perturbation-report`
- SI-04/SI-05/SI-06 checks (depend on claim schema)

These are designed in AD-012 but not implemented. The current tooling covers reference resolution, structural integrity, prose quality, and style checking — which is what you need to start writing.

---

## Open Research Tasks

Run `seldon task list --open` for the full list. From the previous handoff, blocking items include:

- Operations-per-bit efficiency fitness (not implemented)
- Combined optimal config test
- Wrong-limit attractor density formal analysis
- Second-order kinetics proof
- Lit review (Schmidt & Lipson 2009, Cranmer 2023, Hillar & Sommer 2012, Brunton et al. 2016)

---

## Key Files

| File | Purpose |
|------|---------|
| `paper/conventions.md` | Writing rules — READ FIRST |
| `paper/paper_qc_config.yaml` | Tier 2 prose rules (machine-checkable) |
| `paper/paper_style_config.yaml` | Tier 3 banned words/clichés |
| `paper/sections/*.md` | Section files (create these) |
| `paper/references.bib` | BibTeX (create when needed) |
| `seldon.yaml` | Seldon project config |
| `seldon_events.jsonl` | Event log (71+ events) |
| `RESEARCH_NOTES.md` | Findings and preprint outline |
| `v3_results_summary.md` | Master results summary |

---

*The infrastructure is ready. Write the paper.*
