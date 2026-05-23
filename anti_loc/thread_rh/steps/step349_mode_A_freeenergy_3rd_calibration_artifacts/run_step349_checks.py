#!/usr/bin/env python3
"""Validator for Step 349 free-energy Mode A calibration artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step349_mode_A_freeenergy_3rd_calibration_artifacts")

REQUIRED = [
    "virtual_freeenergy_spec_step349.md",
    "self_consistency_solve_step349.csv",
    "extrapolation_compare_step349.csv",
    "ablation_self_consistency_step349.csv",
    "step349_results_summary.md",
    "step349_schema.json",
    "nonclaim_boundary_step349.md",
    "run_step349_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    mp.mp.dps = 80

    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step349_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 349
    assert int(schema["dps"]) >= 80
    assert int(schema["virtual_gamma_count"]) == 3
    assert int(schema["empirical_match_within_10_percent"]) == 3
    assert schema["trivial_ablation_outputs_changed"] is True
    assert schema["mode_A_retract_count_update"] == 2
    assert schema["final_verdict"] == "V_mode_A_freeenergy_stage_I_partial_on_track_not_theorem_grade"

    solve_rows = read_csv("self_consistency_solve_step349.csv")
    assert len(solve_rows) == 3
    for row in solve_rows:
        theta = mp.mpf(row["theta"])
        lam = mp.mpf(row["lambda"])
        gamma = mp.mpf(row["gamma_virtual"])
        residual = gamma + lam * gamma**3 - theta
        assert abs(residual) < mp.mpf("1e-45")

    compare_rows = read_csv("extrapolation_compare_step349.csv")
    assert len(compare_rows) == 3
    assert all(mp.mpf(row["relative_error"]) < mp.mpf("0.10") for row in compare_rows)
    assert all(row["status"] == "match_within_10_percent" for row in compare_rows)

    ablation_rows = read_csv("ablation_self_consistency_step349.csv")
    assert len(ablation_rows) == 6
    trivial = [row for row in ablation_rows if row["ablation"] == "F_identically_zero"]
    linear = [row for row in ablation_rows if row["ablation"] == "linearized_no_quartic_term"]
    assert len(trivial) == 3
    assert len(linear) == 3
    assert all(mp.mpf(row["relative_change"]) == mp.mpf("1.0") for row in trivial)
    assert max(mp.mpf(row["relative_change"]) for row in linear) < mp.mpf("0.04")
    assert max(mp.mpf(row["relative_change"]) for row in linear) > mp.mpf("0.005")

    spec = (BASE / "virtual_freeenergy_spec_step349.md").read_text(encoding="utf-8")
    assert "dimensionless-temperature lens" in spec
    assert "gamma + lambda gamma^3" in spec

    boundary = (BASE / "nonclaim_boundary_step349.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "not a theorem-grade derivation" in boundary

    print("Step 349 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
