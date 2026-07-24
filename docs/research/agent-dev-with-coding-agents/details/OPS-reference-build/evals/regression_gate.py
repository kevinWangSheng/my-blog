#!/usr/bin/env python3
"""Regression gate: compare grader reports against a committed baseline.

Fails (exit 1) if any suite's pass^k mean dropped by more than --threshold
vs evals/baseline.json. Judges results only (consumes grader reports).

Run:
    python evals/regression_gate.py \
        --baseline evals/baseline.json \
        --reports runs/extraction_report.json runs/classification_report.json \
        --threshold 0.02
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def suite_name(report_path: Path) -> str:
    # runs/extraction_report.json -> extraction
    return report_path.stem.replace("_report", "")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True, type=Path)
    ap.add_argument("--reports", required=True, nargs="+", type=Path)
    ap.add_argument("--threshold", type=float, default=0.02)
    args = ap.parse_args(argv)

    if not args.baseline.exists():
        print(f"baseline missing: {args.baseline}", file=sys.stderr)
        return 2
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))

    regressed = False
    for rp in args.reports:
        rep = json.loads(rp.read_text(encoding="utf-8"))
        name = suite_name(rp)
        cur = rep["pass_caret_k_mean"]
        base = baseline.get(name, {}).get("pass_caret_k_mean")
        if base is None:
            print(f"{name}: no baseline entry; current pass^k={cur:.4f} (skipped)")
            continue
        drop = base - cur
        status = "OK"
        if drop > args.threshold:
            status = "REGRESSION"
            regressed = True
        print(
            f"{name:16s} baseline={base:.4f} current={cur:.4f} "
            f"drop={drop:+.4f} (threshold {args.threshold:.4f}) -> {status}"
        )

    if regressed:
        print("\nregression gate FAILED", file=sys.stderr)
        return 1
    print("\nregression gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
