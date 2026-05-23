#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step223_cross_track_NS_CTMT_test_artifacts")

required = [
    "step223_results_summary.md",
    "step223_schema.json",
    "content_classification_step223.csv",
    "nonclaim_boundary_step223.md",
    "step223_cross_track_NS_CTMT_test.tex",
    "run_step223_checks.py",
    "NS_records_summary_step223.csv",
    "literature_audit_step223.csv",
    "CTMT_recursion_layers_ns_step223.csv",
    "cross_track_implication_step223.csv",
    "residual_tree_step223.csv",
    "route_status_step223.csv",
    "construction_tasks_step223.csv",
    "classical_theorems_cited_step223.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step223_schema.json").read_text())
assert schema["step"] == 223
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_ns_CTMT_recursion_verified"
assert "verified-on-4-track-instances" in schema["framework_finding_upgrade_status"]
assert len(schema["recursion_layers_observed"]) >= 8
assert "EXT1 sector-matched radius-window product theorem" in schema["NS_external_theorem_typed"]["central_obligation"]

with (OUT / "literature_audit_step223.csv").open() as f:
    lit_rows = list(csv.DictReader(f))
assert len(lit_rows) >= 10
assert any("Caffarelli" in row["source"] for row in lit_rows)
assert any("Tao" in row["source"] for row in lit_rows)
assert any("Grujic" in row["source"] for row in lit_rows)

with (OUT / "CTMT_recursion_layers_ns_step223.csv").open() as f:
    layer_rows = list(csv.DictReader(f))
assert len(layer_rows) >= 8
assert any("radius-window" in row["gate"] for row in layer_rows)
assert any("Gevrey" in row["gate"] for row in layer_rows)

with (OUT / "NS_records_summary_step223.csv").open() as f:
    rec_rows = list(csv.DictReader(f))
assert len(rec_rows) >= 8
assert any("ns55" in row["record_path"] for row in rec_rows)
assert any("ns54" in row["record_path"] for row in rec_rows)

print("Step 223 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
