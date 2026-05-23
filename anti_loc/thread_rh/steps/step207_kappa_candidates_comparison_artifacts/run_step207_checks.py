#!/usr/bin/env python3
"""Validate Step 207 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts")

REQUIRED = [
    "step207_results_summary.md",
    "step207_schema.json",
    "content_classification_step207.csv",
    "nonclaim_boundary_step207.md",
    "step207_kappa_candidates_comparison.tex",
    "compute_CAND1_step207.py",
    "compute_CAND2_step207.py",
    "compare_candidates_step207.py",
    "compute_c_matrix_step207.py",
    "compute_xi_decision_step207.py",
    "compute_step207_output.txt",
    "CAND1_samples_step207.csv",
    "CAND2_samples_step207.csv",
    "ratio_table_step207.csv",
    "transport_sampling_resolution_step207.csv",
    "c_matrix_step207.csv",
    "G_matrix_step207.csv",
    "xi_decision_step207.csv",
    "residual_tree_step207.csv",
    "route_status_step207.csv",
    "construction_tasks_step207.csv",
    "classical_theorems_cited_step207.csv",
]


def count_rows(name: str) -> int:
    with (BASE / name).open(newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step207_schema.json").read_text())
    assert schema["step"] == 207
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_kappa_tau_candidates_disagree"

    expected_counts = {
        "CAND1_samples_step207.csv": 600,
        "CAND2_samples_step207.csv": 600,
        "ratio_table_step207.csv": 600,
        "c_matrix_step207.csv": 9,
        "G_matrix_step207.csv": 9,
    }
    for name, expected in expected_counts.items():
        got = count_rows(name)
        if got != expected:
            raise SystemExit(f"{name}: expected {expected} rows, got {got}")

    with (BASE / "transport_sampling_resolution_step207.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    overall = [r for r in rows if r["rho_index"] == "overall"]
    if not overall or overall[0]["verdict"] != "V_kappa_tau_candidates_disagree":
        raise SystemExit("transport resolution missing disagreement verdict")

    with (BASE / "xi_decision_step207.csv").open(newline="") as f:
        xi_rows = list(csv.DictReader(f))
    if xi_rows[0]["verdict"] != "V_kappa_tau_candidates_disagree":
        raise SystemExit("Xi decision does not carry disagreement verdict")

    print("Step 207 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_kappa_tau_candidates_disagree")


if __name__ == "__main__":
    main()
