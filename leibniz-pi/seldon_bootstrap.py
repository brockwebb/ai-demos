#!/usr/bin/env python3
"""
Seldon Dogfood: Batch registration for leibniz-pi project.

Calls Seldon's internal Python API directly — no CLI UUID copy-paste.
All artifacts are created in-process with cross-references resolved by name.

Usage:
    cd ~/Documents/GitHub/ai-demos/leibniz-pi
    seldon init leibniz-pi          # Run once to create project
    python seldon_bootstrap.py      # Run this script
    seldon briefing                 # Verify it worked
"""

import sys
from pathlib import Path

# Ensure seldon is importable
seldon_repo = Path.home() / "Documents" / "GitHub" / "seldon"
if str(seldon_repo) not in sys.path:
    sys.path.insert(0, str(seldon_repo))

from seldon.config import load_project_config, get_neo4j_driver, start_session
from seldon.core.artifacts import create_artifact, create_link, transition_state
from seldon.domain.loader import load_domain_config

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

PROJECT_DIR = Path.cwd()
config = load_project_config(PROJECT_DIR)
driver = get_neo4j_driver(config)
database = config["neo4j"]["database"]

domain_yaml = seldon_repo / "seldon" / "domain" / "research.yaml"
domain_config = load_domain_config(domain_yaml)

session_id = start_session(PROJECT_DIR)
print(f"Session started: {session_id}")

# Registries: name → UUID (built as we go)
scripts = {}
datafiles = {}
results = {}
tasks = {}
sections = {}


def reg_script(name: str, path: str, description: str) -> str:
    """Register a Script artifact, return its UUID."""
    uid = create_artifact(
        project_dir=PROJECT_DIR, driver=driver, database=database,
        domain_config=domain_config, artifact_type="Script",
        properties={"name": name, "path": path, "description": description},
        actor="human", authority="accepted", session_id=session_id,
    )
    scripts[name] = uid
    print(f"  Script: {name} → {uid[:8]}...")
    return uid


def reg_datafile(name: str, path: str, description: str) -> str:
    """Register a DataFile artifact, return its UUID."""
    uid = create_artifact(
        project_dir=PROJECT_DIR, driver=driver, database=database,
        domain_config=domain_config, artifact_type="DataFile",
        properties={"name": name, "path": path, "description": description},
        actor="human", authority="accepted", session_id=session_id,
    )
    datafiles[name] = uid
    print(f"  DataFile: {name} → {uid[:8]}...")
    return uid


def reg_result(
    name: str, value: float, units: str, description: str,
    script_name: str = None, datafile_names: list = None,
) -> str:
    """Register a Result artifact with optional provenance links resolved by name."""
    uid = create_artifact(
        project_dir=PROJECT_DIR, driver=driver, database=database,
        domain_config=domain_config, artifact_type="Result",
        properties={
            "name": name, "value": value, "units": units,
            "description": description,
        },
        actor="human", authority="accepted", session_id=session_id,
    )
    results[name] = uid

    if script_name and script_name in scripts:
        create_link(
            project_dir=PROJECT_DIR, driver=driver, database=database,
            domain_config=domain_config,
            from_id=uid, to_id=scripts[script_name],
            from_type="Result", to_type="Script",
            rel_type="generated_by", actor="human", authority="accepted",
            session_id=session_id,
        )
        print(f"  Result: {name} = {value} {units} → {uid[:8]}... (→ {script_name})")
    else:
        print(f"  Result: {name} = {value} {units} → {uid[:8]}...")

    if datafile_names:
        for df_name in datafile_names:
            if df_name in datafiles:
                create_link(
                    project_dir=PROJECT_DIR, driver=driver, database=database,
                    domain_config=domain_config,
                    from_id=uid, to_id=datafiles[df_name],
                    from_type="Result", to_type="DataFile",
                    rel_type="computed_from", actor="human", authority="accepted",
                    session_id=session_id,
                )

    return uid


