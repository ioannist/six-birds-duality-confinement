#!/usr/bin/env python3
"""Validate Step 179 Branch A Calkin attack artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step179_branch_a_calkin_attack_artifacts"
)

REQUIRED = [
    "step179_results_summary.md",
    "step179_schema.json",
    "content_classification_step179.csv",
    "nonclaim_boundary_step179.md",
    "step179_branch_a_calkin_attack.tex",
    "compute_branch_a_step179.py",
    "compute_branch_a_output_step179.txt",
    "run_step179_branch_a_checks.py",
    "inherited_records_step179.csv",
    "derivation_chain_step179.csv",
    "calkin_class_evidence_step179.csv",
    "branch_A_status_update_step179.csv",
    "residual_tree_step179.csv",
    "route_status_step179.csv",
    "construction_tasks_step179.csv",
]

ALLOWED = {
    "V_branch_a_calkin_compact",
    "V_branch_a_calkin_essential_nonzero",
    "V_branch_a_calkin_partial",
    "V_branch_a_stuck_at_kappa",
    "V_branch_a_stuck_at_specific_other_record",
    "V_branch_a_target_equivalent",
}

FORBIDDEN = [
    r"\bthis is an RH proof\b",
    r"\btherefore C_l P_eta is compact\b",
    r"\btherefore essential norm is positive\b",
    r"\bhard-support shadow proves\b",
    r"\bfinite-window evidence proves\b",
    r"\bretained no-gos are removed\b",
]


def fail(msg: str) -> None:
    print(f"FAIL step179 Branch A checks: {msg}", file=sys.stderr)
    sys.exit(1)


def text(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def check_files() -> None:
    for name in REQUIRED:
        path = ROOT / name
        if not path.exists():
            fail(f"missing {name}")
        if path.stat().st_size == 0:
            fail(f"empty {name}")


def check_schema() -> dict:
    try:
        schema = json.loads(text("step179_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema JSON error: {exc}")
    if schema.get("step") != 179:
        fail("schema step must be 179")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    for key in [
        "target",
        "inherited_records",
        "attack_pursued",
        "derivation_chain",
        "calkin_class_evidence",
        "calkin_class_verdict",
        "no_go_theorem",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    verdict = schema["calkin_class_verdict"]
    if verdict not in ALLOWED:
        fail(f"invalid verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal calkin_class_verdict")
    if verdict == "V_branch_a_stuck_at_kappa":
        if "kappa" not in schema["calkin_class_evidence"].get("blocking_equivalence", ""):
            fail("stuck-at-kappa verdict must name kappa blocking equivalence")
        statuses = {item["status"] for item in schema["derivation_chain"]}
        if not any("kappa" in status for status in statuses):
            fail("derivation statuses must include kappa blockage")
    return schema


def check_csvs() -> None:
    for name in REQUIRED:
        if not name.endswith(".csv"):
            continue
        with (ROOT / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must have data rows")
    with (ROOT / "calkin_class_evidence_step179.csv").open(newline="", encoding="utf-8") as handle:
        evidence = list(csv.DictReader(handle))
    if not any(row["status"] == "blocked_at_kappa" for row in evidence):
        fail("evidence CSV must record blocked_at_kappa")


def check_tex_and_output() -> None:
    tex = text("step179_branch_a_calkin_attack.tex")
    snippets = [
        r"V\_branch\_a\_stuck\_at\_kappa",
        r"\Cell\Peta",
        "T2a",
        "T2b",
        "T2c",
        "T2d",
        r"\|\Cell\Peta\|_{\mathrm{HS}}^2",
        "Branch A",
        r"\kappa",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"tex missing snippet {snippet!r}")
    out = text("compute_branch_a_output_step179.txt")
    if "verdict=V_branch_a_stuck_at_kappa" not in out:
        fail("compute output must record stuck-at-kappa verdict")
    if "T2a_matrix_elements=blocked_at_kappa" not in out:
        fail("compute output must record T2a blockage")


def check_forbidden() -> None:
    combined = "\n".join(text(name) for name in REQUIRED if name != "run_step179_branch_a_checks.py")
    for pattern in FORBIDDEN:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")


def main() -> None:
    if not ROOT.exists():
        fail(f"missing artifact directory {ROOT}")
    check_files()
    schema = check_schema()
    check_csvs()
    check_tex_and_output()
    check_forbidden()
    print("PASS step179 Branch A checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"calkin_class_verdict={schema['calkin_class_verdict']}")
    print("blocking_gap=kappa/P_eta projected Sonine kernel")


if __name__ == "__main__":
    main()
