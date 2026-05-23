#!/usr/bin/env python3
"""Validate Step 397 artifact contract."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step397_non_close_pair_T_trend_artifacts")
REQUIRED = [
    "non_cp_delta_Dk_step397.csv",
    "trend_fits_step397.csv",
    "step397_results_summary.md",
    "step397_schema.json",
    "nonclaim_boundary_step397.md",
    "run_step397_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step397_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 397:
        raise SystemExit("schema step is not 397")
    if int(schema.get("dps", 0)) < 80:
        raise SystemExit("schema dps below 80")

    rows = read_csv("non_cp_delta_Dk_step397.csv")
    if len(rows) != int(schema["sample_size"]):
        raise SystemExit("non-CP row count does not match schema sample_size")
    if not rows:
        raise SystemExit("empty non-CP table")
    for row in rows:
        if float(row["s_min"]) <= 1.5:
            raise SystemExit(f"row j={row['j']} violates s_min > 1.5")
        if int(row["k"]) != 5:
            raise SystemExit(f"row j={row['j']} has k != 5")
        val = float(row["abs_delta_Dk_float"])
        if not math.isfinite(val) or val <= 0:
            raise SystemExit(f"bad abs_delta_Dk value at j={row['j']}")
        if "Step292 raw delta_Dk" not in row["evaluator"]:
            raise SystemExit(f"missing evaluator provenance at j={row['j']}")

    fits = read_csv("trend_fits_step397.csv")
    models = {row["model"] for row in fits}
    expected = {
        "linear_a_plus_bT",
        "quadratic_a_plus_bT_plus_cT2",
        "power_decay_a_over_T_alpha",
    }
    if models != expected:
        raise SystemExit(f"unexpected trend model set: {models}")
    for row in fits:
        rmse = float(row["rmse"])
        if not math.isfinite(rmse) or rmse < 0:
            raise SystemExit(f"bad RMSE for {row['model']}")

    nonclaim = (ART / "nonclaim_boundary_step397.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("nonclaim boundary missing No RH claim")

    print("Step 397 checks passed.")
    print(f"sample_size={len(rows)}")
    print(f"trend_models={len(fits)}")


if __name__ == "__main__":
    main()