def verify_result(name: str):
    """Transition a result from proposed → verified (via accepted if needed)."""
    uid = results[name]
    # Results start as 'proposed' per the state machine. Move to verified.
    transition_state(
        project_dir=PROJECT_DIR, driver=driver, database=database,
        domain_config=domain_config, artifact_id=uid,
        artifact_type="Result", current_state="proposed", new_state="verified",
        actor="human", authority="accepted", session_id=session_id,
    )
    print(f"  Verified: {name}")


def reg_task(name: str, description: str, blocks_results: list = None) -> str:
    """Register a ResearchTask with optional blocks links to Result artifacts."""
    uid = create_artifact(
        project_dir=PROJECT_DIR, driver=driver, database=database,
        domain_config=domain_config, artifact_type="ResearchTask",
        properties={"name": name, "description": description},
        actor="human", authority="accepted", session_id=session_id,
    )
    tasks[name] = uid

    if blocks_results:
        for r_name in blocks_results:
            if r_name in results:
                create_link(
                    project_dir=PROJECT_DIR, driver=driver, database=database,
                    domain_config=domain_config,
                    from_id=uid, to_id=results[r_name],
                    from_type="ResearchTask", to_type="Result",
                    rel_type="blocks", actor="human", authority="accepted",
                    session_id=session_id,
                )
    # Also link to PaperSection if specified
    if blocks_results:
        for s_name in blocks_results:
            if s_name in sections:
                create_link(
                    project_dir=PROJECT_DIR, driver=driver, database=database,
                    domain_config=domain_config,
                    from_id=uid, to_id=sections[s_name],
                    from_type="ResearchTask", to_type="PaperSection",
                    rel_type="blocks", actor="human", authority="accepted",
                    session_id=session_id,
                )

    print(f"  Task: {name} → {uid[:8]}...")
    return uid


def reg_section(name: str, description: str) -> str:
    """Register a PaperSection artifact."""
    uid = create_artifact(
        project_dir=PROJECT_DIR, driver=driver, database=database,
        domain_config=domain_config, artifact_type="PaperSection",
        properties={"name": name, "description": description},
        actor="human", authority="accepted", session_id=session_id,
    )
    sections[name] = uid
    print(f"  PaperSection: {name} → {uid[:8]}...")
    return uid


def link_result_to_section(result_name: str, section_name: str):
    """Create a CITES link from a PaperSection to a Result."""
    if result_name in results and section_name in sections:
        create_link(
            project_dir=PROJECT_DIR, driver=driver, database=database,
            domain_config=domain_config,
            from_id=sections[section_name], to_id=results[result_name],
            from_type="PaperSection", to_type="Result",
            rel_type="cites", actor="human", authority="accepted",
            session_id=session_id,
        )


# ===========================================================================
# PHASE 1: Scripts
# ===========================================================================
print("\n=== Registering Scripts ===")

reg_script("entropy_v3_minimal",
           "entropy-leibniz-v3/entropy_leibniz_v3_minimal.py",
           "Entropy fitness, minimal terminals {k,1,-1,2}, no injection, 5 seeds")

reg_script("gp_v3_minimal",
           "gp-leibniz-v3/gp_leibniz_v3_minimal.py",
           "GP convergence fitness, minimal terminals {k,1,-1,2}, no injection, 5 seeds")

reg_script("gp_sensitivity_sweep",
           "gp-leibniz-v3/gp_sensitivity_sweep.py",
           "Parameterized GP sensitivity sweep: alpha, lambda_p, pop_size, tournament_k")

reg_script("entropy_stress_test",
           "entropy-leibniz-v3/entropy_stress_test.py",
           "Progressive difficulty stress test for entropy fitness, levels 1-4")

reg_script("fitness_sensitivity_test",
           "entropy-leibniz-v3/fitness_sensitivity_test.py",
           "Three fitness fix approaches on 15-terminal entropy failure")

