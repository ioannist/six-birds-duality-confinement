#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "hadamard_predictions_L_chi3_step411.csv",
    "cross_L_analytical_universality_step411.md",
    "step411_results_summary.md",
    "step411_schema.json",
    "nonclaim_boundary_step411.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

rows = list(csv.DictReader((ROOT / "hadamard_predictions_L_chi3_step411.csv").open()))
if len(rows) != 50:
    raise SystemExit(f"expected 50 prediction rows, found {len(rows)}")

exceptions = [r for r in rows if r["is_exception"] == "True"]
nonexceptions = [r for r in rows if r["is_exception"] == "False"]
if [r["j"] for r in exceptions] != ["39", "48"]:
    raise SystemExit(f"unexpected exceptions: {[r['j'] for r in exceptions]}")

exc_match = sum(r["prediction_correct"] == "True" for r in exceptions)
non_match = sum(r["prediction_correct"] == "True" for r in nonexceptions)
overall = sum(r["prediction_correct"] == "True" for r in rows)
pred_pos = sum(r["predicted_sign_Re_L_double_prime"] == "1" for r in rows)

if exc_match != 2:
    raise SystemExit("exception match failed")
if non_match != 10:
    raise SystemExit(f"unexpected nonexception match count: {non_match}")
if overall != 12:
    raise SystemExit(f"unexpected overall match count: {overall}")
if pred_pos != 40:
    raise SystemExit(f"unexpected predicted positive count: {pred_pos}")

print("Step 411 checks passed.")
print(f"exception_match={exc_match}/2")
print(f"nonexception_match={non_match}/48")
print(f"overall_match={overall}/50")
