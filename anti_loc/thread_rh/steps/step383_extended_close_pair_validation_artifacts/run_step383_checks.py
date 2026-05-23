#!/usr/bin/env python3
"""Validate Step 383 extended close-pair validation artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step383_extended_close_pair_validation_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP383_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "gamma_R_table_100_zeros_step383.csv",
        "fits_step383.csv",
        "step383_results_summary.md",
        "step383_schema.json",
        "nonclaim_boundary_step383.md",
        "run_step383_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    table = rows("gamma_R_table_100_zeros_step383.csv")
    fits = rows("fits_step383.csv")
    require(len(table) == 100, f"expected 100 gamma rows, got {len(table)}")
    require(len(fits) == 3, f"expected 3 fit rows, got {len(fits)}")
    require([int(r["j"]) for r in table] == list(range(1, 101)), "gamma table j sequence mismatch")

    main_fit = fits[0]
    require(main_fit["model"] == "R=a+b/s_min", "first fit is not main model")
    require(float(main_fit["slope_rel_err_vs_pi2"]) > 0.10, "slope unexpectedly within 10 percent")
    require(float(main_fit["offset_rel_err_vs_minus_3pi_over_2"]) > 0.10, "offset unexpectedly within 10 percent")
    require(abs(float(main_fit["pearson_r"])) < 0.3, "main correlation unexpectedly strong")

    schema = json.loads((BASE / "step383_schema.json").read_text())
    require(schema["dps"] >= 80, "dps below hard constraint")
    require(schema["n_computed"] == 100, "schema n mismatch")
    require(schema["verdict"] == "slope_or_offset_drift_reformulate", "schema verdict mismatch")

    boundary = (BASE / "nonclaim_boundary_step383.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("raw delta proxy" in boundary, "missing proxy caveat")

    print("STEP383_CHECK_PASS")
    print("n=100")
    print(f"a={float(main_fit['intercept_a']):.12g}")
    print(f"b={float(main_fit['slope_b_inv_s']):.12g}")
    print(f"r={float(main_fit['pearson_r']):.12g}")


if __name__ == "__main__":
    main()
