#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step311_leibniz_phase_analysis_artifacts")
K_TARGETS = [10, 20, 30, 50]

required = [
    "compute_leibniz_phases_step311.py",
    "phase_smoothness_summary_step311.csv",
    "inferred_C0_C1_step311.csv",
    "step311_results_summary.md",
    "step311_schema.json",
    "nonclaim_boundary_step311.md",
]
required += [f"leibniz_phases_k{k}_step311.csv" for k in K_TARGETS]

for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step311_schema.json").read_text())
if schema.get("step") != 311:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_leibniz_phase_smooth_but_no_direct_BV_bound":
    raise SystemExit("unexpected verdict")

for k in K_TARGETS:
    with (BASE / f"leibniz_phases_k{k}_step311.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != k + 1:
        raise SystemExit(f"k={k}: expected {k+1} phase rows, got {len(rows)}")
    for col in ["arg_raw_minus_pi_pi", "arg_unwrapped", "delta_arg_from_previous", "in_central_window"]:
        if col not in rows[0]:
            raise SystemExit(f"k={k}: missing column {col}")

with (BASE / "phase_smoothness_summary_step311.csv").open(newline="", encoding="utf-8") as fh:
    summary_rows = list(csv.DictReader(fh))
if len(summary_rows) != len(K_TARGETS):
    raise SystemExit("phase summary row count mismatch")
for row in summary_rows:
    if row["smoothness_flag"] != "smooth_near_linear_central":
        raise SystemExit(f"unexpected smoothness flag: {row}")
    if float(row["linear_R2_central"]) < 0.99:
        raise SystemExit(f"central R2 too low: {row}")
    if float(row["central_phase_variation"]) <= 0:
        raise SystemExit(f"nonpositive central phase variation: {row}")

with (BASE / "inferred_C0_C1_step311.csv").open(newline="", encoding="utf-8") as fh:
    inferred = list(csv.DictReader(fh))
if len(inferred) != len(K_TARGETS):
    raise SystemExit("inferred row count mismatch")
if not all(row["inferred_C0"] == "not_feasible" for row in inferred):
    raise SystemExit("expected not_feasible C0 entries")

summary = (BASE / "step311_results_summary.md").read_text()
for needle in [
    "not chaotic",
    "bounded-variation/cosine lower bound is not usable",
    "discrete stationary-phase",
]:
    if needle not in summary:
        raise SystemExit(f"summary missing: {needle}")

print("STEP311_CHECKS_PASS")

