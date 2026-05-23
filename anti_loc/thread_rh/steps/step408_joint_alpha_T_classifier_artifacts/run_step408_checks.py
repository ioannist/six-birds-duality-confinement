#!/usr/bin/env python3
"""Validate Step 408 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step408_joint_alpha_T_classifier_artifacts")
REQUIRED = [
    "joint_classifier_step408.csv",
    "classifier_summary_step408.md",
    "step408_results_summary.md",
    "step408_schema.json",
    "nonclaim_boundary_step408.md",
    "run_step408_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step408_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 408:
        raise SystemExit("schema step is not 408")
    if float(schema["balanced_accuracy"]) >= 0.80:
        raise SystemExit("schema unexpectedly claims clean >=80% criterion")

    with (ART / "joint_classifier_step408.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != int(schema["n_rows"]):
        raise SystemExit(f"expected {schema['n_rows']} rows, got {len(rows)}")
    if sum(int(r["actual_fail"]) for r in rows) != int(schema["n_fail"]):
        raise SystemExit("failure count mismatch")
    if "alpha" not in rows[0]:
        raise SystemExit("missing alpha column")

    nonclaim = (ART / "nonclaim_boundary_step408.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 408 checks passed.")
    print("best_balanced_accuracy=0.7601412066752247")
    print("verdict=no clean >=80% joint criterion")


if __name__ == "__main__":
    main()
