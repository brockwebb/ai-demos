# CC Task: Fix Scaling Heatmap to Census Bureau Data Viz Standards

**Date:** 2026-03-27
**Priority:** Medium — visual quality fix for Figure 1

---

## Context

Figure 1 (scaling heatmap) has visual problems:
1. Text color is computed per cell but never applied — all labels are white, unreadable on yellow cells
2. Needs Census Bureau data visualization standards: white background, colorblind-friendly palette, descriptive title, 300 DPI
3. Phase boundary annotation clips at right edge
4. Aspect ratio is too wide

## Pre-Flight

1. Read `paper/figures/generate_figures.py` — understand the full script structure
2. Read the `make_fig1_heatmap` function specifically
3. Note: Only modify `make_fig1_heatmap`. Do NOT touch any other function or the verification logic.

---

## Step 1: Fix `make_fig1_heatmap` in `paper/figures/generate_figures.py`

Replace ONLY the `make_fig1_heatmap` function with a version that applies the following changes:

### Census Bureau standards
- **White background**: Use `theme_bw()` base or set `plot_background` and `panel_background` to white
- **Colorblind-friendly sequential palette**: Use a single-hue sequential blue palette. Map rate 0.0 → light gray (#f0f0f0), rate 1.0 → Census blue (#002b5c or similar dark blue). This gives clear visual separation between zero cells and nonzero cells. Use `scale_fill_gradientn` with colors like `["#f0f0f0", "#c6dbef", "#6baed6", "#2171b5", "#002b5c"]` (light gray through blues).
- **300 DPI**: Already set, keep it.
- **Descriptive title**: Keep existing title, it's fine.

### Bug fixes
- **Text color**: Use the computed `text_color` column in `geom_text`. Dark text (#333333) on light cells (rate >= 0.4), white on dark cells (rate < 0.4).
- **Phase boundary**: Move the text label inside the plot area. Use `x=3.5` or similar so it doesn't clip. Consider placing the label below the line rather than to the right, or use a shorter label like "phase boundary" at a position that fits.
- **Aspect ratio**: The heatmap has 7 rows × 4 columns. Set `figure_size=(6, 6)` or `(5.5, 5.5)` to get closer-to-square tiles.
- **Grid lines**: Remove all panel grid lines (`panel_grid_major=element_blank(), panel_grid_minor=element_blank()`). The tile borders provide the structure.

### Font
- Keep DejaVu Sans (it's available in the environment and is a clean sans-serif)

### Do NOT change
- The data (`SCALING_GRID` dictionary)
- The output filenames (`fig1_scaling_heatmap.pdf`, `fig1_scaling_heatmap.png`)
- Any other function in the script
- The verification logic

---

## Step 2: Regenerate Figure 1 Only

Run:
```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/figures/generate_figures.py
```

This regenerates ALL figures (they all share verification). Confirm:
- All verification checks pass
- `paper/figures/fig1_scaling_heatmap.png` is updated
- `paper/figures/fig1_scaling_heatmap.pdf` is updated
- Other figures are unchanged (they'll regenerate identically)

---

## Step 3: Visual Check

Open `paper/figures/fig1_scaling_heatmap.png` and verify:
- White background
- Blue sequential color ramp (light gray for 0, dark blue for 5)
- All cell labels are readable (dark text on light cells, white text on dark cells)
- Phase boundary annotation is fully visible, not clipped
- Tiles are closer to square
- No grid lines inside the heatmap area

---

## Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
seldon paper build --no-render
```

---

## Do NOT

- Do not modify any function other than `make_fig1_heatmap`
- Do not change the SCALING_GRID data
- Do not change output filenames
- Do not modify this task file
- Do not hardcode any values that come from SCALING_GRID
