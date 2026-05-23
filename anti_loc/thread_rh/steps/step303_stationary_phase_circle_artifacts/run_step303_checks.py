#!/usr/bin/env python3
"""Validator for Step 303 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step303_stationary_phase_circle_artifacts")
REQUIRED = [
    "compute_stationary_phase_step303.py",
    "stationary_phase_points_step303.csv",
    "predicted_via_stationary_phase_step303.csv",
    "step303_results_summary.md",
    "step303_schema.json",
    "nonclaim_boundary_step303.md",
    "run_step303_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP303_ARTIFACTS {missing}")
    pred = rows("predicted_via_stationary_phase_step303.csv")
    if {int(r["k"]) for r in pred} != {10, 20, 30, 50}:
        raise SystemExit("BAD_PRED_K_SET")
    if any(int(r["stationary_point_count"]) < 0 for r in pred):
        raise SystemExit("BAD_STATIONARY_COUNT")
    if any(float(r["certified_delta_abs"]) <= 0 for r in pred):
        raise SystemExit("BAD_CERTIFIED")
    points = rows("stationary_phase_points_step303.csv")
    if not points:
        raise SystemExit("NO_STATIONARY_POINTS_ANY_K")
    if any(float(r["Phi_pp_abs"]) <= 0 for r in points):
        raise SystemExit("BAD_PHI_PP")
    schema = json.loads((ART / "step303_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 303:
        raise SystemExit("BAD_SCHEMA_STEP")
    if schema.get("mellin_convention") != "inherited t^{-z}":
        raise SystemExit("BAD_CONVENTION")
    print("STEP303_CHECKS_PASS")


if __name__ == "__main__":
    main()
