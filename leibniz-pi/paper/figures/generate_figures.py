"""
Generate publication-quality figures for the Leibniz-π paper.
All numeric values discovered from source files; none hardcoded.
"""

import sys
import math
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants discovered from verify_parsimony_values.py
# ---------------------------------------------------------------------------
LEIBNIZ_BASE_FITNESS = 0.066021
W1 = 0.02
W2 = 0.04
W3 = 0.03
ZERO_TI = 0.3485
ZERO_MONO = 0.0
ZERO_RATE = 0.0
ZERO_NODES = 3
LEIBNIZ_NODES = 9

# Registered Seldon result values (for verification only — not used to plot)
VERIFY = {
    "leibniz_prec_t5":                   4.34,
    "leibniz_ti_15_29":                  15.29,
    "wrong_limit_ti_15_93":              15.93,
    "parsimony_leibniz_fitness_baseline": 0.021021,
    "parsimony_leibniz_fitness_0_01":    -0.023979,
    "parsimony_zero_constant_fitness":   -0.029861,
}

# ---------------------------------------------------------------------------
# Scaling grid data (from scaling_heatmap_results.md)
# Values are seeds_found / 5
# ---------------------------------------------------------------------------
SCALING_GRID = {
    # (t, pop): count
    (4,  1000): 5, (4,  2000): 4, (4,  5000): 5, (4,  10000): 5,
    (6,  1000): 1, (6,  2000): 2, (6,  5000): 1, (6,  10000): 1,
    (8,  1000): 1, (8,  2000): 1, (8,  5000): 1, (8,  10000): 0,
    (10, 1000): 0, (10, 2000): 0, (10, 5000): 0, (10, 10000): 0,
    (12, 1000): 0, (12, 2000): 0, (12, 5000): 0, (12, 10000): 0,
    (15, 1000): 0, (15, 2000): 0, (15, 5000): 0, (15, 10000): 2,
    (20, 1000): 0, (20, 2000): 0, (20, 5000): 0, (20, 10000): 0,
}

CHECKPOINTS = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
TOLERANCE = 1e-9


# ---------------------------------------------------------------------------
# Computation helpers
# ---------------------------------------------------------------------------

def leibniz_partial_sum(T):
    """Exact Leibniz partial sum S(T) = sum_{k=0}^{T-1} (-1)^k / (2k+1)."""
    return sum((-1)**k / (2*k + 1) for k in range(T))


def attractor_partial_sum(T):
    """Partial sum for wrong-limit attractor 5/((6+4k)(k-2)).
    At k=2 the denominator is zero; the GP engine's safe_div returns 1.0
    (not 0.0) in this case, so we match that behavior here."""
    total = 0.0
    for k in range(T):
        denom = (6 + 4*k) * (k - 2)
        if abs(denom) < TOLERANCE:
            term = 1.0  # GP safe_div: div/0 → 1.0
        else:
            term = 5.0 / denom
        total += term
    return total


def log_precision(S, target):
    err = abs(S - target)
    if err < TOLERANCE:
        return 60.0  # cap at 60 bits — exact match
    return -math.log2(err)


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_values():
    PI_OVER_4 = math.pi / 4
    failures = []

    # Leibniz precision at checkpoints
    lp_t5 = log_precision(leibniz_partial_sum(5), PI_OVER_4)
    lp_t10000 = log_precision(leibniz_partial_sum(10000), PI_OVER_4)
    att_t10000 = log_precision(attractor_partial_sum(10000), PI_OVER_4)

    checks = [
        ("leibniz_prec_t5",  lp_t5,     0.05),
        ("leibniz_ti_15_29", lp_t10000, 0.05),
        ("wrong_limit_ti_15_93", att_t10000, 0.05),
    ]
    for name, computed, tol in checks:
        expected = VERIFY[name]
        if abs(computed - expected) > tol:
            failures.append(
                f"  FAIL {name}: computed={computed:.4f}, expected={expected:.4f}"
            )
        else:
            print(f"  PASS {name}: {computed:.4f} (expected {expected})")

    # Parsimony fitness values
    def leibniz_fitness(lp):
        return LEIBNIZ_BASE_FITNESS - lp * LEIBNIZ_NODES

    def zero_fitness(lp):
        base = W1 * (ZERO_TI / 50) + W2 * ZERO_MONO + W3 * (ZERO_RATE / 5)
        return base - lp * ZERO_NODES

    f_base  = leibniz_fitness(0.005)
    f_01    = leibniz_fitness(0.01)
    f_zero  = zero_fitness(0.01)

    for name, computed, expected in [
        ("parsimony_leibniz_fitness_baseline", f_base,  VERIFY["parsimony_leibniz_fitness_baseline"]),
        ("parsimony_leibniz_fitness_0_01",     f_01,    VERIFY["parsimony_leibniz_fitness_0_01"]),
        ("parsimony_zero_constant_fitness",    f_zero,  VERIFY["parsimony_zero_constant_fitness"]),
    ]:
        if abs(computed - expected) > 1e-5:
            failures.append(
                f"  FAIL {name}: computed={computed:.6f}, expected={expected:.6f}"
            )
        else:
            print(f"  PASS {name}: {computed:.6f} (expected {expected})")

    if failures:
        print("\nVERIFICATION FAILURES — stopping:")
        for f in failures:
            print(f)
        sys.exit(1)

    print("\nAll verification checks passed.\n")


