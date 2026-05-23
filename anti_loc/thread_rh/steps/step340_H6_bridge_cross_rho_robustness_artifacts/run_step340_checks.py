#!/usr/bin/env python3
"""Validate Step 340 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step340_H6_bridge_cross_rho_robustness_artifacts")
REQUIRED = [
    "compute_L_k_rho_2_step340.py",
    "cross_rho_prediction_step340.csv",
    "b0_rho_specific_step340.csv",
    "step340_results_summary.md",
    "step340_schema.json",
    "nonclaim_boundary_step340.md",
    "run_step340_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step340_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 340
    assert schema["dps"] >= 80
    assert schema["rho_tested"] == "rho_2"
    assert schema["k_values"] == [1, 2, 3, 5, 10, 15, 20]
    assert schema["final_verdict"] == "V_H6_multiplicative_bridge_cross_rho_fails"

    fixed = rows("cross_rho_prediction_step340.csv")
    assert [int(r["k"]) for r in fixed] == [1, 2, 3, 5, 10, 15, 20]
    assert max(float(r["relative_residual"]) for r in fixed) > 0.05

    rho_rows = rows("b0_rho_specific_step340.csv")
    assert rho_rows[0]["row_type"] == "rho2_intercept"
    tested = [r for r in rho_rows if r["row_type"] == "rho2_specific_b0_shared_a_chi"]
    assert len(tested) == 7
    assert max(float(r["relative_residual"]) for r in tested) > 0.05

    summary = (ART / "step340_results_summary.md").read_text(encoding="utf-8")
    assert "rho-specific rather than structurally cross-rho robust" in summary
    nonclaim = (ART / "nonclaim_boundary_step340.md").read_text(encoding="utf-8")
    assert "No RH or GRH claim" in nonclaim
    print("Step 340 validator: PASS")


if __name__ == "__main__":
    main()
