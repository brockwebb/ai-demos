# Chapter: Key Vocabulary

This chapter provides definitions for essential terms. Terms marked with **[SLIDE]** have standalone visual aids in the presentation.

---

## Source Key
- **[NIST]** - National Institute of Standards and Technology
- **[ISO]** - International Organization for Standardization  
- **[SEMINAL]** - Academic paper that coined/defined the term
- **[WIKI]** - Wikipedia

---

## Foundational Concepts

### Artificial Intelligence (AI) **[SLIDE]**
A machine-based system that can, for a given set of human-defined objectives, make predictions, recommendations, or decisions influencing real or virtual environments.

**Source:** [NIST] CSRC Glossary  
https://csrc.nist.gov/glossary/term/artificial_intelligence

---

### Machine Learning (ML)
A subset of AI involving computer systems that adapt and learn from data, improving accuracy over time without being explicitly programmed for each task.

**Source:** [NIST] CSRC Glossary  
https://csrc.nist.gov/glossary/term/machine_learning

**Key distinction:** Traditional software = you write rules. ML = you provide examples.

---

### Large Language Model (LLM)
A computational model notable for its ability to achieve general-purpose language generation and other natural language processing tasks. LLMs acquire these abilities by learning statistical relationships from vast amounts of text during training.

**Source:** [WIKI] "Large language model"  
https://en.wikipedia.org/wiki/Large_language_model

**Examples:** GPT-4, Claude, Gemini, Llama

---

### Generative AI (GenAI)
Artificial intelligence capable of generating text, images, videos, or other data using generative models, often in response to prompts. These models learn patterns and structure from training data, then generate new data with similar characteristics.

**Source:** [WIKI] "Generative artificial intelligence"  
https://en.wikipedia.org/wiki/Generative_artificial_intelligence

---

## Working with LLMs

### Prompt
Input provided to a generative AI model to guide output—including text instructions, questions, context, constraints, and examples.

**Source:** [WIKI] "Prompt engineering"  
https://en.wikipedia.org/wiki/Prompt_engineering

---

### Prompt Engineering
The process of structuring instructions to produce desired output from a generative AI model. Involves clear queries, context, constraints, and iterative refinement.

**Source:** [WIKI] "Prompt engineering"  
https://en.wikipedia.org/wiki/Prompt_engineering

---

### Context Window **[SLIDE]**
The maximum span of text (measured in tokens) that a language model can process at once—including both input and output. Functions as the model's working memory.

**Source:** [WIKI] "Large language model"  
https://en.wikipedia.org/wiki/Large_language_model

**Practical note:** Ranges from ~4K to 1M+ tokens depending on model. When exceeded, earlier content is effectively "forgotten."

---

### Token
The basic unit of text that language models process. Can represent words, subwords, or characters depending on the tokenization scheme.

**Source:** [WIKI] "Large language model"  
https://en.wikipedia.org/wiki/Large_language_model

**Rule of thumb:** 1 token ≈ 4 characters ≈ ¾ word. 1,000 words ≈ 1,300-1,500 tokens.

---

### Confabulation
When an AI generates false or misleading information presented as fact—filling gaps with plausible but fabricated content, without any indication of uncertainty. The system produces confident-sounding output that has no basis in its training data or provided context.

**Source:** [WIKI] "Confabulation"  
https://en.wikipedia.org/wiki/Confabulation

**Origin:** From neuropsychology—describes producing false information without intent to deceive, typically to fill memory gaps. The person (or system) genuinely "believes" what it's generating.

**Note:** The AI field commonly calls this "hallucination" (see below), but confabulation is the more accurate term.

**Critical implication:** LLMs don't "know" when they're wrong. Verification is your responsibility.

---

### Hallucination **[SLIDE]**
A common but imprecise term for AI confabulation (see above). Widely used in industry and media.

**Source:** [WIKI] "Hallucination (artificial intelligence)"  
https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence)

**Why it's a misnomer:** Hallucination implies perceiving something that isn't there. LLMs don't perceive—they generate. Confabulation (generating plausible content to fill gaps) is the accurate descriptor. The term "hallucination" persists because it's convenient and dramatic, not because it's correct.

---

## Prompting Techniques

### Zero-Shot Prompting
Asking a model to perform a task without providing examples—relying entirely on the model's pre-existing knowledge and instruction clarity.

**Source:** [WIKI] "Prompt engineering"  
https://en.wikipedia.org/wiki/Prompt_engineering

**Example:** "Classify this feedback as positive, negative, or neutral: [text]"

---

### Few-Shot Prompting **[SLIDE]**
Providing a small number of examples (typically 2-5) in your prompt to demonstrate the desired pattern before asking the model to perform on new input.

