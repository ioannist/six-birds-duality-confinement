#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "L_chi4_zeros_and_sign_step412.csv",
    "L_chi5_zeros_and_sign_step412.csv",
    "hadamard_predictions_multi_step412.csv",
    "cross_selberg_summary_step412.md",
    "step412_results_summary.md",
    "step412_schema.json",
    "nonclaim_boundary_step412.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

def load(name):
    return list(csv.DictReader((ROOT / name).open()))

chi4 = load("L_chi4_zeros_and_sign_step412.csv")
chi5 = load("L_chi5_zeros_and_sign_step412.csv")
multi = load("hadamard_predictions_multi_step412.csv")

if len(chi4) != 30:
    raise SystemExit(f"expected 30 chi4 rows, found {len(chi4)}")
if len(chi5) != 30:
    raise SystemExit(f"expected 30 chi5 rows, found {len(chi5)}")
if len(multi) != 60:
    raise SystemExit(f"expected 60 multi rows, found {len(multi)}")

def stats(rows):
    exc = [r for r in rows if r["is_exception"] == "True"]
    non = [r for r in rows if r["is_exception"] == "False"]
    return {
        "exceptions": len(exc),
        "exception_matches": sum(r["prediction_correct"] == "True" for r in exc),
        "non_matches": sum(r["prediction_correct"] == "True" for r in non),
        "pred_pos": sum(r["predicted_sign_Re_L_double_prime"] == "1" for r in rows),
        "exception_j": [r["j"] for r in exc],
    }

s4 = stats(chi4)
s5 = stats(chi5)

if s4["exceptions"] != 1 or s4["exception_matches"] != 0 or s4["exception_j"] != ["30"]:
    raise SystemExit(f"unexpected chi4 stats: {s4}")
if s5["exceptions"] != 3 or s5["exception_matches"] != 3 or s5["exception_j"] != ["11", "22", "28"]:
    raise SystemExit(f"unexpected chi5 stats: {s5}")

aggregate_matches = 7 + 2 + s4["exception_matches"] + s5["exception_matches"]
aggregate_total = 7 + 2 + s4["exceptions"] + s5["exceptions"]
rate = aggregate_matches / aggregate_total
if aggregate_matches != 12 or aggregate_total != 13:
    raise SystemExit("aggregate mismatch")

print("Step 412 checks passed.")
print(f"chi4_exception_match={s4['exception_matches']}/{s4['exceptions']}")
print(f"chi5_exception_match={s5['exception_matches']}/{s5['exceptions']}")
print(f"aggregate_exception_match={aggregate_matches}/{aggregate_total} ({rate:.6f})")
