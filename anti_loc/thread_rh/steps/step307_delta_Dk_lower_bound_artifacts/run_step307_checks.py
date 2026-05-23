#!/usr/bin/env python3
"""Validator for Step 307 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step307_delta_Dk_lower_bound_artifacts")
REQUIRED = [
    "compute_M_G_at_1_step307.py",
    "derive_h_order_type_step307.py",
    "lower_bound_theorem_step307.tex",
    "predicted_lower_bound_step307.csv",
    "step307_results_summary.md",
    "step307_schema.json",
    "nonclaim_boundary_step307.md",
    "run_step307_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP307_ARTIFACTS {missing}")
    mrows = rows("M_G_at_1_step307.csv")
    m1 = next((r for r in mrows if r["quantity"] == "M_G_star_1"), None)
    mrho = next((r for r in mrows if r["quantity"] == "M_G_star_rho1"), None)
    if m1 is None or mrho is None:
        raise SystemExit("MISSING_M_VALUES")
    if float(m1["abs"]) >= 1e-50:
        raise SystemExit("M_G_1_NOT_ZERO_NUMERICALLY")
    if float(mrho["abs"]) <= 1e-6:
        raise SystemExit("M_G_RHO_TOO_SMALL")
    lb = rows("predicted_lower_bound_step307.csv")
    if {int(r["k"]) for r in lb} != {5, 10, 15, 20, 30, 50}:
        raise SystemExit("BAD_LB_K_SET")
    schema = json.loads((ART / "step307_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 307:
        raise SystemExit("BAD_SCHEMA_STEP")
    if schema.get("explicit_lower_bound_derived") is not False:
        raise SystemExit("BAD_BOUND_DERIVED_FLAG")
    print("STEP307_CHECKS_PASS")


if __name__ == "__main__":
    main()
