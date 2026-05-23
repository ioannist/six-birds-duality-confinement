#!/usr/bin/env python3
"""Validator for Step 356 Mode B Stage-I artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step356_mode_B_stage_I_top_down_design_artifacts")

REQUIRED = [
    "U_flat_operational_signature_step356.md",
    "minimal_finite_kernel_step356.csv",
    "SAU_gate_checks_step356.csv",
    "stage_II_preview_step356.csv",
    "step356_results_summary.md",
    "step356_schema.json",
    "nonclaim_boundary_step356.md",
    "run_step356_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step356_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 356
    assert schema["state_count"] == 5
    assert schema["states"] == ["a", "b", "c", "d", "e"]
    assert schema["non_descent_witness"] == "e"
    assert schema["rewrite_rule_count"] == 6
    assert schema["SAU_gates_passed"] == 6
    assert schema["SAU_gates_failed"] == 0
    assert schema["stage_II_preview_count"] == 1
    assert schema["stage_II_preview_relative_error"] == 0.0
    assert schema["target_tau_primitive"] is False
    assert schema["mode_B_retract_count"] == 0
    assert schema["final_verdict"] == "V_mode_B_stage_I_finite_signature_passes_SAU"

    kernel = read_csv("minimal_finite_kernel_step356.csv")
    assert len(kernel) == 6
    assert {row["rule"] for row in kernel} == {
        "R_H_load",
        "R_Z_load",
        "R_compare",
        "R_operator_audit",
        "R_block",
        "R_admit",
    }

    gates = read_csv("SAU_gate_checks_step356.csv")
    assert len(gates) == 6
    assert all(row["status"] == "pass" for row in gates)
    assert any(row["gate"] == "primitive_exclusion" and "target_tau_not" in row["evidence"] for row in gates)

    preview = read_csv("stage_II_preview_step356.csv")
    assert len(preview) == 1
    assert preview[0]["used_in_design"] == "no"
    assert float(preview[0]["relative_error"]) == 0.0

    spec = (BASE / "U_flat_operational_signature_step356.md").read_text(encoding="utf-8")
    assert "Sigma = {a, b, c, d, e}" in spec
    assert "q(e) = undefined / blocked" in spec
    assert "does not contain a primitive transfer" in spec

    boundary = (BASE / "nonclaim_boundary_step356.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary

    print("Step 356 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
