#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step201_burnol_kappa_operationalization_artifacts")

REQUIRED = [
    "step201_results_summary.md",
    "step201_schema.json",
    "content_classification_step201.csv",
    "nonclaim_boundary_step201.md",
    "step201_burnol_kappa_operationalization.tex",
    "derive_kappa_step201.py",
    "compute_kappa_output_step201.txt",
    "run_step201_checks.py",
    "inherited_records_step201.csv",
    "burnol_2002_theorem_4_formula_step201.csv",
    "burnol_2002_theorem_8_E_function_step201.csv",
    "branch_A_attack_vectors_step201.csv",
    "branch_B_SL164_reattempt_step201.csv",
    "CTMT_instance_reevaluation_step201.csv",
    "residual_tree_step201.csv",
    "route_status_step201.csv",
    "construction_tasks_step201.csv",
    "classical_theorems_cited_step201.csv",
]

VALID_FINAL = {
    "V_kappa_inherited_both_close",
    "V_kappa_inherited_branch_A_closes",
    "V_kappa_inherited_branch_B_closes",
    "V_kappa_inherited_branch_AB_attempted",
    "V_kappa_inherited_neither_closes",
    "V_kappa_inherited_partial",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def read_csv(name: str):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step201_schema.json").read_text())
    if schema.get("step") != 201:
        fail("step must be 201")
    if schema.get("orientation") != "adequacy":
        fail("orientation must be adequacy")
    if schema.get("final_verdict") not in VALID_FINAL:
        fail("invalid final verdict")
    if "Burnol 2002/2004" not in schema.get("kappa_status", ""):
        fail("schema must mark kappa inherited via Burnol 2002/2004")
    if len(schema.get("inherited_records_I1_to_I6", [])) != 6:
        fail("schema must list I1-I6")
    if schema.get("branch_A_reattempt_verdict", {}).get("closure") is not False:
        fail("Branch A closure status should be false for this verdict")
    if schema.get("branch_B_reattempt_verdict", {}).get("closure") is not False:
        fail("Branch B closure status should be false for this verdict")

    records = read_csv("inherited_records_step201.csv")
    if len(records) != 6:
        fail("inherited records CSV must have 6 rows")
    for token in ["I1", "I2", "I3", "I4", "I5", "I6"]:
        if not any(row["id"] == token for row in records):
            fail(f"missing inherited record {token}")

    citations = (BASE / "classical_theorems_cited_step201.csv").read_text()
    for token in ["Burnol 2002", "Theorem 4", "Theorem 8", "Burnol 2004", "Theorem 6.10"]:
        if token not in citations:
            fail(f"missing citation token {token}")

    branch_a = read_csv("branch_A_attack_vectors_step201.csv")
    if len(branch_a) < 4:
        fail("Branch A attack vector CSV must have at least 4 rows")
    branch_b = (BASE / "branch_B_SL164_reattempt_step201.csv").read_text()
    for token in ["kappa_vector", "kernel_gram", "commutator_matrix", "Xi_matrix_source"]:
        if token not in branch_b:
            fail(f"Branch B CSV missing {token}")

    tex = (BASE / "step201_burnol_kappa_operationalization.tex").read_text()
    for token in [
        "V\\_kappa\\_inherited\\_branch\\_AB\\_attempted",
        "Burnol 2002",
        "Theorem 4",
        "E_\\lambda",
        "\\kappa_{a,w,k}",
        "Branch A",
        "Branch B",
    ]:
        if token not in tex:
            fail(f"tex missing token {token}")

    output = (BASE / "compute_kappa_output_step201.txt").read_text()
    for token in ["kappa_formula", "branch_B_Gram", "Branch_A_status", "rho_1"]:
        if token not in output:
            fail(f"derive output missing {token}")

    print("PASS step201 Burnol kappa operationalization checks")
    print(f"verdict={schema['final_verdict']}")


if __name__ == "__main__":
    main()

