# CC Task: Generate Publication-Quality Figures for Paper

**Date:** 2026-03-24
**Scope:** Create four figures for the Leibniz-π paper using Python (plotnine or matplotlib with ggplot theme)
**Output:** PDF and PNG to `paper/figures/`
**Register:** Each figure as a Seldon artifact (type: DataFile, tags: [figure, paper])

---

## Pre-Flight

1. Read `paper/conventions.md` for style rules.
2. Read `paper/evidence_map.md` for the Key Figures table and data sources.
3. Read `paper/verify_parsimony_values.py` for parsimony fitness computation logic.
4. Read `entropy-leibniz-v3/scaling_heatmap_results.md` for the scaling grid data.
5. Create directory `paper/figures/` if it does not exist.

## Style Requirements

All figures must follow Census Bureau data visualization standards (census.gov/content/dam/Census/library/working-papers/2017/demo/communicating-with-census-data-data-visualization.pdf) and produce publication-quality ggplot-style output.

### Mandatory style rules

- **Library:** Use `plotnine` (Python ggplot2 port). Install with `pip install plotnine` if needed. Fall back to matplotlib with `plt.style.use('ggplot')` only if plotnine fails.
- **Theme base:** `theme_minimal()` with customizations below.
- **Font:** "Helvetica" or "DejaVu Sans" (sans-serif). Title 12pt bold, axis labels 10pt, tick labels 9pt, annotation 8pt.
- **Colors:** Use a colorblind-friendly palette. For sequential data (heatmap): viridis or a single-hue blue ramp. For categorical/multi-line: use a qualitative palette from ColorBrewer (e.g., Set2 or Dark2). No red-green only distinctions.
- **Background:** White. No gray panel background.
- **Grid:** Light gray horizontal gridlines only (no vertical gridlines). Remove panel border.
- **Axes:** Thin black axis lines. Quantitative axes start at zero unless log-scale. Tick marks outward.
- **Legends:** Inside the plot area (top-right or bottom-right) where they do not obscure data. No legend box border.
- **Titles:** Descriptive, stating the variable and context. Not cute. Example: "Discovery Rate by Terminal Set Size and Population" not "The Phase Transition."
- **Source line:** Every figure gets a small annotation below the plot: "Source: [specific data file or script]"
- **Aspect ratio:** 4:3 default. Heatmap may be wider.
- **DPI:** 300 for PNG. PDF vector output.
- **No:** 3D effects, drop shadows, decorative elements, excessive tick marks, chartjunk.

---

## Figure 1: Scaling Grid Heatmap (Section 5.3)

**File:** `paper/figures/fig1_scaling_heatmap.{pdf,png}`

**What it shows:** The 7×4 discovery rate grid (terminals × population). The phase transition between t=8 and t=10.

**Data source:** Discover values from `entropy-leibniz-v3/scaling_heatmap_results.md`. Cross-check against Seldon results named `scaling_grid_t{T}_p{POP}`. The grid has 28 cells.

**Spec:**
- Heatmap (tiles) with t (terminal set size) on the y-axis (categorical: 4, 6, 8, 10, 12, 15, 20) and population on the x-axis (categorical: 1000, 2000, 5000, 10000).
- Color fill: sequential palette (viridis or blues). Map 0/5 to darkest, 5/5 to lightest (or reverse if more intuitive; the key pattern is "dark = failure, light = success").
- Annotate each cell with the discovery count (e.g., "5", "2", "0"). Use white text on dark cells, black text on light cells.
- Draw a visible horizontal separator or annotation line between t=8 and t=10 to mark the phase boundary.
- Title: "Discovery Rate Across Terminal Set Sizes and Population (Seeds Found / 5)"
- Y-axis label: "Terminal Set Size (t)"
- X-axis label: "Population Size"
- Source annotation: "Source: entropy-leibniz-v3/scaling_heatmap_results.md"

**Key values to discover (do not hardcode):** Read the results table from `scaling_heatmap_results.md`. Parse the "Seeds found / 5" column. The t=4/p=1000 value comes from `logprec_minimal_5_5`; the t=15/p=1000 value comes from `logprec_stress_l1_0_5`. Verify these are consistent.

---

## Figure 2: Precision vs T — Leibniz vs Wrong-Limit Attractor (Section 5.2)

**File:** `paper/figures/fig2_precision_vs_T.{pdf,png}`

**What it shows:** Log-precision trajectories of Leibniz and the Grandi-Leibniz attractor (wrong-limit attractor from seed 42, 15-terminal run). Leibniz gains precision steadily; the attractor plateaus.

**Data source:** Compute from formulas. Do NOT use pre-existing CSV files for this; compute fresh.

**Computation:**
- For T in [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]:
  - Leibniz: S(T) = sum_{k=0}^{T-1} (-1)^k / (2k+1). Precision = -log2(|S(T) - π/4|).
  - Attractor: S(T) = sum_{k=0}^{T-1} 5/((6+4k)(k-2)). Handle k=2 with safe division (return 0 for that term). Precision = -log2(|S(T) - π/4|).

**Spec:**
- Line plot. X-axis: T (log scale). Y-axis: Precision in bits.
- Two lines: Leibniz (solid, primary color) and Attractor (dashed, secondary color).
- Leibniz should show steady linear increase on this semi-log plot.
- Attractor should show initial rapid increase then plateau/ceiling.
- Legend with descriptive labels: "Leibniz: (-1)^k / (2k+1)" and "Attractor: 5/((6+4k)(k-2))"
- Title: "Log-Precision Trajectories: Leibniz Series vs Wrong-Limit Attractor"
- X-axis: "Evaluation Depth T (log scale)"
- Y-axis: "Precision (bits) = -log₂|S(T) - π/4|"
- Source: "Source: Computed from closed-form expressions"

