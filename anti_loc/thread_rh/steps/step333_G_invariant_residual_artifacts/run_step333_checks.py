#!/usr/bin/env python3
"""Validator for Step 333 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step333_G_invariant_residual_artifacts")
REQUIRED = [
    "compute_residuals_step333.py",
    "height_fits_per_G_step333.csv",
    "residuals_per_G_step333.csv",
    "residual_correlation_step333.csv",
    "step333_results_summary.md",
    "step333_schema.json",
    "nonclaim_boundary_step333.md",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")
    schema = json.loads((ART / "step333_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 333:
        raise SystemExit("schema step mismatch")
    height = read_csv("height_fits_per_G_step333.csv")
    residuals = read_csv("residuals_per_G_step333.csv")
    corr = read_csv("residual_correlation_step333.csv")
    if len(height) != 2:
        raise SystemExit("expected two height fits")
    if len(residuals) != 15:
        raise SystemExit(f"expected 15 residual rows, got {len(residuals)}")
    if not corr or corr[0]["metric"] != "Pearson_R_G_star_R_G_prime":
        raise SystemExit("missing Pearson row")
    print("STEP333_CHECKS_PASS")
    print(f"residual_pearson={float(corr[0]['value']):.6g} verdict={corr[0]['verdict']}")


if __name__ == "__main__":
    main()
