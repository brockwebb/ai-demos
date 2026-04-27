# CC Task: Rewrite Introduction + Write Handoff

**Date:** 2026-03-27
**Priority:** High (final pre-abstract task)

---

## Objective

1. Replace Section 01 (Introduction) with the approved rewrite
2. Write session handoff document

---

## Pre-Flight

1. Read `paper/conventions.md`
2. Read `paper/sections/01_introduction.md` — confirm current content before overwriting

---

## Step 1: Replace Introduction

Replace the ENTIRE contents of `paper/sections/01_introduction.md` with the following:

```markdown
# 1. Introduction

Every AI system is evaluated within a finite horizon. Training runs end. Test sets have boundaries. Context windows close. This is not a defect in any particular architecture. It is a structural property of how we build and test all of them. Any search process evaluated within a finite window will find outputs that look correct inside that window. Whether those outputs remain correct beyond it is a question that finite evaluation cannot answer. You cannot close that gap by designing a better test. You can only manage it by constraining the search space. This paper demonstrates that mechanism, gives it a name, and shows through a controlled experiment what works and what does not.

We call these failures *wrong-limit attractors*: outputs of a search process that appear to converge toward a target value within the evaluation window but whose long-term behavior is unknown. They could plausibly converge to the target. They could converge to a nearby but different value. They could eventually diverge. Without carrying evaluation to the limit, we cannot distinguish these cases. They are not overfitting: they genuinely appear to converge. They are not noise: they are structurally coherent. They are not evaluation function errors: the evaluation correctly ranks the right answer above them when both are present. Wrong-limit attractors arise because the gap between finite observation and infinite-horizon behavior is not closable by finite means. As the search space grows, outputs consistent with the target within the evaluation window multiply combinatorially while the actual target remains a single point. At some point, the difference between the target and a wrong-limit attractor's trajectory may fall below the resolution of the evaluation instrument, and the distinction becomes unmeasurable. The problem lives in the space between that resolution floor and the evaluation horizon: deviations large enough to matter, too small to detect within the window.

We study this through a clean, controlled case: can genetic programming rediscover the Leibniz series for π/4 from arithmetic primitives alone?

$$\frac{\pi}{4} = \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots$$

The series converges to π/4 but does so slowly, gaining roughly {{result:info_rate_3_32:value}} bits of precision per decade of terms. Leibniz is an ideal laboratory: the target is known exactly, the search space is enumerable, the failure mode is quantifiable, and success or failure is binary. We develop two fitness functions that evaluate convergence behavior across evaluation depths rather than pointwise accuracy, motivated by an analogy to reaction kinetics developed in Section 6.1. Both correctly identify Leibniz as optimal when it is present. We demonstrate this in a controlled setting where the failure mode can be quantified exactly. The structural argument extends to any finite-horizon evaluation of infinite-horizon processes.

Discovery exhibits a sharp phase transition as the search space grows. With 4 arithmetic primitives, discovery is reliable: 19 of 20 seeds found Leibniz across all tested population sizes. With 15 primitives, discovery fails completely despite the fitness function still ranking Leibniz as optimal. Seven modifications to the fitness function all failed at 15 primitives. Increasing the population by 10x did not shift the failure boundary. Extending the time budget by 4x did not rescue discovery. The bottleneck is not the fitness landscape, which places Leibniz at its global optimum. The bottleneck is coverage: the probability that the correct building blocks appear in the population before wrong-limit attractors dominate. After correcting an initial methodological confound in which the target expression was inadvertently seeded in the population (Section 4.1), all experiments use pure random initialization. The failure conditions are more instructive than the success.

This failure mode is not specific to genetic programming or to the Leibniz problem. Any system that evaluates process behavior within a finite horizon faces the same structural constraint. In reinforcement learning, policies optimized over finite episodes can exploit the reward structure within the evaluation horizon without learning genuinely robust behavior. In large language models, training against finite context windows creates the conditions for confabulation: outputs that appear well-formed and plausible within the training distribution but do not correspond to truth. In symbolic regression, pointwise fitness creates wrong-limit attractors for any problem involving convergence, stability, or asymptotic behavior. The common structure is that finite evaluation of infinite-horizon processes creates a space of outputs that are indistinguishable from the correct answer within the evaluation window. The lever that matters is not a better evaluation function but a more constrained search space.

Section 2 reviews related work on symbolic regression and process-level fitness design. Sections 3 and 4 describe the GP engine, fitness functions, and experimental design, including terminal set construction and the scaling grid. Section 5 presents results: the phase transition, wrong-limit attractor families, parsimony effects, and threshold sensitivity. Sections 6 and 7 discuss the kinetics connection, the confabulation analogy, implications for symbolic regression, and conclude.
```

---

## Step 2: Post-flight checks

1. Run: `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && python paper/prose_qc.py` — confirm Tier 2 = 0
2. Run: `python paper/check_glossary.py` — confirm 0 violations
3. Run: `seldon paper sync`
4. Run: `seldon paper build --no-render`

If prose_qc.py flags any Tier 2 violations (e.g., sentence length), note them but do NOT fix them without explicit approval. The intro was carefully drafted and any reformatting must be reviewed.

---

## Do NOT

- Do not modify any other section files
- Do not overwrite any existing CC task files
- Do not change any `{{result:...}}` references
- Do not "improve" or edit the introduction text — apply it exactly as written above
- Do not fix prose_qc violations without explicit approval
