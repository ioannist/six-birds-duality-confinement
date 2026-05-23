#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step181_de_branges_pivot_artifacts")

REQUIRED = [
    "step181_results_summary.md",
    "step181_schema.json",
    "content_classification_step181.csv",
    "nonclaim_boundary_step181.md",
    "step181_de_branges_pivot.tex",
    "run_step181_de_branges_checks.py",
    "de_branges_declaration_step181.csv",
    "bridge_to_Xi_BC_step181.csv",
    "no_go_transfer_step181.csv",
    "cascade_initial_branches_step181.csv",
    "residual_tree_step181.csv",
    "route_status_step181.csv",
    "construction_tasks_step181.csv",
    "classical_theorems_cited_step181.csv",
]

ALLOWED_VERDICTS = {
    "V_dB_substantively_new",
    "V_dB_CTMT_instance",
    "V_dB_target_equivalent",
    "V_dB_partial",
    "V_dB_carrier_stuck_at_E",
}


def fail(msg: str) -> None:
    print(f"FAIL step181 de Branges checks: {msg}", file=sys.stderr)
    sys.exit(1)


def read_text(name: str) -> str:
    path = ROOT / name
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"could not read {name}: {exc}")


def read_csv_rows(name: str):
    path = ROOT / name
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except Exception as exc:
        fail(f"could not parse CSV {name}: {exc}")


def main() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing artifacts: " + ", ".join(missing))

    try:
        schema = json.loads(read_text("step181_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema JSON invalid: {exc}")

    if schema.get("step") != 181:
        fail("schema step must be 181")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("primary_carrier") != "de Branges spaces H(E_RH)":
        fail("schema primary_carrier mismatch")

    verdict = schema.get("dB_verdict")
    if verdict not in ALLOWED_VERDICTS:
        fail(f"dB_verdict not allowed: {verdict}")
    if schema.get("final_verdict") != verdict:
        fail("final_verdict must equal dB_verdict")
    if verdict != "V_dB_target_equivalent":
        fail("this dispatch must record V_dB_target_equivalent")

    e_def = schema.get("E_RH_definition", {})
    if e_def.get("status") != "conditional_target_equivalent":
        fail("E_RH_definition.status must be conditional_target_equivalent")
    if "Xi" not in e_def.get("candidate", ""):
        fail("E_RH candidate must mention Xi")

    retained = schema.get("retained_nogos", [])
    if not isinstance(retained, list) or len(retained) < 8:
        fail("retained_nogos must contain at least 8 entries")
    new_nogo = "de Branges RH-carrier closure target-equivalence / Conrey-Li survival"
    if new_nogo not in retained:
        fail("new de Branges no-go missing from retained_nogos")
    if schema.get("new_no_gos_count") != 1:
        fail("new_no_gos_count must be 1")

    branches = schema.get("cascade_initial_branches", [])
    branch_ids = {row.get("branch") for row in branches if isinstance(row, dict)}
    for expected in {"dB-E", "dB-chain", "dB-kernel", "dB-bridge"}:
        if expected not in branch_ids:
            fail(f"missing cascade branch {expected}")

    cited = " ".join(row.get("source", "") for row in schema.get("classical_theorems_cited", []))
    if "de Branges" not in cited or "Conrey-Li" not in cited:
        fail("classical_theorems_cited must include de Branges and Conrey-Li")

    for csv_name in [
        "de_branges_declaration_step181.csv",
        "bridge_to_Xi_BC_step181.csv",
        "no_go_transfer_step181.csv",
        "cascade_initial_branches_step181.csv",
        "residual_tree_step181.csv",
        "route_status_step181.csv",
        "construction_tasks_step181.csv",
        "classical_theorems_cited_step181.csv",
    ]:
        if not read_csv_rows(csv_name):
            fail(f"{csv_name} has no data rows")

    no_go_rows = read_csv_rows("no_go_transfer_step181.csv")
    if not any(row.get("no_go") == new_nogo and row.get("transfer_status") == "new" for row in no_go_rows):
        fail("no_go_transfer_step181.csv must record the new no-go")

    branch_rows = read_csv_rows("cascade_initial_branches_step181.csv")
    branch_csv_ids = {row.get("branch") for row in branch_rows}
    if not {"dB-E", "dB-chain", "dB-kernel", "dB-bridge"} <= branch_csv_ids:
        fail("cascade_initial_branches_step181.csv missing required branches")

    tex = read_text("step181_de_branges_pivot.tex")
    snippets = [
        r"V_\{\\dB\\_\\mathrm\{target\\_equivalent\}\}",
        "Hermite-Biehler",
        "K_E",
        r"\\XidB",
        "Conrey--Li",
        "target-equivalent",
        "dB-E",
        "dB-chain",
    ]
    for snippet in snippets:
        if not re.search(snippet, tex):
            fail(f"TeX missing required snippet: {snippet}")

    combined = "\n".join(
        read_text(name)
        for name in [
            "step181_results_summary.md",
            "nonclaim_boundary_step181.md",
            "step181_de_branges_pivot.tex",
        ]
    )
    forbidden = [
        r"\bthis is an RH proof\b",
        r"\bwe assume RH\b",
        r"\bassume the Riemann Hypothesis\b",
        r"\btherefore closes Xi_BC\b",
        r"\bde Branges proves RH\b",
        r"\bConrey-Li obstruction ignored\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step181 de Branges checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"dB_verdict={verdict}")
    print(f"new_no_gos_count={schema.get('new_no_gos_count')}")


if __name__ == "__main__":
    main()
