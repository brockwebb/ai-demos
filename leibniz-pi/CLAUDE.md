# Leibniz-Pi

Research project: can genetic programming rediscover the Leibniz series for π/4 from arithmetic primitives and a convergence objective, without being given the formula?

## Status
Research experiments complete. Paper in iterative editing. Medium article will be a summary linking to preprint.

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
gp-leibniz-v2/                 # GP v2: convergence-aware fitness (v2 injected Leibniz at gen 0)
entropy-leibniz/               # Entropy fitness v2 (injected Leibniz at gen 0)
gp-leibniz-v3/                 # Clean GP experiments (no injection)
entropy-leibniz-v3/            # Clean log-precision experiments (no injection)
v3_results_summary.md          # Master results: all v3 experiments in one place
paper/                         # Paper manuscript and supporting files
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

**Log-precision / information-theoretic (entropy-leibniz, entropy-leibniz-v3):**
```
info(T) = -log₂(|partial_sum(T) - π/4|)
fitness = W1*(total_info/50) + W2*monotonicity + W3*(mean_rate/5) - LAMBDA_P*nodes
```
W1=0.02, W2=0.04, W3=0.03, LAMBDA_P=0.005

## Paper Writing

Paper lives in `paper/`. Seldon is initialized on this project (`seldon-leibniz-pi` Neo4j database). All 9 sections registered as PaperSection artifacts with content hashes.

### Foundation Files — READ THESE FIRST

| File | Purpose |
|------|---------|
| `paper/glossary.md` | Controlled vocabulary. Authoritative term definitions + banned synonyms. |
| `paper/keyword_index.md` | Auto-generated concordance. Which terms appear where. |
| `paper/evidence_map.md` | Results → claims → sections mapping. Provenance reference. |
| `paper/conventions.md` | Style rules + paper-specific terminology rules. |

**Before writing or editing any section, read `glossary.md` and `conventions.md`.** These are the constraint surface. Using an undefined term or a banned synonym is a violation.

### Writing Workflow — MANDATORY: edit → check → sync → build

1. Read `paper/glossary.md` and `paper/conventions.md` before writing any prose
2. Write/edit sections in `paper/sections/NN_name.md` (sorted by number)
3. Use `{{result:NAME:value}}` for all research numbers — NEVER write literals
4. **After ANY edit to section files:**
   ```bash
   python paper/check_glossary.py       # check terms + regenerate keyword index
   seldon paper sync                    # reconcile graph with disk
   seldon paper build --no-render       # verify references resolve
   ```
5. This includes CC tasks. If a task modifies section files or renames Result artifacts, the full check → sync → build cycle MUST follow.

### Reference Syntax
```
{{result:logprec_minimal_5_5:value}}         → 1.0
{{result:logprec_minimal_runtime:value}}     → 369.9
{{result:info_rate_3_32:value}}              → 3.32
{{result:wrong_limit_ti_15_93:value}}        → 15.93
```

Available results: `seldon result list` (11 verified results)
Result provenance: `seldon result trace <n>`

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
