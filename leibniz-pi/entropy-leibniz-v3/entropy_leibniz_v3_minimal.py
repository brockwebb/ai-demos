#!/usr/bin/env python3
"""
Entropy-Leibniz v3 minimal: Information-theoretic fitness, minimal terminal set, no injection.

Fork of entropy_leibniz.py with ONLY these changes:
- TERM_FIXED = ["k", 1, -1, 2]  (no ephemerals)
- EPHEMERALS = []
- MAX_TOTAL = 1800.0
- MAX_SEED = 360.0
- Output filenames use _minimal suffix
- NO Leibniz injection in population initialization

Tests whether the entropy fitness can rediscover Leibniz from a minimal
terminal set {k, 1, -1, 2} without the crutch of injecting Leibniz
at generation 0.
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
MIN_GAIN = 0.5

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


# ── TEVV ──────────────────────────────────────────────────────────────────────

def run_unit_tests():
    W = 72
    lines = ["=" * W, "T — UNIT TESTS (Entropy v3 minimal)", "=" * W]
    passed = failed = 0

    def check(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            lines.append(f"  [PASS] {name}")
        else:
            failed += 1
            lines.append(f"  [FAIL] {name}" + (f": {detail}" if detail else ""))

    lines.append("\n  ── Info Bits Computation ──")
    check("-log2(0.025) ≈ 5.32",
          abs(info_bits(0.025) - 5.321928) < 0.0001,
          f"got {info_bits(0.025):.6f}")
    check("error=0 → info=50 (capped)",
          info_bits(0.0) == INFO_CAP,
          f"got {info_bits(0.0)}")
    check("error=1.0 → info=0.0",
          abs(info_bits(1.0) - 0.0) < 1e-10,
          f"got {info_bits(1.0):.6f}")

    lines.append("\n  ── Terminal set (v3 minimal) ──")
    lines.append(f"  TERM_FIXED = {TERM_FIXED}")
    lines.append(f"  EPHEMERALS = {EPHEMERALS}")
    lines.append(f"  ALL_TERMINALS = {ALL_TERMINALS}")
    check("Exactly 4 terminals", len(ALL_TERMINALS) == 4,
          f"got {len(ALL_TERMINALS)}: {ALL_TERMINALS}")
    check("Terminals are k, 1, -1, 2",
          set(ALL_TERMINALS) == {"k", 1, -1, 2},
          f"got {ALL_TERMINALS}")

    lines.append("\n  ── Tree Primitives ──")
    k5 = np.array([0., 1., 2., 3., 4.])
    leibniz = make_leibniz_tree()
    gp1_best = make_gp1_best_tree()

    n_div = Node(op="div", children=[Node(value=1), Node(value=0)])
    check("div(1,0) → 1.0",
          np.isscalar(evaluate_tree(n_div, k5)) and evaluate_tree(n_div, k5) == 1.0)

    n_pow = Node(op="pow", children=[Node(value=-1), Node(value="k")])
    res = safe_eval(n_pow, k5)
    check("pow(-1,k) = [1,-1,1,-1,1]",
          res is not None and np.allclose(res, [1., -1., 1., -1., 1.]))

    lei_terms = safe_eval(leibniz, np.arange(10, dtype=float))
    expected = np.array([(-1) ** k / (2 * k + 1) for k in range(10)])
    check("Leibniz tree k=0..9 correct",
          lei_terms is not None and np.allclose(lei_terms, expected, atol=1e-10))

    lines.append("\n  ── Fitness Calibration ──")
    lei_fit = compute_fitness(leibniz)
    gp1_fit = compute_fitness(gp1_best)
    lines.append(f"  Leibniz fitness  : {lei_fit:.6f}")
    lines.append(f"  GP v1 best fitness: {gp1_fit:.6f}")
    lei_ti, lei_mo, lei_mr, lei_ps, _ = entropy_components(leibniz)
    gp1_ti, gp1_mo, gp1_mr, gp1_ps, _ = entropy_components(gp1_best)
    lines.append(f"    Leibniz : ti={lei_ti:.3f} mo={lei_mo:.2f} mr={lei_mr:.3f} ps={lei_ps:.4f}")
    lines.append(f"    GP v1   : ti={gp1_ti:.3f} mo={gp1_mo:.2f} mr={gp1_mr:.3f} ps={gp1_ps:.4f}")
    check(f"Leibniz ({lei_fit:.4f}) beats GP v1 ({gp1_fit:.4f})",
          lei_fit > gp1_fit, f"margin={lei_fit - gp1_fit:.4f}")
    check("Leibniz monotonicity = 1.0", abs(lei_mo - 1.0) < 0.01, f"got {lei_mo}")
    check("GP v1 monotonicity < 0.25", gp1_mo < 0.25, f"got {gp1_mo}")

    ok = True
    for _ in range(50):
        t = make_random_tree()
        if t.node_count() > MAX_NODES or t.depth() > MAX_DEPTH + 1:
            ok = False
            break
    check("50 random trees within constraints", ok)

    t1, t2 = make_leibniz_tree(), make_random_tree(3)
    c1, c2 = crossover(t1, t2)
    check("Crossover valid sizes",
          c1.node_count() <= MAX_NODES and c2.node_count() <= MAX_NODES)
    check("Mutation valid size",
          mutate(make_leibniz_tree()).node_count() <= MAX_NODES)

    random.seed(0)
    sample = ramped_h_h(100)
    sample_fits = sorted([compute_fitness(ind) for ind in sample], reverse=True)
    pct90 = sample_fits[9]
    check(f"Leibniz ({lei_fit:.4f}) in top 10% of random pop (≥{pct90:.4f})",
          lei_fit >= pct90)

    lines.append(f"\n  Results: {passed} passed, {failed} failed")
    return "\n".join(lines), passed, failed


def run_eval_report(seed_results):
    W = 72
    lines = ["\n" + "=" * W, "E — EVALUATION (per seed)", "=" * W]

    any_equiv = any_struct = any_mono = False
    best_fits = []

    for r in seed_results:
        ana = r.get("analysis", {})
        lines.append(f"\nSeed {r['seed']} (val={r['seed_val']}):")
        lines.append(f"  Gens: {r['generations']}  Elapsed: {r['elapsed']:.1f}s")
        lines.append(f"  Expression : {r['best_expr']}")
        lines.append(f"  Nodes      : {r['best_ind'].node_count()}")
        lines.append(f"  Fitness    : {r['best_fitness']:.8f}")

        ti, mo, mr, ps, total = entropy_components(r["best_ind"])
        lines.append(f"  Components : {W1}×(ti/50)={W1*ti/50:.6f} + {W2}×mo={W2*mo:.6f} "
                     f"+ {W3}×(mr/5)={W3*mr/5:.6f} - ps={ps:.6f} = {total:.6f}")
        lines.append(f"  Total info : {ti:.4f} bits at T=10000")
        lines.append(f"  Monotonicity: {mo:.4f}  Mean rate: {mr:.4f} bits/decade")

        infos = ana.get("infos", {})
        errors = ana.get("errors", {})
        lines.append(f"\n  Information profile (bits of precision about π/4):")
        lines.append(f"  {'T':>6}  {'info (bits)':>12}  {'error':>12}  {'Leibniz bits':>12}")
        lines.append("  " + "─" * 50)
        for T in T_CHECKPOINTS:
            i_val = infos.get(T)
            e_val = errors.get(T)
            lei_e = abs(LEIBNIZ_REFS.get(T, 0) - PI_OVER_4)
            lei_i = round(info_bits(lei_e), 2)
            if i_val is not None and e_val is not None:
                lines.append(f"  {T:>6}  {i_val:>12.4f}  {e_val:>12.8f}  {lei_i:>12.4f}")
            else:
                lines.append(f"  {T:>6}  {'diverges':>12}  {'diverges':>12}  {lei_i:>12.4f}")

        is_eq = ana.get("is_equivalent", False)
        is_st = ana.get("is_structural", False)
        is_mn = ana.get("is_monotone", False)
        lines.append(f"\n  Equivalent to Leibniz  : {is_eq}")
        lines.append(f"  Structural resemblance : {is_st}")
        lines.append(f"  Monotone info profile  : {is_mn}")
        if is_eq: any_equiv = True
        if is_st: any_struct = True
        if is_mn: any_mono = True
        best_fits.append(r["best_fitness"])

    lines.append("\n" + "─" * W)
    lines.append("Aggregate:")
    if best_fits:
        lines.append(f"  Mean best fitness  : {sum(best_fits)/len(best_fits):.8f}")
        lines.append(f"  Best (any seed)    : {max(best_fits):.8f}")
    lines.append(f"  Any equiv Leibniz  : {any_equiv}")
    lines.append(f"  Any structural     : {any_struct}")
    lines.append(f"  Any monotone info  : {any_mono}")
    return "\n".join(lines)


def run_vv_report(seed_results):
    W = 72
    lines = ["\n" + "=" * W, "V — VERIFICATION", "=" * W]

    leibniz = make_leibniz_tree()
    gp1 = make_gp1_best_tree()
    lei_fit = compute_fitness(leibniz)
    gp1_fit = compute_fitness(gp1)
    lines.append(f"\nFitness under entropy minimal function:")
    lines.append(f"  Leibniz : {lei_fit:.6f}")
    lines.append(f"  GP v1   : {gp1_fit:.6f}")
    lines.append(f"  Margin  : {lei_fit - gp1_fit:.6f}")

    random.seed(0)
    sample = ramped_h_h(100)
    sample_fits = sorted([compute_fitness(ind) for ind in sample], reverse=True)
    lines.append(f"\nLeibniz rank vs random-100: {lei_fit:.4f} ≥ p90={sample_fits[9]:.4f}: "
                 f"{lei_fit >= sample_fits[9]}")

    lines.append("\n" + "=" * W)
    lines.append("V — VALIDATION")
    lines.append("=" * W)

    best_r = max(seed_results, key=lambda r: r["best_fitness"])
    ana = best_r.get("analysis", {})
    errs = ana.get("errors", {})
    infos = ana.get("infos", {})

    lines.append(f"\nBest seed: {best_r['seed']}  Gens: {best_r['generations']}")
    lines.append(f"  Expression: {best_r['best_expr']}")
    lines.append(f"  T=5000 error: {errs.get(5000, 'N/A')}")
    lines.append(f"  T=5000 info : {infos.get(5000, 'N/A')} bits")

    e10k = errs.get(10000)
    e20k = errs.get(20000)
    if e10k is not None:
        lines.append(f"  T=10000 error: {e10k:.8f}  info: {infos.get(10000, '?')} bits")
    else:
        lines.append(f"  T=10000: diverges")
    if e20k is not None:
        lines.append(f"  T=20000 error: {e20k:.8f}  (still converging: {e20k < (e10k or 1e9):.0f})")
    else:
        lines.append(f"  T=20000: diverges")

    is_mn = ana.get("is_monotone", False)
    lines.append(f"  Monotone info profile: {is_mn}")

    lines.append("\n" + "─" * W)
    lines.append("Cross-experiment comparison:")
    lines.append(f"  {'Method':<16} {'info@T=10':>10} {'info@T=1k':>10} "
                 f"{'info@T=5k':>10} {'mono?':>7} {'rate':>6}  Notes")
    lines.append("  " + "─" * 72)

    prior_methods = [
        ("RL v1",         4.3,   None,  None, False, "~0.0",  "Diverges T>10"),
        ("RL v2",         4.3,   None,  None, False, "~0.0",  "Diverges T>20"),
        ("ACO",           14.1,  None,  None, False, "~0.0",  "Collapses T>40"),
        ("GP v1",         11.44, 11.44, 11.44, False, "~0.0", "Flatlines (wrong limit)"),
        ("GP v2",         4.4,   10.97, 14.29, True,  "~3.32","5/5 Leibniz (with injection)"),
        ("Entropy",       4.4,   10.97, 14.29, True,  "~3.32","5/5 Leibniz (with injection)"),
        ("GP v3 wide",    None,  None,  None, False, "N/A",   "0/5 no injection"),
        ("Entropy v3 wide",None, None,  None, False, "N/A",   "0/5 no injection"),
        ("GP v3 hostile", None,  None,  None, False, "N/A",   "0/5 no injection"),
        ("Entr v3 hostile",None, None,  None, False, "N/A",   "0/5 no injection"),
    ]
    for name, i10, i1k, i5k, mono, rate, note in prior_methods:
        i10s = f"{i10:.2f}" if i10 is not None else "N/A"
        i1ks = f"{i1k:.2f}" if i1k is not None else "N/A"
        i5ks = f"{i5k:.2f}" if i5k is not None else "N/A"
        lines.append(f"  {name:<16} {i10s:>10} {i1ks:>10} {i5ks:>10} {str(mono):>7} {rate:>6}  {note}")

    this_i10 = infos.get(10)
    this_i1k = infos.get(1000)
    this_i5k = infos.get(5000)
    this_mono = ana.get("is_monotone", False)
    this_mr = round(ana.get("mean_rate", 0.0), 2)
    i10s = f"{this_i10:.2f}" if this_i10 is not None else "N/A"
    i1ks = f"{this_i1k:.2f}" if this_i1k is not None else "N/A"
    i5ks = f"{this_i5k:.2f}" if this_i5k is not None else "N/A"
    note = "Leibniz found!" if ana.get("is_equivalent", False) else "See results"
    lines.append(f"  {'Entr v3 minimal':<16} {i10s:>10} {i1ks:>10} {i5ks:>10} "
                 f"{str(this_mono):>7} {str(this_mr):>6}  {note}")

    lines.append("\n" + "=" * W)
    lines.append("V — VERDICT")
    lines.append("=" * W)
    any_equiv = any(r.get("analysis", {}).get("is_equivalent", False) for r in seed_results)
    any_mono_info = any(r.get("analysis", {}).get("is_monotone", False) for r in seed_results)
    lines.append(f"  Found Leibniz equivalent : {any_equiv}")
    lines.append(f"  Found monotone info profile: {any_mono_info}")
    n_equiv = sum(1 for r in seed_results if r.get("analysis", {}).get("is_equivalent", False))
    lines.append(f"  Seeds finding Leibniz: {n_equiv}/{len(seed_results)}")

    return "\n".join(lines)


def confabulation_discussion():
    return """
