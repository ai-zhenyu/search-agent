"""The ONLY place that talks to an LLM.

Every agent calls `call_llm()`. To switch to a local Ollama model later, only this file
(and config.py) need to change. We use the Chat Completions format because Ollama
also serves an OpenAI-compatible Chat Completions endpoint.
"""

from dataclasses import dataclass, field

from openai import OpenAI

import config
from core.budget import Budget

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=config.get_key("OPENAI_API_KEY"))
    return _client


@dataclass
class LLMResponse:
    content: str | None                              # the model's text (None if it only called tools)
    tool_calls: list = field(default_factory=list)   # tool calls the model asked us to run
    message: dict = field(default_factory=dict)      # assistant message to append to the history


def call_llm(messages: list[dict], budget: Budget, tools: list[dict] | None = None) -> LLMResponse:
    """Send a conversation to the LLM, record token usage in `budget`, and return the reply."""
    budget.check_tokens()

    kwargs = {
        "model": config.LLM_MODEL,
        "messages": messages,
        "max_completion_tokens": config.MAX_OUTPUT_TOKENS_PER_CALL,
    }
    if config.LLM_REASONING_EFFORT:
        kwargs["reasoning_effort"] = config.LLM_REASONING_EFFORT
    if tools:
        kwargs["tools"] = tools

    response = _get_client().chat.completions.create(**kwargs)

    usage = response.usage
    details = usage.prompt_tokens_details
    cached = (details.cached_tokens or 0) if details else 0
    budget.add_llm_usage(usage.prompt_tokens, cached, usage.completion_tokens)

    msg = response.choices[0].message
    return LLMResponse(
        content=msg.content,
        tool_calls=msg.tool_calls or [],
        message=msg.model_dump(exclude_none=True),
    )


if __name__ == "__main__":
    # Stage 1 demo: one real call, then print the reply and the cost.
    b = Budget()
    reply = call_llm(
        [
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "In one sentence: what is an AI agent?"},
        ],
        budget=b,
    )
    print("Reply:", reply.content)
    print("Cost: ", b.summary())
