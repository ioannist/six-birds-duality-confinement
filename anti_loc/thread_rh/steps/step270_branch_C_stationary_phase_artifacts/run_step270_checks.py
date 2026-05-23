#!/usr/bin/env python3
"""Validate Step 270 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step270_branch_C_stationary_phase_artifacts")

REQUIRED = [
    "step270_results_summary.md",
    "step270_schema.json",
    "content_classification_step270.csv",
    "nonclaim_boundary_step270.md",
    "step270_branch_C_stationary_phase.tex",
    "derive_stationary_phase_step270.py",
    "compute_step270_output.txt",
    "run_step270_checks.py",
    "closed_identity_step270.csv",
    "saddle_point_step270.csv",
    "predicted_vs_numerical_step270.csv",
    "residual_tree_step270.csv",
    "route_status_step270.csv",
    "construction_tasks_step270.csv",
    "classical_theorems_cited_step270.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step270_schema.json").read_text(encoding="utf-8"))
    required_schema = [
        "step",
        "orientation",
        "target",
        "closed_identity_L_k",
        "saddle_point_form",
        "predicted_b_c",
        "numerical_comparison",
        "retained_nogos",
        "final_verdict",
    ]
    absent = [key for key in required_schema if key not in schema]
    if absent:
        raise SystemExit(f"schema missing keys: {absent}")
    if schema["step"] != 270:
        raise SystemExit("schema step mismatch")
    if schema["final_verdict"] != "V_branch_C_stationary_phase_partial":
        raise SystemExit("unexpected verdict")

    identity = read_csv("closed_identity_step270.csv")
    if len(identity) != 21:
        raise SystemExit(f"expected 21 identity rows, got {len(identity)}")
    for row in identity:
        ratio = float(row["raw_to_inherited_abs_ratio"])
        if ratio <= 0:
            raise SystemExit(f"bad ratio row: {row}")

    pred = read_csv("predicted_vs_numerical_step270.csv")
    if len(pred) != 3:
        raise SystemExit("expected 3 predicted-vs-numerical rows")
    if not all(row["predicted_b"] == "undetermined_without_projected_kernel_saddle" for row in pred):
        raise SystemExit("predicted b status mismatch")

    output = (ART / "compute_step270_output.txt").read_text(encoding="utf-8")
    if "verdict" in output:
        raise SystemExit("compute output should contain diagnostic ratios only")

    print("run_step270_checks.py PASS")


if __name__ == "__main__":
    main()
