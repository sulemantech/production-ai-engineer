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

---

## How my agent loop works
1. What the agent does
   The agent helps answer vehicle-diagnostic questions. It gives Claude three tools: one for looking up DTC codes, and two for checking recalls and complaints from NHTSA. Claude decides which tools are actually needed for each question. So a simple DTC question might use only `search_dtc`, while a broader question about a vehicle could require all three.

2. How the main loop works
   Every time we talk to Claude, we send the conversation history along with the available tool definitions. Claude then tells us what it wants to do next. If it returns `"tool_use"`, it means it wants our code to run one or more tools. If it returns `"end_turn"`, it means it has enough information and is ready to give the final answer.

3. Where Claude stops and our code takes over
   Claude doesn't actually run Python functions or call the NHTSA API itself. It simply sends us a structured request saying, essentially, *"I want to call this tool with these parameters."* Our dispatcher receives that request and turns it into the actual Python function call. This is separate from the safety guards — the dispatcher controls **how a tool gets executed**, while the guards control **how far the agent is allowed to run**.

4. How multiple tools are handled
   Claude can ask for several tools in the same response. For example, it might ask for recalls, complaints, and DTC information all at once. Our loop goes through those requests, runs each tool, collects the results, and sends them back to Claude together. At the moment, though, the tools run **one after another**, not at the same time. That's why a query using all three tools can take around 33 seconds.

5. The three limits that keep the agent under control
   There are three main safeguards. A maximum iteration limit prevents the agent from getting stuck in an endless tool-calling loop. A timeout prevents one slow operation from making the whole request run indefinitely. And **cost tracking** keeps track of the tokens used across all the Claude calls, including any fallback call, so we can estimate the cost. If one of these limits is reached, the system tries to produce a final answer rather than simply crashing.

6. How tool errors are handled
   If a tool fails — for example, because the arguments are wrong, an API throws an exception, or no data is found — we don't let the raw error or Python traceback go straight to Claude. Instead, we turn it into a consistent error response such as `{"error": "..."}`. We also mark the tool result as an error, so Claude clearly knows that the tool failed and can respond appropriately.

7. The main limitation right now
   The biggest limitation is that the tools currently run sequentially. If Claude needs all three tools, each one has to finish before the next starts, which contributed to the roughly 33-second response time we measured. Since recalls and complaints don't depend on each other, they could be run **in parallel** later to reduce the overall response time significantly.

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
