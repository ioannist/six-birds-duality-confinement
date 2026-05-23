#!/usr/bin/env python3
"""Validate Step 202 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts")
REQUIRED = [
    "step202_results_summary.md",
    "step202_schema.json",
    "content_classification_step202.csv",
    "nonclaim_boundary_step202.md",
    "step202_xi_matrix_source_numerical.tex",
    "compute_E_half_step202.py",
    "compute_xi_matrix_source_step202.py",
    "compute_step202_output.txt",
    "run_step202_checks.py",
    "E_half_values_step202.csv",
    "G_matrix_step202.csv",
    "c_matrix_step202.csv",
    "xi_matrix_source_decision_step202.csv",
    "robustness_step202.csv",
    "residual_tree_step202.csv",
    "route_status_step202.csv",
    "construction_tasks_step202.csv",
    "classical_theorems_cited_step202.csv",
]
ALLOWED = {
    "V_xi_matrix_source_closes",
    "V_xi_matrix_source_nonzero",
    "V_xi_matrix_source_inconclusive",
    "V_xi_matrix_source_partial",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL step202: {msg}")


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step202_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "E_half_values",
        "G_matrix",
        "c_matrix",
        "xi_matrix_source_value",
        "xi_matrix_source_error",
        "xi_matrix_source_verdict",
        "robustness_table",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 202:
        fail("schema step must be 202")
    if schema["final_verdict"] not in ALLOWED:
        fail("invalid final verdict")

    e_rows = read_csv("E_half_values_step202.csv")
    if len(e_rows) != 6:
        fail("E_half_values_step202.csv must have 6 rows")
    g_rows = read_csv("G_matrix_step202.csv")
    if len(g_rows) != 9:
        fail("G_matrix_step202.csv must have 9 rows")
    c_rows = read_csv("c_matrix_step202.csv")
    if len(c_rows) != 27:
        fail("c_matrix_step202.csv must have 27 rows for 3 ell values")
    decision_text = (BASE / "xi_matrix_source_decision_step202.csv").read_text(encoding="utf-8")
    if "literal_K_rho_j_rho_i_diagonal_zero" not in decision_text:
        fail("decision must record diagonal-status blocker")
    citations = (BASE / "classical_theorems_cited_step202.csv").read_text(encoding="utf-8")
    for token in ["Burnol 2002", "Theorem 4", "Theorem 8", "equation 1", "Burnol 2004", "Theorem 6.10"]:
        if token not in citations:
            fail(f"missing citation token {token}")
    tex = (BASE / "step202_xi_matrix_source_numerical.tex").read_text(encoding="utf-8")
    for token in ["E_{1/2}", "G_{ij}", "c_{ij}", "V\\_xi\\_matrix\\_source\\_partial"]:
        if token not in tex:
            fail(f"tex missing {token}")
    output = (BASE / "compute_step202_output.txt").read_text(encoding="utf-8")
    if "Xi_matrix_source verdict" not in output:
        fail("compute output must contain Xi verdict")
    print("PASS step202 Xi_matrix_source numerical checks")


if __name__ == "__main__":
    main()
