#!/usr/bin/env python3
"""Validate Step 390 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step390_dirichlet_structural_law_universality_artifacts")
REQUIRED = [
    "L_chi3_gamma_extraction_step390.csv",
    "comparison_to_predicted_structural_step390.csv",
    "step390_results_summary.md",
    "step390_schema.json",
    "nonclaim_boundary_step390.md",
    "run_step390_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step390_schema.json").read_text())
    if schema.get("step") != 390:
        raise SystemExit("wrong step")
    if schema.get("mpmath_dps", 0) < 50:
        raise SystemExit("dps below requirement")
    if schema.get("zeros_used") != 10:
        raise SystemExit("expected 10 zeros")

    gamma_rows = rows("L_chi3_gamma_extraction_step390.csv")
    comp_rows = rows("comparison_to_predicted_structural_step390.csv")
    if len(gamma_rows) != 10 or len(comp_rows) != 10:
        raise SystemExit("row count mismatch")
    for row in gamma_rows:
        float(row["gamma_L_linear_in_k"])
        float(row["fit_log_RMSE"])
        for k in [5, 10, 15, 20, 30]:
            float(row[f"k{k}_abs_delta"])
    for row in comp_rows:
        float(row["rel_err_q3"])
        float(row["rel_err_q1"])
        if row["better_predictor"] not in {"q1", "q3"}:
            raise SystemExit("bad predictor label")

    if "No RH claim" not in (ART / "nonclaim_boundary_step390.md").read_text():
        raise SystemExit("nonclaim missing")
    if "Verdict" not in (ART / "step390_results_summary.md").read_text():
        raise SystemExit("summary missing verdict")

    print("step390 checks passed")


if __name__ == "__main__":
    main()
