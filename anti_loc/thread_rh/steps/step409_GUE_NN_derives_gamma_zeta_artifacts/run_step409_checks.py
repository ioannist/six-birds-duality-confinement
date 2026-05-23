#!/usr/bin/env python3
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "gue_moments_step409.csv",
    "derivation_chain_step409.md",
    "step409_results_summary.md",
    "step409_schema.json",
    "nonclaim_boundary_step409.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

rows = list(csv.DictReader((ROOT / "gue_moments_step409.csv").open()))
lookup = {row["quantity"]: float(row["value"]) for row in rows}

if abs(lookup["normalization"] - 1.0) > 1e-12:
    raise SystemExit("normalization check failed")
if abs(lookup["mean_spacing"] - 1.0) > 1e-12:
    raise SystemExit("mean spacing check failed")

T1 = lookup["T1"]
expected = math.pi / (T1 * math.log(T1 / (2 * math.pi)))
if abs(lookup["gamma_GUE_T1"] - expected) > 1e-12:
    raise SystemExit("gamma T1 check failed")

summary = (ROOT / "step409_results_summary.md").read_text()
if "RMT-natural" not in summary:
    raise SystemExit("summary verdict missing")

print("Step 409 checks passed.")
print(f"mean_spacing={lookup['mean_spacing']}")
print(f"gamma_GUE_T1={lookup['gamma_GUE_T1']}")
