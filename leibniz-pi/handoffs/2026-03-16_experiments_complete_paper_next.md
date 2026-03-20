# Handoff: 2026-03-16 — All Experiments Complete, Paper Build Next

**Date:** 2026-03-16
**From:** Claude Desktop (leibniz-pi research thread)
**To:** Next Claude thread (paper writing)

---

## Status: Experiments Done. Write the Paper.

All experimental work is complete. The next task is building the paper using Seldon's paper authoring infrastructure.

---

## What Was Accomplished This Session

### Scaling heat map (entropy / log-precision fitness)
Ran a 7×4 grid: terminal counts [4, 6, 8, 10, 12, 15, 20] × population sizes [1000, 2000, 5000, 10000]. 28 cells, 5 seeds each.

| Terminals | Pop=1000 | Pop=2000 | Pop=5000 | Pop=10000 |
|-----------|----------|----------|----------|-----------|
| 4         | 5/5*     | 4/5      | 5/5      | 5/5       |
| 6         | 1/5      | 2/5      | 1/5      | 1/5       |
| 8         | 1/5      | 1/5      | 1/5      | 0/5       |
| 10        | 0/5      | 0/5      | 0/5      | 0/5       |
| 12        | 0/5      | 0/5      | 0/5      | 0/5       |
| 15        | 0/5*     | 0/5      | 0/5      | 2/5       |
| 20        | 0/5      | 0/5      | 0/5      | 0/5       |

### GP convergence-aware fitness scaling (supplementary)
Ran p=5000 and p=10000 columns across all 7 terminal counts.

| Terminals | GP Conv p=5000 | GP Conv p=10000 | Entropy p=5000 | Entropy p=10000 |
|-----------|----------------|-----------------|----------------|-----------------|
| 4         | 4/5            | 5/5             | 5/5            | 5/5             |
| 6         | 1/5            | 4/5             | 1/5            | 1/5             |
| 8         | 0/5            | 0/5             | 1/5            | 0/5             |
| 10        | 1/5            | 0/5             | 0/5            | 0/5             |
| 12        | 0/5            | 0/5             | 0/5            | 0/5             |
| 15        | 1/5            | 0/5             | 0/5            | 2/5             |
| 20        | 0/5            | 0/5             | 0/5            | 0/5             |

Neither fitness function is uniformly better. 5 seeds per cell is a pilot, not definitive. The t=10 and t=15 single-seed hits at GP conv p=5000 did not replicate at p=10000 — likely noise.

### Extended time test
GP convergence-aware, t=10, p=5000, 2 hours per seed (4x the standard budget). Result: 1/5 again, same seed (val=7). The other 4 seeds found the same wrong-limit attractors they found in 30 minutes. More time doesn't help. The bottleneck is coverage at initialization.

### Grandi-Leibniz attractor analysis
At t=4/p=2000, seed 31415 found `(-1)^(k+1) * 2k/(2k+1)`, which decomposes algebraically to S_Leibniz(T) - G(T) where G is the Grandi series. At even T, this equals Leibniz exactly. At odd T, it differs by exactly 1. The fitness couldn't distinguish it because 10/11 checkpoints are even. Strongest example of the evaluation horizon trap — it exploits checkpoint structure, not just finite T.

### Combinatorial coverage analysis
Quantified why population can't fix the terminal count problem. Search space grows as N^L (exponential in terminal count), population grows linearly. At t=20, you'd need hundreds of millions to match the coverage ratio that t=4/p=1000 has. This applies equally to both fitness functions.

### Critical terminology fix
"Entropy fitness" renamed to "log-precision fitness" throughout. The fitness computes -log₂(|error|), which is log-scale precision, not entropy. Calling it entropy was a confabulation — the exact error this project studies. Thermodynamic framing (free energy, dissipation, far from equilibrium) stripped from research notes.

The design *motivation* came from chemical engineering intuition about crystallization, reaction kinetics, and steady-state ordering processes. The post-hoc recognition that the fitness corresponds to the integrated second-order rate law is real math. But the fitness itself is not entropy.

### Lit review and BibTeX
Three Perplexity queries run. All three novelty gaps confirmed: (1) no prior work on fitness for infinite-horizon convergent processes, (2) no taxonomy of wrong-limit attractors distinct from bloat, (3) no second-order kinetics connection to fitness design. BibTeX filed at `paper/references.bib` with 14 entries.

---

## Key Files

### Research Notes (read all of these before writing)
| File | Contents |
|------|---------|
| `RESEARCH_NOTES.md` | Master findings, all experiment results, scaling grid, GP comparison, combinatorial analysis |
| `RESEARCH_NOTES_SUPP_core_finding.md` | The thesis: constrain primitives, not algorithms |
| `RESEARCH_NOTES_SUPP_design_motivation.md` | ChemE lens, crystallization analogy, min-gradient experiment motivation |
| `RESEARCH_NOTES_SUPP_complexity_ceiling.md` | Constructive search limits, slime mold/TSP distinction, fundamental laws are compact |
| `RESEARCH_NOTES_SUPP_applicability.md` | Where the method transfers: chemical kinetics, dynamical systems, protein folding, ML |
| `RESEARCH_NOTES_SUPP_pi_entropy_connection.md` | π in entropy formulas — open question, clearly labeled speculation |
| `RESEARCH_NOTES_SUPP_future_work.md` | Building block init, MCTS, island migration, automated terminal pruning, efficiency fitness |

