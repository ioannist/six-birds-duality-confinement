#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step318_hecke_H5_paper_audit_artifacts")
required = [
    "fetched_references_step318.csv",
    "bombieri_2000_extract_step318.md",
    "conrey_soundararajan_extract_step318.md",
    "conrey_snaith_extract_step318.md",
    "H5_subclaim_match_step318.csv",
    "H5_status_update_step318.csv",
    "step318_results_summary.md",
    "step318_schema.json",
    "nonclaim_boundary_step318.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step318_schema.json").read_text())
if schema.get("step") != 318:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_hecke_H5_literature_framework_available_ledger_missing":
    raise SystemExit("unexpected verdict")

with (BASE / "fetched_references_step318.csv").open(newline="", encoding="utf-8") as fh:
    refs = list(csv.DictReader(fh))
if len(refs) < 4:
    raise SystemExit("too few fetched/reference rows")
if not any("Bombieri" in r["reference"] and r["accessible"] == "Y" for r in refs):
    raise SystemExit("Bombieri accessible row missing")
if not any("Conrey-Snaith" in r["reference"] and r["accessible"] == "Y" for r in refs):
    raise SystemExit("Conrey-Snaith accessible row missing")

with (BASE / "H5_subclaim_match_step318.csv").open(newline="", encoding="utf-8") as fh:
    sub = list(csv.DictReader(fh))
if len(sub) < 8:
    raise SystemExit("H5 subclaim table too short")
if not any(r["H5_sub_item"] == "Hecke L-functions" and r["match"].startswith("none") for r in sub):
    raise SystemExit("expected Hecke L-functions gap row")
if not any(r["H5_sub_item"] == "Dirichlet conductor" and "full" in r["match"] for r in sub):
    raise SystemExit("expected conductor match row")

with (BASE / "H5_status_update_step318.csv").open(newline="", encoding="utf-8") as fh:
    status = list(csv.DictReader(fh))
if status[0]["new_status"] != "framework_available_but_ledger_missing_score_1_5":
    raise SystemExit("status update mismatch")

summary = (BASE / "step318_results_summary.md").read_text()
for needle in ["H5 status update", "ledger_missing", "H1-H4"]:
    if needle not in summary:
        raise SystemExit(f"summary missing: {needle}")

print("STEP318_CHECKS_PASS")

