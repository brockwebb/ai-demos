#!/usr/bin/env python3
"""
Coprime-Pi: Monte Carlo π estimation via number theory
═══════════════════════════════════════════════════════

Identity:   Pr(gcd(m, n) = 1) = 6/π²
Estimator:  π̂ = √(6 / p̂)   where p̂ = empirical coprime fraction

Runs full TEVV analysis, saves convergence data, and generates a
publication-ready convergence plot.

Usage:
    python coprime_pi.py

Outputs (in script directory):
    tevv_results.txt           – full TEVV report
    convergence_data.csv       – K=1000 π estimates per (N, M) config
    coprime_pi_convergence.png – publication-ready convergence plot
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
from scipy import stats

# ── Constants ─────────────────────────────────────────────────────────────────
TRUE_PI = math.pi
P_HAT_THEORY = 6.0 / (math.pi**2)  # ≈ 0.607927…
SCRIPT_DIR = Path(__file__).parent


# ── Core algorithm ────────────────────────────────────────────────────────────
def estimate_pi_batch(N: int, M: int, K: int, seed: int | None = None) -> np.ndarray:
    """
    K independent Monte Carlo trials, each drawing N random pairs from {1…M}².
    Returns shape-(K,) array of π estimates.
    """
    rng = np.random.default_rng(seed)
    estimates = np.empty(K)
    for k in range(K):
        m_arr = rng.integers(1, M + 1, size=N)
        n_arr = rng.integers(1, M + 1, size=N)
        p_hat = float(np.mean(np.gcd(m_arr, n_arr) == 1))
        estimates[k] = math.sqrt(6.0 / p_hat) if p_hat > 0 else math.nan
    return estimates


def exact_coprime_fraction(M: int) -> float:
    """
    Exact Pr(gcd(m,n)=1) for m,n ∈ {1…M} via exhaustive enumeration.
    Feasible for M ≤ 1 000 (M² = 1 M pairs).
    """
    idx = np.arange(1, M + 1)
    mm, nn = np.meshgrid(idx, idx, indexing="ij")
    return float(np.mean(np.gcd(mm, nn) == 1))


# ── T — Testing ───────────────────────────────────────────────────────────────
def run_testing(log) -> None:
    log("=" * 72)
    log("T — TESTING")
    log("=" * 72)

    # gcd(1, k) == 1 for all k
    for k in [1, 2, 5, 100, 999_983]:
        assert math.gcd(1, k) == 1
    log("PASS  gcd(1, k) == 1  for k ∈ {1, 2, 5, 100, 999983}")

    # gcd(p, p) == p for prime p (not coprime with itself)
    for p in [2, 7, 13, 97]:
        assert math.gcd(p, p) == p
    log("PASS  gcd(p, p) == p  for primes {2, 7, 13, 97}")

    # Known coprime / non-coprime pairs
    assert math.gcd(8, 15) == 1
    assert math.gcd(12, 18) == 6
    assert math.gcd(35, 64) == 1
    assert math.gcd(6, 10) == 2
    log("PASS  Known pairs: gcd(8,15)=1  gcd(12,18)=6  gcd(35,64)=1  gcd(6,10)=2")

    # Edge case M=1: all pairs are (1,1), gcd=1, p̂=1.0, π̂=√6 (known systematic bias)
    est_m1 = estimate_pi_batch(10_000, 1, K=1, seed=0)[0]
    assert abs(est_m1 - math.sqrt(6)) < 1e-9
    log(f"PASS  M=1 edge: π̂ = √6 = {est_m1:.8f}  (systematic bias; floor of identically-1 GCDs)")

    # Edge case M=2: exact p̂ = 3/4, π̂ = √8 ≈ 2.8284
    #   Pairs: (1,1)→1, (1,2)→1, (2,1)→1, (2,2)→2  →  3 coprime of 4
    exact_p_m2 = exact_coprime_fraction(2)
    assert exact_p_m2 == 0.75, f"M=2 exact p̂ should be 0.75, got {exact_p_m2}"
    exact_pi_m2 = math.sqrt(6.0 / exact_p_m2)  # = √8
    mc_m2 = estimate_pi_batch(50_000, 2, K=40, seed=1)
    mc_mean_m2 = float(np.mean(mc_m2))
    assert abs(mc_mean_m2 - exact_pi_m2) < 0.01, (
        f"M=2 MC mean {mc_mean_m2:.4f} ≠ √8={exact_pi_m2:.4f}"
    )
    log(
        f"PASS  M=2 edge: exact p̂=3/4  π̂=√8={exact_pi_m2:.6f}  MC mean={mc_mean_m2:.6f}"
    )

    log("All T-checks passed.\n")


# ── E — Evaluation ────────────────────────────────────────────────────────────
def run_evaluation(log, K: int = 100) -> dict:
    log("=" * 72)
    log(f"E — EVALUATION  (K={K} independent runs per configuration)")
    log("=" * 72)

    N_values = [1_000, 10_000, 100_000, 1_000_000]
    M_fixed = 1_000_000

    log(f"\n── Multi-run distribution of π̂ (M={M_fixed:,}, K={K}) ──")
    header = (
        f"{'N':>12}  {'mean':>10}  {'std':>10}  {'|bias|':>10}  "
        f"{'95% CI':^24}  {'SW p-val':>10}  {'SW':>6}"
    )
    log(header)
    log("─" * len(header))

    eval_rows: list[dict] = []
    for N in N_values:
        t0 = time.time()
        ests = estimate_pi_batch(N, M_fixed, K, seed=N)
        elapsed = time.time() - t0

        mean_ = float(np.mean(ests))
        std_ = float(np.std(ests))
        bias_ = abs(mean_ - TRUE_PI)
        ci_lo, ci_hi = (float(v) for v in np.percentile(ests, [2.5, 97.5]))
        sw_stat, sw_p = stats.shapiro(ests)
        sw_label = "PASS" if sw_p > 0.05 else "FAIL"

        log(
            f"{N:>12,}  {mean_:>10.6f}  {std_:>10.6f}  {bias_:>10.6f}  "
            f"[{ci_lo:.5f}, {ci_hi:.5f}]  {sw_p:>10.4f}  {sw_label:>6}"
            f"    ({elapsed:.1f}s)"
        )
        eval_rows.append(
            dict(
                N=N,
                M=M_fixed,
                K=K,
                mean=mean_,
                std=std_,
                bias=bias_,
                ci_lo=ci_lo,
                ci_hi=ci_hi,
                sw_p=sw_p,
                estimates=ests,
            )
        )

    # Finite-M bias via exact enumeration
    log(
        f"\n── Finite-M bias: exact p̂ vs theory 6/π² = {P_HAT_THEORY:.8f} ──"
    )
    log(f"{'M':>8}  {'exact p̂':>14}  {'bias from 6/π²':>16}  {'exact π̂':>12}")
    log("─" * 56)

    M_exact = [2, 10, 100, 1_000]
    bias_rows: list[dict] = []
    for M in M_exact:
        ep = exact_coprime_fraction(M)
        epi = math.sqrt(6.0 / ep)
        bias = ep - P_HAT_THEORY
        log(f"{M:>8,}  {ep:>14.8f}  {bias:>+16.8f}  {epi:>12.8f}")
        bias_rows.append(dict(M=M, exact_p=ep, exact_pi=epi, bias=bias))

    log(f"\n  True π = {TRUE_PI:.10f}")
    log("E-evaluation complete.\n")
    return dict(eval_rows=eval_rows, bias_rows=bias_rows)


# ── V1 — Verification ─────────────────────────────────────────────────────────
def run_verification(log, eval_data: dict) -> None:
    log("=" * 72)
    log("V1 — VERIFICATION")
    log("=" * 72)

    # Delta method: std(π̂) ≈ |dπ/dp̂| × √(p(1-p)/N)
    # π = √(6/p̂)  →  dπ/dp̂ = -√6 / (2 p̂^{3/2})
    p = P_HAT_THEORY
    deriv_mag = math.sqrt(6.0) / (2.0 * p**1.5)

    log(f"\n── CLT convergence: empirical vs delta-method prediction ──")
    log(f"  std(π̂) ≈ {deriv_mag:.4f} × √(p(1-p)/N)   [p = 6/π²]")
    log(
        f"\n{'N':>12}  {'emp std':>10}  {'theory std':>12}  "
        f"{'ratio':>8}  {'within 15%':>12}"
    )
    log("─" * 60)

    stds, Ns = [], []
    for row in eval_data["eval_rows"]:
        N = row["N"]
        th_std = deriv_mag * math.sqrt(p * (1.0 - p) / N)
        ratio = row["std"] / th_std
        ok = "OK" if 0.85 < ratio < 1.15 else "WARN"
        log(
            f"{N:>12,}  {row['std']:>10.6f}  {th_std:>12.6f}  "
            f"{ratio:>8.4f}  {ok:>12}"
        )
        stds.append(row["std"])
        Ns.append(N)

    log(f"\n── Std scaling — should be O(1/√N) ──")
    for i in range(1, len(Ns)):
        nr = Ns[i] / Ns[i - 1]
        sr = stds[i] / stds[i - 1]
        expected = 1.0 / math.sqrt(nr)
        ok = "OK" if abs(sr - expected) / expected < 0.15 else "WARN"
        log(
            f"  N {Ns[i-1]:>8,} → {Ns[i]:>10,}  (×{nr:.0f})  "
            f"std ratio={sr:.4f}  expected={expected:.4f}  [{ok}]"
        )

    # Cross-seed consistency
    log(f"\n── Cross-seed consistency (N=100K, M=1M, 10 seeds) ──")
    seed_ests = [
        estimate_pi_batch(100_000, 1_000_000, K=1, seed=s)[0] for s in range(10)
    ]
    spread = max(seed_ests) - min(seed_ests)
    log(f"  Estimates: {[f'{e:.5f}' for e in seed_ests]}")
    log(f"  Range:     {min(seed_ests):.5f} – {max(seed_ests):.5f}  (spread={spread:.5f})")
    ok = "OK" if spread < 4 * stds[2] else "WARN"
    log(f"  Cross-seed spread [{ok}]")

    log("V1-verification complete.\n")


# ── V2 — Validation ───────────────────────────────────────────────────────────
def run_validation(log, K: int = 100) -> np.ndarray:
    log("=" * 72)
    log("V2 — VALIDATION")
    log("=" * 72)

    N_large, M_large = 1_000_000, 1_000_000
    log(f"\n── High-N accuracy (N={N_large:,}, M={M_large:,}, K={K}) ──")

    ests = estimate_pi_batch(N_large, M_large, K, seed=42)
    mean_est = float(np.mean(ests))
    std_est = float(np.std(ests))
    bias = abs(mean_est - TRUE_PI)
    _, sw_p = stats.shapiro(ests)

    bias_ok = bias < 0.001
    sw_ok = sw_p > 0.05

    log(f"  Mean π̂       : {mean_est:.8f}  (true π = {TRUE_PI:.8f})")
    log(f"  |bias|        : {bias:.8f}  [{'PASS' if bias_ok else 'FAIL'}]  (threshold 0.001)")
    log(f"  Std dev       : {std_est:.8f}")
    log(
        f"  Shapiro-Wilk  : p={sw_p:.4f}  [{'PASS' if sw_ok else 'FAIL'}]"
        f"  (H₀: estimates are normally distributed)"
    )

    # Theoretical SE from delta method
    p = P_HAT_THEORY
    deriv_mag = math.sqrt(6.0) / (2.0 * p**1.5)
    theory_std = deriv_mag * math.sqrt(p * (1.0 - p) / N_large)
    ratio = std_est / theory_std
    log(f"\n  Delta-method SE: {theory_std:.8f}")
    log(
        f"  Empirical / theory: {ratio:.4f}  "
        f"[{'OK' if 0.85 < ratio < 1.15 else 'WARN'}]"
    )

    # Efficiency vs geometric Monte Carlo
    log("\n── Efficiency: Coprime MC vs Geometric MC ──")
    p_geo = math.pi / 4.0  # π/4 ≈ 0.785
    p_cop = P_HAT_THEORY  # 6/π² ≈ 0.608

    # π_geo = 4p̂  →  Var(π_geo) × N = 16 × p_geo(1-p_geo)
    var_geo = 16.0 * p_geo * (1.0 - p_geo)

    # π_cop = √(6/p̂)  →  Var(π_cop) × N = (√6 / 2p^{3/2})² × p(1-p)
    d_cop = math.sqrt(6.0) / (2.0 * p_cop**1.5)
    var_cop = d_cop**2 * p_cop * (1.0 - p_cop)

    rel_eff = var_cop / var_geo

    log(f"  Geometric MC  asymptotic Var(π̂)×N = {var_geo:.4f}  (p̂ ≈ π/4 ≈ {p_geo:.4f})")
    log(f"  Coprime MC    asymptotic Var(π̂)×N = {var_cop:.4f}  (p̂ ≈ 6/π² ≈ {p_cop:.4f})")
    log(f"  Efficiency ratio (cop / geo)       = {rel_eff:.4f}")
    if rel_eff < 1.0:
        log(
            f"  → Coprime MC is {1/rel_eff:.2f}× MORE efficient per sample than geometric MC"
        )
        log(
            f"  → Counter-intuitive: despite lower p̂, the gentler dπ/dp̂ sensitivity wins"
        )
    else:
        log(
            f"  → Coprime MC needs {rel_eff:.2f}× more samples for the same precision"
        )
    log(f"  → Both are O(1/√N)")

    log("\nAll V2-validation checks complete.\n")
    return ests


# ── Convergence plot ──────────────────────────────────────────────────────────
# Palette: works in both colour and greyscale
_PALETTE = ["#4a90d9", "#5bbf8a", "#e8a838", "#c9514a"]


def make_convergence_plot(eval_data: dict, output_path: Path) -> None:
    """Publication-ready 2-panel convergence figure."""
    rows = eval_data["eval_rows"]
    N_vals = [r["N"] for r in rows]
    means = [r["mean"] for r in rows]
    all_ests = [r["estimates"] for r in rows]
    ci_lo = np.array([r["ci_lo"] for r in rows])
    ci_hi = np.array([r["ci_hi"] for r in rows])

    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor("#f8f9fa")

    gs = gridspec.GridSpec(
        2,
        4,
        figure=fig,
        height_ratios=[1.7, 1.0],
        hspace=0.50,
        wspace=0.38,
        left=0.07,
        right=0.97,
        top=0.91,
        bottom=0.07,
    )

    # ── Top panel: violin plot + mean line + 95% CI ───────────────────────────
    ax = fig.add_subplot(gs[0, :])
    ax.set_facecolor("white")
    ax.grid(axis="y", linewidth=0.5, alpha=0.4, zorder=0)
    ax.set_axisbelow(True)

    # Use log10(N) as x-position so violins are evenly spaced
    log10_N = [math.log10(n) for n in N_vals]

    # 95% CI shading
    ax.fill_between(
        log10_N,
        ci_lo,
        ci_hi,
        alpha=0.12,
        color="#4a90d9",
        label="95% empirical CI",
        zorder=1,
    )

    # Violins
    for ests, pos, col in zip(all_ests, log10_N, _PALETTE):
        parts = ax.violinplot(
            ests,
            positions=[pos],
            widths=[0.28],
            showmedians=True,
            showextrema=False,
        )
        for pc in parts["bodies"]:
            pc.set_facecolor(col)
            pc.set_edgecolor("none")
            pc.set_alpha(0.55)
        parts["cmedians"].set_color(col)
        parts["cmedians"].set_linewidth(1.8)

    # Mean line
    ax.plot(
        log10_N,
        means,
        "o--",
        color="#1a1a2a",
        linewidth=1.6,
        markersize=7,
        zorder=5,
        label="Mean π̂",
    )

    # True π reference
    ax.axhline(
        TRUE_PI,
        color="#c0392b",
        linewidth=1.5,
        linestyle="--",
        zorder=4,
        label=f"True π = {TRUE_PI:.6f}…",
    )

    # Formula annotation
    ax.annotate(
        r"$\hat{\pi} = \sqrt{6\,/\,\hat{p}}$"
        "\n"
        r"$\hat{p}$ = fraction of coprime pairs",
        xy=(0.97, 0.95),
        xycoords="axes fraction",
        fontsize=11,
        ha="right",
        va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cccccc"),
    )

    ax.set_xticks(log10_N)
    ax.set_xticklabels([f"{n:,}" for n in N_vals], fontsize=10)
    ax.set_xlabel("Pairs sampled per run  (N)", fontsize=11, labelpad=6)
    ax.set_ylabel("π estimate", fontsize=11)
    K_used = rows[0]["K"]
    ax.set_title(
        f"Convergence of Coprime Monte Carlo π Estimator  —  K = {K_used:,} independent runs per N",
        fontsize=12,
        pad=10,
    )
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.4f}"))
    ax.tick_params(axis="both", labelsize=9)
    ax.legend(fontsize=9, framealpha=0.9, loc="upper left")

    # ── Bottom panels: histogram small multiples ──────────────────────────────
    labels = ["N = 1,000", "N = 10,000", "N = 100,000", "N = 1,000,000"]
    for col_idx, (ests, label, col) in enumerate(zip(all_ests, labels, _PALETTE)):
        ax_h = fig.add_subplot(gs[1, col_idx])
        ax_h.set_facecolor("white")
        ax_h.grid(axis="y", linewidth=0.4, alpha=0.4)
        ax_h.set_axisbelow(True)

        ax_h.hist(
            ests,
            bins=18,
            color=col,
            alpha=0.72,
            edgecolor="white",
            linewidth=0.5,
        )
        ax_h.axvline(
            TRUE_PI,
            color="#c0392b",
            linewidth=1.4,
            linestyle="--",
            zorder=5,
        )
        ax_h.axvline(
            float(np.mean(ests)),
            color="#1a1a2a",
            linewidth=1.1,
            linestyle="-",
            alpha=0.6,
            zorder=4,
        )
        ax_h.set_title(label, fontsize=9, pad=4)
        ax_h.set_xlabel("π̂", fontsize=8)
        if col_idx == 0:
            ax_h.set_ylabel("Count", fontsize=8)
        ax_h.tick_params(labelsize=7)

    plt.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved plot → {output_path}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    lines: list[str] = []

    def log(s: str = "") -> None:
        print(s)
        lines.append(s)

    wall_start = time.time()

    log("Coprime-Pi: Monte Carlo π Estimation — TEVV Report")
    log("=" * 72)
    log(f"  True π            = {TRUE_PI:.12f}")
    log(f"  Theoretical p̂     = 6/π² = {P_HAT_THEORY:.12f}")
    log(f"  Generated         : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log()

    run_testing(log)
    eval_data = run_evaluation(log, K=1000)
    run_verification(log, eval_data)
    run_validation(log, K=1000)

    elapsed = time.time() - wall_start
    log(f"Total wall time: {elapsed:.1f}s")

    # Save TEVV report
    tevv_path = SCRIPT_DIR / "tevv_results.txt"
    tevv_path.write_text("\n".join(lines) + "\n")
    print(f"\nSaved → {tevv_path}")

    # Save convergence CSV
    csv_rows = [
        {"N": row["N"], "M": row["M"], "run": i, "pi_estimate": float(est)}
        for row in eval_data["eval_rows"]
        for i, est in enumerate(row["estimates"])
    ]
    csv_path = SCRIPT_DIR / "convergence_data.csv"
    pd.DataFrame(csv_rows).to_csv(csv_path, index=False)
    print(f"Saved → {csv_path}")

    # Generate convergence plot
    plot_path = SCRIPT_DIR / "coprime_pi_convergence.png"
    make_convergence_plot(eval_data, plot_path)


if __name__ == "__main__":
    main()