reg_script("gp_v2",
           "gp-leibniz-v2/gp_leibniz_v2.py",
           "GP v2 convergence-rate fitness, Leibniz INJECTED at gen 0 (confounded)")

reg_script("entropy_v2",
           "entropy-leibniz/entropy_leibniz.py",
           "Entropy GP v2, info-theoretic fitness, Leibniz INJECTED (confounded)")

reg_script("rl_v2",
           "EDA/rl-leibniz/rl_leibniz_v2.py",
           "RL v2 policy gradient (FAILED — diverges after T>20)")

reg_script("aco",
           "EDA/aco-leibniz/aco_leibniz.py",
           "Ant Colony Optimization (FAILED — collapses after T>40)")

# ===========================================================================
# PHASE 2: DataFiles
# ===========================================================================
print("\n=== Registering DataFiles ===")

reg_datafile("entropy_v3_minimal_data",
             "entropy-leibniz-v3/entropy_data_minimal.json",
             "Entropy v3 minimal 5-seed machine-readable data")

reg_datafile("gp_v3_minimal_convergence",
             "gp-leibniz-v3/convergence_v3_minimal.csv",
             "GP v3 minimal per-generation convergence, 5 seeds")

reg_datafile("gp_sensitivity_data",
             "gp-leibniz-v3/progress_sweep.json",
             "Full parameter sensitivity sweep data")

reg_datafile("entropy_stress_L1_data",
             "entropy-leibniz-v3/stress_L1_data.json",
             "Entropy stress test level 1 (15 terminals) per-seed data")

reg_datafile("fitness_sensitivity_data",
             "entropy-leibniz-v3/fitness_sensitivity_results.md",
             "Fitness sensitivity results across 3 approaches")

reg_datafile("v3_results_summary",
             "v3_results_summary.md",
             "Comprehensive v3 results summary with all variant comparisons")

# ===========================================================================
# PHASE 3: Results
# ===========================================================================
print("\n=== Registering Results ===")

# --- Core discovery results ---
reg_result("entropy_minimal_5_5", 1.0, "discovery_rate",
           "Entropy fitness, minimal terminals {k,1,-1,2}, no injection: 5/5 seeds found Leibniz in 369.9s total",
           script_name="entropy_v3_minimal",
           datafile_names=["entropy_v3_minimal_data"])

reg_result("gp_minimal_2_5", 0.4, "discovery_rate",
           "GP convergence fitness, minimal terminals, no injection, pop=1000: 2/5 seeds found Leibniz",
           script_name="gp_v3_minimal",
           datafile_names=["gp_v3_minimal_convergence"])

reg_result("gp_pop2000_5_5", 1.0, "discovery_rate",
           "GP convergence fitness, minimal terminals, pop=2000: 5/5 seeds. Phase transition boundary.",
           script_name="gp_sensitivity_sweep",
           datafile_names=["gp_sensitivity_data"])

reg_result("entropy_minimal_runtime", 369.9, "seconds",
           "Total runtime for entropy v3 minimal 5/5 discovery (all seeds)",
           script_name="entropy_v3_minimal")

reg_result("info_rate_3_32", 3.32, "bits_per_decade",
           "Constant information gain rate for all Leibniz-equivalent expressions. Theoretical: -log2(1/(2T+1)) rate.")

reg_result("entropy_stress_L1_0_5", 0.0, "discovery_rate",
           "Entropy fitness 0/5 at 15 terminals. Wrong-limit attractor 5/((6+4k)(k-2)) dominates.",
           script_name="entropy_stress_test",
           datafile_names=["entropy_stress_L1_data"])

# --- Wrong-limit attractor characterization ---
reg_result("wrong_limit_ti_15_93", 15.93, "bits",
           "Wrong-limit attractor 5/((6+4k)(k-2)) achieves 15.93 bits at T=10000 — EXCEEDS Leibniz (15.29). Converges to ~0.7855 != pi/4.",
           script_name="entropy_stress_test")

