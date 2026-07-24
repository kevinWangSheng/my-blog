#!/usr/bin/env bash
# PostToolUse formatter+linter for expense-agent.
# Fires after Edit/Write/MultiEdit. Formats the just-edited Python file with
# black and lints with ruff. Runs prettier for JSON/YAML/MD.
# PostToolUse CANNOT block the tool (it already ran); exit 2 only surfaces
# stderr to Claude. We use exit 2 on lint failure so Claude sees and fixes it;
# formatting (black/prettier) auto-fixes in place, so it stays exit 0.
set -uo pipefail

INPUT="$(cat)"
file_path="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')"

# Nothing to format if no concrete file path (e.g. Bash edits).
[ -z "$file_path" ] && exit 0
[ -f "$file_path" ] || exit 0

ext="${file_path##*.}"
status=0

case "$ext" in
  py)
    if command -v black >/dev/null 2>&1; then
      black --quiet "$file_path" || true
    fi
    if command -v ruff >/dev/null 2>&1; then
      # ruff check is the lint gate; --fix auto-applies safe fixes, remaining
      # issues are real and reported back to Claude via stderr + exit 2.
      if ! ruff check --fix "$file_path" >/tmp/ruff_out.$$ 2>&1; then
        echo "ruff lint failed for $file_path:" >&2
        cat /tmp/ruff_out.$$ >&2
        status=2
      fi
      rm -f /tmp/ruff_out.$$
    fi
    ;;
  json|yaml|yml|md|markdown)
    if command -v prettier >/dev/null 2>&1; then
      prettier --write "$file_path" >/dev/null 2>&1 || true
    fi
    ;;
  *)
    exit 0
    ;;
esac

exit "$status"
