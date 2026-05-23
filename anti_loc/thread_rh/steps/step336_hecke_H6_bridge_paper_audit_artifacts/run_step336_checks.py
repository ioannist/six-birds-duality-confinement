#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import sys

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step336_hecke_H6_bridge_paper_audit_artifacts")
REQUIRED = [
    "fetched_sources_step336.csv",
    "paper_extracts_step336.md",
    "H6_bridge_status_step336.csv",
    "step336_results_summary.md",
    "step336_schema.json",
    "nonclaim_boundary_step336.md",
    "run_step336_checks.py",
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

schema = json.loads((BASE / "step336_schema.json").read_text())
if schema.get("step") != 336:
    fail("schema step is not 336")
if schema.get("final_verdict") != "V_hecke_H6_no_bridge_found_V_NC_paper_audited":
    fail("unexpected final verdict")
if schema.get("bridge_theorem_found") is not False:
    fail("bridge theorem flag should be false")

with (BASE / "H6_bridge_status_step336.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
if len(rows) < 7:
    fail("H6 bridge status table has too few rows")
if not any(row["subclaim_or_source"] == "Overall H6" for row in rows):
    fail("missing Overall H6 row")

extract = (BASE / "paper_extracts_step336.md").read_text()
for marker in [
    "Connes-Consani",
    "Bost-Connes",
    "Burnol",
    "Meyer",
    "Hecke-side conclusion => Burnol/Sonine zeta residual conclusion",
]:
    if marker not in extract:
        fail(f"missing extract marker {marker}")

summary = (BASE / "step336_results_summary.md").read_text()
if "No RH or Hecke closure claim is made" not in summary:
    fail("summary missing nonclaim sentence")

print("PASS: Step 336 artifacts validate")
