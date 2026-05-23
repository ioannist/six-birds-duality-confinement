#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step310_lower_bound_theorem_statement_artifacts")

required = [
    "theorem_statement_step310.tex",
    "rigor_audit_per_component_step310.csv",
    "b0_saddle_match_step310.csv",
    "step310_results_summary.md",
    "step310_schema.json",
    "nonclaim_boundary_step310.md",
]

for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step310_schema.json").read_text())
if schema.get("step") != 310:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_lower_bound_theorem_statement_conditional_gap_interference":
    raise SystemExit("unexpected final verdict")

theorem = (BASE / "theorem_statement_step310.tex").read_text()
for needle in [
    "Candidate Theorem 310.A",
    "A_0=10^{-2}",
    "B_0=2.5",
    "Required Lemma 2",
    "not finite type",
]:
    if needle not in theorem:
        raise SystemExit(f"theorem missing expected text: {needle}")

with (BASE / "rigor_audit_per_component_step310.csv").open(newline="") as fh:
    rows = list(csv.DictReader(fh))
if len(rows) < 10:
    raise SystemExit("rigor audit too short")
if not any(row["status"] == "missing_load_bearing" and "interference" in row["component"].lower() for row in rows):
    raise SystemExit("missing interference load-bearing gap")
if not any(row["component"] == "Finite-type entire-function route" and row["status"] == "blocked" for row in rows):
    raise SystemExit("missing finite-type blocked audit row")

with (BASE / "b0_saddle_match_step310.csv").open(newline="") as fh:
    b_rows = list(csv.DictReader(fh))
if not any(row["quantity"] == "candidate_theorem_base_B0" and row["value"] == "2.5" for row in b_rows):
    raise SystemExit("missing candidate B0 row")
if not any(row["quantity"] == "interference_eta_fit_step309" for row in b_rows):
    raise SystemExit("missing eta row")

print("STEP310_CHECKS_PASS")

