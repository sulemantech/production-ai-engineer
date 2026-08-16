[← Track 2](../README.md)

# Week 4 — Transformer Architecture, End to End

**Objective:** Build a full (small) transformer from scratch. This is the single highest-leverage artifact in this track.

## Daily Build
- **Day 1:** Positional encoding — implement, explain why transformers need it (no recurrence = no inherent order).
- **Day 2:** Transformer encoder block — attention + feedforward + residual connections + layer norm, from scratch.
- **Day 3:** Decoder block + causal masking — implement, verify masking prevents future-token leakage.
- **Day 4:** Assemble a small full transformer (few layers), train on a toy task (e.g. character-level language modeling).
- **Day 5:** Tokenization — implement/inspect a BPE tokenizer, understand why subword tokenization matters.
- **Day 6-7:** Train your toy transformer to convergence, generate sample output, document architecture choices.

## Daily Interview Questions
1. Why residual connections in transformers — what breaks in deep networks without them?
2. What does layer norm do differently from batch norm, and why does that matter for transformers?
3. Explain causal masking — what exact matrix operation enforces it?
4. Why subword tokenization (BPE) instead of word-level or character-level?
5. What's the actual difference between encoder-only, decoder-only, and encoder-decoder transformers — give a model example of each.
6. Where does your toy transformer's context length limit come from, mechanically?

## Week 4 Assessment Gate
- Whiteboard the full transformer architecture from memory (encoder or decoder block, your choice).
- Live task: modify your transformer to add a new layer without breaking dimensions, timed.
- **Pass bar:** Full architecture explained without notes, live modification succeeds, can explain encoder/decoder/decoder-only distinction with real model examples.

## Milestone
A working from-scratch (small) transformer trained on a toy task, with generated output as proof, plus full architectural understanding demonstrated live.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 3](../week3-cnn-rnn-transformers/README.md) · [Track 2](../README.md) · [Next: Week 5 — Training, Fine-Tuning, and LLM-Specific Behavior →](../week5-training-finetuning/README.md)
