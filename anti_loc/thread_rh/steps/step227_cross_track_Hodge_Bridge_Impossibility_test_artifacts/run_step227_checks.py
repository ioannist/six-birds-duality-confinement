#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step227_cross_track_Hodge_Bridge_Impossibility_test_artifacts")

required = [
    "step227_results_summary.md",
    "step227_schema.json",
    "content_classification_step227.csv",
    "nonclaim_boundary_step227.md",
    "step227_cross_track_Hodge_Bridge_Impossibility.tex",
    "run_step227_checks.py",
    "candidate_carriers_step227.csv",
    "literature_audit_step227.csv",
    "bridge_assessment_step227.csv",
    "cross_track_implication_step227.csv",
    "residual_tree_step227.csv",
    "route_status_step227.csv",
    "construction_tasks_step227.csv",
    "classical_theorems_cited_step227.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step227_schema.json").read_text())
assert schema["step"] == 227
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_hodge_Bridge_Impossibility_verified"
assert len(schema["Hodge_non_equivalent_carriers"]) >= 6
assert "verified-on-3-track-instances" in schema["framework_finding_upgrade_status"]

with (OUT / "candidate_carriers_step227.csv").open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 6
assert all("Hodge-strength" in row["bridge_strength_assessment"] for row in rows)
assert any("Lefschetz" in row["carrier"] for row in rows)
assert any("Cattani" in row["carrier"] for row in rows)

with (OUT / "literature_audit_step227.csv").open() as f:
    lit = list(csv.DictReader(f))
assert len(lit) >= 8
assert any("Deligne" in row["source"] for row in lit)
assert any("Tate" in row["source"] for row in lit)
assert any("Voisin" in row["source"] for row in lit)

print("Step 227 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
