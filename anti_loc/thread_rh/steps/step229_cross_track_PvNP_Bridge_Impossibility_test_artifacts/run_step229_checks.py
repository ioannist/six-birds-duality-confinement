#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step229_cross_track_PvNP_Bridge_Impossibility_test_artifacts")

required = [
    "step229_results_summary.md",
    "step229_schema.json",
    "content_classification_step229.csv",
    "nonclaim_boundary_step229.md",
    "step229_cross_track_PvNP_Bridge_Impossibility.tex",
    "run_step229_checks.py",
    "candidate_carriers_step229.csv",
    "literature_audit_step229.csv",
    "bridge_assessment_step229.csv",
    "cross_track_implication_step229.csv",
    "residual_tree_step229.csv",
    "route_status_step229.csv",
    "construction_tasks_step229.csv",
    "classical_theorems_cited_step229.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step229_schema.json").read_text())
assert schema["step"] == 229
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_pvnp_Bridge_Impossibility_verified"
assert len(schema["pvnp_non_equivalent_carriers"]) >= 10
assert "verified-on-5-track-instances" in schema["framework_finding_upgrade_status"]

with (OUT / "candidate_carriers_step229.csv").open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 10
assert all("P-vs-NP-strength" in row["bridge_strength_assessment"] for row in rows)
assert any("Cook" in row["carrier"] for row in rows)
assert any("Williams" in row["carrier"] for row in rows)
assert any("Aaronson" in row["carrier"] for row in rows)

with (OUT / "literature_audit_step229.csv").open() as f:
    lit = list(csv.DictReader(f))
assert len(lit) >= 10
assert any("Natural" in row["source"] or "Razborov-Rudich" in row["source"] for row in lit)
assert any("Algebrization" in row["source"] or "Aaronson" in row["source"] for row in lit)
assert any("Clay" in row["source"] for row in lit)

print("Step 229 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
