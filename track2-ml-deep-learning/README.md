# Track 2 — ML & Deep Learning Fundamentals

**Prerequisite:** [Track 1 (Agentic Systems)](../track1-agentic-systems/README.md) complete.
**Goal:** Be able to defend "why does this model behave this way" from first principles — math foundations, neural nets from scratch, transformer internals, training/fine-tuning basics. Not a full ML degree — the subset that shows up in top-tier AI engineering interviews.
**Format:** Daily build/study task + daily interview question. Weekly Assessment Gate before advancing.

---

## Weeks

| Week | Focus | Milestone |
|---|---|---|
| [1 — Math Foundations](week1-math-foundations/README.md) | Only what you'll actually use | From-scratch NumPy gradient descent, softmax, cross-entropy, verified against autograd |
| [2 — Neural Networks from Scratch](week2-nn-from-scratch/README.md) | Forward pass, backprop, optimization | From-scratch neural net trained on real data, with loss curves as evidence |
| [3 — CNNs, RNNs, and Why Transformers Won](week3-cnn-rnn-transformers/README.md) | Architectures before attention | From-scratch attention + multi-head attention, trained CNN, written architecture comparison |
| [4 — Transformer Architecture, End to End](week4-transformer-architecture/README.md) | Build a full (small) transformer from scratch | Working from-scratch transformer trained on a toy task, with generated output as proof |
| [5 — Training, Fine-Tuning, and LLM-Specific Behavior](week5-training-finetuning/README.md) | How large models are trained and adapted | Documented fine-tuning experiment (full vs. LoRA) + written pretrain → SFT → RLHF explanation |
| [6 — Applied ML System Design + Interview Packaging](week6-system-design/README.md) | ML system design, not just theory recall | From-scratch transformer + fine-tuning experiment as portfolio artifacts, fluency in ML system design |

**Track 2 Complete:** From-scratch transformer + fine-tuning experiment as portfolio artifacts, plus demonstrated fluency in ML system design and passed full mock interview.

---

## What to Ignore in This Track
- Training frontier-scale models yourself — impossible and not what's tested; focus on toy-scale understanding
- Every architecture variant (Mamba, MoE internals, etc.) — know they exist and roughly why, don't implement each
- Full RLHF implementation — understand the pipeline conceptually, don't build a reward model from scratch
- Chasing latest papers weekly — depth on fundamentals beats breadth on the newest architecture

## Track Navigation

← [Track 1 — Agentic Systems](../track1-agentic-systems/README.md) · [Next: Track 3 — DSA / Algorithms Interview Prep →](../track3-dsa/README.md)
