# CC Task: Agent Swarm End-to-End Test — Write the Methods Section

**Date:** 2026-03-17
**Project:** leibniz-pi (`/Users/brock/Documents/GitHub/ai-demos/leibniz-pi`)
**Depends on:** `2026-03-17_register_agent_roles_workflows.md` (must complete first)
**Goal:** End-to-end test of AD-014 agent swarm workflow. Use CC agent teams to write the Methods section of the leibniz-pi paper using specialist roles from the Seldon graph.

---

## Prerequisites

1. Agent roles and workflows are registered in the graph (previous CC task completed)
2. `seldon go --brief` shows the Agent Roles and Workflows sections
3. CC agent teams enabled: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` set to `"1"` in settings.json
4. CC version >= 2.1.32: `claude --version`
5. Neo4j running locally

## Context for the Lead

The lead agent needs to understand:
- This is a **Seldon-managed research project**
- Paper sections live in `paper/sections/`
- The Methods section is `paper/sections/03_methods.md` — it has scaffolding content that needs to be rewritten as publication-quality prose
- All numeric values MUST use `{{result:NAME:value}}` references, never literals
- Writing conventions are in `paper/conventions.md` — every teammate must read this
- Results are queryable via `seldon result list` and `seldon result trace <id>`
- Prose quality is checked via `seldon paper audit paper/sections/03_methods.md`
- The argument structure and evidence comes from the Seldon graph

## The Prompt

Run this from the leibniz-pi project root (`cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`):

```
claude
```

Then give the lead this prompt:

---

Create an agent team to write the Methods section of this research paper. This is a Seldon-managed project — run `seldon go --brief` first to get the full project context including agent role definitions.

The Methods section is at `paper/sections/03_methods.md`. It has scaffolding that needs to be rewritten as publication-quality academic prose.

**Team structure** (use the role definitions from `seldon go` output):

Spawn 4 teammates:

1. **Methods specialist** — spawn with the `methods` role system prompt from `seldon go`. Their job: rewrite each subsection of 03_methods.md with accurate methodology documentation. They must read the actual scripts in `entropy-leibniz-v3/` and `gp-leibniz-v3/` to verify parameters match what the code does. Use `seldon result list` and `seldon result trace` for all numeric values. Every number must use `{{result:NAME:value}}` syntax.

2. **Verifier** — spawn with the `verifier` role system prompt from `seldon go`. Their job: after the methods writer finishes each subsection, verify every `{{result:NAME:value}}` reference resolves, every claimed parameter matches the source code, and every provenance chain is complete. Run `seldon paper audit paper/sections/03_methods.md`. Create ResearchTasks for any gaps found via `seldon task create`.

3. **Writer** — spawn with the `writer` role system prompt from `seldon go`. Their job: take the methods specialist's technically-accurate draft and polish it into clean academic prose. Must read `paper/conventions.md` first. No em dashes. No inline bold. Max 35 words per sentence. Active voice. "We" throughout. Run `seldon paper audit` on their own output.

4. **Red team** — spawn with the `red_team` role system prompt from `seldon go`. Their job: read the final Methods section and find problems. Are there unstated assumptions? Does the experimental design description match what was actually done? Are there claims that sound plausible but aren't backed by artifacts? Report all issues as ResearchTasks.

**Task sequence:**
1. All teammates: read `paper/conventions.md` and `RESEARCH_NOTES.md`
2. Methods specialist: rewrite 03_methods.md subsections (3.1, 3.2, 3.3)
3. Verifier: verify the draft (depends on task 2)
4. Writer: polish prose (depends on task 3)
5. Red team: final review (depends on task 4)
6. Writer: incorporate red team fixes (depends on task 5)

**Important rules:**
- Do NOT rerun any experiments
- Do NOT write literal numbers — always `{{result:NAME:value}}`
- Read `paper/conventions.md` before writing anything
- The existing scaffolding in 03_methods.md has useful content — preserve the technical substance while improving the prose
- Each teammate owns their phase. Don't let the lead implement anything directly.

Wait for all teammates to complete before synthesizing. Use delegate mode (Shift+Tab) to stay in coordination-only mode.

---

## What to Observe

This is a test. Pay attention to:

1. **Did `seldon go` successfully provide role definitions to the lead?** If not, the registration task didn't work.
2. **Did the lead correctly use the system prompts as spawn prompts?** The role definitions from the graph should become the teammate instructions.
3. **Did the task sequencing work?** Methods → Verify → Polish → Red Team → Fix
4. **Did teammates actually use `seldon` CLI?** Check if they ran `seldon result list`, `seldon paper audit`, etc.
5. **Did the verifier catch real issues?** Or did it rubber-stamp?
6. **Did the red team find anything the others missed?**
7. **What was the token cost?** Note approximate usage.
8. **What broke?** File conflicts, task status lag, teammates going off-script, lead implementing instead of delegating?

## After the Test

Write findings to `handoffs/2026-03-17_swarm_test_results.md` covering:
- What worked
- What didn't
- Role definition quality (too vague? too prescriptive? missing context?)
- Workflow decomposition quality
- Whether the `seldon go` → spawn prompt pipeline is viable
- Recommendations for role/workflow artifact revisions
- Token cost observations

Update any stale AgentRole or Workflow artifacts based on findings:
```bash
seldon artifact update <id-prefix> -p state=stale
```

## Success Criteria

1. Methods section is rewritten with publication-quality prose
2. All `{{result:NAME:value}}` references are valid
3. `seldon paper audit paper/sections/03_methods.md` passes Tier 1 (structural)
4. Red team issues are logged as ResearchTasks in the graph
5. Handoff document captures findings for AD-014 iteration

## Do NOT

- Do not modify the seldon engine or schema
- Do not rerun experiments
- Do not modify other paper sections (only 03_methods.md)
- Do not skip the observation/findings step — this is a test, the findings are as valuable as the prose
