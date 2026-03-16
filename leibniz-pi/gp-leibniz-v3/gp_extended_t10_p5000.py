#!/usr/bin/env python3
"""
GP Extended Time Test: t=10, pop=5000, convergence-aware fitness.
MAX_SEED=7200s (2h), MAX_TOTAL=36000s (10h).

Asks: with 4x the time budget, do additional seeds beyond seed 1 (val=7)
find Leibniz at the t=10/p=5000 condition?

Seeds loaded from: entropy-leibniz-v3/config/scaling_heatmap_config.json
Output: gp-leibniz-v3/results_gp_extended_t10_p5000/

Usage:
    python3 gp_extended_t10_p5000.py
"""

import json
import time
import math
import random
import sys
from pathlib import Path

import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────

_CFG_PATH = Path(__file__).parent.parent / "entropy-leibniz-v3" / "config" / "scaling_heatmap_config.json"
with open(_CFG_PATH) as _f:
    _cfg = json.load(_f)

SEED_VALS = _cfg["seeds"]   # [42, 7, 137, 2718, 31415]
N_SEEDS   = len(SEED_VALS)

# Fixed condition
TERMINALS_N = 10
POP_SIZE    = 5000

# Extended time budgets (not from config — this is the point of the test)
MAX_SEED  = 7200.0   # 2 hours per seed
MAX_TOTAL = 36000.0  # 10 hours total

# Output
OUT_DIR = Path(__file__).parent / "results_gp_extended_t10_p5000"

# GP hyperparameters (match gp_sensitivity_sweep.py baseline)
MAX_DEPTH    = 6
MAX_NODES    = 30
TOURNAMENT_K = 7
P_CROSS      = 0.70
P_MUT        = 0.20
N_ELITE      = 5
ALPHA        = 0.05
LAMBDA_P     = 0.005
PATIENCE     = 100
STOP_THRESH  = 0.001
DIV_INJECT   = 100
WORST        = -1e9
LOG_INTERVAL = 10

# Fitness evaluation
K_MAX     = 5000
K_ARRAY   = np.arange(K_MAX, dtype=float)
T_EVAL    = [10, 50, 200, 1000, 5000]
PI_OVER_4 = math.pi / 4

FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
FNAMES       = list(FUNC_ARITIES.keys())
EPHEMERALS   = []

# Runtime globals (set by setup_globals)
TERM_FIXED    = []
ALL_TERMINALS = []
_fitness_cache: dict = {}


# ── Terminal set ──────────────────────────────────────────────────────────────

def make_terminals(n):
    base = ["k", 1, -1, 2]
    if n <= 4:
        return base
    result = list(base)
    p = 3
    while len(result) < n:
        if len(result) < n:
            result.append(p)
        if len(result) < n:
            result.append(-(p - 1))
        p += 1
    return result[:n]


def setup_globals():
    global TERM_FIXED, ALL_TERMINALS, _fitness_cache
    TERM_FIXED    = make_terminals(TERMINALS_N)
    ALL_TERMINALS = TERM_FIXED + EPHEMERALS
    _fitness_cache = {}


# ── Node class ────────────────────────────────────────────────────────────────

class Node:
    __slots__ = ("op", "children", "value")

    def __init__(self, op=None, children=None, value=None):
        self.op       = op
        self.children = children if children is not None else []
        self.value    = value

    def is_terminal(self):
        return self.op is None

    def copy(self):
        if self.is_terminal():
            return Node(value=self.value)
        return Node(op=self.op, children=[c.copy() for c in self.children])

    def node_count(self):
        if self.is_terminal():
            return 1
        return 1 + sum(c.node_count() for c in self.children)

    def depth(self):
        if self.is_terminal():
            return 0
        return 1 + max(c.depth() for c in self.children)

    def to_str(self):
        if self.is_terminal():
            return "k" if self.value == "k" else str(self.value)
        a = self.children[0].to_str()
        if self.op == "neg":
            return f"(-{a})"
        b = self.children[1].to_str()
        sym = {"add": "+", "sub": "-", "mul": "*", "div": "/", "pow": "^"}[self.op]
        return f"({a} {sym} {b})"


# ── Tree evaluation ───────────────────────────────────────────────────────────

