#!/usr/bin/env python3
"""Validate Step 180 CTMT formalization artifacts."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step180_CTMT_formalization_artifacts"
)

REQUIRED = [
    "step180_results_summary.md",
    "step180_schema.json",
    "content_classification_step180.csv",
    "nonclaim_boundary_step180.md",
    "step180_CTMT_formalization.tex",
    "CTMT_typed_condition.md",
    "run_step180_CTMT_checks.py",
    "CTMT_definition_step180.csv",
    "CTMT_instances_step180.csv",
    "CTMT_consequence_step180.csv",
    "residual_tree_step180.csv",
    "route_status_step180.csv",
    "construction_tasks_step180.csv",
]

FORBIDDEN = [
    r"\bthis proves RH\b",
    r"\bCTMT proves RH\b",
    r"\bCTMT closes Xi_BC\b",
    r"\bretained no-gos are removed\b",
    r"\bcorpus update performed\b",
]


def fail(msg: str) -> None:
    print(f"FAIL step180 CTMT checks: {msg}", file=sys.stderr)
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
        schema = json.loads(text("step180_schema.json"))
    except json.JSONDecodeError as exc:
        fail(f"schema JSON error: {exc}")
    if schema.get("step") != 180:
        fail("schema step must be 180")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("foundational_typed_condition") != "Carrier-Typed Matrix-Element Terminality (CTMT)":
        fail("foundational typed condition mismatch")
    for key in [
        "CTMT_definition",
        "CTMT_instances",
        "CTMT_consequence_theorem",
        "corpus_inclusion_candidate",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            fail(f"schema missing {key}")
    if schema["final_verdict"] != "V_CTMT_formalized":
        fail("final verdict must be V_CTMT_formalized")
    if len(schema["CTMT_instances"]) != 4:
        fail("schema must record four CTMT instances")
    modes = {row["resolution_mode"].split(":")[0] for row in schema["CTMT_instances"]}
    if not {"CTMT-stuck", "CTMT-foreclosed-numerical", "CTMT-bridge-failure"}.issubset(modes):
        fail("instances must include all three CTMT resolution modes")
    corpus = schema["corpus_inclusion_candidate"]
    if corpus.get("candidate") is not True:
        fail("corpus inclusion candidate must be true")
    if corpus.get("target_file") != "anti_loc/CTMT.md":
        fail("corpus target file mismatch")
    return schema


def check_csvs() -> None:
    for name in REQUIRED:
        if not name.endswith(".csv"):
            continue
        with (ROOT / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) < 2:
            fail(f"{name} must have data rows")
    with (ROOT / "CTMT_instances_step180.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 4:
        fail("CTMT instances CSV must have four rows")
    if {row["instance"] for row in rows} != {"A", "B", "C", "H6"}:
        fail("CTMT instances must be A, B, C, H6")


def check_docs() -> None:
    tex = text("step180_CTMT_formalization.tex")
    md = text("CTMT_typed_condition.md")
    for snippet in [
        "Carrier-Typed Matrix-Element Terminality",
        "CTMT-stuck",
        "CTMT-foreclosed-numerical",
        "CTMT-bridge-failure",
        "V\\_CTMT\\_formalized",
    ]:
        if snippet not in tex:
            fail(f"tex missing {snippet!r}")
    for snippet in [
        "Carrier-Typed Matrix-Element Terminality",
        "Instance | Carrier | M form",
        "anti_loc/CTMT.md",
        "CTMT-bridge-failure",
    ]:
        if snippet not in md:
            fail(f"markdown missing {snippet!r}")


def check_forbidden() -> None:
    combined = "\n".join(text(name) for name in REQUIRED if name != "run_step180_CTMT_checks.py")
    for pattern in FORBIDDEN:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            fail(f"forbidden phrase matched: {pattern}")


def main() -> None:
    if not ROOT.exists():
        fail(f"missing artifact directory {ROOT}")
    check_files()
    schema = check_schema()
    check_csvs()
    check_docs()
    check_forbidden()
    print("PASS step180 CTMT checks")
    print(f"artifacts_checked={len(REQUIRED)}")
    print(f"final_verdict={schema['final_verdict']}")
    print("corpus_candidate=anti_loc/CTMT.md")


if __name__ == "__main__":
    main()
