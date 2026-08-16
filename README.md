# Production AI Engineer

A ~5-6 month, four-track journey to become interview-ready for top-tier AI/agentic engineering roles — with a deployed, evaluated, defensible portfolio as proof, not just theory recall.

**Baseline going in:** Strong Python. Built prompt chains + basic RAG (real, not production). Built one LangGraph tool-calling agent. Aware of evals/observability but never implemented. ~10-15 hrs/week.

**Format (every track, every week):** Daily build/study task + daily interview question + a Weekly Assessment Gate (pass/fail) before advancing. No week is "done" until the gate is passed.

---

Track progress week by week in [PROGRESS.md](PROGRESS.md).

## The Throughline

Each track hands the next one something real to build on:

1. **[Track 1 — Agentic Systems](track1-agentic-systems/README.md)** produces the capstone: a working multi-agent system with evals, observability, and documented failure modes.
2. **[Track 2 — ML & Deep Learning Fundamentals](track2-ml-deep-learning/README.md)** builds the first-principles understanding (math → neural nets → transformers → fine-tuning) needed to defend *why* that capstone's models behave the way they do.
3. **[Track 3 — DSA / Algorithms Interview Prep](track3-dsa/README.md)** is pure drilling — pattern recognition under time pressure, so live coding rounds stop being the bottleneck.
4. **[Track 4 — Distributed Systems / Infra Depth](track4-distributed-systems/README.md)** returns to the Track 1 capstone and re-architects it for scale — queues, caching, sharded data, observability, chaos testing — closing the loop on the entire journey.

Track 4's final week is the synthesis: one portfolio document linking all four tracks' artifacts, one coherent "tell me about your background" narrative, and a full back-to-back mock interview loop (DSA + ML fundamentals + system design + behavioral).

## Sequencing

Tracks are meant to run **sequentially** — each has the previous as a stated prerequisite:

| Order | Track | Prerequisite |
|---|---|---|
| 1 | [Agentic Systems](track1-agentic-systems/README.md) | Baseline above |
| 2 | [ML & Deep Learning Fundamentals](track2-ml-deep-learning/README.md) | Track 1 complete |
| 3 | [DSA / Algorithms Interview Prep](track3-dsa/README.md) | Track 2 complete |
| 4 | [Distributed Systems / Infra Depth](track4-distributed-systems/README.md) | Track 3 complete |

## What Each Track Ends With

| Track | Weeks | Final Milestone |
|---|---|---|
| [1 — Agentic Systems](track1-agentic-systems/README.md) | 6 | Live, deployed multi-agent system with public repo, eval suite, trace/cost dashboard, documented failure-mode analysis, system design doc, rehearsed walkthrough |
| [2 — ML & Deep Learning](track2-ml-deep-learning/README.md) | 6 | From-scratch transformer + fine-tuning experiment as portfolio artifacts, fluency in ML system design |
| [3 — DSA](track3-dsa/README.md) | 5 | 100+ problems solved across all major patterns, documented weak-spot repair, passed a full timed mock interview |
| [4 — Distributed Systems](track4-distributed-systems/README.md) | 6 | Track 1 capstone re-architected and load-tested for horizontal scale; full 4-track portfolio; passed complete back-to-back mock interview loop |

## Repo Layout

```
production-ai-engineer/
├── README.md                          ← this file
├── track1-agentic-systems/
│   ├── README.md
│   ├── week1-raw-agent/
│   ├── week2-langgraph/
│   ├── week3-multi-agent/
│   ├── week4-evals-observability/
│   ├── week5-reliability-security/
│   └── week6-deployment/
├── track2-ml-deep-learning/
│   ├── README.md
│   ├── week1-math-foundations/
│   ├── week2-nn-from-scratch/
│   ├── week3-cnn-rnn-transformers/
│   ├── week4-transformer-architecture/
│   ├── week5-training-finetuning/
│   └── week6-system-design/
├── track3-dsa/
│   ├── README.md
│   ├── week1-arrays-strings/
│   ├── week2-trees-graphs/
│   ├── week3-dynamic-programming/
│   ├── week4-heaps-tries-intervals/
│   └── week5-mock-interviews/
└── track4-distributed-systems/
    ├── README.md
    ├── week1-core-concepts/
    ├── week2-queues-caching-lb/
    ├── week3-databases-at-scale/
    ├── week4-scaling-ai-workloads/
    ├── week5-observability-reliability/
    └── week6-system-design-synthesis/
```

Each week folder holds a `README.md` with that week's objective, daily build tasks, interview questions, assessment gate, and milestone — plus whatever code/notes/writeups get produced while working through it.
