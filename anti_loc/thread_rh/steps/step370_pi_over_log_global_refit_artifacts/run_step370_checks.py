#!/usr/bin/env python3
"""Validator for Step 370 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step370_pi_over_log_global_refit_artifacts")
REQUIRED = [
    "three_model_fits_step370.csv",
    "per_zero_predictions_step370.csv",
    "per_zero_A_j_local_step370.csv",
    "step370_results_summary.md",
    "step370_schema.json",
    "nonclaim_boundary_step370.md",
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

    fits = read_csv("three_model_fits_step370.csv")
    pred = read_csv("per_zero_predictions_step370.csv")
    local = read_csv("per_zero_A_j_local_step370.csv")
    schema = json.loads((ART / "step370_schema.json").read_text(encoding="utf-8"))
    boundary = (ART / "nonclaim_boundary_step370.md").read_text(encoding="utf-8")

    models = {r["model"] for r in fits}
    require({"M1_constant_A_baseline", "M2_bare_pi_over_log", "M3_scaled_pi_over_log"}.issubset(models), "missing model rows")
    require(len(pred) == 45, f"expected 45 per-zero prediction rows, got {len(pred)}")
    require(len(local) == 15, f"expected 15 local A_j rows, got {len(local)}")
    require(schema["n_rows"] == 15, "schema n_rows mismatch")
    require(schema["M2_RMSE"] > 0, "M2 RMSE must be positive")
    require(schema["M1_RMSE"] > 0, "M1 RMSE must be positive")
    require(schema["local_Aj_rel_err_stats"]["mean"] >= 0, "local A_j mean rel err invalid")
    require("does not prove RH" in boundary, "nonclaim boundary missing RH disclaimer")

    print("STEP370_VALIDATION_OK")
    print(f"M2_RMSE_ratio_vs_M1={schema['M2_RMSE_ratio_vs_M1']:.12e}")
    print(f"verdict={schema['final_verdict']}")


if __name__ == "__main__":
    main()
