# day6_stress_test.py

import sys

from langgraph.checkpoint.sqlite import SqliteSaver
from day1_graph import graph


DB_PATH = "checkpoints.db"
THREAD_ID = "stress-test-1"

config = {
    "configurable": {
        "thread_id": THREAD_ID
    }
}


def run():
    with SqliteSaver.from_conn_string(DB_PATH) as checkpointer:
        checkpointer.setup()

        app = graph.compile(checkpointer=checkpointer)

        print("Starting stress test...")
        print("Kill this process after the first tool call if you want to test recovery.")

        result = app.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                "For a 2018 BMW 320i, explain DTC P0171 and also "
                                "check for any relevant recalls."
                            ),
                        }
                    ]
                },
                config=config,
            )

        print("\nRun completed.")
        print(result)


def resume():
    with SqliteSaver.from_conn_string(DB_PATH) as checkpointer:
        checkpointer.setup()

        app = graph.compile(checkpointer=checkpointer)

        snapshot = app.get_state(config)

        print("\nRecovered checkpoint:")
        print("Next node to run:", snapshot.next)
        print("Messages:", snapshot.values["messages"])

        if snapshot.next:
            print("\nResuming graph...")

            result = app.invoke(None, config=config)

            print("\nResume completed.")
            print(result)

        else:
            print("\nNo pending work. Graph already completed.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python day6_stress_test.py run")
        print("  python day6_stress_test.py resume")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "run":
        run()

    elif mode == "resume":
        resume()

    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)