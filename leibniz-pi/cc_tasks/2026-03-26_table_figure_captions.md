# CC Task: Add Table Captions and Figure Placement References

**Date:** 2026-03-26
**Priority:** High (blocks abstract)

---

## Objective

Add proper numbered captions to all tables in the paper sections, and add figure placement references with captions where figures are generated but not yet referenced.

---

## Pre-Flight

1. Read `paper/conventions.md` for style rules.
2. Read each section file listed below BEFORE editing it. Brock edits files externally; never assume stale content.

---

## Part A: Table Captions

Add a bold caption line immediately ABOVE each markdown table. Format: `**Table N:** Caption text in sentence case.`

Tables are numbered sequentially across the entire paper (not per-section).

### Section 04 (04_experimental_design.md)

Read the file first. Find these tables and add captions:

- **Table 1:** The operator/safe-evaluation table in Section 4.3. Caption: `**Table 1:** GP operator set and safe-evaluation behavior. Safe division and power overflow return implicit constant terminals.`
- **Table 2:** The terminal set construction table in Section 4.3. Caption: `**Table 2:** Terminal set construction at each size N. The base set {k, 1, -1, 2} is always present.`

### Section 05 (05_results.md)

Read the file first. Find these tables and add captions:

- **Table 3:** The fitness comparison table in Section 5.1 (Fitness / Pop / Seeds Found / Mean Generations). Caption: `**Table 3:** Discovery rates under minimal terminals (N=4) by fitness function and population size.`
- **Table 4:** The expression variants table in Section 5.1 (Seed / Expression / Nodes / Notes). Caption: `**Table 4:** Structural variants of the Leibniz series discovered across five seeds.`
- **Table 5:** The 7x4 scaling grid in Section 5.3. Caption: `**Table 5:** Discovery rate (seeds found / 5) across terminal set sizes and population sizes. The phase transition between t=8 and t=10 holds across all population sizes.`
- **Table 6:** The parsimony sweep in Section 5.4. Caption: `**Table 6:** Effect of parsimony pressure on discovery. The transition from full discovery to complete failure occurs between lambda_p = 0.005 and lambda_p = 0.01.`
- **Table 7:** The fitness modifications table in Section 5.5. Caption: `**Table 7:** Fitness function modifications tested on the 15-terminal configuration. No modification achieved reliable discovery.`

---

## Part B: Figure Placement References

Add figure references at the appropriate location in each section. Format: a paragraph that references the figure naturally in the prose, followed by a standalone line:

```
![Figure N caption](../figures/FILENAME.png)

**Figure N:** Caption text in sentence case.
```

Figures are numbered sequentially across the entire paper.

### Section 05 (05_results.md)

- **Figure 1** in Section 5.2, after the paragraph describing the wrong-limit attractor from seed 42. File: `fig2_precision_vs_T.png`. Caption: `**Figure 1:** Log-precision trajectories for the Leibniz series and the strongest wrong-limit attractor (seed 42, 15 terminals). The attractor exceeds Leibniz precision within the evaluation horizon (T <= 10,000) but converges to a different limit.`

- **Figure 2** in Section 5.3, after the scaling grid table. File: `fig1_scaling_heatmap.png`. Caption: `**Figure 2:** Discovery rate across terminal set sizes and population sizes. The dashed red line marks the phase transition between t=8 and t=10. The anomalous partial recovery at t=15, pop=10,000 is visible.`

- **Figure 3** in Section 5.4, after the parsimony sweep table and the paragraph about the crossover point. File: `fig3_parsimony_collapse.png`. Caption: `**Figure 3:** Fitness score as a function of parsimony coefficient (lambda_p) for the 9-node Leibniz tree and the 3-node zero-constant attractor. The crossover at lambda_p approximately 0.0110 marks where the zero-constant becomes fitter than Leibniz.`

### Section 06 (06_discussion.md)

- **Figure 4** in Section 6.1, after the paragraph about plotting 1/error versus T. File: `fig4_second_order_kinetics.png`. Caption: `**Figure 4:** Reciprocal error (1/|S(T) - pi/4|) versus evaluation depth T for the Leibniz series. The linear relationship confirms second-order convergence structure. The computed values (slope approximately 2) track the theoretical bound 2T+1 with a constant offset due to the alternating series remainder.`

- **Figure 5** (optional, include only if both Fig 4 and 4b add value; if redundant, skip 4b). File: `fig4b_second_order_loglog.png`. Caption: `**Figure 5:** Same data as Figure 4 on log-log axes (T = 1 to 10,000). The parallel lines with slope 1 confirm the linear 1/T error scaling across four decades.`

NOTE: The figure numbering in the filenames (fig1, fig2, etc.) does NOT match the paper figure numbers. The paper numbers are assigned by order of appearance in the text. Do not renumber the files; only the captions and in-text references use the paper numbering.

---

## Post-Flight

1. After all edits, run: `python paper/prose_qc.py` -- confirm 0 violations.
2. Run: `python paper/check_glossary.py` -- confirm 0 violations.
3. Run: `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && seldon paper sync`
4. Run: `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && seldon paper build --no-render`

---

## Do NOT

- Do not modify any prose content beyond adding caption lines and figure references.
- Do not renumber existing section headings.
- Do not change any `{{result:...}}` references.
- Do not overwrite any existing CC task files.
- Do not hardcode measured values -- all values come from Seldon references already in the text.
- Do not reorder tables or move existing content.
