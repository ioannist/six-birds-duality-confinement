#!/usr/bin/env python3
"""Validate Step 401 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step401_near_diagonal_bergman_sufficiency_artifacts")
REQUIRED = [
    "scale_comparison_step401.csv",
    "partial_closure_attempt_step401.md",
    "step401_results_summary.md",
    "step401_schema.json",
    "nonclaim_boundary_step401.md",
    "run_step401_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step401_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 401:
        raise SystemExit("schema step is not 401")
    if "marginal" not in schema.get("verdict", ""):
        raise SystemExit("unexpected verdict")

    with (ART / "scale_comparison_step401.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 10:
        raise SystemExit("scale table too small")
    if not any(row["T"] == "10000" and row["p"] == "1000000" and row["inside_standard_1_over_sqrt_p"] == "TRUE" for row in rows):
        raise SystemExit("expected T=10000,p=1000000 standard inside row")
    if not any(row["T"].startswith("14.134") and row["p"] == "30" and row["inside_standard_1_over_sqrt_p"] == "FALSE" for row in rows):
        raise SystemExit("expected low-T p=30 marginal row")

    nonclaim = (ART / "nonclaim_boundary_step401.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 401 checks passed.")
    print("verdict=marginal_conditional_sufficiency_for_Branch_A_large_T")


if __name__ == "__main__":
    main()
