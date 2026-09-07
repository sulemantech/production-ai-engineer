'''
Lookup function for retrieving transaction information
'''
import json
from pathlib import Path


DATA_FILE = Path(__file__).parent.parent / "data" / "banking_data.json"

def load_data()->dict:
    # Placeholder implementation for demonstration purposes
    # In a real application, this would load data from a database or an external service
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return data


def lookup_transactions(account_id:str) -> dict:
    """
    Lookup transactions by account ID.

    Args:
        account_id (str): The ID of the account whose transactions to look up.

    Returns:
        dict: A dictionary containing transaction details.
    """
    # Placeholder implementation for demonstration purposes
    # In a real application, this would query a database or an external service
    data = load_data()
    return [
        transaction
        for transaction in data["transactions"]
        if transaction["account_id"] == account_id
    ]