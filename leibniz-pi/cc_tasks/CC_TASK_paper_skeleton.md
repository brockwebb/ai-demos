# CC Task: Set Up Paper Infrastructure and Write Non-Results Sections

## Context

The paper uses Seldon's paper authoring infrastructure. Read the handoff at `handoffs/2026-03-15_paper_infrastructure_ready.md` for full details on how the system works. Read `paper/conventions.md` (once created), `paper/paper_qc_config.yaml`, and `paper/paper_style_config.yaml` before writing any prose.

The preprint outline is in `RESEARCH_NOTES.md` under "Preprint Paper Outline (Draft)." The lit review leads and positioning are in `handoffs/2026-03-15_seldon_integration_complete.md`. All experimental findings are in `RESEARCH_NOTES.md` and `v3_results_summary.md`.

## Step 1: Set Up Infrastructure

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
mkdir -p paper/sections
cp ~/Documents/GitHub/seldon/templates/paper/conventions.md paper/conventions.md
```

Delete the monolithic `paper/paper.md` — it's the wrong format.

```bash
rm paper/paper.md
```

## Step 2: Add Paper-Specific Conventions

Append leibniz-pi-specific rules to the bottom of `paper/conventions.md` under the "Paper-Specific Rules" section. These rules:

### Terminology
- **"Wrong-limit attractor"** is our coined term. Define on first use, then use consistently. Not "deceptive series," "false positive," or "spurious convergent."
- **"Discovery"** means the GP found a Leibniz-equivalent expression from random initialization. Not "rediscovery" (implies prior knowledge). Not "recovery" (implies reconstruction).
- **"Evaluation horizon"** is the maximum T at which partial sums are checked. Not "evaluation window" or "test range."
- **"Coverage"** refers to the fraction of structurally distinct building blocks present in the population. Not "diversity" (which has a specific GP meaning related to fitness variance).
- **"Log-precision fitness"** is the correct term. Do not write "entropy fitness" or "information-theoretic fitness."
- **"Convergence-aware fitness"** for the first-order variant. Not "GP fitness" or "rate fitness."
- **"Phase transition"** for the sharp boundary between discoverable and non-discoverable regions. Use "degradation" if data shows the boundary is gradual rather than sharp.

### Numbers and References
- All research numbers use Seldon references: `{{result:NAME:value}}`. Never write a literal number for a measured or computed result.
- GP engine parameters (P_CROSS=0.70, TOURNAMENT_K=7, etc.) can be literal since they are fixed experimental conditions.
- Mathematical constants (π/4, log₂(10)) can be literal.

### Framing
- The injection confound is our mistake. Frame it as "we made this error, caught it, and corrected it." Do not blame the tooling.
- The Hillar & Sommer (2012) parallel to our injection confound is a narrative strength. Use it.
- Wrong-limit attractors are the central finding. They are not failures of the fitness function. They are coverage failures exploiting the evaluation horizon.
- The second-order kinetics connection is analogical, not rigorous. Present as "observation" in Discussion, not as a proven result.

## Step 3: Check Available Seldon Results

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
seldon result list
```

Use the output to know what `{{result:NAME:value}}` references are available. Every research number in the paper must use these references.

## Step 4: Write Section Files

Create these files in `paper/sections/`. Write them in order. After each section, run `seldon paper audit paper/sections/FILENAME.md` and fix violations before moving on.

### 00_abstract.md

Working title: "Reverse Engineering Leibniz: Evolutionary Discovery of the π/4 Series from Arithmetic Primitives"

The abstract should cover: what we did (GP + log-precision fitness discovers Leibniz from primitives), the key positive result (5/5 at minimal terminals), the key negative result (sharp failure as terminals expand), the mechanism (wrong-limit attractors), and the framing (discovery difficulty is coverage, not fitness landscape). ~200 words.

### 01_introduction.md

Frame the problem: Leibniz is famous for convergence structure, not efficiency. Our constructive question: can evolutionary search rediscover it from primitives and a process-level fitness? This differs from standard SR (which fits data points) because there are no data points — we evaluate process properties.

Key argument: "find a series that sums to π/4" does not produce Leibniz. "Find the simplest rule that never stops converging" does. The question matters more than the answer.

Preview the three novelty gaps (from the handoff lit review section):
1. Fitness design for infinite-horizon convergent processes
2. Wrong-limit attractor analysis vs terminal set size
3. The evaluation horizon trap

### 02_background.md

Position against:
- Schmidt & Lipson (2009) — foundational GP-SR, Hillar & Sommer injection critique parallels ours
- Cranmer (2023) PySR — SOTA practical SR, fits data points (we evaluate process properties)
- Brunton et al. (2016) SINDy — sparse regression alternative paradigm
- Neural/transformer SR: SymbolicGPT, DySymNet, GFlowNet-SR, EGG-SR, MCTS approaches — all pointwise fitness

Three subsections: Symbolic Regression, Fitness Design for Convergent Processes (gap 1), Wrong-Limit Attractors and the Evaluation Horizon Trap (gaps 2 and 3).

None of the cited work addresses infinite-horizon process-level fitness. State this clearly.

### 03_methods.md

Three subsections:

*Expression Representation.* Trees over operators {+,-,×,÷,^,neg} and configurable terminal sets. Safe division, overflow protection.

