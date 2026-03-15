#!/usr/bin/env python3
"""
Scaling Heat Map: Terminals × Population → Discovery Rate

Fork of entropy_leibniz_v3_minimal.py with parameterized terminal count
and population size. Measures how discovery rate scales with both axes.

Usage:
  python3 scaling_heatmap.py --terminals 4 --pop_size 1000
  python3 scaling_heatmap.py --full-grid
"""

import argparse
import json
import csv
import time
import math
import random
import sys
import os
import multiprocessing
import io
from pathlib import Path

import numpy as np

OUT_DIR = Path(__file__).parent
PI_OVER_4 = math.pi / 4

# ── Config loader ──────────────────────────────────────────────────────────────

def load_config():
    """Load experiment config from config/scaling_heatmap_config.json."""
    cfg_path = Path(__file__).parent / "config" / "scaling_heatmap_config.json"
    with open(cfg_path) as f:
        return json.load(f)


_CONFIG = load_config()

# ── Grid / seed configuration from config ─────────────────────────────────────

GRID_TERMINAL_COUNTS = _CONFIG["grid"]["terminal_counts"]
GRID_POP_SIZES = _CONFIG["grid"]["pop_sizes"]
SEED_VALS = _CONFIG["seeds"]
N_SEEDS = len(SEED_VALS)

MAX_SEED = float(_CONFIG["time_budgets"]["max_seed_seconds"])
MAX_TOTAL = float(_CONFIG["time_budgets"]["max_total_seconds"])
MAX_WORKERS = int(_CONFIG["parallelism"]["max_workers"])

PRIOR_RESULTS = {
    (c["terminals"], c["pop_size"]): c
    for c in _CONFIG["prior_results"]["cells"]
}

# ── Evaluation setup ──────────────────────────────────────────────────────────
K_MAX = 10000
K_ARRAY = np.arange(K_MAX, dtype=float)
T_CHECKPOINTS = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
T_EVAL = T_CHECKPOINTS

LEIBNIZ_REFS = {T: sum((-1) ** k / (2 * k + 1) for k in range(T))
                for T in T_CHECKPOINTS + [20000]}

# ── Entropy fitness weights ───────────────────────────────────────────────────
W1 = 0.02
W2 = 0.04
W3 = 0.03
LAMBDA_P = 0.005
INFO_CAP = 50.0
INFO_NORM = 50.0
RATE_NORM = 5.0
MIN_GAIN = 0.5

# ── GP hyperparameters ────────────────────────────────────────────────────────
POP_SIZE = 1000          # overridden by --pop_size
MAX_DEPTH = 6
MAX_NODES = 30
TOURNAMENT_K = 7
P_CROSS = 0.70
P_MUT = 0.20
N_ELITE = 5
PATIENCE = 100
DIV_INJECT = 100
WORST = -1e9
CHECKPOINT_INTERVAL = 50
LOG_INTERVAL = 10

# Primitives
FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
FNAMES = list(FUNC_ARITIES.keys())

# EPHEMERALS always empty
EPHEMERALS = []

# ── Terminal set construction ─────────────────────────────────────────────────

def make_terminals(n):
    """
    Construct terminal set of size n following the prescribed pattern:
      N=4:  ["k", 1, -1, 2]
      N=6:  ["k", 1, -1, 2, 3, -2]
      N=8:  ["k", 1, -1, 2, 3, -2, 4, -3]
      N=10: ["k", 1, -1, 2, 3, -2, 4, -3, 5, -4]
      N=12: ["k", 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5]
      N=15: ["k", 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8]
      N=20: ["k", 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8, -7, 9, -8, 10, -9]
    """
    # Base: always starts with ["k", 1, -1, 2]
    base = ["k", 1, -1, 2]
    if n <= 4:
        return base

    # After the base 4, pattern continues: 3, -2, 4, -3, 5, -4, ...
    # i.e., pairs (p, -(p-1)) for p = 3, 4, 5, ...
    result = list(base)
    p = 3
    while len(result) < n:
        # Add positive p
        if len(result) < n:
            result.append(p)
        # Add negative (p-1)
        if len(result) < n:
            result.append(-(p - 1))
        p += 1

    return result[:n]


# Runtime globals (set by setup_globals)
TERM_FIXED = ["k", 1, -1, 2]
ALL_TERMINALS = TERM_FIXED + EPHEMERALS

_fitness_cache: dict = {}


def setup_globals(terminals_n, pop_size):
    """Configure module-level globals from CLI args."""
    global TERM_FIXED, ALL_TERMINALS, POP_SIZE, _fitness_cache
    TERM_FIXED = make_terminals(terminals_n)
    ALL_TERMINALS = TERM_FIXED + EPHEMERALS
    POP_SIZE = pop_size
    _fitness_cache = {}


# ── Node class ────────────────────────────────────────────────────────────────

