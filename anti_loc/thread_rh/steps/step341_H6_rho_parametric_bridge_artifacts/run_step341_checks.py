#!/usr/bin/env python3
"""Validate Step 341 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step341_H6_rho_parametric_bridge_artifacts")
REQUIRED = [
    "compute_L_k_rho_3_step341.py",
    "rho_parametric_fit_step341.csv",
    "training_residuals_step341.csv",
    "cross_validation_rho_3_step341.csv",
    "step341_results_summary.md",
    "step341_schema.json",
    "nonclaim_boundary_step341.md",
    "run_step341_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step341_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 341
    assert schema["dps"] >= 80
    assert schema["training_rhos"] == ["rho_1", "rho_2"]
    assert schema["holdout_rho"] == "rho_3"
    assert schema["final_verdict"] == "V_H6_rho_parametric_bridge_cross_rho3_fails"
    assert schema["design_rank"] == 16

    params = rows("rho_parametric_fit_step341.csv")
    assert len(params) == 17
    train = rows("training_residuals_step341.csv")
    assert len(train) == 20
    assert max(float(r["relative_residual"]) for r in train) < 0.05

    cv = rows("cross_validation_rho_3_step341.csv")
    assert [int(r["k"]) for r in cv] == [1, 5, 10, 15, 20]
    assert max(float(r["relative_residual"]) for r in cv) > 0.05

    summary = (ART / "step341_results_summary.md").read_text(encoding="utf-8")
    assert "rho_3 holdout max residual" in summary
    nonclaim = (ART / "nonclaim_boundary_step341.md").read_text(encoding="utf-8")
    assert "No RH or GRH claim" in nonclaim
    print("Step 341 validator: PASS")


if __name__ == "__main__":
    main()
