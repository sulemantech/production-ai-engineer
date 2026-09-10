"""
                         MAIN / PARENT GRAPH

Customer request
      │
      ▼
┌──────────────────┐
│ classify_intent  │  ← LLM
└────────┬─────────┘
         │
         ▼
┌──────────────┐
│ route_intent │  ← deterministic router
└──────┬───────┘
       │
       │ "transaction_issue"
       ▼
╔══════════════════════════════════════════════════════════════╗
║                  INVESTIGATION SUBGRAPH                     ║
║                                                              ║
║ START                                                        ║
║   │                                                          ║
║   ▼                                                          ║
║ get_customer                                                 ║
║   │                                                          ║
║   ▼                                                          ║
║ get_accounts                                                  ║
║   │                                                          ║
║   ▼                                                          ║
║ get_transactions                                              ║
║   │                                                          ║
║   ▼                                                          ║
║ find_duplicates                                               ║
║   │                                                          ║
║   ▼                                                          ║
║ check_disputes                                                ║
║   │                                                          ║
║   ▼                                                          ║
║ check_refund_eligibility                                      ║
║   │                                                          ║
║   ▼                                                          ║
║ calculate_confidence                                          ║
║   │                                                          ║
║   ▼                                                          ║
║ END                                                          ║
╚═══════════════════════════════╤══════════════════════════════╝
                                │
                                │ investigation_result
                                ▼
                       ┌────────────────┐
                       │ decide_outcome │
                       └───────┬────────┘
                               │
                               ▼
                        route_outcome
                     ┌────────┼────────┐
                     ▼        ▼        ▼
                  refund   clarify  human_review
                     │        │        │
                     └────────┴────────┘
                              │
                              ▼
                             END
"""

from langgraph.graph import StateGraph, START, END

from graph.state import BankingAgentState

from graph.nodes import (
    classify_intent,
    route_intent,
    investigation_subgraph,
    decide_outcome,
    route_outcome,
    refund,
    clarify,
    human_review,
)


graph = StateGraph(BankingAgentState)


# --------------------------------------------------
# Nodes
# --------------------------------------------------

graph.add_node("classify_intent", classify_intent)

graph.add_node(
    "investigation",
    investigation_subgraph
)

graph.add_node(
    "decide_outcome",
    decide_outcome
)

graph.add_node("refund", refund)

graph.add_node("clarify", clarify)

graph.add_node("human_review", human_review)


# --------------------------------------------------
# Start
# --------------------------------------------------

graph.add_edge(
    START,
    "classify_intent"
)


# --------------------------------------------------
# Intent routing
# --------------------------------------------------

graph.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "investigation": "investigation",
        "decide_outcome": "decide_outcome",
    }
)


# --------------------------------------------------
# Investigation → outcome decision
# --------------------------------------------------

graph.add_edge(
    "investigation",
    "decide_outcome"
)


# --------------------------------------------------
# Outcome routing
# --------------------------------------------------

graph.add_conditional_edges(
    "decide_outcome",
    route_outcome,
    {
        "refund": "refund",
        "clarify": "clarify",
        "human_review": "human_review",
    }
)


# --------------------------------------------------
# End states
# --------------------------------------------------

graph.add_edge("refund", END)

graph.add_edge("clarify", END)

graph.add_edge("human_review", END)


app = graph.compile()