"""
Transaction Investigation Subgraph

START
  │
  ▼
┌──────────────────┐
│   get_customer   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   get_accounts   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  get_transactions    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   find_duplicates    │
└──────────┬───────────┘
           │
           ▼
          END
"""

from datetime import datetime
import sys
from pathlib import Path


from tools.customer import lookup_customer
from tools.accounts import lookup_accounts
from tools.transactions import lookup_transactions
from tools.disputes import lookup_disputes


def get_customer(state):
    customer_id = state["customer_id"]
    customer = lookup_customer(customer_id)
    state["customer"] = customer
    return {"customer": customer}

def get_accounts(state):
    customer_id = state["customer_id"]
    result = lookup_accounts(customer_id)
    state["accounts"] = result.get("accounts", [])
    return {"accounts": state["accounts"]}

def get_transactions(state):
    # Implementation for getting transactions
    accounts = state["accounts"]
    transactions = []
    for account in accounts:
        account_id = account["account_id"]
        account_transactions = lookup_transactions(account_id)
        transactions.extend(account_transactions)
    return {"transactions": transactions}

def find_duplicates(state):
    # Implementation for finding duplicates
    duplicate_txns=[]
    transactions = state["transactions"]
    for i, txn in enumerate(transactions):
        for j, other_txn in enumerate(transactions):
            if j <= i or txn["merchant"] != other_txn["merchant"] or txn["amount"] != other_txn["amount"]:
                continue
            t1 = datetime.fromisoformat(txn["timestamp"])
            t2 = datetime.fromisoformat(other_txn["timestamp"])
            if(abs((t1 - t2).total_seconds()) <= 300):
                duplicate_txns.append({"transaction_1": txn["transaction_id"], "transaction_2": other_txn["transaction_id"], "merchant": txn["merchant"], "amount": txn["amount"], "timestamp": txn["timestamp"]})
    return {"duplicate_found": len(duplicate_txns) > 0, "duplicate_transactions": duplicate_txns}


def check_disputes(state):
    customer_id = state["customer_id"]
    transactions = state["transactions"]
    result = lookup_disputes(customer_id)
    disputes = result.get("disputes", [])
    disputed_transactions = []
    for txn in transactions:
        for dispute in disputes:
            if txn["transaction_id"] == dispute["transaction_id"]:
                disputed_transactions.append(txn)
    state["disputes"] = disputes
    state["disputed_transactions"] = disputed_transactions
    return {"disputes": disputes, "disputed_transactions": disputed_transactions}


def check_refund_eligibility(state):
    duplicate_found = state["duplicate_found"]
    disputed_transactions = state["disputed_transactions"]
    refund_eligible = duplicate_found and len(disputed_transactions) > 0
    return {"refund_eligible": refund_eligible}


def calculate_confidence(state):
    duplicate_found = state["duplicate_found"]
    refund_eligible = state["refund_eligible"]
    confidence = 0.0
    if duplicate_found and refund_eligible:
        confidence = 0.9
    elif duplicate_found or refund_eligible:
        confidence = 0.5
    return {"confidence": confidence}