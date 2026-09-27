import random
import time
import threading


import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-haiku-4-5"
MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_TOKENS = 1024
from langsmith.wrappers import wrap_anthropic

client = anthropic.Anthropic()
try:
    wrap_anthropic(client)
except AttributeError:
    # langsmith's wrap_anthropic still tries to patch the legacy
    # `completions` API, which anthropic>=1.0 removed. It patches
    # `messages.create` (the one we actually use) before hitting that,
    # so the client is already traced by the time this fires.
    pass

class TokenBucketLimiter:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate          # tokens added per second
        self.capacity = capacity  # max burst size
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now

            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                time.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1


_rate_limiter = TokenBucketLimiter(rate=0.5, capacity=3)

def call_llm_with_retries(
    messages: list[dict],
    tools: list[dict] = [],
    model: str = MODEL,
    max_retries: int = MAX_RETRIES,
    base_delay: float = BASE_DELAY,
    max_tokens: int = MAX_TOKENS,
) -> anthropic.types.Message:

    _rate_limiter.acquire()
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


