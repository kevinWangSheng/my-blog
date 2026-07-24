"""Handler for the expense_post_ledger_entry tool — interface contract (placeholder).

Shape: DANGEROUS / SIDE-EFFECTFUL / IRREVERSIBLE by the agent.
  - Writes one finalized accounting entry to the local ledger.db.
  - This mutation cannot be undone by the agent.
  - Default-deny: must not write unless explicitly approved.

Two deployment routes — human-approval gate location differs by route:

  Route A — tools exposed via MCP server (mcp_server/server.py):
      Gate lives in .claude/settings.json under "ask":
      ["mcp__expense__expense_post_ledger_entry"]. The settings.json permission
      check fires before this handler runs on the MCP route.

  Route B — SDK direct (client.messages.create(tools=ALL_TOOLS) + manual loop):
      .claude/settings.json does NOT participate in SDK runtime calls. The gate
      must be built into the agentic loop BEFORE dispatching to this handler.
      Pass approved=True only after human confirmation.

In-process defense (general safety convention, not business logic):
  Regardless of route, this handler should refuse to commit when needs_human
  is True unless the caller passes approved=True. This is a second line of
  defense for the case where the outer gate is misconfigured.

Business implementation: connect your SQLite (or other) write path here.
The harness does not prescribe the DB schema, migration strategy, or ORM.
"""

from __future__ import annotations


def post_ledger_entry(entry: dict, approved: bool = False) -> dict:
    """Insert one finalized expense entry into ledger.db.

    When to call (mirrors inputSchema description): only after all fields are
    extracted, the base-currency amount is computed, and (if needs_human is
    true) a human has approved.

    Args:
        entry:    Dict matching the expense_post_ledger_entry inputSchema:
                  {vendor, date, amount, currency, amount_base, category,
                   needs_human}. All fields required; see schemas.py.
        approved: Must be True when entry['needs_human'] is True. Callers on
                  Route B must set this after obtaining human confirmation.

    Returns:
        Dict with at minimum {"posted": bool}. On success include the
        newly created record id. On refusal include a "reason" string.

    Raises:
        NotImplementedError: Until a real write-path is wired in.
    """
    raise NotImplementedError(
        "接入你的业务逻辑; harness 不规定 DB schema、迁移策略或写库实现。"
        " 实现应: 1) 当 entry['needs_human'] and not approved 时拒绝(返回 posted=False), "
        "2) 校验必填字段和类型, "
        "3) 执行写库操作, "
        "4) 返回 {'posted': True, 'id': <row_id>} 或 {'posted': False, 'reason': str}。"
    )
