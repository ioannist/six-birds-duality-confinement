#!/usr/bin/env python3
"""Validate Step 393 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step393_precision_diagnostic_artifacts")
REQUIRED = [
    "high_precision_j470_step393.csv",
    "neighbor_zeros_step393.csv",
    "step393_results_summary.md",
    "step393_schema.json",
    "nonclaim_boundary_step393.md",
    "run_step393_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step393_schema.json").read_text())
    if schema.get("step") != 393:
        raise SystemExit("wrong step")
    if schema.get("dps") != 200:
        raise SystemExit("dps must be 200")
    if not schema.get("failure_preserved"):
        raise SystemExit("schema should preserve failure")

    hp = rows("high_precision_j470_step393.csv")
    nb = rows("neighbor_zeros_step393.csv")
    if len(hp) != 7:
        raise SystemExit("expected k=2..8 sweep")
    if len(nb) != 5:
        raise SystemExit("expected five neighbor rows")
    for r in hp + nb:
        float(r["abs_delta_Dk_dps200"])
        if r["pass_foreclosure"] not in {"PASS", "FAIL"}:
            raise SystemExit("bad pass status")
    k5 = [r for r in hp if r["k"] == "5"][0]
    if k5["pass_foreclosure"] != "FAIL":
        raise SystemExit("k=5 should fail")
    if "No RH claim" not in (ART / "nonclaim_boundary_step393.md").read_text():
        raise SystemExit("nonclaim missing")

    print("step393 checks passed")


if __name__ == "__main__":
    main()
