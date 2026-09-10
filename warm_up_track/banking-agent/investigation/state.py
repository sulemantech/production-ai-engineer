from typing import TypedDict

class InvestigationState(TypedDict):
    customer_id: str
    customer: dict
    accounts: list
    transactions: list
    duplicate_found: bool
    duplicate_transactions: list
    disputes: list
    disputed_transactions: list
    refund_eligible: bool
    confidence: float
