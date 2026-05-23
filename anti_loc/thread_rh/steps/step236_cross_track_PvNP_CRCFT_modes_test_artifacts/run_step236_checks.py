#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step236_cross_track_PvNP_CRCFT_modes_test_artifacts")

required = [
    "step236_results_summary.md",
    "step236_schema.json",
    "content_classification_step236.csv",
    "nonclaim_boundary_step236.md",
    "step236_cross_track_PvNP_CRCFT_modes.tex",
    "pvnp_components_step236.csv",
    "component_mode_classification_step236.csv",
    "literature_audit_step236.csv",
    "cross_track_implication_step236.csv",
    "residual_tree_step236.csv",
    "route_status_step236.csv",
    "construction_tasks_step236.csv",
    "classical_theorems_cited_step236.csv",
]

missing = [name for name in required if not (ART / name).exists()]
if missing:
    raise SystemExit(f"missing required artifacts: {missing}")

schema = json.loads((ART / "step236_schema.json").read_text())
assert schema["step"] == 236
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["target"] == "CRCFT modes test on P-vs-NP components"
assert schema["final_verdict"] == "V_pvnp_CRCFT_modes_verified"
assert "verified-on-5-track-instances" in schema["framework_finding_upgrade_status"]

with (ART / "component_mode_classification_step236.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
modes = {row["primary_mode"] for row in rows}
assert {"TE", "CTMT", "BF"}.issubset(modes), modes
assert len(rows) >= 11
assert any("universal P-machine" in row["component"] and row["primary_mode"] == "TE" for row in rows)
assert any("barrier" in row["component"] and row["primary_mode"] == "BF" for row in rows)

summary = (ART / "step236_results_summary.md").read_text()
for token in ["Xi_pack", "V_pvnp_CRCFT_modes_verified", "verified-on-5-track-instances"]:
    assert token in summary

nonclaim = (ART / "nonclaim_boundary_step236.md").read_text()
assert "does not prove `P != NP`" in nonclaim

print("Step 236 validation passed")
print(f"artifact_dir={ART}")
print("final_verdict=V_pvnp_CRCFT_modes_verified")
