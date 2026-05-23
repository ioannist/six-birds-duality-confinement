#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step198_RH_framework_audit_artifacts"
MASTER = ROOT / "anti_loc/RH_framework_audit.md"
CASCADE_MAP = ROOT / "anti_loc/thread/cascade_map_rh.md"

REQUIRED = [
    "step198_results_summary.md",
    "step198_schema.json",
    "content_classification_step198.csv",
    "nonclaim_boundary_step198.md",
    "step198_RH_framework_audit_meta.tex",
    "RH_framework_audit.md",
    "run_step198_audit_checks.py",
    "audit_structure_step198.csv",
    "integrated_typed_conditions_step198.csv",
    "integrated_carrier_instances_step198.csv",
    "integrated_no_gos_step198.csv",
    "corpus_inclusion_recommendations_step198.csv",
    "open_questions_step198.csv",
    "residual_tree_step198.csv",
    "route_status_step198.csv",
    "construction_tasks_step198.csv",
]

EXPECTED_SECTIONS = [
    "Executive Abstract",
    "Foundational Typed Condition I",
    "Foundational Typed Condition II",
    "Foundational Typed Condition III",
    "Foundational Typed Condition IV",
    "Bridge Impossibility Corollary",
    "Carrier Classification Table",
    "Numerical Experiment I",
    "Numerical Experiment II",
    "Retained Framework No-Gos",
    "Path 1/2/3 Strategic Conclusion",
    "Corpus-Inclusion Recommendations",
    "Open Questions",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read_csv(name: str):
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        fail(f"missing step artifacts: {missing}")
    if not MASTER.exists():
        fail("master audit document missing")
    if not CASCADE_MAP.exists():
        fail("cascade map missing")

    master_text = MASTER.read_text()
    copy_text = (BASE / "RH_framework_audit.md").read_text()
    if master_text != copy_text:
        fail("artifact audit copy differs from master")
    line_count = len(master_text.splitlines())
    if not (500 <= line_count <= 1500):
        fail(f"audit line count outside requested range: {line_count}")

    for section in EXPECTED_SECTIONS:
        if section not in master_text:
            fail(f"master audit missing section token: {section}")

    schema = json.loads((BASE / "step198_schema.json").read_text())
    if schema.get("step") != 198:
        fail("schema step must be 198")
    if schema.get("orientation") != "adequacy":
        fail("schema orientation must be adequacy")
    if schema.get("audit_document_path") != "anti_loc/RH_framework_audit.md":
        fail("schema audit path mismatch")
    if schema.get("audit_document_size_lines") != line_count:
        fail("schema audit line count mismatch")
    if len(schema.get("integrated_typed_conditions", [])) != 4:
        fail("schema must list 4 typed conditions")
    if schema.get("integrated_corollary") != "Framework Bridge Impossibility Corollary":
        fail("schema corollary mismatch")
    if schema.get("integrated_carrier_instances_count", 0) < 11:
        fail("carrier instance count too low")
    if schema.get("integrated_numerical_experiments_count") != 2:
        fail("numerical experiment count must be 2")
    if schema.get("integrated_no_gos_count") != 10:
        fail("no-go count must be 10")
    if schema.get("final_verdict") != "V_audit_integrated":
        fail("final verdict mismatch")

    typed_rows = read_csv("integrated_typed_conditions_step198.csv")
    if len(typed_rows) != 4:
        fail("typed conditions CSV must have 4 rows")
    carrier_rows = read_csv("integrated_carrier_instances_step198.csv")
    if len(carrier_rows) < 11:
        fail("carrier instances CSV must have at least 11 rows")
    nogo_rows = read_csv("integrated_no_gos_step198.csv")
    if len(nogo_rows) != 10:
        fail("no-go CSV must have 10 rows")

    cascade_text = CASCADE_MAP.read_text()
    if "RH_framework_audit.md" not in cascade_text:
        fail("cascade map does not reference RH_framework_audit.md")

    print("PASS step198 RH framework audit checks")
    print(f"audit_lines={line_count} carrier_rows={len(carrier_rows)}")


if __name__ == "__main__":
    main()

