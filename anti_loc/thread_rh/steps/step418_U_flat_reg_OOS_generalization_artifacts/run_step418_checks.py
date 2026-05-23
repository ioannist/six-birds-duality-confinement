#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required = [
    "OOS_zeros_per_char_step418.csv",
    "phase_match_OOS_step418.csv",
    "magnitude_OOS_step418.csv",
    "step418_results_summary.md",
    "mode_b_constraint_ledger_step418_snapshot.csv",
    "mode_b_target_lineage_step418_snapshot.csv",
    "step418_schema.json",
    "nonclaim_boundary_step418.md",
]

for name in required:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"missing artifact: {name}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty artifact: {name}")

phase = list(csv.DictReader((ROOT / "phase_match_OOS_step418.csv").open()))
by_char = {r["character"]: r for r in phase}

if by_char["chi_13"]["phase_match"] != "3" or by_char["chi_13"]["phase_total"] != "3":
    raise SystemExit("chi_13 phase mismatch")
if by_char["chi_15"]["phase_match"] != "1" or by_char["chi_15"]["phase_total"] != "1":
    raise SystemExit("chi_15 phase mismatch")
if "blocked" not in by_char["chi_16"]["search_note"]:
    raise SystemExit("chi_16 block not recorded")

mag = list(csv.DictReader((ROOT / "magnitude_OOS_step418.csv").open()))
if any(r["OOS_magnitude_status"] != "blocked" for r in mag):
    raise SystemExit("magnitude OOS should be blocked for all requested characters")

summary = (ROOT / "step418_results_summary.md").read_text()
if "Mixed" not in summary:
    raise SystemExit("mixed verdict missing")

print("Step 418 checks passed.")
print("phase_OOS_match=4/4 computable")
print("magnitude_OOS_status=blocked")
