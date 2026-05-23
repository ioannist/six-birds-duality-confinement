#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step313_rigorous_gaussian_linear_phase_artifacts")
required = [
    "derive_sigma_alpha_step313.py",
    "sigma_alpha_predicted_vs_empirical_step313.csv",
    "second_derivative_bounds_step313.csv",
    "upgraded_theorem_step313.tex",
    "step313_results_summary.md",
    "step313_schema.json",
    "nonclaim_boundary_step313.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step313_schema.json").read_text())
if schema.get("step") != 313:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_gaussian_linear_phase_partial_binomial_dominates_sigma_alpha_still_empirical":
    raise SystemExit("unexpected final verdict")

with (BASE / "sigma_alpha_predicted_vs_empirical_step313.csv").open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
if len(rows) != 4:
    raise SystemExit("sigma/alpha row count mismatch")
for row in rows:
    ratio = float(row["sigma_total_over_empirical"])
    if not (0.9 <= ratio <= 1.1):
        raise SystemExit(f"sigma_total not close to empirical: {row}")
    alpha_ratio = float(row["alpha_local_over_empirical"])
    if not (0.9 <= alpha_ratio <= 1.1):
        raise SystemExit(f"alpha_local not close to empirical: {row}")

with (BASE / "second_derivative_bounds_step313.csv").open(newline="", encoding="utf-8") as fh:
    bounds = list(csv.DictReader(fh))
if len(bounds) != 4:
    raise SystemExit("bounds row count mismatch")
for row in bounds:
    if float(row["total_logabs_second_difference"]) >= 0:
        raise SystemExit(f"nonnegative total curvature: {row}")
    if float(row["abs_correction_over_abs_binomial"]) > 0.25:
        raise SystemExit(f"unexpectedly large correction ratio: {row}")

theorem = (BASE / "upgraded_theorem_step313.tex").read_text()
for needle in ["not upgraded to rigorous status", "Gaussian magnitude saddle", "remaining load-bearing gap"]:
    if needle not in theorem:
        raise SystemExit(f"theorem missing: {needle}")

print("STEP313_CHECKS_PASS")

