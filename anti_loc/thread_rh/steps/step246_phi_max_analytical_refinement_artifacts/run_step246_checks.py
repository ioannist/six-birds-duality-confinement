#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step246_phi_max_analytical_refinement_artifacts")

required = [
    "step246_results_summary.md",
    "step246_schema.json",
    "content_classification_step246.csv",
    "nonclaim_boundary_step246.md",
    "step246_phi_max_analytical_refinement.tex",
    "compute_phi_grid_step246.py",
    "fit_phi_step246.py",
    "run_step246_checks.py",
    "phi_grid_step246.csv",
    "alternative_fits_step246.csv",
    "constant_lookup_step246.csv",
    "residual_tree_step246.csv",
    "route_status_step246.csv",
    "construction_tasks_step246.csv",
]
missing = [name for name in required if not (BASE / name).exists()]
if missing:
    raise SystemExit(f"missing artifacts: {missing}")

schema = json.loads((BASE / "step246_schema.json").read_text())
assert schema["step"] == 246
assert schema["orientation"] == "adequacy"
assert schema["target"] == "Phi(sigma, ell) analytical refinement"
assert schema["grid_size"] == 90
assert schema["final_verdict"] == "V_phi_no_simple_closed_form"

with (BASE / "phi_grid_step246.csv").open(newline="") as f:
    grid = list(csv.DictReader(f))
assert len(grid) == 90
assert max(float(r["Phi"]) for r in grid) > 0.48

with (BASE / "alternative_fits_step246.csv").open(newline="") as f:
    fits = list(csv.DictReader(f))
assert len(fits) >= 5
best = min(float(r["rmse"]) for r in fits)
assert best > 1e-4

with (BASE / "constant_lookup_step246.csv").open(newline="") as f:
    const = list(csv.DictReader(f))
assert any("OEIS" in r["constant_or_formula"] for r in const)

print("step246 validation passed")
