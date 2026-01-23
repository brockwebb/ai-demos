# Appendix: Implementation Templates

These templates are for practitioners ready to implement. Copy, adapt, and use.

They align with 2025-2026 industry practice for bounded AI agents in enterprise and government settings.

---

## 1. Agent Mission & Scope One-Pager

**Title:** `[Agent Name] – Mission & Scope`

### 1. Mission (1-2 sentences)
- Purpose: What this agent is for, in business terms.
- Example: "Assist survey analysts by flagging inconsistent records and drafting human-readable rationales; never modify source data."

### 2. Intended Users & Context
- Primary users/teams:
- Processes this agent supports:
- Systems it interfaces with:

### 3. Risk Tier & Autonomy Mode

**Risk tier:** ☐ Low ☐ Medium ☐ High

Explain why, referencing impact on people/resources/compliance.

**Autonomy mode** (pick one per main action type):
- ☐ Auto-execute (low risk, reversible)
- ☐ Suggest-then-approve (human must approve)
- ☐ Human-initiated, agent-assisted (agent only helps)

### 4. Scope – What the Agent May / May Not Do

**May access** (data domains, systems, fields):
- Example: "Read-only access to survey response tables and codebooks; no access to PII beyond [fields]."

**May take actions** (verbs):
- Example: "Propose edit flags, draft rationales, draft emails for analysts to send."

**Must not do:**
- Example: "Cannot commit edits to production DB, cannot send external emails, cannot change weights or imputation parameters."

### 5. Guardrails & Constraints

- Policy constraints (legal, statistical, confidentiality):
- Technical constraints (rate-limits, step-limits, tool whitelist):
- Oversight mechanisms:
  - Who reviews outputs?
  - How are overrides logged?

### 6. Success Criteria & Metrics

- Primary success metrics (e.g., precision/recall vs. human baseline, time saved, override rate):
- Target thresholds (e.g., "≥90% of auto-flags accepted by analysts on low-risk categories"):

---

## 2. Process Map Worksheet

**Title:** `[Workflow Name] – AI-Augmentation Worksheet`

Use with field reps, analysts, or program staff in a workshop setting.

### Step 1 – Describe the current process

| Step ID | Step Name | Who Does It? | Inputs | Outputs | Risk Tier (L/M/H) |
|---------|-----------|--------------|--------|---------|-------------------|
| | | | | | |
| | | | | | |
| | | | | | |

### Step 2 – Identify candidate "AI spots"

| Step ID | Repetitive? (Y/N) | Heavy Reading/Context? (Y/N) | Could AI Help? (Describe) |
|---------|-------------------|------------------------------|---------------------------|
| | | | |
| | | | |
| | | | |

Highlight rows with many "Y" answers. These are candidates for AI augmentation.

### Step 3 – Assign minimal technology

| Step ID | Pattern | Tech Choice |
|---------|---------|-------------|
| | A – LLM as lens (summarize/explain) | Prompt-only / RAG |
| | B – LLM as recommender (flags, routing) | Prompt-only initially; bounded agent if multi-step |
| | C – LLM as actor (tool calls) | Bounded agent via framework |

---

## 3. Tool Catalog & Policy Sheet

**Title:** `[System Name] – AI Tool Catalog`

For each tool callable by any agent:

| Field | Description |
|-------|-------------|
| Tool ID | Unique identifier |
| Name | Human-readable name |
| Description | What it does |
| Allowed agents/roles | Who can call this tool |
| Inputs (schema) | Expected input format |
| Outputs (schema) | Expected output format |
| Preconditions | Business rules and access policies (e.g., "only for de-identified records") |
| Postconditions | What must be true after the tool runs (e.g., "ticket updated with timestamp") |
| Risk tier | Low/Medium/High |
| Logging requirements | What must be captured for audit |

**Guidance:**
- Preconditions: business rules and access policies
- Postconditions: what must be true after the tool runs
- Logging requirements: what must be captured for audit (actor, time, inputs, outputs, decision rationale)

---

## 4. Risk & Human-Oversight Checklist

**Title:** `[Agent Name] – Risk & Human-Oversight Checklist`

