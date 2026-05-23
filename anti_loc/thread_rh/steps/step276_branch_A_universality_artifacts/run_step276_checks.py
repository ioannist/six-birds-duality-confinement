#!/usr/bin/env python3
"""Validator for Step 276 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step276_branch_A_universality_artifacts")

REQUIRED = [
    "step276_results_summary.md",
    "step276_schema.json",
    "content_classification_step276.csv",
    "nonclaim_boundary_step276.md",
    "step276_branch_A_universality.tex",
    "compute_phi_max_sweep_step276.py",
    "compute_phi_max_filter_step276.py",
    "compute_step276_output.txt",
    "run_step276_checks.py",
    "phi_max_sweep_step276.csv",
    "filter_family_step276.csv",
    "universality_assessment_step276.csv",
    "residual_tree_step276.csv",
    "route_status_step276.csv",
    "construction_tasks_step276.csv",
    "classical_theorems_cited_step276.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step276_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 276
    assert schema["orientation"] == "numerical_extension"
    assert schema["target"] == "Branch A essential-norm universality"
    assert schema["final_verdict"] == "V_branch_A_essential_norm_family_specific"

    sweep = read_csv("phi_max_sweep_step276.csv")
    assert len(sweep) == 80, len(sweep)
    best = max(sweep, key=lambda row: float(row["Phi"]))
    assert best["sigma"] == "0.35000000"
    assert best["ell"] == "2.00000000"
    assert abs(float(best["Phi"]) - 0.4904766200298252) < 1e-12

    filters = read_csv("filter_family_step276.csv")
    assert len(filters) >= 4
    values = {row["filter_family"]: float(row["Phi"]) for row in filters}
    assert "burnol_sonine_pswf24_baseline" in values
    assert "smoothed_step_sinc_gaussian_edge" in values
    assert values["burnol_sonine_pswf24_baseline"] - values["smoothed_step_sinc_gaussian_edge"] > 0.02

    cited = "\n".join(row["source"] + row["quote"] for row in read_csv("classical_theorems_cited_step276.csv"))
    assert "Burnol" in cited
    assert "Phi_max = 0.49047661902424095" in cited

    output = (ART / "compute_step276_output.txt").read_text(encoding="utf-8")
    assert "final_verdict=V_branch_A_essential_norm_family_specific" in output

    print("run_step276_checks.py PASS")


if __name__ == "__main__":
    main()
