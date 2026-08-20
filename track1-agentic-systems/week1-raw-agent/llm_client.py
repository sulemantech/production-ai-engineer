import random
import time

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-4-5"
MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_TOKENS = 1024

client = anthropic.Anthropic()


def call_llm_with_retries(
    messages: list[dict],
    tools: list[dict] = [],
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
