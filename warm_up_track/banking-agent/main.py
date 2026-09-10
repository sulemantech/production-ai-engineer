'''
                    main.py
                       │
                       ▼
              ┌─────────────────┐
              │   Parent Graph  │
              │                 │
              │ Intent / Router │
              └────────┬────────┘
                       │
                       ▼
          ┌─────────────────────────┐
          │ Transaction Investigation│
          │       SUBGRAPH           │
          │                          │
          │ Customer                │
          │ Account                 │
          │ Transactions            │
          │ Duplicate Check         │
          │ Dispute Check           │
          │ Refund Eligibility      │
          │ Confidence              │
          └────────────┬────────────┘
                       │
                  Evidence +
                  Confidence
                       │
                       ▼
              ┌─────────────────┐
              │ Parent Decision │
              │                 │
              │ Refund          │
              │ Clarify         │
              │ Human Review    │
              └─────────────────┘
              '''


from graph.graph import app

if __name__ == "__main__":
    initial_state = {
        "customer_message": "I was charged twice by Amazon for the same order.",
        "customer_id": "CUST001",
        "intent": "",
        "investigation_result": {},
        "decision": "",
        "response": "",
    }

    result = app.invoke(initial_state)

    print("--- Final state ---")
    print(result)
    print()
    print("--- Response to customer ---")
    print(result["response"])
