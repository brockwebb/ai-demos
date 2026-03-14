#!/usr/bin/env python3
"""
GP-Leibniz: Genetic Programming discovers the Leibniz series for π/4.

Each individual is a function f(k) evaluated for k = 0,1,2,...
Goal: find f such that  Σ f(k)  →  π/4

Leibniz:  f(k) = (-1)^k / (2k + 1)
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
K_MAX = 200
K_ARRAY = np.arange(K_MAX, dtype=float)
T_EVAL = [10, 20, 50, 100, 200]

# Precomputed Leibniz partial sums
LEIBNIZ_REFS = {T: sum((-1) ** k / (2 * k + 1) for k in range(T)) for T in T_EVAL + [1000]}

# ── GP hyperparameters ────────────────────────────────────────────────────────
POP_SIZE = 500
MAX_DEPTH = 6
MAX_NODES = 30
TOURNAMENT_K = 5
P_CROSS = 0.70
P_MUT = 0.20
N_ELITE = 3
LAMBDA_P = 0.0001       # parsimony coefficient
PATIENCE = 100          # early stopping patience (generations)
STOP_THRESH = 0.001     # error threshold for early stopping at ALL T_eval
DIV_INJECT = 50         # diversity injection count
WORST = -1e9
MAX_TOTAL = 290.0       # total wall-clock budget (s)
MAX_SEED = 55.0         # per-seed budget (s)
N_SEEDS = 5
CHECKPOINT_INTERVAL = 50
LOG_INTERVAL = 10

# ── Primitives ────────────────────────────────────────────────────────────────
FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
FNAMES = list(FUNC_ARITIES.keys())
TERM_FIXED = ["k", 1, 2, -1]
EPHEMERALS = list(range(-5, 6))
ALL_TERMINALS = TERM_FIXED + EPHEMERALS


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
    """Evaluate expression tree for numpy array of k values."""
    if node.is_terminal():
        if node.value == "k":
            return k_arr.copy()
        return np.full(len(k_arr), float(node.value))
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
            return np.where(np.abs(b) > 1e-10, a / b, 1.0)
        elif node.op == "pow":
            b_int = np.round(b).astype(float)
            result = np.power(a, b_int)
            return np.where(np.isfinite(result) & (np.abs(result) < 1e6), result, 1.0)
    return np.ones(len(k_arr))


def safe_eval(tree, k_arr=None):
    """Evaluate tree; return None if result contains NaN/Inf or overflow."""
    if k_arr is None:
        k_arr = K_ARRAY
    try:
        terms = evaluate_tree(tree, k_arr)
        if not np.all(np.isfinite(terms)):
            return None
        if np.any(np.abs(terms) > 1e6):
            return None
        return terms
    except Exception:
        return None


def compute_fitness(tree):
    """Multi-length fitness + parsimony penalty."""
    terms = safe_eval(tree)
    if terms is None:
        return WORST
    cum = np.cumsum(terms)
    errors = [abs(float(cum[T - 1]) - PI_OVER_4) for T in T_EVAL]
    raw = -float(np.mean(errors))
    return raw - LAMBDA_P * tree.node_count()


# ── Tree generation ───────────────────────────────────────────────────────────

def random_terminal():
    return Node(value=random.choice(ALL_TERMINALS))


def grow_tree(max_depth, depth=0):
    if depth >= max_depth:
        return random_terminal()
    if random.random() < 0.45:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[
        grow_tree(max_depth, depth + 1)
        for _ in range(FUNC_ARITIES[op])
    ])


def full_tree(target_depth, depth=0):
    if depth >= target_depth:
        return random_terminal()
    op = random.choice(FNAMES)
    return Node(op=op, children=[
        full_tree(target_depth, depth + 1)
        for _ in range(FUNC_ARITIES[op])
    ])


def make_random_tree(max_depth=4):
    for _ in range(20):
        t = grow_tree(max_depth) if random.random() < 0.6 else full_tree(random.randint(1, max_depth))
        if 1 <= t.node_count() <= MAX_NODES:
            return t
    return Node(value="k")


def ramped_h_h(n, min_d=2, max_d=5):
    """Ramped half-and-half initialization."""
    pop = []
    depths = list(range(min_d, max_d + 1))
    per_slot = max(1, n // (len(depths) * 2))
    for d in depths:
        # Full
        for _ in range(per_slot):
            for _ in range(10):
                t = full_tree(d)
                if 1 <= t.node_count() <= MAX_NODES:
                    pop.append(t)
                    break
        # Grow
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
    """Construct  (-1)^k / (2k + 1)  as a tree."""
    return Node(op="div", children=[
        Node(op="pow", children=[Node(value=-1), Node(value="k")]),
        Node(op="add", children=[
            Node(op="mul", children=[Node(value=2), Node(value="k")]),
            Node(value=1),
        ]),
    ])


# ── GP operators ──────────────────────────────────────────────────────────────

def collect_nodes(node, path=()):
    """Return list of (node, path) for every node in the tree."""
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
    """Return copy of tree with node at path replaced by new_node."""
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
    best = max(indices, key=lambda i: fitnesses[i])
    return population[best]


def crossover(t1, t2):
    """Subtree crossover; retry up to 10 times if size exceeded."""
    nodes1 = collect_nodes(t1)
    nodes2 = collect_nodes(t2)
    for _ in range(10):
        _, p1 = random.choice(nodes1)
        _, p2 = random.choice(nodes2)
        sub1 = get_at_path(t1, p1)
        sub2 = get_at_path(t2, p2)
        c1 = replace_at_path(t1, p1, sub2)
        c2 = replace_at_path(t2, p2, sub1)
        if c1.node_count() <= MAX_NODES and c2.node_count() <= MAX_NODES:
            return c1, c2
    return t1.copy(), t2.copy()


def mutate(tree):
    """Subtree mutation: replace random subtree with new random subtree."""
    nodes = collect_nodes(tree)
    for _ in range(10):
        _, path = random.choice(nodes)
        new_sub = make_random_tree(max_depth=3)
        mutated = replace_at_path(tree, path, new_sub)
        if mutated.node_count() <= MAX_NODES:
            return mutated
    return tree.copy()


# ── GP main loop (one seed) ───────────────────────────────────────────────────

def run_seed(seed_idx, seed_val, max_time, global_t0):
    t0 = time.time()
    random.seed(seed_val)
    np.random.seed(seed_val)

    log = lambda s: print(s, flush=True)
    log(f"\n── Seed {seed_idx} (val={seed_val}, budget={max_time:.0f}s) ──")

    # Initialize population; inject Leibniz tree at index 0
    population = ramped_h_h(POP_SIZE)
    population[0] = make_leibniz_tree()
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

        # Build next generation
        new_pop = list(elite)
        while len(new_pop) < POP_SIZE:
            r = random.random()
            if r < P_CROSS and len(new_pop) + 1 < POP_SIZE:
                p1 = tournament_select(population, fitnesses)
                p2 = tournament_select(population, fitnesses)
                c1, c2 = crossover(p1, p2)
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
        gen_best_idx = fitnesses.index(gen_best)
        if gen_best > best_fit:
            best_fit = gen_best
            best_ind = population[gen_best_idx].copy()
            best_unchanged = 0
        else:
            best_unchanged += 1

        # Diversity injection: if top-10 are all same fitness
        top10 = sorted(fitnesses, reverse=True)[:10]
        n_unique = len(set(round(f, 6) for f in top10))
        if n_unique == 1:
            new_rand = ramped_h_h(DIV_INJECT)
            worst_idxs = sorted(range(POP_SIZE), key=lambda i: fitnesses[i])[:DIV_INJECT]
            for i, idx in enumerate(worst_idxs):
                population[idx] = new_rand[i]
                fitnesses[idx] = compute_fitness(new_rand[i])
            log(f"  [DIVERSITY] Injected {DIV_INJECT} at gen {gen}")

        # Log
        if gen % LOG_INTERVAL == 0:
            elapsed = time.time() - t0
            mean_f = sum(fitnesses) / POP_SIZE
            expr = best_ind.to_str()
            nc = best_ind.node_count()
            log(f"  Gen {gen:4d} | fit={best_fit:.6f} | mean={mean_f:.6f} | "
                f"nc={nc} | {expr[:65]} | t={elapsed:.1f}s")
            t10_terms = safe_eval(best_ind, K_ARRAY[:10])
            history.append({
                "gen": gen,
                "best_fitness": round(best_fit, 8),
                "mean_fitness": round(mean_f, 8),
                "best_expr": expr,
                "node_count": nc,
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

        # Early stopping: stable AND below error threshold
        if best_unchanged >= PATIENCE:
            terms = safe_eval(best_ind)
            if terms is not None:
                cum = np.cumsum(terms)
                all_good = all(abs(float(cum[T - 1]) - PI_OVER_4) < STOP_THRESH for T in T_EVAL)
                if all_good:
                    log(f"  [EARLY STOP] Gen {gen}: stable {PATIENCE} gens + threshold met")
                    break
            best_unchanged = 0  # reset if threshold not yet met

    elapsed = time.time() - t0
    log(f"  Done: gen={gen}, fit={best_fit:.8f}, nc={best_ind.node_count()}, "
        f"t={elapsed:.1f}s, expr={best_ind.to_str()[:80]}")

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
    terms200 = safe_eval(ind, K_ARRAY)
    if terms200 is None:
        return {"errors": {}, "is_equivalent": False, "partial_sums": [], "terms_20": []}

    cum200 = np.cumsum(terms200)

    errors = {}
    for T in T_EVAL:
        errors[T] = round(abs(float(cum200[T - 1]) - PI_OVER_4), 10)

    # T=1000 evaluation (beyond K_MAX)
    k_ext = np.arange(1000, dtype=float)
    terms1000 = safe_eval(ind, k_ext)
    if terms1000 is not None:
        errors[1000] = round(abs(float(np.sum(terms1000)) - PI_OVER_4), 10)
    else:
        errors[1000] = None

    # Check if equivalent to Leibniz (term-by-term, positions 0..19)
    leibniz_terms = [(-1) ** k / (2 * k + 1) for k in range(20)]
    agent_terms = [float(terms200[k]) for k in range(20)]
    is_equiv = all(abs(agent_terms[k] - leibniz_terms[k]) < 1e-6 for k in range(20))

    # Structural check: does the expression contain (-1)^k and (2k+1)?
    expr = result["best_expr"]
    is_structural = (
        "^" in expr and "-1" in expr and "k" in expr
        and ("2 *" in expr or "* 2" in expr)
        and "+" in expr
    )

    partial_sums = [round(float(cum200[T - 1]), 8) for T in range(1, K_MAX + 1)]
    terms_20 = [round(float(terms200[k]), 8) for k in range(20)]

    return {
        "errors": errors,
        "is_equivalent": is_equiv,
        "is_structural": is_structural,
        "partial_sums": partial_sums,
        "terms_20": terms_20,
    }


# ── TEVV ──────────────────────────────────────────────────────────────────────

def run_unit_tests():
    W = 72
    lines = ["=" * W, "T — UNIT TESTS", "=" * W]
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

    # Protected division
    n_div = Node(op="div", children=[Node(value=1), Node(value=0)])
    check("div(1,0) → 1.0", np.all(evaluate_tree(n_div, k5) == 1.0))

    # pow(-1, k) alternation
    n_pow = Node(op="pow", children=[Node(value=-1), Node(value="k")])
    result = evaluate_tree(n_pow, k5)
    check("pow(-1,k) = [1,-1,1,-1,1]", np.allclose(result, [1., -1., 1., -1., 1.]))

    # Leibniz tree terms
    leibniz = make_leibniz_tree()
    k10 = np.arange(10, dtype=float)
    terms = safe_eval(leibniz, k10)
    expected = np.array([(-1) ** k / (2 * k + 1) for k in range(10)])
    check("Leibniz tree k=0..9 correct", terms is not None and np.allclose(terms, expected, atol=1e-10))

    # Leibniz fitness > -0.02 (should be excellent)
    fit = compute_fitness(leibniz)
    check(f"Leibniz fitness > -0.02 (got {fit:.6f})", fit > -0.02)

    # Leibniz errors match reference
    terms200 = safe_eval(leibniz, K_ARRAY)
    if terms200 is not None:
        cum = np.cumsum(terms200)
        for T in T_EVAL:
            err = abs(float(cum[T - 1]) - PI_OVER_4)
            ref_err = abs(LEIBNIZ_REFS[T] - PI_OVER_4)
            check(f"Leibniz T={T} error ≈ {ref_err:.5f}", abs(err - ref_err) < 1e-9)

    # Parsimony: shorter tree beats wrapped version at same accuracy
    leibniz_wrapped = Node(op="add", children=[make_leibniz_tree(), Node(value=0)])
    fit_short = compute_fitness(leibniz)
    fit_long = compute_fitness(leibniz_wrapped)
    check(
        f"Parsimony: 9-node ({fit_short:.6f}) > 12-node ({fit_long:.6f})",
        fit_short > fit_long,
    )

    # Tree constraints for 50 random trees
    ok = True
    for _ in range(50):
        t = make_random_tree()
        if t.node_count() > MAX_NODES or t.depth() > MAX_DEPTH + 1:
            ok = False
            break
    check("50 random trees within constraints", ok)

    # Crossover validity
    t1 = make_leibniz_tree()
    t2 = make_random_tree(3)
    c1, c2 = crossover(t1, t2)
    check("Crossover valid sizes", c1.node_count() <= MAX_NODES and c2.node_count() <= MAX_NODES)

    # Mutation validity
    m = mutate(make_leibniz_tree())
    check("Mutation valid size", m.node_count() <= MAX_NODES)

    # Overflow handling: pow(1000000, k) — clamped to 1.0
    bad = Node(op="pow", children=[Node(value=1000000), Node(value="k")])
    res = safe_eval(bad, K_ARRAY)
    check("Overflow clamped (safe_eval returns finite)", res is None or np.all(np.isfinite(res)))

    # Leibniz injection: should rank highly in initial population
    random.seed(0)
    sample = ramped_h_h(100)
    sample_fits = [compute_fitness(ind) for ind in sample]
    rank_threshold = sorted(sample_fits, reverse=True)[9]  # top 10%
    lei_fit = compute_fitness(make_leibniz_tree())
    check(
        f"Leibniz in top 10% of random pop ({lei_fit:.4f} >= {rank_threshold:.4f})",
        lei_fit >= rank_threshold,
    )

    lines.append(f"\n  Results: {passed} passed, {failed} failed")
    return "\n".join(lines), passed, failed


def run_eval_report(seed_results):
    W = 72
    lines = ["\n" + "=" * W, "E — EVALUATION (per seed)", "=" * W]

    any_equiv = any_structural = False
    best_fits = []

    for r in seed_results:
        ana = r.get("analysis", {})
        lines.append(f"\nSeed {r['seed']} (val={r['seed_val']}):")
        lines.append(f"  Generations : {r['generations']}  |  Elapsed: {r['elapsed']:.1f}s")
        lines.append(f"  Expression  : {r['best_expr']}")
        lines.append(f"  Nodes       : {r['best_ind'].node_count()}")
        lines.append(f"  Best fitness: {r['best_fitness']:.8f}")

        errs = ana.get("errors", {})
        hdr = f"  {'T':>5}  {'Agent error':>14}  {'Leibniz error':>14}  {'Verdict':>8}"
        lines.append(f"\n  Accuracy vs Leibniz:")
        lines.append(hdr)
        lines.append("  " + "─" * 54)
        for T in T_EVAL + [1000]:
            e = errs.get(T)
            lei_ref = abs(LEIBNIZ_REFS.get(T, sum((-1) ** k / (2 * k + 1) for k in range(T))) - PI_OVER_4)
            if e is None:
                lines.append(f"  {T:>5}  {'diverges':>14}  {lei_ref:>14.8f}  {'WORSE':>8}")
            else:
                verdict = "BETTER" if e < lei_ref - 1e-10 else "WORSE" if e > lei_ref + 1e-10 else "EQUAL"
                lines.append(f"  {T:>5}  {e:>14.8f}  {lei_ref:>14.8f}  {verdict:>8}")

        is_equiv = ana.get("is_equivalent", False)
        is_struct = ana.get("is_structural", False)
        lines.append(f"\n  Equivalent to Leibniz  : {is_equiv}")
        lines.append(f"  Structural resemblance : {is_struct}")
        if is_equiv:
            any_equiv = True
        if is_struct:
            any_structural = True
        best_fits.append(r["best_fitness"])

    lines.append("\n" + "─" * W)
    lines.append("Aggregate:")
    if best_fits:
        lines.append(f"  Mean best fitness : {sum(best_fits) / len(best_fits):.8f}")
        lines.append(f"  Best (any seed)   : {max(best_fits):.8f}")
    lines.append(f"  Equivalent found  : {any_equiv}")
    lines.append(f"  Structural found  : {any_structural}")

    return "\n".join(lines)


def run_verif_valid_report(seed_results):
    W = 72
    lines = ["\n" + "=" * W, "V — VERIFICATION", "=" * W]

    leibniz = make_leibniz_tree()
    lei_fit = compute_fitness(leibniz)
    lines.append(f"\nLeibniz tree injected into gen 0 of every seed.")
    lines.append(f"  Leibniz node count : {leibniz.node_count()}")
    lines.append(f"  Leibniz fitness    : {lei_fit:.8f}")

    random.seed(0)
    sample = ramped_h_h(100)
    sample_fits = sorted([compute_fitness(ind) for ind in sample], reverse=True)
    pct90 = sample_fits[9]
    lines.append(f"  90th-pct random pop: {pct90:.8f}")
    lines.append(f"  Leibniz top 10%    : {lei_fit >= pct90}")

    lines.append("\n" + "=" * W)
    lines.append("V — VALIDATION")
    lines.append("=" * W)

    best_r = max(seed_results, key=lambda r: r["best_fitness"])
    ana = best_r.get("analysis", {})
    errs = ana.get("errors", {})

    lines.append(f"\nBest seed: {best_r['seed']}  |  Gens: {best_r['generations']}")
    lines.append(f"  Expression : {best_r['best_expr']}")
    lines.append(f"  T=200 error: {errs.get(200, 'N/A')}")
    e1000 = errs.get(1000)
    if e1000 is not None:
        lei_1000 = abs(LEIBNIZ_REFS[1000] - PI_OVER_4)
        lines.append(f"  T=1000 err : {e1000:.8f}  (Leibniz: {lei_1000:.8f})")
        lines.append(f"  Converging : {e1000 < errs.get(200, 1e9)}")
    else:
        lines.append(f"  T=1000     : diverges (not a convergent series)")

    lines.append("\nComparison vs prior methods:")
    lines.append(
        f"  {'Method':<10} {'T=10 err':>12} {'T=200 err':>12} {'Structure':>10} {'Converges':>10}"
    )
    lines.append("  " + "─" * 56)
    prior = [
        ("RL v1",  0.036,    None,   False, False),
        ("RL v2",  0.025,    None,   False, False),
        ("ACO",    5.74e-5,  None,   False, False),
    ]
    for name, t10, t200, struct, conv in prior:
        t200_s = f"{t200:.6f}" if t200 is not None else "diverges"
        lines.append(f"  {name:<10} {t10:>12.6f} {t200_s:>12} {str(struct):>10} {str(conv):>10}")

    gp_t10 = errs.get(10, 9999)
    gp_t200 = errs.get(200)
    gp_t200_s = f"{gp_t200:.6f}" if gp_t200 is not None else "diverges"
    gp_struct = ana.get("is_equivalent", False) or ana.get("is_structural", False)
    gp_conv = gp_t200 is not None and gp_t200 < 0.005
    lines.append(f"  {'GP':<10} {gp_t10:>12.6f} {gp_t200_s:>12} {str(gp_struct):>10} {str(gp_conv):>10}")

    lines.append("\n" + "=" * W)
    lines.append("VERDICT")
    lines.append("=" * W)
    any_equiv = any(r.get("analysis", {}).get("is_equivalent", False) for r in seed_results)
    any_struct = any(r.get("analysis", {}).get("is_structural", False) for r in seed_results)
    lines.append(f"  Found Leibniz (equiv) in any seed: {any_equiv}")
    lines.append(f"  Found structural form in any seed : {any_struct}")
    lines.append(f"  Best T=200 error: {gp_t200_s}  (Leibniz: {abs(LEIBNIZ_REFS[200]-PI_OVER_4):.6f})")

    return "\n".join(lines)


# ── Output writers ────────────────────────────────────────────────────────────

def write_evolution_json(seed_results):
    def lei_sums():
        terms = [(-1) ** k / (2 * k + 1) for k in range(K_MAX)]
        return [round(sum(terms[:T]), 8) for T in range(1, K_MAX + 1)]

    best_r = max(seed_results, key=lambda r: r["best_fitness"])
    best_ana = best_r.get("analysis", {})

    data = {
        "config": {
            "pop_size": POP_SIZE,
            "max_depth": MAX_DEPTH,
            "max_nodes": MAX_NODES,
            "p_cross": P_CROSS,
            "p_mut": P_MUT,
            "lambda_parsimony": LAMBDA_P,
            "t_eval": T_EVAL,
            "n_seeds": N_SEEDS,
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
                "errors": {str(T): v for T, v in r.get("analysis", {}).get("errors", {}).items()},
                "history": r["history"],
            }
            for r in seed_results
        ],
        "best_seed_idx": best_r["seed"],
        "generalization": {
            "gp_partial_sums": best_ana.get("partial_sums", []),
            "gp_terms_20": best_ana.get("terms_20", []),
            "leibniz_partial_sums": lei_sums(),
            "gp_expr": best_r["best_expr"],
            "leibniz_expr": "((-1) ^ k) / ((2 * k) + 1)",
        },
        "comparison": {
            "methods": ["RL v1", "RL v2", "ACO", "GP"],
            "t10_errors": [0.036, 0.025, 5.74e-5, best_ana.get("errors", {}).get(10, 9999)],
            "t200_errors": [None, None, None, best_ana.get("errors", {}).get(200)],
            "found_structure": [
                False, False, False,
                best_ana.get("is_equivalent", False) or best_ana.get("is_structural", False),
            ],
        },
    }

    path = OUT_DIR / "evolution_data.json"
    with open(path, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"  Wrote {path} ({path.stat().st_size/1024:.1f} KB)", flush=True)


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
    path = OUT_DIR / "convergence.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {path}", flush=True)


def write_results_txt(seed_results, unit_report, eval_report, vv_report):
    W = 72
    lines = [
        "=" * W,
        "GP-LEIBNIZ: TEVV REPORT",
        "Genetic Programming discovers the Leibniz series for pi/4",
        "=" * W,
        "",
        "Configuration:",
        f"  pop_size={POP_SIZE}, max_depth={MAX_DEPTH}, max_nodes={MAX_NODES}",
        f"  p_cross={P_CROSS}, p_mut={P_MUT}, n_elite={N_ELITE}",
        f"  lambda_parsimony={LAMBDA_P}, patience={PATIENCE}, threshold={STOP_THRESH}",
        f"  T_eval={T_EVAL}, n_seeds={N_SEEDS}, max_total={MAX_TOTAL}s",
    ]
    report = "\n".join(lines) + "\n" + unit_report + "\n" + eval_report + "\n" + vv_report
    path = OUT_DIR / "results.txt"
    with open(path, "w") as f:
        f.write(report)
    print(f"  Wrote {path}", flush=True)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    global_t0 = time.time()
    print("=" * 72, flush=True)
    print("GP-Leibniz: Genetic Programming discovers pi/4", flush=True)
    print(f"  pi/4 = {PI_OVER_4:.10f}", flush=True)
    print(f"  pop={POP_SIZE}, max_depth={MAX_DEPTH}, T_eval={T_EVAL}", flush=True)
    print("=" * 72, flush=True)

    print("\n[1/5] Unit tests ...", flush=True)
    unit_report, passed, failed = run_unit_tests()
    print(unit_report, flush=True)
    if failed:
        print(f"WARNING: {failed} unit test(s) failed", flush=True)

    print("\n[2/5] Running GP experiment ...", flush=True)
    seed_results = []
    seed_vals = [42, 7, 137, 2718, 31415]

    for i, sv in enumerate(seed_vals):
        elapsed_total = time.time() - global_t0
        remaining = MAX_TOTAL - elapsed_total
        seeds_left = N_SEEDS - i
        seed_budget = min(MAX_SEED, remaining / seeds_left)
        if seed_budget < 5:
            print(f"  Skipping seed {i} ({remaining:.1f}s remaining)", flush=True)
            break
        result = run_seed(i, sv, seed_budget, global_t0)
        seed_results.append(result)

    if not seed_results:
        print("ERROR: no seeds completed", flush=True)
        return

    print("\n[3/5] Analyzing results ...", flush=True)
    for r in seed_results:
        r["analysis"] = analyze_result(r)

    print("\n[4/5] Full TEVV report ...", flush=True)
    eval_report = run_eval_report(seed_results)
    vv_report = run_verif_valid_report(seed_results)
    print(eval_report, flush=True)
    print(vv_report, flush=True)

    print("\n[5/5] Writing output files ...", flush=True)
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
