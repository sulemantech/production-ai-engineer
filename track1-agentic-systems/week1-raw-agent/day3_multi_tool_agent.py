import time

from vehicle_issues_lookup import fetch_recalls, fetch_complaints
from llm_client import call_llm_with_retries
from dtc_lookup import search_dtc
from vin_decoder import decode_vin_code
import json

MAX_ITERATIONS  = 5
MAX_ELAPSED_TIME = 60  # seconds
 # Pricing constants for Claude Haiku 4.5
HAIKU_INPUT_COST_PER_TOKEN = 1.00 / 1_000_000
HAIKU_OUTPUT_COST_PER_TOKEN = 5.00 / 1_000_000


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
    {
    "name": "search_dtc",
    "description": (
        "Look up a vehicle diagnostic trouble code (DTC) "
        "and return its details."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "dtc_code": {
                "type": "string",
                "description": (
                    "The diagnostic trouble code to look up, "
                    "for example U0100 or P0171."
                ),
            }
        },
        "required": ["dtc_code"],
    },
},
{
    "name": "decode_vin_code",
    "description": (
        "Decode a VIN code and return vehicle information."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "vin": {
                "type": "string",
                "description": "The VIN code to decode."
            }
        },
        "required": ["vin"]
    }
},


]

# -----------------------------------------------------------------------------
# Tool dispatcher
# -----------------------------------------------------------------------------

TOOL_DISPATCHER = {
    "fetch_recalls": fetch_recalls,
    "fetch_complaints": fetch_complaints,
    "search_dtc": search_dtc,
    "decode_vin_code": decode_vin_code,
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

def force_final_answer(messages: list[dict], reason: str) -> tuple[str, int, int]:
    if reason == "timeout":
        prompt_reason = "You have reached your execution time limit."
    else:
        prompt_reason = "You have reached your maximum tool invocation limit."

    messages.append({
        "role": "user",
        "content": f"{prompt_reason} Please provide your final answer based on the information gathered so far."
    })
    
    final_response = call_llm_with_retries(messages)  # Exclude tools
    
    text_block = next(
        block for block in final_response.content if block.type == "text"
    )
    return (
        text_block.text,
        final_response.usage.input_tokens,
        final_response.usage.output_tokens
    )


def run_vehicle_agent(user_message: str) -> dict:
    messages = [{"role": "user", "content": user_message}]
    
    iteration_count = 0
    total_input_tokens = 0
    total_output_tokens = 0
    start_time = time.monotonic()

    while True:
        elapsed_time = time.monotonic() - start_time
        
        # Determine if any guard condition was triggered
        hit_max_iterations = iteration_count >= MAX_ITERATIONS
        hit_timeout = elapsed_time >= MAX_ELAPSED_TIME

        if hit_max_iterations or hit_timeout:
            reason = "timeout" if hit_timeout else "max_iterations"
            final_text, final_in, final_out = force_final_answer(messages, reason=reason)
            
            total_input_tokens += final_in
            total_output_tokens += final_out
            
            return {
                "response": final_text,
                "usage": {
                    "input_tokens": total_input_tokens,
                    "output_tokens": total_output_tokens,
                    "total_tokens": total_input_tokens + total_output_tokens,
                    "cost_usd": calculate_cost_usd(total_input_tokens, total_output_tokens)
                }
            }

        iteration_count += 1
        response = call_llm_with_retries(messages, tools=VEHICLE_TOOLS)

        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            text_block = next(
                block for block in response.content if block.type == "text"
            )
            return {
                "response": text_block.text,
                "usage": {
                    "input_tokens": total_input_tokens,
                    "output_tokens": total_output_tokens,
                    "total_tokens": total_input_tokens + total_output_tokens,
                    "cost_usd": calculate_cost_usd(total_input_tokens, total_output_tokens)
                }
            }

        if response.stop_reason == "tool_use":
            tool_results = []
            for content_block in response.content:
                is_error = False
                if content_block.type != "tool_use":
                    continue

                tool_name = content_block.name
                tool_input = content_block.input
                tool_use_id = content_block.id

                try:
                    result = dispatch_tool(tool_name, tool_input)
                except Exception as exc:
                    result = {"error": str(exc)}
                    is_error = True
              
                if result is None:
                    is_error = True
                    result = {"error": f"DTC code {tool_input.get('dtc_code')} not found."}

                tool_results.append({
                    "type": "tool_result",
                    "is_error": is_error,
                    "tool_use_id": tool_use_id,
                    "content": json.dumps(result),
                })

            messages.append({"role": "user", "content": tool_results})
            continue

        raise RuntimeError(f"Unexpected stop reason: {response.stop_reason}")

       
def calculate_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """Calculate the estimated cost in USD for token usage."""
    return (input_tokens * HAIKU_INPUT_COST_PER_TOKEN) + (output_tokens * HAIKU_OUTPUT_COST_PER_TOKEN)