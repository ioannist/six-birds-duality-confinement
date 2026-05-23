#!/usr/bin/env python3
"""Validate Step 339 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step339_H6_multiplicative_bridge_artifacts")
REQUIRED = [
    "compute_multiplicative_bridge_step339.py",
    "multiplicative_fit_step339.csv",
    "hold_out_multiplicative_step339.csv",
    "step339_results_summary.md",
    "step339_schema.json",
    "nonclaim_boundary_step339.md",
    "run_step339_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step339_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 339
    assert schema["dps"] >= 80
    assert schema["fit_k"] == list(range(1, 11))
    assert schema["holdout_k"] == [11, 12, 15, 20]

    fit = rows("multiplicative_fit_step339.csv")
    coeffs = [r for r in fit if r["row_type"] == "exponent" and r["model"] == "unconstrained_constant_intercept"]
    train = [r for r in fit if r["row_type"] == "training_residual" and r["model"] == "unconstrained_constant_intercept"]
    taut = [r for r in fit if r["row_type"] == "k_dependent_intercept_correction"]
    assert len(coeffs) == 7
    assert len(train) == 10
    assert len(taut) == 10
    assert max(float(r["relative_magnitude_residual"]) for r in train) < 0.01

    hold = [r for r in rows("hold_out_multiplicative_step339.csv") if r["model"] == "unconstrained_constant_intercept"]
    assert [int(r["k"]) for r in hold] == [11, 12, 15, 20]
    assert max(float(r["relative_magnitude_residual"]) for r in hold) < 0.01

    summary = (ART / "step339_results_summary.md").read_text(encoding="utf-8")
    assert "V_hecke_H6_multiplicative_bridge_candidate_verified_numerically" in summary
    assert "product-form numerical bridge candidate" in summary
    nonclaim = (ART / "nonclaim_boundary_step339.md").read_text(encoding="utf-8")
    assert "No RH or GRH claim" in nonclaim
    print("Step 339 validator: PASS")


if __name__ == "__main__":
    main()
