# Design Principles

These are the ideas that should stay with you after the vocabulary fades and the examples blur. If you remember nothing else, remember these.

## 1. Without Good Judgment in Upfront Design, Junk Probability Skyrockets

AI doesn't fix bad process. It accelerates it.

If your workflow is poorly defined, an agent will produce poorly defined outputs faster. If your criteria are vague, the agent will make vague decisions at scale. If you haven't thought through edge cases, the agent will hit those edge cases and do something you didn't anticipate.

The quality of agent output is bounded by the quality of agent design. No amount of model capability compensates for unclear instructions, missing constraints, or unexamined assumptions.

```mermaid
flowchart LR
    subgraph Input Quality
        Good[Clear goals<br/>Defined constraints<br/>Explicit edge cases]
        Bad[Vague goals<br/>Missing constraints<br/>Unexamined assumptions]
    end
    
    subgraph Output Quality
        GoodOut[Consistent<br/>Auditable<br/>Predictable]
        BadOut[Inconsistent<br/>Mysterious<br/>Surprising]
    end
    
    Good --> GoodOut
    Bad --> BadOut
    
    style Good fill:#d4edda
    style GoodOut fill:#d4edda
    style Bad fill:#f8d7da
    style BadOut fill:#f8d7da
```

**Practical implication:** Spend more time on design than you think you need. The time you "save" by rushing into implementation, you'll spend debugging unexpected behavior.

## 2. Autonomy Is a Governance Choice, Not a Technical Upgrade

Giving an agent more autonomy is not an improvement. It's a tradeoff.

More autonomy means more flexibility. It also means less predictability. The question isn't "how autonomous can we make this?" but "how much autonomy does this task actually require?"

Most tasks don't require much. A well-structured workflow with minimal agency often outperforms a loosely-defined agent with maximum flexibility.

**The dial, not the switch:**

```mermaid
flowchart LR
    A[No Agency<br/>Fixed script<br/>Same every time] --> B[Low Agency<br/>Small adjustments<br/>Within tight bounds] --> C[Moderate Agency<br/>Meaningful decisions<br/>Clear constraints] --> D[High Agency<br/>Open-ended<br/>Minimal guardrails]
    
    style A fill:#d4edda
    style B fill:#d1ecf1
    style C fill:#fff3cd
    style D fill:#f8d7da
```

Move right only when you have to. Stay left when you can.

**Practical implication:** Start with the least autonomy that accomplishes the goal. Add agency only when you've identified specific decisions that require it.

## 3. Most Problems Don't Need Agents (And That's Fine)

The hype cycle wants you to believe everything should be agentic. That's marketing, not engineering.

Many problems are better solved with:
- A simple prompt and a copy-paste workflow
- A traditional script with no AI at all
- A human making the decision directly

Agents add value when:
- The task has genuine variability that can't be pre-scripted
- Decisions need to be made at scale
- The cost of human attention exceeds the cost of imperfect automation

If those conditions aren't met, you don't need an agent. You need a simpler solution.

**Practical implication:** Before building an agent, ask: "What's the simplest thing that could work?" Often, that's the right answer.

## 4. The Skill Is Describing What You Want and Spotting Bad Design

You don't need to code to work with agents. But you do need to think clearly.

The core skill is **specification**: being precise about what you want, what constraints apply, what success looks like, and what should happen when things go wrong.

The second skill is **recognition**: looking at an agent workflow and spotting where it's going to fail. Where are the vague instructions? Where are the missing guardrails? Where will edge cases cause problems?

Both skills improve with practice. Neither requires a computer science degree.

**The specification checklist:**

| Question | Why It Matters |
|----------|----------------|
| What's the goal? | Agents need a target |
| What are the constraints? | Bounds prevent chaos |
| What does success look like? | You need to know when you're done |
| What should happen when it's uncertain? | Silence is not a strategy |
| How will you know if it's wrong? | You need feedback loops |

**Practical implication:** Practice writing prompts that are unambiguous. Show them to someone else. If they interpret them differently than you intended, the agent will too.

### Quick Reference: Describing an Agent

When you need to specify what an agent should do, fill in these blanks:

