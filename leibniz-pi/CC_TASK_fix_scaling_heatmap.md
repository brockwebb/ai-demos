# CC Task: Fix scaling_heatmap.py Before Re-Run

## Context
The first run of `scaling_heatmap.py --full-grid` launched all 21 cells as subprocesses simultaneously. This caused two problems:
1. CPU starvation (21 processes on 8 cores)
2. Killing the parent process did not kill the 21 child subprocesses

The script needs modifications before re-running. All changes are to `entropy-leibniz-v3/scaling_heatmap.py`.

## Pre-Work: Clean Up Stale Files

Delete ALL files matching these patterns in `entropy-leibniz-v3/`:
- `scaling_heatmap_t*_p*.log`
- `scaling_heatmap_t*_p*_data.json`
- `scaling_heatmap_t*_p*.txt`
- `scaling_heatmap_results.md`
- `progress.json`

Do NOT delete `scaling_heatmap.py` itself or any other files.

## Change 1: Load Config File

Add config loading at the top of the script. The config file is at `config/scaling_heatmap_config.json` (relative to the script directory).

```python
def load_config():
    config_path = Path(__file__).parent / "config" / "scaling_heatmap_config.json"
    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)
```

Use the config to set:
- `GRID_TERMINAL_COUNTS` from `config["grid"]["terminal_counts"]`
- `GRID_POP_SIZES` from `config["grid"]["pop_sizes"]`
- `SEED_VALS` from `config["seeds"]`
- `MAX_SEED` from `config["time_budgets"]["max_seed_seconds"]`
- `MAX_TOTAL` from `config["time_budgets"]["max_total_seconds"]`
- `MAX_WORKERS` from `config["parallelism"]["max_workers"]`
- `PRIOR_RESULTS` from `config["prior_results"]["cells"]`

The CLI `--terminals` and `--pop_size` args should still work for single-cell runs, overriding the config for those values.

Update `N_SEEDS` to be `len(SEED_VALS)`.

## Change 2: Eliminate Subprocesses — Run Cells In-Process

**This is the critical fix.** The current `run_full_grid()` spawns each cell as a `subprocess.run()` call. This prevents clean termination.

Replace with in-process execution via multiprocessing Pool workers:

```python
def run_cell_inprocess(args):
    """Worker function: runs one cell in-process (no subprocess)."""
    t_n, p_s = args
    # Redirect stdout to log file
    log_file = OUT_DIR / f"scaling_heatmap_t{t_n}_p{p_s}.log"
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    try:
        with open(log_file, "w") as lf:
            sys.stdout = lf
            sys.stderr = lf
            main_single(t_n, p_s)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    # Return result summary
    data = load_cell_data(t_n, p_s)
    n_found = data.get("n_found", "?") if data else "?"
    return (t_n, p_s, n_found)


def run_full_grid():
    config = load_config()
    max_workers = config["parallelism"]["max_workers"]
    terminal_counts = config["grid"]["terminal_counts"]
    pop_sizes = config["grid"]["pop_sizes"]
    prior_cells = {(c["terminals"], c["pop_size"]) for c in config["prior_results"]["cells"]}
    
    # Build cell list, skipping prior results
    cells = []
    for t in terminal_counts:
        for p in pop_sizes:
            if (t, p) not in prior_cells:
                cells.append((t, p))
    
    print(f"\n[FULL GRID] {len(cells)} cells to run, {len(prior_cells)} from prior results", flush=True)
    print(f"  Max workers: {max_workers}", flush=True)
    print(f"  MAX_SEED: {MAX_SEED:.0f}s, MAX_TOTAL: {MAX_TOTAL:.0f}s per cell", flush=True)
    
    with multiprocessing.Pool(processes=max_workers) as pool:
        results = pool.map(run_cell_inprocess, cells)
    
    print(f"\n[FULL GRID] All {len(cells)} cells complete.", flush=True)
    for t_n, p_s, nf in results:
        print(f"  t={t_n:>2} p={p_s:>4}: {nf}/5", flush=True)
    
    write_grid_results_md()
```

