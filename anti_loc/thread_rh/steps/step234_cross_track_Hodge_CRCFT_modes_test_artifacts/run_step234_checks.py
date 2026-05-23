#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step234_cross_track_Hodge_CRCFT_modes_test_artifacts")

required = [
    "step234_results_summary.md",
    "step234_schema.json",
    "content_classification_step234.csv",
    "nonclaim_boundary_step234.md",
    "step234_cross_track_Hodge_CRCFT_modes.tex",
    "Hodge_components_step234.csv",
    "component_mode_classification_step234.csv",
    "literature_audit_step234.csv",
    "cross_track_implication_step234.csv",
    "residual_tree_step234.csv",
    "route_status_step234.csv",
    "construction_tasks_step234.csv",
    "classical_theorems_cited_step234.csv",
]

missing = [name for name in required if not (ART / name).exists()]
if missing:
    raise SystemExit(f"missing required artifacts: {missing}")

schema = json.loads((ART / "step234_schema.json").read_text())
assert schema["step"] == 234
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["target"] == "CRCFT modes test on Hodge components"
assert schema["final_verdict"] == "V_hodge_CRCFT_modes_verified"

modes = set()
with (ART / "component_mode_classification_step234.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
for row in rows:
    modes.add(row["primary_mode"])
assert {"TE", "CTMT", "BF"}.issubset(modes), modes
assert len(rows) >= 7

summary = (ART / "step234_results_summary.md").read_text()
for token in ["Xi_H^std", "V_hodge_CRCFT_modes_verified", "verified-on-3-track-instances"]:
    assert token in summary

nonclaim = (ART / "nonclaim_boundary_step234.md").read_text()
assert "does not prove" in nonclaim

print("Step 234 validation passed")
print(f"artifact_dir={ART}")
print("final_verdict=V_hodge_CRCFT_modes_verified")
