"""
                 INVESTIGATION SUBGRAPH

customer_id
     │
     ▼
┌──────────────┐
│ get_customer │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ get_accounts │
└──────┬───────┘
       │
       ▼
┌───────────────────┐
│ get_transactions  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  find_duplicates   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   check_disputes  │
└─────────┬─────────┘
          │
          ▼
┌──────────────────────────┐
│ check_refund_eligibility │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   calculate_confidence   │
└────────────┬─────────────┘
             │
             ▼
            END

INPUT:
    customer_id

OUTPUT:
    investigation_result
"""

from langgraph.graph import StateGraph, START, END

from investigation.state import InvestigationState

from investigation.nodes import (
    get_customer,
    get_accounts,
    get_transactions,
    find_duplicates,
    check_disputes,
    check_refund_eligibility,
    calculate_confidence
)


graph = StateGraph(InvestigationState)


graph.add_node(
    "get_customer",
    get_customer
)

graph.add_node(
    "get_accounts",
    get_accounts
)

graph.add_node(
    "get_transactions",
    get_transactions
)

graph.add_node(
    "find_duplicates",
    find_duplicates
)

graph.add_node(
    "check_disputes",
    check_disputes
)

graph.add_node(
    "check_refund_eligibility",
    check_refund_eligibility
)

graph.add_node(
    "calculate_confidence",
    calculate_confidence
)


graph.add_edge(
    START,
    "get_customer"
)

graph.add_edge(
    "get_customer",
    "get_accounts"
)

graph.add_edge(
    "get_accounts",
    "get_transactions"
)

graph.add_edge(
    "get_transactions",
    "find_duplicates"
)

graph.add_edge(
    "find_duplicates",
    "check_disputes"
)

graph.add_edge(
    "check_disputes",
    "check_refund_eligibility"
)

graph.add_edge(
    "check_refund_eligibility",
    "calculate_confidence"
)

graph.add_edge(
    "calculate_confidence",
    END
)


investigation_graph = graph.compile()