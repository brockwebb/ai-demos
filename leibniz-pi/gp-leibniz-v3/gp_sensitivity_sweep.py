#!/usr/bin/env python3
"""
GP Parameter Sensitivity Sweep.

Copy of gp_leibniz_v3_minimal.py with argparse to override ALPHA, LAMBDA_P,
POP_SIZE, and TOURNAMENT_K. All other logic is identical to the original.

Usage:
    python3 gp_sensitivity_sweep.py                   # baseline
    python3 gp_sensitivity_sweep.py --alpha 0.1
    python3 gp_sensitivity_sweep.py --lambda_p 0.01
    python3 gp_sensitivity_sweep.py --pop_size 2000
    python3 gp_sensitivity_sweep.py --tournament_k 3
"""

import argparse
import json
import csv
import time
import math
import random
import sys
import numpy as np
from pathlib import Path

# ── Argparse (must come before module-level constants) ────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="GP Leibniz v3 sensitivity sweep — vary one parameter at a time"
    )
    parser.add_argument("--alpha",        type=float, default=0.05,
                        help="Convergence bonus weight (default: 0.05)")
    parser.add_argument("--lambda_p",     type=float, default=0.005,
                        help="Parsimony penalty per node (default: 0.005)")
    parser.add_argument("--pop_size",     type=int,   default=1000,
                        help="Population size (default: 1000)")
    parser.add_argument("--tournament_k", type=int,   default=7,
                        help="Tournament selection size (default: 7)")
    return parser.parse_args()

_args = parse_args()

OUT_DIR = Path(__file__).parent
PI_OVER_4 = math.pi / 4

# ── Evaluation setup ──────────────────────────────────────────────────────────
K_MAX = 5000
K_ARRAY = np.arange(K_MAX, dtype=float)
T_EVAL = [10, 50, 200, 1000, 5000]

LEIBNIZ_REFS = {T: sum((-1) ** k / (2 * k + 1) for k in range(T)) for T in T_EVAL + [10000]}

# ── GP hyperparameters (with argparse overrides) ──────────────────────────────
POP_SIZE    = _args.pop_size
MAX_DEPTH   = 6
MAX_NODES   = 30
TOURNAMENT_K = _args.tournament_k
P_CROSS     = 0.70
P_MUT       = 0.20
N_ELITE     = 5
ALPHA       = _args.alpha
LAMBDA_P    = _args.lambda_p
PATIENCE    = 100
STOP_THRESH = 0.001
DIV_INJECT  = 100
WORST       = -1e9
MAX_TOTAL   = 1800.0
MAX_SEED    = 360.0
N_SEEDS     = 5
CHECKPOINT_INTERVAL = 50
LOG_INTERVAL = 10

# Primitives
FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
FNAMES = list(FUNC_ARITIES.keys())
TERM_FIXED = ["k", 1, -1, 2]
EPHEMERALS = []
ALL_TERMINALS = TERM_FIXED + EPHEMERALS

# Global fitness cache (expression string → fitness value)
_fitness_cache: dict = {}


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


# ── Tree evaluation (scalar-optimized) ───────────────────────────────────────

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
            b_safe = b if not np.isscalar(b) else np.array(b)
            mask = np.abs(b_safe) > 1e-10
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


# ── Fitness function (v2) ─────────────────────────────────────────────────────

def compute_fitness(tree):
    """
    Three-component fitness:
      accuracy        = -mean(errors at T_EVAL)
      convergence_bonus = fraction of consecutive pairs with >5% error improvement
      parsimony       = LAMBDA_P * node_count

    fitness = accuracy + ALPHA * convergence_bonus - parsimony
    """
    key = tree.to_str()
    if key in _fitness_cache:
        return _fitness_cache[key]

    terms = safe_eval(tree)
    if terms is None:
        _fitness_cache[key] = WORST
        return WORST

    cum = np.cumsum(terms)
    errors = [abs(float(cum[T - 1]) - PI_OVER_4) for T in T_EVAL]

    if any(e > 1e4 for e in errors):
        _fitness_cache[key] = WORST
        return WORST

    accuracy = -float(np.mean(errors))

    n_improving = sum(
        1 for i in range(len(errors) - 1)
        if errors[i + 1] < errors[i] * 0.95
    )
    conv_bonus = n_improving / (len(errors) - 1)

    parsimony = LAMBDA_P * tree.node_count()

    fitness = accuracy + ALPHA * conv_bonus - parsimony
    _fitness_cache[key] = fitness
    return fitness


def fitness_components(tree):
    """Return (accuracy, conv_bonus, parsimony, fitness) for reporting."""
    terms = safe_eval(tree)
    if terms is None:
        return (WORST, 0.0, 0.0, WORST)
    cum = np.cumsum(terms)
    errors = [abs(float(cum[T - 1]) - PI_OVER_4) for T in T_EVAL]
    accuracy = -float(np.mean(errors))
    n_improving = sum(1 for i in range(len(errors) - 1) if errors[i + 1] < errors[i] * 0.95)
    conv_bonus = n_improving / (len(errors) - 1)
    parsimony = LAMBDA_P * tree.node_count()
    return (round(accuracy, 8), round(conv_bonus, 4), round(parsimony, 4),
            round(accuracy + ALPHA * conv_bonus - parsimony, 8))


