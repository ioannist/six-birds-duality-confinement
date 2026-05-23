#!/usr/bin/env python3
"""Validate Step 295 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step295_I_k_saddle_asymptotic_artifacts")

REQUIRED = [
    "step295_I_k_asymptotic.tex",
    "I_k_integrand_step295.md",
    "saddle_z_star_I_k_step295.py",
    "I_k_predicted_vs_certified_step295.csv",
    "compute_step295_output.txt",
    "step295_results_summary.md",
    "step295_schema.json",
    "content_classification_step295.csv",
    "nonclaim_boundary_step295.md",
]


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step295_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 295:
        raise SystemExit("schema step mismatch")
    rows = list(csv.DictReader((ART / "I_k_predicted_vs_certified_step295.csv").open(newline="", encoding="utf-8")))
    if {int(r["k"]) for r in rows} != {10, 20, 30, 50}:
        raise SystemExit("missing comparison k values")
    if schema["predicted"]["b"] != 0.0 or schema["predicted"]["c"] != -1.0:
        raise SystemExit("endpoint exponents missing")
    print("STEP295_CHECKS_PASS")


if __name__ == "__main__":
    main()
