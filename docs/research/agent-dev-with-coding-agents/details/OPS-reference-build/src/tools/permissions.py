"""Runtime permission gate for the expense-agent's OWN tools.

This is the enforcement point referenced by .codex/config.toml's cross-reference
note. Claude Code / Codex permissions gate the *developer harness*; this module
gates the *agent's three tools at runtime*. They must agree that
post_ledger_entry is human-gated.

Policy (code, not prompt):
  ocr_extract        -> allow  (read-only external read; no local side effect)
  fx_rate            -> allow  (read-only external read)
  post_ledger_entry  -> ask    (writes ledger.db; irreversible) -> default DENY

"ask" means: call the injected approver callback; if it returns False (or no
approver is wired), the call is DENIED. Default-deny is the safe failure mode.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

# Per-tool policy. Mirrors the .claude/.codex stance.
_TOOL_POLICY: dict[str, str] = {
    "ocr_extract": "allow",
    "fx_rate": "allow",
    "post_ledger_entry": "ask",
}


class PermissionDenied(Exception):
    """Raised when a gated tool call is not approved."""


# Approver: given (tool_name, tool_input) -> True to allow. Default rejects,
# so an unwired approver means post_ledger_entry can never fire unattended.
ApproverFn = Callable[[str, dict[str, Any]], bool]


def _default_approver(tool_name: str, tool_input: dict[str, Any]) -> bool:
    return False  # default-deny: no human wired => no ledger write


def check_tool_permission(
    tool_name: str,
    tool_input: dict[str, Any],
    approver: ApproverFn | None = None,
) -> None:
    """Raise PermissionDenied unless the tool is allowed or approved.

    Unknown tools default to "ask" (deny-by-default).
    """
    policy = _TOOL_POLICY.get(tool_name, "ask")
    if policy == "allow":
        return
    if policy == "deny":
        raise PermissionDenied(f"{tool_name} is denied by policy")
    # policy == "ask"
    approve = approver or _default_approver
    if not approve(tool_name, tool_input):
        raise PermissionDenied(
            f"{tool_name} requires human approval and was not approved"
        )
