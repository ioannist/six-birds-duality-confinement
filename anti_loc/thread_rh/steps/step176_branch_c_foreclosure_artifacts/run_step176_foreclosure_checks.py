#!/usr/bin/env python3
"""Validate Step 176 Branch C foreclosure artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step176_branch_c_foreclosure_artifacts"
)

REQUIRED = [
    "step176_results_summary.md",
    "step176_schema.json",
    "content_classification_step176.csv",
    "nonclaim_boundary_step176.md",
    "step176_branch_c_foreclosure.tex",
    "compute_L_confirmation_step176.py",
    "compute_L_confirmation_output_step176.txt",
    "run_step176_foreclosure_checks.py",
    "confirmation_data_points_step176.csv",
    "no_go_theorem_step176.csv",
    "branch_C_status_update_step176.csv",
    "retained_nogos_step176.csv",
    "residual_tree_step176.csv",
    "route_status_step176.csv",
    "construction_tasks_step176.csv",
]

ALLOWED = {
    "V_branch_c_foreclosed_generic",
    "V_branch_c_foreclosed_specific",
    "V_branch_c_partial",
    "V_branch_c_all_zero",
    "V_normalization_caveat",
}

FORBIDDEN = [
    r"\bthis is an RH proof\b",
    r"\btherefore closes Xi_BC\b",
    r"\bforecloses Xi_BC closure\b",
    r"\btherefore closes Branch A\b",
    r"\btherefore closes Branch B\b",
    r"\btherefore closes any Hecke branch\b",
    r"\bdoes not need retained no-gos\b",
]


def fail(msg: str) -> None:
    print(f"FAIL step176 foreclosure checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step176_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema JSON error: {exc}")
    if schema.get("step") != 176:
        fail("schema step must be 176")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    for key in [
        "confirmation_data_points",
        "no_go_theorem",
        "foreclosure_verdict",
        "retained_nogos",
        "new_no_go_count_after_this_step",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    verdict = schema["foreclosure_verdict"]
    if verdict not in ALLOWED:
        fail(f"invalid foreclosure verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal foreclosure_verdict")
    points = schema["confirmation_data_points"]
    if len(points) < 2:
        fail("at least two confirmation data points required")
    if verdict == "V_branch_c_foreclosed_generic":
        if schema["new_no_go_count_after_this_step"] != 1:
            fail("generic foreclosure should add one no-go")
        for point in points:
            if point.get("verdict") != "nonzero":
                fail("generic foreclosure requires all confirmation points nonzero")
            if float(point.get("lower_bound_abs", 0)) <= float(point.get("error_bound", 0)):
                fail("nonzero lower bound must dominate error bound")
    theorem = schema["no_go_theorem"]
    for key in ["statement", "scope", "nonclaim", "proof_sketch"]:
        if key not in theorem or not theorem[key]:
            fail(f"no_go_theorem missing {key}")
    return schema


def check_csvs() -> None:
    for name in REQUIRED:
        if not name.endswith(".csv"):
            continue
        with (ROOT / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must have data rows")
    with (ROOT / "confirmation_data_points_step176.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 3:
        fail("confirmation CSV must include three computed rows")
    for row in rows:
        if row["verdict"] != "nonzero":
            fail(f"confirmation row {row['case_id']} not nonzero")
        if float(row["lower_bound_abs"]) <= 1e-3:
            fail(f"confirmation row {row['case_id']} not separated from zero")


def check_tex_and_output() -> None:
    tex = text("step176_branch_c_foreclosure.tex")
    snippets = [
        r"V\_branch\_c\_foreclosed\_generic",
        "Branch C full-carrier ZI-COV(i) foreclosure",
        "0.16442101662000874",
        "-0.06557366346002169",
        "0.20421356560997495",
        "unitarily equivalent",
        "does not close",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"tex missing snippet {snippet!r}")
    out = text("compute_L_confirmation_output_step176.txt")
    for case in ["rho2_G_star", "rho3_G_star", "rho1_G_prime"]:
        if case not in out:
            fail(f"compute output missing {case}")
    if out.count("verdict=nonzero") < 3:
        fail("compute output must show three nonzero verdicts")


def check_forbidden() -> None:
    combined = "\n".join(text(name) for name in REQUIRED if name != "run_step176_foreclosure_checks.py")
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
    print("PASS step176 foreclosure checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"foreclosure_verdict={schema['foreclosure_verdict']}")
    print(f"new_no_go_count_after_this_step={schema['new_no_go_count_after_this_step']}")


if __name__ == "__main__":
    main()
