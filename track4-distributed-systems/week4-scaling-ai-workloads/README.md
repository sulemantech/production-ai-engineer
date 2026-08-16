[← Track 4](../README.md)

# Week 4 — Scaling AI/Agent Workloads Specifically

**Objective:** Apply distributed systems concepts to the agentic systems from [Track 1](../../track1-agentic-systems/README.md) — this is where the whole journey connects.

## Daily Build
- **Day 1:** Take your Track 1 capstone — identify every bottleneck at 100x traffic (API rate limits, DB, compute).
- **Day 2:** Add async/queue-based processing for agent requests — decouple request intake from agent execution.
- **Day 3:** Horizontal scaling for stateless agent workers — containerize, run multiple instances behind a load balancer.
- **Day 4:** Handle stateful agent sessions (conversation state) at scale — design for session affinity or externalized state (Redis/DB).
- **Day 5:** Cost/rate-limit management at scale — implement token bucket rate limiting for LLM API calls across distributed workers.
- **Day 6-7:** Load test your scaled capstone, document what broke and what you fixed.

## Daily Interview Questions
1. What's the first thing that breaks when you 100x traffic to a single-instance agent service?
2. How do you handle conversation state when agent requests can hit any of N stateless workers?
3. Why is rate-limiting LLM API calls harder in a distributed system than a single process?
4. What's the tradeoff between session affinity (sticky sessions) and fully externalized state?
5. How would you design cost controls that work across many distributed agent workers, not just one process?

## Week 4 Assessment Gate
- Present your scaled architecture for the capstone, explaining every design decision made this week.
- Live task: given a new bottleneck scenario, propose and sketch a fix, timed.
- **Pass bar:** Architecture is coherent and load-test results back it up, live bottleneck diagnosis shows real distributed-systems judgment.

## Milestone
Track 1 capstone re-architected and load-tested for horizontal scale, with documented bottlenecks and fixes — the throughline of the entire journey.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go. This is the week that touches [Track 1's CAPSTONE.md](../../track1-agentic-systems/CAPSTONE.md) directly — link the re-architected repo/deploy here._

---
[← Week 3](../week3-databases-at-scale/README.md) · [Track 4](../README.md) · [Next: Week 5 — Observability, Reliability, and Failure at Scale →](../week5-observability-reliability/README.md)
