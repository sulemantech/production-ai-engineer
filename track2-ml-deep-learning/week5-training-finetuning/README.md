[← Track 2](../README.md)

# Week 5 — Training, Fine-Tuning, and LLM-Specific Behavior

**Objective:** Understand how large models are actually trained and adapted — enough to reason about behavior, not to train a frontier model yourself.

## Daily Build
- **Day 1:** Pretraining objectives (next-token prediction, masked LM) — explain and contrast.
- **Day 2:** Fine-tuning basics — full fine-tune a small open model on a toy task, observe behavior change.
- **Day 3:** Parameter-efficient fine-tuning (LoRA) — implement or use a library, compare to full fine-tune (cost, quality, speed).
- **Day 4:** RLHF / instruction tuning conceptually — explain the pipeline (SFT → reward model → RL), don't implement full RLHF.
- **Day 5:** Sampling strategies — temperature, top-k, top-p — implement and observe effect on generation.
- **Day 6-7:** Write a doc: "how does a base model become a chat model" — the full pipeline, in your own words.

## Daily Interview Questions
1. What's the difference between pretraining and fine-tuning, mechanically?
2. Why does LoRA work — what's the low-rank assumption it's making?
3. Walk me through the RLHF pipeline at a high level — what does each stage actually optimize for?
4. What does temperature control mathematically in sampling — connect it to the softmax.
5. Why might a model hallucinate more at high temperature vs. low?
6. What's the difference between a base model and an instruction-tuned model in terms of what they were trained to do?

## Week 5 Assessment Gate
- Explain the full base-model-to-chat-model pipeline from memory.
- Live task: fine-tune a small model with LoRA on a new toy dataset, timed.
- **Pass bar:** Pipeline explanation is accurate and fluent, LoRA fine-tune completes correctly, can reason about temperature/sampling tradeoffs live.

## Milestone
Documented fine-tuning experiment (full vs. LoRA comparison) plus a written, accurate explanation of the pretrain → SFT → RLHF pipeline.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 4](../week4-transformer-architecture/README.md) · [Track 2](../README.md) · [Next: Week 6 — Applied ML System Design + Interview Packaging →](../week6-system-design/README.md)
