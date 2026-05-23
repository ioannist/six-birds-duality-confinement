#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step335_hecke_H2_paper_audit_artifacts")
REQUIRED = [
    "fetched_sources_step335.csv",
    "paper_extracts_step335.md",
    "H2_subclaim_match_step335.csv",
    "step335_results_summary.md",
    "step335_schema.json",
    "nonclaim_boundary_step335.md",
    "run_step335_checks.py",
]

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

for name in REQUIRED:
    path = BASE / name
    if not path.exists():
        fail(f"missing {path}")
    if path.stat().st_size == 0:
        fail(f"empty {path}")

schema = json.loads((BASE / "step335_schema.json").read_text())
if schema.get("step") != 335:
    fail("schema step is not 335")
if schema.get("final_verdict") != "V_hecke_H2_framework_partial_available_lower_frame_missing":
    fail("unexpected final verdict")
if float(schema.get("new_score", 0)) != 1.5:
    fail("unexpected H2 score")

with (BASE / "H2_subclaim_match_step335.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
if len(rows) < 5:
    fail("H2 subclaim table has too few rows")
subclaims = {row["subclaim"] for row in rows}
for expected in [
    "source lower-frame F_n >= Lambda_n (Theta_0^-)^{-1}",
    "Lambda_n -> infinity",
    "Plancherel tail",
    "exhaustivity over conductor",
    "overall H2",
]:
    if expected not in subclaims:
        fail(f"missing subclaim {expected}")

extract = (BASE / "paper_extracts_step335.md").read_text()
for marker in [
    "Soundararajan 2000",
    "Conrey-Soundararajan 2002",
    "Asymptotic Large Sieve",
    "Khan-Ngo 2015",
]:
    if marker not in extract:
        fail(f"missing extract marker {marker}")

summary = (BASE / "step335_results_summary.md").read_text()
if "No RH, GRH, or Hecke closure claim is made" not in summary:
    fail("summary missing nonclaim sentence")

print("PASS: Step 335 artifacts validate")
