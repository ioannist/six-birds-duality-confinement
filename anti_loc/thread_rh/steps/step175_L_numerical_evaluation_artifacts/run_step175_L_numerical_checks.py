#!/usr/bin/env python3
"""Validate Step 175 numerical-evaluation artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step175_L_numerical_evaluation_artifacts"
)

REQUIRED = [
    "step175_results_summary.md",
    "step175_schema.json",
    "content_classification_step175.csv",
    "nonclaim_boundary_step175.md",
    "step175_L_numerical_evaluation.tex",
    "compute_L_numerical_step175.py",
    "compute_L_numerical_output_step175.txt",
    "run_step175_L_numerical_checks.py",
    "G_star_moments_step175.csv",
    "sinc_quadrature_step175.csv",
    "pswf_evaluations_step175.csv",
    "L_numerical_step175.csv",
    "branch_C_status_update_step175.csv",
    "residual_tree_step175.csv",
    "route_status_step175.csv",
    "construction_tasks_step175.csv",
]

ALLOWED = {
    "V_L_numerical_zero",
    "V_L_numerical_nonzero",
    "V_L_quadrature_indeterminate",
    "V_L_truncation_error_dominant",
}

FORBIDDEN = [
    r"\bthis is an RH proof\b",
    r"\bunconditional Xi_BC=0\b",
    r"\bauxiliary-GRH smuggling is allowed\b",
    r"\bpublic-shadow non-promotion is optional\b",
    r"\bfinite-window Calkin blindness is optional\b",
    r"\bincomplete character spectrum is accepted\b",
    r"\bscalar identity is carrier identity\b",
]


def fail(msg: str) -> None:
    print(f"FAIL step175 L numerical checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step175_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema JSON error: {exc}")
    if schema.get("step") != 175:
        fail("schema step must be 175")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("target") != "numerical L_{rho_1,0}(G_*)":
        fail("schema target mismatch")
    for key in [
        "inherited_formula",
        "G_star_moments",
        "I_sinc_numerical",
        "Psi_n_rho_1",
        "J_n",
        "pswf_truncation_bound",
        "L_numerical",
        "L_verdict",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    verdict = schema["L_verdict"]
    if verdict not in ALLOWED:
        fail(f"invalid verdict {verdict}")
    if schema["final_verdict"] != verdict:
        fail("final_verdict must equal L_verdict")
    if len(schema["Psi_n_rho_1"]) != 3 or len(schema["J_n"]) != 3:
        fail("schema must record n=0,1,2 PSWF and J values")
    L = schema["L_numerical"]
    if L.get("total_error_radius", 0) <= 0:
        fail("total_error_radius must be positive")
    if verdict == "V_L_numerical_nonzero":
        if L.get("lower_bound_abs", 0) <= 1e-3:
            fail("nonzero verdict must be separated from zero")
    return schema


def check_csvs() -> None:
    for name in REQUIRED:
        if not name.endswith(".csv"):
            continue
        with (ROOT / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must have at least one data row")

    with (ROOT / "L_numerical_step175.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    main = next((row for row in rows if row["quantity"] == "L_using_n_0_2"), None)
    if main is None:
        fail("L_numerical_step175.csv missing L_using_n_0_2 row")
    if float(main["total_error_radius"]) <= 0:
        fail("L_numerical_step175.csv missing positive total_error_radius")
    if float(main["lower_bound_abs"]) <= 1e-3:
        fail("L lower bound is not separated from zero")


def check_tex_and_output() -> None:
    tex = text("step175_L_numerical_evaluation.tex")
    required_snippets = [
        r"V\_L\_numerical\_nonzero",
        "0.12146653476134234",
        "0.08985731971133760",
        "1.9648066412630187",
        "I_{\\rm sinc}",
        "A_1",
        "PSWF",
        "total error radius",
    ]
    for snippet in required_snippets:
        if snippet not in tex:
            fail(f"tex missing snippet {snippet!r}")
    out = text("compute_L_numerical_output_step175.txt")
    if "verdict=V_L_numerical_nonzero" not in out:
        fail("compute output missing numerical nonzero verdict")
    if "mpmath_dps=50" not in out:
        fail("compute output must record precision")


def check_forbidden() -> None:
    combined = "\n".join(text(name) for name in REQUIRED if name != "run_step175_L_numerical_checks.py")
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
    print("PASS step175 L numerical checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"L_verdict={schema['L_verdict']}")
    print(f"L_lower_bound_abs={schema['L_numerical']['lower_bound_abs']:.16e}")


if __name__ == "__main__":
    main()
