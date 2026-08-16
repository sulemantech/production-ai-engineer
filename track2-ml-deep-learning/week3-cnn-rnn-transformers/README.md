[← Track 2](../README.md)

# Week 3 — CNNs, RNNs, and Why Transformers Won

**Objective:** Understand the architectures that came before transformers, so you can explain *why* attention won — not just that it did.

## Daily Build
- **Day 1:** Convolution operation from scratch — implement, visualize on an image.
- **Day 2:** Build a small CNN (PyTorch this time — framework is fine now that fundamentals are solid), train on image classification.
- **Day 3:** RNN/LSTM basics — implement a simple RNN forward pass, understand vanishing gradients over sequence length.
- **Day 4:** Attention mechanism from scratch — implement scaled dot-product attention, no framework shortcuts.
- **Day 5:** Multi-head attention — extend your implementation, understand why multiple heads help.
- **Day 6-7:** Write a comparison doc: CNN vs RNN vs Transformer — what each is good/bad at and why.

## Daily Interview Questions
1. What does a convolution actually compute, and why does weight-sharing matter?
2. Why do RNNs struggle with long sequences — connect this to vanishing gradients specifically.
3. Walk me through scaled dot-product attention, step by step, with the actual math.
4. Why scale by sqrt(d_k) in attention — what breaks without it?
5. Why does multi-head attention help over single-head?
6. Give a task where a CNN would still beat a transformer today, and why.

## Week 3 Assessment Gate
- Derive attention math on a whiteboard from memory.
- Live task: implement multi-head attention from scratch, timed.
- **Pass bar:** Attention math is correct without reference, can articulate a genuine (not textbook) case for CNN/RNN over transformer.

## Milestone
From-scratch attention + multi-head attention implementation, plus a trained CNN and a written architecture comparison.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 2](../week2-nn-from-scratch/README.md) · [Track 2](../README.md) · [Next: Week 4 — Transformer Architecture, End to End →](../week4-transformer-architecture/README.md)
