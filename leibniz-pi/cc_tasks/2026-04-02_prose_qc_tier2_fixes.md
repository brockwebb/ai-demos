# CC Task: Prose QC Fixes (Tier 2)

**Date:** 2026-04-02
**Source:** Prose QC run (local replication of `paper/prose_qc.py` checks)
**Scope:** Fix all Tier 2 violations. Leave Tier 3 warnings (25-30 word sentences) unless a split is trivial.

---

## Pre-Flight

Read each file before editing:
- `paper/sections/01_introduction.md`
- `paper/sections/03_methods.md`
- `paper/sections/05_results.md`
- `paper/sections/06_discussion.md`
- `paper/conventions.md`
- `paper/glossary.md`

---

## Fixes

### 1. Section 01 — Introduction

**1a. Staccato fix (lines 3-5).**

Replace the opening five sentences:

```
Every AI system is evaluated within a finite horizon. Training runs end. Test sets have boundaries. Context windows close. This is not a defect in any particular architecture. It is a structural property of how we build and test all of them.
```

With:

```
Every AI system is evaluated within a finite horizon. Training runs end, test sets have boundaries, and context windows close. This is not a defect in any particular architecture; it is a structural property of how we build and test all of them.
```

This merges three staccato fragments into one comma-list sentence, and merges two ambiguous-pronoun sentences into one compound sentence with semicolon. Net: 5 sentences → 3 sentences, same content.

**1b. Over-length sentence (LLM confabulation sentence, ~31 words).**

Find the sentence starting "In large language models, training against finite context windows creates the conditions for confabulation..." — it runs ~31 words. Split it:

Current:
```
In large language models, training against finite context windows creates the conditions for confabulation [@Ji2023Hallucination; @NIST2024AI600]: outputs that appear well-formed and plausible within the training distribution but do not correspond to truth.
```

Replace with:
```
In large language models, training against finite context windows creates the conditions for confabulation [@Ji2023Hallucination; @NIST2024AI600]. The resulting outputs appear well-formed and plausible within the training distribution but do not correspond to truth.
```

### 2. Section 03 — Methods

**2a. Diversity injection sentence (~32 words).**

Current:
```
A diversity injection mechanism replaces the worst 100 individuals with fresh random trees when the top 20 fitness values become identical (to six decimal places), preventing premature convergence to a single attractor.
```

Replace with:
```
A diversity injection mechanism replaces the worst 100 individuals with fresh random trees when the top 20 fitness values become identical to six decimal places. This prevents premature convergence to a single attractor.
```

**2b. Fitness formula definitions (~38 words each).** These are inline formula explanations. They are inherently long because they define multiple variables in one sentence. Leave these as-is — splitting a "where X = ..., Y = ..., Z = ..." definition across sentences makes it harder to read, not easier. **No action.**

### 3. Section 05 — Results

**3a. Wrong-limit attractor sentence (~32 words).**

Current:
```
Its partial sums converge to a value that appears closer to π/4 than Leibniz within the evaluation horizon, but at T→∞, Leibniz converges exactly while this attractor converges to a different value.
```

Replace with:
```
Within the evaluation horizon, its partial sums converge to a value that appears closer to π/4 than Leibniz. At T→∞, Leibniz converges exactly while this attractor converges to a different value.
```

**3b. Population scaling sentence (~33 words).**

Current:
```
Increasing population from 1,000 to 10,000 does not shift this boundary: it provides marginal gains at t=6 and t=8 and produces the anomalous partial recovery at t=15, but the t=10 wall remains intact.
```

Replace with:
```
Increasing population from 1,000 to 10,000 does not shift this boundary. Larger populations provide marginal gains at t=6 and t=8 and produce the anomalous partial recovery at t=15, but the t=10 wall remains intact.
```

**3c. Ambiguous pronoun at end of Section 5.6.**

Current:
```
It is constrained by the problem, not freely tunable.
```

Replace with:
```
The threshold is constrained by the problem, not freely tunable.
```

### 4. Section 06 — Discussion

**4a. Road-map sentence at top (~34 words).**

Current:
```
We first analyze the convergence structure that makes Leibniz detectable (6.1), then generalize the discovery mechanism (6.2), draw the analogy to broader AI systems (6.3), and identify implications for the symbolic regression community (6.4).
```

Replace with:
```
We first analyze the convergence structure that makes Leibniz detectable (6.1), then generalize the discovery mechanism (6.2). Sections 6.3 and 6.4 draw the analogy to broader AI systems and identify implications for symbolic regression.
```

**4b. Gradient-based selection sentence (~31 words).**

Current:
```
The gradient-based selection variant minimized the gradient norm across fitness dimensions (precision, monotonicity, rate, and parsimony balance), selecting for expressions where perturbing the tree produced the smallest change across all dimensions.
```

Replace with:
```
The gradient-based selection variant minimized the gradient norm across fitness dimensions (precision, monotonicity, rate, and parsimony balance). It selected for expressions where perturbing the tree produced the smallest change across all dimensions.
```

**4c. Sastry population-sizing sentence (~36 words).**

Current:
```
@Sastry2005PopulationSizing derived a population-sizing relationship for GP from building-block decision-making theory, showing that the required population grows with the number of building blocks that must be simultaneously present and the difficulty of distinguishing them under selection.
```

Replace with:
```
@Sastry2005PopulationSizing derived a population-sizing relationship for GP from building-block decision-making theory. The required population grows with the number of building blocks that must be simultaneously present and the difficulty of distinguishing them under selection.
```

**4d. Phase transition sentence (~31 words).**

Current:
```
The phase transition occurs where coverage/search_space drops below the threshold needed for the correct building blocks to appear in the initial population and survive long enough for selection to assemble them.
```

This is 30 words by my count and borderline. Leave as-is unless the actual QC script flags it at >30. **No action unless flagged.**

**4e. Population range sentence (~41 words). This is the worst offender.**

Current:
```
Our population range (1,000 to 10,000) does not reach the scales tested in some GP studies; however, the sharpness of the transition between t=8 and t=10, which holds across a 10x population range, suggests the bottleneck is structural rather than computational.
```

Replace with:
```
Our population range (1,000 to 10,000) does not reach the scales tested in some GP studies. The sharpness of the transition between t=8 and t=10, holding across a 10x population range, suggests the bottleneck is structural rather than computational.
```

**4f. Confabulation analogy sentence (~40 words).**

Current:
```
A language model that generates a plausible citation to a paper that does not exist exhibits the same structure: the output is locally consistent within the generation horizon (correct formatting, topically relevant author names, reasonable year) but false under verification.
```

Replace with:
```
A language model that generates a plausible citation to a paper that does not exist exhibits the same structure. The output is locally consistent within the generation horizon (correct formatting, topically relevant author names, reasonable year) but false under verification.
```

---

## Do NOT

- Do not change any Tier 3 warnings (25-30 word sentences) unless explicitly listed above
- Do not touch Section 07 (Conclusion) — the staccato there is intentional
- Do not touch the inline fitness formula definitions in Section 03 (the "where X = ..." sentences)
- Do not change any `{{result:...}}` references
- Do not use em dashes anywhere
- Do not modify existing CC task files
- Do not reword beyond the specific replacements above — these are surgical edits

---

## Post-Flight

After all edits:

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify no new violations introduced. Report the final `prose_qc.py` output.

---

## Verification

Run `python paper/prose_qc.py` after all edits. Expected: 0 Tier 2 violations in sections 01, 03, 05, 06. Section 07 staccato flags are accepted and not fixed.
