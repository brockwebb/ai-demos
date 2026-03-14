#!/usr/bin/env python3
"""
ACO-Leibniz: Ant Colony Optimization discovers the Leibniz series for pi/4.

Approach:
  - 300 ants build series term-by-term using pheromone-weighted sampling
  - Separate pheromone tables for sign (+/-) and denominator at each position
  - Multi-length fitness kills degenerate short-horizon solutions
  - Curriculum expands evaluation length over generations
  - 5-minute wall-clock hard limit; checkpoint every 100 gens
  - Early stopping when pheromone top-choices stabilize

Target: pi/4 = 1 - 1/3 + 1/5 - 1/7 + ...  (Leibniz series)
"""

import json
import csv
import time
import math
import random
import sys
from pathlib import Path

# ── Output directory ──────────────────────────────────────────────────────────
OUT_DIR = Path(__file__).parent

# ── Constants ─────────────────────────────────────────────────────────────────
PI_OVER_4 = math.pi / 4

T_MAX = 50           # Max series length (positions 0..49)
D_MAX = 50           # Denominator choices: index d → denom 2d+1 (1,3,5,...,99)
N_ANTS = 300
N_ELITE = max(1, int(N_ANTS * 0.10))   # top 10% deposit pheromone
RHO = 0.15           # Evaporation rate
TAU_MIN = 0.01       # Pheromone floor
MAX_TIME = 290.0     # Hard wall-clock limit (seconds)
EARLY_STOP_PATIENCE = 200   # Stop if top choices stable for this many gens
CHECKPOINT_INTERVAL = 100   # Write progress.json every N gens
SNAPSHOT_INTERVAL = 100     # Pheromone snapshot for viz every N gens


# ── Utility functions ─────────────────────────────────────────────────────────

def idx_to_denom(d: int) -> int:
    return 2 * d + 1


def denom_to_idx(denom: int) -> int:
    return (denom - 1) // 2


def partial_sum(signs: list, dens: list, T: int) -> float:
    return sum(signs[k] / dens[k] for k in range(min(T, len(signs))))


def leibniz_partial(T: int) -> float:
    return sum((-1) ** k / (2 * k + 1) for k in range(T))


# Precomputed reference values
LEIBNIZ_REFS = {T: leibniz_partial(T) for T in [5, 10, 20, 30, 40, 50]}


def get_t_eval(gen: int) -> list:
    """Curriculum: expand evaluation horizon over generations."""
    if gen <= 500:
        return [5, 10]
    elif gen <= 1500:
        return [10, 20, 30]
    else:
        return [10, 20, 30, 40]


def multi_fitness(signs: list, dens: list, t_eval: list) -> float:
    """
    Multi-length fitness: mean negative absolute error across T_eval lengths.
    Negative so higher is better.
    """
    errors = [abs(partial_sum(signs, dens, T) - PI_OVER_4) for T in t_eval]
    return -sum(errors) / len(errors)


def detect_leibniz(signs: list, dens: list, T: int) -> dict:
    """Structural pattern detection — no hardcoded Leibniz series."""
    signs_alt = all(signs[k] == (1 if k % 2 == 0 else -1) for k in range(T))
    dens_odd = all(dens[k] % 2 == 1 for k in range(T))
    dens_inc = all(dens[k] < dens[k + 1] for k in range(T - 1))
    dens_consec = all(dens[k] == 2 * k + 1 for k in range(T))
    return {
        "signs_alternate": signs_alt,
        "denoms_odd": dens_odd,
        "denoms_increasing": dens_inc,
        "denoms_consecutive": dens_consec,
        "is_leibniz": signs_alt and dens_consec,
    }


# ── Ant Colony ────────────────────────────────────────────────────────────────

