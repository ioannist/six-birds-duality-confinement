#!/usr/bin/env python3
"""Step 174 artifact validator.

Checks the local artifact contract for the L_{rho,k} evaluation attempt.
The validator is intentionally syntactic: it verifies that the requested
objects, verdict fields, decomposition, and nonclaim boundaries are present.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step174_L_rho_k_evaluation_artifacts"
)

REQUIRED_FILES = [
    "step174_results_summary.md",
    "step174_schema.json",
    "content_classification_step174.csv",
    "nonclaim_boundary_step174.md",
    "step174_L_rho_k_evaluation.tex",
    "run_step174_L_evaluation_checks.py",
    "inherited_records_step174.csv",
    "computation_chain_step174.csv",
    "G_star_legality_step174.csv",
    "L_verdict_step174.csv",
    "branch_C_status_update_step174.csv",
    "residual_tree_step174.csv",
    "route_status_step174.csv",
    "construction_tasks_step174.csv",
]

ALLOWED_VERDICTS = {
    "V_L_zero_explicit",
    "V_L_nonzero_explicit",
    "V_L_symbolic_form",
    "V_L_pswf_truncation",
    "V_L_stuck_at_normalization",
    "V_L_target_equivalent",
}

FORBIDDEN_PATTERNS = [
    r"\bRH proof\b",
    r"\bthis is an RH proof\b",
    r"\bunconditional Xi_BC=0\b",
    r"\bauxiliary-GRH smuggling is allowed\b",
    r"\bpublic-shadow non-promotion is optional\b",
    r"\bfinite-window Calkin blindness is optional\b",
    r"\bincomplete character spectrum is accepted\b",
    r"\bscalar identity is carrier identity\b",
    r"\bproves full ZI-COV\b",
    r"\bproves projected jet-surjectivity\b",
]


def fail(message: str) -> None:
    print(f"FAIL step174 L evaluation checks: {message}", file=sys.stderr)
    sys.exit(1)


def read_text(name: str) -> str:
    path = ROOT / name
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"could not read {name}: {exc}")


def check_required_files() -> None:
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.exists():
            fail(f"missing required artifact {name}")
        if path.stat().st_size == 0:
            fail(f"empty required artifact {name}")


def check_schema() -> dict:
    try:
        schema = json.loads(read_text("step174_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema is not valid JSON: {exc}")

    expected = {
        "step": 174,
        "orientation": "adequacy",
        "target_evaluation": "L_{rho_1, 0}(G_*)",
    }
    for key, value in expected.items():
        if schema.get(key) != value:
            fail(f"schema {key!r} expected {value!r}, got {schema.get(key)!r}")

    for key in [
        "G_star_definition",
        "lambda_choice",
        "pswf_truncation_order",
        "computation_chain",
        "L_verdict",
        "L_value",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")

    verdict = schema["L_verdict"]
    if verdict not in ALLOWED_VERDICTS:
        fail(f"schema has invalid L_verdict {verdict!r}")
    if schema["final_verdict"] != verdict:
        fail("schema final_verdict does not equal L_verdict")

    if verdict in {
        "V_L_zero_explicit",
        "V_L_nonzero_explicit",
        "V_L_symbolic_form",
        "V_L_pswf_truncation",
    } and not str(schema.get("L_value", "")).strip():
        fail("schema L_value required for formula/value verdict")

    g_def = json.dumps(schema["G_star_definition"], sort_keys=True)
    for token in ["g_*", "G_*(0)=0", "G_*(1)=0", "nonzero", "C_c^infty"]:
        if token not in g_def:
            fail(f"G_star_definition missing {token!r}")

    stages = {item.get("stage") for item in schema["computation_chain"]}
    if not {"T3a", "T3b", "T3c", "T3d"}.issubset(stages):
        fail("schema computation_chain must contain T3a, T3b, T3c, T3d")

    return schema


def check_tex(schema: dict) -> None:
    tex = read_text("step174_L_rho_k_evaluation.tex")

    required_snippets = [
        "T3a",
        "T3b",
        "T3c",
        "T3d",
        r"(\Psym F_*)(s)=D_*(s)-C_*(s)-R_*(s)",
        r"L_{\rho_1,0}(G_*)",
        r"\sum_{n=0}^{2}",
        r"G_*(0)=0",
        r"G_*(1)=0",
        r"V\_L\_symbolic\_form",
        r"\zeta(\rho_1)G_*(\rho_1)=0",
    ]
    for snippet in required_snippets:
        if snippet not in tex:
            fail(f"tex missing required snippet {snippet!r}")

    if "Slepian--Pollak PSWFs" not in tex:
        fail("tex must cite the PSWF diagonalization used")

    if schema["L_verdict"] == "V_L_symbolic_form":
        if (
            "does not prove that the value is zero or nonzero" not in tex
            and "does not decide whether" not in tex
            and "zero/nonzero is undecided" not in tex
        ):
            fail("symbolic verdict must state that zero/nonzero is undecided")


def check_csvs() -> None:
    for name in REQUIRED_FILES:
        if not name.endswith(".csv"):
            continue
        path = ROOT / name
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must contain a header and at least one data row")


def check_forbidden() -> None:
    combined = "\n".join(
        read_text(name)
        for name in REQUIRED_FILES
        if name != "run_step174_L_evaluation_checks.py"
    )
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")


def main() -> None:
    if not ROOT.exists():
        fail(f"artifact directory missing: {ROOT}")
    check_required_files()
    schema = check_schema()
    check_tex(schema)
    check_csvs()
    check_forbidden()
    print("PASS step174 L evaluation checks")
    print(f"artifacts_checked={len(REQUIRED_FILES)}")
    print(f"L_verdict={schema['L_verdict']}")


if __name__ == "__main__":
    main()
