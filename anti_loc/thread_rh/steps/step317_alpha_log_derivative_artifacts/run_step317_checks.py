#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step317_alpha_log_derivative_artifacts")
required = [
    "compute_L_j_log_derivatives_step317.py",
    "L_j_values_step317.csv",
    "xi_via_L_j_step317.csv",
    "alpha_pair_correlation_connection_step317.csv",
    "step317_results_summary.md",
    "step317_schema.json",
    "nonclaim_boundary_step317.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step317_schema.json").read_text())
if schema.get("step") != 317:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_alpha_log_derivative_power_sum_partial_pair_correlation_indirect":
    raise SystemExit("unexpected verdict")

with (BASE / "L_j_values_step317.csv").open(newline="", encoding="utf-8") as fh:
    lrows = list(csv.DictReader(fh))
if len(lrows) < 30:
    raise SystemExit("L_j table too short")
if float(lrows[9]["zero_sum_rel_error_vs_D_j"]) > 1e-8:
    raise SystemExit("expected good zero-sum approximation by j=10")

with (BASE / "xi_via_L_j_step317.csv").open(newline="", encoding="utf-8") as fh:
    xrows = list(csv.DictReader(fh))
if len(xrows) < 8:
    raise SystemExit("xi reconstruction table too short")
for row in xrows:
    if float(row["relative_error"]) > 1e-40:
        raise SystemExit(f"xi reconstruction error too high: {row}")

with (BASE / "alpha_pair_correlation_connection_step317.csv").open(newline="", encoding="utf-8") as fh:
    arows = list(csv.DictReader(fh))
if len(arows) != 4:
    raise SystemExit("alpha connection row count mismatch")
for row in arows:
    if abs(float(row["rho2_gap_abs"]) - 6.88731449703686) > 1e-9:
        raise SystemExit(f"rho2 gap mismatch: {row}")

summary = (BASE / "step317_results_summary.md").read_text()
for needle in ["indirect Montgomery-pair-correlation connection", "Bell-polynomial asymptotics", "Final verdict"]:
    if needle not in summary:
        raise SystemExit(f"summary missing: {needle}")

print("STEP317_CHECKS_PASS")

