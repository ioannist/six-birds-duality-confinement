#!/usr/bin/env python3
"""Validate Step 177 SL164.1 attack artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step177_branch_b_SL164_attack_artifacts"
)

REQUIRED = [
    "step177_results_summary.md",
    "step177_schema.json",
    "content_classification_step177.csv",
    "nonclaim_boundary_step177.md",
    "step177_branch_b_SL164_attack.tex",
    "compute_c_ij_step177.py",
    "compute_c_ij_output_step177.txt",
    "run_step177_SL164_checks.py",
    "inherited_records_step177.csv",
    "derivation_chain_step177.csv",
    "projected_kernel_formula_step177.csv",
    "c_ij_numerical_step177.csv",
    "SL164_verdict_step177.csv",
    "branch_B_status_update_step177.csv",
    "residual_tree_step177.csv",
    "route_status_step177.csv",
    "construction_tasks_step177.csv",
]

ALLOWED = {
    "V_SL164_kernel_derived",
    "V_SL164_diagonal_nonzero",
    "V_SL164_off_diagonal_structure",
    "V_SL164_partial",
    "V_SL164_stuck_at_normalization",
    "V_SL164_target_equivalent",
}

FORBIDDEN = [
    r"\bthis is an RH proof\b",
    r"\bcloses Xi_BC\b",
    r"\bambient Hardy shadow is sufficient\b",
    r"\bpublic-shadow substitution accepted\b",
    r"\bretained no-gos are removed\b",
]


def fail(msg: str) -> None:
    print(f"FAIL step177 SL164 checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step177_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema JSON error: {exc}")
    if schema.get("step") != 177:
        fail("schema step must be 177")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("target") != "P_{L_a^Gamma} K_a^Gamma derivation + c_{ij}(l) evaluation":
        fail("schema target mismatch")
    for key in [
        "inherited_records",
        "derivation_chain",
        "projected_kernel_formula",
        "c_ij_numerical_values",
        "SL164_verdict",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    verdict = schema["SL164_verdict"]
    if verdict not in ALLOWED:
        fail(f"invalid SL164 verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal SL164_verdict")
    stages = {item["stage"] for item in schema["derivation_chain"]}
    if not {"T2a", "T2b", "T2c", "T2d"}.issubset(stages):
        fail("derivation_chain missing T2 stages")
    if verdict == "V_SL164_stuck_at_normalization":
        row = schema["c_ij_numerical_values"][0]
        if row.get("verdict") != "not_evaluable_missing_kappa":
            fail("stuck verdict must record missing kappa row")
        if "kappa" not in row.get("gap", ""):
            fail("blocking gap must name kappa")
    return schema


def check_csvs() -> None:
    for name in REQUIRED:
        if not name.endswith(".csv"):
            continue
        with (ROOT / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must have data rows")
    with (ROOT / "c_ij_numerical_step177.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if rows[0]["verdict"] != "not_evaluable_missing_kappa":
        fail("c_ij CSV must record not_evaluable_missing_kappa")


def check_tex_and_output() -> None:
    tex = text("step177_branch_b_SL164_attack.tex")
    snippets = [
        r"V\_SL164\_stuck\_at\_normalization",
        r"\kappa_{a,w}",
        "T2a",
        "T2b",
        "T2c",
        "T2d",
        "c_{11}",
        "not evaluable",
        "ambient Hardy shadow",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"tex missing snippet {snippet!r}")
    out = text("compute_c_ij_output_step177.txt")
    if "numerical_status=blocked_before_quadrature" not in out:
        fail("compute output must record blocked_before_quadrature")
    if "blocking_gap=missing explicit Mellin representative" not in out:
        fail("compute output must name blocking gap")


def check_forbidden() -> None:
    combined = "\n".join(text(name) for name in REQUIRED if name != "run_step177_SL164_checks.py")
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
    print("PASS step177 SL164 checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"SL164_verdict={schema['SL164_verdict']}")
    print("blocking_gap=kappa_{a,w}=T_a^*K_a^Gamma(.,w)")


if __name__ == "__main__":
    main()
