#!/usr/bin/env python3
"""Validate Step 219 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step219_essential_norm_analytical_artifacts")

REQUIRED = [
    "step219_results_summary.md",
    "step219_schema.json",
    "content_classification_step219.csv",
    "nonclaim_boundary_step219.md",
    "step219_essential_norm_analytical.tex",
    "compute_phi_step219.py",
    "fit_closed_form_step219.py",
    "run_step219_checks.py",
    "phi_values_step219.csv",
    "ell_fits_step219.csv",
    "sigma_fits_step219.csv",
    "closed_form_candidates_step219.csv",
    "residual_tree_step219.csv",
    "route_status_step219.csv",
    "construction_tasks_step219.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step219_schema.json").read_text())
    assert schema["step"] == 219
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_essential_norm_ell_dependence_numerical_pattern"

    phi = rows("phi_values_step219.csv")
    if len(phi) != 17:
        raise SystemExit(f"expected 17 phi rows, got {len(phi)}")
    ell_fits = rows("ell_fits_step219.csv")
    band = [r for r in ell_fits if r["formula"] == "band_shift_erf_sigma1_piecewise"][0]
    if float(band["rmse"]) >= 0.003:
        raise SystemExit("band-shift fit unexpectedly poor")
    if min(float(r["rmse"]) for r in ell_fits if r["status"] == "generic_fit") <= 0.01:
        raise SystemExit("generic fit unexpectedly too good")

    print("Step 219 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_essential_norm_ell_dependence_numerical_pattern")


if __name__ == "__main__":
    main()
