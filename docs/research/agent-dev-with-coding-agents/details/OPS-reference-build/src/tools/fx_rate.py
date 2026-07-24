"""Handler for the expense_fx_rate tool — interface contract (placeholder).

Shape: read-external / fast-changing data / no-local-write.
  - Makes an outbound call to retrieve an exchange rate.
  - Returns a rate result (structure defined by implementer).
  - FX rates are fast-moving data: the result must NOT be used as a long-lived
    fact. Always fetch for the specific invoice date. If caching, attach a TTL
    and record the fetch timestamp.

Knowledge-freshness note (general convention, not business logic):
  FX rates change daily. Any cached value must carry a fetched_at timestamp and
  an explicit TTL. The amount_base field in ledger entries must always reflect
  "rate fetched for this invoice date", not a stale remembered rate.

Business implementation: connect your FX data source here (e.g. Open Exchange
Rates, ECB, xe.com, or a web_search-backed freshening path). The harness does
not prescribe the provider, caching strategy, or web_search integration.
"""

from __future__ import annotations


def fx_rate(currency: str, date: str, base: str = "USD", client=None):
    """Return the exchange rate for 1 unit of `currency` into `base` on `date`.

    When to call (mirrors inputSchema description): call only after the invoice
    currency and date are known from extraction. FX is fast-moving data: always
    fetch for the invoice date, never reuse a remembered rate.

    Args:
        currency: ISO 4217 source currency code to convert FROM (e.g. 'EUR',
                  'JPY', 'USD'). Exactly 3 uppercase letters.
        date:     Invoice date the rate is quoted for, as ISO-8601 'YYYY-MM-DD'.
                  Use the date extracted from the document, not today's date.
        base:     Base (target) currency code. Default 'USD' aligns with
                  amount_base in the ledger schema.
        client:   Optional API client for the FX data source; injected for
                  testability.

    Returns:
        Implementation-defined rate result. At minimum it must expose a `rate`
        field (float) representing 1 unit of `currency` in `base`.

    Raises:
        NotImplementedError: Until a real FX data source is wired in.
    """
    raise NotImplementedError(
        "接入你的业务逻辑; harness 不规定 FX 数据源、缓存策略或 web_search 集成。"
        " 实现应: 1) 按 currency+date+base 查询汇率, "
        "2) 若缓存则带 TTL 和 fetched_at, "
        "3) 返回含 rate(float) 的结果对象。"
    )
