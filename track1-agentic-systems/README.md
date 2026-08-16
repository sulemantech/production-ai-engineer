# Track 1 — Agentic Systems

**Goal:** Be interview-ready for top-tier AI/agentic engineering roles, with a deployed, evaluated, defensible portfolio piece as proof.
**Baseline:** Strong Python. Built prompt chains + basic RAG (real, not production). Built one LangGraph tool-calling agent. Aware of evals/observability but never implemented. 10-15 hrs/week.
**Format:** Daily build task + daily interview question. Weekly Assessment Gate (pass/fail) before advancing.

---

## Weeks

| Week | Focus | Milestone |
|---|---|---|
| [1 — Raw Agent](week1-raw-agent/README.md) | Agent Fundamentals, From Scratch (Raw API, No Framework) | Raw-API agent (3 tools), loop guards, cost tracking — architecture explained cold |
| [2 — LangGraph](week2-langgraph/README.md) | State, Persistence, Human-in-the-Loop | LangGraph agent with state, routing, checkpoint/resume, human-approval interrupt |
| [3 — Multi-Agent](week3-multi-agent/README.md) | Multi-Agent Orchestration | Multi-agent system (orchestrator + 2+ workers) on real task, with failure handling |
| [4 — Evals & Observability](week4-evals-observability/README.md) | Closing the production-rigor gap | Eval suite (golden set + LLM-as-judge) that catches real regressions + trace/cost dashboard |
| [5 — Reliability & Security](week5-reliability-security/README.md) | Guardrails | Documented failure-mode analysis with real, implemented mitigations |
| [6 — Deployment](week6-deployment/README.md) | Production Deployment + Interview Packaging | Deployed capstone + system design doc + rehearsed walkthrough + passed full mock interview |

**Track 1 Complete (Capstone):** Live, deployed multi-agent system with public repo, eval suite, trace/cost dashboard, documented failure-mode analysis, system design doc, and a rehearsed 5-minute walkthrough.

See [CAPSTONE.md](CAPSTONE.md) for the capstone domain, agent roles, and key decisions once chosen in Week 3.

---

## What to Ignore For Now
- Framework-hopping (CrewAI, AutoGen, etc.) — LangGraph + raw API is enough depth
- Fine-tuning / training your own models — not tested in these interviews
- Frontend polish on the capstone — functional beats pretty
- Exotic vector DB / RAG re-ranking tuning — you already have basic RAG, don't rabbit-hole
- Benchmarking every model provider — go deep on one family (Claude) instead of wide

## Next Track

→ [Track 2 — ML & Deep Learning Fundamentals](../track2-ml-deep-learning/README.md)
