'''
                                                      START
                                │
                                ▼
                         ┌──────────────┐
                         │   "safety"   │  ← keyword check on raw message
                         └──────┬───────┘
                                │
                    route_after_safety_check
                         ┌──────┴──────┐
                         │             │
                    "escalate"    "intake"
                         │             │
                         ▼      route_after_intake_check
                  ┌───────────┐        ┌──────┴──────┐
                  │ "escalate"│        │             │
                  │  fixed    │   "clarify"    "diagnostics"
                  │  urgent   │        │             │
                  │  message  │        ▼             ▼
                  └─────┬─────┘ ┌────────────┐ ┌───────────────────────────────┐
                        │       │ "clarify"  │ │  "diagnostics" (subgraph)     │
                        │       │  fixed ask │ │  ← retry_policy(max_attempts=3)│
                        │       │  for detail│ │  [model ↔ tools ↔ approval]   │
                        │       └─────┬──────┘ └──────────────┬────────────────┘
                        │             │                       │
                        │             │            validate_diagnostics_result
                        │             │               ┌───────┴──────┐
                        │             │               │              │
                        │             │            "ok"         "invalid"
                        │             │               │              │
                        │             │               ▼              ▼
                        │             │             END        ┌────────────┐
                        │             │                        │ "fallback" │
                        │             │                        └─────┬──────┘
                        │             │                              │
                        ▼             ▼                              ▼
                       END           END                            END

'''

from langgraph.graph import StateGraph, START, END
from state import OrchestratorState
from langgraph.types import RetryPolicy
from langgraph.checkpoint.sqlite import SqliteSaver


import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "diagnostics_worker"))

from diagnostics_worker.day1_graph import graph as diagnostics_worker_builder
diagnostics_worker_graph = diagnostics_worker_builder.compile()
from safety_check import safety_check, escalate, route_after_safety_check
from intake_check import intake_check, ask_clarification, route_after_intake_check

def validate_diagnostics_result(state):
    content = state["messages"][-1]["content"]
    role = state["messages"][-1]["role"]
    if(content and role =="assistant"):
        return "ok"
    else:
        return "invalid"
    
def handle_workder_failure(state):
    return {
                "messages": [{"role": "assistant", 
                    "content": 
                    [{"type": "text", 
                    "text": "Diagnosis unavailable, please try again."
                    }]
                }]
            }

graph = StateGraph(OrchestratorState)


graph.add_node("intake",intake_check)
graph.add_node("clarify", ask_clarification)
graph.add_node("diagnostics", diagnostics_worker_graph,retry_policy=RetryPolicy(max_attempts=3))
graph.add_node("fallback", handle_workder_failure)
graph.add_node("safety",safety_check)
graph.add_node("escalate", escalate)

graph.add_conditional_edges(
    "intake",
    route_after_intake_check,
    {"clarify": "clarify", "diagnostics": "diagnostics"},
)
graph.add_edge(START, "safety")
graph.add_edge("clarify", END)

graph.add_conditional_edges(
    "diagnostics",
    validate_diagnostics_result,
    {"ok": END, "invalid": "fallback"},
)
graph.add_conditional_edges(
    "safety",
    route_after_safety_check,
    {
        "escalate": "escalate",
        "diagnostics": "intake",
    },
)

graph.add_edge("escalate", END)

graph.add_edge("fallback", END)


app = graph.compile()

with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)
    # move the __main__ test block inside this `with`

    if __name__ == "__main__":
        config = {"configurable": {"thread_id": "e2e-test-vague"}}

        result = app.invoke({"messages": [{"role": "user", "content": "My brakes are failing and I smell smoke"}]}, config=config)
        print(result["messages"][-1])

        result = app.invoke({"messages": [{"role": "user", "content": "My car is running slow and experiencing poor acceleration response."}]},config=config)
        print(result["messages"][-1])

        config = {"configurable": {"thread_id": "e2e-test-vague-1"}}
        result1 = app.invoke(
                {"messages": [{"role": "user", "content": "What does DTC code P0171 mean?"}]},
                config=config,
            )
        print("--- First response ---")
        print(result1["messages"][-1])
        result2 = app.invoke(
            {"messages": [{"role": "user", "content": "Is that expensive to fix?"}]},    
            config=config,
        )
        print("--- Second response (should reference the P0171 answer) ---")
        print(result2["messages"][-1])

        result = app.invoke({"messages": [{"role": "user", "content": "my car is broken"}]}, config={"configurable": {"thread_id": "e2e-test-clarify"}})
        print(result["messages"][-1])
