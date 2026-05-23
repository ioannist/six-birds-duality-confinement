#!/usr/bin/env python3
"""Validate Step 396 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step396_failure_predictor_identification_artifacts")
REQUIRED = [
    "extended_features_step396.csv",
    "correlations_step396.csv",
    "logistic_or_linear_fit_step396.md",
    "step396_results_summary.md",
    "step396_schema.json",
    "nonclaim_boundary_step396.md",
    "run_step396_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step396_schema.json").read_text())
    if schema.get("step") != 396:
        raise SystemExit("wrong step")
    if schema.get("dps", 0) < 50:
        raise SystemExit("dps below requirement")

    feat = rows("extended_features_step396.csv")
    corr = rows("correlations_step396.csv")
    if len(feat) != schema["rows"]:
        raise SystemExit("feature row count mismatch")
    if len(corr) < 5:
        raise SystemExit("too few correlation rows")
    if sum(int(r["fail"]) for r in feat) != schema["fail_count"]:
        raise SystemExit("fail count mismatch")
    for r in feat[:5]:
        float(r["abs_zeta_prime"])
        float(r["Re_zeta_double_prime"])
        float(r["relative_compression"])
    for r in corr:
        float(r["pearson_vs_fail"])
        float(r["abs_pearson_vs_fail"])
    if "No RH claim" not in (ART / "nonclaim_boundary_step396.md").read_text():
        raise SystemExit("nonclaim missing")
    if "Balanced accuracy" not in (ART / "logistic_or_linear_fit_step396.md").read_text():
        raise SystemExit("fit summary missing")

    print("step396 checks passed")


if __name__ == "__main__":
    main()