class Node:
    __slots__ = ("op", "children", "value")

    def __init__(self, op=None, children=None, value=None):
        self.op = op
        self.children = children if children is not None else []
        self.value = value

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
    """Evaluate expression tree. Returns scalar or ndarray."""
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
    """Evaluate tree; return ndarray or None on failure/overflow."""
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


# ── Entropy fitness function ──────────────────────────────────────────────────

def info_bits(error: float) -> float:
    """Convert absolute error to bits of precision about π/4."""
    if error < 1e-15:
        return INFO_CAP
    return -math.log2(error)


def compute_info_profile(tree, k_arr=None) -> list | None:
    """Compute info_bits at each T_CHECKPOINT. Returns None if tree is invalid."""
    terms = safe_eval(tree, k_arr)
    if terms is None:
        return None
    cum = np.cumsum(terms)
    infos = []
    for T in T_CHECKPOINTS:
        if T <= len(cum):
            error = abs(float(cum[T - 1]) - PI_OVER_4)
            infos.append(info_bits(error))
        else:
            infos.append(0.0)
    return infos


def compute_fitness(tree) -> float:
    key = tree.to_str()
    if key in _fitness_cache:
        return _fitness_cache[key]

    infos = compute_info_profile(tree)
    if infos is None:
        _fitness_cache[key] = WORST
        return WORST

    total_info = infos[-1]

    n_gains = sum(1 for i in range(len(infos) - 1)
                  if infos[i + 1] - infos[i] >= MIN_GAIN)
    monotonicity = n_gains / (len(infos) - 1)

    total_span = math.log10(T_CHECKPOINTS[-1] / T_CHECKPOINTS[0])
    mean_rate = (total_info - infos[0]) / total_span if total_span > 0 else 0.0

    parsimony = LAMBDA_P * tree.node_count()

    fitness = (W1 * total_info / INFO_NORM
               + W2 * monotonicity
               + W3 * mean_rate / RATE_NORM
               - parsimony)
    _fitness_cache[key] = fitness
    return fitness


def entropy_components(tree):
    """Return (total_info, monotonicity, mean_rate, parsimony, fitness) for reporting."""
    infos = compute_info_profile(tree)
    if infos is None:
        return (WORST, 0.0, 0.0, 0.0, WORST)

    total_info = infos[-1]
    n_gains = sum(1 for i in range(len(infos) - 1)
                  if infos[i + 1] - infos[i] >= MIN_GAIN)
    monotonicity = n_gains / (len(infos) - 1)

    total_span = math.log10(T_CHECKPOINTS[-1] / T_CHECKPOINTS[0])
    mean_rate = (total_info - infos[0]) / total_span if total_span > 0 else 0.0
    parsimony = LAMBDA_P * tree.node_count()
    fitness = (W1 * total_info / INFO_NORM + W2 * monotonicity
               + W3 * mean_rate / RATE_NORM - parsimony)
    return (round(total_info, 4), round(monotonicity, 4), round(mean_rate, 4),
            round(parsimony, 4), round(fitness, 8))


# ── Tree generation ───────────────────────────────────────────────────────────

def random_terminal():
    return Node(value=random.choice(ALL_TERMINALS))


def grow_tree(max_depth, depth=0):
    if depth >= max_depth:
        return random_terminal()
    if random.random() < 0.45:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[grow_tree(max_depth, depth + 1)
                                  for _ in range(FUNC_ARITIES[op])])


def full_tree(target_depth, depth=0):
    if depth >= target_depth:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[full_tree(target_depth, depth + 1)
                                  for _ in range(FUNC_ARITIES[op])])


def make_random_tree(max_depth=4):
    for _ in range(20):
        t = grow_tree(max_depth) if random.random() < 0.6 else full_tree(random.randint(1, max_depth))
        if 1 <= t.node_count() <= MAX_NODES:
            return t
    return Node(value="k")


