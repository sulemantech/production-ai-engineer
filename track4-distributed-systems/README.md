# Track 4 — Distributed Systems / Infra Depth

**Prerequisite:** [Track 3](../track3-dsa/README.md) complete (per your sequential preference).
**Goal:** Design and defend systems that scale — applied specifically to AI/agent workloads where relevant. Enough to pass "design a system that handles X scale" interview rounds at top-tier companies.
**Format:** Daily build/study task + daily interview question. Weekly Assessment Gate before advancing.

---

## Weeks

| Week | Focus | Milestone |
|---|---|---|
| [1 — Core Distributed Systems Concepts](week1-core-concepts/README.md) | The vocabulary and mental models everything else builds on | Working consistent-hashing implementation, fluent CAP/consistency/replication explanations |
| [2 — Queues, Caching, Load Balancing](week2-queues-caching-lb/README.md) | Building blocks in almost every system design interview | Small service combining queue + cache + load balancer, load-tested, with a from-scratch LRU cache |
| [3 — Databases at Scale](week3-databases-at-scale/README.md) | How databases behave under real load | Documented DB design (schema + sharding + replication) for a 10x-scale scenario |
| [4 — Scaling AI/Agent Workloads Specifically](week4-scaling-ai-workloads/README.md) | Where the whole journey connects — back to the Track 1 capstone | Track 1 capstone re-architected and load-tested for horizontal scale |
| [5 — Observability, Reliability, and Failure at Scale](week5-observability-reliability/README.md) | How production systems stay debuggable and resilient | Full observability stack on the capstone, plus a real postmortem from a self-induced failure |
| [6 — System Design Interview Practice + Full Journey Synthesis](week6-system-design-synthesis/README.md) | Package all four tracks into one interview narrative | Scaled, observable capstone; full 4-track portfolio; passed complete back-to-back mock interview loop |

**Track 4 Complete — Full Journey Complete:** Scaled, observable capstone system; full portfolio document linking all 4 tracks; passed a complete back-to-back mock interview loop across all disciplines.

---

## What to Ignore in This Track
- Building your own database or queue system from scratch at a research level — use real tools (Postgres, Redis, etc.), understand internals conceptually, don't reinvent them
- Multi-region/global-scale specifics (unless a target company specifically operates at that scale) — single-region horizontal scaling covers most interview bars
- Kubernetes/infra-as-code deep mastery — understand containers and orchestration conceptually; going deep on K8s internals is a separate specialization
- Chasing every cloud provider's specific services — pick one (or use what you already know from FoodieTrack's Vercel deployment) and go deep there

## Track Navigation

← [Track 3 — DSA / Algorithms Interview Prep](../track3-dsa/README.md) · [Back to journey overview →](../README.md)
