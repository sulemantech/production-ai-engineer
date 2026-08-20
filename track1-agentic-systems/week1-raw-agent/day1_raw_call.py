import random
import time

from llm_client import call_llm_with_retries

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-4-5"
MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_TOKENS = 1024

client = anthropic.Anthropic()


if __name__ == "__main__":
    messages = [{"role": "user", "content": "In one sentence, what does a tool-calling agent loop do?"}]
    response = call_llm_with_retries(messages, tools=[], model=MODEL, max_retries=MAX_RETRIES, base_delay=BASE_DELAY, max_tokens=MAX_TOKENS)
    print(response.content[0].text)
