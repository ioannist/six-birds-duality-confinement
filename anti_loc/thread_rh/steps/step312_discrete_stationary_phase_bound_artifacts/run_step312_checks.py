#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step312_discrete_stationary_phase_bound_artifacts")
required = [
    "extract_alpha_sigma_step312.py",
    "alpha_sigma_per_k_step312.csv",
    "stationary_phase_interference_step312.csv",
    "derived_C0_C1_step312.csv",
    "updated_theorem_step312.tex",
    "step312_results_summary.md",
    "step312_schema.json",
    "nonclaim_boundary_step312.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step312_schema.json").read_text())
if schema.get("step") != 312:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_discrete_stationary_phase_matches_empirical_interference_but_not_rigorous":
    raise SystemExit("unexpected verdict")

with (BASE / "alpha_sigma_per_k_step312.csv").open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
if len(rows) != 4:
    raise SystemExit("alpha/sigma row count mismatch")
for row in rows:
    if float(row["central_linear_R2"]) < 0.99:
        raise SystemExit(f"central R2 too low: {row}")
    if float(row["alpha_squared_sigma_weighted_squared_over_2"]) <= 0:
        raise SystemExit(f"nonpositive exponent: {row}")

with (BASE / "stationary_phase_interference_step312.csv").open(newline="", encoding="utf-8") as fh:
    sp = list(csv.DictReader(fh))
if len(sp) != 4:
    raise SystemExit("stationary-phase row count mismatch")
for row in sp:
    if float(row["abs_rel_err_weighted"]) > 0.02:
        raise SystemExit(f"stationary-phase error too high: {row}")

with (BASE / "derived_C0_C1_step312.csv").open(newline="", encoding="utf-8") as fh:
    bounds = list(csv.DictReader(fh))
if not any(row["bound_type"] == "conservative_sample_bound" and row["C1"] == "0.028" for row in bounds):
    raise SystemExit("missing conservative sample bound")
if not any(row["rigor_status"] == "finite_range_empirical_not_theorem" for row in bounds):
    raise SystemExit("missing non-rigorous status")

summary = (BASE / "step312_results_summary.md").read_text()
for needle in [
    "matches the empirical interference ratios",
    "not theorem-grade",
    "Final verdict",
]:
    if needle not in summary:
        raise SystemExit(f"summary missing: {needle}")

print("STEP312_CHECKS_PASS")

