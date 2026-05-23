#!/usr/bin/env python3
"""Validate Step 343 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step343_zeta_internal_ratio_structure_artifacts")
REQUIRED = [
    "compute_L_k_zeta_zeros_step343.py",
    "zeta_ratios_step343.csv",
    "functional_form_fits_step343.csv",
    "step343_results_summary.md",
    "step343_schema.json",
    "nonclaim_boundary_step343.md",
    "run_step343_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step343_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 343
    assert schema["dps"] >= 80
    assert schema["rho_indices"] == [1, 2, 3, 4, 5]
    assert schema["k_range"] == "1..20"
    assert schema["final_verdict"] == "V_zeta_internal_ratio_no_clean_form"

    ratios = rows("zeta_ratios_step343.csv")
    assert len(ratios) == 100
    assert {int(r["rho_index"]) for r in ratios} == {1, 2, 3, 4, 5}
    assert {int(r["k"]) for r in ratios} == set(range(1, 21))

    fits = rows("functional_form_fits_step343.csv")
    assert len(fits) == 60
    assert {r["model"] for r in fits} == {
        "pure_height_ratio_r=(T/T1)^f",
        "linear_polynomial_in_T_r=a0+a1*T",
        "anchored_exponential_r=exp(g*(T-T1))",
    }
    selected = [r for r in fits if int(r["k"]) in {1, 2, 3, 5, 10, 15, 20}]
    assert min(float(r["max_relative"]) for r in selected) > 0.1

    summary = (ART / "step343_results_summary.md").read_text(encoding="utf-8")
    assert "No candidate is uniformly accurate" in summary
    nonclaim = (ART / "nonclaim_boundary_step343.md").read_text(encoding="utf-8")
    assert "No RH claim" in nonclaim
    print("Step 343 validator: PASS")


if __name__ == "__main__":
    main()
