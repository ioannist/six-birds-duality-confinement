#!/usr/bin/env python3
"""Validate Step 271 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step271_branch_C_saddle_numerics_artifacts")

REQUIRED = [
    "step271_results_summary.md",
    "step271_schema.json",
    "content_classification_step271.csv",
    "nonclaim_boundary_step271.md",
    "step271_branch_C_saddle_numerics.tex",
    "solve_saddle_step271.py",
    "compute_step271_output.txt",
    "run_step271_checks.py",
    "saddle_z_star_step271.csv",
    "predicted_b_c_step271.csv",
    "comparison_predicted_vs_numerical_step271.csv",
    "residual_tree_step271.csv",
    "route_status_step271.csv",
    "construction_tasks_step271.csv",
    "classical_theorems_cited_step271.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step271_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "saddle_z_star",
        "predicted_b_c",
        "numerical_b_c",
        "comparison_table",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            raise SystemExit(f"schema missing key {key}")
    if schema["step"] != 271:
        raise SystemExit("schema step mismatch")
    if schema["final_verdict"] != "V_branch_C_closed_form_mismatched":
        raise SystemExit("unexpected verdict")

    saddles = read_csv("saddle_z_star_step271.csv")
    if len(saddles) != 15:
        raise SystemExit(f"expected 15 saddle rows, got {len(saddles)}")
    for row in saddles:
        if float(row["abs_z_minus_rho"]) <= 0:
            raise SystemExit(f"bad saddle radius: {row}")

    comparisons = read_csv("comparison_predicted_vs_numerical_step271.csv")
    if len(comparisons) != 3:
        raise SystemExit("expected 3 comparison rows")
    if any(row["match_within_10_percent"] == "True" for row in comparisons):
        raise SystemExit("unexpected all-criteria match")

    print("run_step271_checks.py PASS")


if __name__ == "__main__":
    main()