# ── Tree generation ───────────────────────────────────────────────────────────

def random_terminal():
    return Node(value=random.choice(ALL_TERMINALS))


def grow_tree(max_depth, depth=0):
    if depth >= max_depth:
        return random_terminal()
    if random.random() < 0.45:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[grow_tree(max_depth, depth + 1) for _ in range(FUNC_ARITIES[op])])


def full_tree(target_depth, depth=0):
    if depth >= target_depth:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[full_tree(target_depth, depth + 1) for _ in range(FUNC_ARITIES[op])])


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
    """(-1)^k / (2k + 1) — kept for reporting/comparison only."""
    return Node(op="div", children=[
        Node(op="pow", children=[Node(value=-1), Node(value="k")]),
        Node(op="add", children=[
            Node(op="mul", children=[Node(value=2), Node(value="k")]),
            Node(value=1),
        ]),
    ])


def make_gp1_best_tree():
    """GP v1 best: (-3-k)^(-k)  =  pow(sub(-3, k), neg(k))"""
    return Node(op="pow", children=[
        Node(op="sub", children=[Node(value=-3), Node(value="k")]),
        Node(op="neg", children=[Node(value="k")]),
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
        if elapsed_seed >= max_time or elapsed_total >= MAX_TOTAL:
            log(f"  [STOP] Time at gen {gen} ({elapsed_seed:.1f}s seed / {elapsed_total:.1f}s total)")
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
            acc, cb, ps, _ = fitness_components(best_ind)
            expr = best_ind.to_str()
            log(f"  Gen {gen:4d} | fit={best_fit:.6f} | mean={mean_f:.6f} | "
                f"acc={acc:.5f} cb={cb:.2f} ps={ps:.3f} | nc={best_ind.node_count()} | "
                f"{expr[:55]} | t={elapsed:.1f}s")
            t10_k = np.arange(10, dtype=float)
            t10_terms = safe_eval(best_ind, t10_k)
            history.append({
                "gen": gen,
                "best_fitness": round(best_fit, 8),
                "mean_fitness": round(mean_f, 8),
                "best_expr": expr,
                "node_count": best_ind.node_count(),
                "accuracy": acc,
                "conv_bonus": cb,
                "parsimony": ps,
                "terms_t10": [round(float(v), 6) for v in
                              (t10_terms if t10_terms is not None else [0.0] * 10)],
            })

        if gen % CHECKPOINT_INTERVAL == 0:
            elapsed = time.time() - t0
            with open(OUT_DIR / "progress_sweep.json", "w") as f:
                json.dump({
                    "seed": seed_idx,
                    "generation": gen,
                    "best_fitness": best_fit,
                    "best_expr": best_ind.to_str(),
                    "elapsed": round(elapsed, 2),
                    "remaining": round(max_time - elapsed, 2),
                    "params": {
                        "alpha": ALPHA, "lambda_p": LAMBDA_P,
                        "pop_size": POP_SIZE, "tournament_k": TOURNAMENT_K,
                    },
                }, f)

        if best_unchanged >= PATIENCE:
            terms = safe_eval(best_ind)
            if terms is not None:
                cum = np.cumsum(terms)
                all_good = all(abs(float(cum[T - 1]) - PI_OVER_4) < STOP_THRESH for T in T_EVAL)
                if all_good:
                    log(f"  [EARLY STOP] Gen {gen}: stable + threshold met")
                    break
            best_unchanged = 0

    elapsed = time.time() - t0
    acc, cb, ps, _ = fitness_components(best_ind)
    log(f"  Done: gen={gen}, fit={best_fit:.8f}, nc={best_ind.node_count()}, "
        f"acc={acc:.5f} cb={cb:.2f} t={elapsed:.1f}s\n  expr={best_ind.to_str()[:80]}")

    return {
        "seed": seed_idx,
        "seed_val": seed_val,
        "generations": gen,
        "best_fitness": best_fit,
        "best_expr": best_ind.to_str(),
        "best_ind": best_ind,
        "history": history,
        "elapsed": round(elapsed, 2),
    }


# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze_result(result):
    ind = result["best_ind"]
    terms = safe_eval(ind, K_ARRAY)
    if terms is None:
        return {"errors": {}, "is_equivalent": False, "partial_sums": [], "terms_20": [],
                "accuracy": WORST, "conv_bonus": 0.0}

    cum = np.cumsum(terms)
    errors = {}
    for T in T_EVAL:
        errors[T] = round(abs(float(cum[T - 1]) - PI_OVER_4), 10)

    k_ext = np.arange(10000, dtype=float)
    terms_ext = safe_eval(ind, k_ext)
    if terms_ext is not None:
        errors[10000] = round(abs(float(np.sum(terms_ext)) - PI_OVER_4), 10)
    else:
        errors[10000] = None

    leibniz_terms = [(-1) ** k / (2 * k + 1) for k in range(20)]
    agent_terms = [float(terms[k]) for k in range(20)]
    is_equiv = all(abs(agent_terms[k] - leibniz_terms[k]) < 1e-6 for k in range(20))

    expr = result["best_expr"]
    is_structural = ("^" in expr and "-1" in expr and "k" in expr
                     and ("2 *" in expr or "* 2") and "+" in expr)

    error_list = [errors[T] for T in T_EVAL]
    is_monotone = all(error_list[i + 1] < error_list[i] for i in range(len(error_list) - 1))

    acc, cb, ps, _ = fitness_components(ind)

    t_samples = sorted(set([1] + list(range(10, 201, 10)) + [500, 1000, 2000, 5000]))
    partial_sums = {T: round(float(cum[T - 1]), 8) for T in t_samples if T <= K_MAX}

    return {
        "errors": errors,
        "is_equivalent": is_equiv,
        "is_structural": is_structural,
        "is_monotone_converging": is_monotone,
        "accuracy": acc,
        "conv_bonus": cb,
        "partial_sums": partial_sums,
        "terms_20": [round(float(terms[k]), 8) for k in range(20)],
    }


# ── Output writers ────────────────────────────────────────────────────────────

def param_tag():
    """Build a short filename-safe tag for the current parameter config."""
    parts = []
    if ALPHA != 0.05:
        parts.append(f"alpha{ALPHA}")
    if LAMBDA_P != 0.005:
        parts.append(f"lp{LAMBDA_P}")
    if POP_SIZE != 1000:
        parts.append(f"pop{POP_SIZE}")
    if TOURNAMENT_K != 7:
        parts.append(f"tk{TOURNAMENT_K}")
    return "_".join(parts) if parts else "baseline"


def write_sensitivity_txt(seed_results, expressions_found, gens_found):
    tag = param_tag()
    fname = f"sensitivity_{tag}.txt"
    path = OUT_DIR / fname

    lines = [
        f"=== GP Sensitivity Sweep: {tag} ===",
        f"alpha={ALPHA}  lambda_p={LAMBDA_P}  pop_size={POP_SIZE}  tournament_k={TOURNAMENT_K}",
        f"Seeds: {[r['seed_val'] for r in seed_results]}",
        f"Seeds found: {len(expressions_found)}/5",
        "",
    ]

    for r in seed_results:
        ana = r.get("analysis", {})
        is_eq = ana.get("is_equivalent", False)
        status = "FOUND" if is_eq else "not found"
        lines.append(f"  Seed {r['seed']} (val={r['seed_val']}): gen={r['generations']} "
                     f"fit={r['best_fitness']:.6f} [{status}]  expr={r['best_expr']}")

    lines.append("")
    lines.append(f"Expressions found: {expressions_found}")
    lines.append(f"Gens at success:   {gens_found}")
    lines.append("")
    lines.append(
        f"RESULT: alpha={ALPHA} lambda_p={LAMBDA_P} pop_size={POP_SIZE} "
        f"tournament_k={TOURNAMENT_K} seeds_found={len(expressions_found)}/5 "
        f"expressions={expressions_found}"
    )

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {path}", flush=True)
    return path


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    global_t0 = time.time()
    tag = param_tag()

    print("=" * 72, flush=True)
    print(f"GP Sensitivity Sweep: {tag}", flush=True)
    print(f"  alpha={ALPHA}  lambda_p={LAMBDA_P}  pop_size={POP_SIZE}  tournament_k={TOURNAMENT_K}", flush=True)
    print(f"  π/4 = {PI_OVER_4:.10f}", flush=True)
    print(f"  T_eval = {T_EVAL}", flush=True)
    print(f"  Terminals: {ALL_TERMINALS}", flush=True)
    print(f"  Leibniz injection: NONE", flush=True)
    print("=" * 72, flush=True)

    seed_vals = [42, 7, 137, 2718, 31415]
    seed_results = []

    for i, sv in enumerate(seed_vals):
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

    # Analyze
    for r in seed_results:
        r["analysis"] = analyze_result(r)

    expressions_found = []
    gens_found = []
    for r in seed_results:
        if r["analysis"].get("is_equivalent", False):
            expressions_found.append(r["best_expr"])
            gens_found.append(r["generations"])

    # Write output file
    write_sensitivity_txt(seed_results, expressions_found, gens_found)

    # Print summary line
    result_line = (
        f"RESULT: alpha={ALPHA} lambda_p={LAMBDA_P} pop_size={POP_SIZE} "
        f"tournament_k={TOURNAMENT_K} seeds_found={len(expressions_found)}/5 "
        f"expressions={expressions_found}"
    )
    print("", flush=True)
    print(result_line, flush=True)
    print(f"Total elapsed: {time.time() - global_t0:.1f}s", flush=True)
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