Remove the old `run_cell()` function that used `subprocess.run()`. Remove the `import subprocess` if no longer needed.

**IMPORTANT:** The `setup_globals()` function modifies module-level globals (TERM_FIXED, ALL_TERMINALS, POP_SIZE). In a multiprocessing Pool with fork, each worker gets its own copy of the module globals. `main_single()` calls `setup_globals()` first, so each worker will have the correct values. This should work on macOS/Linux with fork. However, if the platform uses spawn (macOS default for Python 3.8+), the globals will be re-initialized from the module-level defaults. 

**Fix for spawn safety:** In `main_single()`, ensure `setup_globals()` is called BEFORE any fitness computation. It already does this — verify it's the first substantive call. Also ensure `_fitness_cache` is cleared in `setup_globals()` (it already is).

Actually, on macOS with Python 3.8+, the default start method is `spawn`. This means each worker process re-imports the module from scratch. `setup_globals()` in `main_single()` will set the correct values. The `_fitness_cache = {}` reset in `setup_globals()` handles cache isolation. This should be fine.

## Change 3: Track Stop Reason Per Seed

In `run_seed()`, record why the seed stopped. Add a `stop_reason` field to the returned dict:

- `"early_stop_converged"` — when the early-stop condition fires (info >= 13.0 and monotone)
- `"time_limit_seed"` — when `elapsed_seed >= max_time`
- `"time_limit_total"` — when `elapsed_total >= MAX_TOTAL`

Currently the function just breaks out of the loop. Add a variable `stop_reason = None` before the loop, set it at each break point, and include it in the return dict.

Also include `stop_reason` in the per-seed entries in `write_results()` JSON output and text output.

## Change 4: Update Time Budget Defaults

Change the module-level defaults to match the config:
- `MAX_SEED = 1800.0`
- `MAX_TOTAL = 10800.0`

These are overridden by config when loaded, but the defaults should match for single-cell runs without config.

## Change 5: Update GRID_CELLS

Replace the hardcoded `GRID_CELLS` list with dynamic generation from config in `run_full_grid()`. Remove the `GRID_CELLS` module-level constant.

## Change 6: Update write_grid_results_md() to Use Config

The function should load the config to get terminal_counts, pop_sizes, and prior_results instead of hardcoding them. The PRIOR dict should be built from `config["prior_results"]["cells"]`.

## Change 7: Print Cell Progress to Console

Since stdout is redirected to log files in workers, add progress printing to the parent process. After `pool.map()` returns, that's handled. But for real-time progress, consider using `pool.imap_unordered()` instead of `pool.map()` so we can print as each cell completes:

```python
with multiprocessing.Pool(processes=max_workers) as pool:
    results = []
    for result in pool.imap_unordered(run_cell_inprocess, cells):
        t_n, p_s, nf = result
        print(f"  [DONE] t={t_n:>2} p={p_s:>4}: {nf}/5 "
              f"({len(results)+1}/{len(cells)} complete)", flush=True)
        results.append(result)
```

## Verification After Changes

Before running `--full-grid`, test a single cell:
```bash
cd entropy-leibniz-v3
python3 scaling_heatmap.py --terminals 4 --pop_size 1000
```

This should:
1. Load the config file successfully
2. Run 5 seeds with the correct terminal set
3. Produce `scaling_heatmap_t4_p1000.txt` and `scaling_heatmap_t4_p1000_data.json`
4. Include `stop_reason` in the JSON output

Expected result: 5/5 (matches prior). This validates the script still works correctly.

Then run the full grid:
```bash
python3 scaling_heatmap.py --full-grid
```

Verify:
- Only 5 processes running at a time (check with `ps aux | grep scaling`)
- Console shows progress as cells complete
- Killing the parent kills all workers

## Files to Copy into Repo

Before running, copy these files from Claude's computer to the user's repo:

1. `config/scaling_heatmap_config.json` → `entropy-leibniz-v3/config/scaling_heatmap_config.json`
2. `scaling_heatmap_methodology.md` → `entropy-leibniz-v3/scaling_heatmap_methodology.md`
