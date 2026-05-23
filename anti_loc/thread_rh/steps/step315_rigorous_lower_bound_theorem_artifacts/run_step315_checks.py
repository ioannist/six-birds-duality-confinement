#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step315_rigorous_lower_bound_theorem_artifacts")
required = [
    "derive_lower_bound_step315.py",
    "term_j_star_lower_bounds_step315.csv",
    "delta_Dk_lower_bound_step315.csv",
    "theorem_with_constants_step315.tex",
    "tightness_audit_step315.md",
    "step315_results_summary.md",
    "step315_schema.json",
    "nonclaim_boundary_step315.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step315_schema.json").read_text())
if schema.get("step") != 315:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_worst_case_alpha_theorem_blocked_invalid_interference_lower_bound":
    raise SystemExit("unexpected verdict")

with (BASE / "delta_Dk_lower_bound_step315.csv").open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
if len(rows) != 4:
    raise SystemExit("lower-bound row count mismatch")
for row in rows:
    if row["sample_check"] != "passes_finite_sample":
        raise SystemExit(f"finite sample did not pass: {row}")
    if row["proof_status"] != "not_rigorous_interference_step_invalid":
        raise SystemExit(f"unexpected proof status: {row}")
    if float(row["formal_lower_over_certified"]) >= 1:
        raise SystemExit(f"formal lower not below certified: {row}")

theorem = (BASE / "theorem_with_constants_step315.tex").read_text()
for needle in [
    "This implication is not rigorous",
    "direction issue",
    "No fully rigorous constants",
]:
    if needle not in theorem:
        raise SystemExit(f"theorem audit missing: {needle}")

summary = (BASE / "step315_results_summary.md").read_text()
if "proof step is invalid" not in summary:
    raise SystemExit("summary missing invalid-proof statement")

print("STEP315_CHECKS_PASS")
