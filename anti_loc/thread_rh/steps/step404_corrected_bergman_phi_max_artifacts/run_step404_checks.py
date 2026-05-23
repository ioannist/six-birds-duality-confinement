#!/usr/bin/env python3
"""Validate Step 404 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step404_corrected_bergman_phi_max_artifacts")
REQUIRED = [
    "corrected_bergman_eq37_step404.csv",
    "phi_max_normalization_step404.md",
    "step404_results_summary.md",
    "step404_schema.json",
    "nonclaim_boundary_step404.md",
    "run_step404_checks.py",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step404_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 404:
        raise SystemExit("schema step is not 404")
    if "no_match" not in schema.get("verdict", ""):
        raise SystemExit("unexpected verdict")

    with (ART / "corrected_bergman_eq37_step404.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 12:
        raise SystemExit(f"expected 12 cells, got {len(rows)}")
    if not all(row["status"].startswith("finite") for row in rows):
        raise SystemExit("expected finite statuses")
    if not any(row["T"] == "10" and row["p"] == "12" for row in rows):
        raise SystemExit("missing T=10 p=12 row")

    nonclaim = (ART / "nonclaim_boundary_step404.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 404 checks passed.")
    print("verdict=corrected diagonal Bergman no match")


if __name__ == "__main__":
    main()