class AntColony:
    def __init__(self):
        # tau_sign[k] = [pheromone_for_+1, pheromone_for_-1]
        self.tau_sign = [[1.0, 1.0] for _ in range(T_MAX)]
        # tau_denom[k][d] = pheromone for denominator 2d+1 at position k
        self.tau_denom = [[1.0] * D_MAX for _ in range(T_MAX)]

    def build_solution(self) -> tuple:
        """Build one ant's solution by probabilistic sampling."""
        signs, dens = [], []
        for k in range(T_MAX):
            si = random.choices([0, 1], weights=self.tau_sign[k], k=1)[0]
            signs.append(1 if si == 0 else -1)
            di = random.choices(range(D_MAX), weights=self.tau_denom[k], k=1)[0]
            dens.append(idx_to_denom(di))
        return signs, dens

    def greedy_solution(self) -> tuple:
        """Return series using max-pheromone choice at each position."""
        signs, dens = [], []
        for k in range(T_MAX):
            si = 0 if self.tau_sign[k][0] >= self.tau_sign[k][1] else 1
            signs.append(1 if si == 0 else -1)
            di = max(range(D_MAX), key=lambda d: self.tau_denom[k][d])
            dens.append(idx_to_denom(di))
        return signs, dens

    def top_choices(self) -> list:
        """Fingerprint of current max-pheromone choices, for early stopping."""
        return [
            (
                0 if self.tau_sign[k][0] >= self.tau_sign[k][1] else 1,
                max(range(D_MAX), key=lambda d: self.tau_denom[k][d]),
            )
            for k in range(T_MAX)
        ]

    def evaporate(self):
        """Apply pheromone evaporation with floor."""
        decay = 1.0 - RHO
        for k in range(T_MAX):
            self.tau_sign[k] = [max(TAU_MIN, v * decay) for v in self.tau_sign[k]]
            self.tau_denom[k] = [max(TAU_MIN, v * decay) for v in self.tau_denom[k]]

    def deposit(self, elite_solutions: list):
        """
        Elite ants deposit pheromone with linear rank weighting.
        elite_solutions: list of (signs, dens), sorted best-first.
        """
        n = len(elite_solutions)
        for rank, (signs, dens) in enumerate(elite_solutions):
            weight = (n - rank) / n   # 1.0 for rank 0 down to 1/n for last
            for k in range(T_MAX):
                si = 0 if signs[k] == 1 else 1
                self.tau_sign[k][si] += weight
                di = denom_to_idx(dens[k])
                if 0 <= di < D_MAX:
                    self.tau_denom[k][di] += weight

    def certainties(self) -> list:
        """Per-position pheromone certainty: mean of sign and denom certainty."""
        result = []
        for k in range(T_MAX):
            s = self.tau_sign[k]
            s_cert = max(s) / sum(s)
            d = self.tau_denom[k]
            d_cert = max(d) / sum(d)
            result.append((s_cert + d_cert) / 2.0)
        return result

    def snapshot(self) -> dict:
        """Normalized pheromone state for visualization."""
        denom_snap = []
        for k in range(T_MAX):
            total = sum(self.tau_denom[k])
            denom_snap.append([round(v / total, 5) for v in self.tau_denom[k]])
        sign_snap = []
        for k in range(T_MAX):
            total = sum(self.tau_sign[k])
            sign_snap.append([round(v / total, 5) for v in self.tau_sign[k]])
        return {"denom": denom_snap, "sign": sign_snap}


# ── Main ACO loop ─────────────────────────────────────────────────────────────

