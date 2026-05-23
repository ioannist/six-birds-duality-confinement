#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step190_iwasawa_main_pivot_artifacts")

REQUIRED = [
    "step190_results_summary.md",
    "step190_schema.json",
    "content_classification_step190.csv",
    "nonclaim_boundary_step190.md",
    "step190_iwasawa_main_pivot.tex",
    "run_step190_iwasawa_checks.py",
    "iwasawa_declaration_step190.csv",
    "CRE_status_audit_step190.csv",
    "CRCFT_applicability_step190.csv",
    "framework_closure_audit_step190.csv",
    "cascade_initial_branches_step190.csv",
    "residual_tree_step190.csv",
    "route_status_step190.csv",
    "construction_tasks_step190.csv",
    "classical_theorems_cited_step190.csv",
]

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)

def read_csv_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).is_file()]
    if missing:
        fail(f"missing artifacts: {missing}")

    schema = json.loads((BASE / "step190_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "primary_carrier",
        "carrier_definition",
        "iwasawa_module",
        "p_adic_L_function",
        "characteristic_ideal",
        "parent_residual_on_IW",
        "CRE_status",
        "CRCFT_applicability",
        "framework_closure_status",
        "iwasawa_verdict",
        "classical_theorems_cited",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")

    if schema["step"] != 190:
        fail("schema step is not 190")
    if schema["orientation"] != "adequacy":
        fail("schema orientation is not adequacy")
    if schema["primary_carrier"] != "Iwasawa Main Conjecture (cyclotomic over Q)":
        fail("unexpected primary carrier")
    if schema["CRE_status"] != "not_CRE":
        fail("CRE_status must be not_CRE")
    if schema["CRCFT_applicability"] != "does_not_apply":
        fail("CRCFT_applicability must be does_not_apply")
    if schema["iwasawa_verdict"] != "V_iwasawa_closes":
        fail("iwasawa_verdict must be V_iwasawa_closes")
    if schema["final_verdict"] != schema["iwasawa_verdict"]:
        fail("final_verdict must equal iwasawa_verdict")
    if schema["framework_closure_status"].get("status") != "closed_native_iwasawa":
        fail("closure status must be closed_native_iwasawa")
    if schema["framework_closure_status"].get("does_not_transfer_to_RH") is not True:
        fail("schema must mark no transfer to RH")
    if "main_conjecture_equality" not in schema["characteristic_ideal"]:
        fail("characteristic_ideal missing main_conjecture_equality")

    cited = " ".join(item.get("source", "") for item in schema["classical_theorems_cited"])
    for token in ["Iwasawa", "Kubota-Leopoldt", "Mazur-Wiles 1984", "Wiles 1990", "Skinner-Urban 2014"]:
        if token not in cited:
            fail(f"classical citation missing {token}")

    tex = (BASE / "step190_iwasawa_main_pivot.tex").read_text(encoding="utf-8")
    for snippet in [
        "V_{\\mathrm{iwasawa\\_closes}}",
        "\\LambdaIW",
        "X_\\infty",
        "L_p(\\chi)",
        "\\XiIW=0",
        "Mazur--Wiles",
        "not \\(\\CRE\\)",
        "does not apply",
        "does not prove Riemann RH",
    ]:
        if snippet not in tex:
            fail(f"TeX missing required snippet: {snippet}")

    forbidden = [
        "therefore proves Riemann",
        "therefore transfers",
        "Iwasawa implies Riemann RH",
        "closes Xi_BC",
        "proves Xi_BC",
        "weakens the retained no-go",
    ]
    all_text = "\n".join((BASE / name).read_text(encoding="utf-8", errors="ignore") for name in REQUIRED if (BASE / name).suffix in {".md", ".tex", ".json", ".csv"})
    lowered = all_text.lower()
    for phrase in forbidden:
        if phrase.lower() in lowered:
            fail(f"forbidden phrase found: {phrase}")

    for csv_name in [
        "iwasawa_declaration_step190.csv",
        "CRE_status_audit_step190.csv",
        "CRCFT_applicability_step190.csv",
        "framework_closure_audit_step190.csv",
        "cascade_initial_branches_step190.csv",
        "residual_tree_step190.csv",
        "route_status_step190.csv",
        "construction_tasks_step190.csv",
        "classical_theorems_cited_step190.csv",
    ]:
        rows = read_csv_rows(BASE / csv_name)
        if not rows:
            fail(f"{csv_name} has no data rows")

    cre_rows = read_csv_rows(BASE / "CRE_status_audit_step190.csv")
    if not any(row.get("result") == "not_CRE" for row in cre_rows):
        fail("CRE_status_audit lacks not_CRE result")

    closure_rows = read_csv_rows(BASE / "framework_closure_audit_step190.csv")
    if not any(row.get("component") == "main_conjecture_equality" and row.get("status") == "closed" for row in closure_rows):
        fail("framework_closure_audit lacks closed main_conjecture_equality")

    print("PASS step190_iwasawa_checks: all required artifacts and fields validated")

if __name__ == "__main__":
    main()