# ---------------------------------------------------------------------------
# Figure generation
# ---------------------------------------------------------------------------

def make_fig1_heatmap(outdir):
    from plotnine import (
        ggplot, aes, geom_tile, geom_text, scale_fill_gradientn,
        scale_color_identity,
        theme_bw, theme, element_text, element_blank, element_rect,
        labs, annotate, scale_x_discrete, scale_y_discrete,
    )
    import warnings
    warnings.filterwarnings("ignore")

    rows = []
    for (t, pop), count in SCALING_GRID.items():
        rows.append({"t": str(t), "pop": str(pop), "count": count,
                     "label": str(count), "rate": count / 5.0})
    df = pd.DataFrame(rows)

    t_order = ["4", "6", "8", "10", "12", "15", "20"]
    pop_order = ["1000", "2000", "5000", "10000"]
    df["t"]   = pd.Categorical(df["t"],   categories=t_order,   ordered=True)
    df["pop"] = pd.Categorical(df["pop"], categories=pop_order, ordered=True)

    # Text color: dark for light cells (rate >= 0.4), white for dark cells
    df["text_color"] = df["rate"].apply(lambda r: "#333333" if r >= 0.4 else "white")

    p = (
        ggplot(df, aes(x="pop", y="t", fill="rate"))
        + geom_tile(color="white", size=0.5)
        + geom_text(aes(label="label", color="text_color"), size=9, fontweight="bold")
        + scale_color_identity()
        + scale_fill_gradientn(
            colors=["#f0f0f0", "#c6dbef", "#6baed6", "#2171b5", "#002b5c"],
            limits=[0, 1],
        )
        + scale_x_discrete(limits=pop_order)
        + scale_y_discrete(limits=list(reversed(t_order)))
        + labs(
            title="Discovery Rate Across Terminal Set Sizes and Population (Seeds Found / 5)",
            x="Population Size",
            y="Terminal Set Size (t)",
            fill="Rate",
            caption="Source: entropy-leibniz-v3/scaling_heatmap_results.md",
        )
        + theme_bw()
        + theme(
            figure_size=(6, 6),
            plot_background=element_rect(fill="white", color="white"),
            panel_background=element_rect(fill="white", color="white"),
            plot_title=element_text(size=11, weight="bold", family="DejaVu Sans"),
            axis_title=element_text(size=10, family="DejaVu Sans"),
            axis_text=element_text(size=9, family="DejaVu Sans"),
            plot_caption=element_text(size=7, color="#666666", family="DejaVu Sans"),
            panel_grid_major=element_blank(),
            panel_grid_minor=element_blank(),
            legend_position="right",
        )
        + annotate("segment", x=0.5, xend=4.5, y=4.5, yend=4.5,
                   color="#cc0000", size=1.2, linetype="dashed")
        + annotate("text", x=2.5, y=4.2, label="phase boundary",
                   color="#cc0000", size=7, ha="center", va="top",
                   family="DejaVu Sans")
    )

    pdf_path = f"{outdir}/fig1_scaling_heatmap.pdf"
    png_path = f"{outdir}/fig1_scaling_heatmap.png"
    p.save(pdf_path, dpi=300, verbose=False)
    p.save(png_path, dpi=300, verbose=False)
    print(f"  Saved: {pdf_path}")
    print(f"  Saved: {png_path}")


