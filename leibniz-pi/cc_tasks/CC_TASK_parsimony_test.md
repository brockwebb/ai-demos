# Claude Code Task: Parsimony Pressure Test — Force Canonical Form

## Context
Entropy v3 minimal finds Leibniz 5/5, but produces bloated algebraic equivalents:
- Seed 0: `(-(-1^k)) / ((-k) - (k - -1))` — 11 nodes
- Seed 1: `(-(-1^k)) / ((-1 - k) - k)` — 10 nodes  
- Seed 3: `(-1^k) / (k + (1 + k))` — 9 nodes (canonical complexity, non-canonical form)
- Seed 4: `(-1^k) / ((k * 2) - -1)` — 9 nodes

The canonical Leibniz is `(-1^k) / ((2*k) + 1)` at 9 nodes. The current parsimony penalty (LAMBDA_P = 0.005, costing 0.005 per node) creates only a 0.01 fitness difference between 9 and 11 nodes. That's not enough pressure to prefer the compact form.

If the slime mold analogy holds — finding the shortest path — the algorithm should produce the most compact expression, not a roundabout equivalent.

## What to Do
Run entropy v3 minimal with heavier parsimony. Same everything else: TERM_FIXED=["k",1,-1,2], EPHEMERALS=[], no injection, MAX_SEED=360s, 5 seeds.

### Parsimony values to test:
1. LAMBDA_P = 0.01 (2x current)
2. LAMBDA_P = 0.02 (4x current)  
3. LAMBDA_P = 0.05 (10x current)

### For each configuration, report:
- Seeds finding Leibniz (out of 5)
- Node count of each result
- The actual expression found
- Whether it's the 9-node canonical form or a bloated equivalent

### What we're looking for:
- Does heavier parsimony push results toward the 9-node canonical form?
- Does heavier parsimony BREAK discovery (algorithm can't find Leibniz at all because parsimony kills promising larger intermediates)?
- Is there a sweet spot where the algorithm both discovers AND simplifies?

### Implementation
Fork entropy_leibniz_v3_minimal.py, change only LAMBDA_P. Or parameterize it. Three configs × 5 seeds.

### Output
Create `entropy-leibniz-v3/parsimony_test_results.md`
