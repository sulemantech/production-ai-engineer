[← Track 1](../README.md)

# Week 3 — Multi-Agent Orchestration

**Objective:** Understand when multi-agent beats single-agent (and when it's overkill), and build a real orchestrator-worker system. Begin capstone architecture.

## Daily Build
- **Day 1:** Design the capstone: pick a domain, define 2-3 specialized agent roles + an orchestrator.
- **Day 2:** Build the orchestrator agent — routes tasks, doesn't do the work itself.
- **Day 3:** Build worker agent #1, wire it to the orchestrator.
- **Day 4:** Build worker agent #2, handle agent-to-agent handoff and shared context.
- **Day 5:** Add failure handling: a worker fails or times out — orchestrator recovers or escalates.
- **Day 6-7:** End-to-end test: run a real multi-step task through the full system.

## Daily Interview Questions
1. When does multi-agent actually beat a single well-prompted agent? When is it overkill?
2. How does your orchestrator decide which worker to call — is that logic reliable or a coin flip in disguise?
3. What context gets passed between agents, and what's deliberately withheld?
4. What happens in your system if a worker agent returns garbage — does the orchestrator notice?
5. How would this design change if you needed 10 worker agents instead of 2?
6. What's the single biggest risk in a multi-agent system that doesn't exist in a single-agent one?

## Week 3 Assessment Gate
- Whiteboard your multi-agent architecture from memory, explaining each handoff.
- Live task: add a third worker agent and route to it correctly, timed.
- Scenario: "One of your workers just silently returned wrong data — walk me through debugging it."
- **Pass bar:** Can defend the architecture choice (not just describe it), adds a worker without breaking existing flow, gives a concrete debugging approach (not "I'd add logging").

## Milestone
Working multi-agent system (orchestrator + 2+ workers) solving a real end-to-end task, with basic failure handling.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go. Capstone domain decision (Day 1) belongs in [CAPSTONE.md](../CAPSTONE.md), not just here._

---
[← Week 2](../week2-langgraph/README.md) · [Track 1](../README.md) · [Next: Week 4 — Evals & Observability →](../week4-evals-observability/README.md)
