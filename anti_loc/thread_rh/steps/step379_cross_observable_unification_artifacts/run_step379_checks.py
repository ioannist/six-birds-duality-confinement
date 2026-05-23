#!/usr/bin/env python3
"""Validate Step 379 cross-observable unification artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step379_cross_observable_unification_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP379_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "exceptional_gamma_residuals_step379.csv",
        "baseline_residuals_step379.csv",
        "two_sample_test_step379.md",
        "step379_results_summary.md",
        "step379_schema.json",
        "nonclaim_boundary_step379.md",
        "run_step379_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    exc = rows("exceptional_gamma_residuals_step379.csv")
    base = rows("baseline_residuals_step379.csv")
    require(len(exc) == 7, f"expected 7 exception rows, got {len(exc)}")
    require(len(base) == 15, f"expected 15 baseline rows, got {len(base)}")
    require([r["j"] for r in exc] == ["34", "41", "64", "71", "79", "80", "92"], "unexpected exception list")

    mean_exc = sum(float(r["abs_R"]) for r in exc) / len(exc)
    mean_base = sum(float(r["abs_R"]) for r in base) / len(base)
    ratio = mean_exc / mean_base
    require(ratio > 2.0, f"expected >2x effect, got ratio={ratio}")

    schema = json.loads((BASE / "step379_schema.json").read_text())
    require(schema["dps"] >= 80, "dps below hard constraint")
    require(schema["verdict"] == "unification_confirmed_exceptional_residuals_large", "schema verdict mismatch")
    require(abs(schema["ratio_exceptional_to_baseline"] - ratio) < 1e-9, "schema ratio mismatch")

    summary = (BASE / "step379_results_summary.md").read_text()
    require("Step 292 raw delta proxy" in summary, "summary missing evaluator disclosure")
    require("Welch" in (BASE / "two_sample_test_step379.md").read_text(), "two-sample test missing Welch statistic")

    boundary = (BASE / "nonclaim_boundary_step379.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("raw delta proxy" in boundary, "missing proxy caveat")

    print("STEP379_CHECK_PASS")
    print(f"exception_rows={len(exc)} baseline_rows={len(base)}")
    print(f"mean_abs_R_exceptional={mean_exc:.12g}")
    print(f"mean_abs_R_baseline={mean_base:.12g}")
    print(f"ratio={ratio:.12g}")


if __name__ == "__main__":
    main()
