#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step231_ramanujan_tau_pivot_artifacts")

required = [
    "step231_results_summary.md",
    "step231_schema.json",
    "content_classification_step231.csv",
    "nonclaim_boundary_step231.md",
    "step231_ramanujan_tau_pivot.tex",
    "derive_tau_residual_step231.py",
    "run_step231_checks.py",
    "tau_declaration_step231.csv",
    "CRE_audit_step231.csv",
    "classification_step231.csv",
    "selberg_class_generalization_step231.csv",
    "residual_tree_step231.csv",
    "route_status_step231.csv",
    "construction_tasks_step231.csv",
    "classical_theorems_cited_step231.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step231_schema.json").read_text())
assert schema["step"] == 231
assert schema["final_verdict"] == "V_tau_outside_dichotomy"
assert schema["carrier_definition"]["critical_line"] == "Re(s)=6"
assert "Open" in schema["L_tau_RH_open_status"]
assert schema["CRE_status"] == "not_CRE_for_Riemann_RH"

with (OUT / "CRE_audit_step231.csv").open() as f:
    rows = list(csv.DictReader(f))
assert any(row["status"] == "not_CRE" for row in rows)
assert any(row["status"] == "open" for row in rows)

with (OUT / "classification_step231.csv").open() as f:
    cls = list(csv.DictReader(f))
assert any(row["classification_option"] == "outside Dichotomy" and row["status"] == "accepted" for row in cls)

print("Step 231 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
