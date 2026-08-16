[← Track 4](../README.md)

# Week 2 — Queues, Caching, Load Balancing

**Objective:** The building blocks that show up in almost every system design interview.

## Daily Build
- **Day 1:** Message queues — set up a real queue (e.g. Redis-based or similar), build producer/consumer.
- **Day 2:** Queue patterns — implement retry logic, dead-letter queue, at-least-once vs. exactly-once handling.
- **Day 3:** Caching — implement an LRU cache from scratch, then add a real cache layer (e.g. Redis) in front of a slow operation.
- **Day 4:** Cache invalidation strategies — implement write-through vs. write-behind, explain the classic "cache invalidation is hard" problem with a real bug you hit.
- **Day 5:** Load balancing — study algorithms (round robin, least connections, consistent hashing), configure a real load balancer in front of a multi-instance service.
- **Day 6-7:** Combine: build a small service with queue + cache + load balancer, load test it.

## Daily Interview Questions
1. Why use a message queue instead of a direct API call between services — what failure does it protect against?
2. What's the difference between at-least-once and exactly-once delivery, and why is exactly-once so hard to actually guarantee?
3. Walk me through LRU cache implementation — what data structures give you O(1) get/put?
4. What's a cache stampede, and how do you prevent one?
5. When would you choose least-connections load balancing over round robin?

## Week 2 Assessment Gate
- Live task: implement an LRU cache from scratch, timed.
- Scenario: "Your cache and database are out of sync — walk me through diagnosing and fixing it."
- **Pass bar:** LRU cache is correct and O(1), diagnosis approach is systematic (not guessing), can explain a real invalidation bug from personal testing this week.

## Milestone
Small service combining queue + cache + load balancer, load-tested, with a from-scratch LRU cache implementation.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 1](../week1-core-concepts/README.md) · [Track 4](../README.md) · [Next: Week 3 — Databases at Scale →](../week3-databases-at-scale/README.md)
