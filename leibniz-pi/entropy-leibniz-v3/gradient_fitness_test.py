#!/usr/bin/env python3
"""
Gradient-based fitness test — thermodynamic selection variants.

Fork of entropy_leibniz_v3_minimal.py with:
- argparse: --approach (A, B, C, orig_pop2000) and --n_perturbations INT
- 15-terminal config: TERM_FIXED=["k",1,-1,2], EPHEMERALS=list(range(-5,6))
- MAX_SEED=360.0, MAX_TOTAL=1800.0, no injection

Approaches:
  A          - Pure gradient magnitude (negate, GP maximizes)
  B          - Hybrid: scalar entropy fitness × uniformity bonus
  C          - Min-component bottleneck
  orig_pop2000 - Original entropy fitness, POP_SIZE=2000 (coverage control)
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

# ── Parse args first ──────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description="Gradient-based GP fitness experiments")
parser.add_argument("--approach", type=str, default="A",
                    choices=["A", "B", "C", "orig_pop2000"],
                    help="Fitness approach to use")
parser.add_argument("--n_perturbations", type=int, default=5,
                    help="Number of perturbations for gradient estimation")
ARGS = parser.parse_args()

APPROACH = ARGS.approach
N_PERTURBATIONS = ARGS.n_perturbations

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
RATE_CAP = 5.0
MIN_GAIN = 0.5

# ── GP hyperparameters ────────────────────────────────────────────────────────
POP_SIZE = 2000 if APPROACH == "orig_pop2000" else 1000
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

# ── 15-terminal config ────────────────────────────────────────────────────────
FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
FNAMES = list(FUNC_ARITIES.keys())
TERM_FIXED = ["k", 1, -1, 2]
EPHEMERALS = list(range(-5, 6))
ALL_TERMINALS = TERM_FIXED + EPHEMERALS

# Result file per approach
RESULT_FILE = OUT_DIR / f"gradient_approach_{APPROACH}_results.txt"

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


# ── Info bits / profile ───────────────────────────────────────────────────────

def info_bits(error: float) -> float:
    if error < 1e-15:
        return INFO_CAP
    return -math.log2(error)


def compute_info_profile(tree, k_arr=None):
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


# ── Component vector ──────────────────────────────────────────────────────────

def compute_components(tree):
    infos = compute_info_profile(tree)
    if infos is None:
        return None
    total_info = infos[-1]
    n_gains = sum(1 for i in range(len(infos) - 1) if infos[i + 1] - infos[i] >= MIN_GAIN)
    monotonicity = n_gains / (len(infos) - 1)
    total_span = math.log10(T_CHECKPOINTS[-1] / T_CHECKPOINTS[0])
    mean_rate = (infos[-1] - infos[0]) / total_span if total_span > 0 else 0.0
    parsimony_eff = 1.0 - (tree.node_count() / MAX_NODES)
    return np.array([
        max(0.0, total_info / INFO_CAP),
        max(0.0, monotonicity),
        max(0.0, mean_rate / RATE_CAP),
        max(0.0, parsimony_eff)
    ])


# ── Gradient computation ──────────────────────────────────────────────────────

def compute_gradient(tree, n_perturb=5):
    V = compute_components(tree)
    if V is None:
        return None, None
    deltas = []
    for _ in range(n_perturb):
        mutant = mutate(tree.copy())
        Vm = compute_components(mutant)
        if Vm is not None:
            deltas.append(Vm - V)
    if not deltas:
        return 0.0, 0.0
    mean_grad = np.mean(deltas, axis=0)
    magnitude = float(np.linalg.norm(mean_grad))
    cv = float(np.std(np.abs(mean_grad)) / (np.mean(np.abs(mean_grad)) + 1e-10))
    return magnitude, cv


# ── Base entropy fitness (for approach B and orig_pop2000) ────────────────────

def compute_entropy_fitness_base(tree):
    infos = compute_info_profile(tree)
    if infos is None:
        return None, None, None

    total_info = infos[-1]
    n_gains = sum(1 for i in range(len(infos) - 1)
                  if infos[i + 1] - infos[i] >= MIN_GAIN)
    monotonicity = n_gains / (len(infos) - 1)
    total_span = math.log10(T_CHECKPOINTS[-1] / T_CHECKPOINTS[0])
    mean_rate = (total_info - infos[0]) / total_span if total_span > 0 else 0.0
    return total_info, monotonicity, mean_rate


# ── Fitness function (approach-specific) ──────────────────────────────────────

def compute_fitness(tree) -> float:
    key = (APPROACH, tree.to_str())
    if key in _fitness_cache:
        return _fitness_cache[key]

    result = _compute_fitness_inner(tree)
    _fitness_cache[key] = result
    return result


def _compute_fitness_inner(tree) -> float:
    if APPROACH == "A":
        # Pure gradient magnitude — negate so GP maximizes
        magnitude, cv = compute_gradient(tree, N_PERTURBATIONS)
        if magnitude is None:
            return WORST
        fitness = -magnitude - LAMBDA_P * tree.node_count()
        return fitness

    elif APPROACH == "B":
        # Hybrid: scalar entropy fitness × uniformity bonus
        total_info, monotonicity, mean_rate = compute_entropy_fitness_base(tree)
        if total_info is None:
            return WORST
        base_fitness = (W1 * (total_info / INFO_CAP) + W2 * monotonicity
                        + W3 * (mean_rate / RATE_CAP) - LAMBDA_P * tree.node_count())
        magnitude, cv = compute_gradient(tree, N_PERTURBATIONS)
        if magnitude is None:
            return base_fitness
        uniformity_bonus = 1.0 / (1.0 + cv)
        fitness = base_fitness * uniformity_bonus
        return fitness

    elif APPROACH == "C":
        # Min-component bottleneck
        V = compute_components(tree)
        if V is None:
            return WORST
        fitness = float(np.min(V)) - LAMBDA_P * tree.node_count()
        return fitness

    elif APPROACH == "orig_pop2000":
        # Original entropy fitness (same as minimal script), POP_SIZE=2000
        infos = compute_info_profile(tree)
        if infos is None:
            return WORST
        total_info = infos[-1]
        n_gains = sum(1 for i in range(len(infos) - 1)
                      if infos[i + 1] - infos[i] >= MIN_GAIN)
        monotonicity = n_gains / (len(infos) - 1)
        total_span = math.log10(T_CHECKPOINTS[-1] / T_CHECKPOINTS[0])
        mean_rate = (total_info - infos[0]) / total_span if total_span > 0 else 0.0
        parsimony = LAMBDA_P * tree.node_count()
        fitness = (W1 * total_info / INFO_NORM + W2 * monotonicity
                   + W3 * mean_rate / RATE_NORM - parsimony)
        return fitness

    return WORST


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


def make_wrong_limit_tree():
    """5 / (((1 + 5) + (k * 4)) * (k + -2))
    Manually built: add(1,5)=6, add(6, mul(k,4)) = 6+4k, mul that by (k+-2)=(k-2), div 5 by it.
    """
    inner_left = Node(op="add", children=[
        Node(value=1),
        Node(value=5),
    ])  # 1+5 = 6
    inner_right = Node(op="mul", children=[
        Node(value="k"),
        Node(value=4),
    ])  # k*4
    denominator_left = Node(op="add", children=[inner_left, inner_right])  # (1+5)+(k*4) = 6+4k
    denominator_right = Node(op="add", children=[
        Node(value="k"),
        Node(value=-2),
    ])  # k+(-2) = k-2
    denominator = Node(op="mul", children=[denominator_left, denominator_right])  # (6+4k)*(k-2)
    tree = Node(op="div", children=[Node(value=5), denominator])  # 5 / ((6+4k)*(k-2))
    return tree


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


# ── Calibration check ─────────────────────────────────────────────────────────

def run_calibration():
    lines = []
    W = 72
    lines.append("=" * W)
    lines.append(f"CALIBRATION CHECK — Approach {APPROACH}")
    lines.append("=" * W)

    leibniz = make_leibniz_tree()
    wrong_limit = make_wrong_limit_tree()
    zero_const = Node(value=0)

    lei_fit = compute_fitness(leibniz)
    wl_fit = compute_fitness(wrong_limit)
    zero_fit = compute_fitness(zero_const)

    # Also compute entropy components for context
    lei_ti, lei_mo, lei_mr, lei_ps, lei_ent = entropy_components(leibniz)
    wl_ti, wl_mo, wl_mr, wl_ps, wl_ent = entropy_components(wrong_limit)
    zero_ti, zero_mo, zero_mr, zero_ps, zero_ent = entropy_components(zero_const)

    # Gradient diagnostics
    lei_mag, lei_cv = compute_gradient(leibniz, N_PERTURBATIONS)
    wl_mag, wl_cv = compute_gradient(wrong_limit, N_PERTURBATIONS)
    zero_mag, zero_cv = compute_gradient(zero_const, N_PERTURBATIONS)

    lines.append(f"\nFitness under Approach {APPROACH}:")
    lines.append(f"  {'Tree':<30} {'Fitness':>12}  {'Entropy':>10}  {'Mag':>8}  {'CV':>8}")
    lines.append("  " + "-" * 70)

    def fmt_val(v):
        if v is None:
            return "    None"
        return f"{v:8.4f}"

    lines.append(f"  {'Leibniz (-1)^k/(2k+1)':<30} {lei_fit:12.6f}  {lei_ent:10.6f}  "
                 f"{fmt_val(lei_mag)}  {fmt_val(lei_cv)}")
    lines.append(f"  {'Wrong-limit 5/((6+4k)(k-2))':<30} {wl_fit:12.6f}  {wl_ent:10.6f}  "
                 f"{fmt_val(wl_mag)}  {fmt_val(wl_cv)}")
    lines.append(f"  {'Zero constant (0)':<30} {zero_fit:12.6f}  {zero_ent:10.6f}  "
                 f"{fmt_val(zero_mag)}  {fmt_val(zero_cv)}")

    leibniz_beats_wl = lei_fit > wl_fit
    lines.append(f"\nLeibniz beats wrong-limit attractor: {leibniz_beats_wl}")
    if leibniz_beats_wl:
        lines.append(f"  Margin: {lei_fit - wl_fit:.6f}")
    else:
        lines.append(f"  PROBLEM: wrong-limit has higher fitness by {wl_fit - lei_fit:.6f}")

    lines.append(f"\nEntropy components (for reference):")
    lines.append(f"  {'Tree':<30} {'ti':>8}  {'mono':>6}  {'rate':>8}  {'parsimony':>9}")
    lines.append("  " + "-" * 65)
    lines.append(f"  {'Leibniz':<30} {lei_ti:8.3f}  {lei_mo:6.3f}  {lei_mr:8.3f}  {lei_ps:9.4f}")
    lines.append(f"  {'Wrong-limit':<30} {wl_ti:8.3f}  {wl_mo:6.3f}  {wl_mr:8.3f}  {wl_ps:9.4f}")
    lines.append(f"  {'Zero constant':<30} {zero_ti:8.3f}  {zero_mo:6.3f}  {zero_mr:8.3f}  {zero_ps:9.4f}")

    lines.append("")

    report = "\n".join(lines)
    print(report, flush=True)

    return {
        "leibniz_fit": lei_fit,
        "wrong_limit_fit": wl_fit,
        "zero_fit": zero_fit,
        "leibniz_beats_wl": leibniz_beats_wl,
        "leibniz_mag": lei_mag,
        "leibniz_cv": lei_cv,
        "wrong_limit_mag": wl_mag,
        "wrong_limit_cv": wl_cv,
        "zero_mag": zero_mag,
        "zero_cv": zero_cv,
        "lei_entropy": lei_ent,
        "wl_entropy": wl_ent,
        "zero_entropy": zero_ent,
    }, report


# ── GP main loop ──────────────────────────────────────────────────────────────

def run_seed(seed_idx, seed_val, max_time, global_t0):
    global _fitness_cache
    t0 = time.time()
    random.seed(seed_val)
    np.random.seed(seed_val)

    log = lambda s: print(s, flush=True)
    log(f"\n── Seed {seed_idx} (val={seed_val}, budget={max_time:.0f}s, approach={APPROACH}) ──")

    sample = ramped_h_h(min(50, POP_SIZE))
    t_check = time.time()
    for ind in sample:
        compute_fitness(ind)
    t_per_ind = (time.time() - t_check) / len(sample)
    est_per_gen = t_per_ind * POP_SIZE * 1.5
    log(f"  Perf check: {t_per_ind*1000:.2f}ms/ind, ~{est_per_gen*1000:.0f}ms/gen → "
        f"~{int(max_time / max(est_per_gen, 1e-6))} gens")

    # NO injection — pure random initialization
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
            ti, mo, mr, ps, ent_fit = entropy_components(best_ind)
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
            with open(OUT_DIR / f"progress_{APPROACH}.json", "w") as f:
                json.dump({
                    "approach": APPROACH,
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
    ti, mo, mr, ps, ent_fit = entropy_components(best_ind)
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


# ── Result writing ────────────────────────────────────────────────────────────

def write_results(seed_results, calib_data, calib_report):
    W = 72
    lines = []
    lines.append("=" * W)
    lines.append(f"GRADIENT FITNESS TEST — Approach {APPROACH}")
    lines.append(f"n_perturbations={N_PERTURBATIONS}, pop_size={POP_SIZE}")
    lines.append(f"15 terminals: {ALL_TERMINALS}")
    lines.append("=" * W)
    lines.append("")

    lines.append(calib_report)

    lines.append("=" * W)
    lines.append("GP RESULTS — Per Seed")
    lines.append("=" * W)

    n_equiv = 0
    best_fits = []

    for r in seed_results:
        ana = r.get("analysis", {})
        is_eq = ana.get("is_equivalent", False)
        if is_eq:
            n_equiv += 1
        best_fits.append(r["best_fitness"])

        lines.append(f"\nSeed {r['seed']} (val={r['seed_val']}):")
        lines.append(f"  Gens: {r['generations']}  Elapsed: {r['elapsed']:.1f}s")
        lines.append(f"  Expression : {r['best_expr']}")
        lines.append(f"  Nodes      : {r['best_ind'].node_count()}")
        lines.append(f"  Fitness (approach {APPROACH}): {r['best_fitness']:.8f}")

        ti, mo, mr, ps, ent_fit = entropy_components(r["best_ind"])
        lines.append(f"  Entropy fitness (for reference): {ent_fit:.8f}")
        lines.append(f"  Components: ti={ti:.4f} mo={mo:.4f} mr={mr:.4f} ps={ps:.4f}")

        infos = ana.get("infos", {})
        errors = ana.get("errors", {})
        lines.append(f"  Info profile (bits):")
        for T in [10, 100, 1000, 5000, 10000]:
            i_val = infos.get(T, "?")
            e_val = errors.get(T, "?")
            lines.append(f"    T={T:>6}: {str(i_val):>10} bits, error={str(e_val):>14}")

        lines.append(f"  Equivalent to Leibniz : {is_eq}")
        lines.append(f"  Monotone info profile : {ana.get('is_monotone', False)}")

    lines.append("\n" + "─" * W)
    lines.append("AGGREGATE:")
    if best_fits:
        lines.append(f"  Seeds finding Leibniz: {n_equiv}/{len(seed_results)}")
        lines.append(f"  Mean best fitness    : {sum(best_fits)/len(best_fits):.8f}")
        lines.append(f"  Best (any seed)      : {max(best_fits):.8f}")

    with open(RESULT_FILE, "w") as f:
        f.write("\n".join(lines))
    print(f"  Wrote {RESULT_FILE}", flush=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    global_t0 = time.time()
    print("=" * 72, flush=True)
    print(f"Gradient Fitness Test — Approach {APPROACH}", flush=True)
    print(f"  n_perturbations={N_PERTURBATIONS}, pop_size={POP_SIZE}", flush=True)
    print(f"  15 terminals: {ALL_TERMINALS}", flush=True)
    print(f"  MAX_SEED={MAX_SEED}s, MAX_TOTAL={MAX_TOTAL}s, no injection", flush=True)
    print("=" * 72, flush=True)

    print("\n[1/4] Calibration check ...", flush=True)
    calib_data, calib_report = run_calibration()

    print("\n[2/4] GP experiment ...", flush=True)
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

    print("\n[3/4] Analyzing ...", flush=True)
    for r in seed_results:
        r["analysis"] = analyze_result(r)

    print("\n[4/4] Writing results ...", flush=True)
    write_results(seed_results, calib_data, calib_report)

    # Clean up progress file
    prog = OUT_DIR / f"progress_{APPROACH}.json"
    if prog.exists():
        prog.unlink()

    n_equiv = sum(1 for r in seed_results
                  if r.get("analysis", {}).get("is_equivalent", False))
    print(f"\nApproach {APPROACH}: {n_equiv}/{len(seed_results)} seeds found Leibniz", flush=True)
    print(f"Total elapsed: {time.time() - global_t0:.1f}s", flush=True)
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
