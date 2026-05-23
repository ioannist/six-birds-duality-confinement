#!/usr/bin/env python3
"""Validate Step 209 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step209_riemann_siegel_Z_pivot_artifacts")

REQUIRED = [
    "step209_results_summary.md",
    "step209_schema.json",
    "content_classification_step209.csv",
    "nonclaim_boundary_step209.md",
    "step209_riemann_siegel_Z_pivot.tex",
    "derive_Z_residual_step209.py",
    "run_step209_checks.py",
    "Z_declaration_step209.csv",
    "theta_function_step209.csv",
    "CRE_audit_step209.csv",
    "CRCFT_mode_audit_step209.csv",
    "residual_formulation_step209.csv",
    "cascade_initial_branches_step209.csv",
    "residual_tree_step209.csv",
    "route_status_step209.csv",
    "construction_tasks_step209.csv",
    "classical_theorems_cited_step209.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step209_schema.json").read_text())
    assert schema["step"] == 209
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_Z_CRCFT_TE"
    assert schema["CRE_status"] == "CRE"
    assert schema["CRCFT_mode_classification"] == "CRCFT-TE"

    residuals = rows("residual_formulation_step209.csv")
    if not any(r["candidate_residual"] == "ImZ_L2" and r["RH_equivalent"] == "false" for r in residuals):
        raise SystemExit("missing ImZ non-RH residual audit")
    if not any(r["candidate_residual"] == "zero_count_defect" and r["RH_equivalent"] == "true" for r in residuals):
        raise SystemExit("missing zero-count RH-equivalent residual")

    print("Step 209 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_Z_CRCFT_TE")


if __name__ == "__main__":
    main()
