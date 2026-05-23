#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "L_chi7_zeros_step414.csv",
    "L_chi8_zeros_step414.csv",
    "L_chi11_zeros_step414.csv",
    "hadamard_match_summary_step414.md",
    "step414_results_summary.md",
    "step414_schema.json",
    "nonclaim_boundary_step414.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

expected = {
    "L_chi7_zeros_step414.csv": {"exceptions": 4, "matches": 4, "zeros": 30, "exception_j": ["10", "17", "25", "26"]},
    "L_chi8_zeros_step414.csv": {"exceptions": 1, "matches": 1, "zeros": 30, "exception_j": ["24"]},
    "L_chi11_zeros_step414.csv": {"exceptions": 4, "matches": 4, "zeros": 30, "exception_j": ["4", "11", "21", "28"]},
}

new_matches = 0
new_total = 0
for name, exp in expected.items():
    rows = list(csv.DictReader((ROOT / name).open()))
    if len(rows) != exp["zeros"]:
        raise SystemExit(f"{name}: expected {exp['zeros']} rows, found {len(rows)}")
    exc = [r for r in rows if r["is_exception"] == "True"]
    matches = sum(r["prediction_correct"] == "True" for r in exc)
    if len(exc) != exp["exceptions"]:
        raise SystemExit(f"{name}: expected {exp['exceptions']} exceptions, found {len(exc)}")
    if [r["j"] for r in exc] != exp["exception_j"]:
        raise SystemExit(f"{name}: unexpected exception j list {[r['j'] for r in exc]}")
    if matches != exp["matches"]:
        raise SystemExit(f"{name}: expected {exp['matches']} exception matches, found {matches}")
    missing_boundary = [r for r in rows if not r["boundary_extra_T_N_plus_1"]]
    if missing_boundary:
        raise SystemExit(f"{name}: missing boundary extra zero marker")
    new_matches += matches
    new_total += len(exc)

inherited_matches = 13
inherited_total = 13
total_matches = inherited_matches + new_matches
total = inherited_total + new_total

if new_matches != 9 or new_total != 9:
    raise SystemExit("new aggregate mismatch")
if total_matches != 22 or total != 22:
    raise SystemExit("total aggregate mismatch")

print("Step 414 checks passed.")
print(f"new_exception_match={new_matches}/{new_total}")
print(f"total_exception_match={total_matches}/{total}")