reg_result("leibniz_ti_10000", 15.29, "bits",
           "Leibniz series info(T=10000) = -log2(|error|) = 15.29 bits. The theoretical baseline.")

# --- GP sensitivity key results ---
reg_result("gp_alpha05_4_5", 0.8, "discovery_rate",
           "GP v3 minimal with alpha=0.5 (convergence bonus weight): 4/5 seeds.",
           script_name="gp_sensitivity_sweep")

reg_result("fitness_fix_w01_1_5", 0.2, "discovery_rate",
           "Fitness sensitivity: large-T penalty w=0.1 on 15-terminal entropy: 1/5. Only fix that found Leibniz.",
           script_name="fitness_sensitivity_test",
           datafile_names=["fitness_sensitivity_data"])

# --- Clean rerun 0/5 results ---
reg_result("gp_wide_clean_0_5", 0.0, "discovery_rate",
           "GP v3 wide (41 terminals), no injection, 55s/seed: 0/5",
           script_name="gp_v3_minimal")

reg_result("gp_hostile_clean_0_5", 0.0, "discovery_rate",
           "GP v3 hostile (no 2 in terminals), no injection: 0/5",
           script_name="gp_v3_minimal")

reg_result("entropy_wide_clean_0_5", 0.0, "discovery_rate",
           "Entropy v3 wide, no injection: 0/5",
           script_name="entropy_v3_minimal")

reg_result("entropy_hostile_clean_0_5", 0.0, "discovery_rate",
           "Entropy v3 hostile, no injection: 0/5. (-11)^-4 constant attractor dominated.",
           script_name="entropy_v3_minimal")

# --- Injection confound ---
reg_result("injection_confound", 1.0, "discovery_rate",
           "GP v2 and Entropy v2 '5/5' results were ARTIFACTS of Leibniz tree injection at gen 0. Survived via elitism, not discovered.",
           script_name="gp_v2")

# --- Verify the ones we're confident about ---
print("\n=== Verifying Results ===")
for name in [
    "entropy_minimal_5_5", "gp_minimal_2_5", "gp_pop2000_5_5",
    "entropy_minimal_runtime", "info_rate_3_32", "entropy_stress_L1_0_5",
    "wrong_limit_ti_15_93", "leibniz_ti_10000", "gp_alpha05_4_5",
    "fitness_fix_w01_1_5", "injection_confound",
    "gp_wide_clean_0_5", "gp_hostile_clean_0_5",
    "entropy_wide_clean_0_5", "entropy_hostile_clean_0_5",
]:
    verify_result(name)


# ===========================================================================
# PHASE 4: Paper Sections
# ===========================================================================
print("\n=== Registering Paper Sections ===")

reg_section("abstract",
            "Paper abstract: fitness landscape topology for infinite-horizon convergent processes")

reg_section("introduction",
            "Can ML rediscover fundamental math? Leibniz as clean test case with known answer.")

reg_section("methods",
            "GP engine, entropy fitness, convergence-rate fitness, terminal set design, experimental protocol")

reg_section("results_discovery",
            "Discovery rates: injection confound, minimal terminals, sensitivity analysis, phase transitions")

reg_section("results_attractors",
            "Wrong-limit attractor analysis: density vs terminal set size, fitness landscape topology")

reg_section("discussion_thermodynamic",
            "Information-theoretic interpretation: second-order kinetics, constant dissipation, efficiency metric")

reg_section("conclusion",
            "Generalizable insight: define success as process properties, not target proximity")


# Link key results to paper sections
print("\n=== Linking Results → Paper Sections ===")

# Results section: discovery rates
for r in ["entropy_minimal_5_5", "gp_minimal_2_5", "gp_pop2000_5_5",
          "entropy_minimal_runtime", "injection_confound",
          "gp_wide_clean_0_5", "gp_hostile_clean_0_5",
          "entropy_wide_clean_0_5", "entropy_hostile_clean_0_5"]:
    link_result_to_section(r, "results_discovery")

