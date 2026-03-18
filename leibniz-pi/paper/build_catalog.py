#!/usr/bin/env python3
"""
Build the expression catalog for the Leibniz-Pi paper.

Walks all experiment directories, parses *_data.json files, and writes
paper/expression_catalog.json with per-seed expression records.

Usage:
    python paper/build_catalog.py
"""

import json
import re
import sys
import warnings
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
OUTPUT_FILE = PROJECT_ROOT / "paper" / "expression_catalog.json"

# Directories to scan (relative to project root)
SCAN_DIRS = [
    "gp-leibniz-v3",
    "entropy-leibniz-v3",
    "entropy-leibniz",
    "gp-leibniz-v2",
    "EDA",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def derive_experiment_name(file_path: Path) -> str:
    """Derive a stable experiment name from the data file path."""
    stem = file_path.stem  # e.g. "gp_scaling_t4_p5000_data"
    name = stem.removesuffix("_data")
    # Normalise: strip leading path-specific cruft
    return name


def infer_fitness_function(file_path: Path) -> str:
    """Determine which fitness function was used from the file path."""
    parts = str(file_path).lower()
    if any(tok in parts for tok in ("entropy", "logprec", "heatmap")):
        return "log-precision"
    if "gp" in parts:
        return "convergence-aware"
    return "unknown"


def count_nodes(expr_str: str) -> int:
    """
    Rough node count heuristic.
    Count operators and value tokens in the expression string.
    """
    if not expr_str or not isinstance(expr_str, str):
        return 0
    # Remove outer whitespace and parentheses for tokenisation
    tokens = re.split(r"[\s\(\)]+", expr_str)
    operators = {"+", "-", "*", "/", "^", "neg"}
    count = 0
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok in operators:
            count += 1
        elif re.match(r"^-?\d+(\.\d+)?$", tok):
            count += 1  # numeric literal
        elif re.match(r"^[a-zA-Z_]\w*$", tok):
            count += 1  # variable / constant name
    return max(count, 1)


def simplify_expr(expr_str: str) -> str:
    """
    Attempt sympy simplification of an expression string.

    The GP engine uses Python-like syntax: ^ for power, / for division.
    We map ^ to ** before passing to sympy, then display the result
    using ^ notation.

    Returns the raw form unchanged if sympy fails.
    """
    if not expr_str or not isinstance(expr_str, str):
        return expr_str
    try:
        import sympy  # noqa: PLC0415
        from sympy import symbols, simplify, sympify, Rational  # noqa: PLC0415

        k = symbols("k")
        # Convert ^ to ** for sympy
        py_expr = expr_str.replace("^", "**")
        # Suppress evaluation warnings for malformed expressions
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sym = sympify(py_expr, locals={"k": k}, evaluate=True)
        simplified = simplify(sym)
        # Convert back: ** -> ^
        result = str(simplified).replace("**", "^")
        return result
    except Exception:  # noqa: BLE001
        return expr_str


def classify(best_expr: str, is_equivalent: bool, best_fitness: float) -> str:
    """Classify an expression into one of three categories."""
    if is_equivalent:
        return "leibniz-equivalent"
    # Trivial: very bad fitness or constant-looking expression
    if best_fitness is not None and best_fitness < -10:
        return "trivial"
    # Check for constant-looking expressions (no 'k' variable)
    if best_expr and "k" not in best_expr:
        return "trivial"
    return "wrong-limit-attractor"


# ---------------------------------------------------------------------------
# Per-file parsers
# ---------------------------------------------------------------------------

def extract_top_level_meta(data: dict, file_path: Path) -> dict:
    """
    Pull terminal_count, term_fixed, pop_size from a standard v3-schema JSON.
    Returns a dict of meta fields (may be empty for non-standard files).
    """
    meta = {
        "terminal_count": None,
        "term_fixed": None,
        "pop_size": None,
    }
    # Standard v3 GP scaling schema
    meta["terminal_count"] = data.get("terminal_count") or data.get("terminals_n")
    meta["term_fixed"] = data.get("term_fixed")
    meta["pop_size"] = data.get("pop_size")
    return meta


def parse_standard_seeds(
    data: dict,
    file_path: Path,
    experiment_name: str,
    fitness_function: str,
    meta: dict,
) -> list[dict]:
    """
    Parse seeds from a standard per-seed list (v3 schema).
    Each seed has: seed, seed_val, generations, best_fitness, best_expr, elapsed,
    is_equivalent, is_monotone, [accuracy], [conv_bonus], [total_info], ...
    """
    seeds = data.get("seeds", [])
    records = []
    for s in seeds:
        if not isinstance(s, dict):
            continue
        seed_val = s.get("seed_val") or s.get("seed")
        best_expr = s.get("best_expr", "")
        is_equiv = bool(s.get("is_equivalent", False))
        best_fitness = s.get("best_fitness")

        record = {
            "id": f"expr_{experiment_name}_seed{seed_val}",
            "experiment": experiment_name,
            "fitness_function": fitness_function,
            "terminal_count": meta["terminal_count"],
            "terminal_set": str(meta["term_fixed"]) if meta["term_fixed"] is not None else None,
            "pop_size": meta["pop_size"],
            "seed": seed_val,
            "generations": s.get("generations"),
            "elapsed_seconds": s.get("elapsed"),
            "raw_form": best_expr,
            "simplified_form": simplify_expr(best_expr),
            "nodes": s.get("node_count") or count_nodes(best_expr),
            "fitness_score": best_fitness,
            "is_leibniz": is_equiv,
            "is_monotone": bool(s.get("is_monotone", False)),
            "classification": classify(best_expr, is_equiv, best_fitness),
            "source_file": str(file_path),
        }
        records.append(record)
    return records


def parse_entropy_v1(data: dict, file_path: Path) -> list[dict]:
    """
    Parse the entropy-leibniz v1 file (entropy_data.json).
    Schema: top-level 'seeds' list with same per-seed keys as stress_L1.
    """
    experiment_name = "entropy_v1_wide"
    fitness_function = "log-precision"
    # Attempt to extract config
    config = data.get("config", {})
    terminal_count = config.get("terminal_count") or config.get("terminals_n")
    term_fixed = config.get("term_fixed")
    pop_size = config.get("pop_size")
    meta = {
        "terminal_count": terminal_count,
        "term_fixed": term_fixed,
        "pop_size": pop_size,
    }
    return parse_standard_seeds(data, file_path, experiment_name, fitness_function, meta)


def parse_stress_l1(data: dict, file_path: Path) -> list[dict]:
    """stress_L1_data.json has top-level keys: level, level_name, config, seeds."""
    experiment_name = "stress_L1"
    fitness_function = "log-precision"
    config = data.get("config", {})
    meta = {
        "terminal_count": data.get("level") or config.get("terminal_count"),
        "term_fixed": config.get("term_fixed"),
        "pop_size": config.get("pop_size"),
    }
    return parse_standard_seeds(data, file_path, experiment_name, fitness_function, meta)


def parse_fitness_approach(data: dict, file_path: Path, experiment_name: str) -> list[dict]:
    """fitness_approachN_*.json: keys: approach, weight, config, seeds."""
    fitness_function = "log-precision"
    config = data.get("config", {})
    meta = {
        "terminal_count": config.get("terminal_count") or config.get("terminals_n"),
        "term_fixed": config.get("term_fixed"),
        "pop_size": config.get("pop_size"),
    }
    return parse_standard_seeds(data, file_path, experiment_name, fitness_function, meta)


def parse_parsimony(data: dict, file_path: Path, experiment_name: str) -> list[dict]:
    """
    parsimony_lp*_data.json: top-level keys include config, seeds.
    Seeds have 'node_count' field.
    """
    fitness_function = "log-precision"
    config = data.get("config", {})
    meta = {
        "terminal_count": config.get("terminal_count") or config.get("terminals_n"),
        "term_fixed": config.get("term_fixed"),
        "pop_size": config.get("pop_size"),
    }
    return parse_standard_seeds(data, file_path, experiment_name, fitness_function, meta)


def parse_eda_gp(data: dict, file_path: Path) -> list[dict]:
    """
    EDA/gp-leibniz/evolution_data.json.
    Seeds: seed, generations, best_fitness, best_expr, elapsed, is_equivalent, ...
    No terminal_count/pop_size at top level — read from config.
    """
    experiment_name = "eda_gp_v1"
    fitness_function = "convergence-aware"
    config = data.get("config", {})
    meta = {
        "terminal_count": config.get("terminal_count") or config.get("terminals_n"),
        "term_fixed": config.get("term_fixed"),
        "pop_size": config.get("pop_size"),
    }
    seeds = data.get("seeds", [])
    records = []
    for s in seeds:
        if not isinstance(s, dict):
            continue
        seed_val = s.get("seed") or s.get("seed_val")
        best_expr = s.get("best_expr", "")
        is_equiv = bool(s.get("is_equivalent", False))
        best_fitness = s.get("best_fitness")
        record = {
            "id": f"expr_{experiment_name}_seed{seed_val}",
            "experiment": experiment_name,
            "fitness_function": fitness_function,
            "terminal_count": meta["terminal_count"],
            "terminal_set": str(meta["term_fixed"]) if meta["term_fixed"] is not None else None,
            "pop_size": meta["pop_size"],
            "seed": seed_val,
            "generations": s.get("generations"),
            "elapsed_seconds": s.get("elapsed"),
            "raw_form": best_expr,
            "simplified_form": simplify_expr(best_expr),
            "nodes": count_nodes(best_expr),
            "fitness_score": best_fitness,
            "is_leibniz": is_equiv,
            "is_monotone": bool(s.get("is_monotone", False)),
            "classification": classify(best_expr, is_equiv, best_fitness),
            "source_file": str(file_path),
        }
        records.append(record)
    return records


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def parse_data_file(file_path: Path) -> list[dict]:
    """
    Load one *_data.json file and return a list of expression records.
    Returns empty list (with warning) on failure.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:  # noqa: BLE001
        print(f"  WARNING: could not load {file_path}: {exc}", file=sys.stderr)
        return []

    name = file_path.stem.removesuffix("_data")
    path_str = str(file_path)

    # --- EDA files: different schemas ---
    if "EDA/rl-leibniz" in path_str or "EDA\\rl-leibniz" in path_str:
        print(f"  SKIP (RL schema): {file_path.name}")
        return []

    if "EDA/aco-leibniz" in path_str or "EDA\\aco-leibniz" in path_str:
        print(f"  SKIP (ACO schema): {file_path.name}")
        return []

    if "EDA/gp-leibniz" in path_str or "EDA\\gp-leibniz" in path_str:
        print(f"  PARSE (EDA GP v1): {file_path.name}")
        return parse_eda_gp(data, file_path)

    # --- Special entropy v1 ---
    if file_path.name == "entropy_data.json":
        print(f"  PARSE (entropy v1): {file_path.name}")
        return parse_entropy_v1(data, file_path)

    # --- stress_L1 ---
    if file_path.name == "stress_L1_data.json":
        print(f"  PARSE (stress L1): {file_path.name}")
        return parse_stress_l1(data, file_path)

    # --- fitness_approach files ---
    if "fitness_approach" in file_path.name:
        print(f"  PARSE (fitness approach): {file_path.name}")
        return parse_fitness_approach(data, file_path, name)

    # --- parsimony files ---
    if file_path.name.startswith("parsimony_"):
        print(f"  PARSE (parsimony): {file_path.name}")
        return parse_parsimony(data, file_path, name)

    # --- Standard v3 schema (scaling_heatmap, gp_scaling, gp_extended, stress) ---
    if "seeds" not in data:
        print(f"  SKIP (no seeds key): {file_path.name}", file=sys.stderr)
        return []

    fitness_function = infer_fitness_function(file_path)
    meta = extract_top_level_meta(data, file_path)

    print(f"  PARSE (standard): {file_path.name} | ff={fitness_function} | t={meta['terminal_count']} | pop={meta['pop_size']}")
    return parse_standard_seeds(data, file_path, name, fitness_function, meta)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    all_records: list[dict] = []
    processed_files = 0
    skipped_files = 0

    for scan_dir_rel in SCAN_DIRS:
        scan_dir = PROJECT_ROOT / scan_dir_rel
        if not scan_dir.exists():
            print(f"WARN: scan dir not found: {scan_dir}", file=sys.stderr)
            continue
        data_files = sorted(scan_dir.rglob("*_data.json"))
        print(f"\n=== {scan_dir_rel}: {len(data_files)} files ===")
        for fp in data_files:
            records = parse_data_file(fp)
            if records:
                all_records.extend(records)
                processed_files += 1
            else:
                skipped_files += 1

    # ---------------------------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------------------------
    total = len(all_records)
    leibniz_count = sum(1 for r in all_records if r["is_leibniz"])
    wrong_limit = sum(1 for r in all_records if r["classification"] == "wrong-limit-attractor")
    trivial = sum(1 for r in all_records if r["classification"] == "trivial")

    print(f"\n{'='*60}")
    print(f"Total expression records : {total}")
    print(f"  Leibniz-equivalent     : {leibniz_count}")
    print(f"  Wrong-limit attractor  : {wrong_limit}")
    print(f"  Trivial                : {trivial}")
    print(f"Files processed          : {processed_files}")
    print(f"Files skipped            : {skipped_files}")
    print(f"{'='*60}")

    # ---------------------------------------------------------------------------
    # Write output
    # ---------------------------------------------------------------------------
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "metadata": {
                    "total_records": total,
                    "leibniz_equivalent": leibniz_count,
                    "wrong_limit_attractor": wrong_limit,
                    "trivial": trivial,
                    "files_processed": processed_files,
                    "files_skipped": skipped_files,
                },
                "records": all_records,
            },
            f,
            indent=2,
        )
    print(f"\nCatalog written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
