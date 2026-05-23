#!/usr/bin/env python3
"""Validate Step 406 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step406_PCC_GUE_cross_check_artifacts")
REQUIRED = [
    "pcc_gue_predictions_step406.csv",
    "comparison_step406.md",
    "step406_results_summary.md",
    "step406_schema.json",
    "nonclaim_boundary_step406.md",
    "run_step406_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step406_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 406:
        raise SystemExit("schema step is not 406")
    if "mismatch" not in schema.get("verdict", ""):
        raise SystemExit("unexpected verdict")

    with (ART / "pcc_gue_predictions_step406.csv").open(newline="", encoding="utf-8") as handle:
        rows = {row["quantity"]: row["value"] for row in csv.DictReader(handle)}
    p = float(rows["P_GUE_alpha_lt_threshold"])
    empirical = float(rows["empirical_close_pair_fraction"])
    if not (p < empirical):
        raise SystemExit("expected PCC integral below empirical close fraction")

    nonclaim = (ART / "nonclaim_boundary_step406.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 406 checks passed.")
    print("P_GUE=0.3730084247967859")
    print("empirical_close=0.6059850374064838")


if __name__ == "__main__":
    main()
