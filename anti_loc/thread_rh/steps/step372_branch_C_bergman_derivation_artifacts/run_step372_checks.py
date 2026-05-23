#!/usr/bin/env python3
"""Validator for Step 372 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step372_branch_C_bergman_derivation_artifacts")
REQUIRED = [
    "bergman_kernel_derivation_step372.md",
    "saddle_solution_step372.md",
    "derived_gamma_vs_empirical_step372.csv",
    "step372_results_summary.md",
    "step372_schema.json",
    "nonclaim_boundary_step372.md",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    for name in REQUIRED:
        path = ART / name
        require(path.exists(), f"missing {name}")
        require(path.stat().st_size > 0, f"empty {name}")
    rows = list(csv.DictReader((ART / "derived_gamma_vs_empirical_step372.csv").open(newline="", encoding="utf-8")))
    schema = json.loads((ART / "step372_schema.json").read_text(encoding="utf-8"))
    deriv = (ART / "bergman_kernel_derivation_step372.md").read_text(encoding="utf-8")
    boundary = (ART / "nonclaim_boundary_step372.md").read_text(encoding="utf-8")
    require(len(rows) == 15, f"expected 15 comparison rows, got {len(rows)}")
    require(schema["literal_formula_finite_saddle"] is False, "literal saddle should be marked false")
    require("no finite saddle" in schema["literal_formula_issue"], "schema should surface no finite saddle")
    require("P_infty" in deriv, "projector mismatch should be documented")
    require("does not prove RH" in boundary, "nonclaim boundary missing RH disclaimer")
    print("STEP372_VALIDATION_OK")
    print(f"verdict={schema['final_verdict']}")


if __name__ == "__main__":
    main()
