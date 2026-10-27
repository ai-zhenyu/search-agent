"""Per-run budget: counts tokens, searches, and fetches, and enforces the hard limits in config.py."""

from dataclasses import dataclass

import config


class BudgetExceeded(Exception):
    """Raised when a run hits one of the hard limits."""


@dataclass
class Budget:
    model: str = config.LLM_MODEL
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    llm_calls: int = 0
    searches: int = 0
    pages_fetched: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def check_tokens(self) -> None:
        if self.total_tokens >= config.MAX_TOKENS_PER_RUN:
            raise BudgetExceeded(f"token limit reached ({self.total_tokens} >= {config.MAX_TOKENS_PER_RUN})")

    def add_llm_usage(self, input_tokens: int, cached_input_tokens: int, output_tokens: int) -> None:
        self.llm_calls += 1
        self.input_tokens += input_tokens
        self.cached_input_tokens += cached_input_tokens
        self.output_tokens += output_tokens

    def add_search(self) -> None:
        self.searches += 1

    def add_fetch(self) -> None:
        if self.pages_fetched >= config.MAX_PAGES_FETCHED:
            raise BudgetExceeded(f"page limit reached ({config.MAX_PAGES_FETCHED})")
        self.pages_fetched += 1

    def cost_usd(self) -> float:
        """Approximate cost of the run so far (LLM tokens + Serper queries)."""
        prices = config.PRICES_PER_M_TOKENS.get(self.model)
        llm_cost = 0.0
        if prices:
            uncached = self.input_tokens - self.cached_input_tokens
            llm_cost = (
                uncached * prices["input"]
                + self.cached_input_tokens * prices["cached_input"]
                + self.output_tokens * prices["output"]
            ) / 1_000_000
        return llm_cost + self.searches * config.SERPER_COST_PER_QUERY

    def summary(self) -> str:
        return (
            f"~${self.cost_usd():.5f} "
            f"({self.input_tokens:,} in / {self.output_tokens:,} out tokens, "
            f"{self.llm_calls} LLM calls, {self.searches} searches, {self.pages_fetched} pages)"
        )

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "input_tokens": self.input_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "output_tokens": self.output_tokens,
            "llm_calls": self.llm_calls,
            "searches": self.searches,
            "pages_fetched": self.pages_fetched,
            "cost_usd": round(self.cost_usd(), 6),
        }
