#!/usr/bin/env python3
"""Validator for Step 358 Mode B Stage-III admissibility artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step358_mode_B_stage_III_admissibility_artifacts")

REQUIRED = [
    "admissibility_formalization_step358.md",
    "transfer_search_step358.csv",
    "cross_validation_step358.csv",
    "mode_B_vs_mode_C_stage_III_comparison_step358.csv",
    "step358_results_summary.md",
    "step358_schema.json",
    "nonclaim_boundary_step358.md",
    "run_step358_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step358_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 358
    assert schema["transfer_families_tested"] == 2
    assert schema["best_training_rmse"] > 1.0
    assert schema["operator_gate_certified"] is False
    assert schema["admissible_transfer_found"] is False
    assert schema["mode_B_retract_count"] == 1
    assert schema["final_verdict"] == "V_mode_B_stage_III_fails_training_transfer_not_found"

    search = read_csv("transfer_search_step358.csv")
    assert len(search) == 14
    assert {row["candidate"] for row in search} == {"tau_character_scalar", "tau_character_affine_log"}
    assert all(row["operator_status"] == "missing_operator_certificate" for row in search)

    cv = read_csv("cross_validation_step358.csv")
    assert len(cv) == 6
    assert all(row["admissible"] == "no" for row in cv)
    assert min(float(row["rmse_combined"]) for row in cv if row["test_target"] == "rho_1") > 1.0

    comparison = read_csv("mode_B_vs_mode_C_stage_III_comparison_step358.csv")
    assert len(comparison) == 3
    assert any(row["mode"] == "Mode_C" and "overfits" in row["diagnosis"] for row in comparison)
    assert all(row["operator_gate"] in {"not_certified", "missing_operator_certificate"} for row in comparison)

    formal = (BASE / "admissibility_formalization_step358.md").read_text(encoding="utf-8")
    assert "R_admit" in formal
    assert "tau_character_scalar" in formal
    assert "tau_character_affine_log" in formal

    boundary = (BASE / "nonclaim_boundary_step358.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary
    assert "not inserted as a carrier primitive" in boundary

    print("Step 358 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