*Evolutionary Search.* Standard GP: ramped half-and-half init, tournament selection, subtree crossover/mutation, elitism, diversity injection. No domain-specific operators. Parameters in a table.

*Two Fitness Functions.* Convergence-aware (first-order: is error shrinking?) and log-precision (second-order: is 1/error growing linearly?). Mathematical definitions. Why the second-order question is more selective.

Use the "what the GP builds" walkthrough — explaining the three structural components (oscillation, odd denominator, division) that must be assembled. This makes the mechanism concrete for readers outside GP.

### 04_experimental_design.md

*The Injection Confound.* v2 seeded the population with Leibniz. Both fitness functions reported 5/5. This was retention, not discovery. All v3 results use pure random init. Frame as our mistake, parallel to Hillar & Sommer critique.

*Clean Protocol.* Five seeds, time budgets, equivalence test definition.

*Terminal Set Construction.* Option A: {k,1,-1,2} base + expanding integers. Table of exact sets at each N. Design rationale: isolates search space expansion from primitive availability.

*Scaling Grid.* Reference `scaling_heatmap_methodology.md` for the full protocol. [PENDING results]

### 05_results.md

This section has PENDING stubs for the heat map. Write what we have:

*Discovery Under Minimal Terminals.* Information-theoretic: 5/5 at pop=1000. Convergence-aware: 2/5 at pop=1000, 5/5 at pop=2000. Table of discovered expressions. All algebraically equivalent, verified at k=100,000.

*Failure Under Expanded Terminals.* 15 terminals at pop=1000: 0/5. The 5/((6+4k)(k-2)) attractor example scoring 15.93 bits vs Leibniz's 15.29. The wrong-limit attractor scores *better* within the evaluation horizon.

*Parsimony Pressure.* Table: λ_p = 0.005 (5/5) → 0.01 (0/5) → 0.02 (0/5) → 0.05 (0/5). Sharp transition. The log-precision reward ceiling (~0.07) sets a hard limit on viable parsimony.

*Fitness Modifications.* Table of attempted fixes on 15 terminals (extended checkpoints, large-T penalty, rate consistency, gradient-based). All 0/5. Confirms coverage bottleneck, not fitness bottleneck.

*The Scaling Boundary.* [PENDING — leave a stub with `[PENDING: Heat map experiment results. See scaling_heatmap_methodology.md.]`]

### 06_discussion.md

*Second-Order Kinetics Connection.* Error decays as 1/(2T+1). Plot 1/error vs T: straight line = second-order signature. The log-precision fitness is the integrated second-order rate law. Present as observation, not proof. The 3.32 bits/decade constant is a property of Leibniz's error decay, not evidence of thermodynamic behavior.

*Discovery = Fitness Quality × Coverage / Search Space.* The unifying finding. Fitness quality is fixed (correctly ranks Leibniz). Coverage scales linearly with population. Search space scales combinatorially with terminals. Phase transition where coverage/space drops below threshold.

*The Confabulation Analogy.* Wrong-limit attractors as LLM confabulation analogues. RL/ACO = confabulation, GP v1 = miscalibration, Leibniz = calibrated. The analogy: optimization against finite evaluation produces locally plausible but globally incorrect outputs.

*Implications for Symbolic Regression.* Three generalizable findings: (1) process-level fitness design, (2) wrong-limit attractors as a distinct failure mode from bloat, (3) evaluation horizon trap is fundamental.

### 07_conclusion.md

Short. Leibniz is discoverable from primitives under constrained search. The fitness need not mention π. Discovery fails sharply as the search space expands, not because the fitness landscape degrades, but because coverage becomes insufficient. The question is harder than the answer.

Future work: efficiency fitness (bits per operation), formal analysis of attractor density scaling, extension to other convergent series.

### 08_references.md

Create `paper/references.bib` with BibTeX entries for:
- Schmidt & Lipson (2009) Science
- Hillar & Sommer (2012) arXiv
- Cranmer (2023) arXiv
- Brunton, Proctor & Kutz (2016) PNAS
- Valipour et al. (2021) SymbolicGPT
- Li et al. (2023) DySymNet
- Li et al. (2023) GFlowNet-SR
- Jiang et al. (2025) EGG-SR
- Kamienny et al. (2023) NeurIPS
- Shojaee et al. (2023) NeurIPS

Use web search to get correct BibTeX entries. The references section file just contains `\bibliography{references}` or equivalent for the build system.

## Step 5: Audit All Sections

After all sections are written:

```bash
seldon paper audit paper/sections/*.md
```

Fix all Tier 2 violations. Review Tier 3 findings.

## Step 6: Test Build

```bash
seldon paper build --no-render --skip-qc
```

This checks that all `{{result:NAME:value}}` references resolve. Fix any missing references. If a result doesn't exist in the graph, either register it with Seldon or leave a `[PENDING]` note.

## Do NOT

- Do not write literal numbers for research results. Use `{{result:NAME:value}}`.
- Do not use em dashes anywhere.
- Do not use any banned words from `paper_style_config.yaml`.
- Do not write the Results scaling boundary section — it's pending the heat map experiment.
- Do not write bullet points in prose sections.
- Do not use bold in running prose.
- Do not write "novel," "robust," "notably," "remarkably," or any word on the banned list.
