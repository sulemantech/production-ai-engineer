[← Track 1](../README.md)

# Week 5 — Reliability, Security, Guardrails

**Objective:** Break your own system on purpose. This week's artifact — a documented failure-mode analysis — is one of the strongest interview signals you can bring.

## Daily Build
- **Day 1:** Attempt prompt injection via a tool's returned content (e.g. RAG doc, web result) — see if you can hijack the agent.
- **Day 2:** Add input/output guardrails to block the injection you found.
- **Day 3:** Add tool-permission scoping — no agent/tool has more access than it needs.
- **Day 4:** Add rate limiting and cost circuit-breakers (kill a run that exceeds a budget).
- **Day 5:** Stress test for infinite loops, runaway costs, and hallucinated tool arguments — force each failure on purpose.
- **Day 6-7:** Write a "failure modes and mitigations" doc: each failure you found, how you fixed it, what's still a residual risk.

## Daily Interview Questions
1. What's prompt injection, specifically in the context of tool outputs or RAG content (not just user input)?
2. How do you scope tool permissions so a compromised agent can't do unlimited damage?
3. What's a circuit breaker in this context, and what should trigger one?
4. How do you distinguish a hallucinated tool call from a legitimate but wrong one?
5. What's a guardrail that sounds good but is actually weak or easily bypassed?
6. If you had to ship this system today, what's the one unmitigated risk you'd flag to your team?

## Week 5 Assessment Gate
- Present your failure-modes doc like a security review.
- Live task: given a new tool, identify its injection risk and propose a mitigation on the spot, timed.
- Scenario: "A user reports your agent did something it shouldn't have — walk me through your incident response."
- **Pass bar:** Found at least one real injection/failure vector (not hypothetical), mitigations are concrete and implemented (not "I'd add validation"), can reason about a *new* tool's risk live.

## Milestone
Documented, tested failure-mode analysis with real mitigations implemented (injection defense, permission scoping, circuit breakers).

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 4](../week4-evals-observability/README.md) · [Track 1](../README.md) · [Next: Week 6 — Deployment →](../week6-deployment/README.md)
