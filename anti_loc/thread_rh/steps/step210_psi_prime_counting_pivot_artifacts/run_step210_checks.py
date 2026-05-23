#!/usr/bin/env python3
"""Validate Step 210 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step210_psi_prime_counting_pivot_artifacts")

REQUIRED = [
    "step210_results_summary.md",
    "step210_schema.json",
    "content_classification_step210.csv",
    "nonclaim_boundary_step210.md",
    "step210_psi_prime_counting_pivot.tex",
    "derive_psi_residual_step210.py",
    "run_step210_checks.py",
    "psi_declaration_step210.csv",
    "CRE_audit_step210.csv",
    "CRCFT_mode_audit_step210.csv",
    "explicit_formula_decomposition_step210.csv",
    "cross_relation_with_Mertens_step210.csv",
    "residual_tree_step210.csv",
    "route_status_step210.csv",
    "construction_tasks_step210.csv",
    "classical_theorems_cited_step210.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step210_schema.json").read_text())
    assert schema["step"] == 210
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_psi_CRCFT_TE"
    assert schema["CRE_status"] == "CRE"
    assert schema["CRCFT_mode_classification"] == "CRCFT-TE"

    explicit = rows("explicit_formula_decomposition_step210.csv")
    if not any(r["component"] == "CTMT_verdict" and "not CTMT" in r["formula"] for r in explicit):
        raise SystemExit("missing explicit formula CTMT audit verdict")

    print("Step 210 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_psi_CRCFT_TE")


if __name__ == "__main__":
    main()
