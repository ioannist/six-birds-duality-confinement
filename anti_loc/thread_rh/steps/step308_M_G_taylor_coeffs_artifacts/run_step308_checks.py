#!/usr/bin/env python3
"""Validator for Step 308 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step308_M_G_taylor_coeffs_artifacts")
REQUIRED = [
    "compute_M_G_derivatives_step308.py",
    "M_G_taylor_coeffs_step308.csv",
    "leibniz_reconstruction_step308.csv",
    "j1_dominance_step308.csv",
    "step308_results_summary.md",
    "step308_schema.json",
    "nonclaim_boundary_step308.md",
    "run_step308_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP308_ARTIFACTS {missing}")
    coeffs = rows("M_G_taylor_coeffs_step308.csv")
    if len(coeffs) != 31 or {int(r["k"]) for r in coeffs} != set(range(31)):
        raise SystemExit("BAD_COEFF_K_SET")
    if any(float(r["M_derivative_abs"]) <= 0 for r in coeffs):
        raise SystemExit("ZERO_DERIVATIVE")
    recon = rows("leibniz_reconstruction_step308.csv")
    if {int(r["k"]) for r in recon} != {10, 20, 30, 50}:
        raise SystemExit("BAD_RECON_K_SET")
    if max(float(r["relative_error_abs"]) for r in recon) >= 1e-12:
        raise SystemExit("RECON_ERROR_TOO_LARGE")
    j1 = rows("j1_dominance_step308.csv")
    if any(float(r["j1_over_full_delta"]) >= 1 for r in j1):
        raise SystemExit("J1_DOMINATES_UNEXPECTEDLY")
    schema = json.loads((ART / "step308_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 308:
        raise SystemExit("BAD_SCHEMA_STEP")
    print("STEP308_CHECKS_PASS")


if __name__ == "__main__":
    main()
