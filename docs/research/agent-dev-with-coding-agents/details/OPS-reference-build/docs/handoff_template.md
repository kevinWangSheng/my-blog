# Handoff prompt template (delegating a scoped task to a subagent)
#
# Fill every <...> before sending. This is the message you give Claude when you say
# "use the <subagent> to ...". A non-fork subagent starts with FRESH context: it does
# NOT see your conversation, the files you already read, or prior tool results. So the
# handoff must be self-contained. (Source: code.claude.ai/docs/en/sub-agents,
# "What loads at startup".)
#
# ---------------------------------------------------------------------------
# UPSTREAM SUMMARY  (what the delegating session already established)
# ---------------------------------------------------------------------------
UPSTREAM_SUMMARY:
- Current commit SHA: <e.g. git rev-parse --short HEAD output, e.g. "a3f1b9c">
- Work done so far: <one paragraph: what was implemented/reviewed and the evidence
  that it passed, e.g. "Added fx_rate TTL guard; evals.run pass^k=5/5 on cls suite">
- Decisions carried forward: <constraints the subagent MUST respect, e.g.
  "ADR-0001: single agent + tools only; ADR-0002: post_ledger_entry always ask/deny">
- Open questions left for subagent: <what the subagent still needs to resolve, e.g.
  "Does the staleness guard fire correctly when TTL is exactly 0s?">

# ---------------------------------------------------------------------------
# TASK
# ---------------------------------------------------------------------------
TASK: <one sentence: exactly what to produce, e.g. "review the diff in src/tools/fx_rate.py
for tool-contract drift and fx freshness">

REPO CONTEXT (restate; the subagent cannot see your session):
- Repo: expense-agent/ (single agent + tools, Python, calls Claude API).
- Relevant files: <e.g. src/tools/fx_rate.py, src/agent.py call site lines 40-70>.
- Fixed tool contracts (MUST NOT change): ocr_extract(file_path), fx_rate(currency, date),
  post_ledger_entry(entry) -> writes ledger.db.
- Agent output contract: {vendor, date, amount, currency, amount_base, category,
  confidence, needs_human}.

# ---------------------------------------------------------------------------
# TESTABLE SUCCESS DEFINITION (the subagent is done only when ALL are true)
# ---------------------------------------------------------------------------
SUCCESS:
1. <objective check 1, e.g. "every finding cites file path + line">
2. <objective check 2, e.g. "confirms fx_rate still takes (currency, date) and passes date through">
3. <objective check 3, e.g. "no hardcoded rate; flags any cached/stale value">
   These must be verifiable from the returned report alone, with no follow-up questions.

# ---------------------------------------------------------------------------
# ISOLATION BOUNDARY (what the subagent may and may NOT touch)
# ---------------------------------------------------------------------------
ISOLATION:
- Allowed tools: <e.g. Read, Grep, Glob only — read-only review>.
- Do NOT edit, write, or run any file. Do NOT call post_ledger_entry. Do NOT touch ledger.db.
- Stay within: <paths, e.g. src/tools/ and src/agent.py>. Ignore: <e.g. evals/fixtures/, vendor/>.
- Do NOT rename or change the signature of any of the three fixed tools.
- If the task needs writes, STOP and report that instead of writing.

# ---------------------------------------------------------------------------
# OUTPUT FORMAT (return EXACTLY this JSON, nothing else)
# ---------------------------------------------------------------------------
# NOTE: This OUTPUT_JSON schema applies to general-purpose subagents delegated via
# this template. The built-in `reviewer` subagent (.claude/agents/reviewer.md) is
# EXEMPT: it uses its own prose contract (Critical/Warnings/Suggestions sections),
# because it is invoked proactively by Claude Code's sub-agent mechanism, not via
# a handoff prompt. Do NOT pass OUTPUT_JSON instructions to the reviewer subagent;
# its prose output is the correct and expected format for that agent.
OUTPUT_JSON:
{
  "status": "pass" | "fail",
  "findings": [
    {"severity": "critical" | "warning" | "suggestion",
     "file": "<path>", "line": <int|null>,
     "issue": "<what is wrong>", "fix": "<suggested fix as text, do not apply>"}
  ],
  "summary": "<one line>",
  "checkpoint": {
    "commit_sha": "<the SHA from UPSTREAM_SUMMARY, or HEAD if you can read it>",
    "reviewed_paths": ["<list of files actually read>"],
    "next_step": "<what the delegating session should do with these findings>"
  }
}
# status = "fail" if any critical finding exists, else "pass". Empty findings -> [].

# ---------------------------------------------------------------------------
# ERROR HANDLING (do not silently swallow problems)
# ---------------------------------------------------------------------------
ERROR_HANDLING:
- If a named file/path does not exist: return status="fail" with a finding that says so;
  do not guess at file contents.
- If the task is ambiguous or needs a write to complete: return status="fail", summary
  explaining the blocker; do not improvise outside ISOLATION.
- If you hit the turn limit before finishing: return partial findings with
  summary="INCOMPLETE: hit maxTurns, reviewed <X of Y>".
- Never emit prose outside the OUTPUT_JSON object.

# ---------------------------------------------------------------------------
# ROLLBACK PATH (if the subagent's output is rejected)
# ---------------------------------------------------------------------------
ROLLBACK:
- Safe revert point: commit <SHA from UPSTREAM_SUMMARY> — run `git checkout <SHA> -- <paths>`
  to restore the files this task touches if the findings or changes are discarded.
- No DB state to roll back for read-only reviewer tasks. For tasks that touched ledger.db,
  state the last-known ledger row id before the task started so the delegating session
  can delete rows > that id if needed.

# ---------------------------------------------------------------------------
# TURN BUDGET
# ---------------------------------------------------------------------------
MAX_TURNS: <e.g. 12>   # also enforce structurally via maxTurns in the subagent frontmatter;
                       # this line tells the subagent to wrap up and return partial JSON
                       # rather than die uninformatively when the budget is near.
