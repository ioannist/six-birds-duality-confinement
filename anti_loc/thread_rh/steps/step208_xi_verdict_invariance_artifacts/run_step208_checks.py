#!/usr/bin/env python3
"""Validate Step 208 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts")

REQUIRED = [
    "step208_results_summary.md",
    "step208_schema.json",
    "content_classification_step208.csv",
    "nonclaim_boundary_step208.md",
    "step208_xi_verdict_invariance.tex",
    "compute_c_matrices_step208.py",
    "compute_xi_invariance_step208.py",
    "compute_step208_output.txt",
    "c_matrix_CAND1_step208.csv",
    "c_matrix_CAND2_step208.csv",
    "xi_matrix_source_CAND1_step208.csv",
    "xi_matrix_source_CAND2_step208.csv",
    "verdict_invariance_step208.csv",
    "robustness_step208.csv",
    "residual_tree_step208.csv",
    "route_status_step208.csv",
    "construction_tasks_step208.csv",
    "classical_theorems_cited_step208.csv",
]


def count_rows(path: Path) -> int:
    with path.open(newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step208_schema.json").read_text())
    assert schema["step"] == 208
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_xi_invariant_partial"

    for name in ["c_matrix_CAND1_step208.csv", "c_matrix_CAND2_step208.csv"]:
        got = count_rows(BASE / name)
        if got != 9:
            raise SystemExit(f"{name}: expected 9 rows, got {got}")
    if count_rows(BASE / "robustness_step208.csv") < 6:
        raise SystemExit("robustness table too small")

    with (BASE / "verdict_invariance_step208.csv").open(newline="") as f:
        row = next(csv.DictReader(f))
    if row["final_verdict"] != "V_xi_invariant_partial":
        raise SystemExit("unexpected invariance verdict")

    print("Step 208 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_xi_invariant_partial")


if __name__ == "__main__":
    main()