def ramped_h_h(n, min_d=2, max_d=5):
    pop = []
    depths = list(range(min_d, max_d + 1))
    per_slot = max(1, n // (len(depths) * 2))
    for d in depths:
        for _ in range(per_slot):
            for _ in range(10):
                t = full_tree(d)
                if 1 <= t.node_count() <= MAX_NODES:
                    pop.append(t)
                    break
        for _ in range(per_slot):
            for _ in range(10):
                t = grow_tree(d)
                if 1 <= t.node_count() <= MAX_NODES:
                    pop.append(t)
                    break
    while len(pop) < n:
        pop.append(make_random_tree(random.randint(min_d, max_d)))
    return pop[:n]


def make_leibniz_tree():
    """(-1)^k / (2k + 1)"""
    return Node(op="div", children=[
        Node(op="pow", children=[Node(value=-1), Node(value="k")]),
        Node(op="add", children=[
            Node(op="mul", children=[Node(value=2), Node(value="k")]),
            Node(value=1),
        ]),
    ])


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


# ── GP main loop ──────────────────────────────────────────────────────────────

def run_seed(seed_idx, seed_val, max_time, global_t0):
    global _fitness_cache
    t0 = time.time()
    random.seed(seed_val)
    np.random.seed(seed_val)
    stop_reason = "time_limit_seed"  # default; overridden below

    log = lambda s: print(s, flush=True)
    log(f"\n── Seed {seed_idx} (val={seed_val}, budget={max_time:.0f}s) ──")

    sample = ramped_h_h(min(50, POP_SIZE))
    t_check = time.time()
    for ind in sample:
        compute_fitness(ind)
    t_per_ind = (time.time() - t_check) / len(sample)
    est_per_gen = t_per_ind * POP_SIZE * 1.5
    log(f"  Perf check: {t_per_ind*1000:.2f}ms/ind, ~{est_per_gen*1000:.0f}ms/gen → "
        f"~{int(max_time / est_per_gen)} gens")

    # NO Leibniz injection — pure random initialization
    population = ramped_h_h(POP_SIZE)

    fitnesses = [compute_fitness(ind) for ind in population]

    best_fit = max(fitnesses)
    best_ind = population[fitnesses.index(best_fit)].copy()
    best_unchanged = 0
    history = []
    gen = 0

    while True:
        elapsed_seed = time.time() - t0
        elapsed_total = time.time() - global_t0
        if elapsed_total >= MAX_TOTAL:
            stop_reason = "time_limit_total"
            log(f"  [STOP] Total time limit at gen {gen} ({elapsed_seed:.1f}s seed / {elapsed_total:.1f}s total)")
            break
        if elapsed_seed >= max_time:
            stop_reason = "time_limit_seed"
            log(f"  [STOP] Seed time limit at gen {gen} ({elapsed_seed:.1f}s seed / {elapsed_total:.1f}s total)")
            break

        gen += 1

        sorted_idx = sorted(range(POP_SIZE), key=lambda i: fitnesses[i], reverse=True)
        elite = [population[i].copy() for i in sorted_idx[:N_ELITE]]

        new_pop = list(elite)
        while len(new_pop) < POP_SIZE:
            r = random.random()
            if r < P_CROSS and len(new_pop) + 1 < POP_SIZE:
                c1, c2 = crossover(
                    tournament_select(population, fitnesses),
                    tournament_select(population, fitnesses),
                )
                new_pop.append(c1)
                if len(new_pop) < POP_SIZE:
                    new_pop.append(c2)
            elif r < P_CROSS + P_MUT:
                new_pop.append(mutate(tournament_select(population, fitnesses)))
            else:
                new_pop.append(tournament_select(population, fitnesses).copy())

        population = new_pop[:POP_SIZE]
        fitnesses = [compute_fitness(ind) for ind in population]

        gen_best = max(fitnesses)
        if gen_best > best_fit:
            best_fit = gen_best
            best_ind = population[fitnesses.index(gen_best)].copy()
            best_unchanged = 0
        else:
            best_unchanged += 1

        top20 = sorted(fitnesses, reverse=True)[:20]
        if len(set(round(f, 6) for f in top20)) == 1:
            new_rand = ramped_h_h(DIV_INJECT)
            worst_idxs = sorted(range(POP_SIZE), key=lambda i: fitnesses[i])[:DIV_INJECT]
            for i, idx in enumerate(worst_idxs):
                population[idx] = new_rand[i]
                fitnesses[idx] = compute_fitness(new_rand[i])
            log(f"  [DIVERSITY] Gen {gen}: injected {DIV_INJECT}")

        if gen % LOG_INTERVAL == 0:
            elapsed = time.time() - t0
            mean_f = sum(fitnesses) / POP_SIZE
            ti, mo, mr, ps, _ = entropy_components(best_ind)
            expr = best_ind.to_str()
            log(f"  Gen {gen:4d} | fit={best_fit:.6f} | mean={mean_f:.6f} | "
                f"ti={ti:.2f} mo={mo:.2f} mr={mr:.2f} ps={ps:.3f} | "
                f"nc={best_ind.node_count()} | {expr[:50]} | t={elapsed:.1f}s")
            history.append({
                "gen": gen,
                "best_fitness": round(best_fit, 8),
                "mean_fitness": round(mean_f, 8),
                "best_expr": expr,
                "node_count": best_ind.node_count(),
                "total_info": ti,
                "monotonicity": mo,
                "mean_rate": mr,
                "parsimony": ps,
            })

        if gen % CHECKPOINT_INTERVAL == 0:
            elapsed = time.time() - t0
            with open(OUT_DIR / "progress.json", "w") as f:
                json.dump({
                    "seed": seed_idx, "generation": gen,
                    "best_fitness": best_fit, "best_expr": best_ind.to_str(),
                    "elapsed": round(elapsed, 2), "remaining": round(max_time - elapsed, 2),
                }, f)

        if best_unchanged >= PATIENCE:
            infos = compute_info_profile(best_ind)
            if infos is not None:
                if infos[-1] >= 13.0:
                    is_mono = all(infos[i + 1] >= infos[i] for i in range(len(infos) - 1))
                    if is_mono:
                        stop_reason = "early_stop_converged"
                        log(f"  [EARLY STOP] Gen {gen}: stable + converging (info={infos[-1]:.2f} bits)")
                        break
            best_unchanged = 0

    elapsed = time.time() - t0
    ti, mo, mr, ps, _ = entropy_components(best_ind)
    log(f"  Done: gen={gen}, fit={best_fit:.8f}, nc={best_ind.node_count()}, "
        f"ti={ti:.2f} mo={mo:.2f} mr={mr:.2f} t={elapsed:.1f}s\n  expr={best_ind.to_str()[:80]}")
    log(f"  stop_reason={stop_reason}")

    return {
        "seed": seed_idx,
        "seed_val": seed_val,
        "generations": gen,
        "best_fitness": best_fit,
        "best_expr": best_ind.to_str(),
        "best_ind": best_ind,
        "history": history,
        "elapsed": round(elapsed, 2),
        "stop_reason": stop_reason,
    }


# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze_result(result):
    ind = result["best_ind"]
    terms = safe_eval(ind, K_ARRAY)
    if terms is None:
        return {"errors": {}, "infos": {}, "is_equivalent": False,
                "is_monotone": False, "monotonicity": 0.0, "mean_rate": 0.0}

    cum = np.cumsum(terms)
    errors = {}
    infos = {}
    for T in T_CHECKPOINTS:
        e = abs(float(cum[T - 1]) - PI_OVER_4)
        errors[T] = round(e, 10)
        infos[T] = round(info_bits(e), 4)

    k_ext = np.arange(20000, dtype=float)
    terms_ext = safe_eval(ind, k_ext)
    if terms_ext is not None:
        e20k = abs(float(np.sum(terms_ext)) - PI_OVER_4)
        errors[20000] = round(e20k, 10)
        infos[20000] = round(info_bits(e20k), 4)
    else:
        errors[20000] = None
        infos[20000] = None

    leibniz_terms = [(-1) ** k / (2 * k + 1) for k in range(20)]
    agent_terms = [float(terms[k]) for k in range(20)]
    is_equiv = all(abs(agent_terms[k] - leibniz_terms[k]) < 1e-6 for k in range(20))

    expr = result["best_expr"]
    is_structural = ("^" in expr and "-1" in expr and "k" in expr
                     and ("2 *" in expr or "* 2") and "+" in expr)

    info_list = [infos[T] for T in T_CHECKPOINTS]
    is_mono = all(info_list[i + 1] >= info_list[i] for i in range(len(info_list) - 1))

    ti, mo, mr, ps, fit = entropy_components(ind)

    t_samples = sorted(set([1] + list(range(10, 201, 10)) + [500, 1000, 2000, 5000]))
    partial_sums = {T: round(float(cum[T - 1]), 8) for T in t_samples if T <= K_MAX}

    return {
        "errors": errors,
        "infos": infos,
        "is_equivalent": is_equiv,
        "is_structural": is_structural,
        "is_monotone": is_mono,
        "monotonicity": mo,
        "mean_rate": mr,
        "total_info": ti,
        "partial_sums": partial_sums,
        "terms_20": [round(float(terms[k]), 8) for k in range(20)],
    }


# ── Output writers ────────────────────────────────────────────────────────────

def write_results(seed_results, terminals_n, pop_size):
    """Write per-cell output files."""
    tag = f"t{terminals_n}_p{pop_size}"
    txt_path = OUT_DIR / f"scaling_heatmap_{tag}.txt"
    json_path = OUT_DIR / f"scaling_heatmap_{tag}_data.json"

    # Compute summary stats
    n_found = sum(1 for r in seed_results if r.get("analysis", {}).get("is_equivalent", False))
    successful = [r for r in seed_results if r.get("analysis", {}).get("is_equivalent", False)]
    mean_gens = (sum(r["generations"] for r in successful) / len(successful)) if successful else None
    mean_elapsed = (sum(r["elapsed"] for r in successful) / len(successful)) if successful else None

    # Collect top expressions for failed seeds
    failed = [r for r in seed_results if not r.get("analysis", {}).get("is_equivalent", False)]
    top_exprs = [r["best_expr"] for r in sorted(failed, key=lambda r: r["best_fitness"], reverse=True)]

    W = 72
    lines = [
        "=" * W,
        f"SCALING HEATMAP: terminals={terminals_n}, pop_size={pop_size}",
        f"Terminal set: {TERM_FIXED}",
        f"EPHEMERALS: {EPHEMERALS}",
        f"MAX_SEED={MAX_SEED:.0f}s, MAX_TOTAL={MAX_TOTAL:.0f}s",
        "=" * W,
        "",
        f"Discovery: {n_found}/{N_SEEDS} seeds found Leibniz",
    ]
    if mean_gens is not None:
        lines.append(f"Mean generations (successful): {mean_gens:.1f}")
        lines.append(f"Mean elapsed (successful): {mean_elapsed:.1f}s")
    if top_exprs:
        lines.append(f"\nTop expressions (failed seeds):")
        for expr in top_exprs[:5]:
            lines.append(f"  {expr}")
    lines.append("")

    for r in seed_results:
        ana = r.get("analysis", {})
        is_eq = ana.get("is_equivalent", False)
        ti = ana.get("total_info", 0.0)
        mo = ana.get("monotonicity", 0.0)
        mr = ana.get("mean_rate", 0.0)
        sr = r.get("stop_reason", "unknown")
        lines.append(f"Seed {r['seed']} (val={r['seed_val']}): "
                     f"gens={r['generations']} elapsed={r['elapsed']:.1f}s "
                     f"found={is_eq} ti={ti:.2f} mo={mo:.2f} mr={mr:.2f} stop={sr}")
        lines.append(f"  expr={r['best_expr'][:80]}")
    lines.append("")

    txt_path.write_text("\n".join(lines))
    print(f"  Wrote {txt_path}", flush=True)

    # JSON data
    data = {
        "terminals_n": terminals_n,
        "term_fixed": TERM_FIXED,
        "ephemerals": EPHEMERALS,
        "pop_size": pop_size,
        "n_seeds": N_SEEDS,
        "n_found": n_found,
        "mean_gens_success": round(mean_gens, 2) if mean_gens is not None else None,
        "mean_elapsed_success": round(mean_elapsed, 2) if mean_elapsed is not None else None,
        "top_failed_exprs": top_exprs[:5],
        "seeds": [
            {
                "seed": r["seed"],
                "seed_val": r["seed_val"],
                "generations": r["generations"],
                "best_fitness": round(r["best_fitness"], 8),
                "best_expr": r["best_expr"],
                "elapsed": r["elapsed"],
                "stop_reason": r.get("stop_reason", "unknown"),
                "is_equivalent": r.get("analysis", {}).get("is_equivalent", False),
                "is_monotone": r.get("analysis", {}).get("is_monotone", False),
                "total_info": r.get("analysis", {}).get("total_info", 0.0),
                "monotonicity": r.get("analysis", {}).get("monotonicity", 0.0),
                "mean_rate": r.get("analysis", {}).get("mean_rate", 0.0),
                "info_profile": {str(T): v for T, v in
                                 r.get("analysis", {}).get("infos", {}).items()},
            }
            for r in seed_results
        ],
    }
    with open(json_path, "w") as f:
        json.dump(data, f, separators=(",", ":"), indent=2)
    print(f"  Wrote {json_path}", flush=True)

    return n_found, mean_gens, mean_elapsed


# ── In-process cell runner for multiprocessing Pool ───────────────────────────

def run_cell_inprocess(args):
    """
    Worker function for multiprocessing.Pool.
    Runs one cell in-process (not subprocess), redirecting stdout/stderr to a log file.
    """
    t_n, p_s = args
    log_file = OUT_DIR / f"scaling_heatmap_t{t_n}_p{p_s}.log"

    print(f"  [GRID] Starting t={t_n} p={p_s} → log: {log_file.name}", flush=True)
    t0 = time.time()

    try:
        with open(log_file, "w") as lf:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = lf
            sys.stderr = lf
            try:
                main_single(t_n, p_s)
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
        elapsed = time.time() - t0
        print(f"  [GRID] Done t={t_n} p={p_s} in {elapsed:.0f}s [OK]", flush=True)
        return (t_n, p_s, 0, elapsed)
    except Exception as exc:
        elapsed = time.time() - t0
        print(f"  [GRID] Error t={t_n} p={p_s} in {elapsed:.0f}s: {exc}", flush=True)
        return (t_n, p_s, 1, elapsed)


# ── Full-grid runner ──────────────────────────────────────────────────────────

def run_full_grid():
    """Run all grid cells in parallel via multiprocessing.Pool with imap_unordered."""
    # Generate grid dynamically from config
    grid_cells = [(t, p) for t in GRID_TERMINAL_COUNTS for p in GRID_POP_SIZES]

    # Skip prior results that don't need re-running
    cells_to_run = [(t, p) for (t, p) in grid_cells if (t, p) not in PRIOR_RESULTS]

    print(f"\n[FULL GRID] {len(grid_cells)} total cells, "
          f"{len(PRIOR_RESULTS)} prior (skip), "
          f"{len(cells_to_run)} to run", flush=True)
    print(f"  MAX_WORKERS={MAX_WORKERS}, MAX_SEED={MAX_SEED:.0f}s, MAX_TOTAL={MAX_TOTAL:.0f}s", flush=True)

    results = []
    with multiprocessing.Pool(processes=MAX_WORKERS) as pool:
        for result in pool.imap_unordered(run_cell_inprocess, cells_to_run):
            t_n, p_s, rc, elapsed = result
            status = "OK" if rc == 0 else f"ERR({rc})"
            print(f"  [GRID] Completed t={t_n} p={p_s} [{status}] in {elapsed:.0f}s "
                  f"({len(results)+1}/{len(cells_to_run)})", flush=True)
            results.append(result)

    print(f"\n[FULL GRID] All cells complete.", flush=True)

    # Write summary markdown
    write_grid_results_md()

    return results


def load_cell_data(t_n, p_s):
    """Load JSON data for a completed cell, or return None."""
    json_path = OUT_DIR / f"scaling_heatmap_t{t_n}_p{p_s}_data.json"
    if not json_path.exists():
        return None
    try:
        with open(json_path) as f:
            return json.load(f)
    except Exception:
        return None


def write_grid_results_md():
    """Collect all cell results and write scaling_heatmap_results.md."""
    # Load prior results from config
    prior_map = {}
    for c in _CONFIG["prior_results"]["cells"]:
        prior_map[(c["terminals"], c["pop_size"])] = {
            "n_found": c["seeds_found"],
            "prior": True,
            "mean_gens": c.get("mean_gens_success"),
            "mean_elapsed": c.get("mean_elapsed_success"),
        }

    terminal_counts = GRID_TERMINAL_COUNTS
    pop_sizes = GRID_POP_SIZES

    # Build data table
    table = {}  # (t, p) -> {n_found, mean_gens, mean_elapsed, top_exprs, prior}
    for t in terminal_counts:
        for p in pop_sizes:
            if (t, p) in prior_map:
                entry = dict(prior_map[(t, p)])
                data = load_cell_data(t, p)
                if data:
                    entry["n_found"] = data.get("n_found", entry["n_found"])
                    entry["mean_gens"] = data.get("mean_gens_success")
                    entry["mean_elapsed"] = data.get("mean_elapsed_success")
                    entry["top_exprs"] = data.get("top_failed_exprs", [])
                    entry["term_fixed"] = data.get("term_fixed", make_terminals(t))
                else:
                    entry.setdefault("mean_gens", None)
                    entry.setdefault("mean_elapsed", None)
                    entry["top_exprs"] = []
                    entry["term_fixed"] = make_terminals(t)
                table[(t, p)] = entry
            else:
                data = load_cell_data(t, p)
                if data:
                    table[(t, p)] = {
                        "n_found": data.get("n_found", "?"),
                        "mean_gens": data.get("mean_gens_success"),
                        "mean_elapsed": data.get("mean_elapsed_success"),
                        "top_exprs": data.get("top_failed_exprs", []),
                        "term_fixed": data.get("term_fixed", make_terminals(t)),
                        "prior": False,
                    }
                else:
                    table[(t, p)] = {
                        "n_found": "?",
                        "mean_gens": None,
                        "mean_elapsed": None,
                        "top_exprs": [],
                        "term_fixed": make_terminals(t),
                        "prior": False,
                    }

    lines = []
    lines.append("# Scaling Heat Map: Terminals × Population → Discovery Rate")
    lines.append("")
    lines.append("Experiment: entropy-leibniz-v3 minimal, no injection, 5 seeds per cell.")
    lines.append(f"Budget: MAX_SEED={MAX_SEED:.0f}s, MAX_TOTAL={MAX_TOTAL:.0f}s per cell.")
    lines.append("")

    # ── Table 1: Discovery rates ──
    lines.append("## Discovery Rate Table (seeds found / 5)")
    lines.append("")
    lines.append("| Terminals | Terminal Set | Pop=1000 | Pop=2000 | Pop=5000 |")
    lines.append("|-----------|-------------|----------|----------|----------|")

    for t in terminal_counts:
        term_set = make_terminals(t)
        term_str = "{" + ", ".join(str(x) for x in term_set) + "}"
        cells = []
        for p in pop_sizes:
            entry = table.get((t, p), {})
            nf = entry.get("n_found", "?")
            star = "*" if entry.get("prior", False) else ""
            cells.append(f"{nf}/5{star}")
        lines.append(f"| {t:<9} | `{term_str}`{' ' * max(0, 24 - len(term_str))} | {cells[0]:<8} | {cells[1]:<8} | {cells[2]:<8} |")

    lines.append("")
    lines.append("\\* = from prior experiment (not re-run)")
    lines.append("")

    # ── Table 2: Mean generations (successful only) ──
    lines.append("## Mean Generations (successful seeds only)")
    lines.append("")
    lines.append("| Terminals | Pop=1000 | Pop=2000 | Pop=5000 |")
    lines.append("|-----------|----------|----------|----------|")
    for t in terminal_counts:
        cells = []
        for p in pop_sizes:
            entry = table.get((t, p), {})
            mg = entry.get("mean_gens")
            nf = entry.get("n_found", 0)
            if nf == 0 or mg is None:
                cells.append("—")
            else:
                cells.append(f"{mg:.0f}")
        lines.append(f"| {t:<9} | {cells[0]:<8} | {cells[1]:<8} | {cells[2]:<8} |")
    lines.append("")

    # ── Table 3: Mean elapsed time (successful only) ──
    lines.append("## Mean Elapsed Time / successful seed (seconds)")
    lines.append("")
    lines.append("| Terminals | Pop=1000 | Pop=2000 | Pop=5000 |")
    lines.append("|-----------|----------|----------|----------|")
    for t in terminal_counts:
        cells = []
        for p in pop_sizes:
            entry = table.get((t, p), {})
            me = entry.get("mean_elapsed")
            nf = entry.get("n_found", 0)
            if nf == 0 or me is None:
                cells.append("—")
            else:
                cells.append(f"{me:.0f}s")
        lines.append(f"| {t:<9} | {cells[0]:<8} | {cells[1]:<8} | {cells[2]:<8} |")
    lines.append("")

    # ── Phase transition analysis ──
    lines.append("## Phase Transition Analysis")
    lines.append("")
    lines.append("At what terminal count does each population size fail (0/5)?")
    lines.append("")
    for p in pop_sizes:
        first_fail = None
        for t in terminal_counts:
            nf = table.get((t, p), {}).get("n_found", "?")
            if nf == 0:
                first_fail = t
                break
        if first_fail is not None:
            lines.append(f"- Pop={p}: first complete failure at terminals={first_fail}")
        else:
            lines.append(f"- Pop={p}: no complete failure observed in grid")
    lines.append("")

    # ── Wrong-limit attractors ──
    lines.append("## Wrong-Limit Attractors")
    lines.append("")
    lines.append("Top expressions dominating failed cells:")
    lines.append("")
    seen_exprs = {}
    for t in terminal_counts:
        for p in pop_sizes:
            entry = table.get((t, p), {})
            nf = entry.get("n_found", 0)
            if nf == 0 or nf == "?":
                for expr in entry.get("top_exprs", []):
                    seen_exprs[expr] = seen_exprs.get(expr, 0) + 1
    if seen_exprs:
        sorted_exprs = sorted(seen_exprs.items(), key=lambda x: x[1], reverse=True)
        for expr, count in sorted_exprs[:10]:
            lines.append(f"- (×{count}) `{expr[:80]}`")
    else:
        lines.append("- (no failed cells with data yet)")
    lines.append("")

    # ── Conclusions ──
    lines.append("## Conclusions")
    lines.append("")

    # Determine if there is a sharp boundary
    boundary_counts = {}
    for p in pop_sizes:
        boundary_counts[p] = []
        for t in terminal_counts:
            nf = table.get((t, p), {}).get("n_found", "?")
            boundary_counts[p].append((t, nf))

    lines.append("### Is there a sharp phase boundary?")
    lines.append("")
    for p in pop_sizes:
        bc = boundary_counts[p]
        # Find transition: last success → first failure
        last_success = None
        first_failure = None
        for t, nf in bc:
            if isinstance(nf, int) and nf > 0:
                last_success = t
            elif isinstance(nf, int) and nf == 0 and first_failure is None:
                first_failure = t
        if last_success and first_failure:
            lines.append(f"- Pop={p}: last success at t={last_success}, "
                         f"first 0/5 at t={first_failure} → "
                         f"boundary between {last_success} and {first_failure} terminals")
        elif last_success and not first_failure:
            lines.append(f"- Pop={p}: all tested terminal counts succeed (up to t={last_success})")
        elif first_failure and not last_success:
            lines.append(f"- Pop={p}: all tested terminal counts fail")
        else:
            lines.append(f"- Pop={p}: insufficient data")
    lines.append("")

    lines.append("### Does pop=5000 extend the boundary?")
    lines.append("")
    # Compare pop=1000 vs pop=5000 failure boundaries
    fail_1k = None
    fail_5k = None
    for t in terminal_counts:
        nf_1k = table.get((t, 1000), {}).get("n_found", "?")
        nf_5k = table.get((t, 5000), {}).get("n_found", "?")
        if isinstance(nf_1k, int) and nf_1k == 0 and fail_1k is None:
            fail_1k = t
        if isinstance(nf_5k, int) and nf_5k == 0 and fail_5k is None:
            fail_5k = t
    if fail_1k and fail_5k:
        if fail_5k > fail_1k:
            lines.append(f"Yes: pop=5000 pushes the failure boundary from "
                         f"t={fail_1k} to t={fail_5k} (+{fail_5k - fail_1k} terminals).")
        elif fail_5k == fail_1k:
            lines.append(f"No: pop=5000 fails at the same terminal count (t={fail_5k}) as pop=1000.")
        else:
            lines.append(f"Unexpected: pop=5000 fails earlier (t={fail_5k}) than pop=1000 (t={fail_1k}).")
    elif fail_5k is None and fail_1k is not None:
        lines.append(f"Yes: pop=1000 first fails at t={fail_1k}, but pop=5000 never fails in this grid.")
    else:
        lines.append("Insufficient data to determine.")
    lines.append("")

    lines.append("### Summary")
    lines.append("")
    total_cells = len(terminal_counts) * len(pop_sizes)
    cells_with_data = sum(1 for t in terminal_counts for p in pop_sizes
                          if isinstance(table.get((t, p), {}).get("n_found"), int))
    cells_found = sum(1 for t in terminal_counts for p in pop_sizes
                      if isinstance(table.get((t, p), {}).get("n_found"), int)
                      and table[(t, p)]["n_found"] > 0)
    lines.append(f"- Grid: {len(terminal_counts)} terminal counts × {len(pop_sizes)} pop sizes = {total_cells} cells")
    lines.append(f"- Cells with data: {cells_with_data}/{total_cells}")
    lines.append(f"- Cells with ≥1 discovery: {cells_found}/{cells_with_data}")
    lines.append("")
    lines.append("The entropy information-theoretic fitness creates a search landscape")
    lines.append("where discovery rate degrades as the terminal set grows, consistent")
    lines.append("with the search space expanding faster than the fitness gradient can guide.")
    lines.append("")

    md_path = OUT_DIR / "scaling_heatmap_results.md"
    md_path.write_text("\n".join(lines))
    print(f"\n  Wrote {md_path}", flush=True)


# ── Single-cell entry point ───────────────────────────────────────────────────

def main_single(terminals_n, pop_size):
    """Run a single grid cell."""
    setup_globals(terminals_n, pop_size)

    global_t0 = time.time()
    tag = f"t{terminals_n}_p{pop_size}"

    print("=" * 72, flush=True)
    print(f"Scaling Heatmap: terminals={terminals_n}, pop_size={pop_size}", flush=True)
    print(f"  Terminal set: {TERM_FIXED}", flush=True)
    print(f"  EPHEMERALS: {EPHEMERALS}", flush=True)
    print(f"  π/4 = {PI_OVER_4:.10f}", flush=True)
    print(f"  MAX_SEED={MAX_SEED:.0f}s  MAX_TOTAL={MAX_TOTAL:.0f}s", flush=True)
    print("=" * 72, flush=True)

    seed_results = []

    for i, sv in enumerate(SEED_VALS):
        elapsed_total = time.time() - global_t0
        remaining = MAX_TOTAL - elapsed_total
        seed_budget = min(MAX_SEED, remaining / (N_SEEDS - i))
        if seed_budget < 5:
            print(f"  Skipping seed {i} ({remaining:.1f}s remaining)", flush=True)
            break
        result = run_seed(i, sv, seed_budget, global_t0)
        seed_results.append(result)

    if not seed_results:
        print("ERROR: no seeds completed", flush=True)
        return

    print(f"\nAnalyzing {len(seed_results)} seeds...", flush=True)
    for r in seed_results:
        r["analysis"] = analyze_result(r)

    n_found, mean_gens, mean_elapsed = write_results(seed_results, terminals_n, pop_size)

    print(f"\nResult: {n_found}/{N_SEEDS} seeds found Leibniz", flush=True)
    if mean_gens:
        print(f"  Mean generations (success): {mean_gens:.1f}", flush=True)
        print(f"  Mean elapsed (success): {mean_elapsed:.1f}s", flush=True)
    print(f"Total elapsed: {time.time() - global_t0:.1f}s", flush=True)
    print("=" * 72, flush=True)


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Scaling Heat Map: Terminals × Population → Discovery Rate"
    )
    parser.add_argument(
        "--terminals", type=int, default=4,
        choices=[4, 6, 8, 10, 12, 15, 20],
        help="Number of terminals (4, 6, 8, 10, 12, 15, or 20)"
    )
    parser.add_argument(
        "--pop_size", type=int, default=1000,
        help="GP population size (default: 1000)"
    )
    parser.add_argument(
        "--full-grid", action="store_true",
        help="Run all grid cells in parallel (skips prior results)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.full_grid:
        run_full_grid()
    else:
        main_single(args.terminals, args.pop_size)
