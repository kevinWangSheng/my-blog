#!/usr/bin/env bash
# PreToolUse guard for expense-agent.
# Blocks edits/writes to protected paths (ledger.db, .env, .git/) and
# blocks Bash commands that reference them or do destructive ops on them.
#
# Block mechanism: print JSON permissionDecision:deny on stdout AND exit 2.
#   - exit 2 is the authoritative PreToolUse block: it stops the tool call and
#     feeds stderr back to Claude. Per the Claude Code hooks docs, on a
#     PreToolUse exit code of 2 the hook's STDOUT JSON may be IGNORED (exit 2
#     takes precedence). The JSON deny block is the documented non-exit-2 path
#     (used when a hook exits 0 and wants to deny via JSON). We emit BOTH as
#     belt-and-suspenders, but the actual block here comes from exit 2; the JSON
#     is informational and may or may not be parsed when exit==2.
# exit 0 = no decision, normal permission flow applies (do NOT block).
set -euo pipefail

INPUT="$(cat)"

tool_name="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')"
# Edit/Write/MultiEdit/NotebookEdit carry a file_path; Bash carries a command.
file_path="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')"
notebook_path="$(printf '%s' "$INPUT" | jq -r '.tool_input.notebook_path // empty')"
command="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"

# Protected path fragments. ledger.db is the agent's local ledger (post_ledger_entry
# writes here); .env holds the Claude API key; .git is repo history.
#
# Two DIFFERENT regexes on purpose:
#  - PATH_PROTECTED_REGEX matches a bare path value (file_path/notebook_path),
#    so it anchors on (^|/): the value IS the path.
#  - BASH_PROTECTED_REGEX matches inside a shell command string, where the
#    protected name is almost always preceded by a space / redirect / quote /
#    '/' and followed by a space / redirect / end / dot / dash. A (^|/) anchor
#    is WRONG here (it misses 'sqlite3 ledger.db', 'cat .env', '>> ledger.db'),
#    so we use boundary character classes instead.
PATH_PROTECTED_REGEX='(^|/)ledger\.db($|-journal|-wal|-shm)|(^|/)\.env($|\.)|(^|/)\.git(/|$)'
BASH_PROTECTED_REGEX='(^|[[:space:]/=>|])(ledger\.db|\.env|\.git)([[:space:]/=>|.-]|$)'

deny() {
  local reason="$1"
  # NOTE: on exit 2 this stdout JSON may be ignored by Claude Code (exit 2
  # wins). It is emitted for the non-exit-2 deny path and for human/debug logs.
  jq -n --arg r "$reason" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $r
    }
  }'
  echo "BLOCKED by pre_tool_use_guard: $reason" >&2
  exit 2
}

# 1) File-targeting tools (Edit/Write/MultiEdit/NotebookEdit).
for p in "$file_path" "$notebook_path"; do
  [ -z "$p" ] && continue
  if printf '%s' "$p" | grep -Eq "$PATH_PROTECTED_REGEX"; then
    deny "Refusing to modify protected file '$p' (ledger.db/.env/.git are off-limits to the agent; use post_ledger_entry tool for ledger writes)."
  fi
done

# 2) Bash commands that touch protected paths or do destructive ops on them.
if [ "$tool_name" = "Bash" ] && [ -n "$command" ]; then
  if printf '%s' "$command" | grep -Eq "$BASH_PROTECTED_REGEX"; then
    deny "Refusing Bash command that references a protected path (ledger.db/.env/.git): $command"
  fi
  if printf '%s' "$command" | grep -Eq 'rm[[:space:]]+(-[A-Za-z]*[rRfF][A-Za-z]*[[:space:]]+)+';
then
    deny "Refusing destructive 'rm -rf'-style Bash command: $command"
  fi
fi

# No protected path hit -> let normal permission flow decide.
exit 0
