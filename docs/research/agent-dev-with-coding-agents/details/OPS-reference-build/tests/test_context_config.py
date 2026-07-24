"""test_context_config.py — interface contract placeholder (business tests removed).

WHY THIS FILE IS A PLACEHOLDER
================================
The original test file asserted expense-agent runtime context management
functions from src/context_config.py:
  cc.build_jit_reference / cc.clear_stale_tool_results / cc.should_compact
  cc.Message / cc.KEEP_RECENT_MESSAGES / cc.CONTEXT_WINDOW_TOKENS
  cc.context_health / cc.estimate_tokens

src/context_config.py contains business runtime logic (JIT reference
building, tool-result clearing thresholds, compaction trigger ratios,
compaction prompt text) that belongs to the *expense-agent implementation*,
not the harness.  Per the c2 boundary rule:

  "business runtime logic → placeholder; harness mechanisms → produce full"

src/context_config.py should itself become an interface-contract placeholder
when the context/eval category is addressed.  Until then, keeping these tests
creates a co-dependency: if context_config is later correctly occupied, these
tests would fail at collection with ImportError/AttributeError against the
now-absent symbols, breaking the Stop-hook pytest gate.

Removing the business tests here eliminates that future break and makes the
harness boundary explicit: context management policy (which tokens to clear,
when to compact, what the compaction prompt says) is the implementer's choice.

WHAT GOES HERE WHEN YOU IMPLEMENT context_config
=================================================
Wire your context management logic in src/context_config.py, then replace
the body of this file with real tests.  The tests should verify the
*interface contract*:

  def test_should_compact_returns_bool():
      # should_compact(used_tokens) -> bool
      ...

  def test_clear_stale_tool_results_scopes_to_non_recent():
      # recent messages (within keep_recent window) must not be cleared
      ...

  def test_build_jit_reference_is_lightweight():
      # JIT reference must not embed full document content
      ...

Tests that assert specific threshold values (KEEP_RECENT_MESSAGES == 6,
COMPACT_TRIGGER_RATIO == 0.75, etc.) belong here ONLY after those constants
are defined by the implementer in src/context_config.py.
"""

import pytest


def test_context_config_placeholder_skip() -> None:
    """Placeholder: no business implementation to test yet.

    Remove this test and add real tests once src/context_config.py is
    implemented.  See module docstring for the contract to verify.
    """
    pytest.skip(
        "context_config business implementation not present; "
        "add real tests after wiring src/context_config.py"
    )
