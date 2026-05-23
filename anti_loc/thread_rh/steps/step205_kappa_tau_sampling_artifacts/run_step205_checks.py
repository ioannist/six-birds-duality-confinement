#!/usr/bin/env python3
"""Validate Step 205 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step205_kappa_tau_sampling_artifacts")
REQUIRED = [
    "step205_results_summary.md",
    "step205_schema.json",
    "content_classification_step205.csv",
    "nonclaim_boundary_step205.md",
    "step205_kappa_tau_sampling.tex",
    "derive_kappa_tau_step205.py",
    "compute_kappa_tau_samples_step205.py",
    "compute_c_matrix_step205.py",
    "compute_xi_decision_step205.py",
    "compute_step205_output.txt",
    "run_step205_checks.py",
    "kappa_tau_formula_derivation_step205.csv",
    "kappa_tau_samples_step205.csv",
    "c_matrix_step205.csv",
    "G_matrix_step205.csv",
    "xi_decision_step205.csv",
    "robustness_step205.csv",
    "residual_tree_step205.csv",
    "route_status_step205.csv",
    "construction_tasks_step205.csv",
    "classical_theorems_cited_step205.csv",
]
ALLOWED = {
    "V_kappa_tau_sampled_xi_closes",
    "V_kappa_tau_sampled_xi_nonzero",
    "V_kappa_tau_sampled_xi_inconclusive",
    "V_kappa_tau_sampled_partial",
    "V_kappa_tau_sampling_formula_corrected",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL step205: {msg}")


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")
    schema = json.loads((BASE / "step205_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "kappa_tau_formula_derivation",
        "kappa_tau_grid_values",
        "c_matrix",
        "G_matrix",
        "xi_matrix_source_value",
        "xi_matrix_source_error",
        "xi_matrix_source_verdict",
        "robustness_table",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["step"] != 205:
        fail("schema step must be 205")
    if schema["final_verdict"] not in ALLOWED:
        fail("invalid verdict")
    samples = read_csv("kappa_tau_samples_step205.csv")
    if len(samples) != 600:
        fail("kappa sample CSV must have 600 data rows")
    if len(read_csv("c_matrix_step205.csv")) != 9:
        fail("c matrix must have 9 rows")
    if len(read_csv("G_matrix_step205.csv")) != 9:
        fail("G matrix must have 9 rows")
    derivation = (BASE / "kappa_tau_formula_derivation_step205.csv").read_text(encoding="utf-8")
    if "missing" not in derivation or "candidate_shadow_not_certified_as_kappa" not in derivation:
        fail("derivation must record missing transport theorem")
    citations = (BASE / "classical_theorems_cited_step205.csv").read_text(encoding="utf-8")
    for token in ["Burnol 2002", "Step152", "Step153", "Step173"]:
        if token not in citations:
            fail(f"missing citation token {token}")
    tex = (BASE / "step205_kappa_tau_sampling.tex").read_text(encoding="utf-8")
    for token in ["V\\_kappa\\_tau\\_sampling\\_formula\\_corrected", "T_a^*", "candidate"]:
        if token not in tex:
            fail(f"tex missing {token}")
    output = (BASE / "compute_step205_output.txt").read_text(encoding="utf-8")
    if "verdict=V_kappa_tau_sampling_formula_corrected" not in output:
        fail("output must record verdict")
    print("PASS step205 kappa tau sampling checks")


if __name__ == "__main__":
    main()
