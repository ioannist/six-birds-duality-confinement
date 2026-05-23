#!/usr/bin/env python3
"""Validator for Step 369 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step369_per_zero_local_refit_artifacts")

REQUIRED = [
    "L_k_per_zero_per_d_step369.csv",
    "per_zero_fits_step369.csv",
    "A_j_vs_pi_over_log_step369.csv",
    "step369_results_summary.md",
    "step369_schema.json",
    "nonclaim_boundary_step369.md",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    for name in REQUIRED:
        path = ART / name
        require(path.exists(), f"missing {name}")
        require(path.stat().st_size > 0, f"empty {name}")

    raw = read_csv("L_k_per_zero_per_d_step369.csv")
    fits = read_csv("per_zero_fits_step369.csv")
    comp = read_csv("A_j_vs_pi_over_log_step369.csv")
    schema = json.loads((ART / "step369_schema.json").read_text(encoding="utf-8"))
    boundary = (ART / "nonclaim_boundary_step369.md").read_text(encoding="utf-8")

    require(len(raw) == 75, f"expected 75 raw rows, got {len(raw)}")
    require(len(fits) == 15, f"expected 15 fit rows, got {len(fits)}")
    require(len(comp) == 15, f"expected 15 comparison rows, got {len(comp)}")
    require({r["defect_order_d"] for r in raw} == {"0"}, "raw rows should be d=0 only")
    require(
        all(r["defect_order_evaluator_support"] == "unsupported_by_step292_no_d_argument" for r in raw),
        "raw rows must surface unsupported d-axis",
    )
    require(
        all(r["A_j_status"] == "not_identifiable_no_d_variation" for r in fits),
        "all A_j fits must be marked non-identifiable",
    )
    require(
        all(r["A_j_model_comparison_status"] == "blocked_no_d_sweep" for r in comp),
        "all A_j comparisons must be blocked",
    )
    require(schema["defect_order_supported"] is False, "schema should mark defect_order_supported false")
    require(schema["per_zero_Aj_identifiable"] is False, "schema should mark per_zero_Aj_identifiable false")
    require(schema["raw_rows"] == 75, "schema raw_rows mismatch")
    require("does not prove RH" in boundary, "nonclaim boundary missing RH disclaimer")

    print("STEP369_VALIDATION_OK")
    print(f"raw_rows={len(raw)}")
    print("per_zero_Aj_identifiable=false")


if __name__ == "__main__":
    main()