def evaluate_tree(node, k_arr):
    if node.is_terminal():
        return k_arr if node.value == "k" else float(node.value)
    a = evaluate_tree(node.children[0], k_arr)
    if node.op == "neg":
        return -a
    b = evaluate_tree(node.children[1], k_arr)
    with np.errstate(all="ignore"):
        if node.op == "add":
            return a + b
        elif node.op == "sub":
            return a - b
        elif node.op == "mul":
            return a * b
        elif node.op == "div":
            if np.isscalar(a) and np.isscalar(b):
                return a / b if abs(b) > 1e-10 else 1.0
            return np.where(np.abs(b) > 1e-10, a / b, 1.0)
        elif node.op == "pow":
            b_int = np.round(b).astype(float) if not np.isscalar(b) else float(round(b))
            result = np.power(a, b_int)
            if np.isscalar(result):
                return result if (math.isfinite(result) and abs(result) < 1e6) else 1.0
            return np.where(np.isfinite(result) & (np.abs(result) < 1e6), result, 1.0)
    return 1.0


def safe_eval(tree, k_arr=None):
    if k_arr is None:
        k_arr = K_ARRAY
    try:
        result = evaluate_tree(tree, k_arr)
        if np.isscalar(result) or (isinstance(result, np.ndarray) and result.ndim == 0):
            terms = np.full(len(k_arr), float(result))
        else:
            terms = np.asarray(result, dtype=float)
        if len(terms) != len(k_arr):
            return None
        if not np.all(np.isfinite(terms)):
            return None
        if np.any(np.abs(terms) > 1e6):
            return None
        return terms
    except Exception:
        return None


# ── Convergence-aware fitness ─────────────────────────────────────────────────

def compute_fitness(tree):
    key = tree.to_str()
    if key in _fitness_cache:
        return _fitness_cache[key]

    terms = safe_eval(tree)
    if terms is None:
        _fitness_cache[key] = WORST
        return WORST

    cum    = np.cumsum(terms)
    errors = [abs(float(cum[T - 1]) - PI_OVER_4) for T in T_EVAL]

    if any(e > 1e4 for e in errors):
        _fitness_cache[key] = WORST
        return WORST

    accuracy   = -float(np.mean(errors))
    n_improv   = sum(1 for i in range(len(errors) - 1) if errors[i+1] < errors[i] * 0.95)
    conv_bonus = n_improv / (len(errors) - 1)
    parsimony  = LAMBDA_P * tree.node_count()

    fitness = accuracy + ALPHA * conv_bonus - parsimony
    _fitness_cache[key] = fitness
    return fitness


def fitness_components(tree):
    terms = safe_eval(tree)
    if terms is None:
        return (WORST, 0.0, 0.0, WORST)
    cum    = np.cumsum(terms)
    errors = [abs(float(cum[T - 1]) - PI_OVER_4) for T in T_EVAL]
    acc    = -float(np.mean(errors))
    n_imp  = sum(1 for i in range(len(errors)-1) if errors[i+1] < errors[i] * 0.95)
    cb     = n_imp / (len(errors) - 1)
    ps     = LAMBDA_P * tree.node_count()
    return (round(acc, 8), round(cb, 4), round(ps, 4), round(acc + ALPHA*cb - ps, 8))


# ── Tree generation ───────────────────────────────────────────────────────────

def random_terminal():
    return Node(value=random.choice(ALL_TERMINALS))


def grow_tree(max_depth, depth=0):
    if depth >= max_depth:
        return random_terminal()
    if random.random() < 0.45:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[grow_tree(max_depth, depth+1)
                                  for _ in range(FUNC_ARITIES[op])])


def full_tree(target_depth, depth=0):
    if depth >= target_depth:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[full_tree(target_depth, depth+1)
                                  for _ in range(FUNC_ARITIES[op])])


def make_random_tree(max_depth=4):
    for _ in range(20):
        t = grow_tree(max_depth) if random.random() < 0.6 else full_tree(random.randint(1, max_depth))
        if 1 <= t.node_count() <= MAX_NODES:
            return t
    return Node(value="k")