**Verify:** The Leibniz precision at T=5 should match `leibniz_prec_t5` (4.34 bits) and at T=10000 should match `leibniz_ti_15_29` (15.29 bits). The attractor at T=10000 should match `wrong_limit_ti_15_93` (15.93 bits). If these do not match, STOP and report the discrepancy. Do not fudge.

---

## Figure 3: Parsimony Collapse (Section 5.4)

**File:** `paper/figures/fig3_parsimony_collapse.{pdf,png}`

**What it shows:** Fitness score as a function of parsimony coefficient λ_p for the 9-node Leibniz tree and the 3-node zero-constant attractor. Shows the crossover where zero-constant becomes favored.

**Data source:** Use the computation logic from `paper/verify_parsimony_values.py`. Read that file first and extract the constants (BASE_FITNESS, weights, node counts, ZERO_TI, etc.). Compute fitness for both trees across a range of λ_p.

**Computation:**
- λ_p range: 0.0 to 0.025 in steps of 0.0005
- Leibniz fitness(λ_p) = BASE_FITNESS - λ_p × 9
- Zero-constant fitness(λ_p) = W1×(ZERO_TI/50) + W2×0 + W3×0 - λ_p × 3
- Discover BASE_FITNESS, W1, ZERO_TI, and all other constants from `verify_parsimony_values.py`. Do not hardcode.

**Spec:**
- Line plot. X-axis: λ_p. Y-axis: Fitness score.
- Two lines: "9-node Leibniz tree" (solid) and "3-node zero-constant" (dashed).
- Mark the crossover point with a vertical dashed gray line and annotate with the λ_p value.
- Mark the baseline λ_p = 0.005 with a subtle vertical dotted line labeled "baseline."
- Mark λ_p = 0.01 with a subtle vertical dotted line labeled "collapse threshold."
- Shade the region where Leibniz fitness > zero-constant fitness in light blue (alpha=0.1).
- Title: "Parsimony Pressure: Fitness vs Size Penalty Coefficient"
- X-axis: "Parsimony Coefficient (λ_p)"
- Y-axis: "Fitness Score"
- Source: "Source: paper/verify_parsimony_values.py"

**Verify:** At λ_p=0.005, Leibniz fitness should match `parsimony_leibniz_fitness_baseline` (0.021021). At λ_p=0.01, Leibniz fitness should match `parsimony_leibniz_fitness_0_01` (-0.023979). Zero-constant at λ_p=0.01 should match `parsimony_zero_constant_fitness` (-0.029861). If discrepancies, STOP.

---

## Figure 4: Second-Order Kinetics — 1/Error vs T (Section 6.1)

**File:** `paper/figures/fig4_second_order_kinetics.{pdf,png}`

**What it shows:** Plotting 1/|error| vs T for the Leibniz series yields a straight line, the signature of second-order kinetics (1/error grows linearly with T). This is the empirical basis for the kinetics analogy in the Discussion.

**Data source:** Compute from Leibniz partial sums.

**Computation:**
- For T in range 1 to 500 (every integer, for a smooth line) and also the checkpoint values [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]:
  - S(T) = sum_{k=0}^{T-1} (-1)^k / (2k+1)
  - error = |S(T) - π/4|
  - inv_error = 1 / error
- Also compute the theoretical line: error ≈ 1/(2T+1), so 1/error ≈ 2T+1. Plot this as a reference.

**Spec:**
- Line plot. X-axis: T. Y-axis: 1/|error|.
- Plot the actual computed 1/error as a solid line.
- Plot the theoretical 2T+1 as a dashed gray reference line.
- The near-perfect overlap demonstrates the second-order kinetics structure.
- Use linear axes (NOT log scale) to make the linearity visually obvious.
- Title: "Reciprocal Error vs Evaluation Depth: Second-Order Rate Structure"
- X-axis: "Evaluation Depth T"
- Y-axis: "1 / |S(T) - π/4|"
- Annotation: Small text noting "Slope ≈ 2, consistent with error ≈ 1/(2T+1)"
- Source: "Source: Computed from Leibniz partial sums"
- For the full-range version (T up to 10000), also produce a second version with log-log axes to show the linearity persists across scales. Save as `fig4b_second_order_loglog.{pdf,png}`.

---

## Post-Flight

1. Verify all figures render correctly: `open paper/figures/fig*.png`
2. Run `seldon paper sync` to pick up any new artifacts.
3. Register each figure in Seldon:
   ```
   seldon artifact add --name fig1_scaling_heatmap --type DataFile --path paper/figures/fig1_scaling_heatmap.pdf --tags figure,paper,results
   seldon artifact add --name fig2_precision_vs_T --type DataFile --path paper/figures/fig2_precision_vs_T.pdf --tags figure,paper,results
   seldon artifact add --name fig3_parsimony_collapse --type DataFile --path paper/figures/fig3_parsimony_collapse.pdf --tags figure,paper,results
   seldon artifact add --name fig4_second_order_kinetics --type DataFile --path paper/figures/fig4_second_order_kinetics.pdf --tags figure,paper,results
   ```
4. Report: list all figures generated, verification checks (pass/fail for each registered value match), and any discrepancies.

## Do NOT

- Do not hardcode any numeric values. Discover everything from source files.
- Do not modify any existing files outside `paper/figures/`.
- Do not use dark backgrounds (this is an academic paper, not a Medium article).
- Do not use pie charts or 3D effects.
- Do not skip verification checks. If a computed value does not match a registered Seldon result, STOP and report.
