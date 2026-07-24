"""test_fx_rate.py — interface contract placeholder (business tests removed).

WHY THIS FILE IS A PLACEHOLDER
================================
The original test file asserted FX cache internals:
  fx.FxResult / fx._cache_put / fx._init_cache / fx.CACHE_TTL_SECONDS
  + web_search freshening path

These 5 symbols belong to the *business implementation* of fx_rate
(cache strategy, TTL policy, web_search integration) — not the harness.
src/tools/fx_rate.py was correctly made an interface-contract placeholder
(signature + docstring + NotImplementedError); those symbols no longer
exist there.  Keeping the original tests would:

  1. cause pytest collection to fail with AttributeError (confirmed via
     `module 'src.tools.fx_rate' has no attribute '_init_cache'`), which
     breaks the Stop-hook pytest gate for every dev session; and
  2. leak the business cache/web_search implementation decision into the
     harness layer.

WHAT GOES HERE WHEN YOU IMPLEMENT fx_rate
==========================================
Wire your FX data source in src/tools/fx_rate.py, then replace the body
of this file with real tests.  The tests should verify the *interface
contract* defined in fx_rate's docstring:

  def test_returns_rate_field():
      # fx_rate(currency, date) must return an object with a .rate float
      ...

  def test_fresh_data_per_invoice_date():
      # each call for a different date must produce an independent result
      # (no stale rate bleed-across)
      ...

  def test_does_not_return_stale_cached_value():
      # if caching is implemented: verify TTL + fetched_at discipline
      ...

Tests that assert internal symbols (_init_cache, _cache_put, FxResult,
CACHE_TTL_SECONDS) belong here ONLY after those symbols are defined in
src/tools/fx_rate.py by the implementer.
"""

import pytest


def test_fx_rate_placeholder_skip() -> None:
    """Placeholder: no business implementation to test yet.

    Remove this test and add real tests once src/tools/fx_rate.py is
    implemented.  See module docstring for the contract to verify.
    """
    pytest.skip(
        "fx_rate business implementation not present; "
        "add real tests after wiring src/tools/fx_rate.py"
    )
