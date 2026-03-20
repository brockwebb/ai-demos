# CC Task: Introduction Section (01) Review Edits

**Date:** 2026-03-18
**Scope:** `paper/sections/01_introduction.md`
**Constraint:** All numbers must come from source scripts or data files. No hardcoded values. Follow `paper/conventions.md` and `paper/glossary.md`.

---

## Pre-flight

1. `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
2. Read `paper/conventions.md` and `paper/glossary.md` before writing any prose.
3. Read current state of `paper/sections/01_introduction.md`.
4. Read `paper/sections/06_discussion.md` Section 6.3 (confabulation analogy) and Section 6.1 (kinetics) for reference. Do not edit.
5. Read `paper/sections/07_conclusion.md` for reference. Do not edit.

---

## Task 1: Fix anthropomorphizing in paragraph 1

The current closing clause of paragraph 1 reads:

> "a process that approaches its target monotonically, each term a smaller correction than the last, improving forever without arriving."

This anthropomorphizes the series ("improving," "arriving") and is technically wrong (the series does converge in the limit). Replace with a factual characterization. Something like:

> "a process whose error decreases algebraically as 1/T, gaining roughly 3.3 bits of precision per decade of terms."

Use `{{result:info_rate_3_32:value}}` for the bits-per-decade number. Discover the exact decay rate characterization from `RESEARCH_NOTES.md` or `RESEARCH_NOTES_SUPP_design_motivation.md` if needed to confirm the 1/T framing.

---

## Task 2: Tighten "conditionally yes"

Paragraph 2 currently reads:

> "The answer is conditionally yes. The conditions under which discovery fails are more instructive than the conditions under which it succeeds."

The conditions are the whole point of the paper. Name them here. Replace with something like:

> "The answer is yes when the terminal set is small enough that correct building blocks dominate the search space, and no when additional terminals drown the signal in combinatorial alternatives. The failure conditions are more instructive than the success."

Keep to two sentences max. Active voice.

---

## Task 3: Simplify kinetics framing

Paragraph 4 currently introduces the "first-order question" / "second-order question" kinetics analogy. This is too much machinery for the introduction. The reader hasn't encountered Section 6.1 yet.

Simplify to plain language. Replace the kinetics-specific framing with the operational distinction:

- Convergence-aware fitness: rewards expressions whose error shrinks between checkpoints.
- Log-precision fitness: rewards expressions that gain precision at a constant rate across scales.

Keep the sentence noting log-precision is more reliable (succeeds at half the population size). Drop the "first-order" / "second-order" labels and the "(see Section 6.1)" reference from this paragraph. The kinetics connection can be mentioned in passing ("motivated by an analogy to reaction kinetics developed in Section 6.1") but should not be the framing device here.

The key framing for the intro: the research question was about learning to ask the right questions of an optimizer. Pointwise accuracy is the wrong question. Process-level behavior (is it still improving? at what rate? is the rate sustained?) is the right question. The fitness functions encode different versions of that question.

---

## Task 4: Define "wrong-limit attractor" on first use

Paragraph 5 uses "wrong-limit attractors" without a crisp definition. The conventions doc requires definition on first use.

Add a definition sentence when the term first appears. Something like:

> "We call these wrong-limit attractors: expressions whose partial sums converge, but to a value other than the target."

Then the existing description of their behavior follows naturally. Check `paper/glossary.md` for the authoritative definition and use it.

---

## Task 5: Define "coverage" on first use

Paragraph 6 uses "coverage" without definition. Conventions doc defines it as "the fraction of structurally distinct building blocks present in the population."

Add the definition on first use in paragraph 6. One sentence.

---

## Task 6: Preview the confabulation analogy

The Discussion (6.3) develops the confabulation analogy (wrong-limit attractors as analogous to LLM confabulation). The Introduction currently does not mention this.

Add one sentence, either at the end of paragraph 5 or in paragraph 6, previewing this connection. Something like:

> "The failure mode parallels confabulation in language models: outputs that appear correct within a finite evaluation window but do not correspond to the true target (Section 6.3)."

One sentence only. Do not develop the analogy here.

---

## Task 7: Mention injection confound

The intro says "from scratch" but never acknowledges that the first attempt planted the answer accidentally. Add a brief mention, either in paragraph 2 or as a parenthetical where "from scratch" appears.

Something like:

> "After correcting an initial methodological confound in which the target expression was inadvertently seeded in the population (Section 4.1), all experiments use pure random initialization."

One sentence. The experimental design section handles the details.

---

## Task 8: Add roadmap paragraph

Add a final paragraph to the introduction that orients the reader to the paper structure. Brief, one paragraph, no bullet points (conventions doc prohibits them in prose). Cover:

- Section 2: background
- Section 3: methods (fitness functions, expression representation)
- Section 4: experimental design (terminal sets, scaling grid)
- Section 5: results (phase transition, wrong-limit attractors, parsimony)
- Section 6: discussion (kinetics connection, confabulation analogy, implications for symbolic regression)
- Section 7: conclusion

Keep it to 3-4 sentences. Do not describe every section in detail. Orient, don't summarize.

---

## Post-flight

After all edits:

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify Tier 1 clean. Report any new warnings.

---

## Do NOT

- Do not edit any section file other than `paper/sections/01_introduction.md`.
- Do not hardcode any values. All numbers come from source scripts, data files, or Seldon results.
- Do not overwrite any existing CC task files.
- Do not add bold in prose. Do not use em dashes. Follow `conventions.md`.
- Do not add speculative text. Every claim must trace to source.
- Do not over-develop the kinetics analogy, confabulation analogy, or injection confound in the intro. One sentence each. The relevant sections handle the details.
