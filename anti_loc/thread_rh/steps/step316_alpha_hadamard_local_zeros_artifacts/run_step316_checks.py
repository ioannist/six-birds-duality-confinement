#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step316_alpha_hadamard_local_zeros_artifacts")
required = [
    "compute_xi_derivatives_step316.py",
    "xi_derivatives_at_rho1_step316.csv",
    "hadamard_truncated_approximation_step316.csv",
    "alpha_local_zero_connection_step316.csv",
    "step316_results_summary.md",
    "step316_schema.json",
    "nonclaim_boundary_step316.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step316_schema.json").read_text())
if schema.get("step") != 316:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_alpha_hadamard_partial_local_power_sums_not_xi_derivatives":
    raise SystemExit("unexpected verdict")

with (BASE / "xi_derivatives_at_rho1_step316.csv").open(newline="", encoding="utf-8") as fh:
    xi_rows = list(csv.DictReader(fh))
if len(xi_rows) != 11:
    raise SystemExit("xi derivative row count mismatch")

with (BASE / "hadamard_truncated_approximation_step316.csv").open(newline="", encoding="utf-8") as fh:
    h_rows = list(csv.DictReader(fh))
if len(h_rows) < 50:
    raise SystemExit("Hadamard approximation table too short")
if not any(row["M"] == "20" and row["j"] == "10" and float(row["relative_error"]) > 100 for row in h_rows):
    raise SystemExit("expected local Hadamard failure at M=20,j=10")

with (BASE / "alpha_local_zero_connection_step316.csv").open(newline="", encoding="utf-8") as fh:
    conn_rows = list(csv.DictReader(fh))
if len(conn_rows) != 4:
    raise SystemExit("connection row count mismatch")
if not all(row["dominant_zero_index"] == "2" for row in conn_rows):
    raise SystemExit("expected rho_2 as dominant local zero diagnostic")
if float(conn_rows[-1]["power_sum_weight_share"]) < 0.99:
    raise SystemExit("expected high-k nearest-neighbor dominance")

summary = (BASE / "step316_results_summary.md").read_text()
for needle in ["did not approximate", "power-sum diagnostic", "Final verdict"]:
    if needle not in summary:
        raise SystemExit(f"summary missing: {needle}")

print("STEP316_CHECKS_PASS")

