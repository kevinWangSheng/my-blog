#!/usr/bin/env python3
"""Run the expense-agent k times per dataset task and emit runs JSONL.

This is the ONLY eval file that imports the agent. The grader never does
(see check_isolation.py C3). Output rows: {"id": <task_id>, "output": {...}}.

The agent is invoked once per trial with a fresh state so trials are
independent (no correlated failure across the k trials of one task).

Run:
    python evals/run_agent.py --dataset evals/dataset/extraction.jsonl \
        --k 5 --out runs/extraction.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Import path: repo root on sys.path so `src` is importable when run from CI.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from src.agent import run_expense_agent  # noqa: E402
except Exception as exc:  # pragma: no cover - surfaced clearly in CI
    print(
        f"cannot import src.agent.run_expense_agent: {exc}\n"
        "run_agent.py must be able to load the agent under test.",
        file=sys.stderr,
    )
    run_expense_agent = None  # type: ignore


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, type=Path)
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    if run_expense_agent is None:
        return 2

    tasks = load_jsonl(args.dataset)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        for task in tasks:
            for _ in range(args.k):
                # fresh invocation per trial — independent runs
                # NOTE: run_expense_agent is the agent business implementation.
                # src/agent.py contains only a placeholder (NotImplementedError).
                # Implement the agent in src/agent.py; this harness loop is complete.
                output = run_expense_agent(**task["input"])
                fh.write(
                    json.dumps({"id": task["id"], "output": output}, ensure_ascii=False)
                    + "\n"
                )
    print(f"wrote {args.out} ({len(tasks)} tasks x {args.k} trials)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
