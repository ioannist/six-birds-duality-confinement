#!/usr/bin/env python3
"""Validator for Step 351 Mode C ID/OL profile-transfer artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step351_mode_C_profile_transfer_artifacts")

REQUIRED = [
    "profile_transfer_construction_step351.md",
    "ID_OL_recombined_carrier_step351.csv",
    "stage_II_preview_step351.csv",
    "ablation_drop_OL_step351.csv",
    "SAU_inherited_audit_hypotheses_step351.csv",
    "step351_results_summary.md",
    "step351_schema.json",
    "nonclaim_boundary_step351.md",
    "run_step351_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step351_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 351
    assert schema["profiles"] == ["invariant_descent", "obstruction_ledger"]
    assert schema["stage_II_preview_rows"] == 12
    assert schema["stage_II_preview_reproduced_with_zero_error"] == 12
    assert schema["nonzero_obstruction_rows"] == 12
    assert schema["drop_OL_descent_decisions_changed"] == 12
    assert schema["mode_A_retract_count"] == 3
    assert schema["mode_C_retract_count"] == 0
    assert schema["final_verdict"] == "V_mode_C_ID_OL_stage_I_on_track_substantive_OL"

    carrier = read_csv("ID_OL_recombined_carrier_step351.csv")
    assert len(carrier) == 12
    assert all(float(row["lambda_obs"]) > 0.0 for row in carrier)
    assert all(row["descent_status"] == "blocked_by_OL" for row in carrier)

    preview = read_csv("stage_II_preview_step351.csv")
    assert len(preview) == 12
    assert all(float(row["relative_error"]) == 0.0 for row in preview)
    assert all(row["OL_status"] == "nonzero_obstruction" for row in preview)

    ablation = read_csv("ablation_drop_OL_step351.csv")
    assert len(ablation) == 12
    assert all(row["descent_decision_changed"] == "yes" for row in ablation)
    assert all(row["ablated_descent_status"] == "forced_descend" for row in ablation)
    assert max(float(row["false_descent_relative_error"]) for row in ablation) > 10.0

    sau = read_csv("SAU_inherited_audit_hypotheses_step351.csv")
    assert len(sau) >= 5
    assert any(row["profile_or_component"] == "SAU_no_smuggling" and row["status"] == "passed" for row in sau)

    construction = (BASE / "profile_transfer_construction_step351.md").read_text(encoding="utf-8")
    assert "Invariant-descent" in construction
    assert "Obstruction-ledger" in construction

    boundary = (BASE / "nonclaim_boundary_step351.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary

    print("Step 351 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
