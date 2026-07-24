#!/usr/bin/env bash
# scripts/preflight.sh
# Startup verification checklist for an expense-agent dev session.
# Confirms: (1) working dir is the expense-agent repo root, (2) git worktree state,
# (3) progress/handoff file exists & is fresh, (4) external tool deps are healthy.
# Prints a PASS/FAIL line per check and exits non-zero if any hard check fails.
#
# Two-tier result: HARNESS_READY (all structure/env checks pass) vs BUSINESS_IMPL
# (agent.py placeholder vs implemented). Business-pending WARNs but does NOT fail:
# harness is usable for coding-agent dev even before agent.py is written.
#
# Usage:
#   scripts/preflight.sh
#   ANTHROPIC_API_KEY=... scripts/preflight.sh   # enables the API-key check
set -uo pipefail

FAIL=0
HARNESS_WARN=0   # soft warnings; exit 0 unless FAIL=1

pass() { printf '  PASS  %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1"; FAIL=1; }
warn() { printf '  WARN  %s\n' "$1"; HARNESS_WARN=1; }

echo "== expense-agent preflight =="

# --- Check 1: working directory is the repo root we expect ---
if REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  if [ "$(basename "$REPO_ROOT")" = "expense-agent" ] \
     && [ -f "$REPO_ROOT/src/agent.py" ] \
     && [ -d "$REPO_ROOT/src/tools" ] \
     && [ -d "$REPO_ROOT/evals" ]; then
    pass "repo root: $REPO_ROOT (src/agent.py, src/tools/, evals/ present)"
    cd "$REPO_ROOT"
  else
    fail "repo layout mismatch at $REPO_ROOT — expected expense-agent/{src/agent.py,src/tools,evals}"
  fi
else
  fail "not inside a git repository (run from expense-agent/ checkout)"
fi

# --- Check 2: git worktree / tree state ---
if git rev-parse --git-dir >/dev/null 2>&1; then
  BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
  DIRTY_COUNT="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  pass "git ok: branch=$BRANCH dirty_files=$DIRTY_COUNT"
  if [ "$DIRTY_COUNT" != "0" ]; then
    warn "uncommitted changes present — confirm they are yours before destructive ops"
    git status --short 2>/dev/null | sed 's/^/        /'
  fi
  WT_COUNT="$(git worktree list 2>/dev/null | wc -l | tr -d ' ')"
  pass "active worktrees: $WT_COUNT (main + any .claude/worktrees/*)"
else
  fail "git metadata unreadable"
fi

# --- Check 3: progress / handoff file present and fresh (<24h) ---
PROGRESS_FILE="${PROGRESS_FILE:-PROGRESS.md}"
if [ -f "$PROGRESS_FILE" ]; then
  # Cross-platform mtime: try GNU stat, fall back to BSD/macOS stat.
  MTIME="$(stat -c %Y "$PROGRESS_FILE" 2>/dev/null || stat -f %m "$PROGRESS_FILE" 2>/dev/null || echo 0)"
  NOW="$(date +%s)"
  AGE_H=$(( (NOW - MTIME) / 3600 ))
  if [ "$AGE_H" -le 24 ]; then
    pass "progress file $PROGRESS_FILE present (updated ${AGE_H}h ago)"
  else
    warn "progress file $PROGRESS_FILE is stale (${AGE_H}h old) — re-read before continuing"
  fi
else
  warn "no $PROGRESS_FILE — first session, or set PROGRESS_FILE=path"
fi

# --- Check 4: external tool / dependency health ---
# 4a. python + venv
if command -v python3 >/dev/null 2>&1; then
  pass "python3: $(python3 --version 2>&1)"
else
  fail "python3 not found"
fi

# 4b. harness SDK importable (anthropic package — needed for agent.py to call Claude).
#     This is a HARNESS check: import fails means harness infra is not installed.
#     It is NOT a business-logic check; we do not run agent.py here.
if python3 -c "import anthropic" 2>/dev/null; then
  pass "harness: anthropic SDK importable"
else
  fail "harness: 'anthropic' not importable — run: pip install anthropic  (or: uv sync)"
fi

# 4c. Determine whether agent.py is a business placeholder or implemented.
#     A placeholder has the literal string "PLACEHOLDER" or an empty function body
#     (just `pass` / `...` after the def line). We WARN, not FAIL: harness tooling
#     works for coding-agent development even when the business body is pending.
AGENT_PY="${REPO_ROOT:-$PWD}/src/agent.py"
if [ -f "$AGENT_PY" ]; then
  if grep -qE '^\s*(pass|\.\.\..)\s*$|PLACEHOLDER' "$AGENT_PY" 2>/dev/null; then
    warn "BUSINESS_IMPL_PENDING: src/agent.py appears to be a placeholder — harness is ready, business body not yet written"
  else
    pass "BUSINESS_IMPL: src/agent.py has non-placeholder content"
  fi
else
  warn "src/agent.py missing — harness structure ok, business entry point not yet created"
fi

# 4d. ledger.db is reachable and writable (post_ledger_entry target).
LEDGER="${LEDGER_DB:-ledger.db}"
if [ -e "$LEDGER" ]; then
  if [ -w "$LEDGER" ]; then
    pass "ledger.db present and writable ($LEDGER)"
  else
    fail "ledger.db exists but is NOT writable ($LEDGER)"
  fi
else
  warn "ledger.db missing ($LEDGER) — will be created on first post_ledger_entry"
fi

# 4e. Anthropic API key for claude-opus-4-8 / claude-sonnet-4-6 calls.
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  pass "ANTHROPIC_API_KEY is set (len=${#ANTHROPIC_API_KEY})"
else
  warn "ANTHROPIC_API_KEY not set — agent.py LLM calls will fail"
fi

# 4f. External OCR + FX endpoints reachable (config-driven; skipped if unset).
# NOTE on the curl probe: on connection failure curl prints '000' to stdout AND
# exits non-zero (e.g. 7 for connrefused). We must NOT use a `|| echo 000` fallback:
# that appends a SECOND '000' (yielding CODE=000000) which would defeat the
# `CODE = 000` guard and FALSELY report an unreachable endpoint as healthy.
# Instead capture curl's exit status and gate on (RC != 0 OR CODE == 000).
for pair in "OCR_API_URL:ocr_extract" "FX_API_URL:fx_rate"; do
  VAR="${pair%%:*}"; TOOL="${pair##*:}"
  URL="$(eval "printf '%s' \"\${$VAR:-}\"")"
  if [ -z "$URL" ]; then
    warn "$VAR unset — $TOOL health probe skipped"
  elif command -v curl >/dev/null 2>&1; then
    CODE="$(curl -s -o /dev/null -m 5 -w '%{http_code}' "$URL" 2>/dev/null)"; RC=$?
    if [ "$RC" != "0" ] || [ "$CODE" = "000" ]; then
      fail "$TOOL endpoint unreachable ($VAR=$URL; curl_rc=$RC http=$CODE)"
    else
      pass "$TOOL endpoint reachable ($VAR -> HTTP $CODE)"
    fi
  else
    warn "curl missing — cannot probe $TOOL"
  fi
done

echo "== preflight done =="
if [ "$FAIL" != "0" ]; then
  echo "RESULT: FAIL (one or more hard checks failed — harness not ready)"
  exit 1
fi
if [ "$HARNESS_WARN" != "0" ]; then
  echo "RESULT: HARNESS_READY (with warnings — review WARNs above; BUSINESS_IMPL may be pending)"
  exit 0
fi
echo "RESULT: PASS"
exit 0