def run_aco() -> dict:
    t0 = time.time()
    random.seed(42)

    colony = AntColony()

    best_fitness = -1e9
    best_signs = None
    best_dens = None

    convergence = []
    snapshots = []

    top_prev = None
    stable_gens = 0

    # Generation 0 snapshot (uniform pheromone baseline)
    gs0, gd0 = colony.greedy_solution()
    snapshots.append({
        "gen": 0,
        "elapsed": 0.0,
        "snapshot": colony.snapshot(),
        "greedy_signs": gs0[:20],
        "greedy_dens": gd0[:20],
    })

    gen = 0

    while True:
        elapsed = time.time() - t0
        if elapsed >= MAX_TIME:
            print(f"[STOP] Wall-clock limit at gen {gen}, t={elapsed:.1f}s", flush=True)
            break

        gen += 1
        t_eval = get_t_eval(gen)

        # Build and evaluate all ants
        population = [colony.build_solution() for _ in range(N_ANTS)]
        fitnesses = [multi_fitness(s, d, t_eval) for s, d in population]

        # Update pheromone
        colony.evaporate()
        ranked_sols = [sol for _, sol in sorted(zip(fitnesses, population), key=lambda x: -x[0])]
        colony.deposit(ranked_sols[:N_ELITE])

        # Track global best
        gen_best_idx = max(range(N_ANTS), key=lambda i: fitnesses[i])
        gf = fitnesses[gen_best_idx]
        if gf > best_fitness:
            best_fitness = gf
            best_signs = population[gen_best_idx][0][:]
            best_dens = population[gen_best_idx][1][:]

        # Early stopping check
        tc = colony.top_choices()
        if tc == top_prev:
            stable_gens += 1
        else:
            stable_gens = 0
        top_prev = tc

        if stable_gens >= EARLY_STOP_PATIENCE:
            print(f"[STOP] Early stop at gen {gen} (stable {stable_gens} gens)", flush=True)
            break

        # Statistics
        elapsed = time.time() - t0
        mean_f = sum(fitnesses) / N_ANTS
        gs, gd = colony.greedy_solution()
        gf_greedy = multi_fitness(gs, gd, [10, 20, 30, 40])
        certs = colony.certainties()
        mean_cert = sum(certs) / T_MAX

        convergence.append({
            "generation": gen,
            "best_gen": round(max(fitnesses), 8),
            "best_ever": round(best_fitness, 8),
            "mean_fitness": round(mean_f, 8),
            "greedy_fitness": round(gf_greedy, 8),
            "mean_certainty": round(mean_cert, 5),
            "t_eval_max": max(t_eval),
            "elapsed": round(elapsed, 2),
        })

        # Pheromone snapshot
        if gen % SNAPSHOT_INTERVAL == 0:
            snapshots.append({
                "gen": gen,
                "elapsed": round(elapsed, 2),
                "snapshot": colony.snapshot(),
                "greedy_signs": gs[:20],
                "greedy_dens": gd[:20],
            })
            print(
                f"  Gen {gen:5d} | best_ever={best_fitness:.6f} | greedy={gf_greedy:.6f} | "
                f"cert={mean_cert:.3f} | T_max={max(t_eval)} | t={elapsed:.1f}s",
                flush=True,
            )

        # Checkpoint
        if gen % CHECKPOINT_INTERVAL == 0:
            with open(OUT_DIR / "progress.json", "w") as f:
                json.dump(
                    {
                        "generation": gen,
                        "best_fitness": best_fitness,
                        "elapsed": round(elapsed, 2),
                        "greedy_series": [
                            f"{'+'if s>0 else ''}{s}/{d}" for s, d in zip(gs[:10], gd[:10])
                        ],
                    },
                    f,
                )

    final_gs, final_gd = colony.greedy_solution()
    return {
        "colony": colony,
        "convergence": convergence,
        "snapshots": snapshots,
        "best_signs": best_signs,
        "best_dens": best_dens,
        "greedy_signs": final_gs,
        "greedy_dens": final_gd,
        "best_fitness": best_fitness,
        "generations": gen,
        "elapsed": time.time() - t0,
    }


# ── TEVV ──────────────────────────────────────────────────────────────────────