> As a **[role]**, I want the agent to **[narrow outcome]** so that **[business value]**.
>
> The agent is allowed to see: **[systems/data types]**
>
> The agent is allowed to do: **[actions, e.g., propose flags, draft responses]**
>
> The agent must never: **[forbidden actions]**
>
> If the agent is unsure or the decision is high stakes, it must: **[who to ask / how to escalate]**

If you can't fill in every blank, you don't have a clear enough design yet.

### Quick Reference: Reviewing Agent Behavior

When evaluating whether an agent is working correctly, ask these four questions:

1. Did it stay within its job description and data boundaries?
2. Is the action correct in context?
3. Is the rationale understandable?
4. Would I sign my name under this action?

If the answer to any question is "no," mark it as a bad example. Collect these examples. They become your test cases for improving the agent.

## 5. Design for Uncertainty

Things will go wrong. The question is whether you've designed for that possibility.

**Build in checkpoints.** Don't let agents run indefinitely without human visibility. The recipe workflow pauses at the allergen check. The FSCM pipeline flags low-confidence cases. These aren't bugs; they're features.

**Know when it should stop and ask.** An agent that guesses when it's uncertain is worse than useless. Define the conditions under which the agent should halt and request human input.

**Design for what goes wrong, not just what goes right.** Happy path design is easy. Robust design considers: What if the input is malformed? What if the external service is down? What if the model returns garbage? Each failure mode needs a response.

```mermaid
flowchart TD
    Input[Input arrives]
    Valid{Valid input?}
    Process[Process normally]
    External{External<br/>service OK?}
    Result{Confidence<br/>high enough?}
    Output[Return result]
    
    Invalid[Reject with<br/>clear error message]
    Fallback[Use fallback<br/>or cache]
    Flag[Flag for<br/>human review]
    
    Input --> Valid
    Valid -->|Yes| Process
    Valid -->|No| Invalid
    Process --> External
    External -->|Yes| Result
    External -->|No| Fallback
    Result -->|Yes| Output
    Result -->|No| Flag
    
    style Invalid fill:#f8d7da
    style Fallback fill:#fff3cd
    style Flag fill:#fff3cd
```

**Practical implication:** For every step in your workflow, ask: "What happens if this fails?" If you don't have an answer, you have a gap.

## 6. Break Tasks Into Digestible Chunks

Context windows have hard limits. More importantly, model performance degrades before you hit those limits.

Stuffing everything into one massive prompt doesn't work. The model loses track, misses instructions, hallucinates connections. Quality suffers even when the task technically "fits."

**The 67-80% rule:** Aim to use 67-80% of available context at most. Leave room for the model to reason. Leave room for your output. Leave room for error.

**Specificity is kindness:** A focused prompt with clear scope outperforms a sprawling prompt that tries to cover everything. If your task is complex, break it into stages. Let each stage do one thing well.

```mermaid
flowchart LR
    subgraph Bad[Overloaded Context]
        A1[All instructions<br/>All data<br/>All examples<br/>All edge cases<br/>...]
    end
    
    subgraph Good[Staged Processing]
        B1[Stage 1<br/>Focused task] --> B2[Stage 2<br/>Focused task] --> B3[Stage 3<br/>Focused task]
    end
    
    style Bad fill:#f8d7da
    style Good fill:#d4edda
```

**Practical implication:** If your prompt is getting long and complex, that's a signal to decompose the task, not a challenge to fit more in.

## The Meta-Principle: AI Amplifies Your Process

Good process + AI = faster good outcomes.

Bad process + AI = faster bad outcomes.

AI doesn't relieve you of the need for clear thinking, good documentation, or sound project management. It amplifies whatever you bring to it.

If you're organized, AI helps you move faster. If you're chaotic, AI helps you create chaos at scale.

The fundamentals still matter: know what you're trying to accomplish, break it into manageable pieces, define success criteria, build in feedback loops, document your decisions.

AI is a multiplier. What it multiplies is up to you.

## Summary

| Principle | One-Line Version |
|-----------|------------------|
| 1. Good judgment upfront | Design quality bounds output quality |
| 2. Autonomy is governance | Less autonomy is often better |
| 3. Most problems don't need agents | Simple solutions beat complex ones |
| 4. Specification is the skill | Clarity beats capability |
| 5. Design for uncertainty | Plan for failure, not just success |
| 6. Digestible chunks | Focused beats sprawling |

These principles won't make you an AI expert. They'll help you avoid the mistakes that trip up people who think tools alone are the answer.
