#!/usr/bin/env python3
"""Validate Step 394 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step394_close_pair_foreclosure_universal_artifacts")
REQUIRED = [
    "exceptional_low_k_step394.csv",
    "comparison_to_neighbor_baseline_step394.csv",
    "step394_results_summary.md",
    "step394_schema.json",
    "nonclaim_boundary_step394.md",
    "run_step394_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step394_schema.json").read_text())
    if schema.get("step") != 394:
        raise SystemExit("wrong step")
    if schema.get("dps", 0) < 80:
        raise SystemExit("dps below requirement")

    data = rows("exceptional_low_k_step394.csv")
    comp = rows("comparison_to_neighbor_baseline_step394.csv")
    expected = schema["step378_exceptional_cells"] + schema["confirmed_pair_cells"]
    if len(data) != expected:
        raise SystemExit("data row count mismatch")
    if not comp:
        raise SystemExit("neighbor comparison is empty")
    step378_fail = sum(1 for r in data if r["category"] == "step378_exceptional" and r["pass_foreclosure"] == "FAIL")
    confirmed_fail = sum(1 for r in data if r["category"] == "step393_confirmed_pair" and r["pass_foreclosure"] == "FAIL")
    if step378_fail != schema["step378_exceptional_failures"]:
        raise SystemExit("step378 failure count mismatch")
    if confirmed_fail != schema["confirmed_pair_failures"]:
        raise SystemExit("confirmed failure count mismatch")
    for r in data[:5] + comp[:5]:
        float(r.get("abs_delta_Dk") or r.get("target_abs_delta_Dk"))
    if "No RH claim" not in (ART / "nonclaim_boundary_step394.md").read_text():
        raise SystemExit("nonclaim missing")

    print("step394 checks passed")


if __name__ == "__main__":
    main()
