[← Track 1](../README.md)

# Week 2 — LangGraph Deep Dive: State, Persistence, Human-in-the-Loop

**Objective:** Go back to LangGraph, properly this time — not just "it works" but understanding graph state, checkpointing, and interrupts.

## Daily Build
- **Day 1:** Rebuild Week 1's agent as a LangGraph graph. Define state schema explicitly.
- **Day 2:** Add conditional edges (routing based on model output, not just linear flow).
- **Day 3:** Add checkpointing/persistence — agent can pause and resume from saved state.
- **Day 4:** Add a human-in-the-loop interrupt (agent pauses for approval before a "risky" tool call).
- **Day 5:** Add subgraphs — break one node into a nested graph for a sub-task.
- **Day 6-7:** Stress test: kill the process mid-run, confirm it resumes correctly from checkpoint.

## Daily Interview Questions
1. What does LangGraph's state object actually solve that raw message-passing doesn't?
2. When would you use a conditional edge vs. just branching logic inside a node?
3. Explain checkpointing — what's actually being persisted, and why does that matter for production?
4. Why would you want a human-in-the-loop interrupt in an agent, and where would you place it?
5. What's a subgraph for — give a real scenario where nesting graphs beats one flat graph.
6. What are the downsides of using LangGraph vs. your raw-API version from Week 1?

## Week 2 Assessment Gate
- Diagram your graph's state flow from memory.
- Live task: add a new conditional edge + a human-approval interrupt, timed.
- Scenario: "This agent needs to survive a server restart mid-conversation — what changes?"
- **Pass bar:** Can explain state/checkpointing without notes, implements interrupt correctly, gives a real (not textbook) LangGraph-vs-raw tradeoff.

## Milestone
LangGraph agent with state, conditional routing, checkpoint/resume, and a working human-approval interrupt.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 1](../week1-raw-agent/README.md) · [Track 1](../README.md) · [Next: Week 3 — Multi-Agent →](../week3-multi-agent/README.md)
