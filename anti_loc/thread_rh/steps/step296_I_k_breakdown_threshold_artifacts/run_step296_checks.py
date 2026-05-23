#!/usr/bin/env python3
"""Validate Step 296 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step296_I_k_breakdown_threshold_artifacts")
REQUIRED = [
    "compute_I_k_analytical_step296.py",
    "compute_I_k_legacy_step296.py",
    "I_k_cross_verification_step296.csv",
    "breakdown_threshold_step296.csv",
    "corrected_L_k_step296.csv",
    "step269_smallk_consistency_step296.csv",
    "step296_results_summary.md",
    "step296_schema.json",
    "content_classification_step296.csv",
    "nonclaim_boundary_step296.md",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step296_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 296:
        raise SystemExit("schema mismatch")
    if not rows("breakdown_threshold_step296.csv")[0]["k_star"]:
        raise SystemExit("missing threshold")
    if {int(r["k"]) for r in rows("corrected_L_k_step296.csv")} != {10, 15, 20, 30, 50}:
        raise SystemExit("missing corrected k values")
    print("STEP296_CHECKS_PASS")


if __name__ == "__main__":
    main()
