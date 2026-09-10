from tools.transactions import load_data

def lookup_disputes(customer_id:str) -> dict:
    """
    Lookup disputes by account ID.

    Args:
        account_id (str): The ID of the account whose disputes to look up.

    Returns:
        dict: A dictionary containing dispute details.
    """
    # Placeholder implementation for demonstration purposes
    # In a real application, this would query a database or an external service
    data = load_data()
    disputes =[dispute for dispute in data["disputes"] if dispute["customer_id"] == customer_id]
    if disputes:
        return {"disputes": disputes}
    else:
        return {"error": "Dispute not found",
                "customer_id": customer_id
                }