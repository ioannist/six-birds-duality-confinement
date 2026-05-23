#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step247_branch_C_k1_proper_artifacts")

required = [
    "step247_results_summary.md",
    "step247_schema.json",
    "content_classification_step247.csv",
    "nonclaim_boundary_step247.md",
    "step247_branch_C_k1_proper.tex",
    "derive_k1_kernel_step247.py",
    "compute_L_k1_proper_step247.py",
    "compute_step247_output.txt",
    "run_step247_checks.py",
    "k1_proper_dataset_step247.csv",
    "branch_C_k1_status_step247.csv",
    "robustness_step247.csv",
    "residual_tree_step247.csv",
    "route_status_step247.csv",
    "construction_tasks_step247.csv",
    "classical_theorems_cited_step247.csv",
]

missing = [name for name in required if not (BASE / name).exists()]
if missing:
    raise SystemExit(f"missing artifacts: {missing}")

schema = json.loads((BASE / "step247_schema.json").read_text())
assert schema["step"] == 247
assert schema["orientation"] == "adequacy"
assert schema["final_verdict"] == "V_branch_C_k1_proper_foreclosure"
assert len(schema["k1_proper_values"]) == 3

with (BASE / "k1_proper_dataset_step247.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 18
k1 = [r for r in rows if r["k"] == "1"]
assert len(k1) == 3
assert min(float(r["proper_lower_bound_abs"]) for r in k1) > 0.28

with (BASE / "robustness_step247.csv").open(newline="") as f:
    comp = list(csv.DictReader(f))
assert max(float(r["abs_difference"]) for r in comp) < 3e-5

print("step247 validation passed")
