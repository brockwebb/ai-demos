# CC Task: Replace Abstract and Build Final PDF

**Date:** 2026-03-27
**Priority:** High — final writing task before submission

---

## Pre-Flight

1. Read `paper/conventions.md`
2. Read `paper/sections/00_abstract.md` (confirm it still contains the old GP-centric abstract)
3. Read `paper/sections/01_introduction.md` (first 5 lines — confirm rewrite is applied)
4. Read `paper/sections/07_conclusion.md` (confirm "19 of 20" language)

---

## Step 1: Replace Abstract

Replace the **entire contents** of `paper/sections/00_abstract.md` with the following:

```markdown
# Abstract

When a search process is evaluated within a finite horizon against a target that requires infinite observation to verify, the evaluation will find outputs that look correct inside that horizon but whose behavior beyond it is unknown. We call these outputs wrong-limit attractors and study their emergence through a controlled experiment: genetic programming discovery of the Leibniz series for π/4 from arithmetic primitives alone.

We develop two fitness functions that evaluate convergence behavior across evaluation depths rather than pointwise accuracy. The convergence-aware fitness asks whether error shrinks between checkpoints. The log-precision fitness measures precision gain in bits per decade, selecting for the constant-rate signature of second-order convergence, an analogy to reaction kinetics where the rate depends on interacting quantities rather than a single decaying concentration. Both correctly identify Leibniz as optimal when it is present in the population.

Discovery exhibits a sharp phase transition as the search space grows. With 4 terminals, 19 of 20 seeds found Leibniz across all population sizes. With 15 terminals at the baseline population, none did. Seven fitness modifications, extended time budgets, and 10x population increases all failed to shift this boundary. The log-precision fitness threshold is itself physically constrained: it must be calibrated below the target process's natural precision gain rate, confirming that the fitness encodes domain knowledge about the convergence structure it selects for.

The bottleneck is not fitness landscape quality. The fitness places Leibniz at the global optimum in every configuration tested. The bottleneck is coverage: the probability that correct building blocks appear in the population before wrong-limit attractors dominate. This structural constraint applies wherever finite evaluation meets infinite-horizon processes. Reinforcement learning policies can exploit finite-episode reward structures. Large language models trained against finite context windows produce confabulations that appear well-formed within the training distribution. Symbolic regression with pointwise fitness creates wrong-limit attractors for any convergence problem. The lever that matters is not a better evaluation function but a more constrained search space.
```

---

## Step 2: Verify Conventions Compliance

After writing the file, verify:
- [ ] Zero em dashes in the file
- [ ] No bold in prose (only the `# Abstract` heading)
- [ ] No sentences over 35 words
- [ ] "Log-precision fitness" not "entropy fitness"
- [ ] "Discovery" not "rediscovery"
- [ ] No "novel"
- [ ] "We" used for first person
- [ ] No `{{result:...}}` templates needed (abstract uses no measured values — "19 of 20" is from the conclusion's corrected count, not a Seldon reference)

Note: "19 of 20 seeds" is a summary statement matching the conclusion. It does not require a `{{result:...}}` reference because it aggregates across the entire scaling grid (multiple Seldon results). The conclusion uses the same literal phrasing.

---

## Step 3: Post-Flight

Run in order:

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

Report any errors. If PDF builds successfully, confirm the abstract renders on the first page.

---

## Step 4: Final PDF Verification

Open the generated PDF and verify:
- Abstract appears on page 1
- Table of contents (if present) is correct
- All figures render (Figures 1-5)
- All tables render (Tables 1-8)
- Bibliography appears at end
- No broken `{{result:...}}` references visible in rendered text
- No orphan `\bibliography{references}` command visible

---

## Do NOT

- Do not modify any file other than `paper/sections/00_abstract.md`
- Do not add `{{result:...}}` references to the abstract
- Do not change "19 of 20" to a Seldon reference
- Do not add em dashes
- Do not rerun any experiments
- Do not modify this task file
