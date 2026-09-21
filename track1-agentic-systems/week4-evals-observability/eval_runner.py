import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "week3-multi-agent")
)

from graph import build_app
from golden_set import GOLDEN_SET
from langgraph.types import Command


def get_actual_route(app, config, case):
    """Determine the route from the final LangGraph state."""
    state = app.get_state(config)
    values = state.values or {}

    print(f"\n--- State for {case['id']} ---")
    print(values)

    if values.get("safety_critical") is True:
        return "escalate"

    if values.get("needs_clarification") is True:
        return "clarify"

    response_text = get_final_message({"messages": values.get("messages", [])})

    if "Diagnosis unavailable" in response_text:
        return "fallback"


    return "diagnostics"

def check_route_only(app, config, case):
    """Check whether the graph took the expected route."""
    actual_route = get_actual_route(app, config, case)
    expected_route = case.get("expected_route")

    passed = actual_route == expected_route

    return passed, (
        f"expected_route={expected_route}, "
        f"actual_route={actual_route}"
    )


def check_keyword_match(response, case):
    """Check whether all expected keywords appear in the response."""
    expected_keywords = case.get("expected_keywords", [])

    text = response.lower()

    missing = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() not in text
    ]

    passed = not missing

    return passed, (
        "all keywords found"
        if passed
        else f"missing={missing}"
    )


def get_final_message(result):
    """Extract the final assistant message from the graph result."""
    messages = result.get("messages", [])

    if not messages:
        return ""

    message = messages[-1]

    if isinstance(message, dict):
        content = message.get("content", "")

        if isinstance(content, list):
            return " ".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
            )

        return str(content)

    return getattr(message, "content", "") or ""

def check_llm_judge(response, case):
    """Evaluate the response using an LLM judge."""

    criteria = case.get("judge_criteria", [])

    # Day 2: inspect the response and criteria.
    print("\n--- LLM Judge Input ---")
    print("Case:", case["id"])
    print("Response:", response)
    print("Criteria:", criteria)

    # Temporary until the actual judge is connected.
    return True, f"response collected: {response[:150]}"


def run_case(app, case):
    """Run one golden-set case against the real application."""

    config = {
        "configurable": {
            "thread_id": case["thread_id"]
        }
    }

    # First invocation.
    result = app.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": case["input"],
                }
            ]
        },
        config=config,
    )

    # If the graph paused for human approval, resume it.
    if "__interrupt__" in result:
        print("\n--- Human approval required ---")
        print(result["__interrupt__"])

        result = app.invoke(
            Command(resume=True),
            config=config,
        )

    check_type = case["check_type"]

    if check_type == "route_only":
        return check_route_only(app, config, case)

    response = get_final_message(result)

    if check_type == "keyword_match":
        return check_keyword_match(response, case)

    if check_type == "llm_judge":
        return check_llm_judge(response, case)

    raise ValueError(f"Unknown check_type: {check_type}")

    
def main():
    passed_count = 0

    print(
        f"\nRunning {len(GOLDEN_SET)} golden-set cases...\n"
    )

    # Keep the SQLite checkpointer alive for the entire evaluation.
    with build_app() as app:

        for case in GOLDEN_SET:
            name = case["id"]

            try:
                passed, details = run_case(app, case)

                if passed:
                    passed_count += 1
                    status = "PASS"
                else:
                    status = "FAIL"

                print(f"[{status}] {name}")
                print(f"       {details}")

            except Exception as exc:
                print(f"[FAIL] {name}")
                print(f"       error={exc}")

    total = len(GOLDEN_SET)
    failed_count = total - passed_count

    print("\n" + "=" * 50)
    print(
        f"Results: {passed_count}/{total} passed, "
        f"{failed_count} failed"
    )
    print("=" * 50)


if __name__ == "__main__":
    main()