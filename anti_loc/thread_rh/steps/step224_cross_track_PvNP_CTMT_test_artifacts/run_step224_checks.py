#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step224_cross_track_PvNP_CTMT_test_artifacts")

required = [
    "step224_results_summary.md",
    "step224_schema.json",
    "content_classification_step224.csv",
    "nonclaim_boundary_step224.md",
    "step224_cross_track_PvNP_CTMT_test.tex",
    "run_step224_checks.py",
    "pvnp_records_summary_step224.csv",
    "literature_audit_step224.csv",
    "CTMT_recursion_layers_pvnp_step224.csv",
    "cross_track_implication_step224.csv",
    "residual_tree_step224.csv",
    "route_status_step224.csv",
    "construction_tasks_step224.csv",
    "classical_theorems_cited_step224.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step224_schema.json").read_text())
assert schema["step"] == 224
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_pvnp_CTMT_recursion_verified"
assert "verified-on-5-track-instances" in schema["framework_finding_upgrade_status"]
assert len(schema["recursion_layers_observed"]) >= 10
assert "abstract-interpretation" in schema["pvnp_external_theorem_typed"]["central_obligation"]

with (OUT / "literature_audit_step224.csv").open() as f:
    lit_rows = list(csv.DictReader(f))
assert len(lit_rows) >= 10
assert any("Baker" in row["source"] for row in lit_rows)
assert any("Razborov" in row["source"] for row in lit_rows)
assert any("Aaronson" in row["source"] for row in lit_rows)
assert any("Williams" in row["source"] for row in lit_rows)

with (OUT / "CTMT_recursion_layers_pvnp_step224.csv").open() as f:
    layer_rows = list(csv.DictReader(f))
assert len(layer_rows) >= 10
assert any("universal P-machine" in row["gate"] for row in layer_rows)
assert any("no-smuggling" in row["gate"] for row in layer_rows)
assert any("natural proofs" in row["gate"] for row in layer_rows)

with (OUT / "pvnp_records_summary_step224.csv").open() as f:
    rec_rows = list(csv.DictReader(f))
assert len(rec_rows) >= 8
assert any("np47" in row["record_path"] for row in rec_rows)
assert any("np46" in row["record_path"] for row in rec_rows)

print("Step 224 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
