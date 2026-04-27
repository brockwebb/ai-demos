#!/usr/bin/env python3
"""
Threshold sweep: Convergence-aware fitness, convergence_threshold=0.01 (1%).
Baseline is 0.05 (5%), implemented as errors[i+1] < errors[i] * 0.95.

Fork of gp_leibniz_v3_minimal.py with ONLY these changes:
- Convergence bonus threshold: 0.95 → 0.99 (requires only 1% error reduction)
- Output filenames use threshold_convaware_0.01 prefix

All other parameters identical to gp_leibniz_v3_minimal.py.
"""

import json
import csv
import time
import math
import random
import sys
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).parent
PI_OVER_4 = math.pi / 4

# ── Evaluation setup ──────────────────────────────────────────────────────────
K_MAX = 5000
K_ARRAY = np.arange(K_MAX, dtype=float)
T_EVAL = [10, 50, 200, 1000, 5000]

LEIBNIZ_REFS = {T: sum((-1) ** k / (2 * k + 1) for k in range(T)) for T in T_EVAL + [10000]}

# ── GP hyperparameters ────────────────────────────────────────────────────────
POP_SIZE = 1000
MAX_DEPTH = 6
MAX_NODES = 30
TOURNAMENT_K = 7
P_CROSS = 0.70
P_MUT = 0.20
N_ELITE = 5
ALPHA = 0.05
LAMBDA_P = 0.005
PATIENCE = 100
STOP_THRESH = 0.001
DIV_INJECT = 100
WORST = -1e9
MAX_TOTAL = 1800.0
MAX_SEED = 360.0
N_SEEDS = 5
CHECKPOINT_INTERVAL = 50
LOG_INTERVAL = 10

# Convergence threshold: fraction the next error must be below the current
# 0.99 means 1% reduction required (baseline is 0.95 = 5% reduction)
CONV_THRESHOLD = 0.99  # CHANGED from 0.95 baseline

# Primitives
FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
FNAMES = list(FUNC_ARITIES.keys())
TERM_FIXED = ["k", 1, -1, 2]
EPHEMERALS = []
ALL_TERMINALS = TERM_FIXED + EPHEMERALS

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


# ── Fitness function ──────────────────────────────────────────────────────────

def compute_fitness(tree):
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

    # CHANGED: CONV_THRESHOLD=0.99 instead of 0.95 (1% reduction instead of 5%)
    n_improving = sum(
        1 for i in range(len(errors) - 1)
        if errors[i + 1] < errors[i] * CONV_THRESHOLD
    )
    conv_bonus = n_improving / (len(errors) - 1)

    parsimony = LAMBDA_P * tree.node_count()

    fitness = accuracy + ALPHA * conv_bonus - parsimony
    _fitness_cache[key] = fitness
    return fitness


def fitness_components(tree):
    terms = safe_eval(tree)
    if terms is None:
        return (WORST, 0.0, 0.0, WORST)
    cum = np.cumsum(terms)
    errors = [abs(float(cum[T - 1]) - PI_OVER_4) for T in T_EVAL]
    accuracy = -float(np.mean(errors))
    # CHANGED: CONV_THRESHOLD=0.99
    n_improving = sum(1 for i in range(len(errors) - 1) if errors[i + 1] < errors[i] * CONV_THRESHOLD)
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
    return Node(op="div", children=[
        Node(op="pow", children=[Node(value=-1), Node(value="k")]),
        Node(op="add", children=[
            Node(op="mul", children=[Node(value=2), Node(value="k")]),
            Node(value=1),
        ]),
    ])


