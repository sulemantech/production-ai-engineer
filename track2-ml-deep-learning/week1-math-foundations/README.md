[← Track 2](../README.md)

# Week 1 — Math Foundations (only what you'll actually use)

**Objective:** Linear algebra, calculus, probability — just enough to derive backprop and reason about model behavior, not a full math course.

## Daily Build
- **Day 1:** Vectors, matrices, dot products, matrix multiplication — implement from scratch in NumPy (no `np.dot` shortcuts first).
- **Day 2:** Derivatives, partial derivatives, chain rule — derive gradients for simple functions by hand.
- **Day 3:** Gradient descent — implement from scratch on a toy loss function, visualize convergence.
- **Day 4:** Probability basics — distributions, expectation, entropy, cross-entropy (why it's the loss function of choice).
- **Day 5:** Softmax + cross-entropy loss — derive the gradient by hand, implement, verify against autograd.
- **Day 6-7:** Review + write a one-page "why cross-entropy for classification" explanation from first principles.

## Daily Interview Questions
1. Why does gradient descent use the negative gradient direction — what breaks if you use the positive one?
2. What's the intuition behind the chain rule in the context of backpropagation?
3. Why is cross-entropy the standard loss for classification instead of MSE?
4. What does entropy actually measure, in plain language?
5. What's the difference between a local minimum and a saddle point, and why does it matter for deep nets?
6. Explain softmax — why exponentiate instead of just normalizing?

## Week 1 Assessment Gate
- Derive backprop gradients for a 2-layer network on a whiteboard, no notes.
- Live task: implement gradient descent from scratch on a new toy function, timed.
- **Pass bar:** Can derive the chain rule application without hesitation, implements correctly under time pressure.

## Milestone
From-scratch NumPy implementations of gradient descent, softmax, and cross-entropy, verified against autograd, plus a written first-principles explanation.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Track 2](../README.md) · [Next: Week 2 — Neural Networks from Scratch →](../week2-nn-from-scratch/README.md)
