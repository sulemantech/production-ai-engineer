from vehicle_issues_lookup import fetch_recalls, fetch_complaints
from llm_client import call_llm_with_retries
import json

VEHICLE_TOOLS = [
    {
        "name": "fetch_recalls",
        "description": (
            "Fetch recall information from NHTSA for a vehicle "
            "using its make, model, and model year."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "make": {
                    "type": "string",
                    "description": "Vehicle manufacturer, e.g. Toyota",
                },
                "model": {
                    "type": "string",
                    "description": "Vehicle model, e.g. Corolla",
                },
                "year": {
                    "type": "integer",
                    "description": "Vehicle model year, e.g. 2020",
                },
            },
            "required": ["make", "model", "year"],
        },
    },
    {
        "name": "fetch_complaints",
        "description": (
            "Fetch consumer complaint information from NHTSA for a vehicle "
            "using its make, model, and model year."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "make": {
                    "type": "string",
                    "description": "Vehicle manufacturer, e.g. Toyota",
                },
                "model": {
                    "type": "string",
                    "description": "Vehicle model, e.g. Corolla",
                },
                "year": {
                    "type": "integer",
                    "description": "Vehicle model year, e.g. 2020",
                },
            },
            "required": ["make", "model", "year"],
        },
    },
]

# -----------------------------------------------------------------------------
# Tool dispatcher
# -----------------------------------------------------------------------------

TOOL_DISPATCHER = {
    "fetch_recalls": fetch_recalls,
    "fetch_complaints": fetch_complaints,
}

def dispatch_tool(tool_name: str, tool_input: dict) -> dict:
    """
    Dispatch the tool call to the appropriate function.

    Args:
        tool_name: Name of the tool to call.
        tool_input: Input parameters for the tool.

    Returns:
        dict: The result from the tool function.
    """
    if tool_name not in TOOL_DISPATCHER:
        raise ValueError(f"Tool '{tool_name}' is not recognized.")

    tool_function = TOOL_DISPATCHER[tool_name]
    return tool_function(**tool_input)


# -----------------------------------------------------------------------------
# Agent
# -----------------------------------------------------------------------------

def run_vehicle_agent(user_message: str) -> str:
    """
    Run the vehicle agent with the given user message.

    The agent continues calling the LLM and dispatching tools until
    the LLM produces a final response.
    """

    messages = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    while True:
        # -------------------------------------------------------------
        # 1. Ask the LLM what to do next
        # -------------------------------------------------------------
        response = call_llm_with_retries(
            messages,
            tools=VEHICLE_TOOLS,
        )

        # -------------------------------------------------------------
        # 2. Add Claude's response to the conversation
        # -------------------------------------------------------------
        messages.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

        # -------------------------------------------------------------
        # 3. If Claude is done, return the final answer
        # -------------------------------------------------------------
        if response.stop_reason == "end_turn":
            text_block = next(
                block
                for block in response.content
                if block.type == "text"
            )
            return text_block.text

        # -------------------------------------------------------------
        # 4. Claude wants to use one or more tools
        # -------------------------------------------------------------
        if response.stop_reason == "tool_use":

            tool_results = []

            for content_block in response.content:

                if content_block.type != "tool_use":
                    continue

                tool_name = content_block.name
                tool_input = content_block.input
                tool_use_id = content_block.id

                print(f"Calling tool: {tool_name}")
                print(f"Input: {tool_input}")

                # -----------------------------------------------------
                # 5. Execute the tool
                # -----------------------------------------------------
                try:
                    result = dispatch_tool(
                        tool_name,
                        tool_input,
                    )

                except Exception as exc:
                    result = {
                        "error": str(exc),
                    }

                # -----------------------------------------------------
                # 6. Give the tool result back to Claude
                # -----------------------------------------------------
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": json.dumps(result),
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": tool_results,
                }
            )

            # -------------------------------------------------------------
            # 7. Continue the loop
            # -------------------------------------------------------------
            continue

        # -------------------------------------------------------------
        # Unexpected stop reason
        # -------------------------------------------------------------
        raise RuntimeError(
            f"Unexpected stop reason: {response.stop_reason}"
        )