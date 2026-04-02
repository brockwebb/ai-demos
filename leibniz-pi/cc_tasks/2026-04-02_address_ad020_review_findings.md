# CC Task: Leibniz-Pi Paper — Address AD-020 Review Findings

**Date:** 2026-04-02
**Project:** leibniz-pi (Seldon-managed: `seldon-leibniz-pi` database)
**Reference:** AD-020 dogfood run, `audits/paper_review_synthesis.yaml`
**Scope:** Address clusters 1-5, 7-8 from the review synthesis. Cluster 6 (heatmap) is dismissed — the table is a deliberate design choice.

---

## Environment Setup

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
set -a; source .env; set +a
seldon go --project-dir .
```

Read `audits/paper_review_synthesis.yaml` for full context on each cluster.

## Mandatory Post-Edit Cycle

After EVERY prose change to a section file:
```bash
python paper/check_glossary.py
seldon paper sync --project-dir .
seldon paper build --no-render --project-dir .
```

---

## Cluster 1: t=15 Overstatement (CRITICAL — convergence 4)

**Problem:** Abstract says "With 15, none did." Conclusion says same. Table 5 shows 2/5 at t=15/pop=10,000. Appendix shows 3 total discoveries at t=15 across fitness functions.

**Action:** Option A — qualify the claim. This is more honest than reframing.

1. Edit `paper/sections/00_abstract.md`:
   - Change "With 15, none did" to language that accurately reflects the data: at populations up to 5,000 none discovered Leibniz; at pop=10,000 a partial recovery appeared at t=15 (2/5) but not at adjacent terminal counts.
   - The "19 of 20" claim should also get a parenthetical: "(log-precision fitness)" per unclustered finding CS-03.

2. Edit `paper/sections/07_conclusion.md`:
   - Same fix. Abstract and conclusion must agree.

3. Verify: After edits, grep both files for "15" and "none" to confirm no stale phrasing remains.

4. Update evidence map if the phrasing change introduces a new result reference.

## Cluster 2: Cross-Domain Citations (convergence 3)

**Problem:** Introduction claims wrong-limit attractors manifest as reward hacking (RL) and confabulation (LLMs) with zero citations. Discussion 6.3 develops the analogy but stays abstract. Conclusion proposes only GP-specific future work.

**Action:**

1. Edit `paper/sections/01_introduction.md`:
   - Add citations to the paragraph that makes the cross-domain claims. Target refs:
     - Reward hacking: Skalse et al. 2022 ("Defining and Characterizing Reward Hacking") or Amodei et al. 2016 ("Concrete Problems in AI Safety")
     - Confabulation/hallucination: Ji et al. 2023 ("Survey of Hallucination in NLG") or Huang et al. 2023
     - NIST AI 600-1 for the "confabulation" terminology choice (already in glossary as rationale)
   - Add these to `references.bib` first.

2. Edit `paper/sections/06_discussion.md` (Section 6.3):
   - Add one concrete LLM example: e.g., "A language model that generates a plausible-sounding citation to a non-existent paper is exhibiting the same structural failure — the output is locally consistent within the generation horizon but false under verification."

3. Edit `paper/sections/07_conclusion.md`:
   - Add one non-GP future direction: e.g., detecting wrong-limit attractor analogs in RL reward learning or in LLM evaluation benchmarks.

4. Run `seldon paper sync` after each file edit.

## Cluster 3: Wrong-Limit Attractor Dominance Overstated (convergence 3)

**Problem:** Paper frames wrong-limit attractors as THE failure mode, but at t=15/pop=1000 the actual failure was 4/5 trivial constants and 1/5 wrong-limit attractor. The strong evidence for systematic attractor dominance is at t=20/pop=10,000 (appendix only).

**Action:**

1. Edit `paper/sections/05_results.md` (Section 5.2):
   - Clarify: at t=15/pop=1000, the dominant failure is trivial collapse (constants near π/4). Wrong-limit attractors become the dominant failure mode at higher populations and terminal counts.
   - Reference the t=20/pop=10,000 power-law family from the appendix as the strongest systematic evidence.

2. Consider whether the Grandi-Leibniz attractor analysis (Appendix A.2.3) or the population inversion effect (t=8) warrant a sentence or footnote in the main text. Author decision — don't force it if the section is already long.

3. This is a framing fix, not a data fix. No numbers change. The claim becomes more precise, not weaker.

## Cluster 4: Evidence Map Gaps (convergence 2)

**Problem:** 8 results used in paper not in `evidence_map.md`. Figure inventory says TBD. Table count stale (lists 5, paper has 8).

**Action:**

1. Read `audits/paper_content_audit.yaml` for the specific result IDs (CR-01 through CR-08).
2. Add each to `evidence_map.md` with provenance (script, data source, verification).
3. Update figure inventory — remove TBD entries, add actual generation scripts.
4. Update table inventory from 5 to 8 tables.
5. Run `seldon paper sync` after updating.

This is bookkeeping. No prose changes to the paper itself.

## Cluster 5: Kinetics Analogy Scope (convergence 2)

**Problem:** First-order/second-order labels used in Methods before the kinetics analogy is developed in Discussion 6.1. The analogy currently explains but doesn't predict.

**Action:**

1. Edit `paper/sections/03_methods.md`:
   - At first use of "first-order" / "second-order" labels, add 1-2 sentences: "We label these by analogy to chemical reaction kinetics — first-order asks whether error is shrinking, second-order asks whether the rate of precision gain is sustained. Section 6.1 develops this parallel."

2. Edit `paper/sections/06_discussion.md` (Section 6.1):
   - Add an explicit scope sentence: "The parallel is structural; we do not claim the kinetics framework predicts convergence rates for arbitrary series."
   - This preempts Reviewer 2's "does this predict anything?" question.

## Cluster 7: Population Scaling Argument (convergence 2)

**Problem:** Paper tests up to pop=10,000. GP literature uses 100K+. Sastry's population-sizing theory is cited but not computed.

**Action:** Author decision required — three options:

- **Option A (strongest):** Compute the Sastry population-sizing estimate for t=10. If predicted population is >1M, state that explicitly: "Sastry's model predicts a minimum population of [X] for t=10, well beyond computational feasibility for this study."
- **Option B:** Acknowledge the limitation in one sentence: "Our population range (1,000–10,000) does not reach the scales tested in some GP studies; however, the phase transition's sharpness between t=8 and t=10 at pop=5,000 suggests the bottleneck is structural, not computational."
- **Option C:** Do both.

If Option A: this may require running `verify_parsimony_values.py` or a similar computation script. Check whether a Sastry estimate is computable from existing data.

## Cluster 8: Discovery Equation Rigor (convergence 2)

**Problem:** Section 6.2 presents P(discovery) in an equation block without derivation. May be dismissed as hand-waving.

**Action:** Option B — present as verbal summary rather than equation block. This is a workshop/preprint paper, not a full journal submission. The verbal framing is honest; the equation block implies more rigor than exists.

1. Edit `paper/sections/06_discussion.md` (Section 6.2):
   - Replace the equation block with prose: "The scaling grid data are consistent with a proportionality: discovery probability scales with fitness quality and coverage, and inversely with search space size."
   - Or keep the equation but add a qualifier: "We propose this as an organizing principle consistent with the data, not a derived result."

Author decision on which framing.

## Unclustered Items (address if time permits)

- Add "(log-precision fitness)" parenthetical to "19 of 20" in abstract (CS-03)
- Add 1-sentence Discussion roadmap connecting subsections 6.1-6.4 (narrative finding)
- Add 1-sentence primer on deceptive attractors in Background (clarity finding)
- Add 1-sentence weight provenance for log-precision fitness weights (clarity finding)

These are all single-sentence additions. Low effort, moderate readability improvement.

## Do NOT

- Generate a heatmap figure (Cluster 6 is dismissed — the table is the author's deliberate choice)
- Rewrite sections wholesale — these are targeted edits
- Change any experimental results or numbers
- Skip the post-edit glossary/sync/build cycle
- Create Issue or ResearchTask artifacts in the graph for these findings (the audit outputs serve as the record)

## Verification

After all edits:
```bash
python paper/check_glossary.py
seldon paper sync --project-dir .
seldon paper build --no-render --project-dir .
seldon verify --project-dir .
```

Confirm zero glossary violations, clean sync, clean build.
