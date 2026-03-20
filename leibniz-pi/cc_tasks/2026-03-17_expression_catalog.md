# CC Task: Expression Catalog with Seldon Provenance

## Date: 2026-03-17

## Context

The project generated dozens of expressions across all experiments. The paper needs an appendix cataloging every expression found, in both raw (as-discovered) and simplified algebraic form, with metadata and full Seldon provenance. This catalog serves double duty: it is a paper appendix AND a set of registered artifacts in the graph.

## Objective

1. Parse all experiment result files (`_data.json`, `results*.txt`) across the repo
2. Extract every "best expression" per seed per experiment
3. For each expression, produce: raw form, simplified form, node count, fitness score, terminal set used, seed, experiment name, whether it was classified as Leibniz-equivalent, and any notable properties
4. Register each expression as a Seldon artifact with provenance
5. Produce an appendix markdown table for the paper

## Data Sources

Scan these directories for `_data.json` and `results*.txt` files:

| Directory | Experiments |
|-----------|------------|
| `gp-leibniz-v3/` | GP minimal, wide, hostile, sensitivity sweep |
| `entropy-leibniz-v3/` | Log-precision minimal, wide, hostile, stress test, fitness modifications, gradient tests, parsimony tests, scaling grid (all 28 cells) |
| `gp-leibniz-v3/results_gp_scaling_p5000/` | GP convergence-aware p=5000 column |
| `gp-leibniz-v3/results_gp_scaling_p10000/` | GP convergence-aware p=10000 column |
| `gp-leibniz-v3/results_gp_extended_t10_p5000/` | Extended time test |
| `gp-leibniz-v2/` | v2 confounded results (label as confounded) |
| `entropy-leibniz/` | v2 confounded results (label as confounded) |
| `EDA/` | RL, ACO, GP v1 failures (if expression data exists) |

## Expression Record Schema

Each expression gets these fields:

```yaml
id: expr_<experiment>_<seed>  # e.g. expr_logprec_minimal_seed42
raw_form: "(-(-1^k)) / ((-k) - (k - -1))"
simplified_form: "(-1)^k / (2k+1)"  # algebraic simplification
nodes: 11
fitness_score: 0.01102149
fitness_function: "log-precision"  # or "convergence-aware"
terminal_set: "{k, 1, -1, 2}"
terminal_count: 4
population_size: 1000
seed_value: 42
generations: 711
elapsed_seconds: 20.7
is_leibniz: true
classification: "leibniz-equivalent"  # or "wrong-limit-attractor", "trivial", "divergent"
notes: "bloated form, 11 nodes vs 9-node canonical"
```

Additional fields for wrong-limit attractors:
```yaml
limit_value: 0.7851  # approximate convergent limit (if known)
ti_at_10000: 15.93   # bits of precision at T=10000
monotonicity: 1.00
attractor_family: "rational-k/3"  # classification from research notes
```

Additional fields for notable expressions:
```yaml
notable: true
notable_reason: "Grandi-Leibniz hybrid: identical to Leibniz at all even T"
algebraic_decomposition: "S_Leibniz(T) - G(T) where G is Grandi series"
```

## Simplification Rules

For algebraic simplification:
- `k + k` → `2k`
- `- -1` → `+ 1`
- `-(-1^k)` → `(-1)^(k+1)`
- `(k * 2) - -1` → `2k + 1`
- `(-1 - k) - k` → `-(2k + 1)`

Use sympy if available for automated simplification. If not, apply pattern matching. Flag any expression where simplification is uncertain.

## Seldon Registration

For each expression:

1. Register as artifact:
   ```
   seldon artifact create \
     --name "expr_<experiment>_<seed>" \
     --type Expression \
     --path "<source_data_file>" \
     --description "<simplified_form>, <classification>"
   ```

2. Create provenance links:
   ```
   seldon link create \
     --from "expr_<experiment>_<seed>" \
     --to "<script_artifact>" \
     --type GENERATED_BY
   
   seldon link create \
     --from "expr_<experiment>_<seed>" \
     --to "<data_file_artifact>" \
     --type COMPUTED_FROM
   ```

3. For Leibniz-equivalent expressions, link to the Leibniz reference:
   ```
   seldon link create \
     --from "expr_<experiment>_<seed>" \
     --to "leibniz_series" \
     --type EQUIVALENT_TO
   ```

4. For notable expressions (Grandi-Leibniz, super-attractors), add tags:
   ```
   seldon artifact update \
     --name "expr_<experiment>_<seed>" \
     --tags "notable,grandi-leibniz,evaluation-horizon-trap"
   ```

## Output Files

### 1. Appendix table: `paper/sections/09_appendix_expressions.md`

Structure the appendix as:

```markdown
# Appendix A: Expression Catalog

## A.1 Leibniz-Equivalent Expressions

| Seed | Raw Form | Simplified | Nodes | Fitness | Experiment |
|------|----------|-----------|-------|---------|------------|
| ...  | ...      | ...       | ...   | ...     | ...        |

## A.2 Notable Wrong-Limit Attractors

| Seed | Raw Form | Simplified | Nodes | TI@10k | Limit | Family | Notes |
|------|----------|-----------|-------|--------|-------|--------|-------|
| ...  | ...      | ...       | ...   | ...    | ...   | ...    | ...   |

### A.2.1 The Grandi-Leibniz Attractor

[Full description from RESEARCH_NOTES.md "The Grandi-Leibniz attractor" section]

## A.3 Attractor Families by Terminal Count

[Organized by t=6, t=8, t=10+, t=15 families from research notes]

## A.4 Trivial and Divergent Expressions

[Parsimony collapse expressions, RL/ACO failures if data exists]
```

### 2. Machine-readable catalog: `paper/expression_catalog.json`

Full structured data for all expressions, one JSON object per expression with all fields from the schema above.

## Verification

After completion:
- `seldon artifact list --type Expression` shows all registered expressions
- Every Expression has GENERATED_BY and COMPUTED_FROM links
- `seldon paper build --no-render` resolves any result references in the appendix
- `seldon paper sync` updates the graph
- Cross-check expression count against total seeds run (should be ~140 from scaling grid + ~30 from other experiments)

## Known Expressions to Verify Are Captured

These must appear in the catalog (from research notes):

1. **Leibniz variants (t=4, log-precision minimal):** 5 expressions, seeds 42/7/137/2718/31415
2. **Leibniz variants (t=4, GP minimal):** 2 expressions, seeds 42/2718
3. **Leibniz variants (t=4, GP pop=2000):** 5 expressions
4. **Leibniz variants (t=15, pop=10000):** 2 expressions, seeds 137/2718 — canonical 9-node form
5. **Grandi-Leibniz attractor:** t=4/p=2000/seed=31415, `(-1^k) * (-k) / ((1/2) - (-k))`
6. **Wrong-limit super-attractor:** t=8/p=10000, `(4 - (4-(-3))^-2 - k/(-3))^-2`, ti=20.66
7. **5/((6+4k)(k-2)):** t=15 stress test seed 42, ti=15.93
8. **(-11)^-4 constant:** entropy hostile, 3/5 seeds locked on this
9. **t=6 family:** `((k/3 + c)^-2)` variants
10. **t=15 failure modes:** `(-5/(-5+k))^7`, `(7^7) * (-1^(k/-3))`, `(-4 + k/(-3))^-2`

## Do NOT

- Do not modify any experiment scripts or data files
- Do not rerun any experiments
- Do not modify existing paper sections (only create the new appendix)
- Do not modify existing CC task files
