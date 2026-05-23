#!/usr/bin/env python3
"""Validate Step 299 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step299_saddle_root_enumeration_artifacts")
REQUIRED = [
    "enumerate_saddles_step299.py",
    "saddle_roots_k10_step299.csv",
    "dominant_root_ranking_step299.csv",
    "dominant_prediction_step299.csv",
    "step299_results_summary.md",
    "step299_schema.json",
    "nonclaim_boundary_step299.md",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step299_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 299:
        raise SystemExit("schema mismatch")
    if schema.get("root_count_k10", 0) < 1:
        raise SystemExit("no roots enumerated")
    if {int(r["k"]) for r in rows("dominant_prediction_step299.csv")} != {10, 20, 30, 50}:
        raise SystemExit("bad prediction k set")
    print("STEP299_CHECKS_PASS")


if __name__ == "__main__":
    main()
