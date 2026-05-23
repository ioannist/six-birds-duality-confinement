#!/usr/bin/env python3
"""Validate Step 203 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step203_diagonal_gram_correction_artifacts")
REQUIRED = [
    "step203_results_summary.md",
    "step203_schema.json",
    "content_classification_step203.csv",
    "nonclaim_boundary_step203.md",
    "step203_diagonal_gram_correction.tex",
    "compute_E_prime_half_step203.py",
    "compute_G_corrected_step203.py",
    "compute_xi_matrix_source_corrected_step203.py",
    "compute_step203_output.txt",
    "run_step203_checks.py",
    "L_Hopital_derivation_step203.csv",
    "E_prime_half_values_step203.csv",
    "G_diagonal_corrected_step203.csv",
    "G_matrix_full_step203.csv",
    "c_matrix_corrected_step203.csv",
    "xi_matrix_source_corrected_decision_step203.csv",
    "robustness_step203.csv",
    "residual_tree_step203.csv",
    "route_status_step203.csv",
    "construction_tasks_step203.csv",
    "classical_theorems_cited_step203.csv",
]
ALLOWED = {
    "V_diagonal_corrected_xi_closes",
    "V_diagonal_corrected_xi_nonzero",
    "V_diagonal_corrected_xi_inconclusive",
    "V_diagonal_corrected_dual_system_check_fails",
    "V_diagonal_corrected_partial",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL step203: {msg}")


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")
    schema = json.loads((BASE / "step203_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "L_Hopital_diagonal_formula",
        "dual_system_cross_check_status",
        "E_prime_half_values",
        "G_diagonal_corrected",
        "G_matrix_full",
        "c_matrix",
        "xi_matrix_source_value",
        "xi_matrix_source_error",
        "robustness",
        "sign_convention_resolved",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 203:
        fail("schema step must be 203")
    if schema["final_verdict"] not in ALLOWED:
        fail("invalid final verdict")
    if len(read_csv("E_prime_half_values_step203.csv")) != 3:
        fail("E_prime values must have 3 rows")
    if len(read_csv("G_diagonal_corrected_step203.csv")) != 3:
        fail("G diagonal must have 3 rows")
    if len(read_csv("G_matrix_full_step203.csv")) != 9:
        fail("full G matrix must have 9 rows")
    if len(read_csv("c_matrix_corrected_step203.csv")) != 9:
        fail("c matrix must have 9 rows")
    derivation = (BASE / "L_Hopital_derivation_step203.csv").read_text(encoding="utf-8")
    if "2 Re(conj(E(w))E'(w))" not in derivation:
        fail("L'Hopital derivation must contain corrected conjugate formula")
    citations = (BASE / "classical_theorems_cited_step203.csv").read_text(encoding="utf-8")
    for token in ["Burnol 2002", "equation 1", "Theorem 8", "Burnol 2004", "Theorem 3.1", "Theorem 3.2"]:
        if token not in citations:
            fail(f"missing citation token {token}")
    tex = (BASE / "step203_diagonal_gram_correction.tex").read_text(encoding="utf-8")
    for token in ["K(\\overline w,w)", "E'_{1/2}", "V\\_diagonal\\_corrected\\_xi\\_inconclusive"]:
        if token not in tex:
            fail(f"tex missing {token}")
    output = (BASE / "compute_step203_output.txt").read_text(encoding="utf-8")
    if "Xi_matrix_source verdict" not in output:
        fail("compute output must contain Xi verdict")
    print("PASS step203 diagonal Gram correction checks")


if __name__ == "__main__":
    main()
