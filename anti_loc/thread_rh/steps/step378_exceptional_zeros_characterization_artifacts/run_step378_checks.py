#!/usr/bin/env python3
"""Validate Step 378 exceptional-zero characterization artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step378_exceptional_zeros_characterization_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP378_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "exceptional_zeros_features_step378.csv",
        "correlation_tests_step378.csv",
        "cluster_analysis_step378.md",
        "step378_results_summary.md",
        "step378_schema.json",
        "nonclaim_boundary_step378.md",
        "run_step378_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    exc = rows("exceptional_zeros_features_step378.csv")
    corr = rows("correlation_tests_step378.csv")
    all100 = rows("all100_features_step378.csv")
    require(len(exc) == 7, f"expected 7 exception rows, got {len(exc)}")
    require(len(corr) >= 3, "too few correlation rows")
    require(len(all100) == 100, f"expected 100 full feature rows, got {len(all100)}")
    require([r["j"] for r in exc] == ["34", "41", "64", "71", "79", "80", "92"], "unexpected exception list")
    require(all(r["sign_Re_zeta2"] == "1" for r in exc), "exception row with nonpositive sign")

    top = corr[0]
    require(top["variable"] == "mean_spacing_minus_s_min", f"unexpected top correlation {top}")
    require(float(top["pearson_r"]) > 0.7, "top correlation below expected close-pair threshold")

    mean_exc_smin = sum(float(r["s_min"]) for r in exc) / len(exc)
    nonexc = [r for r in all100 if r["is_exception"] == "False"]
    mean_nonexc_smin = sum(float(r["s_min"]) for r in nonexc) / len(nonexc)
    require(mean_exc_smin < mean_nonexc_smin, "exception s_min not smaller than non-exceptional mean")

    schema = json.loads((BASE / "step378_schema.json").read_text())
    require(schema["dps"] >= 50, "dps below hard constraint")
    require(schema["verdict"] == "close_pair_deficit_signal; not_single_T_cluster", "schema verdict mismatch")

    boundary = (BASE / "nonclaim_boundary_step378.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("empirical" in boundary, "missing empirical scope")

    print("STEP378_CHECK_PASS")
    print("exceptions=34,41,64,71,79,80,92")
    print(f"top_corr={top['variable']} r={float(top['pearson_r']):.12g}")
    print(f"mean_exception_s_min={mean_exc_smin:.12g} mean_nonexception_s_min={mean_nonexc_smin:.12g}")


if __name__ == "__main__":
    main()