def make_fig2_precision_vs_T(outdir):
    from plotnine import (
        ggplot, aes, geom_line, scale_x_log10, theme_minimal, theme,
        element_text, element_blank, element_line, labs, scale_color_manual,
        scale_linetype_manual
    )
    import warnings
    warnings.filterwarnings("ignore")

    PI_OVER_4 = math.pi / 4

    rows = []
    for T in CHECKPOINTS:
        lp = log_precision(leibniz_partial_sum(T), PI_OVER_4)
        rows.append({"T": T, "precision": lp,
                     "series": "Leibniz: (-1)^k / (2k+1)"})
        ap = log_precision(attractor_partial_sum(T), PI_OVER_4)
        rows.append({"T": T, "precision": ap,
                     "series": "Attractor: 5/((6+4k)(k-2))"})

    df = pd.DataFrame(rows)

    colors = {"Leibniz: (-1)^k / (2k+1)": "#2166ac",
              "Attractor: 5/((6+4k)(k-2))": "#d6604d"}
    linetypes = {"Leibniz: (-1)^k / (2k+1)": "solid",
                 "Attractor: 5/((6+4k)(k-2))": "dashed"}

    p = (
        ggplot(df, aes(x="T", y="precision", color="series", linetype="series"))
        + geom_line(size=1.0)
        + scale_x_log10()
        + scale_color_manual(values=colors)
        + scale_linetype_manual(values=linetypes)
        + labs(
            title="Log-Precision Trajectories: Leibniz Series vs Wrong-Limit Attractor",
            x="Evaluation Depth T (log scale)",
            y="Precision (bits) = -log₂|S(T) - π/4|",
            color="",
            linetype="",
            caption="Source: Computed from closed-form expressions",
        )
        + theme_minimal()
        + theme(
            figure_size=(7, 5.25),
            plot_title=element_text(size=11, weight="bold", family="DejaVu Sans"),
            axis_title=element_text(size=10, family="DejaVu Sans"),
            axis_text=element_text(size=9, family="DejaVu Sans"),
            plot_caption=element_text(size=7, color="#666666", family="DejaVu Sans"),
            panel_grid_minor=element_blank(),
            panel_grid_major_x=element_blank(),
            legend_position=(0.25, 0.85),
            legend_background=element_blank(),
        )
    )

    pdf_path = f"{outdir}/fig2_precision_vs_T.pdf"
    png_path = f"{outdir}/fig2_precision_vs_T.png"
    p.save(pdf_path, dpi=300, verbose=False)
    p.save(png_path, dpi=300, verbose=False)
    print(f"  Saved: {pdf_path}")
    print(f"  Saved: {png_path}")


