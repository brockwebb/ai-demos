# CC Task: Fix QC Violations in Introduction

**Date:** 2026-03-27
**Priority:** High (Tier 1 build-blocking violations)
**Context:** Introduction rewrite triggered PQ-02, SP-01, SP-03, and glossary violations. All fixes are mechanical and preserve meaning.

---

## Pre-Flight

1. Read `paper/conventions.md`
2. Read `paper/sections/01_introduction.md` before editing

---

## Fix 1: "evaluation window" → "evaluation horizon" (glossary violation, 2 instances)

"Evaluation horizon" is the controlled vocabulary term. Replace all instances of "evaluation window" with "evaluation horizon."

In paragraph 1, find:
```
Any search process evaluated within a finite window will find outputs that look correct inside that window.
```
Replace with:
```
Any search process evaluated within a finite horizon will find outputs that look correct inside that horizon.
```

In paragraph 2, find:
```
outputs of a search process that appear to converge toward a target value within the evaluation window but whose long-term behavior is unknown.
```
Replace with:
```
outputs of a search process that appear to converge toward a target value within the evaluation horizon but whose long-term behavior is unknown.
```

In paragraph 2, find:
```
outputs consistent with the target within the evaluation window multiply combinatorially
```
Replace with:
```
outputs consistent with the target within the evaluation horizon multiply combinatorially
```

In paragraph 2, find:
```
too small to detect within the window.
```
Replace with:
```
too small to detect within the horizon.
```

In paragraph 5, find:
```
within the evaluation window. The lever
```
Replace with:
```
within the evaluation horizon. The lever
```

---

## Fix 2: "robust" → replacement (SP-01 banned word)

In paragraph 5, find:
```
without learning genuinely robust behavior
```
Replace with:
```
without learning genuinely reliable behavior
```

---

## Fix 3: Split long paragraphs (PQ-02)

### Paragraph 1 (11 sentences → split into two)

After this sentence:
```
Whether those outputs remain correct beyond it is a question that finite evaluation cannot answer.
```

Insert a paragraph break (blank line). This creates:
- Paragraph 1a (5 sentences): The structural reality — finite evaluation is universal
- Paragraph 1b (6 sentences): The consequence — gap can't be closed by better tests

### Paragraph 2 (12 sentences → split into two)

After this sentence:
```
Without carrying evaluation to the limit, we cannot distinguish these cases.
```

Insert a paragraph break (blank line). This creates:
- Paragraph 2a (6 sentences): What wrong-limit attractors are, epistemologically
- Paragraph 2b (6 sentences): Why they arise, how they scale, the resolution limit

### Paragraph 5 (10 sentences → split into two)

After this sentence:
```
Any system that evaluates process behavior within a finite horizon faces the same structural constraint.
```

Insert a paragraph break (blank line). This creates:
- Paragraph 5a (2 sentences): The general claim
- Paragraph 5b (remaining): The specific domain examples (RL, LLM, SR) and the actionable conclusion

---

## Fix 4: Merge single-sentence paragraphs (PQ-02)

The line "We study this through a clean, controlled case: can genetic programming rediscover the Leibniz series for π/4 from arithmetic primitives alone?" is a standalone paragraph followed by the LaTeX formula and then another paragraph.

Merge this sentence into the paragraph that follows the formula. The result should read as one paragraph:

```
We study this through a clean, controlled case: can genetic programming rediscover the Leibniz series for π/4 from arithmetic primitives alone?

$$\frac{\pi}{4} = \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots$$

The series converges to π/4 but does so slowly, gaining roughly {{result:info_rate_3_32:value}} bits of precision per decade of terms.
```

NOTE: If the QC tool counts this as two separate paragraphs because of the LaTeX block, leave as is. The formula must remain on its own line for rendering. If QC still flags it, report the violation but do not restructure further.

---

## Fix 5: Reduce word repetition (SP-03)

The flagged words are "within" ×5, "finite" ×5, "horizon" ×3, "search" ×4. After fixes 1-4, recount. Some repetition is unavoidable given the subject matter (these are the core concepts). Do NOT introduce synonyms that violate the glossary. If repetition count drops below the threshold after the other fixes, no further action needed.

If still flagged after fixes 1-4, look for opportunities to cut redundant uses without changing meaning. Do not replace "evaluation horizon" with any synonym (it is the controlled term). Do not replace "search space" with any synonym. "Finite" may be reducible by restructuring sentences.

---

## Post-Flight

1. Run: `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && python paper/prose_qc.py` — target Tier 1 = 0, Tier 2 = 0
2. Run: `python paper/check_glossary.py` — confirm 0 violations
3. Run: `seldon paper sync`
4. Run: `seldon paper build --no-render`

Report any remaining violations. Do not attempt additional fixes without approval.

---

## Do NOT

- Do not change the meaning or tone of any sentence
- Do not add or remove content beyond paragraph splits, merges, and word replacements specified above
- Do not overwrite any existing CC task files
- Do not "improve" the prose — these are mechanical QC fixes only
