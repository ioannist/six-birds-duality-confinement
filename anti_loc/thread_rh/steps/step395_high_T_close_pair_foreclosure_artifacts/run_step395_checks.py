#!/usr/bin/env python3
"""Validate Step 395 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step395_high_T_close_pair_foreclosure_artifacts")
REQUIRED = [
    "close_pair_list_step395.csv",
    "non_close_pair_baseline_step395.csv",
    "correlation_step395.md",
    "step395_results_summary.md",
    "step395_schema.json",
    "nonclaim_boundary_step395.md",
    "run_step395_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step395_schema.json").read_text())
    if schema.get("step") != 395:
        raise SystemExit("wrong step")
    if schema.get("dps", 0) < 80:
        raise SystemExit("dps below requirement")

    cp = rows("close_pair_list_step395.csv")
    base = rows("non_close_pair_baseline_step395.csv")
    if len(cp) != schema["close_pair_count"]:
        raise SystemExit("close-pair row count mismatch")
    if len(base) != schema["non_close_baseline_count"]:
        raise SystemExit("baseline row count mismatch")
    cp_fail = sum(1 for r in cp if r["pass_foreclosure"] == "FAIL")
    base_fail = sum(1 for r in base if r["pass_foreclosure"] == "FAIL")
    if cp_fail != schema["close_pair_fail_count"]:
        raise SystemExit("close-pair failure count mismatch")
    if base_fail != schema["non_close_fail_count"]:
        raise SystemExit("baseline failure count mismatch")
    for r in (cp[:5] + base[:5]):
        float(r["abs_delta_Dk"])
        float(r["s_min"])
    if "Pearson" not in (ART / "correlation_step395.md").read_text():
        raise SystemExit("correlation summary missing")
    if "No RH claim" not in (ART / "nonclaim_boundary_step395.md").read_text():
        raise SystemExit("nonclaim missing")

    print("step395 checks passed")


if __name__ == "__main__":
    main()
