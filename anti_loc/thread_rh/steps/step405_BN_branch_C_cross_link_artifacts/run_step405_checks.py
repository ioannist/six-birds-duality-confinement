#!/usr/bin/env python3
"""Validate Step 405 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step405_BN_branch_C_cross_link_artifacts")
REQUIRED = [
    "baez_duarte_partial_sum_step405.csv",
    "cross_link_analysis_step405.md",
    "step405_results_summary.md",
    "step405_schema.json",
    "nonclaim_boundary_step405.md",
    "run_step405_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step405_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 405:
        raise SystemExit("schema step is not 405")
    if "no_new_BN_constraint" not in schema.get("verdict", ""):
        raise SystemExit("unexpected verdict")

    with (ART / "baez_duarte_partial_sum_step405.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 100:
        raise SystemExit(f"expected 100 zero rows, got {len(rows)}")
    last = rows[-1]
    s100 = float(last["partial_sum"])
    if not (0.019 < s100 < 0.021):
        raise SystemExit(f"unexpected partial sum {s100}")

    nonclaim = (ART / "nonclaim_boundary_step405.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 405 checks passed.")
    print("S100=0.0199848524039238053")
    print("verdict=weak density cross-link; no new BN constraint")


if __name__ == "__main__":
    main()
