#!/usr/bin/env python3
"""
Threshold sweep: Log-precision fitness, MIN_GAIN=2.0 (baseline is 0.5).

Fork of entropy_leibniz_v3_minimal.py with ONLY these changes:
- MIN_GAIN = 2.0 (instead of 0.5)
- Output filenames use threshold_mingain_2.0 prefix

All other parameters identical to entropy_leibniz_v3_minimal.py.

NOTE: Leibniz gains ~1.0 bit per checkpoint step (3.32 bits/decade over 10 pairs).
With MIN_GAIN=2.0, Leibniz monotonicity will be ~0, meaning W2 term contributes 0.
This tests whether discovery fails when the threshold exceeds Leibniz's actual gain rate.
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
MIN_GAIN = 2.0  # CHANGED from 0.5 baseline — exceeds Leibniz's per-step gain

# ── GP hyperparameters ────────────────────────────────────────────────────────
POP_SIZE = 1000
MAX_DEPTH = 6
MAX_NODES = 30
TOURNAMENT_K = 7
P_CROSS = 0.70
P_MUT = 0.20
N_ELITE = 5
PATIENCE = 100
DIV_INJECT = 100
WORST = -1e9
MAX_TOTAL = 1800.0
MAX_SEED = 360.0
N_SEEDS = 5
CHECKPOINT_INTERVAL = 50
LOG_INTERVAL = 10

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


# ── Entropy fitness function ──────────────────────────────────────────────────

def info_bits(error: float) -> float:
    if error < 1e-15:
        return INFO_CAP
    return -math.log2(error)


def compute_info_profile(tree, k_arr=None) -> list | None:
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
                        log(f"  [EARLY STOP] Gen {gen}: stable + converging (info={infos[-1]:.2f} bits)")
                        break
            best_unchanged = 0

    elapsed = time.time() - t0
    ti, mo, mr, ps, _ = entropy_components(best_ind)
    log(f"  Done: gen={gen}, fit={best_fit:.8f}, nc={best_ind.node_count()}, "
        f"ti={ti:.2f} mo={mo:.2f} mr={mr:.2f} t={elapsed:.1f}s\n  expr={best_ind.to_str()[:80]}")

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

    info_list = [infos[T] for T in T_CHECKPOINTS]
    is_mono = all(info_list[i + 1] >= info_list[i] for i in range(len(info_list) - 1))

    ti, mo, mr, ps, fit = entropy_components(ind)

    t_samples = sorted(set([1] + list(range(10, 201, 10)) + [500, 1000, 2000, 5000]))
    partial_sums = {T: round(float(cum[T - 1]), 8) for T in t_samples if T <= K_MAX}

    return {
        "errors": errors,
        "infos": infos,
        "is_equivalent": is_equiv,
        "is_monotone": is_mono,
        "monotonicity": mo,
        "mean_rate": mr,
        "total_info": ti,
        "partial_sums": partial_sums,
        "terms_20": [round(float(terms[k]), 8) for k in range(20)],
    }


# ── Output writers ────────────────────────────────────────────────────────────

def write_entropy_json(seed_results):
    data = {
        "config": {
            "pop_size": POP_SIZE, "w1": W1, "w2": W2, "w3": W3,
            "lambda_p": LAMBDA_P, "t_checkpoints": T_CHECKPOINTS, "n_seeds": N_SEEDS,
            "term_fixed": TERM_FIXED, "leibniz_injection": False, "min_gain": MIN_GAIN,
        },
        "pi_over_4": PI_OVER_4,
        "seeds": [
            {
                "seed": r["seed"],
                "seed_val": r["seed_val"],
                "generations": r["generations"],
                "best_fitness": round(r["best_fitness"], 8),
                "best_expr": r["best_expr"],
                "elapsed": r["elapsed"],
                "is_equivalent": r.get("analysis", {}).get("is_equivalent", False),
                "is_monotone": r.get("analysis", {}).get("is_monotone", False),
                "total_info": r.get("analysis", {}).get("total_info", 0.0),
                "monotonicity": r.get("analysis", {}).get("monotonicity", 0.0),
                "mean_rate": r.get("analysis", {}).get("mean_rate", 0.0),
                "history": r["history"],
            }
            for r in seed_results
        ],
    }

    path = OUT_DIR / "threshold_mingain_2.0_data.json"
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"  Wrote {path} ({path.stat().st_size / 1024:.1f} KB)", flush=True)


def write_convergence_csv(seed_results):
    rows = []
    for r in seed_results:
        for h in r["history"]:
            row = {"seed": r["seed"]}
            row.update(h)
            rows.append(row)
    if not rows:
        return
    path = OUT_DIR / "threshold_mingain_2.0_convergence.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {path}", flush=True)


def write_results_txt(seed_results, unit_report, eval_report, vv_report):
    W = 72
    header = "\n".join([
        "=" * W,
        "THRESHOLD SWEEP: LOG-PRECISION MIN_GAIN=2.0",
        f"Minimal terminal set {{k, 1, -1, 2}}, no injection, 30-min budget",
        "=" * W,
        "",
        f"Threshold parameter: MIN_GAIN = {MIN_GAIN} (baseline = 0.5)",
        f"  NOTE: Leibniz gains ~1.0 bit/step, so monotonicity will be ~0 with this threshold",
        f"  pop_size={POP_SIZE}, n_seeds={N_SEEDS}, max_total={MAX_TOTAL}s, max_seed={MAX_SEED}s",
        f"  W1={W1}, W2={W2}, W3={W3}, lambda_p={LAMBDA_P}",
    ])
    path = OUT_DIR / "threshold_mingain_2.0_results.txt"
    with open(path, "w") as f:
        f.write(header + "\n" + unit_report + "\n" + eval_report + "\n" + vv_report)
    print(f"  Wrote {path}", flush=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    global_t0 = time.time()
    print("=" * 72, flush=True)
    print(f"Threshold sweep: Log-precision MIN_GAIN={MIN_GAIN} (baseline=0.5)", flush=True)
    print(f"  NOTE: Leibniz ~1.0 bit/step — this threshold exceeds Leibniz's gain rate", flush=True)
    print(f"  Terminals: {ALL_TERMINALS}", flush=True)
    print("=" * 72, flush=True)

    lei = make_leibniz_tree()
    gp1 = make_gp1_best_tree()
    lei_fit = compute_fitness(lei)
    gp1_fit = compute_fitness(gp1)
    lei_ti, lei_mo, lei_mr, lei_ps, _ = entropy_components(lei)
    print(f"Leibniz fitness={lei_fit:.6f}  monotonicity={lei_mo:.3f} (expected ~0 with MIN_GAIN=2.0)", flush=True)
    unit_report = (f"Leibniz fitness={lei_fit:.6f}  GP-v1 fitness={gp1_fit:.6f}  "
                   f"Leibniz>GP-v1: {lei_fit > gp1_fit}  "
                   f"Leibniz monotonicity={lei_mo:.3f} (with MIN_GAIN={MIN_GAIN})")

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
    vv_report = ""
    write_entropy_json(seed_results)
    write_convergence_csv(seed_results)
    write_results_txt(seed_results, unit_report, eval_report, vv_report)

    prog = OUT_DIR / "progress.json"
    if prog.exists():
        prog.unlink()

    print(f"\nTotal elapsed: {time.time() - global_t0:.1f}s", flush=True)
    print(f"MIN_GAIN={MIN_GAIN}: {n_equiv}/{len(seed_results)} seeds found Leibniz", flush=True)
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
