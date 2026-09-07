# Subgraph:
#
# START
#   │
#   ▼
# request_approval
#   │
#   ▼
# route_after_approval
#   ├───────────────┐
#   ▼               ▼
# tools       handle_decline
#   │               │
#   ▼               ▼
#  END             END
#
# The subgraph encapsulates the approval + tool execution workflow
# and can be invoked as a single node from a parent graph.

from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict
from day1_graph import AgentState, execute_tools
from day4_interrupt_graph import request_approval, route_after_approval, handle_decline
from day1_graph import execute_tools, call_model, should_continue
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

subgraph = StateGraph(AgentState)
subgraph.add_node("request_approval", request_approval)
subgraph.add_node("tools", execute_tools)
subgraph.add_node("handle_decline", handle_decline)

subgraph.add_edge(START, "request_approval")
subgraph.add_conditional_edges("request_approval", 
                               route_after_approval, 
                               {"tools": "tools", 
                                "handle_decline": "handle_decline"
                               })

subgraph.add_edge("tools",END)
subgraph.add_edge("handle_decline", END)
compiled_subgraph = subgraph.compile()

def gated_tool_execution(state:AgentState):
    last_message = state["messages"][-1]
    result = compiled_subgraph.invoke({"messages":[last_message]})
    return {"messages": [result["messages"][-1]]}


parent = StateGraph(AgentState)
parent.add_node("model", call_model)
parent.add_node("gated_tool_execution", gated_tool_execution)

parent.add_edge(START, "model")
parent.add_conditional_edges("model", should_continue, {"tools": "gated_tool_execution", END: END})
parent.add_edge("gated_tool_execution", "model")

with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    checkpointer.setup()
    app = parent.compile(checkpointer=checkpointer)

    if __name__ == "__main__":
        config = {"configurable": {"thread_id": "day5-test-1"}}
        result1 = app.invoke(
            {"messages": [{"role": "user", "content": "Decode VIN 1HGCM82633A004352"}]},
            config=config,
        )
        print("--- Paused? ---")
        print(result1)

        answer = input("Approve this? (y/n): ").strip().lower()
        result2 = app.invoke(Command(resume=answer == "y"), config=config)
        print("--- Resumed ---")
        print(result2["messages"][-1])


