#!/usr/bin/env python3
"""Validator for Step 373 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step373_hecke_asymptotic_structural_alignment_artifacts")
REQUIRED = [
    "hecke_gamma_extraction_step373.csv",
    "hecke_3model_fits_step373.csv",
    "ζ_vs_Hecke_structural_alignment_step373.md",
    "step373_results_summary.md",
    "step373_schema.json",
    "nonclaim_boundary_step373.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for name in REQUIRED:
        path = ART / name
        require(path.exists(), f"missing {name}")
        require(path.stat().st_size > 0, f"empty {name}")
    gamma = read_csv("hecke_gamma_extraction_step373.csv")
    fits = read_csv("hecke_3model_fits_step373.csv")
    schema = json.loads((ART / "step373_schema.json").read_text(encoding="utf-8"))
    boundary = (ART / "nonclaim_boundary_step373.md").read_text(encoding="utf-8")
    require(len(gamma) == 7, f"expected 7 Hecke gamma cells, got {len(gamma)}")
    require(len(fits) >= 3, f"expected at least 3 fit rows, got {len(fits)}")
    require(schema["d_Hecke_available"] is False, "schema should record missing d_Hecke")
    require(schema["T_le_2pi_count"] == 5, "expected five Hecke heights at/below 2pi")
    require(schema["M2_RMSE_ratio_vs_M1"] > 3.0, "M2 should fail relative to M1")
    require("does not prove RH" in boundary, "nonclaim boundary missing RH disclaimer")
    print("STEP373_VALIDATION_OK")
    print(f"verdict={schema['final_verdict']}")
    print(f"M2_ratio={schema['M2_RMSE_ratio_vs_M1']:.12e}")


if __name__ == "__main__":
    main()
