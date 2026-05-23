#!/usr/bin/env python3
"""Validator for Step 353 Mode C Stage-III transfer artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step353_mode_C_stage_III_OL_minimizing_transfer_artifacts")

REQUIRED = [
    "OL_minimizing_transfer_step353.py",
    "scalar_normalizer_fit_step353.csv",
    "affine_log_fit_step353.csv",
    "weighted_geometric_mean_fit_step353.csv",
    "cross_validation_transfer_step353.csv",
    "step353_results_summary.md",
    "step353_schema.json",
    "nonclaim_boundary_step353.md",
    "run_step353_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step353_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 353
    assert schema["bridge_candidate_identified"] is False
    assert schema["mode_A_retract_count"] == 3
    assert schema["mode_C_retract_count"] == 0
    assert schema["stage_III_status"] == "translated_target_but_no_valid_transfer"
    assert schema["final_verdict"] == "V_mode_C_stage_III_transfer_overfits_no_structural_H6_candidate"

    scalar = read_csv("scalar_normalizer_fit_step353.csv")
    assert len(scalar) == 3
    assert min(float(row["rmse_lambda"]) for row in scalar) > 0.49

    affine = read_csv("affine_log_fit_step353.csv")
    assert len(affine) == 3
    assert min(float(row["rmse_lambda"]) for row in affine) > 0.28

    weighted = read_csv("weighted_geometric_mean_fit_step353.csv")
    assert len(weighted) == 3
    assert max(float(row["max_lambda"]) for row in weighted) < 0.001

    cv = read_csv("cross_validation_transfer_step353.csv")
    assert len(cv) == 9
    weighted_rho2 = [
        row for row in cv if row["candidate"] == "weighted_geometric_train_rho1" and row["test_target"] == "rho_2"
    ][0]
    weighted_rho3 = [
        row for row in cv if row["candidate"] == "weighted_geometric_train_rho1" and row["test_target"] == "rho_3"
    ][0]
    assert float(weighted_rho2["rmse_lambda"]) > 0.7
    assert float(weighted_rho3["rmse_lambda"]) > 1.5

    boundary = (BASE / "nonclaim_boundary_step353.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary

    print("Step 353 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
