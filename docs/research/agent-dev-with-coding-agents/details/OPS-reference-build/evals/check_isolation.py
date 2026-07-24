#!/usr/bin/env python3
"""Evaluator-isolation gate (day-0, non-negotiable per Berkeley RDI 2026-04).

Statically + structurally verifies that the expense-agent eval cannot be
reward-hacked through the three classic holes:

  C1  dataset + grader are READ-ONLY to the process that runs the agent
      (no ground truth can be mutated, no grader can be patched).
  C2  the agent under test has ZERO write capability over evals/ — enforced
      in the harness permission layer (.claude/settings.json deny list),
      not in a prompt.
  C3  the judge is NOT the agent — the grader is pure code (no import of
      src.agent, no Claude/LLM call), and the model that judges is declared
      distinct from the model the agent uses.

This does NOT run the agent or the model. It is a config/static gate meant
for CI and local pre-flight. Exit 0 = all checks pass; non-zero = a hole.

Run:
    python evals/check_isolation.py
"""
from __future__ import annotations

import ast
import json
import os
import stat
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVALS = REPO / "evals"
DATASET_DIR = EVALS / "dataset"
GRADER = EVALS / "grader.py"
SETTINGS = REPO / ".claude" / "settings.json"

# Modules the GRADER must never import — importing the agent or an LLM client
# means the judge could be the agent (C3 violation).
FORBIDDEN_GRADER_IMPORTS = {
    "anthropic",
    "openai",
    "src.agent",
    "agent",
}

failures: list[str] = []
checks: list[str] = []


def ok(msg: str) -> None:
    checks.append(f"PASS  {msg}")


def fail(msg: str) -> None:
    failures.append(f"FAIL  {msg}")


# ---- C1: dataset + grader read-only ---------------------------------------

def check_readonly() -> None:
    targets = [GRADER]
    targets += sorted(DATASET_DIR.glob("*.jsonl"))
    if not (DATASET_DIR / "extraction.jsonl").exists():
        fail("dataset/extraction.jsonl missing")
    for p in targets:
        if not p.exists():
            fail(f"expected file missing: {p.relative_to(REPO)}")
            continue
        mode = p.stat().st_mode
        writable = mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
        if writable:
            fail(
                f"{p.relative_to(REPO)} is writable ({oct(stat.S_IMODE(mode))}); "
                f"dataset+grader must be read-only (chmod 0444)"
            )
        else:
            ok(f"{p.relative_to(REPO)} read-only ({oct(stat.S_IMODE(mode))})")


# ---- C2: agent has no write path into evals/ ------------------------------

def check_permission_denylist() -> None:
    if not SETTINGS.exists():
        fail(f"{SETTINGS.relative_to(REPO)} missing — agent write perms undeclared")
        return
    try:
        cfg = json.loads(SETTINGS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{SETTINGS.relative_to(REPO)} invalid JSON: {e}")
        return
    deny = cfg.get("permissions", {}).get("deny", [])
    needed = {"Edit(./evals/**)", "Write(./evals/**)"}
    missing = {r for r in needed if r not in deny}
    if missing:
        fail(
            "settings.json permissions.deny missing evals write guards: "
            + ", ".join(sorted(missing))
        )
    else:
        ok("settings.json denies Edit/Write on ./evals/** (agent cannot patch grader)")
    # the agent's own ledger writes must be ask/deny, never silently allowed
    allow = cfg.get("permissions", {}).get("allow", [])
    if any("post_ledger_entry" in str(r) for r in allow):
        # post_ledger_entry in allow is a side-effect-on-by-default smell
        fail("post_ledger_entry is in permissions.allow; must be ask/deny by default")
    else:
        ok("post_ledger_entry not auto-allowed (side-effects gated)")


# ---- C3: judge is pure code, distinct from agent --------------------------

def _imports(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name.split(".")[0])
                names.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            names.add(mod.split(".")[0])
            names.add(mod)
    return names


def check_grader_is_pure_code() -> None:
    if not GRADER.exists():
        fail("grader.py missing")
        return
    tree = ast.parse(GRADER.read_text(encoding="utf-8"))
    imps = _imports(tree)
    bad = imps & FORBIDDEN_GRADER_IMPORTS
    if bad:
        fail(
            f"grader.py imports {sorted(bad)} — a code-based grader must not "
            f"call the agent or an LLM (judge != agent)"
        )
    else:
        ok("grader.py imports no agent/LLM module (pure code-based judge)")


def check_judge_distinct_from_agent() -> None:
    """If an LLM-judge config exists, its model must differ from the agent's."""
    agent_model = os.environ.get("EXPENSE_AGENT_MODEL", "claude-opus-4-8")
    judge_cfg = EVALS / "judge.json"
    if not judge_cfg.exists():
        ok("no LLM-judge configured; grader is code-only (C3 satisfied by code path)")
        return
    try:
        jc = json.loads(judge_cfg.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"judge.json invalid JSON: {e}")
        return
    judge_model = jc.get("model")
    if judge_model and judge_model == agent_model:
        fail(
            f"judge model ({judge_model}) == agent model ({agent_model}); "
            f"judge must be a distinct model"
        )
    else:
        ok(f"judge model ({judge_model}) distinct from agent model ({agent_model})")


def main() -> int:
    check_readonly()
    check_permission_denylist()
    check_grader_is_pure_code()
    check_judge_distinct_from_agent()

    for line in checks:
        print(line)
    for line in failures:
        print(line, file=sys.stderr)

    if failures:
        print(f"\n{len(failures)} isolation check(s) FAILED", file=sys.stderr)
        return 1
    print(f"\nall {len(checks)} isolation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
