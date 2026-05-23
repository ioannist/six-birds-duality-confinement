#!/usr/bin/env python3
"""Validate Step 389 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step389_dirichlet_close_pair_universality_artifacts")
REQUIRED = [
    "dirichlet_L_zeros_and_derivatives_step389.csv",
    "close_pair_correlation_step389.csv",
    "comparison_to_zeta_step389.md",
    "step389_results_summary.md",
    "step389_schema.json",
    "nonclaim_boundary_step389.md",
    "run_step389_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step389_schema.json").read_text())
    if schema.get("step") != 389:
        raise SystemExit("wrong step")
    if schema.get("mpmath_dps_derivative", 0) < 30:
        raise SystemExit("dps below requirement")
    if schema.get("computed_zeros", 0) < 25:
        raise SystemExit("too few zeros")

    data = rows("dirichlet_L_zeros_and_derivatives_step389.csv")
    corr = rows("close_pair_correlation_step389.csv")
    if len(data) != schema["computed_zeros"]:
        raise SystemExit("zero row count mismatch")
    if len(corr) != 1:
        raise SystemExit("expected one correlation row")

    neg = sum(1 for r in data if int(r["sign_Re_L_double_prime"]) < 0)
    pos = len(data) - neg
    if neg != schema["negative_count"] or pos != schema["nonnegative_count"]:
        raise SystemExit("sign counts mismatch")
    float(corr[0]["pearson_Re_Lpp_vs_mean_spacing_minus_smin"])
    for r in data[:5]:
        float(r["Re_L_double_prime"])
        float(r["Im_L_double_prime"])
        float(r["abs_L_double_prime_over_L_prime"])

    if "No RH claim" not in (ART / "nonclaim_boundary_step389.md").read_text():
        raise SystemExit("nonclaim missing")
    if "Step 378" not in (ART / "comparison_to_zeta_step389.md").read_text():
        raise SystemExit("comparison missing zeta baseline")

    print("step389 checks passed")


if __name__ == "__main__":
    main()
