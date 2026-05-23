#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step187_dichotomy_theorem_artifacts")

REQUIRED = [
    "step187_results_summary.md",
    "step187_schema.json",
    "content_classification_step187.csv",
    "nonclaim_boundary_step187.md",
    "step187_dichotomy_theorem.tex",
    "dichotomy_typed_condition.md",
    "run_step187_dichotomy_checks.py",
    "dichotomy_theorem_step187.csv",
    "dichotomy_instances_step187.csv",
    "consequence_theorem_step187.csv",
    "coverage_conjecture_step187.csv",
    "relationship_step187.csv",
    "residual_tree_step187.csv",
    "route_status_step187.csv",
    "construction_tasks_step187.csv",
]

EXPECTED_VERDICT = "V_dichotomy_formalized"


def fail(msg: str) -> None:
    print(f"FAIL step187 dichotomy checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step187_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 187:
        fail("schema step must be 187")
    if schema.get("orientation") != "adequacy":
        fail("orientation must be adequacy")
    if schema.get("foundational_typed_condition_candidate") != "Framework RH-Carrier Dichotomy Theorem":
        fail("foundational typed condition mismatch")
    if schema.get("final_verdict") != EXPECTED_VERDICT:
        fail("final_verdict mismatch")

    theorem = schema.get("theorem_statement", {})
    if "CRCFT" not in theorem.get("CRE_branch", ""):
        fail("CRE branch must mention CRCFT")
    if "Xi_C=0" not in theorem.get("non_CRE_branch", ""):
        fail("non-CRE branch must mention Xi_C=0")

    instances = schema.get("theorem_instances", [])
    if len(instances) != 7:
        fail("schema must contain 7 theorem instances")
    cre_count = sum(1 for row in instances if row.get("CRE_status") == "CRE")
    non_cre_count = sum(1 for row in instances if row.get("CRE_status") == "not_CRE")
    if cre_count != 5 or non_cre_count != 2:
        fail(f"expected 5 CRE and 2 non-CRE instances, got {cre_count}/{non_cre_count}")

    coverage = schema.get("coverage_conjecture", {})
    if coverage.get("status") != "conjecture":
        fail("coverage conjecture must be marked conjecture")
    if "7 carriers" not in coverage.get("support", ""):
        fail("coverage conjecture support must mention 7 carriers")

    relationship = schema.get("relationship_to_CTMT_CRCFT", {})
    if "submode" not in relationship.get("CTMT", ""):
        fail("relationship must say CTMT is submode")
    if "CRE branch" not in relationship.get("dichotomy", ""):
        fail("relationship must say CRCFT is CRE branch")

    if len(schema.get("retained_nogos", [])) < 10:
        fail("retained_nogos must preserve 10 no-gos")

    for csv_name in [
        "dichotomy_theorem_step187.csv",
        "dichotomy_instances_step187.csv",
        "consequence_theorem_step187.csv",
        "coverage_conjecture_step187.csv",
        "relationship_step187.csv",
        "residual_tree_step187.csv",
        "route_status_step187.csv",
        "construction_tasks_step187.csv",
    ]:
        if not rows(csv_name):
            fail(f"{csv_name} has no data rows")

    instance_rows = rows("dichotomy_instances_step187.csv")
    if len(instance_rows) != 7:
        fail("dichotomy_instances_step187.csv must contain 7 rows")
    csv_cre = sum(1 for row in instance_rows if row.get("CRE_status") == "CRE")
    csv_non_cre = sum(1 for row in instance_rows if row.get("CRE_status") == "not_CRE")
    if csv_cre != 5 or csv_non_cre != 2:
        fail("dichotomy_instances CSV must have 5 CRE and 2 non-CRE rows")

    coverage_rows = rows("coverage_conjecture_step187.csv")
    if coverage_rows[0].get("status") != "conjecture":
        fail("coverage conjecture CSV must be conjecture")

    tex = text("step187_dichotomy_theorem.tex")
    md = text("dichotomy_typed_condition.md")
    combined_doc = tex + "\n" + md
    snippets = [
        "Framework RH-Carrier Dichotomy",
        "V_{\\mathrm{dichotomy\\_formalized}}",
        "CRCFT",
        "native closure",
        "Coverage",
        "not a theorem",
        "Relationship to CTMT",
    ]
    for snippet in snippets:
        if snippet not in combined_doc:
            fail(f"documents missing snippet: {snippet}")

    combined = "\n".join(
        text(name)
        for name in [
            "step187_results_summary.md",
            "nonclaim_boundary_step187.md",
            "step187_dichotomy_theorem.tex",
            "dichotomy_typed_condition.md",
        ]
    )
    forbidden = [
        r"\bdichotomy proves RH\b",
        r"\bcoverage conjecture is proved\b",
        r"\bcloses Xi_BC\b",
        r"\btransfers Selberg.*to Riemann RH\b",
        r"\btransfers Weil.*to Riemann RH\b",
        r"\bcorpus integration is performed\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step187 dichotomy checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"final_verdict={schema.get('final_verdict')}")
    print(f"instances={len(instances)}")
    print(f"CRE_instances={cre_count}")
    print(f"non_CRE_instances={non_cre_count}")


if __name__ == "__main__":
    main()
