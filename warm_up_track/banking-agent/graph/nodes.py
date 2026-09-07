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

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from customer import lookup_customer
from accounts import lookup_accounts
from transactions import lookup_transactions
from disputes import lookup_disputes


def get_customer(state):
    customer_id = state["customer_id"]
    customer = lookup_customer(customer_id)
    return {"customer": customer}

def get_accounts(state):
    customer_id = state["customer_id"]
    accounts = lookup_accounts(customer_id)
    return {"accounts": accounts}

def get_transactions(state):
    # Implementation for getting transactions
    customer_id = state["customer_id"]
    transactions = lookup_transactions(customer_id)
    return {"transactions": transactions}

def find_duplicates(state):
    # Implementation for finding duplicates
    customer_id = state["customer_id"]
    transactions = lookup_transactions(customer_id)
    # Placeholder implementation - replace with actual duplicate finding logic
    return {"duplicates": []}