Use as a yes/no checklist before deployment.

### A. Impact & Compliance

- [ ] Have we run an AI impact/risk assessment referencing NIST AI RMF or similar?
- [ ] Are individuals' rights, benefits, or obligations affected by this agent's outputs?
- [ ] If yes, is the agent classified as high-risk under any applicable law or internal standard?

### B. Human Oversight Design

- [ ] For high-risk decisions, does a human review outputs before execution?
- [ ] Can a human override or ignore the agent's suggestions at any time?
- [ ] Is there a documented escalation path for appeals or contested decisions?
- [ ] Do users understand the agent's limitations and know they're interacting with AI?

### C. Confidence & Routing

- [ ] Does the agent produce a confidence score or uncertainty marker for key actions?
- [ ] Are there explicit thresholds where outputs must be sent to a human (e.g., confidence <0.75)?
- [ ] Are specific keywords/patterns (e.g., "appeal", "fraud") always routed to human review?

### D. Logging & Traceability

- [ ] Are all actions logged with: agent ID, tool ID, inputs, outputs, timestamps, user IDs?
- [ ] Can we reconstruct the sequence of steps that led to any given decision?
- [ ] Is there a rollback or kill-switch mechanism?

---

## 5. Evaluation Sheet

**Title:** `[Agent/Workflow Name] – Evaluation Plan`

### 1. Objectives

What are we trying to improve?
- Example: reduce analyst time per flagged case, improve precision of flags, shorten resolution time

### 2. KPIs and Targets

| Metric | Definition | Target |
|--------|------------|--------|
| | | |
| | | |
| | | |

Common metrics:
- Accuracy/precision/recall vs. human gold-standard
- Override rate (how often humans reject agent suggestions)
- Time saved per case

### 3. Offline Test Set

- Source (e.g., past cases with known decisions):
- Size and sampling strategy:
- Red-team cases (deliberately hard or adversarial examples):

### 4. Online Monitoring

- What do we log live?
- How often do we re-evaluate metrics and thresholds?

### 5. Acceptance Criteria

Example: "We will move from suggest-only to auto-execute for low-risk actions when: precision ≥X%, override rate ≤Y% for Z weeks."

---

## 6. Change Log Template

**Title:** `[Agent/Workflow Name] – Change Log`

| Date | Change Type | Description | Reason | Affected Metrics/Risks | Owner | Status |
|------|-------------|-------------|--------|------------------------|-------|--------|
| | prompt/model/workflow/tool/policy | | | | | planned/rolled out/rolled back |
| | | | | | | |
| | | | | | | |

Keep changes auditable and link them to evaluation results and risk assessments.

---

## 7. Non-Technical Training Handouts

### Handout A – "How to Describe a Good Agent"

Fill in the blanks:

> As a **[role]**, I want the agent to **[narrow outcome]** so that **[business value]**.
>
> The agent is allowed to see: **[systems/data types]**
>
> The agent is allowed to do: **[actions, e.g., propose flags, draft responses]**
>
> The agent must never: **[forbidden actions]**
>
> If the agent is unsure or the decision is high stakes, it must: **[who to ask / how to escalate]**

### Handout B – "How to Review Agent Behavior"

For any agent suggestion, ask:

1. Did it stay within its job description and data boundaries?
2. Is the action correct in context?
3. Is the rationale understandable?
4. Would I sign my name under this action?

If "no" to any, mark as **"bad example"** and send to the technical team with a screenshot or copy. This creates a growing test set for evaluation.

---

## Using These Templates

**Minimum viable documentation** for any agent:

1. Mission & Scope one-pager (Template 1)
2. Risk & HITL checklist completed (Template 4)
3. Change log started (Template 6)

**For production agents, add:**

4. Tool catalog for all callable tools (Template 3)
5. Evaluation plan with offline test set (Template 5)

**For workshop-based design with non-technical staff:**

- Process Map Worksheet (Template 2)
- Training Handouts A & B (Template 7)

These templates encode the same principles described in this document: bounded agency, confidence-based routing, human oversight, and auditability.
