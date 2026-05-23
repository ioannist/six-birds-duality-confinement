#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step245_independent_codification_pattern_artifacts")
FINDINGS = Path("/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md")

required = [
    "step245_results_summary.md",
    "step245_schema.json",
    "content_classification_step245.csv",
    "nonclaim_boundary_step245.md",
    "step245_independent_codification_pattern.tex",
    "run_step245_checks.py",
    "BI_independent_codifications_step245.csv",
    "other_typed_conditions_check_step245.csv",
    "framework_finding_step245.csv",
    "residual_tree_step245.csv",
    "route_status_step245.csv",
    "construction_tasks_step245.csv",
]

missing = [name for name in required if not (BASE / name).exists()]
if missing:
    raise SystemExit(f"missing artifacts: {missing}")

schema = json.loads((BASE / "step245_schema.json").read_text())
assert schema["step"] == 245
assert schema["orientation"] == "framework-meta-pattern"
assert schema["target"] == "Independent Codification Pattern"
assert schema["final_verdict"] == "V_independent_codification_typed_3_instance_BI"
assert len(schema["primary_evidence_3_instance_BI"]) == 3

with (BASE / "BI_independent_codifications_step245.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 3
assert {r["track"] for r in rows} == {"RH", "Hodge", "P-vs-NP"}

with (BASE / "other_typed_conditions_check_step245.csv").open(newline="") as f:
    other = list(csv.DictReader(f))
assert len(other) >= 4

findings_text = FINDINGS.read_text()
assert "Independent Codification Pattern" in findings_text
assert "3 independent codifications of Bridge Impossibility" in findings_text

print("step245 validation passed")
