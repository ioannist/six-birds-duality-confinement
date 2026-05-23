#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step228_cross_track_NS_Bridge_Impossibility_test_artifacts")

required = [
    "step228_results_summary.md",
    "step228_schema.json",
    "content_classification_step228.csv",
    "nonclaim_boundary_step228.md",
    "step228_cross_track_NS_Bridge_Impossibility.tex",
    "run_step228_checks.py",
    "candidate_carriers_step228.csv",
    "literature_audit_step228.csv",
    "bridge_assessment_step228.csv",
    "cross_track_implication_step228.csv",
    "residual_tree_step228.csv",
    "route_status_step228.csv",
    "construction_tasks_step228.csv",
    "classical_theorems_cited_step228.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step228_schema.json").read_text())
assert schema["step"] == 228
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_ns_Bridge_Impossibility_verified"
assert len(schema["NS_non_equivalent_carriers"]) >= 8
assert "verified-on-4-track-instances" in schema["framework_finding_upgrade_status"]

with (OUT / "candidate_carriers_step228.csv").open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 8
assert all("NS-strength" in row["bridge_strength_assessment"] for row in rows)
assert any("Caffarelli" in row["carrier"] for row in rows)
assert any("Tao" in row["carrier"] for row in rows)

with (OUT / "literature_audit_step228.csv").open() as f:
    lit = list(csv.DictReader(f))
assert len(lit) >= 9
assert any("Koch" in row["source"] for row in lit)
assert any("Buckmaster" in row["source"] for row in lit)
assert any("Escauriaza" in row["source"] for row in lit)

print("Step 228 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
