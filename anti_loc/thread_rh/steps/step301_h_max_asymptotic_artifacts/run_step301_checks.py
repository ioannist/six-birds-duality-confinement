#!/usr/bin/env python3
"""Validator for Step 301 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step301_h_max_asymptotic_artifacts")
REQUIRED = [
    "derive_h_max_asymptotic_step301.py",
    "h_max_at_R_scan_step301.csv",
    "R_optimal_per_k_step301.csv",
    "step301_results_summary.md",
    "step301_schema.json",
    "nonclaim_boundary_step301.md",
    "run_step301_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP301_ARTIFACTS {missing}")
    scan = rows("h_max_at_R_scan_step301.csv")
    opt = rows("R_optimal_per_k_step301.csv")
    if len(scan) < 6:
        raise SystemExit(f"BAD_SCAN_ROW_COUNT {len(scan)}")
    if {int(r["k"]) for r in opt} != {10, 20, 30, 50}:
        raise SystemExit("BAD_K_TARGETS")
    r1134 = min(scan, key=lambda r: abs(float(r["R"]) - 11.3406995042713383))
    if float(r1134["numerical_max_h"]) < 1e9:
        raise SystemExit("R1134_MAX_TOO_SMALL")
    if any(float(r["C_k_looseness_direct"]) <= 1.0 for r in opt):
        raise SystemExit("CAUCHY_DIRECT_NOT_UPPER_SCALE")
    schema = json.loads((ART / "step301_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 301:
        raise SystemExit("BAD_SCHEMA_STEP")
    if schema.get("mellin_convention") != "inherited t^{-z}":
        raise SystemExit("BAD_MELLIN_CONVENTION")
    print("STEP301_CHECKS_PASS")


if __name__ == "__main__":
    main()
