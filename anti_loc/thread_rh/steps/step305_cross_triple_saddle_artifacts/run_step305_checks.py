#!/usr/bin/env python3
"""Validator for Step 305 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step305_cross_triple_saddle_artifacts")
REQUIRED = [
    "compute_certified_step305.py",
    "certified_delta_Dk_rho2_Gstar_step305.csv",
    "certified_delta_Dk_rho1_Gprime_step305.csv",
    "saddle_fits_per_triple_step305.csv",
    "gamma_zero_robustness_step305.csv",
    "step305_results_summary.md",
    "step305_schema.json",
    "nonclaim_boundary_step305.md",
    "run_step305_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP305_ARTIFACTS {missing}")
    for name in ["certified_delta_Dk_rho2_Gstar_step305.csv", "certified_delta_Dk_rho1_Gprime_step305.csv"]:
        data = rows(name)
        if {int(r["k"]) for r in data} != {10, 20, 30, 50}:
            raise SystemExit(f"BAD_K_SET {name}")
        if any(float(r["delta_Dk_abs_dps80"]) <= 0 for r in data):
            raise SystemExit(f"NONPOSITIVE_DELTA {name}")
    fits = rows("saddle_fits_per_triple_step305.csv")
    if len(fits) != 6:
        raise SystemExit("BAD_FIT_ROW_COUNT")
    robust = rows("gamma_zero_robustness_step305.csv")
    if {r["triple_id"] for r in robust} != {"rho1_G_star", "rho2_G_star", "rho1_G_prime"}:
        raise SystemExit("BAD_ROBUST_TRIPLES")
    schema = json.loads((ART / "step305_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 305:
        raise SystemExit("BAD_SCHEMA_STEP")
    if schema.get("mellin_convention") != "inherited t^{-z}":
        raise SystemExit("BAD_CONVENTION")
    print("STEP305_CHECKS_PASS")


if __name__ == "__main__":
    main()