def make_gp1_best_tree():
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
            with open(OUT_DIR / "progress.json", "w") as f:
                json.dump({
                    "seed": seed_idx,
                    "generation": gen,
                    "best_fitness": best_fit,
                    "best_expr": best_ind.to_str(),
                    "elapsed": round(elapsed, 2),
                    "remaining": round(max_time - elapsed, 2),
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

    error_list = [errors[T] for T in T_EVAL]
    is_monotone = all(error_list[i + 1] < error_list[i] for i in range(len(error_list) - 1))

    acc, cb, ps, _ = fitness_components(ind)

    t_samples = sorted(set([1] + list(range(10, 201, 10)) + [500, 1000, 2000, 5000]))
    partial_sums = {T: round(float(cum[T - 1]), 8) for T in t_samples if T <= K_MAX}

    return {
        "errors": errors,
        "is_equivalent": is_equiv,
        "is_monotone_converging": is_monotone,
        "accuracy": acc,
        "conv_bonus": cb,
        "partial_sums": partial_sums,
        "terms_20": [round(float(terms[k]), 8) for k in range(20)],
    }


# ── Output writers ────────────────────────────────────────────────────────────

def write_evolution_json(seed_results):
    data = {
        "config": {
            "pop_size": POP_SIZE, "max_depth": MAX_DEPTH, "max_nodes": MAX_NODES,
            "tournament_k": TOURNAMENT_K, "p_cross": P_CROSS, "p_mut": P_MUT,
            "n_elite": N_ELITE, "alpha": ALPHA, "lambda_p": LAMBDA_P,
            "t_eval": T_EVAL, "n_seeds": N_SEEDS,
            "term_fixed": TERM_FIXED, "ephemerals": EPHEMERALS,
            "leibniz_injection": False,
            "conv_threshold": CONV_THRESHOLD,
            "conv_threshold_pct": round((1 - CONV_THRESHOLD) * 100, 1),
        },
        "pi_over_4": PI_OVER_4,
        "seeds": [
            {
                "seed": r["seed"],
                "generations": r["generations"],
                "best_fitness": round(r["best_fitness"], 8),
                "best_expr": r["best_expr"],
                "elapsed": r["elapsed"],
                "is_equivalent": r.get("analysis", {}).get("is_equivalent", False),
                "is_monotone": r.get("analysis", {}).get("is_monotone_converging", False),
                "conv_bonus": r.get("analysis", {}).get("conv_bonus", 0.0),
                "errors": {str(T): v for T, v in r.get("analysis", {}).get("errors", {}).items()},
                "history": r["history"],
            }
            for r in seed_results
        ],
    }

    path = OUT_DIR / "threshold_convaware_0.01_data.json"
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"  Wrote {path} ({path.stat().st_size / 1024:.1f} KB)", flush=True)


def write_convergence_csv(seed_results):
    rows = []
    for r in seed_results:
        for h in r["history"]:
            row = {"seed": r["seed"]}
            row.update(h)
            if "terms_t10" in row:
                row["terms_t10"] = json.dumps(row["terms_t10"])
            rows.append(row)
    if not rows:
        return
    path = OUT_DIR / "threshold_convaware_0.01_convergence.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {path}", flush=True)


def write_results_txt(seed_results, unit_report, eval_report):
    W = 72
    header = "\n".join([
        "=" * W,
        "THRESHOLD SWEEP: CONVERGENCE-AWARE, THRESHOLD=0.01 (1%)",
        f"Minimal terminal set {{k, 1, -1, 2}}, no injection, 30-min budget",
        "=" * W,
        "",
        f"Threshold parameter: CONV_THRESHOLD = {CONV_THRESHOLD} (1% reduction required)",
        f"  Baseline: 0.95 (5% reduction required)",
        f"  Lower threshold is less selective — more consecutive pairs qualify",
        f"  pop_size={POP_SIZE}, n_seeds={N_SEEDS}, max_total={MAX_TOTAL}s, max_seed={MAX_SEED}s",
        f"  alpha={ALPHA}, lambda_p={LAMBDA_P}",
        "",
        "Fitness: accuracy + alpha*conv_bonus - lambda*nodes",
        f"  conv_bonus = fraction of T-pairs with errors[i+1] < errors[i] * {CONV_THRESHOLD}",
    ])
    path = OUT_DIR / "threshold_convaware_0.01_results.txt"
    with open(path, "w") as f:
        f.write(header + "\n" + unit_report + "\n" + eval_report)
    print(f"  Wrote {path}", flush=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    global_t0 = time.time()
    print("=" * 72, flush=True)
    print(f"Threshold sweep: Conv-aware CONV_THRESHOLD={CONV_THRESHOLD} (1% reduction, baseline=0.95/5%)", flush=True)
    print(f"  Terminals: {ALL_TERMINALS}", flush=True)
    print("=" * 72, flush=True)

    lei = make_leibniz_tree()
    gp1 = make_gp1_best_tree()
    lei_fit = compute_fitness(lei)
    gp1_fit = compute_fitness(gp1)
    unit_report = (f"Leibniz fitness={lei_fit:.6f}  GP-v1 fitness={gp1_fit:.6f}  "
                   f"Leibniz>GP-v1: {lei_fit > gp1_fit}")
    print(unit_report, flush=True)

    seed_results = []
    seed_vals = [42, 7, 137, 2718, 31415]

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

    for r in seed_results:
        r["analysis"] = analyze_result(r)

    n_equiv = sum(1 for r in seed_results if r.get("analysis", {}).get("is_equivalent", False))
    print(f"\nSeeds finding Leibniz: {n_equiv}/{len(seed_results)}", flush=True)
    for r in seed_results:
        ana = r.get("analysis", {})
        print(f"  Seed {r['seed']} (val={r['seed_val']}): equiv={ana.get('is_equivalent', False)} "
              f"fit={r['best_fitness']:.6f} expr={r['best_expr'][:60]}", flush=True)

    eval_report = f"Seeds finding Leibniz: {n_equiv}/{len(seed_results)}"
    write_evolution_json(seed_results)
    write_convergence_csv(seed_results)
    write_results_txt(seed_results, unit_report, eval_report)

    prog = OUT_DIR / "progress.json"
    if prog.exists():
        prog.unlink()

    print(f"\nTotal elapsed: {time.time() - global_t0:.1f}s", flush=True)
    print(f"CONV_THRESHOLD={CONV_THRESHOLD}: {n_equiv}/{len(seed_results)} seeds found Leibniz", flush=True)
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
