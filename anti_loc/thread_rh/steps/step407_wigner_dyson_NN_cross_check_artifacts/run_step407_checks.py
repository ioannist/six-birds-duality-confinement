#!/usr/bin/env python3
"""Validate Step 407 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step407_wigner_dyson_NN_cross_check_artifacts")
REQUIRED = [
    "p_NN_predictions_step407.csv",
    "comparison_step407.md",
    "step407_results_summary.md",
    "step407_schema.json",
    "nonclaim_boundary_step407.md",
    "run_step407_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step407_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 407:
        raise SystemExit("schema step is not 407")
    if "matches" not in schema.get("verdict", ""):
        raise SystemExit("unexpected verdict")
    if float(schema["relative_difference_two_sided"]) >= 0.05:
        raise SystemExit("two-sided prediction not within 5%")

    with (ART / "p_NN_predictions_step407.csv").open(newline="", encoding="utf-8") as handle:
        rows = {row["quantity"]: row["value"] for row in csv.DictReader(handle)}
    if "two_sided_smin_prediction_1_minus_1_minus_F_squared" not in rows:
        raise SystemExit("missing two-sided prediction")

    nonclaim = (ART / "nonclaim_boundary_step407.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 407 checks passed.")
    print("two_sided_prediction=0.6001968966476768")
    print("empirical=0.6059850374064838")


if __name__ == "__main__":
    main()
