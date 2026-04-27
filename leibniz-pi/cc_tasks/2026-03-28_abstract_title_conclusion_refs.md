# CC Task: Abstract Revision, Title Update, Conclusion Strengthening, References Fix

**Date:** 2026-03-28
**Scope:** 4 targeted edits across paper sections + frontmatter

---

## Pre-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
cat paper/sections/00_abstract.md
cat paper/sections/07_conclusion.md
cat paper/sections/08_references.md
cat paper/frontmatter.yml
seldon paper sync
```

Confirm you can read all four files before proceeding.

---

## Step 1: Replace Abstract

Replace the entire contents of `paper/sections/00_abstract.md` with:

```markdown
# Abstract

Finite evaluation of an infinite-horizon process cannot distinguish a correct answer from one that merely appears correct within the evaluation window. We call these false matches wrong-limit attractors. They arise wherever finite evaluation meets infinite-horizon targets -- in reinforcement learning as reward hacking, in language models as confabulation, in symbolic regression as spurious convergence.

We study their dynamics in a controlled setting: genetic programming tasked with rediscovering the Leibniz series for π/4 from arithmetic primitives. Two fitness functions evaluate convergence across depths rather than pointwise accuracy; both rank Leibniz as optimal when present. With 4 terminals, 19 of 20 seeds discovered Leibniz. With 15, none did. Seven fitness modifications, extended time, and 10x population increases all failed to shift this boundary.

The bottleneck is not fitness quality but coverage: whether correct building blocks appear before wrong-limit attractors dominate. As primitives increase, the space of expressions consistent with the target within the evaluation window grows combinatorially while the target remains a single point. The traps are subtle -- their trajectories fall within measurement resolution of the correct answer at every checkpoint. No amount of fitness engineering, computation time, or population scaling compensates for a search space in which the correct structure is combinatorially outnumbered by indistinguishable impostors.
```

---

## Step 2: Update Title in frontmatter.yml

In `paper/frontmatter.yml`, replace the title line:

**Old:**
```
title: "Wrong-Limit Attractors: Why Constraining the Search Space Dominates Fitness Engineering for Discovery of Convergent Processes"
```

**New:**
```
title: "The Evaluation Horizon Trap: Why Search Space Structure Dominates Fitness Design"
```

---

## Step 3: Strengthen Conclusion Paragraph 3

In `paper/sections/07_conclusion.md`, find the paragraph that begins "This maps directly to machine learning." After the sentence ending "...how many irrelevant primitives are present." add the following two sentences:

```
The mechanism is combinatorial: the number of expressions consistent with the target within the evaluation window grows exponentially with the primitive count, while the target remains a single point. Correct building blocks are not merely hard to find -- they are outnumbered by impostors that finite evaluation cannot distinguish from the real answer.
```

The paragraph should now end:
"...how many irrelevant primitives are present. The mechanism is combinatorial: the number of expressions consistent with the target within the evaluation window grows exponentially with the primitive count, while the target remains a single point. Correct building blocks are not merely hard to find -- they are outnumbered by impostors that finite evaluation cannot distinguish from the real answer."

---

## Step 4: Fix References Placement

Replace the entire contents of `paper/sections/08_references.md` with:

```markdown
# References {.unnumbered}

::: {#refs}
:::
```

The `::: {#refs} :::` div tells Pandoc to place the bibliography at this location instead of appending it after the last section (which currently puts it after the Appendix).

---

## Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify:
1. `check_glossary.py` reports no new violations
2. `seldon paper sync` shows updated content hashes for sections 00, 07, 08
3. `seldon paper build --no-render` resolves all `{{result:NAME:value}}` references without errors

---

## Do NOT

- Do not modify any other section files
- Do not modify existing CC task files
- Do not hardcode any numeric values
- Do not change the font in frontmatter.yml (it should remain Source Sans Pro)
- Do not touch paper.qmd directly -- Seldon build generates it from frontmatter.yml + sections
- Do not rerun any experiments
- Do not use em dashes anywhere
- Do not use "entropy fitness" -- use "log-precision fitness"
