#!/usr/bin/env python3
"""Validator for Step 302 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step302_saddle_width_correction_artifacts")
REQUIRED = [
    "compute_saddle_width_correction_step302.py",
    "z_max_and_phi_pp_step302.csv",
    "predicted_corrected_step302.csv",
    "step302_results_summary.md",
    "step302_schema.json",
    "nonclaim_boundary_step302.md",
    "run_step302_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP302_ARTIFACTS {missing}")
    zrows = rows("z_max_and_phi_pp_step302.csv")
    prows = rows("predicted_corrected_step302.csv")
    if {int(r["k"]) for r in zrows} != {10, 20, 30, 50}:
        raise SystemExit("BAD_ZMAX_K_SET")
    if {int(r["k"]) for r in prows} != {10, 20, 30, 50}:
        raise SystemExit("BAD_PRED_K_SET")
    if any(float(r["phi_pp_abs"]) <= 0 for r in zrows):
        raise SystemExit("NONPOSITIVE_PHI_PP")
    if any(float(r["predicted_corrected"]) <= 0 or float(r["certified_delta_abs"]) <= 0 for r in prows):
        raise SystemExit("NONPOSITIVE_PRED_OR_CERT")
    schema = json.loads((ART / "step302_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 302:
        raise SystemExit("BAD_SCHEMA_STEP")
    if schema.get("mellin_convention") != "inherited t^{-z}":
        raise SystemExit("BAD_CONVENTION")
    print("STEP302_CHECKS_PASS")


if __name__ == "__main__":
    main()
