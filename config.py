"""Central configuration: model choice, prices, and hard limits.

Everything you might want to tune lives here, so experiments only touch one file.
Run `python config.py` to check that your API keys are loaded (values are never printed).
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --- LLM ---------------------------------------------------------------------
LLM_PROVIDER = "openai"          # later: "ollama"
LLM_MODEL = "gpt-6-luna"
LLM_REASONING_EFFORT = "low"     # none | low | medium | high ...

# USD per 1M tokens (standard tier, checked 2026-10-26 on OpenAI's pricing page).
PRICES_PER_M_TOKENS = {
    "gpt-6-luna":   {"input": 0.10, "cached_input": 0.01,  "output": 0.50},
    "gpt-5.4-mini": {"input": 0.75, "cached_input": 0.075, "output": 4.50},
}
SERPER_COST_PER_QUERY = 0.001    # ~$1 / 1k queries after free credits

# --- Hard limits (per run) ---------------------------------------------------
MAX_ROUNDS = 2
MAX_QUERIES_PER_ROUND = 3
RESULTS_PER_QUERY = 8
MAX_PAGES_FETCHED = 5
MAX_CHARS_PER_PAGE = 6000
MAX_TOKENS_PER_RUN = 30_000
MAX_OUTPUT_TOKENS_PER_CALL = 2000
MAX_AGENT_STEPS = 6
FETCH_TIMEOUT_SECONDS = 15

# --- Paths -------------------------------------------------------------------
RUNS_DIR = "runs"


def get_key(name: str) -> str:
    """Return an API key from the environment, or fail with a clear message."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is missing. Add it to your .env file (see .env.example).")
    return value


if __name__ == "__main__":
    for key in ("OPENAI_API_KEY", "SERPER_API_KEY"):
        print(f"{key}: {'found' if os.getenv(key) else 'MISSING'}")
    print(f"Model: {LLM_MODEL} (reasoning effort: {LLM_REASONING_EFFORT})")
