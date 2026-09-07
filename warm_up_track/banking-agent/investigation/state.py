from langgraph.graph import Graph, START, END
from typing import TypedDict, List, Optional, Union

class InvestigationState(TypedDict):
    customer_id: str
    account: dict
    transactions: list
    disputes: list
    duplicate_found: bool
    refund_eligible: bool
    confidence: float