# CC Task: Final Abstract Tightening (Addendum #2)

**Date:** 2026-03-27
**Priority:** High — replaces previous abstract versions

---

## Context

Previous abstract was too long and did not follow writing conventions (throat-clearing, choppy flow, redundant framing). This version is ~170 words, follows all conventions in `paper/conventions.md`, and reads cleanly.

## Pre-Flight

1. Read `paper/conventions.md`
2. Read `paper/sections/00_abstract.md` (confirm current state)

---

## Step 1: Replace Abstract

Replace the **entire contents** of `paper/sections/00_abstract.md` with:

```markdown
# Abstract

Finite evaluation of an infinite-horizon process cannot distinguish a correct answer from one that merely appears correct within the evaluation horizon. We call these false matches wrong-limit attractors. We study their emergence using genetic programming to discover the Leibniz series for π/4 from arithmetic primitives.

We develop two fitness functions that evaluate convergence across depths rather than pointwise accuracy. The convergence-aware fitness measures error reduction between checkpoints. The log-precision fitness measures precision gain in bits per decade, a second-order convergence criterion. Both rank Leibniz as optimal when present. With 4 terminals, 19 of 20 seeds discovered Leibniz. With 15 at the baseline population, none did. Seven fitness modifications, extended time, and 10x larger populations all failed to shift this boundary. The log-precision threshold must be calibrated below the target's natural precision gain rate; it encodes domain knowledge, not a free parameter.

The bottleneck is coverage, not fitness quality: whether correct building blocks appear in the population before wrong-limit attractors take over. This holds wherever finite evaluation meets infinite-horizon processes. The evaluation function is not the bottleneck. The search space is.
```

---

## Step 2: Conventions Verification

- [ ] Zero em dashes
- [ ] No bold in prose
- [ ] No sentence over 35 words
- [ ] "Log-precision fitness" (correct term)
- [ ] "Discovery"/"discovered" (not "rediscovery")
- [ ] "Coverage" (not "diversity")
- [ ] "We" throughout
- [ ] No throat-clearing ("It is worth noting", etc.)
- [ ] No self-congratulation ("remarkably", "notably", etc.)
- [ ] Active voice throughout
- [ ] No `{{result:...}}` needed (summary counts only)

---

## Step 3: Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

**IMPORTANT:** After `seldon paper sync`, verify that paper.qmd still has its YAML frontmatter block (title, author, date, thanks). If sync stripped it, re-add before rendering.

---

## Do NOT

- Do not add domain examples (RL, LLM, SR) back into the abstract
- Do not add `{{result:...}}` references to the abstract
- Do not modify any other section file
- Do not modify any existing CC task file
- Do not modify _quarto.yml or paper.qmd frontmatter
