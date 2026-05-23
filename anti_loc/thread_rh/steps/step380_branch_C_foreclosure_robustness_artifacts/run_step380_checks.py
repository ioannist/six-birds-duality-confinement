#!/usr/bin/env python3
"""Validate Step 380 foreclosure robustness artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step380_branch_C_foreclosure_robustness_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP380_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "exceptional_L_k_values_step380.csv",
        "foreclosure_check_step380.csv",
        "baseline_comparison_step380.md",
        "step380_results_summary.md",
        "step380_schema.json",
        "nonclaim_boundary_step380.md",
        "run_step380_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    exceptional = rows("exceptional_L_k_values_step380.csv")
    checks = rows("foreclosure_check_step380.csv")
    baseline = rows("baseline_L_k_values_step380.csv")
    require(len(exceptional) == 35, f"expected 35 exceptional cells, got {len(exceptional)}")
    require(len(checks) == 35, f"expected 35 check cells, got {len(checks)}")
    require(len(baseline) == 25, f"expected 25 baseline cells, got {len(baseline)}")
    require(all(r["pass_bound"] == "PASS" for r in checks), "found foreclosure failure")
    require(all(r["borderline_10_percent"] == "False" for r in checks), "found borderline cell")

    min_exception = min(float(r["abs_value"]) for r in exceptional)
    min_baseline = min(float(r["abs_value"]) for r in baseline)
    require(min_exception >= 0.034, "min exceptional below threshold")
    require(min_baseline >= 0.034, "min baseline below threshold")

    schema = json.loads((BASE / "step380_schema.json").read_text())
    require(schema["dps"] >= 80, "dps below hard constraint")
    require(schema["pass_count"] == 35 and schema["failure_count"] == 0, "schema pass/fail mismatch")
    require(schema["verdict"] == "robust_raw_proxy_foreclosure_all_35_pass", "schema verdict mismatch")

    boundary = (BASE / "nonclaim_boundary_step380.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("raw delta proxy" in boundary, "missing raw proxy caveat")

    print("STEP380_CHECK_PASS")
    print(f"exceptional_cells={len(exceptional)} pass=35 fail=0 borderline=0")
    print(f"min_exception={min_exception:.12g}")
    print(f"min_baseline={min_baseline:.12g}")


if __name__ == "__main__":
    main()
