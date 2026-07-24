#!/usr/bin/env bash
# Stop hook for expense-agent: run pytest before letting Claude end the turn.
# If tests fail: print JSON decision:block (with reason) AND exit 2.
#   - Stop exit 2 prevents Claude from stopping and feeds stderr back.
#   - decision:block + reason is the documented JSON path to the same effect.
# If tests pass: exit 0 (Claude is allowed to stop).
# Loop-guard: stop_hook_active in the input is true when we are already inside
# a Stop-hook-triggered continuation; bail out to avoid an infinite test loop.
set -uo pipefail

INPUT="$(cat)"

stop_active="$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false')"
if [ "$stop_active" = "true" ]; then
  exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" || exit 0

# No test suite -> nothing to gate on.
if [ ! -d "evals" ] && [ ! -d "tests" ]; then
  exit 0
fi
if ! command -v pytest >/dev/null 2>&1; then
  exit 0
fi

OUT="$(pytest -q 2>&1)"
code=$?

if [ "$code" -ne 0 ]; then
  reason="pytest failed (exit $code); do not stop until tests pass. Tail:
$(printf '%s' "$OUT" | tail -n 30)"
  jq -n --arg r "$reason" '{decision: "block", reason: $r}'
  printf '%s\n' "$reason" >&2
  exit 2
fi

exit 0
