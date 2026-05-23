#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step249_branch_C_k2_proper_artifacts")

required = [
    "step249_results_summary.md",
    "step249_schema.json",
    "content_classification_step249.csv",
    "nonclaim_boundary_step249.md",
    "step249_branch_C_k2_proper.tex",
    "derive_k2_kernel_step249.py",
    "compute_L_k2_proper_step249.py",
    "compute_step249_output.txt",
    "run_step249_checks.py",
    "k2_proper_dataset_step249.csv",
    "branch_C_k2_status_step249.csv",
    "robustness_step249.csv",
    "residual_tree_step249.csv",
    "route_status_step249.csv",
    "construction_tasks_step249.csv",
    "classical_theorems_cited_step249.csv",
]

missing = [name for name in required if not (BASE / name).exists()]
if missing:
    raise SystemExit(f"missing artifacts: {missing}")

schema = json.loads((BASE / "step249_schema.json").read_text())
assert schema["step"] == 249
assert schema["orientation"] == "adequacy"
assert schema["final_verdict"] == "V_branch_C_k2_proper_foreclosure"
assert len(schema["k2_proper_values"]) == 3

with (BASE / "k2_proper_dataset_step249.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 3
assert min(float(r["proper_lower_bound_abs"]) for r in rows) > 0.55

with (BASE / "robustness_step249.csv").open(newline="") as f:
    comp = list(csv.DictReader(f))
assert max(float(r["abs_difference_fd"]) for r in comp) < 1e-4

print("step249 validation passed")
