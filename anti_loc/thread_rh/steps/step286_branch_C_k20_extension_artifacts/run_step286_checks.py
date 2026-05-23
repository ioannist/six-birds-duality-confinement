#!/usr/bin/env python3
"""Validate Step 286 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step286_branch_C_k20_extension_artifacts")


REQUIRED = [
    "step286_results_summary.md",
    "step286_schema.json",
    "content_classification_step286.csv",
    "nonclaim_boundary_step286.md",
    "step286_branch_C_k20.tex",
    "compute_branch_C_k_10_15_20_step286.py",
    "compute_step286_output.txt",
    "run_step286_checks.py",
    "extended_dataset_step286.csv",
    "exponential_fit_extended_step286.csv",
    "residual_high_k_step286.csv",
    "saddle_check_step286.csv",
    "residual_tree_step286.csv",
    "route_status_step286.csv",
    "construction_tasks_step286.csv",
    "classical_theorems_cited_step286.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step286_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 286
    assert schema["mpmath_dps_attempted"] >= 80
    assert schema["final_verdict"] == "V_branch_C_k20_partial"
    assert schema["high_k_values_status"] == "model_probe_not_certified"

    data = read_csv("extended_dataset_step286.csv")
    assert len(data) == 33, f"expected 33 rows, got {len(data)}"
    for triple in ["rho1_G_star", "rho2_G_star", "rho1_G_prime"]:
        ks = sorted(int(r["k"]) for r in data if r["triple_id"] == triple)
        assert ks == [0, 1, 2, 3, 4, 5, 6, 7, 10, 15, 20], (triple, ks)
    high = [r for r in data if int(r["k"]) in [10, 15, 20]]
    assert all(r["method"] == "model_probe_step286_full_projection_timeout_not_certified" for r in high)

    fits = read_csv("exponential_fit_extended_step286.csv")
    assert len(fits) == 3
    assert all(r["fit_status"] == "k0_7_fit_only" for r in fits)

    residuals = read_csv("residual_high_k_step286.csv")
    assert len(residuals) == 9
    assert all(r["diagnostic"] == "projection_timeout" for r in residuals)

    output = (ART / "compute_step286_output.txt").read_text(encoding="utf-8")
    assert "status=partial_projection_timeout" in output
    assert "verdict=V_branch_C_k20_partial" in output

    print("Step 286 checks passed")


if __name__ == "__main__":
    main()
