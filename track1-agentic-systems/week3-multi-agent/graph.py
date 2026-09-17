'''
                              START
                                │
                                ▼
                         ┌──────────────┐
                         │   "safety"   │  ← keyword check on raw user message
                         └──────┬───────┘
                                │
                    route_after_safety_check
                         ┌──────┴──────┐
                         │             │
                    "escalate"   "diagnostics"
                         │             │
                         ▼             ▼
                  ┌───────────┐  ┌───────────────────────────────┐
                  │ "escalate"│  │  "diagnostics" (subgraph)     │
                  │  fixed    │  │  ← retry_policy(max_attempts=3)│
                  │  urgent   │  │  [model ↔ tools ↔ approval]   │
                  │  message  │  └──────────────┬────────────────┘
                  └─────┬─────┘                 │
                        │              validate_diagnostics_result
                        │                 ┌──────┴──────┐
                        │                 │             │
                        │              "ok"        "invalid"
                        │                 │             │
                        │                 ▼             ▼
                        │               END        ┌────────────┐
                        │                          │ "fallback" │
                        │                          └──────┬─────┘
                        │                                 │
                        ▼                                 ▼
                       END                               END

'''

from langgraph.graph import StateGraph, START, END
from state import OrchestratorState
from langgraph.types import RetryPolicy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "diagnostics_worker"))

from diagnostics_worker.day1_graph import graph as diagnostics_worker_builder
diagnostics_worker_graph = diagnostics_worker_builder.compile()
from safety_check import safety_check, escalate, route_after_safety_check

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


graph.add_node("diagnostics", diagnostics_worker_graph,retry_policy=RetryPolicy(max_attempts=3))
graph.add_node("fallback", handle_workder_failure)
graph.add_node("safety",safety_check)
graph.add_node("escalate", escalate)

graph.add_edge(START, "safety")

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
        "diagnostics": "diagnostics",
    },
)
graph.add_edge("escalate", END)

graph.add_edge("fallback", END)


app = graph.compile()
if __name__ == "__main__":
    result = app.invoke({"messages": [{"role": "user", "content": "My brakes are failing and I smell smoke"}]})
    print(result["messages"][-1])
