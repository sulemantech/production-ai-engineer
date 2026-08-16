[← Track 4](../README.md)

# Week 1 — Core Distributed Systems Concepts

**Objective:** The vocabulary and mental models everything else builds on.

## Daily Build
- **Day 1:** CAP theorem — study, then write your own explanation with a real example (not the textbook one).
- **Day 2:** Consistency models (strong, eventual, causal) — map each to a real product feature (e.g. bank balance vs. social media likes).
- **Day 3:** Replication strategies (leader-follower, multi-leader, leaderless) — diagram each, list failure modes.
- **Day 4:** Partitioning/sharding — implement a simple consistent-hashing scheme from scratch.
- **Day 5:** Consensus basics (Raft/Paxos, conceptually) — explain what problem they solve, don't implement full Raft.
- **Day 6-7:** Write a doc: "how would I explain CAP + consistency tradeoffs to a non-distributed-systems engineer."

## Daily Interview Questions
1. Give a real example where you'd choose availability over consistency, and one where you'd choose the opposite.
2. What's the actual difference between eventual consistency and causal consistency — give an example where it matters.
3. What fails when a leader node goes down in leader-follower replication, and how does the system recover?
4. Why does consistent hashing reduce data movement compared to naive modulo hashing when nodes are added/removed?
5. What problem does Raft/Paxos actually solve — in one sentence, no jargon.

## Week 1 Assessment Gate
- Explain CAP + consistency tradeoffs to "a non-technical stakeholder," then to "a senior engineer" — two different depths, live.
- Live task: implement consistent hashing from scratch, timed.
- **Pass bar:** Both explanations are correct and appropriately pitched, hashing implementation works and handles node addition/removal correctly.

## Milestone
Working consistent-hashing implementation, plus fluent, correctly-pitched explanations of CAP/consistency/replication tradeoffs.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Track 4](../README.md) · [Next: Week 2 — Queues, Caching, Load Balancing →](../week2-queues-caching-lb/README.md)
