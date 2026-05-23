#!/usr/bin/env python3
"""Validate Step 204 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step204_unnormalized_xi_matrix_source_artifacts")
REQUIRED = [
    "step204_results_summary.md",
    "step204_schema.json",
    "content_classification_step204.csv",
    "nonclaim_boundary_step204.md",
    "step204_unnormalized_xi_matrix_source.tex",
    "derive_xi_formula_step204.py",
    "compute_c_matrix_step204.py",
    "compute_xi_decision_step204.py",
    "compute_step204_output.txt",
    "run_step204_checks.py",
    "xi_formula_derivation_step204.csv",
    "G_matrix_step204.csv",
    "c_matrix_step204.csv",
    "M_matrix_step204.csv",
    "xi_decision_step204.csv",
    "robustness_step204.csv",
    "residual_tree_step204.csv",
    "route_status_step204.csv",
    "construction_tasks_step204.csv",
    "classical_theorems_cited_step204.csv",
]
ALLOWED = {
    "V_unnormalized_xi_closes",
    "V_unnormalized_xi_nonzero",
    "V_unnormalized_xi_inconclusive",
    "V_unnormalized_partial",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL step204: {msg}")


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")
    schema = json.loads((BASE / "step204_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "xi_matrix_source_formula",
        "G_matrix_full",
        "c_matrix",
        "M_matrix",
        "xi_matrix_source_value",
        "xi_matrix_source_lower_bound",
        "xi_matrix_source_error",
        "xi_matrix_source_verdict",
        "robustness_table",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 204:
        fail("schema step must be 204")
    if schema["final_verdict"] not in ALLOWED:
        fail("invalid final verdict")
    if len(read_csv("G_matrix_step204.csv")) != 9:
        fail("G matrix must have 9 rows")
    if len(read_csv("c_matrix_step204.csv")) != 9:
        fail("c matrix must have 9 rows")
    if len(read_csv("M_matrix_step204.csv")) != 9:
        fail("M matrix must have 9 rows")
    derivation = (BASE / "xi_formula_derivation_step204.csv").read_text(encoding="utf-8")
    for token in ["full finite Hilbert-Schmidt residual requires H_ij", "compressed operator"]:
        if token not in derivation:
            fail(f"formula derivation missing {token}")
    citations = (BASE / "classical_theorems_cited_step204.csv").read_text(encoding="utf-8")
    for token in ["Step162", "Step177", "Burnol 2002", "Step173"]:
        if token not in citations:
            fail(f"citations missing {token}")
    tex = (BASE / "step204_unnormalized_xi_matrix_source.tex").read_text(encoding="utf-8")
    for token in ["tr}(G^{-1}H", "P_\\eta C_\\ell P_\\eta", "V\\_unnormalized\\_partial"]:
        if token not in tex:
            fail(f"tex missing {token}")
    output = (BASE / "compute_step204_output.txt").read_text(encoding="utf-8")
    if "verdict=V_unnormalized_partial" not in output:
        fail("compute output must record verdict")
    print("PASS step204 unnormalized Xi_matrix_source checks")


if __name__ == "__main__":
    main()
