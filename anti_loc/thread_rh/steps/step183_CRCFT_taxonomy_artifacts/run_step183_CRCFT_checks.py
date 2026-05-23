#!/usr/bin/env python3
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step183_CRCFT_taxonomy_artifacts")

REQUIRED = [
    "step183_results_summary.md",
    "step183_schema.json",
    "content_classification_step183.csv",
    "nonclaim_boundary_step183.md",
    "step183_CRCFT_taxonomy.tex",
    "CRCFT_typed_condition.md",
    "run_step183_CRCFT_checks.py",
    "CRCFT_definition_step183.csv",
    "CRCFT_modes_step183.csv",
    "CRCFT_instances_step183.csv",
    "CRCFT_consequence_step183.csv",
    "CRCFT_coverage_conjecture_step183.csv",
    "residual_tree_step183.csv",
    "route_status_step183.csv",
    "construction_tasks_step183.csv",
]

EXPECTED_VERDICT = "V_CRCFT_formalized"
EXPECTED_MODES = {"CRCFT-CTMT", "CRCFT-TE", "CRCFT-BF"}


def fail(msg: str) -> None:
    print(f"FAIL step183 CRCFT checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step183_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"invalid schema JSON: {exc}")

    if schema.get("step") != 183:
        fail("schema step must be 183")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("foundational_typed_condition_candidate") != "Classical-RH Carrier Foreclosure Taxonomy (CRCFT)":
        fail("foundational typed condition candidate mismatch")
    if schema.get("final_verdict") != EXPECTED_VERDICT:
        fail("final_verdict must be V_CRCFT_formalized")

    modes = schema.get("CRCFT_modes", [])
    mode_ids = {row.get("mode") for row in modes if isinstance(row, dict)}
    if mode_ids != EXPECTED_MODES:
        fail(f"CRCFT_modes mismatch: {mode_ids}")

    instances = schema.get("CRCFT_instances", [])
    if len(instances) != 7:
        fail("schema must contain exactly 7 CRCFT instances")
    instance_modes = " ".join(row.get("mode", "") for row in instances)
    for fragment in ["CRCFT-CTMT", "CRCFT-TE", "CRCFT-BF"]:
        if fragment not in instance_modes:
            fail(f"instances missing mode fragment {fragment}")

    coverage = schema.get("CRCFT_coverage_conjecture", {})
    if coverage.get("status") != "conjecture":
        fail("coverage conjecture status must be conjecture")
    if "4 carriers / 7 instances" not in coverage.get("support", ""):
        fail("coverage conjecture support must mention 4 carriers / 7 instances")

    relation = schema.get("relationship_to_CTMT", {})
    if not relation.get("distinct"):
        fail("relationship_to_CTMT.distinct must be true")
    if "target-equivalence" not in relation.get("CRCFT", ""):
        fail("relationship_to_CTMT must say CRCFT adds target-equivalence")

    if len(schema.get("retained_nogos", [])) < 9:
        fail("retained_nogos must include the inherited 9 no-gos")

    mode_rows = rows("CRCFT_modes_step183.csv")
    if {row.get("mode") for row in mode_rows} != EXPECTED_MODES:
        fail("CRCFT_modes_step183.csv must contain the 3 modes")

    instance_rows = rows("CRCFT_instances_step183.csv")
    if len(instance_rows) != 7:
        fail("CRCFT_instances_step183.csv must contain 7 rows")

    coverage_rows = rows("CRCFT_coverage_conjecture_step183.csv")
    if not coverage_rows or coverage_rows[0].get("status") != "conjecture":
        fail("coverage conjecture CSV must mark status conjecture")

    tex = text("step183_CRCFT_taxonomy.tex")
    md = text("CRCFT_typed_condition.md")
    snippets = [
        "Classical-RH Carrier Foreclosure Taxonomy",
        "CRCFT-CTMT",
        "CRCFT-TE",
        "CRCFT-BF",
        "CRCFT coverage",
        "not a theorem",
        "Relationship to CTMT",
    ]
    combined_doc = tex + "\n" + md
    for snippet in snippets:
        if snippet not in combined_doc:
            fail(f"taxonomy documents missing snippet: {snippet}")

    combined = "\n".join(
        text(name)
        for name in [
            "step183_results_summary.md",
            "nonclaim_boundary_step183.md",
            "step183_CRCFT_taxonomy.tex",
            "CRCFT_typed_condition.md",
        ]
    )
    forbidden = [
        r"\bCRCFT proves RH\b",
        r"\bcoverage conjecture is proved\b",
        r"\bcorpus integration is performed\b",
        r"\bcloses Xi_BC\b",
        r"\bremoves retained no-go\b",
    ]
    for pattern in forbidden:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")

    print("PASS step183 CRCFT checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"final_verdict={schema.get('final_verdict')}")
    print(f"instances={len(instances)}")
    print("coverage_status=conjecture")


if __name__ == "__main__":
    main()
