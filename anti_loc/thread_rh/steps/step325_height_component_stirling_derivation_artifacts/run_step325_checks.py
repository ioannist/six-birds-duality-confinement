#!/usr/bin/env python3
"""Validate Step 325 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step325_height_component_stirling_derivation_artifacts")
REQUIRED = [
    "stirling_derivation_step325.tex",
    "predicted_A_per_zero_step325.csv",
    "comparison_step325.csv",
    "step325_results_summary.md",
    "step325_schema.json",
    "nonclaim_boundary_step325.md",
    "run_step325_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    pred = rows("predicted_A_per_zero_step325.csv")
    if len(pred) != 15:
        raise SystemExit(f"expected 15 predicted rows, found {len(pred)}")
    comp = rows("comparison_step325.csv")
    if not any(r["quantity"] == "A_gamma_klogk_from_fixed_order_stirling" for r in comp):
        raise SystemExit("missing A_gamma comparison row")
    schema = json.loads((ART / "step325_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 325:
        raise SystemExit("schema step incorrect")
    if "RH" not in (ART / "nonclaim_boundary_step325.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing RH")
    print("STEP325_CHECKS_PASS")


if __name__ == "__main__":
    main()
