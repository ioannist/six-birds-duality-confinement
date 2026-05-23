#!/usr/bin/env python3
"""Validate Step 300 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step300_h_circle_scan_artifacts")
REQUIRED = [
    "scan_h_circle_step300.py",
    "h_circle_scan_R11p34_k10_step300.csv",
    "h_max_per_radius_step300.csv",
    "h_max_at_k20_step300.csv",
    "step300_results_summary.md",
    "step300_schema.json",
    "nonclaim_boundary_step300.md",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step300_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 300:
        raise SystemExit("schema mismatch")
    if len(rows("h_circle_scan_R11p34_k10_step300.csv")) < 360:
        raise SystemExit("R=11.34 scan too sparse")
    if len(rows("h_max_per_radius_step300.csv")) < 9:
        raise SystemExit("missing radius scans")
    print("STEP300_CHECKS_PASS")


if __name__ == "__main__":
    main()