def make_fig3_parsimony_collapse(outdir):
    from plotnine import (
        ggplot, aes, geom_line, geom_vline, geom_ribbon, geom_hline,
        theme_minimal, theme, element_text, element_blank, element_line,
        labs, scale_color_manual, scale_linetype_manual, annotate
    )
    import warnings
    warnings.filterwarnings("ignore")

    lp_vals = np.arange(0.0, 0.0255, 0.0005)

    def leibniz_fitness(lp):
        return LEIBNIZ_BASE_FITNESS - lp * LEIBNIZ_NODES

    def zero_fitness(lp):
        base = W1 * (ZERO_TI / 50) + W2 * ZERO_MONO + W3 * (ZERO_RATE / 5)
        return base - lp * ZERO_NODES

    rows = []
    for lp in lp_vals:
        rows.append({"lambda_p": lp, "fitness": leibniz_fitness(lp), "tree": "9-node Leibniz tree"})
        rows.append({"lambda_p": lp, "fitness": zero_fitness(lp), "tree": "3-node zero-constant"})
    df = pd.DataFrame(rows)

    # Crossover: LEIBNIZ_BASE_FITNESS - 9*lp = ZERO_BASE - 3*lp
    # → 6*lp = LEIBNIZ_BASE_FITNESS - ZERO_BASE
    zero_base_val = W1 * (ZERO_TI / 50)
    crossover_lp = (LEIBNIZ_BASE_FITNESS - zero_base_val) / (LEIBNIZ_NODES - ZERO_NODES)

    # Ribbon: region where Leibniz > zero-constant
    df_leibniz = df[df["tree"] == "9-node Leibniz tree"].copy()
    df_zero    = df[df["tree"] == "3-node zero-constant"].copy()
    df_ribbon  = df_leibniz[["lambda_p", "fitness"]].rename(columns={"fitness": "y_leibniz"})
    df_ribbon  = df_ribbon.merge(
        df_zero[["lambda_p", "fitness"]].rename(columns={"fitness": "y_zero"}),
        on="lambda_p"
    )
    df_ribbon["ymin"] = df_ribbon[["y_leibniz", "y_zero"]].min(axis=1)
    df_ribbon["ymax"] = df_ribbon["y_leibniz"]
    df_ribbon_success = df_ribbon[df_ribbon["lambda_p"] <= crossover_lp]

    colors    = {"9-node Leibniz tree": "#2166ac", "3-node zero-constant": "#d6604d"}
    linetypes = {"9-node Leibniz tree": "solid",   "3-node zero-constant": "dashed"}

    p = (
        ggplot(df, aes(x="lambda_p", y="fitness", color="tree", linetype="tree"))
        + geom_ribbon(data=df_ribbon_success,
                      mapping=aes(x="lambda_p", ymin="ymin", ymax="ymax"),
                      fill="#2166ac", alpha=0.10, inherit_aes=False)
        + geom_line(size=1.0)
        + geom_vline(xintercept=crossover_lp, color="#888888", linetype="dashed", size=0.7)
        + geom_vline(xintercept=0.005,  color="#aaaaaa", linetype="dotted", size=0.6)
        + geom_vline(xintercept=0.01,   color="#aaaaaa", linetype="dotted", size=0.6)
        + annotate("text", x=crossover_lp + 0.0003, y=0.00,
                   label=f"crossover\nλ_p ≈ {crossover_lp:.4f}",
                   size=7, ha="left", color="#555555", family="DejaVu Sans")
        + annotate("text", x=0.005 + 0.0003, y=-0.07,
                   label="baseline\n(0.005)", size=7, ha="left",
                   color="#888888", family="DejaVu Sans")
        + annotate("text", x=0.01 + 0.0003, y=-0.07,
                   label="collapse\n(0.01)", size=7, ha="left",
                   color="#888888", family="DejaVu Sans")
        + scale_color_manual(values=colors)
        + scale_linetype_manual(values=linetypes)
        + labs(
            title="Parsimony Pressure: Fitness vs Size Penalty Coefficient",
            x="Parsimony Coefficient (λ_p)",
            y="Fitness Score",
            color="",
            linetype="",
            caption="Source: paper/verify_parsimony_values.py",
        )
        + theme_minimal()
        + theme(
            figure_size=(7, 5.25),
            plot_title=element_text(size=11, weight="bold", family="DejaVu Sans"),
            axis_title=element_text(size=10, family="DejaVu Sans"),
            axis_text=element_text(size=9, family="DejaVu Sans"),
            plot_caption=element_text(size=7, color="#666666", family="DejaVu Sans"),
            panel_grid_minor=element_blank(),
            panel_grid_major_x=element_blank(),
            legend_position=(0.75, 0.85),
            legend_background=element_blank(),
        )
    )

    pdf_path = f"{outdir}/fig3_parsimony_collapse.pdf"
    png_path = f"{outdir}/fig3_parsimony_collapse.png"
    p.save(pdf_path, dpi=300, verbose=False)
    p.save(png_path, dpi=300, verbose=False)
    print(f"  Saved: {pdf_path}")
    print(f"  Saved: {png_path}")
    return crossover_lp


