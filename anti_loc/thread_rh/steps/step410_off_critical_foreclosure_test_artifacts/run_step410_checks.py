#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "off_critical_L_k_step410.csv",
    "comparison_step410.md",
    "step410_results_summary.md",
    "step410_schema.json",
    "nonclaim_boundary_step410.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

rows = list(csv.DictReader((ROOT / "off_critical_L_k_step410.csv").open()))
if len(rows) != 4:
    raise SystemExit(f"expected 4 rows, found {len(rows)}")

threshold = 0.034
values = [float(row["abs_delta_Dk"]) for row in rows]
if min(values) <= threshold:
    raise SystemExit("unexpected threshold failure")

labels = {row["point_label"] for row in rows}
expected = {"rho_actual", "rho_off_right", "rho_off_left", "on_line_not_zero"}
if labels != expected:
    raise SystemExit(f"unexpected labels: {labels}")

summary = (ROOT / "step410_results_summary.md").read_text()
if "No foreclosure-discriminating signal" not in summary:
    raise SystemExit("summary verdict missing")

print("Step 410 checks passed.")
print(f"min_abs_delta_Dk={min(values)}")
print(f"pass_count={sum(v > threshold for v in values)}/4")
