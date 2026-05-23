#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step222_cross_track_Hodge_CTMT_test_artifacts")

required = [
    "step222_results_summary.md",
    "step222_schema.json",
    "content_classification_step222.csv",
    "nonclaim_boundary_step222.md",
    "step222_cross_track_Hodge_CTMT_test.tex",
    "run_step222_checks.py",
    "Hodge_records_summary_step222.csv",
    "literature_audit_step222.csv",
    "CTMT_recursion_layers_hodge_step222.csv",
    "cross_track_implication_step222.csv",
    "residual_tree_step222.csv",
    "route_status_step222.csv",
    "construction_tasks_step222.csv",
    "classical_theorems_cited_step222.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step222_schema.json").read_text())
assert schema["step"] == 222
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_hodge_CTMT_recursion_verified"
assert "verified-on-3-track-instances" in schema["framework_finding_upgrade_status"]
assert len(schema["recursion_layers_observed"]) >= 6

with (OUT / "literature_audit_step222.csv").open() as f:
    lit_rows = list(csv.DictReader(f))
assert len(lit_rows) >= 8
assert any("Cattani" in row["source"] for row in lit_rows)
assert any("Aoki" in row["source"] for row in lit_rows)

with (OUT / "CTMT_recursion_layers_hodge_step222.csv").open() as f:
    layer_rows = list(csv.DictReader(f))
assert len(layer_rows) >= 6
assert any("Hodge-Riemann" in row["gate"] for row in layer_rows)
assert any("rational" in row["gate"] for row in layer_rows)

with (OUT / "Hodge_records_summary_step222.csv").open() as f:
    rec_rows = list(csv.DictReader(f))
assert len(rec_rows) >= 7
assert any("H24R" in row["record_path"] for row in rec_rows)
assert any("H36R" in row["record_path"] for row in rec_rows)

print("Step 222 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
