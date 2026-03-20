# CC Task: Add Grandi-Leibniz Attractor + Simplified Forms to Expression Catalog

## Date: 2026-03-17

## Context

The expression catalog (`paper/sections/09_appendix_expressions.md`) is missing two things:

1. **The Grandi-Leibniz attractor** — the most interesting expression in the project. Found at t=4/p=2000/seed=31415. Referenced in A.3.1 but has no table entry and no dedicated subsection. It needs its own subsection (A.2.3) with the full algebraic decomposition.

2. **Simplified forms for wrong-limit attractors.** The catalog shows only raw forms. Add a "Simplified" column using sympy.

## Objective

All data must be discovered from source files and the Seldon graph. Do NOT use hardcoded values. Every number, expression, fitness score, and node count must come from either a `_data.json` file or a Seldon query.

## Steps

### 1. Find the Grandi-Leibniz expression from source data

Read `entropy-leibniz-v3/scaling_heatmap_t4_p2000_data.json`. Find the record for seed value 31415. Extract:
- raw expression
- node count
- fitness score
- generations
- elapsed time
- any other metadata present

Do NOT assume any of these values. Read them from the file.

### 2. Verify against Seldon graph

```bash
seldon artifact list --type DataFile
```

Find the artifact for `scaling_heatmap_t4_p2000_data.json`. If it doesn't exist, register it. Confirm provenance links exist to the generating script.

### 3. Simplify algebraically using sympy

Take the raw expression from step 1 and simplify it with sympy. Verify the decomposition:
- Does it reduce to a form involving `(-1)^k` and `2k/(2k+1)` or equivalent?
- Compute partial sums at T=5, T=10, T=20 and compare to Leibniz partial sums at the same T
- Verify: are they identical at even T and differ by exactly 1 at odd T?

Document what sympy produces. If the decomposition into `S_Leibniz(T) - G(T)` holds, state it. If sympy produces something different, use what sympy says.

### 4. Check evaluation checkpoint structure

Read the checkpoint set from the log-precision fitness (find it in `entropy_leibniz_v3_minimal.py` or equivalent script). Count how many checkpoints are even vs odd. This determines why the fitness couldn't distinguish the attractor from Leibniz.

Do NOT assume 10 of 11 are even. Count them from the source code.

### 5. Register as a Seldon artifact

```bash
seldon artifact create \
  --name "expr_grandi_leibniz_t4_p2000_seed31415" \
  --type DataFile \
  --path "entropy-leibniz-v3/scaling_heatmap_t4_p2000_data.json" \
  --description "<use the simplified form and classification discovered in steps 1-3>" \
  --tags "notable,grandi-leibniz,evaluation-horizon-trap,wrong-limit-attractor"
```

Create provenance links to the generating script and source data file. Use `seldon artifact list` to find the correct artifact names — do not guess.

### 6. Add Section A.2.3 to the appendix

Insert after A.2.2 in `paper/sections/09_appendix_expressions.md`. Write the subsection based on what you discovered in steps 1-4. Include:
- The raw expression (from the data file)
- The simplified form (from sympy)
- The algebraic decomposition (verified computationally, not assumed)
- Why the fitness couldn't distinguish it (from the checkpoint count in step 4)
- The fitness score and node count (from the data file)

Cross-reference the RESEARCH_NOTES.md section "The Grandi-Leibniz attractor" for narrative context, but verify every claim against source data before including it.

### 7. Add the Grandi-Leibniz to the A.2 notable attractors table

Add a row using only values extracted from the data file in step 1.

### 8. Add simplified forms to all A.2 attractor entries

For each expression currently in the A.2 table:
- Parse the raw form
- Simplify with sympy
- Add as a "Simplified" column

Use the expressions as they appear in the existing table. Simplify each computationally. Do not manually simplify.

### 9. Sync and verify

```bash
seldon paper sync
seldon paper build --no-render
seldon paper audit paper/sections/09_appendix_expressions.md
```

## Verification

- The Grandi-Leibniz artifact exists in the graph with provenance links
- Section A.2.3 exists with algebraic decomposition verified against computed partial sums
- The A.2 table has a Simplified column populated by sympy
- The Grandi-Leibniz appears in the A.2 table
- All numbers in the new content come from source files, not from this task spec
- `seldon paper build --no-render` passes
- `seldon paper audit` passes on the appendix

## Do NOT

- Do not hardcode any expression, fitness score, node count, or checkpoint count — discover all from source files
- Do not modify any other paper sections
- Do not modify existing CC task files
- Do not modify experiment scripts or data files
- Do not rerun any experiments
- Do not remove any existing content from the appendix — only add
