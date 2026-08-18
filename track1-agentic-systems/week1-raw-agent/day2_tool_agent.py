import json
import random
import time

import anthropic
from dotenv import load_dotenv

from dtc_lookup import search_dtc


MODEL = "claude-haiku-4-5"
MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_TOKENS = 1024


load_dotenv()

client = anthropic.Anthropic()


search_dtc_tool = {
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
}


def call_llm_with_retries(
    messages: list[dict],
    tools: list[dict],
    model: str = MODEL,
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY,
    max_tokens: int = MAX_TOKENS,
) -> anthropic.types.Message:

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                max_tokens=max_tokens,
                messages=messages,
                model=model,
                tools=tools,
            )

            return response

        except anthropic.RateLimitError as e:
            print(f"Rate limit error occurred: {e}")

        except anthropic.BadRequestError as e:
            print(f"Bad request error occurred: {e}")
            raise

        except anthropic.APIError as e:
            print(f"API error occurred: {e}")

        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)

    raise RuntimeError(
        f"LLM call failed after {max_retries} attempts"
    )

def run_agent(user_message: str) -> str:
    messages = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    response = call_llm_with_retries(
        messages,
        tools=[search_dtc_tool],
    )

    while response.stop_reason == "tool_use":

        tool_use = next(
            block
            for block in response.content
            if block.type == "tool_use"
        )

        # Dispatcher
        if tool_use.name == "search_dtc":
            result = search_dtc(
                tool_use.input["dtc_code"]
            )

            if result is None:
                result = {
                    "error": (
                        f"DTC code "
                        f"{tool_use.input['dtc_code']} "
                        f"not found."
                    )
                }

        else:
            result = {
                "error": f"Unknown tool: {tool_use.name}"
            }

        # Add Claude's tool request
        messages.append({
            "role": "assistant",
            "content": response.content,
        })

        # Add tool result
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result),
                }
            ],
        })

        # Ask Claude again
        response = call_llm_with_retries(
            messages,
            tools=[search_dtc_tool],
        )

    # Get final text response
    text_block = next(
        block
        for block in response.content
        if block.type == "text"
    )

    return text_block.text