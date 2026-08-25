from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Optional, Union

# Graph:
#
#                         ┌──────────────┐
#                         │    START     │
#                         └──────┬───────┘
#                                │
#                                ▼
#                         ┌──────────────┐
#                         │   classify   │
#                         └──────┬───────┘
#                                │
#                                ▼
#                         ┌──────────────┐
#                         │    lookup    │
#                         └──────┬───────┘
#                                │
#                                ▼
#                         ┌──────────────┐
#                    ┌───►│   billing    │
#                    │    └──────┬───────┘
#                    │           │
#                    │           ▼
#                    │    ┌──────────────┐
#                    │    │     eval     │
#                    │    └──────┬───────┘
#                    │           │
#                    │      conditional
#                    │           │
#                    │      ┌────┴────┐
#                    │      │         │
#                    │    "end"    "retry"
#                    │      │         │
#                    │      ▼         │
#                    │     END        │
#                    │                │
#                    └────────────────┘
#
# Flow:
# START → classify → lookup → billing → eval
#                                      │
#                         ┌────────────┴────────────┐
#                         │                         │
#                      "end"                     "retry"
#                         │                         │
#                         ▼                         │
#                        END                        │
#                                                   │
#                                                   ▼
#                                                billing

class CSAgentState(TypedDict):
    customer_id:str
    issue:str
    billing_record:list
    status:str
    issue_type:str
    attempts:int
    resolution:str
    resolved:bool


def classify_issue(state: CSAgentState) -> CSAgentState:
     return {
        "issue_type": "billing"
    }

def lookup_customer(state: CSAgentState):
    print(f"Looking up customer: {state['customer_id']}")
    return {
        "status": "customer_found"
    }

def check_billing(state: CSAgentState):
    print("Checking billing records....")
    return{
        "status":"billing_checked",
        "attempts": state['attempts'] + 1
    }

def evaluate_result(state: CSAgentState) -> None:
    if(state['billing_record']):
        return {
            "resolved":True,
            "resolution":"Billing issue identified"
        } 
    return {
        "resolved": False
    }

def route_after_evaluation(state: CSAgentState):
    if state['resolved']:
        return "end"

    if state['attempts'] >= 3:
        return "end"

    return "retry"

graph = StateGraph(CSAgentState)

graph.add_node("classify",classify_issue)
graph.add_node("lookup", lookup_customer)
graph.add_node("billing", check_billing)
graph.add_node("eval", evaluate_result)

graph.add_edge(START, "classify")
graph.add_edge("classify","lookup")
graph.add_edge("lookup","billing")
graph.add_edge("billing", "eval")
# graph.add_edge("eval", END)

graph.add_conditional_edges("eval", route_after_evaluation,{"end":END, "retry":"billing"})

app = graph.compile()

initial_state = {
    "customer_id": "C001",
    "issue": "I was charged twice",
    "billing_record": [],
    "status": "",
    "issue_type": "",
    "attempts": 0,
    "resolution": "",
    "resolved": False
}

result = app.invoke(initial_state)

print(result)
