# CC Task: Write the Complete Leibniz-Pi Preprint

**Date:** 2026-03-17
**Project:** `/Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
**Execution:** CC agent team (enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json)
**Lead model:** Opus 4.6

---

## Directive

Write the complete leibniz-pi preprint. All 8 sections need publication-quality prose: Abstract, Introduction, Background, Methods, Experimental Design, Results, Discussion, and Conclusion. The Methods section (03) was already rewritten by a prior swarm test pass and may need only light polish. The other sections have substantive scaffolding content that must be rewritten to publication standard.

---

## How to Begin

You are the Lead. Run `seldon go --brief` to load project context, agent roles, and workflows. That output contains everything: role definitions with system prompts, workflow decomposition templates, writing conventions, available seldon CLI commands, project state, and the latest handoff.

Then run:
```bash
seldon briefing
seldon result list
seldon task list --open
```

Read `paper/conventions.md` before making any decisions. Read `RESEARCH_NOTES.md` and the supplementary notes (`RESEARCH_NOTES_SUPP_*.md`) to understand the full research story. Read the swarm test handoff at `handoffs/2026-03-17_swarm_test_results.md` for lessons learned from the Methods section pass.

---

## What the Paper Is

- A demonstration that process-level fitness (rewarding convergence properties, not pointwise accuracy) enables GP discovery of infinite-horizon convergent series
- A characterization of the scaling boundary (phase transition) where discovery fails, with combinatorial analysis explaining why
- An introduction of "wrong-limit attractors" as a failure mode distinct from bloat in symbolic regression
- A documentation of the evaluation horizon trap as a fundamental limitation
- A contribution informed by chemical engineering intuition about rate laws, applied to symbolic regression

## What the Paper Is NOT

- Not a claim that GP can discover arbitrary formulas
- Not a claim that the fitness function is entropy or information-theoretic
- Not a claim that either fitness function is uniformly better (5 seeds is a pilot)
- Not a claim about thermodynamics (the kinetics math is real, the thermodynamic framing was stripped)

---

## Team Strategy

You define the strategy. The `Write Paper Section` workflow in `seldon go` output describes one proven decomposition pattern (Methods → Verify → Write → Red Team → Fix). You may use it, adapt it, batch sections, run parallel teams, or invent a different approach. The prior swarm test on Methods took ~230K tokens for one section with sequential sub-agents. You have agent teams with parallelism available.

**Constraints on your strategy:**
1. Every section must pass through a Verifier and Red Team before it is considered done
2. All numeric values must use `{{result:NAME:value}}` references, never literals
3. `paper/conventions.md` rules are non-negotiable (no em dashes, no inline bold, max 35 words/sentence, etc.)
4. `seldon paper audit paper/sections/*.md` must be run on every section
5. Cross-section consistency matters: the Introduction promises what the Results deliver; the Discussion interprets what the Results report; the Conclusion does not introduce new claims
6. The Abstract is written last, after all other sections are final

**Available roles** (system prompts in `seldon go` output):
- `lead` — you, coordination only
- `methods` — methodology prose, code-vs-paper verification
- `verifier` — reference resolution, provenance checking, audit
- `writer` — publication-quality prose from claims and evidence
- `literature` — citation grounding, references.bib completeness
- `red_team` — adversarial review, cross-section consistency, unstated assumptions

**Spawn prompts:** Use the system_prompt text from `seldon go` for each role. Add section-specific scope to each spawn (e.g., "Your scope for this task is Section 5: Results").

---

## Key Resources

| Resource | Location | Purpose |
|----------|----------|---------|
| Research notes (master) | `RESEARCH_NOTES.md` | All findings, experiment results, analysis |
| Core thesis | `RESEARCH_NOTES_SUPP_core_finding.md` | The paper's central argument |
| Design motivation | `RESEARCH_NOTES_SUPP_design_motivation.md` | ChemE lens, crystallization analogy |
| Complexity ceiling | `RESEARCH_NOTES_SUPP_complexity_ceiling.md` | Why fundamental laws are compact |
| Applicability | `RESEARCH_NOTES_SUPP_applicability.md` | Transfer to other domains |
| Future work | `RESEARCH_NOTES_SUPP_future_work.md` | What comes next |
| π-entropy connection | `RESEARCH_NOTES_SUPP_pi_entropy_connection.md` | Open question, labeled speculation |
| Writing conventions | `paper/conventions.md` | Non-negotiable prose rules |
| QC config | `paper/paper_qc_config.yaml` | Machine-checkable prose rules (Tier 2) |
| Style config | `paper/paper_style_config.yaml` | Banned words, clichés (Tier 3) |
| BibTeX | `paper/references.bib` | 14 entries |
| Experiment results | `v3_results_summary.md` | Master results from all v3 experiments |
| Scaling grid data | `entropy-leibniz-v3/scaling_heatmap_results.md` | Full 7×4 grid |
| GP comparison | `gp-leibniz-v3/results_gp_scaling_p5000/` and `p10000/` | GP convergence-aware scaling |
| Parsimony results | `entropy-leibniz-v3/parsimony_test_results.md` | λ_p sweep |
| Fitness mods | `entropy-leibniz-v3/fitness_sensitivity_results.md` | 6 modifications, all failed at t=15 |
| Swarm test handoff | `handoffs/2026-03-17_swarm_test_results.md` | Lessons from Methods section |
| Seed table | `paper/appendix_seed_table.md` | All seeds across all experiments |

---

## Section-Specific Notes

### 00_abstract.md
Write LAST. Summarize what the paper demonstrates, the key result (phase transition), the key contribution (wrong-limit attractors), and the implication. Keep under 250 words. Must reference key numeric results via `{{result:...}}`.

### 01_introduction.md
Sets up the problem. Current scaffolding is solid on structure. Needs prose polish and tighter connection to the "the question is harder than the answer" thesis. Must promise exactly what Results delivers.

### 02_background.md
Position relative to prior work. Symbolic regression landscape, GP basics, fitness design literature. This is where the Literature role earns its keep. Every claim about prior work needs a citation in references.bib.

### 03_methods.md
Already rewritten by the swarm test. Verify accuracy, polish prose, ensure consistency with any changes made to other sections. Light touch unless Red Team finds issues.

### 04_experimental_design.md
The injection confound, clean protocol, terminal set construction, scaling grid design. Current scaffolding is good. Needs the Hillar & Sommer parallel emphasized. Must define the discovery criterion precisely (20-term match, 10^-6 error).

### 05_results.md
The data. Scaling grid, minimal terminal success, expanded terminal failure, parsimony pressure, fitness modification failures. Current scaffolding has the tables and key results. Needs narrative prose connecting the tables. The t=15/p=10000 anomaly (2/5) must be discussed honestly.

### 06_discussion.md
Interpretation. Kinetics connection (carefully scoped as analogy, not proof). The P(discovery) ∝ (fitness × coverage) / search_space framing. Confabulation analogy. Implications for symbolic regression. Design provenance. Current scaffolding is the most mature section. Needs prose tightening, not rewriting.

### 07_conclusion.md
What we showed, what it means, what comes next. Current scaffolding is tight. Ensure it does not introduce new claims not supported by Results/Discussion.

### 08_references.md
Auto-generated from references.bib by the build. Literature role should verify completeness.

---

## Quality Gates

Before declaring any section done:
1. `seldon paper audit paper/sections/NN_name.md` — Tier 1 must pass, Tier 2 and 3 reviewed
2. All `{{result:NAME:value}}` references verified against `seldon result list`
3. Cross-section references checked (if Section 5 says "as described in Section 3", verify Section 3 says it)
4. Red Team pass completed with issues logged as ResearchTasks

Before declaring the paper done:
5. `seldon paper build --no-render` — full build succeeds, all references resolve
6. `seldon paper audit paper/sections/*.md` — run on all sections together
7. Abstract written last, consistent with final content
8. `seldon task list --open` reviewed — any RED TEAM tasks that block publication?

---

## Completion

When the paper is complete:
1. Run `seldon paper build` to assemble the full manuscript
2. Run `seldon closeout` to log the session
3. Write a handoff to `handoffs/` documenting: what was done, token cost observations, any remaining issues, recommendations for revision

---

## Do NOT

- Do not rerun any experiments — all data is final
- Do not modify experiment scripts or data files
- Do not use the term "entropy fitness" — use "log-precision fitness"
- Do not write thermodynamic claims about the fitness function
- Do not write literal numbers for research results — use `{{result:NAME:value}}`
- Do not skip the Red Team pass on any section
- Do not let the lead implement prose directly — delegate to specialist roles
