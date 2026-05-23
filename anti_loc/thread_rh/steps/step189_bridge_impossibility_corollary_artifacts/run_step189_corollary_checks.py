#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step189_bridge_impossibility_corollary_artifacts")

REQUIRED = [
    "step189_results_summary.md",
    "step189_schema.json",
    "content_classification_step189.csv",
    "nonclaim_boundary_step189.md",
    "step189_bridge_impossibility_corollary.tex",
    "run_step189_corollary_checks.py",
    "corollary_statement_step189.csv",
    "proof_chain_step189.csv",
    "specializations_step189.csv",
    "RH_strategy_paths_step189.csv",
    "residual_tree_step189.csv",
    "route_status_step189.csv",
    "construction_tasks_step189.csv",
]

EXPECTED_VERDICT = "V_corollary_partial"


def fail(msg: str) -> None:
    print(f"FAIL step189 corollary checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step189_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 189:
        fail("schema step must be 189")
    if schema.get("orientation") != "adequacy":
        fail("orientation must be adequacy")
    if schema.get("theorem_derived") != "Framework Bridge Impossibility Corollary":
        fail("theorem_derived mismatch")
    if schema.get("corollary_verdict") != EXPECTED_VERDICT:
        fail("corollary_verdict mismatch")
    if schema.get("final_verdict") != EXPECTED_VERDICT:
        fail("final_verdict mismatch")

    stmt = schema.get("corollary_statement", {})
    if "C+B is CRE" not in stmt.get("general_form", ""):
        fail("general corollary must state composite is CRE")
    if "exact/minimal" not in stmt.get("exact_bridge_TE_form", ""):
        fail("exact bridge TE form must mention exact/minimal")
    if "may be TE, CTMT, or BF" not in stmt.get("caveat", ""):
        fail("caveat must preserve non-TE modes")

    proof = schema.get("proof_summary", [])
    if len(proof) < 7:
        fail("proof_summary too short")
    proof_text = " ".join(proof)
    for expected in ["Xi_C=0", "Xi_BC=0", "CRE", "Dichotomy", "CRCFT"]:
        if expected not in proof_text:
            fail(f"proof summary missing {expected}")

    specs = schema.get("specializations", [])
    if len(specs) != 2:
        fail("must contain Selberg and Weil-Deligne specializations")
    spec_names = " ".join(row.get("name", "") for row in specs)
    if "Selberg" not in spec_names or "Weil-Deligne" not in spec_names:
        fail("specializations missing Selberg or Weil-Deligne")

    paths = schema.get("broader_RH_strategy_implications", [])
    if len(paths) != 3:
        fail("must contain Path 1/2/3")
    path_ids = {row.get("path") for row in paths}
    if path_ids != {"Path 1", "Path 2", "Path 3"}:
        fail(f"path set mismatch: {path_ids}")

    if len(schema.get("retained_nogos", [])) < 10:
        fail("retained_nogos must preserve 10 no-gos")

    for csv_name in [
        "corollary_statement_step189.csv",
        "proof_chain_step189.csv",
        "specializations_step189.csv",
        "RH_strategy_paths_step189.csv",
        "residual_tree_step189.csv",
        "route_status_step189.csv",
        "construction_tasks_step189.csv",
    ]:
        if not rows(csv_name):
            fail(f"{csv_name} has no data rows")

    statement_rows = {row.get("form"): row for row in rows("corollary_statement_step189.csv")}
    if statement_rows.get("overstrong_unrestricted_TE", {}).get("status") != "not_proved_without_extra_restriction":
        fail("statement CSV must reject overstrong unrestricted TE")

    proof_rows = rows("proof_chain_step189.csv")
    if len(proof_rows) < 8:
        fail("proof chain CSV must have at least 8 rows")

    tex = text("step189_bridge_impossibility_corollary.tex")
    snippets = [
        "V_{\\mathrm{corollary\\_partial}}",
        "Framework bridge impossibility",
        "C+B",
        "Step 187",
        "Exact-bridge TE form",
        "Selberg/Maass",
        "Weil--Deligne",
        "Path",
        "not prove RH",
    ]
    for snippet in snippets:
        if snippet not in tex:
            fail(f"TeX missing snippet: {snippet}")

    combined = "\n".join(
        text(name)
        for name in [
            "step189_results_summary.md",
            "nonclaim_boundary_step189.md",
            "step189_bridge_impossibility_corollary.tex",
        ]
    )
    forbidden = [
        r"\bthis step proves RH\b",
        r"\bcloses Xi_BC\b",
        r"\bSelberg.*transfers.*to Riemann RH\b",
        r"\bWeil.*transfers.*to Riemann RH\b",
        r"\btherefore every possible bridge is CRCFT-TE\b",
        r"\bunrestricted.*always TE\b",
        r"\bweakens retained no-go\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step189 corollary checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"corollary_verdict={schema.get('corollary_verdict')}")
    print("exact_bridge_TE=proved_under_restriction")
    print("unrestricted_TE=not_proved")


if __name__ == "__main__":
    main()