def run_tevv(results: dict) -> str:
    colony = results["colony"]
    greedy_s = results["greedy_signs"]
    greedy_d = results["greedy_dens"]
    best_s = results["best_signs"]
    best_d = results["best_dens"]

    W = 72
    lines = []
    lines.append("=" * W)
    lines.append("ACO-LEIBNIZ: TEVV REPORT")
    lines.append("Ant Colony Optimization discovers the Leibniz series for pi/4")
    lines.append("=" * W)

    lines.append(f"\nConfiguration:")
    lines.append(f"  n_ants={N_ANTS}, T_max={T_MAX}, D_max={D_MAX}")
    lines.append(f"  rho (evaporation)={RHO}, tau_min={TAU_MIN}, n_elite={N_ELITE}")
    lines.append(
        f"  Curriculum: gen<=500 T=[5,10]; gen<=1500 T=[10,20,30]; gen>1500 T=[10,20,30,40]"
    )
    lines.append(f"  Early-stop patience: {EARLY_STOP_PATIENCE} gens")

    lines.append(f"\nRun Summary:")
    lines.append(f"  Generations completed : {results['generations']}")
    lines.append(f"  Wall-clock time       : {results['elapsed']:.1f}s")
    lines.append(f"  Best fitness (any ant): {results['best_fitness']:.8f}")

    for label, signs, dens in [
        ("GREEDY (max pheromone at each position)", greedy_s, greedy_d),
        ("BEST ANT EVER SEEN (fitness champion)", best_s, best_d),
    ]:
        lines.append(f"\n{'─'*W}")
        lines.append(label)
        lines.append(f"{'─'*W}")
        ser_str = "  " + "  ".join(
            f"{'+'if s>0 else ''}{s}/{d}" for s, d in zip(signs[:10], dens[:10])
        )
        lines.append(f"Series (T=10):\n{ser_str}")

        lines.append(f"\nAccuracy vs Leibniz:")
        lines.append(
            f"  {'T':>4}  {'partial_sum':>14}  {'error':>12}  {'leibniz_err':>12}  {'verdict':>8}"
        )
        lines.append(f"  {'-'*4}  {'-'*14}  {'-'*12}  {'-'*12}  {'-'*8}")
        for T in [10, 20, 30, 40, 50]:
            ps = partial_sum(signs, dens, T)
            err = abs(ps - PI_OVER_4)
            leib_ref = LEIBNIZ_REFS.get(T, leibniz_partial(T))
            leib_err = abs(leib_ref - PI_OVER_4)
            if err < leib_err - 1e-10:
                verdict = "BETTER"
            elif err > leib_err + 1e-10:
                verdict = "WORSE"
            else:
                verdict = "EQUAL"
            lines.append(
                f"  {T:>4}  {ps:>14.8f}  {err:>12.8f}  {leib_err:>12.8f}  {verdict:>8}"
            )

        det = detect_leibniz(signs, dens, 10)
        lines.append(f"\nStructural Pattern (T=10):")
        lines.append(f"  Signs alternate        : {det['signs_alternate']}")
        lines.append(f"  Denominators odd       : {det['denoms_odd']}")
        lines.append(f"  Denominators increasing: {det['denoms_increasing']}")
        lines.append(f"  Denominators consec 1,3,5,...: {det['denoms_consecutive']}")
        lines.append(f"  IS LEIBNIZ SERIES      : {det['is_leibniz']}")

    lines.append(f"\n{'─'*W}")
    lines.append("PHEROMONE CERTAINTY (first 20 positions)")
    lines.append(f"{'─'*W}")
    lines.append(
        f"  {'k':>3}  {'pref_sign':>10}  {'s_cert':>7}  {'pref_denom':>10}  {'d_cert':>7}  "
        f"{'leibniz':>9}  {'match':>6}"
    )
    lines.append(f"  {'─'*3}  {'─'*10}  {'─'*7}  {'─'*10}  {'─'*7}  {'─'*9}  {'─'*6}")
    for k in range(20):
        sp = colony.tau_sign[k]
        s_cert = max(sp) / sum(sp)
        pref_s = "+1" if sp[0] >= sp[1] else "-1"
        dp = colony.tau_denom[k]
        di = max(range(D_MAX), key=lambda d: dp[d])
        d_cert = max(dp) / sum(dp)
        pref_d = idx_to_denom(di)
        lei_s = "+1" if k % 2 == 0 else "-1"
        lei_d = 2 * k + 1
        match = "OK" if pref_s == lei_s and pref_d == lei_d else "MISS"
        lines.append(
            f"  {k:>3}  {pref_s:>10}  {s_cert:>7.4f}  {pref_d:>10}  {d_cert:>7.4f}  "
            f"{lei_s}/{lei_d:>4}  {match:>6}"
        )

    lines.append(f"\n{'='*W}")
    lines.append("VERDICT")
    lines.append(f"{'='*W}")
    gdet = detect_leibniz(greedy_s, greedy_d, 10)
    bdet = detect_leibniz(best_s, best_d, 10)
    lines.append(f"  Greedy solution  IS Leibniz: {gdet['is_leibniz']}")
    lines.append(f"  Best ant         IS Leibniz: {bdet['is_leibniz']}")
    either = gdet["is_leibniz"] or bdet["is_leibniz"]
    lines.append(f"  Either solution IS Leibniz: {either}")
    g_err10 = abs(partial_sum(greedy_s, greedy_d, 10) - PI_OVER_4)
    lei_err10 = abs(LEIBNIZ_REFS[10] - PI_OVER_4)
    lines.append(f"\n  Greedy T=10 error : {g_err10:.8f}")
    lines.append(f"  Leibniz T=10 error: {lei_err10:.8f}")
    lines.append(f"  Ratio (greedy/leibniz): {g_err10/lei_err10:.4f}")

    return "\n".join(lines)


