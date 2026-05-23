#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step334_hecke_H1_paper_audit_artifacts")

REQUIRED = [
    "fetched_sources_step334.csv",
    "paper_extracts_step334.md",
    "H1_subclaim_match_step334.csv",
    "step334_results_summary.md",
    "step334_schema.json",
    "nonclaim_boundary_step334.md",
    "run_step334_checks.py",
]

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)

for name in REQUIRED:
    path = BASE / name
    if not path.exists():
        fail(f"missing {path}")
    if path.stat().st_size == 0:
        fail(f"empty {path}")

with (BASE / "step334_schema.json").open() as f:
    schema = json.load(f)
if schema.get("step") != 334:
    fail("schema step is not 334")
if schema.get("final_verdict") != "V_hecke_H1_framework_partial_available_ledger_missing":
    fail("unexpected final verdict")
if float(schema.get("new_score", 0)) != 1.5:
    fail("unexpected H1 score")

with (BASE / "H1_subclaim_match_step334.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
if len(rows) < 6:
    fail("H1 subclaim table has too few rows")
subclaims = {row["subclaim"] for row in rows}
for expected in [
    "completed Hecke response",
    "character Plancherel ledger",
    "measurable Schur fields",
    "Moore-Penrose compatibility",
    "tail/exhaustivity",
    "overall H1",
]:
    if expected not in subclaims:
        fail(f"missing subclaim {expected}")

extract = (BASE / "paper_extracts_step334.md").read_text()
for marker in [
    "Dirichlet",
    "Conrey-Iwaniec",
    "Hecke C*-algebras",
    "Schur",
    "Moore-Penrose",
]:
    if marker not in extract:
        fail(f"missing extract marker {marker}")

summary = (BASE / "step334_results_summary.md").read_text()
if "No RH, GRH, or Hecke closure claim is made" not in summary:
    fail("summary missing nonclaim sentence")

print("PASS: Step 334 artifacts validate")
