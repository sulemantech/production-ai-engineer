[← Track 1](../README.md)

# Week 4 — Evals & Observability (closing the production-rigor gap)

**Objective:** This is the week that actually differentiates you. Build a real eval harness and tracing — the thing most candidates can't do.

## Daily Build
- **Day 1:** Define what "good" means for your capstone task. Build a small golden dataset (10-20 examples with expected outcomes).
- **Day 2:** Build an automated eval runner — run the golden set through your agent, capture pass/fail.
- **Day 3:** Add LLM-as-judge scoring for outputs that aren't exact-match (e.g. quality, correctness, tone).
- **Day 4:** Add tracing (LangSmith or OpenTelemetry-based) — every run is inspectable step by step.
- **Day 5:** Add cost/latency/token tracking per run, aggregated into a simple dashboard or report.
- **Day 6-7:** Run a regression: deliberately change a prompt, confirm your evals catch the quality change.

## Daily Interview Questions
1. What makes a good golden dataset for evals? What makes a bad one?
2. Why use LLM-as-judge instead of exact-match — what are the risks of LLM-as-judge itself?
3. What's the difference between an eval and a unit test, conceptually?
4. Walk me through what a trace actually shows you that logs don't.
5. If your agent's cost tripled overnight, how would your dashboard help you find why?
6. How do you know your evals are actually catching regressions and not just always passing?

## Week 4 Assessment Gate
- Present your eval results like you would to a team: what's measured, what passed/failed, why.
- Live task: intentionally break your agent (bad prompt change), confirm the eval suite catches it, timed.
- Scenario: "Your eval pass rate dropped from 95% to 80% overnight — walk me through your investigation."
- **Pass bar:** Eval suite genuinely fails on a real regression (not staged), can explain LLM-as-judge risk unprompted, has real cost/latency numbers to show.

## Milestone
Capstone has a working eval suite (golden set + LLM-as-judge) that catches real regressions, plus a trace/cost dashboard.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Week 3](../week3-multi-agent/README.md) · [Track 1](../README.md) · [Next: Week 5 — Reliability & Security →](../week5-reliability-security/README.md)