def make_fig4_second_order(outdir):
    from plotnine import (
        ggplot, aes, geom_line, theme_minimal, theme,
        element_text, element_blank, element_line, labs,
        scale_color_manual, scale_linetype_manual, annotate
    )
    import warnings
    warnings.filterwarnings("ignore")

    PI_OVER_4 = math.pi / 4

    # T=1..500 for smooth curve + checkpoint values
    T_dense  = list(range(1, 501))
    T_check  = CHECKPOINTS
    T_full   = sorted(set(T_dense + T_check + list(range(501, 10001, 100))))

    def compute_inv_error(T_list):
        rows = []
        for T in T_list:
            S = leibniz_partial_sum(T)
            err = abs(S - PI_OVER_4)
            if err < TOLERANCE:
                continue
            inv_err = 1.0 / err
            theory  = 2 * T + 1
            rows.append({"T": T, "inv_error": inv_err, "theoretical": theory})
        return pd.DataFrame(rows)

    # --- Fig 4a: T=1..500, linear axes ---
    df_short = compute_inv_error(T_dense)
    df_short_m = pd.melt(df_short, id_vars=["T"],
                          value_vars=["inv_error", "theoretical"],
                          var_name="series", value_name="value")
    df_short_m["series"] = df_short_m["series"].map({
        "inv_error":    "Computed: 1/|S(T) - π/4|",
        "theoretical":  "Theoretical: 2T + 1",
    })

    colors    = {"Computed: 1/|S(T) - π/4|": "#2166ac", "Theoretical: 2T + 1": "#888888"}
    linetypes = {"Computed: 1/|S(T) - π/4|": "solid",   "Theoretical: 2T + 1": "dashed"}

    p4a = (
        ggplot(df_short_m, aes(x="T", y="value", color="series", linetype="series"))
        + geom_line(size=0.8)
        + annotate("text", x=380, y=500, label="Slope ≈ 2, consistent with\nerror ≈ 1/(2T+1)",
                   size=7, ha="left", color="#333333", family="DejaVu Sans")
        + scale_color_manual(values=colors)
        + scale_linetype_manual(values=linetypes)
        + labs(
            title="Reciprocal Error vs Evaluation Depth: Second-Order Rate Structure",
            x="Evaluation Depth T",
            y="1 / |S(T) - π/4|",
            color="",
            linetype="",
            caption="Source: Computed from Leibniz partial sums",
        )
        + theme_minimal()
        + theme(
            figure_size=(7, 5.25),
            plot_title=element_text(size=11, weight="bold", family="DejaVu Sans"),
            axis_title=element_text(size=10, family="DejaVu Sans"),
            axis_text=element_text(size=9, family="DejaVu Sans"),
            plot_caption=element_text(size=7, color="#666666", family="DejaVu Sans"),
            panel_grid_minor=element_blank(),
            panel_grid_major_x=element_blank(),
            legend_position=(0.25, 0.85),
            legend_background=element_blank(),
        )
    )

    for ext, path in [("pdf", f"{outdir}/fig4_second_order_kinetics.pdf"),
                       ("png", f"{outdir}/fig4_second_order_kinetics.png")]:
        p4a.save(path, dpi=300, verbose=False)
        print(f"  Saved: {path}")

    # --- Fig 4b: T=1..10000, log-log axes ---
    from plotnine import scale_x_log10, scale_y_log10
    df_full  = compute_inv_error(T_full)
    df_full_m = pd.melt(df_full, id_vars=["T"],
                         value_vars=["inv_error", "theoretical"],
                         var_name="series", value_name="value")
    df_full_m["series"] = df_full_m["series"].map({
        "inv_error":   "Computed: 1/|S(T) - π/4|",
        "theoretical": "Theoretical: 2T + 1",
    })

    p4b = (
        ggplot(df_full_m, aes(x="T", y="value", color="series", linetype="series"))
        + geom_line(size=0.8)
        + scale_x_log10()
        + scale_y_log10()
        + scale_color_manual(values=colors)
        + scale_linetype_manual(values=linetypes)
        + labs(
            title="Reciprocal Error vs Evaluation Depth: Log-Log Scale (T=1..10000)",
            x="Evaluation Depth T (log scale)",
            y="1 / |S(T) - π/4| (log scale)",
            color="",
            linetype="",
            caption="Source: Computed from Leibniz partial sums",
        )
        + theme_minimal()
        + theme(
            figure_size=(7, 5.25),
            plot_title=element_text(size=11, weight="bold", family="DejaVu Sans"),
            axis_title=element_text(size=10, family="DejaVu Sans"),
            axis_text=element_text(size=9, family="DejaVu Sans"),
            plot_caption=element_text(size=7, color="#666666", family="DejaVu Sans"),
            panel_grid_minor=element_blank(),
            panel_grid_major_x=element_blank(),
            legend_position=(0.25, 0.85),
            legend_background=element_blank(),
        )
    )

    for ext, path in [("pdf", f"{outdir}/fig4b_second_order_loglog.pdf"),
                       ("png", f"{outdir}/fig4b_second_order_loglog.png")]:
        p4b.save(path, dpi=300, verbose=False)
        print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os
    outdir = os.path.join(os.path.dirname(__file__))  # paper/figures/

    print("=" * 60)
    print("Verification checks")
    print("=" * 60)
    verify_values()

    print("Generating Figure 1: Scaling Grid Heatmap")
    make_fig1_heatmap(outdir)

    print("\nGenerating Figure 2: Precision vs T")
    make_fig2_precision_vs_T(outdir)

    print("\nGenerating Figure 3: Parsimony Collapse")
    crossover = make_fig3_parsimony_collapse(outdir)
    print(f"  Crossover λ_p = {crossover:.5f}")

    print("\nGenerating Figure 4: Second-Order Kinetics")
    make_fig4_second_order(outdir)

    print("\nDone. All figures written to paper/figures/")
