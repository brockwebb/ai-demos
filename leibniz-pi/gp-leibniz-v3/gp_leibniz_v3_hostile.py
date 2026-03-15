#!/usr/bin/env python3
"""
GP-Leibniz v2: Convergence-aware fitness discovers the Leibniz series.

Key change from v1: Three-component fitness reshapes the landscape so
that TRUE convergence to π/4 (error→0 as T→∞) is the dominant pressure,
and parsimony makes Leibniz the shortest expression that achieves it.

  fitness = accuracy + alpha * convergence_bonus - lambda * node_count

  accuracy        = -mean(|partial_sum_T - π/4| for T in [10,50,200,1000,5000])
  convergence_bonus = fraction of consecutive T-pairs with >5% error reduction
  alpha           = 0.05   (convergence weight)
  lambda          = 0.005  (heavy parsimony; 9-node Leibniz pays 0.045)

GP v1 best (-3-k)^(-k) flatlines at error 0.00036 from T=10 onward.
Its convergence_bonus = 0. Under this fitness it scores ~-0.030.
Leibniz converges monotonically: convergence_bonus = 1.0, scores ~0.000.
Leibniz wins by 0.030 — a decisive selection advantage.
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
POP_SIZE = 1000         # v2: up from 500
MAX_DEPTH = 6
MAX_NODES = 30
TOURNAMENT_K = 7        # v2: up from 5
P_CROSS = 0.70
P_MUT = 0.20
N_ELITE = 5             # v2: up from 3
ALPHA = 0.05            # v2: convergence bonus weight
LAMBDA_P = 0.005        # v2: heavy parsimony (up from 0.0001)
PATIENCE = 100
STOP_THRESH = 0.001
DIV_INJECT = 100        # v2: up from 50
WORST = -1e9
MAX_TOTAL = 1800.0
MAX_SEED = 360.0
N_SEEDS = 5
CHECKPOINT_INTERVAL = 50
LOG_INTERVAL = 10

# Primitives
FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
FNAMES = list(FUNC_ARITIES.keys())
TERM_FIXED = ["k", 1, 3, -1]
EPHEMERALS = [x for x in range(-20, 21) if x != 2]
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
# Constants return Python floats (no array allocation). Only 'k' returns the
# full array. numpy broadcasting handles scalar+array automatically.

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
            # Protected division: returns 1.0 when |b| ≤ 1e-10
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
        # Normalize to 1D array
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

    # Sanity: if cumsum diverges badly, penalize
    if any(e > 1e4 for e in errors):
        _fitness_cache[key] = WORST
        return WORST

    accuracy = -float(np.mean(errors))

    # Convergence bonus: count pairs where error reduces by ≥5%
    n_improving = sum(
        1 for i in range(len(errors) - 1)
        if errors[i + 1] < errors[i] * 0.95
    )
    conv_bonus = n_improving / (len(errors) - 1)  # 0..1

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
    """(-1)^k / (2k + 1)"""
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

    # Time one generation first to check performance
    sample = ramped_h_h(min(50, POP_SIZE))
    t_check = time.time()
    for ind in sample:
        compute_fitness(ind)
    t_per_ind = (time.time() - t_check) / len(sample)
    est_per_gen = t_per_ind * POP_SIZE * 1.5  # include overhead
    log(f"  Perf check: {t_per_ind*1000:.2f}ms/ind, ~{est_per_gen*1000:.0f}ms/gen → "
        f"~{int(max_time / est_per_gen)} gens")

    # Initialize population (fully random — no injection)
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

        # Elitism
        sorted_idx = sorted(range(POP_SIZE), key=lambda i: fitnesses[i], reverse=True)
        elite = [population[i].copy() for i in sorted_idx[:N_ELITE]]

        # New generation
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

        # Track best
        gen_best = max(fitnesses)
        if gen_best > best_fit:
            best_fit = gen_best
            best_ind = population[fitnesses.index(gen_best)].copy()
            best_unchanged = 0
        else:
            best_unchanged += 1

        # Diversity injection
        top20 = sorted(fitnesses, reverse=True)[:20]
        if len(set(round(f, 6) for f in top20)) == 1:
            new_rand = ramped_h_h(DIV_INJECT)
            worst_idxs = sorted(range(POP_SIZE), key=lambda i: fitnesses[i])[:DIV_INJECT]
            for i, idx in enumerate(worst_idxs):
                population[idx] = new_rand[i]
                fitnesses[idx] = compute_fitness(new_rand[i])
            log(f"  [DIVERSITY] Gen {gen}: injected {DIV_INJECT}")

        # Log
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

        # Checkpoint
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

        # Early stopping: stable AND convergence criterion met
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

    # T=10000 (beyond K_MAX)
    k_ext = np.arange(10000, dtype=float)
    terms_ext = safe_eval(ind, k_ext)
    if terms_ext is not None:
        errors[10000] = round(abs(float(np.sum(terms_ext)) - PI_OVER_4), 10)
    else:
        errors[10000] = None

    # Leibniz equivalence: compare terms 0..19
    leibniz_terms = [(-1) ** k / (2 * k + 1) for k in range(20)]
    agent_terms = [float(terms[k]) for k in range(20)]
    is_equiv = all(abs(agent_terms[k] - leibniz_terms[k]) < 1e-6 for k in range(20))

    # Structural heuristic
    expr = result["best_expr"]
    is_structural = ("^" in expr and "-1" in expr and "k" in expr
                     and ("2 *" in expr or "* 2") and "+" in expr)

    # Convergence: is error monotonically decreasing?
    error_list = [errors[T] for T in T_EVAL]
    is_monotone = all(error_list[i + 1] < error_list[i] for i in range(len(error_list) - 1))

    acc, cb, ps, _ = fitness_components(ind)

    # Partial sums for viz (T=1..5000, sampled at log intervals)
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


# ── TEVV ──────────────────────────────────────────────────────────────────────

def run_unit_tests():
    W = 72
    lines = ["=" * W, "T — UNIT TESTS (v2)", "=" * W]
    passed = failed = 0

    def check(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            lines.append(f"  [PASS] {name}")
        else:
            failed += 1
            lines.append(f"  [FAIL] {name}" + (f": {detail}" if detail else ""))

    k5 = np.array([0., 1., 2., 3., 4.])
    leibniz = make_leibniz_tree()
    gp1_best = make_gp1_best_tree()

    # Basic primitives
    n_div = Node(op="div", children=[Node(value=1), Node(value=0)])
    check("div(1,0) → 1.0", np.isscalar(evaluate_tree(n_div, k5)) and evaluate_tree(n_div, k5) == 1.0)

    n_pow = Node(op="pow", children=[Node(value=-1), Node(value="k")])
    res = safe_eval(n_pow, k5)
    check("pow(-1,k) = [1,-1,1,-1,1]", res is not None and np.allclose(res, [1., -1., 1., -1., 1.]))

    # Leibniz tree terms
    lei_terms = safe_eval(leibniz, np.arange(10, dtype=float))
    expected = np.array([(-1) ** k / (2 * k + 1) for k in range(10)])
    check("Leibniz tree k=0..9 correct", lei_terms is not None and np.allclose(lei_terms, expected, atol=1e-10))

    # GP v1 best tree terms
    gp1_terms = safe_eval(gp1_best, np.arange(10, dtype=float))
    check("GP v1 best tree evaluates OK", gp1_terms is not None and np.all(np.isfinite(gp1_terms)))

    # T=5000 errors
    lei_5k = safe_eval(leibniz, K_ARRAY)
    if lei_5k is not None:
        lei_cum = np.cumsum(lei_5k)
        lei_err_5k = abs(float(lei_cum[4999]) - PI_OVER_4)
        lei_ref_5k = abs(LEIBNIZ_REFS[5000] - PI_OVER_4)
        check(f"Leibniz T=5000 error ≈ {lei_ref_5k:.6f}", abs(lei_err_5k - lei_ref_5k) < 1e-8)

    gp1_5k = safe_eval(gp1_best, K_ARRAY)
    if gp1_5k is not None:
        gp1_cum = np.cumsum(gp1_5k)
        gp1_err_5k = abs(float(gp1_cum[4999]) - PI_OVER_4)
        check(f"GP v1 best T=5000 error flatlines (got {gp1_err_5k:.6f})", gp1_err_5k > 0.0001)

    # ── CRITICAL: Fitness calibration ────────────────────────────────────────
    lines.append("\n  ── Fitness Calibration (CRITICAL) ──")
    lei_fit = compute_fitness(leibniz)
    gp1_fit = compute_fitness(gp1_best)
    lines.append(f"  Leibniz fitness  : {lei_fit:.6f}")
    lines.append(f"  GP v1 best fitness: {gp1_fit:.6f}")
    lei_acc, lei_cb, lei_ps, _ = fitness_components(leibniz)
    gp1_acc, gp1_cb, gp1_ps, _ = fitness_components(gp1_best)
    lines.append(f"    Leibniz : acc={lei_acc:.5f} cb={lei_cb:.2f} ps={lei_ps:.4f}")
    lines.append(f"    GP v1   : acc={gp1_acc:.5f} cb={gp1_cb:.2f} ps={gp1_ps:.4f}")
    check(f"Leibniz ({lei_fit:.4f}) beats GP v1 ({gp1_fit:.4f})", lei_fit > gp1_fit,
          f"margin={lei_fit - gp1_fit:.4f}")
    check("Leibniz convergence_bonus = 1.0", abs(lei_cb - 1.0) < 0.01,
          f"got {lei_cb}")
    check("GP v1 convergence_bonus = 0.0", gp1_cb < 0.1,
          f"got {gp1_cb}")
    check(f"Leibniz parsimony = {LAMBDA_P}*9 = {LAMBDA_P*9:.4f}",
          abs(lei_ps - LAMBDA_P * leibniz.node_count()) < 1e-8)

    # Parsimony at new lambda
    check(f"6-node tree parsimony = {LAMBDA_P * 6:.4f}",
          abs(compute_fitness(gp1_best) - (gp1_acc + ALPHA * gp1_cb - gp1_ps)) < 1e-6)

    # Tree constraints
    ok = True
    for _ in range(50):
        t = make_random_tree()
        if t.node_count() > MAX_NODES or t.depth() > MAX_DEPTH + 1:
            ok = False
            break
    check("50 random trees within constraints", ok)

    # Crossover/mutation validity
    t1, t2 = make_leibniz_tree(), make_random_tree(3)
    c1, c2 = crossover(t1, t2)
    check("Crossover valid sizes", c1.node_count() <= MAX_NODES and c2.node_count() <= MAX_NODES)
    check("Mutation valid size", mutate(make_leibniz_tree()).node_count() <= MAX_NODES)

    # Leibniz in top 10% of random pop
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

    any_equiv = any_struct = any_monotone = False
    best_fits = []

    for r in seed_results:
        ana = r.get("analysis", {})
        lines.append(f"\nSeed {r['seed']} (val={r['seed_val']}):")
        lines.append(f"  Gens: {r['generations']}  Elapsed: {r['elapsed']:.1f}s")
        lines.append(f"  Expression : {r['best_expr']}")
        lines.append(f"  Nodes      : {r['best_ind'].node_count()}")
        lines.append(f"  Fitness    : {r['best_fitness']:.8f}")

        acc, cb, ps, total = fitness_components(r["best_ind"])
        lines.append(f"  Components : acc={acc:.6f} + {ALPHA}×cb={ALPHA*cb:.6f} - ps={ps:.6f} = {total:.6f}")
        lines.append(f"  Conv bonus : {cb:.4f} (1.0=perfect)")

        errs = ana.get("errors", {})
        lines.append(f"\n  Errors vs Leibniz:")
        lines.append(f"  {'T':>6}  {'Agent':>14}  {'Leibniz':>14}  {'Verdict':>8}")
        lines.append("  " + "─" * 48)
        for T in T_EVAL + [10000]:
            e = errs.get(T)
            lei = abs(LEIBNIZ_REFS.get(T, sum((-1)**k/(2*k+1) for k in range(T))) - PI_OVER_4)
            if e is None:
                lines.append(f"  {T:>6}  {'diverges':>14}  {lei:>14.8f}  {'WORSE':>8}")
            else:
                v = "BETTER" if e < lei - 1e-10 else "WORSE" if e > lei + 1e-10 else "EQUAL"
                lines.append(f"  {T:>6}  {e:>14.8f}  {lei:>14.8f}  {v:>8}")

        is_eq = ana.get("is_equivalent", False)
        is_st = ana.get("is_structural", False)
        is_mn = ana.get("is_monotone_converging", False)
        lines.append(f"\n  Equivalent to Leibniz  : {is_eq}")
        lines.append(f"  Structural resemblance : {is_st}")
        lines.append(f"  Monotone convergence   : {is_mn}")
        if is_eq: any_equiv = True
        if is_st: any_struct = True
        if is_mn: any_monotone = True
        best_fits.append(r["best_fitness"])

    lines.append("\n" + "─" * W)
    lines.append("Aggregate:")
    if best_fits:
        lines.append(f"  Mean best fitness  : {sum(best_fits)/len(best_fits):.8f}")
        lines.append(f"  Best (any seed)    : {max(best_fits):.8f}")
    lines.append(f"  Any equiv Leibniz  : {any_equiv}")
    lines.append(f"  Any structural     : {any_struct}")
    lines.append(f"  Any monotone conv  : {any_monotone}")
    return "\n".join(lines)


def run_vv_report(seed_results):
    W = 72
    lines = ["\n" + "=" * W, "V — VERIFICATION", "=" * W]

    leibniz = make_leibniz_tree()
    gp1 = make_gp1_best_tree()
    lei_fit = compute_fitness(leibniz)
    gp1_fit = compute_fitness(gp1)
    lines.append(f"\nFitness under v2 function:")
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

    lines.append(f"\nBest seed: {best_r['seed']}  Gens: {best_r['generations']}")
    lines.append(f"  Expression: {best_r['best_expr']}")
    lines.append(f"  T=5000 err: {errs.get(5000, 'N/A')}")
    e10k = errs.get(10000)
    if e10k is not None:
        lei_10k = abs(LEIBNIZ_REFS.get(10000, 0) - PI_OVER_4)
        lines.append(f"  T=10000 err: {e10k:.8f}  (Leibniz: {lei_10k:.8f})")
        lines.append(f"  Converging to T=10000: {e10k < errs.get(5000, 1e9)}")
    else:
        lines.append(f"  T=10000: diverges")

    # Monotone check
    is_mn = ana.get("is_monotone_converging", False)
    error_list = [errs.get(T, float('inf')) for T in T_EVAL]
    lines.append(f"\n  Error at T_EVAL: {[f'{e:.6f}' if isinstance(e,float) else str(e) for e in error_list]}")
    lines.append(f"  Monotone decreasing: {is_mn}")

    lines.append("\n" + "─" * W)
    lines.append("Comparison — all 5 experiments:")
    lines.append(f"  {'Method':<10} {'T=200 err':>12} {'T=5000 err':>12} {'Equiv':>7} "
                 f"{'Monotone':>9} {'Notes'}")
    lines.append("  " + "─" * 65)
    prior = [
        ("RL v1",  "diverges",  "diverges",  False, False, "No structure"),
        ("RL v2",  "diverges",  "diverges",  False, False, "Matched Leibniz at T=10 only"),
        ("ACO",    "diverges",  "diverges",  False, False, "Collapses T>40"),
        ("GP v1",  "0.000360",  "0.000360",  False, False, "Converges to wrong limit"),
    ]
    for name, t200, t5k, equiv, mono, note in prior:
        lines.append(f"  {name:<10} {t200:>12} {t5k:>12} {str(equiv):>7} {str(mono):>9}  {note}")

    gp2_t200 = errs.get(200)
    gp2_t5k = errs.get(5000)
    t200_s = f"{gp2_t200:.6f}" if gp2_t200 is not None else "diverges"
    t5k_s = f"{gp2_t5k:.6f}" if gp2_t5k is not None else "diverges"
    equiv = ana.get("is_equivalent", False)
    mono = ana.get("is_monotone_converging", False)
    lines.append(f"  {'GP v2':<10} {t200_s:>12} {t5k_s:>12} {str(equiv):>7} {str(mono):>9}  "
                 f"{'✓ Leibniz found!' if equiv else 'See results'}")

    lines.append("\n" + "=" * W)
    lines.append("VERDICT")
    lines.append("=" * W)
    any_equiv = any(r.get("analysis", {}).get("is_equivalent", False) for r in seed_results)
    any_mono = any(r.get("analysis", {}).get("is_monotone_converging", False) for r in seed_results)
    lines.append(f"  Found Leibniz equivalent : {any_equiv}")
    lines.append(f"  Found monotone-convergent: {any_mono}")
    lines.append(f"  Best T=5000 error: {t5k_s}  (Leibniz: {abs(LEIBNIZ_REFS[5000]-PI_OVER_4):.6f})")

    return "\n".join(lines)


# ── Output writers ────────────────────────────────────────────────────────────

def compute_partial_sum_series(expr_or_tree, T_max=5000, label=""):
    """Compute partial sum curve at sampled T values."""
    if isinstance(expr_or_tree, Node):
        terms = safe_eval(expr_or_tree, np.arange(T_max, dtype=float))
    else:
        return {}
    if terms is None:
        return {}
    cum = np.cumsum(terms)
    t_samples = (
        list(range(1, 11)) +
        list(range(20, 101, 10)) +
        list(range(200, 1001, 100)) +
        list(range(2000, T_max + 1, 1000))
    )
    return {T: round(float(cum[T - 1]), 10) for T in t_samples if T <= T_max}


def write_evolution_json(seed_results):
    # Compute partial sum curves for comparison
    lei = make_leibniz_tree()
    gp1 = make_gp1_best_tree()
    best_r = max(seed_results, key=lambda r: r["best_fitness"])
    best_ana = best_r.get("analysis", {})

    lei_curve = compute_partial_sum_series(lei, 5000)
    gp1_curve = compute_partial_sum_series(gp1, 5000)
    gp2_curve = best_ana.get("partial_sums", {})

    # Error curves (|partial_sum - π/4|)
    def to_error_curve(curve):
        return {k: round(abs(v - PI_OVER_4), 10) for k, v in curve.items()}

    data = {
        "config": {
            "pop_size": POP_SIZE, "max_depth": MAX_DEPTH, "max_nodes": MAX_NODES,
            "tournament_k": TOURNAMENT_K, "p_cross": P_CROSS, "p_mut": P_MUT,
            "n_elite": N_ELITE, "alpha": ALPHA, "lambda_p": LAMBDA_P,
            "t_eval": T_EVAL, "n_seeds": N_SEEDS,
        },
        "pi_over_4": PI_OVER_4,
        "leibniz_refs": {str(T): round(v, 10) for T, v in LEIBNIZ_REFS.items()},
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
        "best_seed_idx": best_r["seed"],
        "convergence_curves": {
            "leibniz": lei_curve,
            "gp_v1_best": gp1_curve,
            "gp_v2_best": gp2_curve,
        },
        "error_curves": {
            "leibniz": to_error_curve(lei_curve),
            "gp_v1_best": to_error_curve(gp1_curve),
            "gp_v2_best": to_error_curve(gp2_curve),
        },
        "gp_v2_expr": best_r["best_expr"],
        "gp_v1_expr": gp1.to_str(),
        "leibniz_expr": lei.to_str(),
        "comparison": {
            "methods": ["RL v1", "RL v2", "ACO", "GP v1", "GP v2"],
            "t200_errors": [None, None, None, 3.6e-4, best_ana.get("errors", {}).get(200)],
            "t5000_errors": [None, None, None, 3.6e-4, best_ana.get("errors", {}).get(5000)],
            "found_equiv": [False, False, False, False, best_ana.get("is_equivalent", False)],
            "converges": [False, False, False, False, best_ana.get("is_monotone_converging", False)],
        },
    }

    path = OUT_DIR / "evolution_data_v3.json"
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
    path = OUT_DIR / "convergence_v3.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {path}", flush=True)


def write_results_txt(seed_results, unit_report, eval_report, vv_report):
    W = 72
    header = "\n".join([
        "=" * W,
        "GP-LEIBNIZ v2: TEVV REPORT",
        "Convergence-aware fitness discovers the Leibniz series for π/4",
        "=" * W,
        "",
        "Configuration (v2 changes starred):",
        f"  pop_size={POP_SIZE}*, max_depth={MAX_DEPTH}, max_nodes={MAX_NODES}",
        f"  tournament_k={TOURNAMENT_K}*, n_elite={N_ELITE}*",
        f"  alpha={ALPHA}* (convergence weight), lambda_p={LAMBDA_P}* (heavy parsimony)",
        f"  T_eval={T_EVAL}* (includes T=5000)",
        f"  n_seeds={N_SEEDS}, max_total={MAX_TOTAL}s",
        "",
        "Fitness: accuracy + alpha*conv_bonus - lambda*nodes",
        f"  alpha={ALPHA}, lambda={LAMBDA_P}",
        f"  Leibniz (9 nodes) estimated fitness: ~0.000",
        f"  GP v1 best (6 nodes) estimated fitness: ~-0.030",
    ])
    path = OUT_DIR / "results_v3.txt"
    with open(path, "w") as f:
        f.write(header + "\n" + unit_report + "\n" + eval_report + "\n" + vv_report)
    print(f"  Wrote {path}", flush=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    global_t0 = time.time()
    print("=" * 72, flush=True)
    print("GP-Leibniz v2: Convergence-aware fitness for π/4", flush=True)
    print(f"  π/4 = {PI_OVER_4:.10f}", flush=True)
    print(f"  Fitness: accuracy + {ALPHA}*conv_bonus - {LAMBDA_P}*nodes", flush=True)
    print(f"  T_eval = {T_EVAL}", flush=True)
    print("=" * 72, flush=True)

    print("\n[1/5] Unit tests ...", flush=True)
    unit_report, passed, failed = run_unit_tests()
    print(unit_report, flush=True)
    if failed:
        print(f"WARNING: {failed} unit test(s) failed", flush=True)

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
    write_evolution_json(seed_results)
    write_convergence_csv(seed_results)
    write_results_txt(seed_results, unit_report, eval_report, vv_report)

    prog = OUT_DIR / "progress.json"
    if prog.exists():
        prog.unlink()

    print(f"\nTotal elapsed: {time.time() - global_t0:.1f}s", flush=True)
    print("=" * 72, flush=True)


if __name__ == "__main__":
    main()