### Paper Infrastructure
| File | Contents |
|------|---------|
| `paper/references.bib` | BibTeX entries (14 papers) |
| `paper/paper_qc_config.yaml` | Prose quality rules (Tier 2) |
| `paper/paper_style_config.yaml` | Banned words and clichés (Tier 3) |
| `paper/paper.md` | DELETE THIS — wrong format, monolithic draft from early in session |

### Experiment Results
| File | Contents |
|------|---------|
| `entropy-leibniz-v3/scaling_heatmap_results.md` | Entropy grid summary |
| `entropy-leibniz-v3/scaling_heatmap_methodology.md` | Full experimental protocol |
| `entropy-leibniz-v3/config/scaling_heatmap_config.json` | Experiment config (seeds, budgets, parallelism) |
| `gp-leibniz-v3/results_gp_scaling_p5000/gp_scaling_results.md` | GP conv p=5000 summary |
| `gp-leibniz-v3/results_gp_scaling_p10000/gp_scaling_results.md` | GP conv p=10000 summary |
| `gp-leibniz-v3/results_gp_extended_t10_p5000/gp_extended_t10_p5000.txt` | Extended time test |
| `entropy-leibniz-v3/parsimony_test_results.md` | Parsimony pressure sweep |
| `v3_results_summary.md` | Master results from all v3 experiments |

### Handoffs
| File | Contents |
|------|---------|
| `handoffs/2026-03-15_seldon_integration_complete.md` | Seldon setup, lit review leads, target venues |
| `handoffs/2026-03-15_paper_infrastructure_ready.md` | How to use Seldon paper tools |
| `HANDOFF-3-15-2026--0830.md` | Previous session handoff |

---

## CC Task Queue (run in this order)

1. **CC_TASK_paper_skeleton.md** — ALREADY RUNNING. Sets up paper/sections/ infrastructure, writes all section files using Seldon conventions and result references. NOTE: this task has old terminology ("entropy fitness", "information-theoretic") that will be fixed by later tasks.

2. **CC_TASK_rename_entropy.md** — Renames "entropy fitness" → "log-precision fitness" across all research notes and documentation. Does not touch scripts or data files.

3. **CC_TASK_paper_naming_fixes.md** — Fixes terminology in paper/sections/ after the skeleton is built. Strips thermodynamic framing. Limits "slime mold" to one introductory mention.

4. **CC_TASK_fitness_motivation_framing.md** — Adds the ChemE design motivation paragraph to methods section and kinetics connection to discussion.

5. **CC_TASK_capture_design_motivation.md** — Ensures the crystallization analogy and min-gradient experiment motivation are in the paper.

6. **CC_TASK_gp_scaling_extended.md** Part 3 — Generates `paper/appendix_seed_table.md` from all _data.json files across the repo.

---

## The Core Finding (the thesis of the paper)

Constrain your search space to the primitives that matter. The GP found Leibniz at 4 terminals and couldn't at 15. Not because the fitness broke, not because the algorithm failed, but because irrelevant primitives drown out the signal. The narrower the solution space, the better.

This maps to ML directly: feature selection matters more than model architecture. Throwing more parameters at a problem doesn't help if most of them are noise terminals. The signal gets pushed to the tail of the distribution. Regularization can't fix it past a threshold.

---

## What the Paper Is NOT

- Not a claim that GP can discover arbitrary formulas
- Not a claim that the fitness function is entropy or information-theoretic
- Not a claim that either fitness function is uniformly better (5 seeds is a pilot)
- Not a claim about thermodynamics (the kinetics math is real, the thermodynamic framing was stripped)

## What the Paper IS

- A demonstration that process-level fitness (rewarding convergence properties, not pointwise accuracy) enables discovery of infinite-horizon convergent series
- A characterization of the scaling boundary where discovery fails, with combinatorial analysis explaining why
- An introduction of "wrong-limit attractors" as a failure mode distinct from bloat in symbolic regression
- A documentation of the evaluation horizon trap as a fundamental limitation of finite evaluation of infinite-horizon processes
- A contribution informed by chemical engineering intuition about rate laws and ordering processes, applied to symbolic regression

---

## Seldon Status

- 44 artifacts registered in Neo4j
- 11 verified results available for `{{result:NAME:value}}` references
- `seldon paper audit` and `seldon paper build` are operational
- The DERIVED_FROM provenance fix is handled in the Seldon repo thread, not here

---

## Do NOT

- Do not rerun any experiments — all data is final
- Do not modify existing CC task files — they may already be running
- Do not use the term "entropy fitness" in the paper — use "log-precision fitness"
- Do not write thermodynamic claims about the fitness function
- Do not write literal numbers for research results — use `{{result:NAME:value}}`
