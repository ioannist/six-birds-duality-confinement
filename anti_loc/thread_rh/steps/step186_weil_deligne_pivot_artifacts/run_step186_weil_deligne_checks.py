#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step186_weil_deligne_pivot_artifacts")

REQUIRED = [
    "step186_results_summary.md",
    "step186_schema.json",
    "content_classification_step186.csv",
    "nonclaim_boundary_step186.md",
    "step186_weil_deligne_pivot.tex",
    "run_step186_weil_deligne_checks.py",
    "weil_deligne_declaration_step186.csv",
    "CRE_status_audit_step186.csv",
    "CRCFT_applicability_step186.csv",
    "framework_closure_audit_step186.csv",
    "cascade_initial_branches_step186.csv",
    "residual_tree_step186.csv",
    "route_status_step186.csv",
    "construction_tasks_step186.csv",
    "classical_theorems_cited_step186.csv",
]

EXPECTED_VERDICT = "V_weil_deligne_closes"


def fail(msg: str) -> None:
    print(f"FAIL step186 Weil-Deligne checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step186_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 186:
        fail("schema step must be 186")
    if schema.get("orientation") != "adequacy":
        fail("orientation must be adequacy")
    if schema.get("primary_carrier") != "function-field RH (Weil/Deligne) on smooth projective X / F_q":
        fail("primary_carrier mismatch")
    if schema.get("weil_deligne_verdict") != EXPECTED_VERDICT:
        fail("weil_deligne_verdict mismatch")
    if schema.get("final_verdict") != EXPECTED_VERDICT:
        fail("final_verdict mismatch")
    if schema.get("CRE_status") != "not_CRE":
        fail("CRE_status must be not_CRE")
    if schema.get("CRCFT_applicability") != "does_not_apply":
        fail("CRCFT_applicability must be does_not_apply")

    closure = schema.get("framework_closure_status", {})
    if closure.get("status") != "closed_native_weil_deligne":
        fail("framework_closure_status.status must be closed_native_weil_deligne")
    if "0 by Deligne purity" not in closure.get("Xi_WD", ""):
        fail("Xi_WD closure statement must cite Deligne purity")
    if not closure.get("does_not_transfer_to_RH"):
        fail("closure must explicitly not transfer to RH")

    carrier = schema.get("carrier_definition", {})
    if "H^i_et" not in carrier.get("carrier", ""):
        fail("carrier definition must mention H^i_et")

    frob = schema.get("frobenius_operator", {})
    if "alpha" not in frob.get("eigenvalues", ""):
        fail("Frobenius eigenvalues not recorded")

    cited = " ".join(row.get("source", "") for row in schema.get("classical_theorems_cited", []))
    for expected in ["Weil 1948", "Weil 1949", "Grothendieck 1965", "Deligne 1973", "Deligne 1980"]:
        if expected not in cited:
            fail(f"citation missing {expected}")

    if len(schema.get("retained_nogos", [])) < 10:
        fail("retained_nogos must preserve the 10 inherited no-gos")

    for csv_name in [
        "weil_deligne_declaration_step186.csv",
        "CRE_status_audit_step186.csv",
        "CRCFT_applicability_step186.csv",
        "framework_closure_audit_step186.csv",
        "cascade_initial_branches_step186.csv",
        "residual_tree_step186.csv",
        "route_status_step186.csv",
        "construction_tasks_step186.csv",
        "classical_theorems_cited_step186.csv",
    ]:
        if not rows(csv_name):
            fail(f"{csv_name} has no data rows")

    cre_rows = {row.get("audit_item"): row for row in rows("CRE_status_audit_step186.csv")}
    if cre_rows.get("CRE_status", {}).get("result") != "not_CRE":
        fail("CRE status CSV must record not_CRE")

    crcft_rows = {row.get("audit_item"): row for row in rows("CRCFT_applicability_step186.csv")}
    if crcft_rows.get("CRCFT_scope", {}).get("result") != "does_not_apply":
        fail("CRCFT applicability CSV must record does_not_apply")

    closure_rows = {row.get("component"): row for row in rows("framework_closure_audit_step186.csv")}
    if closure_rows.get("weight_residual_Xi_WD", {}).get("status") != "closed":
        fail("framework closure CSV must close weight_residual_Xi_WD")

    tex = text("step186_weil_deligne_pivot.tex")
    snippets = [
        "V_{\\mathrm{weil\\_deligne\\_closes}}",
        "H_{\\mathrm{WD}}",
        "Frob",
        "Grothendieck--Lefschetz",
        "\\XiWD=0",
        "Deligne",
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
            "step186_results_summary.md",
            "nonclaim_boundary_step186.md",
            "step186_weil_deligne_pivot.tex",
        ]
    )
    forbidden = [
        r"\bproves Riemann RH\b",
        r"\btransfers function-field RH to the number-field\b",
        r"\bconstructs a number-field cohomology\b",
        r"\bcloses Xi_BC\b",
        r"\bCRCFT coverage conjecture is proved\b",
        r"\bweakens retained no-go\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step186 Weil-Deligne checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"weil_deligne_verdict={schema.get('weil_deligne_verdict')}")
    print(f"CRE_status={schema.get('CRE_status')}")
    print(f"CRCFT_applicability={schema.get('CRCFT_applicability')}")
    print(f"framework_closure_status={closure.get('status')}")


if __name__ == "__main__":
    main()
