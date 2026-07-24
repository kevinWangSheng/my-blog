#!/usr/bin/env python3
"""Code-based grader for expense-agent extraction/classification eval.

Judges RESULTS, not tool-call paths (Anthropic Demystifying-evals rule:
"grade the result, not the trajectory"). Field-level exact match for
strings/enums + numeric tolerance for amounts. Computes pass@k and pass^k
per Anthropic's definitions.

Run:
    python evals/grader.py --dataset evals/dataset/extraction.jsonl \
        --runs runs/extraction.jsonl --k 3

Exit code: 0 if pass^k_mean >= --gate (default 0.0 => report only);
non-zero if below the gate, so CI can fail on it.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


# ---- field-level comparison ------------------------------------------------

STRING_FIELDS = ("vendor", "currency", "date", "category")
# numeric tolerance: relative OR absolute, whichever is looser (handles
# rounding in amount_base after fx conversion).
NUMERIC_FIELDS = {
    "amount": {"abs": 0.01, "rel": 0.0},
    "amount_base": {"abs": 0.01, "rel": 0.005},  # fx rounding slack
}
BOOL_FIELDS = ("needs_human",)


def _norm_str(v: Any) -> str:
    return "" if v is None else str(v).strip().lower()


def _numeric_close(got: Any, want: Any, abs_tol: float, rel_tol: float) -> bool:
    if got is None or want is None:
        return got == want
    try:
        g, w = float(got), float(want)
    except (TypeError, ValueError):
        return False
    return math.isclose(g, w, abs_tol=abs_tol, rel_tol=rel_tol)


def grade_fields(output: dict, reference: dict) -> dict:
    """Return per-field pass map. Only fields present in reference are graded."""
    result: dict[str, bool] = {}
    for f in STRING_FIELDS:
        if f in reference:
            result[f] = _norm_str(output.get(f)) == _norm_str(reference[f])
    for f, tol in NUMERIC_FIELDS.items():
        if f in reference:
            result[f] = _numeric_close(
                output.get(f), reference[f], tol["abs"], tol["rel"]
            )
    for f in BOOL_FIELDS:
        if f in reference:
            result[f] = bool(output.get(f)) == bool(reference[f])
    return result


def is_trial_pass(output: dict, reference: dict) -> bool:
    """A trial passes iff every graded field passes (exact result match)."""
    fields = grade_fields(output, reference)
    return bool(fields) and all(fields.values())


# ---- pass@k / pass^k -------------------------------------------------------

def pass_at_k(trial_passes: list[bool]) -> float:
    """pass@k: at least one of the k trials passed (tool-style metric)."""
    return 1.0 if any(trial_passes) else 0.0


def pass_caret_k(trial_passes: list[bool]) -> float:
    """pass^k: probability all k trials succeed (Anthropic Demystifying-evals:
    'probability that all k trials succeed'). With one k-sized sample per task
    this is 1.0 iff every trial passed, else 0.0. The dataset-level pass^k is
    the mean of these per-task values."""
    return 1.0 if all(trial_passes) else 0.0


# ---- runner / aggregation --------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{ln}: invalid JSON: {e}")
    return rows


def index_by_task(rows: list[dict], id_key: str = "id") -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows:
        tid = r.get(id_key)
        if tid is None:
            raise SystemExit(f"row missing '{id_key}': {r}")
        out[str(tid)] = r
    return out


def collect_runs(rows: list[dict], k: int) -> dict[str, list[dict]]:
    """runs.jsonl rows: {"id": <task_id>, "output": {...}}. Multiple rows per
    id = multiple trials. We take the first k trials per task."""
    by_task: dict[str, list[dict]] = {}
    for r in rows:
        tid = str(r.get("id"))
        by_task.setdefault(tid, []).append(r.get("output", {}))
    return {tid: outs[:k] for tid, outs in by_task.items()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="expense-agent code-based grader")
    ap.add_argument("--dataset", required=True, type=Path)
    ap.add_argument("--runs", required=True, type=Path)
    ap.add_argument("--k", type=int, default=1, help="trials per task")
    ap.add_argument(
        "--gate",
        type=float,
        default=0.0,
        help="min dataset pass^k mean required for exit 0",
    )
    ap.add_argument("--report", type=Path, default=None, help="write JSON report")
    args = ap.parse_args(argv)

    dataset = index_by_task(load_jsonl(args.dataset))
    runs = collect_runs(load_jsonl(args.runs), args.k)

    per_task = []
    p_at_k_vals, p_caret_k_vals = [], []
    for tid, task in dataset.items():
        ref = task["reference"]
        outs = runs.get(tid, [])
        if len(outs) < args.k:
            # missing trials count as failures (do not silently pass)
            outs = outs + [{}] * (args.k - len(outs))
        trial_passes = [is_trial_pass(o, ref) for o in outs]
        p_at_k = pass_at_k(trial_passes)
        p_caret_k = pass_caret_k(trial_passes)
        p_at_k_vals.append(p_at_k)
        p_caret_k_vals.append(p_caret_k)
        per_task.append(
            {
                "id": tid,
                "trial_passes": trial_passes,
                "pass_at_k": p_at_k,
                "pass_caret_k": p_caret_k,
                "fields": [grade_fields(o, ref) for o in outs],
            }
        )

    n = len(dataset) or 1
    summary = {
        "k": args.k,
        "n_tasks": len(dataset),
        "pass_at_k_mean": sum(p_at_k_vals) / n,
        "pass_caret_k_mean": sum(p_caret_k_vals) / n,
        "per_task": per_task,
    }

    out = json.dumps(summary, indent=2, ensure_ascii=False)
    if args.report:
        args.report.write_text(out, encoding="utf-8")
    print(out)

    gate_ok = summary["pass_caret_k_mean"] >= args.gate
    if not gate_ok:
        print(
            f"FAIL: pass^k mean {summary['pass_caret_k_mean']:.4f} "
            f"< gate {args.gate:.4f}",
            file=sys.stderr,
        )
    return 0 if gate_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
