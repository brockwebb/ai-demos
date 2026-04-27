# CC Task: Tighten Abstract (Addendum to 2026-03-27_abstract_rewrite_and_pdf.md)

**Date:** 2026-03-27
**Priority:** High — abstract is too long (~300 words, should be ~200)

---

## Context

The abstract applied by the earlier task is too long. It reads more like an executive summary than an abstract. The domain examples (RL, LLM, SR) are enumerated individually but already appear in the introduction. The abstract should signal generality in one sentence, not re-enumerate.

## Pre-Flight

1. Read `paper/sections/00_abstract.md` (confirm current state)
2. Read `paper/conventions.md`

---

## Step 1: Replace Abstract

Replace the **entire contents** of `paper/sections/00_abstract.md` with:

```markdown
# Abstract

When a search process is evaluated within a finite horizon against a target that requires infinite observation to verify, the evaluation will find outputs that look correct inside that horizon but whose behavior beyond it is unknown. We call these outputs wrong-limit attractors and study their emergence through a controlled experiment: genetic programming discovery of the Leibniz series for π/4 from arithmetic primitives alone.

We develop two fitness functions that evaluate convergence behavior across evaluation depths rather than pointwise accuracy. The convergence-aware fitness asks whether error shrinks between checkpoints. The log-precision fitness measures precision gain in bits per decade, selecting for the constant-rate signature of second-order convergence, an analogy to reaction kinetics. Both correctly identify Leibniz as optimal when it is present in the population.

Discovery exhibits a sharp phase transition. With 4 terminals, 19 of 20 seeds found Leibniz across all population sizes. With 15 terminals at the baseline population, none did. Seven fitness modifications, extended time budgets, and 10x population increases all failed to shift this boundary. The log-precision threshold is itself physically constrained: it must be calibrated below the target process's natural precision gain rate.

The bottleneck is not fitness landscape quality but coverage: the probability that correct building blocks appear before wrong-limit attractors dominate. This structural constraint applies wherever finite evaluation meets infinite-horizon processes. The lever that matters is not a better evaluation function but a more constrained search space.
```

---

## Step 2: Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

**IMPORTANT:** The earlier formatting task (2026-03-27_census_paper_formatting.md) added YAML frontmatter to paper.qmd and modified _quarto.yml. Seldon paper sync may overwrite paper.qmd. If the YAML frontmatter block (title, author, date, thanks) is stripped by sync, re-add it manually before rendering. Check paper.qmd after sync to confirm frontmatter survived.

---

## Do NOT

- Do not add the RL/LLM/SR domain examples back into the abstract
- Do not add `{{result:...}}` references
- Do not modify any other section file
- Do not modify any existing CC task file
- Do not modify _quarto.yml or paper.qmd frontmatter
