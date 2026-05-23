#!/usr/bin/env python3
import csv
import json
from pathlib import Path

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step230_branch_B_HS_trace_diagnostic_artifacts")

required = [
    "step230_results_summary.md",
    "step230_schema.json",
    "content_classification_step230.csv",
    "nonclaim_boundary_step230.md",
    "step230_branch_B_HS_trace.tex",
    "compute_HS_norm_step230.py",
    "run_step230_checks.py",
    "HS_terms_step230.csv",
    "convergence_analysis_step230.csv",
    "robustness_step230.csv",
    "residual_tree_step230.csv",
    "route_status_step230.csv",
    "construction_tasks_step230.csv",
]

missing = [name for name in required if not (OUT / name).exists()]
if missing:
    raise SystemExit(f"missing required files: {missing}")

schema = json.loads((OUT / "step230_schema.json").read_text())
assert schema["step"] == 230
assert schema["orientation"] == "adequacy"
assert schema["final_verdict"] == "V_HS_partial"
assert schema["orthonormalized_basis_size"]["CAND1_primary"] == 20
assert schema["partial_sum_sequence"]["CAND1_S15"] > 8.0

with (OUT / "HS_terms_step230.csv").open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 25
assert any(row["model"] == "CAND1" and row["n"] == "1" for row in rows)
assert any(row["model"] == "CAND2" and row["n"] == "10" for row in rows)

with (OUT / "convergence_analysis_step230.csv").open() as f:
    analysis = list(csv.DictReader(f))
assert any(row["model"] == "CAND1" and "precision" in row["analysis_verdict"] for row in analysis)
assert any(row["model"] == "CAND2" and "divergence" in row["analysis_verdict"] for row in analysis)

print("Step 230 validation passed")
print(f"artifact_dir={OUT}")
print(f"final_verdict={schema['final_verdict']}")