def ramped_h_h(n, min_d=2, max_d=5):
    pop    = []
    depths = list(range(min_d, max_d + 1))
    per    = max(1, n // (len(depths) * 2))
    for d in depths:
        for _ in range(per):
            for _ in range(10):
                t = full_tree(d)
                if 1 <= t.node_count() <= MAX_NODES:
                    pop.append(t); break
        for _ in range(per):
            for _ in range(10):
                t = grow_tree(d)
                if 1 <= t.node_count() <= MAX_NODES:
                    pop.append(t); break
    while len(pop) < n:
        pop.append(make_random_tree(random.randint(min_d, max_d)))
    return pop[:n]


# ── GP operators ──────────────────────────────────────────────────────────────

def collect_nodes(node, path=()):
    result = [(node, path)]
    if not node.is_terminal():
        for i, child in enumerate(node.children):
            result.extend(collect_nodes(child, path + (i,)))
    return result


def get_at_path(root, path):
    node = root
    for idx in path:
        node = node.children[idx]
    return node


def replace_at_path(root, path, new_node):
    if not path:
        return new_node.copy()
    new_root = Node(op=root.op, value=root.value, children=[])
    for i, child in enumerate(root.children):
        if i == path[0]:
            new_root.children.append(replace_at_path(child, path[1:], new_node))
        else:
            new_root.children.append(child.copy())
    return new_root


def tournament_select(population, fitnesses):
    indices = random.sample(range(len(population)), TOURNAMENT_K)
    return population[max(indices, key=lambda i: fitnesses[i])]


def crossover(t1, t2):
    nodes1, nodes2 = collect_nodes(t1), collect_nodes(t2)
    for _ in range(10):
        _, p1 = random.choice(nodes1)
        _, p2 = random.choice(nodes2)
        c1 = replace_at_path(t1, p1, get_at_path(t2, p2))
        c2 = replace_at_path(t2, p2, get_at_path(t1, p1))
        if c1.node_count() <= MAX_NODES and c2.node_count() <= MAX_NODES:
            return c1, c2
    return t1.copy(), t2.copy()


def mutate(tree):
    nodes = collect_nodes(tree)
    for _ in range(10):
        _, path = random.choice(nodes)
        mutated = replace_at_path(tree, path, make_random_tree(max_depth=3))
        if mutated.node_count() <= MAX_NODES:
            return mutated
    return tree.copy()


# ── GP main loop (single seed) ────────────────────────────────────────────────

def run_seed(seed_idx, seed_val, max_time, global_t0):
    t0 = time.time()
    random.seed(seed_val)
    np.random.seed(seed_val)

    log = lambda s: print(s, flush=True)
    log(f"\n── Seed {seed_idx} (val={seed_val}, budget={max_time:.0f}s) ──")

    # Perf check
    sample = ramped_h_h(min(50, POP_SIZE))
    t_check = time.time()
    for ind in sample:
        compute_fitness(ind)
    t_per_ind = (time.time() - t_check) / len(sample)
    est_per_gen = t_per_ind * POP_SIZE * 1.5
    log(f"  Perf: {t_per_ind*1000:.2f}ms/ind, ~{est_per_gen*1000:.0f}ms/gen → "
        f"~{int(max_time / max(est_per_gen, 1e-6))} gens")

    population = ramped_h_h(POP_SIZE)
    fitnesses  = [compute_fitness(ind) for ind in population]

    best_fit       = max(fitnesses)
    best_ind       = population[fitnesses.index(best_fit)].copy()
    best_unchanged = 0
    history        = []
    gen            = 0
    stop_reason    = None

    while True:
        elapsed_seed  = time.time() - t0
        elapsed_total = time.time() - global_t0

        if elapsed_total >= MAX_TOTAL:
            stop_reason = "time_limit_total"
            log(f"  [STOP] Total time at gen {gen} ({elapsed_seed:.1f}s seed / {elapsed_total:.1f}s total)")
            break
        if elapsed_seed >= max_time:
            stop_reason = "time_limit_seed"
            log(f"  [STOP] Seed time at gen {gen} ({elapsed_seed:.1f}s seed / {elapsed_total:.1f}s total)")
            break

        gen += 1

        sorted_idx = sorted(range(POP_SIZE), key=lambda i: fitnesses[i], reverse=True)
        elite      = [population[i].copy() for i in sorted_idx[:N_ELITE]]

        new_pop = list(elite)
        while len(new_pop) < POP_SIZE:
            r = random.random()
            if r < P_CROSS and len(new_pop) + 1 < POP_SIZE:
                c1, c2 = crossover(tournament_select(population, fitnesses),
                                   tournament_select(population, fitnesses))
                new_pop.append(c1)
                if len(new_pop) < POP_SIZE:
                    new_pop.append(c2)
            elif r < P_CROSS + P_MUT:
                new_pop.append(mutate(tournament_select(population, fitnesses)))
            else:
                new_pop.append(tournament_select(population, fitnesses).copy())

        population = new_pop[:POP_SIZE]
        fitnesses  = [compute_fitness(ind) for ind in population]

        gen_best = max(fitnesses)
        if gen_best > best_fit:
            best_fit       = gen_best
            best_ind       = population[fitnesses.index(gen_best)].copy()
            best_unchanged = 0
        else:
            best_unchanged += 1

        top20 = sorted(fitnesses, reverse=True)[:20]
        if len(set(round(f, 6) for f in top20)) == 1:
            new_rand = ramped_h_h(DIV_INJECT)
            worst_idxs = sorted(range(POP_SIZE), key=lambda i: fitnesses[i])[:DIV_INJECT]
            for i, idx in enumerate(worst_idxs):
                population[idx] = new_rand[i]
                fitnesses[idx]  = compute_fitness(new_rand[i])
            log(f"  [DIVERSITY] Gen {gen}: injected {DIV_INJECT}")

        if gen % LOG_INTERVAL == 0:
            elapsed = time.time() - t0
            mean_f  = sum(fitnesses) / POP_SIZE
            acc, cb, ps, _ = fitness_components(best_ind)
            expr = best_ind.to_str()
            log(f"  Gen {gen:4d} | fit={best_fit:.6f} | mean={mean_f:.6f} | "
                f"acc={acc:.5f} cb={cb:.2f} ps={ps:.3f} | "
                f"nc={best_ind.node_count()} | {expr[:50]} | t={elapsed:.1f}s")
            history.append({
                "gen": gen, "best_fitness": round(best_fit, 8),
                "mean_fitness": round(mean_f, 8), "best_expr": expr,
                "node_count": best_ind.node_count(),
                "accuracy": acc, "conv_bonus": cb, "parsimony": ps,
            })

        if best_unchanged >= PATIENCE:
            terms = safe_eval(best_ind)
            if terms is not None:
                cum    = np.cumsum(terms)
                errors = [abs(float(cum[T-1]) - PI_OVER_4) for T in T_EVAL]
                if all(e < STOP_THRESH for e in errors):
                    stop_reason = "early_stop_converged"
                    log(f"  [EARLY STOP] Gen {gen}: stable + threshold met")
                    break
            best_unchanged = 0

    elapsed = time.time() - t0
    acc, cb, ps, _ = fitness_components(best_ind)
    log(f"  Done: gen={gen}, fit={best_fit:.8f}, nc={best_ind.node_count()}, "
        f"acc={acc:.5f} cb={cb:.2f} t={elapsed:.1f}s\n  expr={best_ind.to_str()[:80]}")
    log(f"  stop_reason={stop_reason}")

    return {
        "seed": seed_idx, "seed_val": seed_val,
        "generations": gen, "best_fitness": best_fit,
        "best_expr": best_ind.to_str(), "best_ind": best_ind,
        "history": history, "elapsed": round(elapsed, 2),
        "stop_reason": stop_reason,
    }


# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze_result(result):
    ind   = result["best_ind"]
    terms = safe_eval(ind, K_ARRAY)
    if terms is None:
        return {"errors": {}, "is_equivalent": False}

    cum    = np.cumsum(terms)
    errors = {T: round(abs(float(cum[T-1]) - PI_OVER_4), 10) for T in T_EVAL}

    k_ext     = np.arange(10000, dtype=float)
    terms_ext = safe_eval(ind, k_ext)
    errors[10000] = (round(abs(float(np.sum(terms_ext)) - PI_OVER_4), 10)
                     if terms_ext is not None else None)

    leibniz_terms = [(-1)**k / (2*k+1) for k in range(20)]
    agent_terms   = [float(terms[k]) for k in range(20)]
    is_equiv = all(abs(agent_terms[k] - leibniz_terms[k]) < 1e-6 for k in range(20))

    acc, cb, ps, _ = fitness_components(ind)
    error_list = [errors[T] for T in T_EVAL]
    is_mono    = all(error_list[i+1] < error_list[i] for i in range(len(error_list)-1))

    return {
        "errors": errors, "is_equivalent": is_equiv,
        "is_monotone": is_mono, "accuracy": acc, "conv_bonus": cb,
        "terms_20": [round(float(terms[k]), 8) for k in range(20)],
    }


# ── Output writers ────────────────────────────────────────────────────────────

def write_results(seed_results):
    n_found    = sum(1 for r in seed_results if r.get("analysis", {}).get("is_equivalent", False))
    successful = [r for r in seed_results if r.get("analysis", {}).get("is_equivalent", False)]
    failed     = [r for r in seed_results if not r.get("analysis", {}).get("is_equivalent", False)]
    mean_gens  = (sum(r["generations"] for r in successful) / len(successful)) if successful else None
    mean_elap  = (sum(r["elapsed"]     for r in successful) / len(successful)) if successful else None
    top_exprs  = [r["best_expr"] for r in sorted(failed, key=lambda r: r["best_fitness"], reverse=True)]

    W = 72
    lines = [
        "=" * W,
        f"GP EXTENDED TIME TEST: terminals={TERMINALS_N}, pop_size={POP_SIZE}",
        f"Fitness: convergence-aware  ALPHA={ALPHA}  LAMBDA_P={LAMBDA_P}",
        f"Terminal set: {TERM_FIXED}",
        f"MAX_SEED={MAX_SEED:.0f}s (2h), MAX_TOTAL={MAX_TOTAL:.0f}s (10h)",
        "=" * W,
        "",
        f"Discovery: {n_found}/{N_SEEDS} seeds found Leibniz",
        f"(Standard 1800s run: 1/5 — seed 1/val=7)",
    ]
    if mean_gens is not None:
        lines.append(f"Mean generations (successful): {mean_gens:.1f}")
        lines.append(f"Mean elapsed (successful): {mean_elap:.1f}s")
    if top_exprs:
        lines.append("\nTop expressions (failed seeds):")
        for expr in top_exprs[:5]:
            lines.append(f"  {expr}")
    lines.append("")

    for r in seed_results:
        ana   = r.get("analysis", {})
        is_eq = ana.get("is_equivalent", False)
        acc   = ana.get("accuracy", 0.0)
        cb    = ana.get("conv_bonus", 0.0)
        sr    = r.get("stop_reason", "unknown")
        lines.append(f"Seed {r['seed']} (val={r['seed_val']}): "
                     f"gens={r['generations']} elapsed={r['elapsed']:.1f}s "
                     f"found={is_eq} acc={acc:.5f} cb={cb:.2f} stop={sr}")
        lines.append(f"  expr={r['best_expr'][:80]}")
    lines.append("")

    txt_path = OUT_DIR / "gp_extended_t10_p5000.txt"
    txt_path.write_text("\n".join(lines))
    print(f"  Wrote {txt_path}", flush=True)

    data = {
        "experiment": "gp_extended_t10_p5000",
        "terminal_count": TERMINALS_N, "term_fixed": TERM_FIXED,
        "pop_size": POP_SIZE, "n_seeds": N_SEEDS,
        "n_found": n_found,
        "mean_gens_success": round(mean_gens, 2) if mean_gens is not None else None,
        "mean_elapsed_success": round(mean_elap, 2) if mean_elap is not None else None,
        "top_failed_exprs": top_exprs[:5],
        "seeds": [
            {
                "seed": r["seed"], "seed_val": r["seed_val"],
                "generations": r["generations"],
                "best_fitness": round(r["best_fitness"], 8),
                "best_expr": r["best_expr"],
                "elapsed": r["elapsed"],
                "stop_reason": r.get("stop_reason", "unknown"),
                "is_equivalent": r.get("analysis", {}).get("is_equivalent", False),
                "is_monotone": r.get("analysis", {}).get("is_monotone", False),
                "accuracy": r.get("analysis", {}).get("accuracy", 0.0),
                "conv_bonus": r.get("analysis", {}).get("conv_bonus", 0.0),
            }
            for r in seed_results
        ],
    }
    json_path = OUT_DIR / "gp_extended_t10_p5000_data.json"
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Wrote {json_path}", flush=True)

    return n_found


def write_config_record():
    lines = [
        "# GP Extended Time Test — Parameter Record",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Condition",
        f"  terminals: {TERMINALS_N}",
        f"  terminal set: {make_terminals(TERMINALS_N)}",
        f"  pop_size: {POP_SIZE}",
        "",
        "## Fitness Function",
        "  name: convergence-aware (slime mold)",
        f"  formula: fitness = accuracy + ALPHA * conv_bonus - LAMBDA_P * nodes",
        f"  ALPHA: {ALPHA}",
        f"  LAMBDA_P: {LAMBDA_P}",
        f"  T_EVAL: {T_EVAL}",
        f"  K_MAX: {K_MAX}",
        "",
        "## Time Budgets (extended — not from config)",
        f"  MAX_SEED: {MAX_SEED}s (2 hours per seed)",
        f"  MAX_TOTAL: {MAX_TOTAL}s (10 hours total)",
        f"  Standard budget was: 1800s/seed, 10800s/cell",
        "",
        "## Seeds",
        f"  values: {SEED_VALS}",
        f"  source: {_CFG_PATH}",
        "",
        "## GP Hyperparameters",
        f"  MAX_DEPTH: {MAX_DEPTH}",
        f"  MAX_NODES: {MAX_NODES}",
        f"  TOURNAMENT_K: {TOURNAMENT_K}",
        f"  P_CROSS: {P_CROSS}",
        f"  P_MUT: {P_MUT}",
        f"  N_ELITE: {N_ELITE}",
        f"  PATIENCE: {PATIENCE}",
        f"  STOP_THRESH: {STOP_THRESH}",
        f"  DIV_INJECT: {DIV_INJECT}",
        "",
        "## Motivation",
        "  At t=10/p=5000 with standard budget, seed 1 (val=7) found Leibniz (1/5).",
        "  This test asks: with 4x the time, do other seeds eventually find it?",
        "  Runs sequentially (no Pool) — single cell, single machine.",
    ]

    cfg_path = OUT_DIR / "gp_extended_config.txt"
    cfg_path.write_text("\n".join(lines))
    print(f"  Wrote {cfg_path}", flush=True)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    setup_globals()
    write_config_record()

    print(f"\n[GP EXTENDED] terminals={TERMINALS_N} pop={POP_SIZE} "
          f"MAX_SEED={MAX_SEED:.0f}s MAX_TOTAL={MAX_TOTAL:.0f}s", flush=True)
    print(f"  Terminal set: {TERM_FIXED}", flush=True)
    print(f"  Seeds (from config): {SEED_VALS}", flush=True)
    print(f"  Log: {OUT_DIR / 'gp_extended_t10_p5000.log'}", flush=True)

    log_path = OUT_DIR / "gp_extended_t10_p5000.log"

    with open(log_path, "w") as lf:
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = lf
        sys.stderr = lf

        try:
            global_t0    = time.time()
            seed_results = []

            for i, sv in enumerate(SEED_VALS):
                elapsed_total = time.time() - global_t0
                remaining     = MAX_TOTAL - elapsed_total
                seed_budget   = min(MAX_SEED, remaining / (N_SEEDS - i))
                if seed_budget < 5:
                    print(f"  Skipping seed {i} ({remaining:.1f}s remaining)", flush=True)
                    break
                result = run_seed(i, sv, seed_budget, global_t0)
                seed_results.append(result)

            if seed_results:
                for r in seed_results:
                    r["analysis"] = analyze_result(r)
        finally:
            sys.stdout = old_out
            sys.stderr = old_err

    if not seed_results:
        print("ERROR: no seeds completed", flush=True)
        return

    n_found = write_results(seed_results)

    print(f"\n[GP EXTENDED] Done: {n_found}/{N_SEEDS} seeds found Leibniz", flush=True)
    print(f"  (Standard 1800s run found 1/5)", flush=True)


if __name__ == "__main__":
    main()
