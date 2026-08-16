[← Track 1](../README.md)

# Week 1 — Agent Fundamentals, From Scratch (Raw API, No Framework)

**Objective:** Strip the framework away. Understand exactly what a tool-calling agent loop does, so LangGraph stops being a black box.

## Daily Build
- **Day 1:** Raw Anthropic API call, no tools. Handle streaming, errors, retries with backoff.
- **Day 2:** Add one tool (e.g. calculator or web search stub). Build the tool schema + dispatch logic by hand.
- **Day 3:** Add a second and third tool. Build the full agentic loop: model responds → tool call detected → tool executed → result fed back → loop until final answer.
- **Day 4:** Add loop guards: max iterations, timeout, cost tracking per run (token count → $ estimate).
- **Day 5:** Add structured error handling: malformed tool args, tool exceptions, model refusing to call a needed tool.
- **Day 6-7:** Polish + write a one-page "how my agent loop works" doc (no code, just architecture).

## Daily Interview Questions
1. Walk me through what happens between a user message and a tool call executing, step by step.
2. Why would an agent loop infinitely, and how do you prevent it?
3. What's the difference between a tool call and a plain function call in your code — where's the boundary?
4. How do you handle a tool that returns malformed data the model didn't expect?
5. Why build this without a framework first? What does LangGraph actually save you from writing?
6. What would you change about your tool schema design if a tool needed to return a huge payload (e.g. a 10k-row table)?

## Week 1 Assessment Gate
- Explain your agent loop from memory, no code visible.
- Live task: add a new tool to your existing agent, timed (~15 min).
- Scenario question: "Your agent just called a tool 40 times in a row — diagnose it live."
- **Pass bar:** Explains the loop cold, adds a tool without referencing docs, names 2+ real failure modes unprompted.

## Milestone
Working raw-API agent (3 tools), loop guards, cost tracking, and a written architecture explanation you can recite.

## Notes / Artifacts

_Log work, links, and outcomes for this week here as you go._

---
[← Track 1](../README.md) · [Next: Week 2 — LangGraph →](../week2-langgraph/README.md)
