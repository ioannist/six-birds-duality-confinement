#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step233_cross_track_BSD_CRCFT_modes_test_artifacts")

required = [
    "step233_results_summary.md",
    "step233_schema.json",
    "content_classification_step233.csv",
    "nonclaim_boundary_step233.md",
    "step233_cross_track_BSD_CRCFT_modes.tex",
    "run_step233_checks.py",
    "BSD_components_step233.csv",
    "component_mode_classification_step233.csv",
    "literature_audit_step233.csv",
    "cross_track_implication_step233.csv",
    "residual_tree_step233.csv",
    "route_status_step233.csv",
    "construction_tasks_step233.csv",
    "classical_theorems_cited_step233.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step233_schema.json").read_text())
assert schema["step"] == 233
assert schema["orientation"] == "cross-track-framework-validation"
assert schema["final_verdict"] == "V_bsd_CRCFT_modes_verified"
assert len(schema["BSD_components"]) == 5
assert "verified-on-2-track-instances" in schema["framework_finding_upgrade_status"]

with (OUT / "component_mode_classification_step233.csv").open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 5
modes = {row["primary_mode"] for row in rows}
assert {"TE", "CTMT", "BF"}.issubset(modes)
assert any(row["component"] == "E_det" and row["primary_mode"] == "CTMT" for row in rows)

with (OUT / "literature_audit_step233.csv").open() as f:
    lit = list(csv.DictReader(f))
assert len(lit) >= 5
assert any("Bloch-Kato" in row["source"] for row in lit)
assert any("Gross-Zagier" in row["source"] for row in lit)

print("Step 233 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
