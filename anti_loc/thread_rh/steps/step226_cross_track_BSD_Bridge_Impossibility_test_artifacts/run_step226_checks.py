#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step226_cross_track_BSD_Bridge_Impossibility_test_artifacts")

required = [
    "step226_results_summary.md",
    "step226_schema.json",
    "content_classification_step226.csv",
    "nonclaim_boundary_step226.md",
    "step226_cross_track_BSD_Bridge_Impossibility.tex",
    "run_step226_checks.py",
    "candidate_carriers_step226.csv",
    "literature_audit_step226.csv",
    "cross_track_implication_step226.csv",
    "residual_tree_step226.csv",
    "route_status_step226.csv",
    "construction_tasks_step226.csv",
    "classical_theorems_cited_step226.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step226_schema.json").read_text())
assert schema["step"] == 226
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_bsd_Bridge_Impossibility_verified"
assert len(schema["BSD_non_BSD_equivalent_carriers"]) >= 6
assert "Bridge Impossibility cross-track verified on BSD" in schema["framework_finding_upgrade_status"]

with (OUT / "candidate_carriers_step226.csv").open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 6
assert all("BSD-strength" in row["bridge_strength_assessment"] for row in rows)
assert any("Modularity" in row["carrier"] for row in rows)
assert any("Iwasawa" in row["carrier"] for row in rows)

with (OUT / "literature_audit_step226.csv").open() as f:
    lit = list(csv.DictReader(f))
assert len(lit) >= 8
assert any("Gross-Zagier" in row["source"] for row in lit)
assert any("Skinner-Urban" in row["source"] for row in lit)
assert any("Bhargava" in row["source"] for row in lit)

print("Step 226 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
