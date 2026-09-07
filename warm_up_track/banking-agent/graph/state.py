from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Optional, Union

class BankingAgentState(TypedDict):
    customer_message: str
    customer_id: str
    intent: str
    investigation_result: dict
    decision: str
    response: str