# Results section: attractors
for r in ["wrong_limit_ti_15_93", "leibniz_ti_10000",
          "entropy_stress_L1_0_5", "fitness_fix_w01_1_5"]:
    link_result_to_section(r, "results_attractors")

# Discussion: thermodynamic
link_result_to_section("info_rate_3_32", "discussion_thermodynamic")

# Sensitivity in methods
link_result_to_section("gp_alpha05_4_5", "methods")

print("  Linked results to paper sections.")


# ===========================================================================
# PHASE 5: Research Tasks
# ===========================================================================
print("\n=== Registering Research Tasks ===")

# Theoretical / analytical
reg_task("ops_per_bit_fitness",
         "Implement operations-per-bit efficiency fitness: info_gain / tree_complexity. Test on 15-terminal problem.",
         blocks_results=["discussion_thermodynamic"])

reg_task("attractor_density_analysis",
         "Formal analysis: wrong-limit attractor density as f(terminal set size N). Combinatorial argument for 4→5/5, 15→0/5.",
         blocks_results=["results_attractors"])

reg_task("second_order_kinetics_proof",
         "Formalize second-order kinetics interpretation: Leibniz error 1/(2T+1) as 2nd-order rate law. Prove uniqueness of constant info rate under parsimony.",
         blocks_results=["discussion_thermodynamic"])

reg_task("vector_space_decomposition",
         "Vector space decomposition of fitness landscape. Min-gradient energy dispersion analysis. IN PROGRESS.")

# Experimental
reg_task("entropy_stress_L2_L4",
         "Run entropy stress test levels L2-L4 (42, 44, 41 terminals). Stopped at L1=0/5 — may be informative with fitness fixes.")

reg_task("combined_optimal_config",
         "Test combined config: pop=2000 + alpha=0.5 + entropy fitness on 15-terminal set. Never tested — each fix was isolated.")

reg_task("thermodynamic_efficiency_fitness",
         "Implement thermodynamic efficiency fitness: constant-rate free energy dissipation. The deeper physical objective from NOTES.",
         blocks_results=["discussion_thermodynamic"])

# Writing
reg_task("medium_closing_rewrite",
         "Rewrite medium draft closing section (Not to be PI-dantic). Lists 3 properties but article establishes 2.")

reg_task("academic_paper_draft",
         "Write academic paper targeting GECCO/EvoStar/Entropy journal. Fitness landscape topology for infinite-horizon convergent processes.",
         blocks_results=["abstract", "introduction", "methods",
                         "results_discovery", "results_attractors",
                         "discussion_thermodynamic", "conclusion"])

# Provenance / cleanup
reg_task("backfill_eda_results",
         "Register EDA experiment results (RL v1/v2, ACO, GP v1) as Result artifacts with failure documentation.")

reg_task("register_v3_wide_hostile_data",
         "Register v3 wide/hostile clean rerun data files and detailed per-seed results.")


# ===========================================================================
# SUMMARY
# ===========================================================================
print("\n" + "=" * 60)
print("SELDON BOOTSTRAP COMPLETE")
print("=" * 60)
print(f"  Scripts:       {len(scripts)}")
print(f"  DataFiles:     {len(datafiles)}")
print(f"  Results:       {len(results)} ({sum(1 for _ in results)} verified)")
print(f"  PaperSections: {len(sections)}")
print(f"  Tasks:         {len(tasks)}")
print(f"  Session:       {session_id}")
print()
print("Next steps:")
print("  seldon briefing          # Verify context surfacing")
print("  seldon result list       # Check registered results")
print("  seldon task list --open  # See research frontier")
print("  seldon status            # Graph overview")
print()
print("When done exploring:")
print("  seldon closeout          # End session, write structured handoff")

driver.close()
