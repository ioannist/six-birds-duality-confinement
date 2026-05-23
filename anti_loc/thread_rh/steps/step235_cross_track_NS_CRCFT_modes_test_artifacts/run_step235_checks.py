#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step235_cross_track_NS_CRCFT_modes_test_artifacts")

required = [
    "step235_results_summary.md",
    "step235_schema.json",
    "content_classification_step235.csv",
    "nonclaim_boundary_step235.md",
    "step235_cross_track_NS_CRCFT_modes.tex",
    "NS_components_step235.csv",
    "component_mode_classification_step235.csv",
    "literature_audit_step235.csv",
    "cross_track_implication_step235.csv",
    "residual_tree_step235.csv",
    "route_status_step235.csv",
    "construction_tasks_step235.csv",
    "classical_theorems_cited_step235.csv",
]

missing = [name for name in required if not (ART / name).exists()]
if missing:
    raise SystemExit(f"missing required artifacts: {missing}")

schema = json.loads((ART / "step235_schema.json").read_text())
assert schema["step"] == 235
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["target"] == "CRCFT modes test on NS components"
assert schema["final_verdict"] == "V_ns_CRCFT_modes_verified"
assert "verified-on-4-track-instances" in schema["framework_finding_upgrade_status"]

with (ART / "component_mode_classification_step235.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
modes = {row["primary_mode"] for row in rows}
assert {"TE", "CTMT", "BF"}.issubset(modes), modes
assert len(rows) >= 9
assert any(row["component"].startswith("EXT1") and row["primary_mode"] == "TE" for row in rows)

summary = (ART / "step235_results_summary.md").read_text()
for token in ["Omega_amp", "V_ns_CRCFT_modes_verified", "verified-on-4-track-instances"]:
    assert token in summary

nonclaim = (ART / "nonclaim_boundary_step235.md").read_text()
assert "does not prove Navier" in nonclaim

print("Step 235 validation passed")
print(f"artifact_dir={ART}")
print("final_verdict=V_ns_CRCFT_modes_verified")
