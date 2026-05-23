#!/usr/bin/env python3
"""Validate Step 250 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step250_branch_C_k_growth_law_artifacts")

REQUIRED = [
    "step250_results_summary.md",
    "step250_schema.json",
    "content_classification_step250.csv",
    "nonclaim_boundary_step250.md",
    "step250_branch_C_k_growth_law.tex",
    "derive_higher_k_kernels_step250.py",
    "compute_L_k34_step250.py",
    "fit_growth_law_step250.py",
    "compute_step250_output.txt",
    "run_step250_checks.py",
    "k_dataset_step250.csv",
    "growth_law_fits_step250.csv",
    "extrapolation_step250.csv",
    "residual_tree_step250.csv",
    "route_status_step250.csv",
    "construction_tasks_step250.csv",
    "classical_theorems_cited_step250.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        print("FAIL missing files:", ", ".join(missing))
        return 1

    schema = json.loads((ART / "step250_schema.json").read_text())
    assert schema["step"] == 250
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_branch_C_k_growth_law_exponential"
    assert len(schema["k_dataset"]) == 15

    rows = read_csv("k_dataset_step250.csv")
    assert len(rows) == 15, len(rows)
    triples = sorted({row["triple_id"] for row in rows})
    assert triples == ["rho1_G_prime", "rho1_G_star", "rho2_G_star"], triples
    for triple in triples:
        ks = sorted(int(row["k"]) for row in rows if row["triple_id"] == triple)
        assert ks == [0, 1, 2, 3, 4], (triple, ks)
        for row in rows:
            if row["triple_id"] == triple:
                assert float(row["lower_bound"]) > 0.0

    fit_rows = read_csv("growth_law_fits_step250.csv")
    models = {row["model"] for row in fit_rows if row["triple_id"] != "GLOBAL_NORMALIZED_BY_K0"}
    expected_models = {"linear", "quadratic", "exponential", "factorial", "affine_factorial", "pochhammer_1k"}
    assert expected_models <= models, models

    expo = [row for row in fit_rows if row["model"] == "exponential" and row["triple_id"] != "GLOBAL_NORMALIZED_BY_K0"]
    assert len(expo) == 3

    extrap = read_csv("extrapolation_step250.csv")
    assert len(extrap) == 6, len(extrap)
    assert {int(row["k"]) for row in extrap} == {5, 10}

    out = (ART / "compute_step250_output.txt").read_text()
    assert "k=3" in out and "k=4" in out

    print("PASS step250 artifact contract")
    print("verdict=V_branch_C_k_growth_law_exponential")
    print("dataset_rows=15 fit_rows=%d extrapolation_rows=6" % len(fit_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
