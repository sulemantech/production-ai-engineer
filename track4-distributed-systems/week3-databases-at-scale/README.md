[← Track 4](../README.md)

# Week 3 — Databases at Scale

**Objective:** Understand how databases behave under real load and how to design schemas/queries that scale.

## Daily Build
- **Day 1:** Indexing — study B-trees conceptually, benchmark a query with and without an index on real data.
- **Day 2:** Query optimization — use EXPLAIN/query plans on a real database, identify and fix a slow query.
- **Day 3:** Database sharding — design a sharding strategy for a scenario (e.g. multi-tenant SaaS — connect to your FoodieTrack experience).
- **Day 4:** SQL vs NoSQL tradeoffs — pick a real scenario, justify the choice, implement a small version of each.
- **Day 5:** Read replicas + replication lag — set up a primary/replica pair, demonstrate and handle replication lag in application logic.
- **Day 6-7:** Design doc: schema + sharding + replication strategy for a scenario at 10x your current scale.

## Daily Interview Questions
1. How does a B-tree index actually speed up a query — what's the complexity improvement?
2. Walk me through reading a query plan — what's a red flag that tells you a query needs an index?
3. What's the hardest part of sharding a database that already has data — how do you migrate without downtime?
4. Give a real scenario where NoSQL is clearly better than SQL, and one where it's clearly worse.
5. If a user reads stale data right after writing due to replication lag, how do you fix it at the application level?

## Week 3 Assessment Gate
- Present a full schema + sharding + replication design for a given scenario, live.
- Live task: given a slow query, diagnose using EXPLAIN and fix it, timed.
- **Pass bar:** Design handles a stated scale target with real reasoning, query fix is correct and reasoning is shown (not trial-and-error).

## Milestone
A documented database design (schema + sharding + replication) for a 10x-scale scenario, plus a real query-optimization fix demonstrated live.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 2](../week2-queues-caching-lb/README.md) · [Track 4](../README.md) · [Next: Week 4 — Scaling AI/Agent Workloads Specifically →](../week4-scaling-ai-workloads/README.md)
