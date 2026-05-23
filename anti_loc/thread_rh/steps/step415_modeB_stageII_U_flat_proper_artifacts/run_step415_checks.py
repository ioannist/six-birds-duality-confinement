#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "stage_II_reproductions_step415.csv",
    "descent_paths_step415.md",
    "independence_audit_step415.md",
    "step415_results_summary.md",
    "mode_b_constraint_ledger_step415_snapshot.csv",
    "mode_b_target_lineage_step415_snapshot.csv",
    "step415_schema.json",
    "nonclaim_boundary_step415.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

rows = list(csv.DictReader((ROOT / "stage_II_reproductions_step415.csv").open()))
if len(rows) != 3:
    raise SystemExit(f"expected 3 reproduction rows, found {len(rows)}")

for row in rows:
    if row["pass_within_5_percent"] != "yes":
        raise SystemExit(f"case failed tolerance: {row['case_id']}")
    if float(row["relative_error"]) > 0.05:
        raise SystemExit(f"relative error too high: {row['case_id']}")
    if "R_Z_load" not in row["U_flat_descent_path"]:
        raise SystemExit(f"missing R_Z_load path: {row['case_id']}")
    if "R_compare" not in row["U_flat_descent_path"]:
        raise SystemExit(f"missing R_compare path: {row['case_id']}")
    if "R_operator_audit" not in row["U_flat_descent_path"]:
        raise SystemExit(f"missing R_operator_audit path: {row['case_id']}")

audit = (ROOT / "independence_audit_step415.md").read_text()
for token in ["C1", "C2", "C4", "C5", "C6", "C8", "Gate 5", "Gate 6"]:
    if token not in audit:
        raise SystemExit(f"missing audit token: {token}")

summary = (ROOT / "step415_results_summary.md").read_text()
if "Stage II earned" not in summary:
    raise SystemExit("Stage II verdict missing")

print("Step 415 checks passed.")
print("reproduction_pass_count=3/3")
print("stage_II_verdict=earned")
