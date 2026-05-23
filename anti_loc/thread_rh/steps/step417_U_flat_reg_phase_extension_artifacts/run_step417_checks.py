#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "U_flat_reg_phase_design_step417.md",
    "R_phase_hadamard_rule_step417.md",
    "joint_mag_phase_residual_step417.csv",
    "SAU_6_of_6_check_step417.csv",
    "C5_C6_C8_satisfaction_step417.md",
    "step417_results_summary.md",
    "mode_b_constraint_ledger_step417_snapshot.csv",
    "mode_b_target_lineage_step417_snapshot.csv",
    "step417_schema.json",
    "nonclaim_boundary_step417.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

sau = list(csv.DictReader((ROOT / "SAU_6_of_6_check_step417.csv").open()))
if len(sau) != 6 or any(r["status"] != "pass" for r in sau):
    raise SystemExit("SAU check failed")

rows = list(csv.DictReader((ROOT / "joint_mag_phase_residual_step417.csv").open()))
lookup = {r["row_type"]: float(r["error_value"]) for r in rows}
if abs(lookup["joint_train"] - 0.06638935814747417) > 1e-12:
    raise SystemExit("joint train mismatch")
if abs(lookup["joint_holdout"] - 0.03872616304405194) > 1e-12:
    raise SystemExit("joint holdout mismatch")
if lookup["joint_ratio"] > 1.3:
    raise SystemExit("C6 ratio failed")
if lookup["joint_train"] >= 0.5:
    raise SystemExit("C5 failed")

summary = (ROOT / "step417_results_summary.md").read_text()
if "C10 operator-certificate-open" not in summary:
    raise SystemExit("C10 residual not recorded")

print("Step 417 checks passed.")
print(f"joint_train={lookup['joint_train']}")
print(f"joint_holdout={lookup['joint_holdout']}")
print(f"ratio={lookup['joint_ratio']}")
