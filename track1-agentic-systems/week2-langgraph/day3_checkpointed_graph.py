from day1_graph import graph
from langgraph.checkpoint.sqlite import SqliteSaver

with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    checkpointer.setup()
    app = graph.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "conversation-1"}}

    result1 = app.invoke(
        {"messages": [{"role": "user", "content": "What does DTC code P0171 mean?"}]},
        config=config,
    )
    print("--- First response ---")
    print(result1["messages"][-1])

    result2 = app.invoke(
        {"messages": [{"role": "user", "content": "Is that expensive to fix?"}]},
        config=config,
    )
    print("--- Second response (should reference the P0171 answer) ---")
    print(result2["messages"][-1])
