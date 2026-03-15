# CC Task: Dogfood Seldon on leibniz-pi Research Project

**Date:** 2026-03-15
**Project:** ~/Documents/GitHub/ai-demos/leibniz-pi
**Seldon repo:** ~/Documents/GitHub/seldon
**Goal:** Initialize Seldon on an active, evolving research project to track results, tasks, scripts, and provenance. This is the first real dogfood — the project is mid-research, not historical backfill.

---

## Prerequisites

1. Seldon must be pip-installed: `cd ~/Documents/GitHub/seldon && pip install -e .`
2. Neo4j must be running locally (bolt://localhost:7687, user neo4j)
3. Working directory for all seldon commands: `cd ~/Documents/GitHub/ai-demos/leibniz-pi`

Verify prerequisites before proceeding:
```bash
seldon --help
# Should show CLI commands: init, status, artifact, link, result, task, briefing, closeout
```

---

## Phase 1: Initialize Project

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
seldon init leibniz-pi
```

This creates:
- `seldon.yaml` in the project root
- `seldon_events.jsonl` (empty, append-only event log)
- Neo4j database `seldon-leibniz-pi`

Verify:
```bash
seldon status
```

---

## Phase 2: Register Script Artifacts

Register the key experimental scripts. Use `seldon artifact create Script` with properties.

**NOTE:** Capture the artifact_id output from each command — you'll need them for linking results.

```bash
# Core experiments
seldon artifact create Script -p "name=entropy_leibniz_v3_minimal.py" -p "path=entropy-leibniz-v3/entropy_leibniz_v3_minimal.py" -p "description=Entropy fitness, minimal terminals {k,1,-1,2}, no injection, 5 seeds"

seldon artifact create Script -p "name=gp_leibniz_v3_minimal.py" -p "path=gp-leibniz-v3/gp_leibniz_v3_minimal.py" -p "description=GP convergence fitness, minimal terminals {k,1,-1,2}, no injection, 5 seeds"

seldon artifact create Script -p "name=gp_sensitivity_sweep.py" -p "path=gp-leibniz-v3/gp_sensitivity_sweep.py" -p "description=Parameterized GP sensitivity sweep over alpha, lambda_p, pop_size, tournament_k"

seldon artifact create Script -p "name=entropy_stress_test.py" -p "path=entropy-leibniz-v3/entropy_stress_test.py" -p "description=Progressive difficulty stress test for entropy fitness, levels 1-4"

seldon artifact create Script -p "name=fitness_sensitivity_test.py" -p "path=entropy-leibniz-v3/fitness_sensitivity_test.py" -p "description=Three fitness fix approaches tested on 15-terminal entropy failure"

# Earlier experiments (EDA / v2 — register for provenance completeness)
seldon artifact create Script -p "name=gp_leibniz_v2.py" -p "path=gp-leibniz-v2/gp_leibniz_v2.py" -p "description=GP v2 with convergence-rate fitness, Leibniz injected at gen 0 (confounded)"

seldon artifact create Script -p "name=entropy_leibniz.py" -p "path=entropy-leibniz/entropy_leibniz.py" -p "description=Entropy GP v2 with info-theoretic fitness, Leibniz injected (confounded)"

seldon artifact create Script -p "name=rl_leibniz_v2.py" -p "path=EDA/rl-leibniz/rl_leibniz_v2.py" -p "description=RL v2 policy gradient approach (failed — diverges after T>20)"

seldon artifact create Script -p "name=aco_leibniz.py" -p "path=EDA/aco-leibniz/aco_leibniz.py" -p "description=Ant Colony Optimization approach (failed — collapses after T>40)"
```

After each command, record the UUID. You'll use these as `--script-id` when registering results.

---

## Phase 3: Register DataFile Artifacts

Register key data files (results files, convergence CSVs, JSON data).

```bash
# Entropy v3 minimal outputs
seldon artifact create DataFile -p "name=entropy_v3_minimal_results" -p "path=entropy-leibniz-v3/results_minimal.txt" -p "description=5-seed run results for entropy v3 minimal"

# GP v3 minimal outputs  
seldon artifact create DataFile -p "name=gp_v3_minimal_convergence" -p "path=gp-leibniz-v3/convergence_v3_minimal.csv" -p "description=Per-generation convergence data, GP v3 minimal 5 seeds"

# Sensitivity sweep data
seldon artifact create DataFile -p "name=gp_sensitivity_sweep_data" -p "path=gp-leibniz-v3/progress_sweep.json" -p "description=Full parameter sensitivity sweep data across alpha, lambda_p, pop_size, tournament_k"

# Stress test data
seldon artifact create DataFile -p "name=entropy_stress_L1_data" -p "path=entropy-leibniz-v3/stress_L1_data.json" -p "description=Entropy stress test level 1 (15 terminals) per-seed data"

# Fitness sensitivity data
seldon artifact create DataFile -p "name=fitness_approach2_w01_data" -p "path=entropy-leibniz-v3/fitness_approach2_w0.1_data.json" -p "description=Fitness sensitivity approach 2 w=0.1 (1/5 success)"
```

---

## Phase 4: Register Verified Results

Start a session, then register each key quantitative result. Link to generating scripts and data files using the UUIDs captured in Phases 2-3.

```bash
seldon briefing
# This starts a session and shows current state (should be empty graph)
```

**IMPORTANT:** For each `seldon result register` command below, substitute the actual UUIDs from Phase 2/3 for `--script-id` and `--data-ids`. If you don't have the script registered yet, omit `--script-id` — the result still gets registered, just without the provenance link (flagged as incomplete provenance in future briefings).

### Core discovery results

```bash
# Entropy v3 minimal: 5/5 discovery rate
seldon result register --value 1.0 --units "discovery_rate" \
  --description "Entropy fitness, minimal terminals {k,1,-1,2}, no injection: 5/5 seeds found Leibniz" \
  --script-id <entropy_v3_minimal_script_uuid>

# GP v3 minimal: 2/5 discovery rate (baseline pop=1000)
seldon result register --value 0.4 --units "discovery_rate" \
  --description "GP convergence fitness, minimal terminals, no injection, pop=1000: 2/5 seeds found Leibniz" \
  --script-id <gp_v3_minimal_script_uuid>

# GP v3 minimal pop=2000: 5/5 discovery rate (phase transition)
seldon result register --value 1.0 --units "discovery_rate" \
  --description "GP convergence fitness, minimal terminals, no injection, pop=2000: 5/5 seeds. Phase transition at pop=2000." \
  --script-id <gp_sensitivity_sweep_uuid>

# Entropy v3 minimal: total runtime
seldon result register --value 369.9 --units "seconds" \
  --description "Entropy v3 minimal total runtime for 5/5 discovery (all seeds)" \
  --script-id <entropy_v3_minimal_script_uuid>

# Information rate: 3.32 bits/decade (all Leibniz-equivalent seeds)
seldon result register --value 3.32 --units "bits_per_decade" \
  --description "Constant information gain rate for all discovered Leibniz expressions. Theoretical rate from error bound 1/(2T+1)."

# Entropy stress test L1: 0/5 at 15 terminals
seldon result register --value 0.0 --units "discovery_rate" \
  --description "Entropy fitness fails at 15 terminals (0/5). Wrong-limit attractor 5/((6+4k)(k-2)) scores ti=15.93 > Leibniz 15.29" \
  --script-id <entropy_stress_test_uuid>
```

### Wrong-limit attractor characterization

```bash
# Wrong-limit attractor info score exceeds Leibniz at T=10000
seldon result register --value 15.93 --units "bits" \
  --description "Wrong-limit attractor 5/((6+4k)(k-2)) achieves 15.93 bits at T=10000, exceeding Leibniz (15.29). Converges to ~0.7855 != pi/4." \
  --script-id <entropy_stress_test_uuid>

# Leibniz info at T=10000
seldon result register --value 15.29 --units "bits" \
  --description "Leibniz series info(T=10000) = -log2(|error|) = 15.29 bits" 
```

### Sensitivity analysis key results

```bash
# GP alpha=0.5 gives 4/5
seldon result register --value 0.8 --units "discovery_rate" \
  --description "GP v3 minimal with alpha=0.5 (convergence bonus weight): 4/5 seeds found Leibniz" \
  --script-id <gp_sensitivity_sweep_uuid>

# Fitness fix approach 2 w=0.1: 1/5 (only successful fitness modification)
seldon result register --value 0.2 --units "discovery_rate" \
  --description "Fitness sensitivity: large-T penalty w=0.1 on 15-terminal entropy: 1/5. Only fix that found Leibniz (seed 137, 389 gens)" \
  --script-id <fitness_sensitivity_test_uuid>
```

### Injection confound documentation

```bash
# v2 results were artifacts of injection
seldon result register --value 1.0 --units "discovery_rate" \
  --description "GP v2 and Entropy v2 5/5 results were CONFOUNDED: Leibniz tree injected at gen 0, survived via elitism. Not discovered." \
  --script-id <gp_v2_script_uuid>
```

After registering, verify each result and link to data files:

```bash
# For each result UUID:
seldon result verify <result_uuid>

# Link results to data files:
# seldon link create --from <result_uuid> --to <datafile_uuid> --rel-type computed_from
```

---

## Phase 5: Register Open Research Tasks

These are the active research threads that need tracking.

```bash
# Theoretical / analytical tasks
seldon task create --description "Implement operations-per-bit efficiency fitness: info_gain / tree_complexity. Test on 15-terminal problem."

seldon task create --description "Formal analysis: wrong-limit attractor density as function of terminal set size N. Combinatorial argument for why 4→5/5 and 15→0/5."

seldon task create --description "Formalize second-order kinetics interpretation: Leibniz error 1/(2T+1) as second-order rate law. Prove uniqueness of constant info rate under parsimony."

seldon task create --description "Vector space decomposition of fitness landscape. Min-gradient energy dispersion analysis (in progress)."

# Experimental tasks
seldon task create --description "Run entropy stress test levels L2-L4 (42, 44, 41 terminals). Stopped at L1=0/5 but may be informative with fitness fixes."

seldon task create --description "Test combined optimal config: pop=2000, alpha=0.5, entropy fitness, on 15-terminal set. Never tested — each fix was isolated."

seldon task create --description "Implement thermodynamic efficiency fitness: constant-rate free energy dissipation selector. The deeper physical objective from NOTES."

# Writing tasks
seldon task create --description "Rewrite medium draft closing section (Not to be PI-dantic). Current version lists 3 properties, article establishes 2."

seldon task create --description "Write academic paper targeting GECCO/EvoStar/Entropy. Structure: fitness landscape topology for infinite-horizon convergent processes."

# Provenance / cleanup tasks
seldon task create --description "Backfill EDA experiment results (RL v1/v2, ACO, GP v1) as Result artifacts with failure documentation."

seldon task create --description "Register v3 wide/hostile clean rerun results (all 0/5) with provenance links."
```

---

## Phase 6: Register Paper Sections (skeleton)

Create PaperSection artifacts for the evolving paper structure. These will be linked to Results via `cites` relationships as writing progresses.

```bash
seldon artifact create PaperSection -p "name=abstract" -p "description=Paper abstract — fitness landscape topology for infinite-horizon processes"

seldon artifact create PaperSection -p "name=introduction" -p "description=Problem framing: can ML rediscover fundamental mathematical formulas? Leibniz as test case."

seldon artifact create PaperSection -p "name=methods" -p "description=GP engine, entropy fitness, convergence-rate fitness, experimental design"

seldon artifact create PaperSection -p "name=results_discovery" -p "description=Discovery rates across conditions: injection confound, minimal terminals, sensitivity"

seldon artifact create PaperSection -p "name=results_attractors" -p "description=Wrong-limit attractor analysis: density, scoring, fitness landscape topology"

seldon artifact create PaperSection -p "name=discussion_thermodynamic" -p "description=Information-theoretic interpretation: second-order kinetics, constant dissipation rate, efficiency"

seldon artifact create PaperSection -p "name=conclusion" -p "description=Generalizable insight: define success as process properties, not target proximity"
```

---

## Phase 7: Validate

```bash
# Check project state
seldon status

# Run briefing to see if it surfaces useful context
seldon briefing

# List all results
seldon result list

# List open tasks  
seldon task list --open

# Trace provenance on a key result
seldon result trace <entropy_5_5_result_uuid>

# Check for incomplete provenance
seldon result check-stale
```

**Expected briefing output should show:**
- 11 open research tasks
- Results with incomplete provenance (no script links where UUIDs weren't available)
- Graph stats: ~25-30 artifacts, multiple relationship types
- No stale results (everything is freshly registered)

---

## Phase 8: Session Closeout

```bash
seldon closeout
```

Document what was done, commit `seldon.yaml` and `seldon_events.jsonl` to git. The `.gitignore` should NOT ignore these — they are the project's traceability state.

**Add to .gitignore (if not already):**
```
# Seldon temp files only
.seldon_session.yaml
```

**Do NOT gitignore:**
```
seldon.yaml
seldon_events.jsonl
```

---

## Success Criteria

1. `seldon briefing` produces a useful session start context — you read it and know what's open, what's stale, what needs doing
2. `seldon result trace` on any registered result shows the generating script and data files
3. `seldon task list --open` shows the actual research frontier — not stale items from 3 weeks ago
4. The JSONL event log captures the full audit trail of what was registered and when
5. Next session: `seldon briefing` surfaces this state without reading any handoff documents

---

## Notes for Execution

- This is a DOGFOOD run. Expect friction. Document what's missing or awkward.
- If a command fails or the CLI doesn't support something you need, note it in a `seldon_dogfood_notes.md` file in the project root.
- The point is not to perfectly register everything — it's to discover whether Seldon's current interface works for a real research workflow.
- If registering results without script UUIDs feels bad (because you have to run commands in sequence and copy-paste UUIDs), that's a real finding. Note it.
- If you wish you could register a result with a script path instead of UUID, note it. That's a feature gap.
- Key question after completion: "Would seldon briefing have prevented any of the problems I've actually had on this project?"
