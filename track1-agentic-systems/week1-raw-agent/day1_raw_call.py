import os
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


def call_llm_with_retries(messages:list[dict], model:str=MODEL, max_retries:int=MAX_RETRIES, base_delay:float=BASE_DELAY, max_tokens:int=MAX_TOKENS):
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                max_tokens=max_tokens,
                messages = messages,
                model=model
            )
            response_text = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            print(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
            return response_text
        except anthropic.RateLimitError as e:
            print("Rate limit error occurred: {}".format(e))
        except anthropic.BadRequestError as e:
            print("Bad request error occurred: {}".format(e))
            raise
        except anthropic.APIError as e:
            print("Error occurred: {}".format(e))
        except Exception as e:
            print("Unexpected error occurred: {}".format(e))
        if attempt < max_retries - 1:
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
    raise RuntimeError(f"LLM call failed after {max_retries} attempts")
if __name__ == "__main__":
    messages = [{"role": "user", "content": "In one sentence, what does a tool-calling agent loop do?"}]
    print(call_llm_with_retries(messages))
