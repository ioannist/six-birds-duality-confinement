#!/usr/bin/env python3
"""Validate Step 178 kappa derivation artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step178_kappa_derivation_artifacts"
)

REQUIRED = [
    "step178_results_summary.md",
    "step178_schema.json",
    "content_classification_step178.csv",
    "nonclaim_boundary_step178.md",
    "step178_kappa_derivation.tex",
    "compute_kappa_step178.py",
    "run_step178_kappa_checks.py",
    "inherited_records_step178.csv",
    "derivation_chain_step178.csv",
    "kappa_sample_values_step178.csv",
    "c_ij_attempt_step178.csv",
    "branch_B_status_update_step178.csv",
    "residual_tree_step178.csv",
    "route_status_step178.csv",
    "construction_tasks_step178.csv",
]

OPTIONAL_RUN_OUTPUT = "compute_kappa_output_step178.txt"

ALLOWED = {
    "V_kappa_closed_form",
    "V_kappa_operational",
    "V_kappa_spectral",
    "V_kappa_partial",
    "V_kappa_classical_theorem_needed",
    "V_kappa_target_equivalent",
}

FORBIDDEN = [
    r"\bthis is an RH proof\b",
    r"\bcloses Xi_BC\b",
    r"\bambient Hardy kernel is sufficient\b",
    r"\bcomputed from the ambient Hardy kernel shadow\b",
    r"\bretained no-gos are removed\b",
]


def fail(msg: str) -> None:
    print(f"FAIL step178 kappa checks: {msg}", file=sys.stderr)
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
    out = ROOT / OPTIONAL_RUN_OUTPUT
    if not out.exists() or out.stat().st_size == 0:
        fail(f"missing run output {OPTIONAL_RUN_OUTPUT}")


def check_schema() -> dict:
    try:
        schema = json.loads(text("step178_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema JSON error: {exc}")
    if schema.get("step") != 178:
        fail("schema step must be 178")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    for key in [
        "target",
        "inherited_records",
        "attack_pursued",
        "derivation_chain",
        "classical_theorems_cited",
        "kappa_formula",
        "kappa_sample_values",
        "kappa_verdict",
        "c_11_log_2",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    verdict = schema["kappa_verdict"]
    if verdict not in ALLOWED:
        fail(f"invalid kappa verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal kappa_verdict")
    if verdict == "V_kappa_classical_theorem_needed":
        needed = [t for t in schema["classical_theorems_cited"] if t.get("status") == "needed_missing"]
        if not needed:
            fail("classical theorem needed verdict must name needed theorem")
        if "Bessel/Hankel" not in needed[0].get("name", ""):
            fail("needed theorem must name Bessel/Hankel projection theorem")
        if schema["kappa_formula"] is not None:
            fail("stuck verdict must not claim a derived kappa formula")
    return schema


def check_csvs() -> None:
    for name in REQUIRED:
        if not name.endswith(".csv"):
            continue
        with (ROOT / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must have data rows")
    with (ROOT / "kappa_sample_values_step178.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 7:
        fail("sample values CSV must include requested tau grid")
    if any(row["status"] != "not_computed_classical_projection_theorem_needed" for row in rows):
        fail("sample rows must record classical theorem blockage")
    with (ROOT / "c_ij_attempt_step178.csv").open(newline="", encoding="utf-8") as handle:
        c_rows = list(csv.DictReader(handle))
    if c_rows[0]["status"] != "not_attempted_kappa_unavailable":
        fail("c_ij attempt must be blocked by unavailable kappa")


def check_tex_and_output() -> None:
    tex = text("step178_kappa_derivation.tex")
    snippets = [
        r"V\_kappa\_classical\_theorem\_needed",
        "Attack A",
        "Attack B",
        "Attack C",
        "Burnol's explicit Bessel/Hankel resolvent formula",
        "No sample values are lawfully computed",
        "not substitute the ambient Hardy kernel",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"tex missing snippet {snippet!r}")
    out = text(OPTIONAL_RUN_OUTPUT)
    if "status=blocked_before_numeric_evaluation" not in out:
        fail("compute output must record blocked status")
    if "Bessel/Hankel resolvent" not in out:
        fail("compute output must name theorem gap")


def check_forbidden() -> None:
    combined = "\n".join(text(name) for name in REQUIRED if name != "run_step178_kappa_checks.py")
    combined += "\n" + text(OPTIONAL_RUN_OUTPUT)
    for pattern in FORBIDDEN:
        if re.search(pattern, combined, flags=re.IGNORECASE | re.DOTALL):
            fail(f"forbidden phrase matched: {pattern}")


def main() -> None:
    if not ROOT.exists():
        fail(f"missing artifact directory {ROOT}")
    check_files()
    schema = check_schema()
    check_csvs()
    check_tex_and_output()
    check_forbidden()
    print("PASS step178 kappa checks")
    print(f"artifacts_checked={len(REQUIRED) + 1}")
    print(f"kappa_verdict={schema['kappa_verdict']}")
    print("needed_theorem=Burnol Bessel/Hankel resolvent for P_{L_a^Gamma}")


if __name__ == "__main__":
    main()
