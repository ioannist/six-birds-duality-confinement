#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step185_selberg_maass_pivot_artifacts")

REQUIRED = [
    "step185_results_summary.md",
    "step185_schema.json",
    "content_classification_step185.csv",
    "nonclaim_boundary_step185.md",
    "step185_selberg_maass_pivot.tex",
    "run_step185_selberg_checks.py",
    "selberg_declaration_step185.csv",
    "CRE_status_audit_step185.csv",
    "CRCFT_applicability_step185.csv",
    "framework_closure_audit_step185.csv",
    "cascade_initial_branches_step185.csv",
    "residual_tree_step185.csv",
    "route_status_step185.csv",
    "construction_tasks_step185.csv",
    "classical_theorems_cited_step185.csv",
]

EXPECTED_VERDICT = "V_selberg_closes_with_proved_RH"


def fail(msg: str) -> None:
    print(f"FAIL step185 Selberg checks: {msg}", file=sys.stderr)
    sys.exit(1)


def text(name: str) -> str:
    try:
        return (ROOT / name).read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"could not read {name}: {exc}")


def rows(name: str):
    try:
        with (ROOT / name).open(newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except Exception as exc:
        fail(f"could not parse {name}: {exc}")


def main() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing artifacts: " + ", ".join(missing))

    try:
        schema = json.loads(text("step185_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 185:
        fail("schema step must be 185")
    if schema.get("orientation") != "adequacy":
        fail("orientation must be adequacy")
    if schema.get("primary_carrier") != "Selberg trace formula / Maass forms on SL_2(Z)":
        fail("primary_carrier mismatch")
    if schema.get("selberg_verdict") != EXPECTED_VERDICT:
        fail("selberg_verdict mismatch")
    if schema.get("final_verdict") != EXPECTED_VERDICT:
        fail("final_verdict mismatch")
    if schema.get("CRE_status") != "not_CRE":
        fail("CRE_status must be not_CRE")
    if schema.get("CRCFT_applicability") != "does_not_apply":
        fail("CRCFT_applicability must be does_not_apply")

    closure = schema.get("framework_closure_status", {})
    if closure.get("status") != "closed_native_selberg":
        fail("framework_closure_status.status must be closed_native_selberg")
    if closure.get("Xi_Gamma") != "0 after the full native Selberg trace ledger is included":
        fail("Xi_Gamma closure statement mismatch")
    if not closure.get("does_not_transfer_to_RH"):
        fail("closure must explicitly not transfer to RH")

    cited = " ".join(row.get("source", "") for row in schema.get("classical_theorems_cited", []))
    for expected in ["Selberg 1956", "Hejhal", "Iwaniec", "Step 90", "Step 92"]:
        if expected not in cited:
            fail(f"citation missing {expected}")

    if len(schema.get("retained_nogos", [])) < 10:
        fail("retained_nogos must preserve the 10 inherited no-gos")

    for csv_name in [
        "selberg_declaration_step185.csv",
        "CRE_status_audit_step185.csv",
        "CRCFT_applicability_step185.csv",
        "framework_closure_audit_step185.csv",
        "cascade_initial_branches_step185.csv",
        "residual_tree_step185.csv",
        "route_status_step185.csv",
        "construction_tasks_step185.csv",
        "classical_theorems_cited_step185.csv",
    ]:
        if not rows(csv_name):
            fail(f"{csv_name} has no data rows")

    cre_rows = {row.get("audit_item"): row for row in rows("CRE_status_audit_step185.csv")}
    if cre_rows.get("CRE_status", {}).get("result") != "not_CRE":
        fail("CRE status CSV must record not_CRE")

    crcft_rows = {row.get("audit_item"): row for row in rows("CRCFT_applicability_step185.csv")}
    if crcft_rows.get("CRCFT_scope", {}).get("result") != "does_not_apply":
        fail("CRCFT applicability CSV must record does_not_apply")

    closure_rows = {row.get("component"): row for row in rows("framework_closure_audit_step185.csv")}
    if closure_rows.get("Schur_residual_Xi_Gamma", {}).get("status") != "closed":
        fail("framework closure CSV must close Schur_residual_Xi_Gamma")

    tex = text("step185_selberg_maass_pivot.tex")
    snippets = [
        "V_{\\mathrm{selberg\\_closes\\_with\\_proved\\_RH}}",
        "H_\\Gamma=L^2",
        "\\Delta=-y^2",
        "Z_{\\Gamma}",
        "\\XiGamma=0",
        "not \\(\\CRE\\)",
        "does not apply",
        "does not prove Riemann RH",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    combined = "\n".join(
        text(name)
        for name in [
            "step185_results_summary.md",
            "nonclaim_boundary_step185.md",
            "step185_selberg_maass_pivot.tex",
        ]
    )
    forbidden = [
        r"\bproves Riemann RH\b",
        r"\btransfers Selberg.*to Riemann RH\b",
        r"\bcloses Xi_BC\b",
        r"\bCRCFT coverage conjecture is proved\b",
        r"\bweakens retained no-go\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step185 Selberg checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"selberg_verdict={schema.get('selberg_verdict')}")
    print(f"CRE_status={schema.get('CRE_status')}")
    print(f"CRCFT_applicability={schema.get('CRCFT_applicability')}")
    print(f"framework_closure_status={closure.get('status')}")


if __name__ == "__main__":
    main()
