# Resources

## In This Document

**Appendix: Research Findings**
Summary of 2025-2026 research and industry practice on bounded agents, confidence thresholds, human-in-the-loop patterns, and teaching non-technical staff. Includes source citations.

**Appendix: Implementation Templates**
Copy-paste ready templates for practitioners:
- Agent Mission & Scope one-pager
- Process Map Worksheet
- Tool Catalog & Policy Sheet
- Risk & Human-Oversight Checklist
- Evaluation Sheet
- Change Log Template
- Non-Technical Training Handouts

## Case Study Source Code

The Federal Survey Concept Mapper pipeline referenced in Chapter 6:

**Repository:** [github.com/brockwebb/federal-survey-concept-mapper](https://github.com/brockwebb/federal-survey-concept-mapper)

Demonstrates:
- Dual-model cross-validation
- Confidence-based arbitration
- Human review flags
- Complete audit trails

## Further Reading

### On Agent Design Patterns

**What Can Go Wrong: Failure Mode Analysis**

- **Microsoft AI Red Team** - "Taxonomy of Failure Modes in Agentic AI Systems" (2025)  
  [cdn.microsoft.com/.../Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)  
  Comprehensive analysis of security and safety failures specific to agentic systems. Essential reading for understanding *why* the design principles in this course matter. The failure modes documented here are what happens when you ignore bounded autonomy, skip human-in-the-loop controls, or deploy agents without clear specifications.

**Vendor Guides (Next Steps)**

When you're ready to move from concepts to implementation, these official guides from major AI providers offer detailed technical guidance. The foundations covered in this course—agent components, bounded autonomy, guardrails, human oversight—will prepare you to navigate whichever ecosystem your organization adopts.

- **OpenAI** - "A Practical Guide to Building Agents" (January 2025)  
  [cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)  

- **Anthropic** - "Building Effective Agents" (December 2024)  
  [anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)  

- **Google Cloud** - "Agents" Whitepaper Series (2024-2025)  
  [cloud.google.com/whitepapers](https://cloud.google.com/whitepapers) (search "agents")  

Each vendor uses different terminology, but the core concepts are the same. You'll recognize the patterns.

**General Documentation**

- Anthropic's documentation on tool use and agent patterns: [docs.anthropic.com](https://docs.anthropic.com)
- OpenAI's guide to function calling: [platform.openai.com/docs](https://platform.openai.com/docs)

### On AI Governance

- NIST AI Risk Management Framework: [nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)
- World Economic Forum, "AI Agents in Action: Foundations for Evaluation and Governance" (2025)

### On Prompt Engineering

- Anthropic's prompt engineering guide: [docs.anthropic.com/en/docs/build-with-claude/prompt-engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

### On Critical Thinking with AI

- Microsoft Research on AI and critical thinking (2025)
- "Ultra-Processed Minds" by Carl Hendrick (2025) on deep reading in the AI era

## Key Sources for This Document

Research findings in the appendix draw from:

- arxiv.org/pdf/2601.08815.pdf (Resource-bounded agents)
- detectionatscale.com/p/ai-security-operations-2025-patterns
- kore.ai/blog/ai-agents-in-2026-from-hype-to-enterprise-reality
- o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026
- World Economic Forum, "AI Agents in Action" (2025)

## Contact

This document is maintained at: [github.com/brockwebb/ai-demos/ai_agents_101](https://github.com/brockwebb/ai-demos)

Feedback, corrections, and contributions welcome.

---

*Content reflects understanding as of January 2026.*
