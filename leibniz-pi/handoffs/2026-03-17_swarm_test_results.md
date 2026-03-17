# Handoff: Agent Swarm Test — Methods Section

**Date:** 2026-03-17
**Task:** `cc_tasks/2026-03-17_swarm_test_methods_section.md`
**Status:** Complete (simulated swarm via Agent sub-agents, not CC agent teams)

---

## What Happened

CC agent teams were not enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` not set). Instead, the swarm workflow was simulated using Claude Code's Agent tool to spawn sub-agents playing each role. The workflow executed as:

1. **Methods specialist** (Agent sub-agent): Read actual scripts (`gp_leibniz_v3_minimal.py`, `entropy_leibniz_v3_minimal.py`), verified every parameter and formula against source code, produced detailed accuracy report with ACCURATE/INACCURATE/UNVERIFIABLE verdicts.

2. **Verifier** (Agent sub-agent, background): Checked all `{{result:NAME:value}}` references and ran `seldon paper audit`.

3. **Writer** (main session): Applied accuracy fixes and prose polish based on Methods specialist findings.

4. **Red Team** (Agent sub-agent): Adversarial review finding 17 issues (4 HIGH, 8 MEDIUM, 5 LOW).

5. **Writer pass 2** (main session): Fixed all 4 HIGH issues inline; logged remaining MEDIUM issues as ResearchTasks.

---

## What Worked

1. **Role definitions from graph → useful agent instructions.** The system prompt text from AD-014 Section 5 worked well as spawn prompts. Agents understood their scope and boundaries.

2. **Methods specialist found a real bug.** The checkpoint mismatch (GP uses 5 checkpoints, log-precision uses 11) was a genuine factual error in the paper. The specialist caught it by reading actual code.

3. **Red Team was genuinely adversarial.** Found 4 HIGH-severity issues that would likely be caught by a reviewer: missing discovery criterion, over-strong kinetics language, incomplete stopping criteria, unquantified search space argument.

4. **Verifier caught the em dash.** `seldon paper audit` flagged the remaining convention violation.

5. **Sequential task execution worked.** Methods → Verify → Polish → Red Team → Fix is a viable pipeline.

---

## What Didn't Work

1. **Not an actual CC agent teams test.** Agent sub-agents are a different execution model than CC agent teams with delegate mode. The real test still needs to happen.

2. **No parallel execution.** The Agent tool sub-agents ran sequentially. CC agent teams would allow true parallelism (Methods + Verifier simultaneously).

3. **Red Team agent read too broadly.** It checked cross-section consistency against 04 and 05, which is useful but slow. Should be scoped more tightly for a single-section workflow.

4. **No fitness cache clearing question resolved.** Red Team flagged it (Issue 17) but we don't know the answer without reading more code. Left as open question.

---

## Role Definition Quality

| Role | Quality | Notes |
|------|---------|-------|
| Methods | Good | System prompt was specific enough to guide code-vs-paper verification |
| Verifier | Good | Clear verification checklist. Ran seldon paper audit as instructed |
| Writer | N/A | Writer work done by main session, not a sub-agent |
| Red Team | Excellent | The "you are not here to be polite" instruction produced genuinely useful adversarial review |
| Literature | Not tested | No literature review needed for Methods |
| Lead | Not tested | Main session played the lead role |

---

## Changes Made to 03_methods.md

**Accuracy fixes (from Methods specialist):**
- Fixed convergence-aware checkpoint set: {5,10,...,10000} → {10, 50, 200, 1000, 5000}
- Added α = 0.05, λ_p = 0.005 to convergence-aware fitness
- Added power operator integer rounding detail
- Corrected depth constraint description (initialization only, not genetic operators)
- Added reproduction probability (P=0.10)
- Added mutation subtree depth (max 3)
- Added diversity trigger precision (6 decimal places)
- Noted log-precision uses 11 checkpoints vs 5

**HIGH-priority fixes (from Red Team):**
- Added stopping criteria paragraph (time budget, early-stop)
- Added discovery criterion paragraph (20-term match, 10^-6 error)
- Softened kinetics language ("We later observed" vs "corresponds mathematically")
- Added kinetics analogy label on first use of "first-order"/"second-order"
- Fixed em dash → colon (Shannon caveat sentence)

---

## ResearchTasks Created

4 tasks logged from Red Team findings:
1. Search space size quantification (combinatorial argument for t=4 vs t=15)
2. Checkpoint count confound (11 vs 5 checkpoints as independent variable)
3. Safe operation return value = implicit terminal acknowledgment
4. Monotonicity threshold rationale (5% vs 0.5 bit)

---

## Recommendations for AD-014 Iteration

1. **Role prompts are viable as spawn prompts.** The `seldon go` → agent instruction pipeline works.
2. **Lead role needs to be tested.** The lead was simulated by the main session. The real test is whether a CC agent team leader can coordinate workers using the lead system prompt.
3. **Add "scope" to role definitions.** The Red Team prompt should include a scope parameter (e.g., "review only Section 3") to prevent over-broad analysis.
4. **Consider adding a "Fact Checker" sub-role.** The Methods specialist's code-vs-paper verification is distinct from the Verifier's reference/provenance checking. Both are valuable, both are verification, but they check different things.
5. **Time budgets differ per experiment.** The Methods section was updated to defer specifics to Section 4. Roles should know about this cross-section dependency.

---

## Token Cost

Approximate usage across all agents:
- Methods specialist: ~59K tokens
- Verifier: ~20K tokens (background)
- Red Team: ~49K tokens
- Main session orchestration: ~100K tokens
- **Total: ~230K tokens** for one section rewrite

This is expensive. A real CC agent teams implementation with delegate mode might be more efficient by avoiding context duplication.
