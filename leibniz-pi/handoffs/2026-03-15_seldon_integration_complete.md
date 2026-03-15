# Handoff: 2026-03-15 — Seldon Dogfood on leibniz-pi + Lit Review Leads

**Date:** 2026-03-15
**From:** Claude Desktop (Seldon infrastructure thread)
**To:** leibniz-pi project thread / next Claude Code session

---

## Seldon Integration — COMPLETE

Seldon is live on leibniz-pi. `seldon briefing` works from the project directory.

### Current State
- **44 artifacts** in Neo4j database `seldon-leibniz-pi`
- **17 relationships** (GENERATED_BY, COMPUTED_FROM, CITES, BLOCKS)
- **71 events** in `seldon_events.jsonl`
- 9 Scripts, 5 DataFiles, 11 Results (all verified), 7 PaperSections, 11 ResearchTasks, 1 LabNotebookEntry
- `.env` with Neo4j credentials in project root (auto-loaded by Seldon via python-dotenv)

### Briefing Output (confirmed working)
- 11 open tasks surfaced
- 0 stale results
- 2 incomplete provenance flags (analytical results — 3.32 bits/decade, 15.29 bits at T=10000)

### Pending CC Task (in seldon repo, not yet run)
File: `~/Documents/GitHub/seldon/cc_tasks/` — needs a task for analytical result provenance fix:
- Add `derived_from` relationship type to `research.yaml` schema
- Create LabNotebookEntry for the error bound derivation
- Link the two analytical results via DERIVED_FROM
- Update briefing query to recognize DERIVED_FROM as valid provenance
- CC task spec was drafted in the Seldon thread (in chat, not yet written to file — write it from the spec in chat or re-derive from the description above)

Run this before the next `seldon briefing` to clear the incomplete provenance flags.

### Seldon Fixes Shipped Today
All in seldon repo, merged to main, 111/111 tests passing:
1. Env var fallback (NEO4J_USER/NEO4J_PASS)
2. Name-based artifact resolution (--script-name, --script-path, --from-name, --to-name)
3. Session idempotency (double briefing doesn't reset session)
4. Link create flag aliases (--from-id, --to-id, --rel)
5. Neo4j GQL notification suppression (NotificationMinimumSeverity.OFF)
6. Auto-load .env via python-dotenv

---

## Lit Review Leads (needs follow-up in leibniz-pi thread)

### The positioning: Three novelty gaps

The paper fills gaps the entire symbolic regression field doesn't address:

1. **Fitness design for infinite-horizon convergent processes.** All existing SR fitness is pointwise (minimize error at observed x,y pairs) or Pareto (accuracy vs. complexity). Nobody measures bits-per-decade information gain rate as fitness.

2. **Wrong-limit attractor analysis vs. terminal set size.** SR literature discusses "bloat" but not structurally distinct wrong-limit attractors that score BETTER than the correct answer on finite evaluation windows. The 15.93 > 15.29 finding appears novel.

3. **The evaluation horizon trap.** Any finite-T evaluation creates exploitable wrong-limit attractors. Extending T doesn't fix it, just shifts attractors. Appears undocumented.

### Key papers to cite / position against

**Schmidt & Lipson (2009)** — "Distilling Free-Form Natural Laws from Experimental Data." Science 324(5923):81-85. Foundational GP symbolic regression. Rediscovered Hamiltonians/Lagrangians. Hillar & Sommer (2012) showed it implicitly baked physics into the fitness structure. Directly parallels the injection confound.

**Cranmer (2023)** — "Interpretable Machine Learning for Science with PySR and SymbolicRegression.jl." arXiv:2305.01582. Current SOTA practical SR. Multi-population evolutionary, Pareto front. Key difference: PySR fits equations to DATA POINTS. This project's fitness evaluates PROCESS PROPERTIES at infinite horizon. Fundamentally different objective class.

**Hillar & Sommer (2012)** — arXiv:1210.7273. The injection critique of Schmidt & Lipson. Same failure mode as the v2 confound.

**Brunton, Proctor & Kutz (2016)** — SINDy. Sparse regression over function library. Alternative paradigm worth citing.

**HuggingFace search results** (none address infinite-horizon fitness):
- SymbolicGPT (Valipour et al., 2021) — transformer-based SR
- DySymNet (Li et al., 2023) — neural-guided symbolic network
- GFN-SR (Li et al., 2023) — GFlowNet for SR
- EGG-SR (Jiang et al., 2025) — symbolic equivalence via equality graphs
- Multiple MCTS-based approaches (Kamienny et al. 2023, Shojaee et al. 2023)

**EA Forum** — "(Re)Discovering Natural Laws" — recent survey of automated law discovery field. Good for related work framing.

### Target venues
- GECCO (Genetic and Evolutionary Computation Conference)
- EvoStar
- Entropy (MDPI, open access)
- arXiv cs.NE as preprint

---

## Open Research Tasks (registered in Seldon)

Run `seldon task list --open` to see them.

**Active experiments:**
- Final experiment running (finishes in hours)
- Vector space decomposition / min-gradient energy dispersion (in progress)

**Blocking the paper:**
- Operations-per-bit efficiency fitness (not implemented)
- Combined optimal config test (pop=2000 + alpha=0.5 + entropy on 15 terminals)
- Wrong-limit attractor density formal analysis
- Second-order kinetics proof

**Writing:**
- Medium draft closing section rewrite
- Academic paper draft

---

## Key Files

| File | Purpose |
|------|---------|
| `seldon.yaml` | Seldon project config |
| `seldon_events.jsonl` | Append-only event log (71 events) |
| `.env` | Neo4j credentials (gitignored) |
| `seldon_bootstrap.py` | Batch registration script (ran once) |
| `seldon_dogfood_notes.md` | Friction findings from bootstrap |
| `.seldon/current_session.json` | Active session (run `seldon closeout` to clear) |
| `handoffs/2026-03-15_seldon_integration_complete.md` | This file |

---

*Next action in leibniz-pi thread: Run the derived_from CC task against seldon repo, then start lit review and paper primitives while final experiment finishes.*
