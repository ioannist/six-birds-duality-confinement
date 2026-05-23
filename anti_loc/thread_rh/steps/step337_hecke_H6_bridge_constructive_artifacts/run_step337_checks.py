#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step337_hecke_H6_bridge_constructive_artifacts")
REQUIRED = [
    "compute_bridge_candidate_step337.py",
    "zeta_dirichlet_identities_step337.csv",
    "bridge_coefficient_fit_step337.csv",
    "step337_results_summary.md",
    "step337_schema.json",
    "nonclaim_boundary_step337.md",
    "run_step337_checks.py",
]

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

for name in REQUIRED:
    path = BASE / name
    if not path.exists():
        fail(f"missing {path}")
    if path.stat().st_size == 0:
        fail(f"empty {path}")

schema = json.loads((BASE / "step337_schema.json").read_text())
if schema.get("step") != 337:
    fail("schema step is not 337")
if schema.get("bridge_claimed") is not False:
    fail("bridge should not be claimed")
if schema.get("final_verdict") != "V_hecke_H6_constructive_bridge_failed_missing_carrier_descent":
    fail("unexpected final verdict")

with (BASE / "zeta_dirichlet_identities_step337.csv").open(newline="") as f:
    identity_rows = list(csv.DictReader(f))
if len(identity_rows) < 5:
    fail("too few identity rows")
if not any(row["candidate"] == "sum_H5_nonprincipal_subfamily" for row in identity_rows):
    fail("missing H5 subfamily identity test")

with (BASE / "bridge_coefficient_fit_step337.csv").open(newline="") as f:
    fit_rows = list(csv.DictReader(f))
if not any(row["row_type"] == "complex_coefficient" and row["character"] == "chi_3" for row in fit_rows):
    fail("missing complex coefficient rows")
if not any(row["row_type"] == "complex_fit_residual" and row["k"] == "10" for row in fit_rows):
    fail("missing k=10 complex residual")
if not any(row["row_type"] == "magnitude_fit_residual" and row["k"] == "1" for row in fit_rows):
    fail("missing magnitude residual rows")

summary = (BASE / "step337_results_summary.md").read_text()
for marker in [
    "Scalar identity audit",
    "Finite coefficient fit",
    "Missing element",
    "V_hecke_H6_constructive_bridge_failed_missing_carrier_descent",
]:
    if marker not in summary:
        fail(f"missing summary marker {marker}")

nonclaim = (BASE / "nonclaim_boundary_step337.md").read_text()
if "No RH or GRH claim is made" not in nonclaim:
    fail("missing RH nonclaim")

print("PASS: Step 337 artifacts validate")
