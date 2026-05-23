#!/usr/bin/env python3
"""Validator for Step 371 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step371_branch_C_integral_derivation_artifacts")
REQUIRED = [
    "integral_derivation_step371.md",
    "saddle_equation_step371.md",
    "derived_gamma_vs_pi_over_log_step371.csv",
    "step371_results_summary.md",
    "step371_schema.json",
    "nonclaim_boundary_step371.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    for name in REQUIRED:
        path = ART / name
        require(path.exists(), f"missing {name}")
        require(path.stat().st_size > 0, f"empty {name}")

    with (ART / "derived_gamma_vs_pi_over_log_step371.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    schema = json.loads((ART / "step371_schema.json").read_text(encoding="utf-8"))
    deriv = (ART / "integral_derivation_step371.md").read_text(encoding="utf-8")
    boundary = (ART / "nonclaim_boundary_step371.md").read_text(encoding="utf-8")

    require(len(rows) == 15, f"expected 15 numerical rows, got {len(rows)}")
    require(schema["exact_integral_available"] is True, "schema should record exact integral availability")
    require(schema["projected_kernel_large_k_asymptotic_available"] is False, "schema should record missing projected asymptotic")
    require("P_infty T_a^*" in deriv, "derivation must include projected kernel term")
    require("does not prove RH" in boundary, "nonclaim boundary missing RH disclaimer")

    print("STEP371_VALIDATION_OK")
    print(f"verdict={schema['final_verdict']}")
    print(f"rmse={schema['numerical_rmse_against_step324_gamma']:.12e}")


if __name__ == "__main__":
    main()