**Source:** [SEMINAL] Brown et al., 2020, "Language Models are Few-Shot Learners"  
https://arxiv.org/abs/2005.14165

**Example:**
```
"Great product!" → Positive
"Broke after one day" → Negative  
"It works" → Neutral
"Best purchase ever" → ?
```

---

### Chain-of-Thought (CoT) Prompting
A technique that encourages the model to generate intermediate reasoning steps before producing a final answer. Improves performance on multi-step reasoning tasks.

**Source:** [SEMINAL] Wei et al., 2022, "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"  
https://arxiv.org/abs/2201.11903

**Trigger phrase:** "Let's think step by step"

**Benefit:** Makes reasoning visible for verification—you can see where it went wrong.

---

## Agentic Concepts

### AI Agent
An AI system designed to perceive its environment, make decisions, and take actions to achieve specific goals with some degree of autonomy.

**Source:** [ISO] ISO/IEC 22989:2022 - "an agent that maximizes its chance of successfully achieving its goals by using AI techniques."

---

### ReAct (Reasoning and Acting)
A framework that prompts LLMs to generate interleaved reasoning traces and actions, allowing dynamic plan creation and adjustment while incorporating information from external sources.

**Source:** [SEMINAL] Yao et al., 2022, "ReAct: Synergizing Reasoning and Acting in Language Models"  
https://arxiv.org/abs/2210.03629

**Pattern:** Thought → Action → Observation → Updated Thought → Next Action

**Note:** This is a specific technical implementation pattern. The feedback cycle discussed in this course (observe → decide → act → check) is a general interaction mechanism—related in concept but distinct in purpose and audience.

---

## Knowledge and Retrieval

### Retrieval-Augmented Generation (RAG) **[SLIDE]**
A generative AI approach where a model is paired with an information retrieval system. Retrieved information is incorporated into the prompt to ground the response in actual sources.

**Source:** [NIST] CSRC Glossary  
https://csrc.nist.gov/glossary/term/retrieval_augmented_generation

**Why it matters:** Reduces hallucination. Enables AI to answer questions about your documents.

---

### Fine-Tuning
Adapting a pre-trained model to a new task by continuing training on a smaller, task-specific dataset while preserving knowledge from initial training.

**Source:** [WIKI] "Fine-tuning (deep learning)"  
https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)

**Distinction from prompting:** Fine-tuning changes the model (requires technical resources). Prompting changes only the input (accessible to anyone).

---

## Trust and Safety

### Bias (in AI) **[SLIDE]**
Systematic errors in AI outputs that can result in unfair outcomes, such as privileging one group over others.

**Source:** [NIST] "Towards a Standard for Identifying and Managing Bias in Artificial Intelligence"  
https://www.nist.gov/publications/towards-standard-identifying-and-managing-bias-artificial-intelligence

**NIST Categories:**
- **Systemic:** Present in data, institutions, society
- **Computational:** From algorithms and data representativeness
- **Human-cognitive:** From human prejudices and assumptions

---

### Guardrails
Programmable safety controls in AI systems ensuring outputs remain within acceptable boundaries—including content filtering, topic restrictions, and output validation.

**Source:** [WIKI] "Guardrails (artificial intelligence)"  
https://en.wikipedia.org/wiki/Guardrails_(artificial_intelligence)

---

### Explainability
The ability to describe an AI system's internal mechanism in human-understandable terms, providing evidence or reasons for outputs.

**Source:** [NIST] IR 8312, "Four Principles of Explainable Artificial Intelligence"  
https://www.nist.gov/publications/four-principles-explainable-artificial-intelligence

**NIST's Four Principles:**
1. Provides evidence/reasons for outputs
2. Understandable to intended audience
3. Accurately reflects actual process
4. Operates within design conditions

---

## Model Behavior

### Training vs. Inference
**Training:** Building a model by exposing it to data and adjusting parameters. Computationally expensive, done by developers.

**Inference:** Using a trained model to generate outputs from new inputs. This is what happens when you chat with an AI.

**Source:** [WIKI] "Training, validation, and test data sets"  
https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets

**Key point:** Chatting with an AI = inference, not training.

---

### Model Drift
Performance degradation over time as real-world patterns change and diverge from patterns learned during training.

**Source:** [WIKI] "Concept drift"  
https://en.wikipedia.org/wiki/Concept_drift

---

## Summary: Slide Candidates

| Term | Rationale |
|------|-----------|
| AI (definition) | Foundational, sets scope |
| Context Window | Practical constraint everyone hits |
| Hallucination | Term they'll encounter; teachable moment for "confabulation" |
| Few-Shot Prompting | Actionable technique |
| RAG | Key architecture for enterprise use |
| Bias | Policy/ethics relevance |

---

*AI Agents 101 - Speaker Handout*
