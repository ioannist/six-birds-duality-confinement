#!/usr/bin/env python3
"""Validator for Step 354 Mode C Stage-IV refinement artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step354_mode_C_stage_IV_four_step_refinement_artifacts")

REQUIRED = [
    "converse_probe_step354.csv",
    "decomposition_step354.csv",
    "earning_at_scale_step354.md",
    "equivalence_audit_step354.csv",
    "step354_results_summary.md",
    "step354_schema.json",
    "nonclaim_boundary_step354.md",
    "run_step354_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step354_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 354
    assert schema["converse_probe_passed"] is True
    assert schema["magnitude_only_translation_overstrong"] is True
    assert schema["decomposition_cells"] == 35
    assert schema["phase_dominant_cells"] == 18
    assert schema["magnitude_dominant_cells"] == 17
    assert schema["earning_at_scale_intermediate_content"] is True
    assert schema["equivalence_audit_distinct"] is True
    assert schema["mode_A_retract_count"] == 3
    assert schema["mode_C_retract_count"] == 0
    assert schema["final_verdict"] == "V_mode_C_stage_IV_passes_refined_residual_needs_phase_operator_terms"

    converse = read_csv("converse_probe_step354.csv")
    assert len(converse) == 3
    assert all(row["converse_result"] == "near_zero_magnitude_OL_does_not_imply_original_H6_bridge" for row in converse)

    decomp = read_csv("decomposition_step354.csv")
    assert len(decomp) == 35
    assert sum(row["dominant_component"] == "phase" for row in decomp) == 18
    assert sum(row["dominant_component"] == "magnitude" for row in decomp) == 17
    assert all(float(row["combined_l2"]) > 0.0 for row in decomp)

    earning = (BASE / "earning_at_scale_step354.md").read_text(encoding="utf-8")
    assert "V-NC bridge-failure" in earning
    assert "transfer-search objective" in earning

    audit = read_csv("equivalence_audit_step354.csv")
    assert len(audit) >= 5
    assert all(row["structurally_distinct"] == "yes" for row in audit)

    boundary = (BASE / "nonclaim_boundary_step354.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary

    print("Step 354 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
