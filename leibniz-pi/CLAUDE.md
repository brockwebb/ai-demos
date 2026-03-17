# Leibniz-Pi

Research project: can genetic programming rediscover the Leibniz series for π/4 from arithmetic primitives and a convergence objective, without being given the formula?

## Status
Research experiments complete. Next: preprint paper (to be written in this repo). Medium article will be a summary linking to preprint.

## Research Notes
Findings, theoretical observations, experiment progression, and preprint outline: `RESEARCH_NOTES.md`

## How to Run Experiments

All v3 experiments use the same pattern:
```bash
cd <experiment-dir>
python3 <script>.py
```

Each run produces: `results*.txt` (human-readable), `*_data.json` (machine-readable), `convergence*.csv` (per-generation data).

**Standard seed values:** 42, 7, 137, 2718, 31415 (5 seeds across all experiments)  
**Convention since v3:** No Leibniz injection into initial population. Pure random init.  
**Time budget:** MAX_SEED=360s (6 min/seed), MAX_TOTAL=1800s (30 min/run)

## Repo Structure

```
EDA/                           # Failed early experiments (RL v1/v2, ACO, GP v1)
  rl-leibniz/                  
  aco-leibniz/                 
  gp-leibniz/                  

gp-leibniz-v2/                 # GP v2: convergence-aware fitness (v2 injected Leibniz at gen 0)
  gp_leibniz_v2.py             
  gp_leibniz_v2_viz.html       # Interactive viz (JSON embedded, works on file://)

entropy-leibniz/               # Entropy fitness v2 (injected Leibniz at gen 0)
  entropy_leibniz.py           
  entropy_leibniz_viz.html     # Interactive viz (JSON embedded, works on file://)

gp-leibniz-v3/                 # Clean GP experiments (no injection)
  gp_leibniz_v3_wide.py        # 42 terminals
  gp_leibniz_v3_hostile.py     # 44 terminals, no 2
  gp_leibniz_v3_minimal.py     # 4 terminals {k, 1, -1, 2}
  gp_sensitivity_sweep.py      # Parameterized sweep (--alpha, --lambda_p, --pop_size, --tournament_k)
  parameter_sensitivity.md     # Sweep results

entropy-leibniz-v3/            # Clean entropy experiments (no injection)
  entropy_leibniz_v3_wide.py   # 42 terminals
  entropy_leibniz_v3_hostile.py # 44 terminals, no 2
  entropy_leibniz_v3_minimal.py # 4 terminals {k, 1, -1, 2}
  entropy_stress_test.py       # Progressive terminal set difficulty (--level)
  stress_test_results.md       
  fitness_sensitivity_test.py  # Extended checkpoints, large-T penalty, rate consistency
  fitness_sensitivity_results.md
  gradient_fitness_test.py     # Gradient-based selection (thermodynamic framing removed)
  gradient_fitness_results.md  
  parsimony_test.py            # Heavier parsimony pressure sweep
  parsimony_test_results.md    

v3_results_summary.md          # Master results: all v3 experiments in one place
medium_draft_final.md          # Working draft (will become Medium summary)
figures/paperbanana/           # Diagram assets
CC_TASK_*.md                   # Claude Code task instructions (historical)
```

## GP Engine (shared across all experiments)

- Ramped half-and-half tree initialization
- Subtree crossover (P_CROSS=0.70) and subtree mutation (P_MUT=0.20)
- Tournament selection (TOURNAMENT_K=7 default)
- Elitism (N_ELITE=5)
- Fitness cache keyed by expression string
- Diversity injection when population stagnates
- Operators: add, sub, mul, div, pow, neg
- Safe division (div by 0 → 1), safe pow (overflow → penalty)

## Fitness Functions

**GP convergence-rate (gp-leibniz-v2, gp-leibniz-v3):**
```
fitness = accuracy + ALPHA * convergence_bonus - LAMBDA_P * node_count
accuracy = -mean(|partial_sum(T) - π/4| for T in T_EVAL)
convergence_bonus = fraction of consecutive T-pairs with >5% error reduction
```

**Entropy / information-theoretic (entropy-leibniz, entropy-leibniz-v3):**
```
info(T) = -log₂(|partial_sum(T) - π/4|)
fitness = W1*(total_info/50) + W2*monotonicity + W3*(mean_rate/5) - LAMBDA_P*nodes
```
W1=0.02, W2=0.04, W3=0.03, LAMBDA_P=0.005

## Key Files for Results
- `v3_results_summary.md` — master summary of all v3 experiments
- `gp-leibniz-v3/parameter_sensitivity.md` — GP parameter sweep
- `entropy-leibniz-v3/stress_test_results.md` — terminal set scaling
- `entropy-leibniz-v3/fitness_sensitivity_results.md` — fitness modifications
- `entropy-leibniz-v3/gradient_fitness_results.md` — gradient-based selection results
- `entropy-leibniz-v3/parsimony_test_results.md` — parsimony pressure

## Paper Writing

Paper lives in `paper/`. Seldon is initialized on this project (44 artifacts, 11 verified results in `seldon-leibniz-pi` Neo4j database).

### Writing Workflow
1. Read `paper/conventions.md` before writing any prose
2. Write sections in `paper/sections/NN_name.md` (sorted by number)
3. Use `{{result:NAME:value}}` for all research numbers — NEVER write literals
4. Run `seldon paper audit paper/sections/*.md` after editing to check prose quality
5. Run `seldon paper build` to resolve references, check structural integrity, assemble .qmd
6. Run `seldon paper build --no-render` if Quarto isn't needed yet

### Reference Syntax
```
{{result:entropy_minimal_5_5:value}}         → 1.0
{{result:entropy_minimal_runtime:value}}     → 369.9
{{result:info_rate_3_32:value}}              → 3.32
{{result:wrong_limit_ti_15_93:value}}        → 15.93
```

Available results: `seldon result list` (11 verified results)
Result provenance: `seldon result trace <name>`

### QC Config
- `paper/paper_qc_config.yaml` — prose rules (Tier 2)
- `paper/paper_style_config.yaml` — banned words, clichés (Tier 3)
- `paper/conventions.md` — human-readable writing rules

### Key Convention Rules
- No em dashes. Zero tolerance.
- No inline bold in prose.
- Max 35 words per sentence.
- Min 2 sentences per paragraph.
- "We" throughout, active voice preferred.
- No "novel", "robust", "leverage", "utilize".
- No throat-clearing ("It is worth noting...").
- See `paper/conventions.md` for full list.

## Known Issues
- v2 HTML viz files originally loaded JSON via fetch() (fails on file://). Fixed versions embed JSON inline.
- v2 experiments injected Leibniz at gen 0. Results are valid as "recognition" tests, not "discovery" tests. All v3 experiments remove injection.
