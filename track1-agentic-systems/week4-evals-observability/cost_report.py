import sys
from langsmith import Client
from dotenv import load_dotenv

PROJECT_NAME = "carscannerai-week4"

load_dotenv()

def format_duration(start_time, end_time):
    if not start_time or not end_time:
        return 0.0

    return (end_time - start_time).total_seconds()


def get_llm_runs(client):
    return list(
        client.list_runs(
            project_name=PROJECT_NAME,
            run_type="llm",
        )
    )


def main():
    client = Client()

    print(f"\nProject: {PROJECT_NAME}")
    print("=" * 80)

    runs = get_llm_runs(client)

    if not runs:
        print("No LLM runs found.")
        return

    total_tokens = 0
    total_cost = 0.0
    total_duration = 0.0

    for run in runs:
        tokens = run.total_tokens or 0
        cost = float(run.total_cost or 0.0)
        duration = format_duration(
            run.start_time,
            run.end_time,
        )

        total_tokens += tokens
        total_cost += cost
        total_duration += duration

    print(f"LLM calls:       {len(runs)}")
    print(f"Total tokens:    {total_tokens:,}")
    print(f"Total cost:      ${total_cost:.6f}")
    print(f"Total LLM time:  {total_duration:.3f}s")

    print("=" * 80)


if __name__ == "__main__":
    main()