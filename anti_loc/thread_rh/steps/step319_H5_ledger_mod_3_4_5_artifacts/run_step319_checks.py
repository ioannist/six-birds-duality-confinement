#!/usr/bin/env python3
import csv
import json
from pathlib import Path

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step319_H5_ledger_mod_3_4_5_artifacts")
required = [
    "derive_H5_ledger_step319.py",
    "H5_ledger_table_step319.csv",
    "functional_equation_verification_step319.csv",
    "step319_results_summary.md",
    "step319_schema.json",
    "nonclaim_boundary_step319.md",
]
for name in required:
    path = BASE / name
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty required artifact: {path}")

schema = json.loads((BASE / "step319_schema.json").read_text())
if schema.get("step") != 319:
    raise SystemExit("schema step mismatch")
if schema.get("final_verdict") != "V_H5_mod_3_4_5_ledger_constructed_subfamily_score_2_5":
    raise SystemExit("unexpected verdict")

with (BASE / "H5_ledger_table_step319.csv").open(newline="", encoding="utf-8") as fh:
    ledger = list(csv.DictReader(fh))
if len(ledger) != 4:
    raise SystemExit("ledger should have four characters")
chars = {row["character"]: row for row in ledger}
for ch in ["chi_3", "chi_4", "chi_5a", "chi_5b"]:
    if ch not in chars:
        raise SystemExit(f"missing character {ch}")
if chars["chi_3"]["conductor"] != "3" or chars["chi_4"]["conductor"] != "4":
    raise SystemExit("bad conductor for chi_3/chi_4")
if chars["chi_5a"]["parity_a"] != "0" or chars["chi_5b"]["parity_a"] != "1":
    raise SystemExit("bad parity for mod 5 characters")

with (BASE / "functional_equation_verification_step319.csv").open(newline="", encoding="utf-8") as fh:
    ver = list(csv.DictReader(fh))
if len(ver) != 4:
    raise SystemExit("FE verification should have four rows")
for row in ver:
    if float(row["relative_error_L"]) > 1e-40:
        raise SystemExit(f"FE relative error too high: {row}")

summary = (BASE / "step319_results_summary.md").read_text()
for needle in ["score 2.5", "Iwaniec-Kowalski", "Final verdict"]:
    if needle not in summary:
        raise SystemExit(f"summary missing: {needle}")

print("STEP319_CHECKS_PASS")

