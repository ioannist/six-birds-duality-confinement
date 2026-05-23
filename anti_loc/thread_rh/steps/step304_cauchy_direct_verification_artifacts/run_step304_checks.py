#!/usr/bin/env python3
"""Validator for Step 304 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step304_cauchy_direct_verification_artifacts")
REQUIRED = [
    "compute_cauchy_direct_step304.py",
    "cauchy_quadrature_per_R_step304.csv",
    "step304_results_summary.md",
    "step304_schema.json",
    "nonclaim_boundary_step304.md",
    "run_step304_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP304_ARTIFACTS {missing}")
    data = rows("cauchy_quadrature_per_R_step304.csv")
    if {row["R"] for row in data} != {"3.0", "5.05999999999999961", "8.0", "11.3399999999999999", "14.0"}:
        raise SystemExit("BAD_RADIUS_SET")
    if any(int(row["N_theta"]) != 2048 for row in data):
        raise SystemExit("BAD_N_THETA")
    if max(float(row["rel_err_complex_vs_dps120"]) for row in data) >= 1e-10:
        raise SystemExit("CAUCHY_REL_ERR_TOO_LARGE")
    schema = json.loads((ART / "step304_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 304:
        raise SystemExit("BAD_SCHEMA_STEP")
    if schema.get("final_verdict") != "V_cauchy_direct_verified":
        raise SystemExit("BAD_VERDICT")
    print("STEP304_CHECKS_PASS")


if __name__ == "__main__":
    main()
