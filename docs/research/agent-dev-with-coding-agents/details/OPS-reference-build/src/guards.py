"""CostGuard: hard runtime ceilings for the expense-agent loop.

Enforces four cumulative budgets and HARD-ABORTS the agent loop the moment any
one is crossed. This is code, not prompt text: the model cannot talk its way
past it. Wire CostGuard.check() into the top of every iteration of the
gather->act->verify runtime loop, and CostGuard.add_usage() after every
client.messages.create() call.

Budgets:
  - max_iterations         : count of agent-loop turns
  - total_tokens_budget    : cumulative input+output tokens across all LLM calls
  - wall_clock_timeout_sec : real seconds since the guard was started
  - cost_ceiling_usd       : cumulative USD derived from per-model token prices

On breach, check() raises GuardTripped, which the loop must NOT catch-and-retry.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

# Prices in USD per 1 token (input, output). Source: claude-api skill model
# table (cached 2026-06-04): Opus 4.8 $5/$25 per 1M, Sonnet 4.6 $3/$15 per 1M.
# Update when pricing changes.
_MODEL_PRICES_USD_PER_TOKEN: dict[str, tuple[float, float]] = {
    "claude-opus-4-8": (5.00 / 1_000_000, 25.00 / 1_000_000),
    "claude-sonnet-4-6": (3.00 / 1_000_000, 15.00 / 1_000_000),
}


class GuardTripped(Exception):
    """Raised when a cumulative budget is exceeded. Do not retry past this."""

    def __init__(self, limit_name: str, value: float, limit: float) -> None:
        self.limit_name = limit_name
        self.value = value
        self.limit = limit
        super().__init__(
            f"CostGuard tripped: {limit_name} = {value} exceeded limit {limit}"
        )


@dataclass
class CostGuard:
    """Accumulates spend and aborts the loop when any ceiling is crossed."""

    max_iterations: int = 12
    total_tokens_budget: int = 200_000
    wall_clock_timeout_sec: float = 300.0
    cost_ceiling_usd: float = 1.00

    iterations: int = field(default=0, init=False)
    total_tokens: int = field(default=0, init=False)
    total_cost_usd: float = field(default=0.0, init=False)
    _start_monotonic: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        self._start_monotonic = time.monotonic()

    def elapsed_sec(self) -> float:
        return time.monotonic() - self._start_monotonic

    def add_usage(self, model: str, input_tokens: int, output_tokens: int) -> None:
        """Record one LLM call's usage. Call after every messages.create().

        Pass response.usage.input_tokens and response.usage.output_tokens from
        the Anthropic SDK Message object.
        """
        self.total_tokens += int(input_tokens) + int(output_tokens)
        in_price, out_price = _MODEL_PRICES_USD_PER_TOKEN.get(model, (0.0, 0.0))
        self.total_cost_usd += input_tokens * in_price + output_tokens * out_price

    def begin_iteration(self) -> None:
        """Call once at the start of each agent-loop turn, then check()."""
        self.iterations += 1

    def check(self) -> None:
        """Raise GuardTripped if any cumulative budget is exceeded.

        Call at the top of every loop turn (after begin_iteration) AND after
        add_usage(), so a single expensive call can't overshoot unchecked.
        """
        if self.iterations > self.max_iterations:
            raise GuardTripped("max_iterations", self.iterations, self.max_iterations)
        if self.total_tokens > self.total_tokens_budget:
            raise GuardTripped(
                "total_tokens_budget", self.total_tokens, self.total_tokens_budget
            )
        elapsed = self.elapsed_sec()
        if elapsed > self.wall_clock_timeout_sec:
            raise GuardTripped(
                "wall_clock_timeout_sec", round(elapsed, 3), self.wall_clock_timeout_sec
            )
        if self.total_cost_usd > self.cost_ceiling_usd:
            raise GuardTripped(
                "cost_ceiling_usd", round(self.total_cost_usd, 6), self.cost_ceiling_usd
            )

    def snapshot(self) -> dict[str, float]:
        """Current accumulators, for logging / OTel span attributes."""
        return {
            "iterations": self.iterations,
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "elapsed_sec": round(self.elapsed_sec(), 3),
        }
