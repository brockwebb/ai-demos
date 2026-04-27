# CC Task: Triage and Close Stale Seldon Tasks

**Date:** 2026-03-28
**Scope:** Review all 18 open (proposed) Seldon tasks, close those that are completed or no longer relevant, leave genuinely open items

---

## Pre-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon task list --open
```

Capture the full list of open tasks with their IDs and descriptions.

---

## Triage Criteria

For each open task, apply this decision tree:

1. **Already done?** Check if the work described has been completed (e.g., paper section written, experiment run, fix applied). If yes → close with status note.
2. **Superseded?** Has the paper's framing changed such that this task is no longer relevant? If yes → close with explanation.
3. **Out of scope?** Is this a future experiment or speculative idea that is NOT needed for the current paper? If yes → close as "deferred/out-of-scope."
4. **Still needed?** If the task describes work genuinely needed for the paper as it stands → leave open.

---

## Expected Dispositions

Based on the task descriptions from the Seldon orient output, here are expected dispositions. Verify each against current state before closing.

### Close as COMPLETED or SUPERSEDED

| Task Description (truncated) | Reason |
|------------------------------|--------|
| "Rewrite medium draft closing section" | Medium article deprioritized. Paper is the deliverable. |
| "Write academic paper targeting GECCO/EvoStar/Entropy" | Paper is written. This was the task that started it all. |
| "RED TEAM: Literal X/5 values in prose" | Check if these were fixed during audit remediation batches (cc_tasks 2026-03-26). If fixed → close. |
| "RED TEAM: Section 5.1 references 'Table 2' but tables lack Quarto cross-references" | Check if table cross-references were fixed. If fixed → close. |
| "RED TEAM: Confabulation analogy not previewed in Introduction" | Introduction was rewritten (2026-03-27) and now previews the confabulation connection. Close if present. |

### Close as DEFERRED / OUT OF SCOPE for current paper

| Task Description (truncated) | Reason |
|------------------------------|--------|
| "Implement operations-per-bit efficiency fitness" | Future experiment. Not in current paper. |
| "Formal analysis: wrong-limit attractor density as function of terminal set size" | Theoretical follow-up. Not in current paper. |
| "Formalize second-order kinetics interpretation" | Discussed qualitatively in Section 6.1. Formal treatment is future work. |
| "Vector space decomposition of fitness landscape" | Theoretical. Not in current paper. |
| "Run entropy stress test levels L2-L4" | Experiment was stopped at L1. Results documented. Not needed for paper. |
| "Test combined optimal config: pop=2000, alpha=0.5, entropy fitness, on 15-terminal" | Would be interesting but not blocking. Paper already shows 15-terminal failure is structural. |
| "Implement thermodynamic efficiency fitness" | Future experiment. Not in current paper. |
| "Backfill EDA experiment results (RL v1/v2, ACO, GP v1) as Result artifacts" | Historical experiments. Nice to have for completeness but not blocking paper. |
| "Register v3 wide/hostile clean rerun results (all 0/5) with provenance links" | Check if these were registered during provenance completion task. If not, this is low priority. |

### Verify before closing -- may still be open

| Task Description (truncated) | Action |
|------------------------------|--------|
| "RED TEAM: Search space size argument in Methods 3.1 is asserted without quantification" | Check Section 3.1. Is the search space size argument now supported? If quantified → close. If still asserted → leave open. |
| "RED TEAM: Checkpoint count confound" | Check if this was addressed in audit remediation. The log-precision fitness uses 11 checkpoints -- is this documented as a design choice vs confound? |
| "RED TEAM: Safe division and power overflow both return 1.0" | Check if this implementation detail is documented in Methods. If addressed → close. |
| "RED TEAM: Monotonicity thresholds differ between fitness functions" | Check if this is documented. If addressed → close. |

---

## Execution

For each task:

1. Read the full task description: `seldon task show {TASK_ID}` (or equivalent command)
2. If closing, verify the disposition by checking the relevant file/section
3. Close with: `seldon task update {TASK_ID} --status closed --note "REASON"`
   - Use clear close reasons: "Completed in audit remediation batch", "Superseded by paper rewrite", "Deferred: future work, not in current paper scope", etc.
4. If leaving open, add a note: `seldon task update {TASK_ID} --note "Still open: REASON"`

---

## Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon task list --open
seldon status
```

Report:
1. How many tasks were closed and why
2. How many tasks remain open and why
3. Final Seldon status summary

---

## Do NOT

- Do not create new tasks
- Do not modify any paper sections or code files
- Do not modify existing CC task files
- Do not close tasks without verifying their status against the actual files
- Do not close RED TEAM tasks unless the issue has been verifiably addressed in the paper
