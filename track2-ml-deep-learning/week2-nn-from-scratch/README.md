[← Track 2](../README.md)

# Week 2 — Neural Networks from Scratch

**Objective:** Build a neural net with no framework — understand forward pass, backprop, and optimization end to end.

## Daily Build
- **Day 1:** Single neuron, then a layer — forward pass in NumPy.
- **Day 2:** Multi-layer network forward pass, activation functions (ReLU, sigmoid, tanh) and why each is used.
- **Day 3:** Backpropagation implemented by hand (no autograd) for your multi-layer network.
- **Day 4:** Add an optimizer beyond vanilla SGD — momentum, then Adam — implement and compare convergence.
- **Day 5:** Train your from-scratch network on a real toy dataset (e.g. MNIST subset), track loss curves.
- **Day 6-7:** Add regularization (dropout, weight decay) — show it changes train/val gap.

## Daily Interview Questions
1. Why do we need non-linear activation functions — what happens with an all-linear network?
2. What's the vanishing gradient problem, and which activation choices make it worse or better?
3. Why does Adam usually converge faster than vanilla SGD — what is it doing differently?
4. What's the difference between dropout at train time vs. inference time?
5. If your train loss is low but val loss is high, what's happening and what do you try first?
6. Why do we initialize weights randomly instead of all zeros?

## Week 2 Assessment Gate
- Explain your backprop implementation line by line, no notes.
- Live task: add a new activation function and confirm gradients still flow correctly, timed.
- **Pass bar:** Can explain every step of backprop without hand-waving, diagnoses overfitting/underfitting correctly on a shown loss curve.

## Milestone
From-scratch neural net (forward + backward pass, optimizer, regularization) trained on real data, with loss curves as evidence.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 1](../week1-math-foundations/README.md) · [Track 2](../README.md) · [Next: Week 3 — CNNs, RNNs, and Why Transformers Won →](../week3-cnn-rnn-transformers/README.md)
