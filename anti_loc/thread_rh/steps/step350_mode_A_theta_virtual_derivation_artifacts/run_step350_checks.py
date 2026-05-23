#!/usr/bin/env python3
"""Validator for Step 350 virtual theta derivation artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step350_mode_A_theta_virtual_derivation_artifacts")

REQUIRED = [
    "virtual_theta_derivation_step350.md",
    "virtual_theta_values_step350.csv",
    "virtual_gamma_inf_step350.csv",
    "ablation_virtual_vs_empirical_theta_step350.csv",
    "step350_results_summary.md",
    "step350_schema.json",
    "nonclaim_boundary_step350.md",
    "run_step350_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    mp.mp.dps = 80
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step350_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 350
    assert int(schema["dps"]) >= 80
    assert schema["empirical_coefficients_used_in_virtual_theta"] is False
    assert schema["selected_candidate"] == "pi_kappa_over_T"
    assert int(schema["selected_candidate_gamma_pass_count_under_30_percent"]) == 1
    assert int(schema["selected_candidate_gamma_fail_count_under_30_percent"]) == 2
    assert schema["ablation_distinguishes_virtual_from_empirical"] is True
    assert schema["mode_A_retract_count_update"] == 3
    assert schema["mode_B_licensed"] is True
    assert schema["final_verdict"] == "V_mode_A_theta_derivation_failed_empirical_field_still_required"

    theta_rows = read_csv("virtual_theta_values_step350.csv")
    assert len(theta_rows) == 9
    assert {row["candidate"] for row in theta_rows} == {"kappa_over_T", "pi_kappa_over_T", "prompt_shape"}
    selected_theta = [row for row in theta_rows if row["candidate"] == "pi_kappa_over_T"]
    assert len(selected_theta) == 3
    assert sum(mp.mpf(row["theta_relative_error"]) < mp.mpf("0.30") for row in selected_theta) == 1

    gamma_rows = read_csv("virtual_gamma_inf_step350.csv")
    assert len(gamma_rows) == 9
    selected_gamma = [row for row in gamma_rows if row["candidate"] == "pi_kappa_over_T"]
    assert len(selected_gamma) == 3
    assert sum(row["acceptance"] == "pass_for_this_rho" for row in selected_gamma) == 1
    assert sum(row["acceptance"] == "fail" for row in selected_gamma) == 2

    ablation_rows = read_csv("ablation_virtual_vs_empirical_theta_step350.csv")
    assert len(ablation_rows) == 3
    assert all(row["interpretation"] == "distinguishes_derivations" for row in ablation_rows)
    assert min(mp.mpf(row["relative_change_vs_virtual"]) for row in ablation_rows) > mp.mpf("0.15")

    derivation = (BASE / "virtual_theta_derivation_step350.md").read_text(encoding="utf-8")
    assert "No step 324 fit coefficients" in derivation
    assert "GUE" in derivation

    boundary = (BASE / "nonclaim_boundary_step350.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary

    print("Step 350 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
