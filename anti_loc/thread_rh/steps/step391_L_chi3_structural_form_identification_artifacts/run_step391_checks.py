#!/usr/bin/env python3
"""Validate Step 391 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step391_L_chi3_structural_form_identification_artifacts")
REQUIRED = [
    "structural_fits_step391.csv",
    "best_fit_analysis_step391.md",
    "step391_results_summary.md",
    "step391_schema.json",
    "nonclaim_boundary_step391.md",
    "run_step391_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step391_schema.json").read_text())
    if schema.get("step") != 391:
        raise SystemExit("wrong step")
    if schema.get("N") != 10:
        raise SystemExit("expected 10 data points")

    with (ART / "structural_fits_step391.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 5:
        raise SystemExit("expected 5 candidate rows")
    candidates = {r["candidate"] for r in rows}
    if candidates != {"C1", "C2", "C3", "C4", "C5"}:
        raise SystemExit(f"unexpected candidates: {candidates}")
    for r in rows:
        float(r["RMSE"])

    best = min(rows, key=lambda r: float(r["RMSE"]))
    if best["candidate"] != schema["best_candidate"]:
        raise SystemExit("best candidate mismatch")
    if "No RH claim" not in (ART / "nonclaim_boundary_step391.md").read_text():
        raise SystemExit("nonclaim missing")
    if "Best candidate" not in (ART / "best_fit_analysis_step391.md").read_text():
        raise SystemExit("analysis missing best candidate")

    print("step391 checks passed")


if __name__ == "__main__":
    main()
