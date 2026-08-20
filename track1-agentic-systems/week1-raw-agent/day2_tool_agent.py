import json
import random
import time

import anthropic
from dotenv import load_dotenv

from dtc_lookup import search_dtc

from llm_client import call_llm_with_retries

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