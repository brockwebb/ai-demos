# CC Task: Register Agent Roles & Workflows in Leibniz-Pi Graph

**Date:** 2026-03-17
**Project:** leibniz-pi (`/Users/brock/Documents/GitHub/ai-demos/leibniz-pi`)
**Depends on:** AD-014 (`/Users/brock/Documents/GitHub/seldon/docs/design/AD-014_agent_roles_as_graph_artifacts.md`)
**Goal:** Register the 6 AgentRole artifacts and 3 Workflow artifacts defined in AD-014 Section 5-6 into the `seldon-leibniz-pi` Neo4j database, with all relationship links. After this, `seldon go` should return an "Agent Roles" and "Workflows" section.

---

## Prerequisites

- `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
- Verify `seldon` CLI is on PATH: `seldon status`
- Verify Neo4j is running: `seldon artifact list` should work
- Read AD-014 for the full role/workflow specs: `/Users/brock/Documents/GitHub/seldon/docs/design/AD-014_agent_roles_as_graph_artifacts.md`

## Step 1: Verify Schema Supports AgentRole and Workflow

```bash
seldon artifact create --type AgentRole --dry-run -p name=test -p display_name=test -p system_prompt=test
```

If this fails with "unknown artifact type", the research.yaml needs updating. Check `/Users/brock/Documents/GitHub/seldon/seldon/domain/research.yaml` — AgentRole and Workflow should already be there with state machines. If missing, STOP and report.

## Step 2: Register the 6 Agent Roles

Register each role with ALL properties from AD-014 Section 5. Set state to `active` after creation.

The 6 roles are:
1. `lead` — Lead / Chief Scientist
2. `methods` — Methods & Analysis
3. `verifier` — Evidence / Verifier
4. `writer` — Prose / Writer
5. `literature` — Literature / Acquisitioner
6. `red_team` — Contrarian / Red Team

For each role:
```bash
seldon artifact create --type AgentRole \
  -p name="<n>" \
  -p display_name="<display_name>" \
  -p system_prompt="<full system prompt from AD-014 Section 5.N>" \
  -p responsibilities="<from AD-014>" \
  -p retrieval_profile="<from AD-014>" \
  -p cli_tools="<from AD-014>" \
  -p checks_performed="<from AD-014 if applicable>" \
  -p does_not_do="<from AD-014 if applicable>"
```

Then transition to active:
```bash
seldon artifact update <id-prefix> -p state=active
```

**IMPORTANT:** The `system_prompt` property contains multi-line text. If the CLI doesn't handle multi-line well via `-p`, write a small Python registration script instead that calls the Seldon API directly. The exact system prompt text is in AD-014 Sections 5.1-5.6. Copy them verbatim.

**NOTE on properties:** Some roles don't have all documentation properties (e.g., `checks_performed` is most relevant to `verifier`). Only include properties that have actual content — don't pad with empty strings.

## Step 3: Register the 3 Workflows

The 3 workflows are:
1. `write_paper_section` — Write Paper Section
2. `verification_pass` — Verification Pass
3. `documentation_audit` — Documentation Audit

For each workflow:
```bash
seldon artifact create --type Workflow \
  -p name="<n>" \
  -p display_name="<display_name>" \
  -p description="<from AD-014 Section 6.N>" \
  -p trigger="<from AD-014>" \
  -p decomposition_strategy="<from AD-014>" \
  -p success_criteria="<from AD-014>"
```

Then transition to active:
```bash
seldon artifact update <id-prefix> -p state=active
```

## Step 4: Create Relationship Links

Link workflows to their roles:

**write_paper_section** includes: lead, methods, verifier, writer, red_team
**write_paper_section** led by: lead

**verification_pass** includes: lead, verifier
**verification_pass** led by: lead

**documentation_audit** includes: lead, verifier
**documentation_audit** led by: lead

```bash
seldon link create --from <workflow-id> --to <role-id> --type includes_role
seldon link create --from <role-id> --to <workflow-id> --type leads
```

Use artifact IDs from the creation output. Partial UUID prefixes (8+ chars) should work.

## Step 5: Verify

```bash
# Should show 6 AgentRole artifacts, all active
seldon artifact list --type AgentRole

# Should show 3 Workflow artifacts, all active
seldon artifact list --type Workflow

# Should show includes_role and leads relationships
seldon link list

# Most important: seldon go should now include Agent Roles and Workflows sections
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon go --brief
```

The `seldon go` output should now have:
- `## Agent Roles` section with all 6 roles and their system prompts
- `## Workflows` section with all 3 workflows and their role lists

## Step 6: Report

Run `seldon status` and report the new node/relationship counts.

Expected: ~54 nodes (was 45), relationships increased by ~11 (8 includes_role + 3 leads).

---

## Success Criteria

1. `seldon artifact list --type AgentRole` returns 6 artifacts, all in `active` state
2. `seldon artifact list --type Workflow` returns 3 artifacts, all in `active` state
3. `seldon link list` shows `includes_role` and `leads` relationships
4. `seldon go --brief` output includes Agent Roles and Workflows sections with full system prompts

## Do NOT

- Do not modify research.yaml — the schema already supports AgentRole and Workflow
- Do not modify seldon engine code — this is purely artifact registration
- Do not change any existing artifacts or results
- Do not run any experiments
