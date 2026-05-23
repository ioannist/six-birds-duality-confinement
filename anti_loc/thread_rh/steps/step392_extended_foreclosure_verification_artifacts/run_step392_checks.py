#!/usr/bin/env python3
"""Validate Step 392 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step392_extended_foreclosure_verification_artifacts")
REQUIRED = [
    "extended_L_k_values_step392.csv",
    "foreclosure_check_extended_step392.csv",
    "trend_analysis_step392.md",
    "step392_results_summary.md",
    "step392_schema.json",
    "nonclaim_boundary_step392.md",
    "run_step392_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step392_schema.json").read_text())
    if schema.get("step") != 392:
        raise SystemExit("wrong step")
    if schema.get("dps", 0) < 50:
        raise SystemExit("dps below requirement")

    vals = rows("extended_L_k_values_step392.csv")
    checks = rows("foreclosure_check_extended_step392.csv")
    if len(vals) != schema["computed_cells"] or len(checks) != schema["computed_cells"]:
        raise SystemExit("row count mismatch")
    pass_count = sum(1 for r in checks if r["pass_foreclosure"] == "PASS")
    fail_count = sum(1 for r in checks if r["pass_foreclosure"] == "FAIL")
    if pass_count != schema["pass_count"] or fail_count != schema["fail_count"]:
        raise SystemExit("pass/fail count mismatch")
    for r in checks:
        float(r["abs_delta_Dk"])
        float(r["threshold"])
    if "No RH claim" not in (ART / "nonclaim_boundary_step392.md").read_text():
        raise SystemExit("nonclaim missing")
    if "j-bin" not in (ART / "trend_analysis_step392.md").read_text():
        raise SystemExit("trend table missing")

    print("step392 checks passed")


if __name__ == "__main__":
    main()
