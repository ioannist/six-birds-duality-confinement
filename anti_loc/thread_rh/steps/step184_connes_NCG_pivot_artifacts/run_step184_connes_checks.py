#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step184_connes_NCG_pivot_artifacts")

REQUIRED = [
    "step184_results_summary.md",
    "step184_schema.json",
    "content_classification_step184.csv",
    "nonclaim_boundary_step184.md",
    "step184_connes_NCG_pivot.tex",
    "run_step184_connes_checks.py",
    "connes_declaration_step184.csv",
    "no_go_transfer_step184.csv",
    "CRCFT_mode_audit_step184.csv",
    "cascade_initial_branches_step184.csv",
    "residual_tree_step184.csv",
    "route_status_step184.csv",
    "construction_tasks_step184.csv",
    "classical_theorems_cited_step184.csv",
    "CRCFT_coverage_status_step184.csv",
]

EXPECTED_VERDICT = "V_connes_CRCFT_TE"


def fail(msg: str) -> None:
    print(f"FAIL step184 Connes checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step184_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 184:
        fail("schema step must be 184")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("primary_carrier") != "Connes adelic / NCG carrier":
        fail("primary_carrier mismatch")
    if schema.get("connes_verdict") != EXPECTED_VERDICT:
        fail("connes_verdict must be V_connes_CRCFT_TE")
    if schema.get("final_verdict") != EXPECTED_VERDICT:
        fail("final_verdict must equal connes_verdict")
    if schema.get("CRCFT_coverage_conjecture_status") != "strengthens":
        fail("coverage status must be strengthens")

    classification = schema.get("CRCFT_mode_classification", {})
    if "not primary" not in classification.get("T3a_CTMT", ""):
        fail("T3a CTMT audit missing or wrong")
    if not classification.get("T3b_TE", "").startswith("yes"):
        fail("T3b TE audit must be yes")
    if "none" not in classification.get("T3d_non_CRCFT", ""):
        fail("T3d non-CRCFT audit must find none")

    new_nogo = "Connes adelic trace-formula full closure target-equivalence / completed spectral ledger not inherited"
    retained = schema.get("retained_nogos", [])
    if new_nogo not in retained:
        fail("new Connes no-go missing from retained_nogos")
    if len(retained) < 10:
        fail("retained_nogos must contain at least 10 entries")
    if schema.get("new_no_gos_count") != 1:
        fail("new_no_gos_count must be 1")

    cited = " ".join(row.get("source", "") for row in schema.get("classical_theorems_cited", []))
    for expected in ["Connes 1999", "Meyer", "Deninger", "Step 93", "Steps 99-100"]:
        if expected not in cited:
            fail(f"classical/inherited citation missing {expected}")

    for csv_name in [
        "connes_declaration_step184.csv",
        "no_go_transfer_step184.csv",
        "CRCFT_mode_audit_step184.csv",
        "cascade_initial_branches_step184.csv",
        "residual_tree_step184.csv",
        "route_status_step184.csv",
        "construction_tasks_step184.csv",
        "classical_theorems_cited_step184.csv",
        "CRCFT_coverage_status_step184.csv",
    ]:
        if not rows(csv_name):
            fail(f"{csv_name} has no data rows")

    audit_rows = {row.get("audit_item"): row for row in rows("CRCFT_mode_audit_step184.csv")}
    for item in ["T3a_CTMT", "T3b_TE", "T3c_BF", "T3d_non_CRCFT_route"]:
        if item not in audit_rows:
            fail(f"CRCFT_mode_audit missing {item}")

    no_go_rows = rows("no_go_transfer_step184.csv")
    if not any(row.get("no_go") == new_nogo and row.get("transfer_status") == "new" for row in no_go_rows):
        fail("no_go_transfer must record new Connes no-go")

    tex = text("step184_connes_NCG_pivot.tex")
    snippets = [
        "V_{\\mathrm{connes\\_CRCFT\\_TE}}",
        "X_\\Q=\\A_\\Q/\\Q^*",
        "C_\\Q=\\A_\\Q^*/\\Q^*",
        "Xi_{\\mathrm{Connes}}",
        "Connes target-equivalence no-go",
        "CRCFT\\_coverage\\_conjecture\\_status",
        "not primary",
        "none found",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    combined = "\n".join(
        text(name)
        for name in [
            "step184_results_summary.md",
            "nonclaim_boundary_step184.md",
            "step184_connes_NCG_pivot.tex",
        ]
    )
    forbidden = [
        r"\bthis proves RH\b",
        r"\bConnes proves RH here\b",
        r"\bwe assume RH\b",
        r"\bcompleted Connes spectral ledger is constructed\b",
        r"\bCRCFT coverage conjecture is proved\b",
        r"\bcloses Xi_Connes\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step184 Connes checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"connes_verdict={schema.get('connes_verdict')}")
    print(f"new_no_gos_count={schema.get('new_no_gos_count')}")
    print(f"CRCFT_coverage_conjecture_status={schema.get('CRCFT_coverage_conjecture_status')}")


if __name__ == "__main__":
    main()
