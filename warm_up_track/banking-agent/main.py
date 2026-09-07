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