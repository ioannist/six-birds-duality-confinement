#!/usr/bin/env python3
"""Validate Step 342 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step342_H6_joint_shared_a_chi_bridge_artifacts")
REQUIRED = [
    "compute_joint_bridge_step342.py",
    "joint_fit_step342.csv",
    "cross_validation_rho_4_step342.csv",
    "step342_results_summary.md",
    "step342_schema.json",
    "nonclaim_boundary_step342.md",
    "run_step342_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step342_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 342
    assert schema["dps"] >= 80
    assert schema["parameter_count"] == 10
    assert schema["training_point_count"] == 30
    assert schema["design_rank"] == 10
    assert schema["final_verdict"] == "V_H6_joint_shared_a_chi_training_fails"

    fit = rows("joint_fit_step342.csv")
    params = [r for r in fit if r["row_type"] == "parameter"]
    train = [r for r in fit if r["row_type"] == "training_residual"]
    assert len(params) == 10
    assert len(train) == 30
    assert max(float(r["relative_residual"]) for r in train) > 0.05

    cv = rows("cross_validation_rho_4_step342.csv")
    assert [r["row_type"] for r in cv] == ["rho4_intercept", "rho4_prediction", "rho4_prediction"]
    assert float(cv[-1]["relative_residual"]) > 0.05

    summary = (ART / "step342_results_summary.md").read_text(encoding="utf-8")
    assert "Max training residual over 30 cells" in summary
    nonclaim = (ART / "nonclaim_boundary_step342.md").read_text(encoding="utf-8")
    assert "No RH or GRH claim" in nonclaim
    print("Step 342 validator: PASS")


if __name__ == "__main__":
    main()
