[← Track 4](../README.md)

# Week 5 — Observability, Reliability, and Failure at Scale

**Objective:** How production systems stay debuggable and resilient when things break — because they will.

## Daily Build
- **Day 1:** Structured logging + centralized log aggregation — set up for your scaled capstone.
- **Day 2:** Metrics + alerting — instrument key metrics (latency, error rate, saturation), set real alert thresholds.
- **Day 3:** Distributed tracing across services — trace a request through queue → worker → DB → response.
- **Day 4:** Circuit breakers + graceful degradation — implement for a dependency that might fail (e.g. LLM API timeout).
- **Day 5:** Chaos testing — deliberately kill a component under load, observe system behavior, fix what breaks.
- **Day 6-7:** Write an incident postmortem for the failure you caused/found this week — real format, real analysis.

## Daily Interview Questions
1. What's the difference between a metric, a log, and a trace — when do you reach for each?
2. What makes a good alert threshold vs. one that causes alert fatigue?
3. Walk me through tracing a slow request across multiple services to find the bottleneck.
4. What's graceful degradation, and give a real design decision from your capstone this week.
5. Walk me through a postmortem you'd actually write — what sections, what tone, what's the point of it?

## Week 5 Assessment Gate
- Present your postmortem like you're presenting to a team after a real incident.
- Live task: given a new failure scenario, propose monitoring/alerting that would have caught it, timed.
- **Pass bar:** Postmortem is honest and specific (not vague), monitoring proposal is concrete and would genuinely catch the stated failure.

## Milestone
Full observability stack (logs, metrics, traces, alerts) on your capstone, plus a real postmortem from a self-induced failure.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 4](../week4-scaling-ai-workloads/README.md) · [Track 4](../README.md) · [Next: Week 6 — System Design Interview Practice + Full Journey Synthesis →](../week6-system-design-synthesis/README.md)
