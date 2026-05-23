#!/usr/bin/env python3
"""Validate Step 297 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step297_delta_Dk_asymptotic_artifacts")
REQUIRED = [
    "step297_delta_Dk_asymptotic.tex",
    "saddle_descent_step297.py",
    "predicted_vs_certified_step297.csv",
    "parameters_step297.csv",
    "compute_step297_output.txt",
    "step297_results_summary.md",
    "step297_schema.json",
    "content_classification_step297.csv",
    "nonclaim_boundary_step297.md",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    schema = json.loads((ART / "step297_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 297:
        raise SystemExit("schema mismatch")
    if schema["parameters"]["gamma"] != 0.0:
        raise SystemExit("expected gamma cancellation")
    pred_ks = {int(r["k"]) for r in rows("predicted_vs_certified_step297.csv") if r["model"].startswith("A")}
    if pred_ks != {5, 10, 15, 20, 30, 50}:
        raise SystemExit(f"bad fit k set {pred_ks}")
    print("STEP297_CHECKS_PASS")


if __name__ == "__main__":
    main()
