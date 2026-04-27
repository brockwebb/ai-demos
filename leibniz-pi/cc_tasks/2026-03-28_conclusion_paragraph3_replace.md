# CC Task: Replace Conclusion Paragraph 3 and Trim Redundancy

**Date:** 2026-03-28
**Scope:** `paper/sections/07_conclusion.md`

---

## Pre-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
cat paper/sections/07_conclusion.md
```

---

## Step 1: Replace paragraph 3 of the Conclusion

In `paper/sections/07_conclusion.md`, find the paragraph that begins with:

> "This maps directly to machine learning."

and ends with:

> "Correct building blocks are not merely hard to find -- they are outnumbered by impostors that finite evaluation cannot distinguish from the real answer."

REPLACE that entire paragraph with:

> This is not specific to genetic programming. A specific prompt constrains an LLM's search space, fewer plausible-looking wrong answers survive the completion process. Curating training data removes irrelevant primitives before the search begins. In both cases, the intervention that works is not a better objective function or more compute but a smaller, cleaner space of candidates. Our scaling grid is a controlled demonstration: same algorithm, same fitness, same target, success or failure determined entirely by how much irrelevant material is in the search space.

Note: no em dashes anywhere in this replacement text. The comma after "search space" in sentence 1 is intentional.

---

## Step 2: Verify flow

After replacement, the conclusion should read:

- Paragraph 1: "Constrain the search space..." (results summary)
- Paragraph 2: "No fitness modification fixed this..." (negative results)
- Paragraph 3: "This is not specific to genetic programming..." (outward connections, NEW)
- Paragraph 4: "Three directions address the coverage bottleneck..." (future work)

Confirm all four paragraphs flow naturally.

---

## Step 3: Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/prose_qc.py paper/sections/07_conclusion.md
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

---

## Do NOT

- Do not modify any other section file
- Do not modify any existing CC task file
- Do not re-add the combinatorial mechanism explanation (the reader already knows it)
- Do not add em dashes anywhere
