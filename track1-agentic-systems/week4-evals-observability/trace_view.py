import sys
from langsmith import Client

from dotenv import load_dotenv
PROJECT_NAME = "carscannerai-week4"

load_dotenv()

def format_duration(start_time, end_time):
    if not start_time or not end_time:
        return "N/A"

    duration = (end_time - start_time).total_seconds()
    return f"{duration:.3f}s"


def print_run(run, level=0):
    indent = "  " * level

    print(f"{indent}Node: {run.name}")
    print(f"{indent}Run ID: {run.id}")
    print(f"{indent}Start: {run.start_time}")
    print(f"{indent}End:   {run.end_time}")
    print(
        f"{indent}Duration: "
        f"{format_duration(run.start_time, run.end_time)}"
    )
    print(f"{indent}Error: {'YES' if run.error else 'NO'}")

    print(f"{indent}Inputs:")
    print(f"{indent}{run.inputs}")

    print(f"{indent}Outputs:")
    print(f"{indent}{run.outputs}")

    print()


def trace_case(case_id):
    client = Client()

    print(f"\nSearching for case: {case_id}")
    print(f"Project: {PROJECT_NAME}")
    print("=" * 80)

    # 1. Find the run tagged with this golden-set case ID
    runs = list(
        client.list_runs(
            project_name=PROJECT_NAME,
            filter=f'has(tags, "{case_id}")',
        )
    )

    if not runs:
        print("No runs found.")
        return

    print(f"Found {len(runs)} tagged run(s).")

    # For now, use the earliest matching run as the root.
    root = min(runs, key=lambda run: run.start_time)

    print("\nROOT RUN")
    print("=" * 80)
    print_run(root)

    # 2. Get every run belonging to the same trace
    trace_runs = list(
        client.list_runs(
            project_name=PROJECT_NAME,
            trace_id=root.trace_id,
        )
    )

    # 3. Sort chronologically
    trace_runs.sort(
        key=lambda run: run.start_time or root.start_time
    )

    print("\nTRACE")
    print("=" * 80)

    for run in trace_runs:
        print_run(run)

    print("=" * 80)
    print(f"Trace ID: {root.trace_id}")
    print(f"Total spans: {len(trace_runs)}")


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python trace_view.py <case_id>")
        print()
        print("Example:")
        print("  python trace_view.py dtc_p0171")
        sys.exit(1)

    case_id = sys.argv[1]

    trace_case(case_id)


if __name__ == "__main__":
    main()