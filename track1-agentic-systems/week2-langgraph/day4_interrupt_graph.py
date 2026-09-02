from day1_graph import AgentState, call_model, execute_tools, should_continue
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command


# -----------------------------------------------------------------------------
# Plan
#
# Reuses Day 1's graph builder (same nodes: model, tools) and Day 3's
# checkpointer pattern (SqliteSaver, thread_id-keyed), and adds one new
# piece: a human-approval gate before a "risky" tool actually runs.
#
#            ┌──────────────┐
#     START ─▶     model     │◀────────────┐
#            └──────┬───────┘             │
#                    │                     │
#             should_continue()            │
#                    │                     │
#           ┌────────┴────────┐            │
#           │                 │            │
#        "tools"             END           │
#           │                               │
#           ▼                               │
#   ┌─────────────────┐                     │
#   │ request_approval │  <- NEW: calls interrupt()
#   │ if tool is risky │     if the requested tool is in
#   └────────┬─────────┘     RISKY_TOOLS, else passes through
#            │
#     approved? ──── declined ──▶ back to model with a decline message
#            │
#            ▼
#          tools ──────────────────────────▶ model (loop, unchanged)
#
# -----------------------------------------------------------------------------

# decode_vin_code requires approval before running: it's the most
# identifying/personal of the four tools (a VIN maps to a specific,
# real vehicle owner), unlike the other three which are anonymous
# lookups by code/make/model.
RISKY_TOOLS = {"decode_vin_code"}

# TODO: write request_approval(state) — inspect the last message's
# tool_use blocks; if any tool name is in RISKY_TOOLS, call interrupt()
# with enough detail for a human to decide, and store the decision.
def request_approval(state):
    last_message = state["messages"][-1]
    
    tool_use_blocks = [
        block for block in last_message.get("blocks", [])
        if block["type"] == "tool_use"
    ]
    risky_tools_requested = [
        block for block in tool_use_blocks
        if block["name"] in RISKY_TOOLS
    ]

    if not risky_tools_requested:
        return {"human_approved": True}

    # If there are risky tools requested, call interrupt() to ask for human approval
    decision = interrupt({
        "risky_tools": [block["name"] for block in risky_tools_requested],
        "question": "Approve execution of the requested risky tools?",
    })
    return {"human_approved": decision}
# TODO: write a routing function for the conditional edge out of
# request_approval — approved (or nothing risky requested) -> "tools",
# declined -> "model" with an injected message telling Claude the human
# said no (same pattern as is_error: surface it, don't swallow it).
def route_after_approval(state):
    if state.get("human_approved", False):
        return "tools"
    else:
        # Inject a message indicating the human declined the risky tool execution
        decline_message = {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Human approval denied execution of the requested risky tools."
                }
            ]
        }
        state["messages"].append(decline_message)
        return "model"

# TODO: wire request_approval into the graph between "model" and "tools",
# and compile with a SqliteSaver checkpointer (same as day3_checkpointed_graph.py).

# TODO: test the same two-step way as Day 3/the hospitality drill —
# first invoke() should return with __interrupt__ present when a risky
# tool is requested, second invoke(Command(resume=...)) should complete it.

graph = StateGraph(AgentState)
graph.add_node("model", call_model)
graph.add_node("request_approval", request_approval)
graph.add_node("tools", execute_tools)

graph.add_edge(START, "model")
graph.add_conditional_edges(
    "model",
    should_continue,
    {"tools": "request_approval", END: END},  # redirect through the gate
)
graph.add_conditional_edges(
    "request_approval",
    route_after_approval,
    {"tools": "tools", "model": "model"},
)
graph.add_edge("tools", "model")

with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
