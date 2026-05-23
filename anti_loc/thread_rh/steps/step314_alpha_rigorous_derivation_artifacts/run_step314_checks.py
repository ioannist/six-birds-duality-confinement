#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step314_alpha_rigorous_derivation_artifacts")
required = [
    "compute_alpha_via_ratios_step314.py",
    "zeta_ratio_args_step314.csv",
    "M_ratio_args_step314.csv",
    "alpha_predicted_vs_empirical_step314.csv",
    "literature_audit_step314.md",
    "updated_theorem_step314.tex",
    "step314_results_summary.md",
    "step314_schema.json",
    "nonclaim_boundary_step314.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step314_schema.json").read_text())
if schema.get("step") != 314:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_alpha_ratio_formula_verified_numerically_literature_bound_missing":
    raise SystemExit("unexpected verdict")

with (BASE / "alpha_predicted_vs_empirical_step314.csv").open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
if len(rows) != 4:
    raise SystemExit("alpha comparison row count mismatch")
for row in rows:
    if float(row["relative_error_user_abs_vs_empirical"]) > 0.07:
        raise SystemExit(f"alpha user formula error too high: {row}")

with (BASE / "zeta_ratio_args_step314.csv").open(newline="", encoding="utf-8") as fh:
    zrows = list(csv.DictReader(fh))
if len(zrows) < 50:
    raise SystemExit("zeta ratio table too short")

with (BASE / "M_ratio_args_step314.csv").open(newline="", encoding="utf-8") as fh:
    mrows = list(csv.DictReader(fh))
if len(mrows) < 50:
    raise SystemExit("M ratio table too short")

audit = (BASE / "literature_audit_step314.md").read_text()
for needle in ["Conrey--Snaith", "Hughes--Keating--O'Connell", "pointwise"]:
    if needle not in audit:
        raise SystemExit(f"audit missing: {needle}")

summary = (BASE / "step314_results_summary.md").read_text().replace("\n", " ")
for needle in ["predicted `0.4103`", "no pointwise high-order phase-ratio bound"]:
    if needle not in summary:
        raise SystemExit(f"summary missing: {needle}")

print("STEP314_CHECKS_PASS")
