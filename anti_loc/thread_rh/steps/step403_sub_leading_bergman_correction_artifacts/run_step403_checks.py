#!/usr/bin/env python3
"""Validate Step 403 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step403_sub_leading_bergman_correction_artifacts")
REQUIRED = [
    "bergman_exact_per_p_step403.csv",
    "phi_max_predictions_step403.csv",
    "step403_results_summary.md",
    "step403_schema.json",
    "nonclaim_boundary_step403.md",
    "run_step403_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step403_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 403:
        raise SystemExit("schema step is not 403")
    if schema.get("literal_formula_status") != "divergent":
        raise SystemExit("expected divergent literal formula status")
    if float(schema["term_ratio_limit_numeric"]) <= 1:
        raise SystemExit("term ratio should exceed 1")

    rows = read_csv("bergman_exact_per_p_step403.csv")
    if {int(r["p"]) for r in rows} != {3, 7, 12}:
        raise SystemExit("missing p rows")
    if not all(r["status"] == "diverges_under_literal_inherited_formula" for r in rows):
        raise SystemExit("expected divergence status for all p rows")

    preds = read_csv("phi_max_predictions_step403.csv")
    if not all(r["match_status"] == "no_finite_prediction" for r in preds):
        raise SystemExit("expected no finite predictions")

    nonclaim = (ART / "nonclaim_boundary_step403.md").read_text(encoding="utf-8")
    if "No RH claim" not in nonclaim:
        raise SystemExit("missing no-RH boundary")

    print("Step 403 checks passed.")
    print("verdict=no finite sub-leading correction under literal inherited formula")


if __name__ == "__main__":
    main()
