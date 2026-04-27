# CC Task: Remove Crystallization, Design Provenance, and Defensive Disclaimers

**Date:** 2026-03-28
**Scope:** `paper/sections/03_methods.md`, `paper/sections/05_results.md`, `paper/sections/06_discussion.md`

---

## Pre-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
cat paper/sections/03_methods.md
cat paper/sections/05_results.md
cat paper/sections/06_discussion.md
```

---

## Step 1: Remove crystallization paragraph from Section 3.3.2

In `paper/sections/03_methods.md`, find and DELETE the entire paragraph that begins with:

> "The design came from a chemical engineering perspective on process dynamics."

and ends with:

> "This connection is discussed in Section 6.1."

This is the paragraph between the fitness equation/weights description and the paragraph starting "By the same kinetics analogy..."

DELETE that entire paragraph. Do not replace it with anything.

After deletion, text flows from:

> Weights: w_1 = 0.02, w_2 = 0.04, w_3 = 0.03, λ_p = 0.005.

directly to:

> By the same kinetics analogy, this asks a "second-order" question...

---

## Step 2: Delete Section 6.5 entirely

In `paper/sections/06_discussion.md`, find the subsection:

> ## Design Provenance and Disciplinary Lens

DELETE the entire subsection -- heading and all content below it, up to the end of the file (it is the last subsection in Section 6).

Do NOT add any replacement text. Nothing from 6.5 is salvaged.

---

## Step 3: Remove defensive disclaiming paragraph from Section 6.1

In `paper/sections/06_discussion.md`, in the "Second-Order Kinetics Connection" subsection, find and DELETE the paragraph that begins with:

> "We present this as a structural observation recognized after the experiment, not a design input or proven result."

and ends with:

> "The mathematical correspondence should not be taken beyond the specific decay-rate relationship described here."

DELETE that entire paragraph.

---

## Step 4: Remove self-congratulatory paragraph from Section 6.1

In `paper/sections/06_discussion.md`, in the "Second-Order Kinetics Connection" subsection, find and DELETE the paragraph that begins with:

> "The design intuition and the kinetics mathematics arrived at the same place by independent routes."

and ends with:

> "provides stronger grounds for the fitness design than either would alone."

DELETE that entire paragraph.

After Steps 3 and 4, Section 6.1 should end with the paragraph about the log-precision fitness asking a second-order question and fewer processes satisfying the second-order criterion.

---

## Step 5: Fix last sentence of Section 5.6

In `paper/sections/05_results.md`, in the "Threshold Sensitivity" subsection, find the last sentence:

> "This sensitivity confirms that the log-precision fitness encodes domain knowledge about the target process's convergence rate. The threshold is constrained by the physics of the problem, not freely tunable."

Replace with:

> "The threshold must be set below the target process's natural gain rate. It is constrained by the problem, not freely tunable."

---

## Step 6: Check for stale cross-references

Search ALL section files for:
- "Section 6.5"
- "Design Provenance"
- Any forward-reference to crystallization or disciplinary lens

If any exist, remove them.

---

## Step 7: Verify untouched sections

Confirm the following are UNCHANGED:
- Section 3.3.1 (convergence-aware fitness) -- "first-order" label stays
- Section 6.1 -- only the two paragraphs specified above are removed, everything else untouched
- Sections 6.2, 6.3, 6.4 -- untouched
- Section 00 (Abstract) -- untouched
- Sections 01, 02, 04, 07 -- untouched

---

## Step 8: Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/prose_qc.py paper/sections/03_methods.md
python paper/prose_qc.py paper/sections/05_results.md
python paper/prose_qc.py paper/sections/06_discussion.md
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

---

## Do NOT

- Do not remove the "first-order" or "second-order" kinetics labels from 3.3.1 or 3.3.2
- Do not modify Section 6.1 beyond deleting the two paragraphs specified in Steps 3 and 4
- Do not add any replacement text for deleted content
- Do not modify any existing CC task file
- Do not modify the abstract, introduction, or conclusion