# ── Output writers ────────────────────────────────────────────────────────────

def write_convergence_csv(convergence: list):
    path = OUT_DIR / "convergence.csv"
    if not convergence:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=convergence[0].keys())
        writer.writeheader()
        writer.writerows(convergence)
    print(f"  Wrote {path}", flush=True)


def write_pheromone_data(results: dict):
    greedy_s = results["greedy_signs"]
    greedy_d = results["greedy_dens"]
    best_s = results["best_signs"]
    best_d = results["best_dens"]

    def series_detail(signs, dens, T_vals):
        out = {}
        for T in T_vals:
            ps = partial_sum(signs, dens, T)
            out[str(T)] = {
                "partial_sum": round(ps, 10),
                "error": round(abs(ps - PI_OVER_4), 10),
                "leibniz_partial": round(LEIBNIZ_REFS.get(T, leibniz_partial(T)), 10),
                "leibniz_error": round(
                    abs(LEIBNIZ_REFS.get(T, leibniz_partial(T)) - PI_OVER_4), 10
                ),
            }
        return out

    data = {
        "config": {
            "n_ants": N_ANTS,
            "t_max": T_MAX,
            "d_max": D_MAX,
            "rho": RHO,
            "tau_min": TAU_MIN,
            "n_elite": N_ELITE,
            "early_stop_patience": EARLY_STOP_PATIENCE,
        },
        "pi_over_4": PI_OVER_4,
        "leibniz_refs": {str(k): round(v, 10) for k, v in LEIBNIZ_REFS.items()},
        "run": {
            "generations": results["generations"],
            "elapsed": round(results["elapsed"], 2),
            "best_fitness": round(results["best_fitness"], 8),
        },
        "greedy_series": {
            "signs": greedy_s,
            "dens": greedy_d,
            "partial_sums": series_detail(greedy_s, greedy_d, [10, 20, 30, 40, 50]),
            "pattern": detect_leibniz(greedy_s, greedy_d, min(10, T_MAX)),
        },
        "best_series": {
            "signs": best_s,
            "dens": best_d,
            "partial_sums": series_detail(best_s, best_d, [10, 20, 30, 40, 50]),
            "pattern": detect_leibniz(best_s, best_d, min(10, T_MAX)),
        },
        "convergence": results["convergence"],
        "snapshots": results["snapshots"],
    }

    path = OUT_DIR / "pheromone_data.json"
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    size_kb = path.stat().st_size / 1024
    print(f"  Wrote {path} ({size_kb:.1f} KB)", flush=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    print("=" * 72, flush=True)
    print("ACO-Leibniz: Ant Colony Optimization discovers pi/4", flush=True)
    print(f"Target: pi/4 = {PI_OVER_4:.10f}", flush=True)
    print(f"Config: {N_ANTS} ants, T_max={T_MAX}, D_max={D_MAX}, rho={RHO}", flush=True)
    print("=" * 72, flush=True)

    print("\n[1/4] Running ACO ...", flush=True)
    results = run_aco()
    print(
        f"\n  Done: {results['generations']} gens in {results['elapsed']:.1f}s, "
        f"best_fitness={results['best_fitness']:.6f}",
        flush=True,
    )

    print("\n[2/4] Running TEVV ...", flush=True)
    tevv_report = run_tevv(results)
    print(tevv_report, flush=True)

    print("\n[3/4] Writing output files ...", flush=True)
    write_convergence_csv(results["convergence"])
    write_pheromone_data(results)

    tevv_path = OUT_DIR / "results.txt"
    with open(tevv_path, "w") as f:
        f.write(tevv_report)
    print(f"  Wrote {tevv_path}", flush=True)

    # Clean up checkpoint
    progress_path = OUT_DIR / "progress.json"
    if progress_path.exists():
        progress_path.unlink()

    print("\n[4/4] All files written.", flush=True)
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