================================================================================
DISCUSSION — Minimal Terminal Set Robustness Test
================================================================================

This experiment tests whether removing the Leibniz injection from population
initialization prevents rediscovery of the series. With only {k, 1, -1, 2}
as terminals and no seed individual, the optimizer must construct the Leibniz
structure purely from selection pressure.

The v2/entropy experiments (5/5 success) injected make_leibniz_tree() at
population[0], guaranteeing the target formula was present in generation 0.
This minimal variant removes that crutch entirely.

Key question: Does the convergence/entropy fitness landscape have a basin of
attraction around Leibniz large enough to be found by random search within a
30-minute budget?
================================================================================
"""


# ── Output writers ────────────────────────────────────────────────────────────

def _leibniz_info_profile():
    terms = safe_eval(make_leibniz_tree(), K_ARRAY)
    if terms is None:
        return {}
    cum = np.cumsum(terms)
    return {T: round(info_bits(abs(float(cum[T-1]) - PI_OVER_4)), 4)
            for T in T_CHECKPOINTS}


def write_entropy_json(seed_results):
    lei = make_leibniz_tree()
    gp1 = make_gp1_best_tree()
    best_r = max(seed_results, key=lambda r: r["best_fitness"])
    best_ana = best_r.get("analysis", {})

    lei_infos = _leibniz_info_profile()

    gp1_infos = compute_info_profile(gp1)
    gp1_profile = {T: round(gp1_infos[i], 4) for i, T in enumerate(T_CHECKPOINTS)} \
        if gp1_infos else {}

    entropy_infos_raw = best_ana.get("infos", {})
    entropy_profile = {T: entropy_infos_raw.get(T) for T in T_CHECKPOINTS}

    def partial_sum_curve(tree, t_samples):
        terms = safe_eval(tree, np.arange(max(t_samples), dtype=float))
        if terms is None:
            return {}
        cum = np.cumsum(terms)
        return {T: round(float(cum[T-1]), 10) for T in t_samples if T <= len(cum)}

    t_samples = sorted(set(
        list(range(1, 11)) + list(range(20, 101, 10)) +
        list(range(200, 1001, 100)) + [2000, 5000]
    ))
    lei_curve = partial_sum_curve(lei, t_samples)
    gp1_curve = partial_sum_curve(gp1, t_samples)
    best_curve = best_ana.get("partial_sums", {})

    def to_error_curve(curve):
        return {k: round(abs(v - PI_OVER_4), 10) for k, v in curve.items()}

    data = {
        "config": {
            "pop_size": POP_SIZE, "max_depth": MAX_DEPTH, "max_nodes": MAX_NODES,
            "tournament_k": TOURNAMENT_K, "p_cross": P_CROSS, "p_mut": P_MUT,
            "n_elite": N_ELITE, "w1": W1, "w2": W2, "w3": W3,
            "lambda_p": LAMBDA_P, "t_checkpoints": T_CHECKPOINTS, "n_seeds": N_SEEDS,
            "term_fixed": TERM_FIXED, "ephemerals": EPHEMERALS,
            "leibniz_injection": False,
        },
        "pi_over_4": PI_OVER_4,
        "leibniz_refs": {str(T): round(v, 10) for T, v in LEIBNIZ_REFS.items()},
        "info_profiles": {
            "leibniz": lei_infos,
            "gp_v1": gp1_profile,
            "entropy_v3_minimal": entropy_profile,
        },
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
                "info_profile": {str(T): v for T, v in
                                 r.get("analysis", {}).get("infos", {}).items()},
                "errors": {str(T): v for T, v in
                           r.get("analysis", {}).get("errors", {}).items()},
                "history": r["history"],
            }
            for r in seed_results
        ],
        "best_seed_idx": best_r["seed"],
        "convergence_curves": {
            "leibniz": lei_curve,
            "gp_v1_best": gp1_curve,
            "entropy_v3_minimal_best": best_curve,
        },
        "error_curves": {
            "leibniz": to_error_curve(lei_curve),
            "gp_v1_best": to_error_curve(gp1_curve),
            "entropy_v3_minimal_best": to_error_curve(best_curve),
        },
        "entropy_v3_minimal_expr": best_r["best_expr"],
        "gp_v1_expr": gp1.to_str(),
        "leibniz_expr": lei.to_str(),
    }

    path = OUT_DIR / "entropy_data_minimal.json"
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
    path = OUT_DIR / "convergence_minimal.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {path}", flush=True)


def write_results_txt(seed_results, unit_report, eval_report, vv_report):
    W = 72
    header = "\n".join([
        "=" * W,
        "ENTROPY-LEIBNIZ v3 MINIMAL: TEVV REPORT",
        "Minimal terminal set {k, 1, -1, 2}, no injection, 30-min budget",
        "=" * W,
        "",
        "Configuration (v3 minimal changes from entropy v1):",
        f"  pop_size={POP_SIZE}, max_depth={MAX_DEPTH}, max_nodes={MAX_NODES}",
        f"  tournament_k={TOURNAMENT_K}, n_elite={N_ELITE}",
        f"  W1={W1}, W2={W2}, W3={W3}, lambda_p={LAMBDA_P}",
        f"  T_checkpoints={T_CHECKPOINTS}",
        f"  n_seeds={N_SEEDS}, max_total={MAX_TOTAL}s, max_seed={MAX_SEED}s",
        f"  TERM_FIXED={TERM_FIXED}  [CHANGED: no ephemerals]",
        f"  EPHEMERALS={EPHEMERALS}  [CHANGED: empty]",
        f"  Leibniz injection: NONE  [CHANGED: removed from pop init]",
        "",
        "Fitness: W1*(total_info/50) + W2*monotonicity + W3*(mean_rate/5) - lambda_p*nodes",
    ])
    path = OUT_DIR / "results_minimal.txt"
    with open(path, "w") as f:
        f.write(header + "\n" + unit_report + "\n" + eval_report + "\n" + vv_report
                + confabulation_discussion())
    print(f"  Wrote {path}", flush=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    global_t0 = time.time()
    print("=" * 72, flush=True)
    print("Entropy-Leibniz v3 minimal: minimal terminals, no injection", flush=True)
    print(f"  π/4 = {PI_OVER_4:.10f}", flush=True)
    print(f"  Fitness: {W1}*(ti/50) + {W2}*mono + {W3}*(rate/5) - {LAMBDA_P}*nodes", flush=True)
    print(f"  T_checkpoints = {T_CHECKPOINTS}", flush=True)
    print(f"  Terminals: {ALL_TERMINALS}", flush=True)
    print(f"  Leibniz injection: NONE", flush=True)
    print("=" * 72, flush=True)

    print("\n[1/5] Unit tests ...", flush=True)
    unit_report, passed, failed = run_unit_tests()
    print(unit_report, flush=True)
    if failed:
        print(f"WARNING: {failed} unit test(s) failed — proceeding anyway", flush=True)

    print("\n[2/5] GP experiment ...", flush=True)
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

    print("\n[3/5] Analyzing ...", flush=True)
    for r in seed_results:
        r["analysis"] = analyze_result(r)

    print("\n[4/5] TEVV report ...", flush=True)
    eval_report = run_eval_report(seed_results)
    vv_report = run_vv_report(seed_results)
    print(eval_report, flush=True)
    print(vv_report, flush=True)

    print("\n[5/5] Writing files ...", flush=True)
    write_entropy_json(seed_results)
    write_convergence_csv(seed_results)
    write_results_txt(seed_results, unit_report, eval_report, vv_report)

    prog = OUT_DIR / "progress.json"
    if prog.exists():
        prog.unlink()

    print(f"\nTotal elapsed: {time.time() - global_t0:.1f}s", flush=True)
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
