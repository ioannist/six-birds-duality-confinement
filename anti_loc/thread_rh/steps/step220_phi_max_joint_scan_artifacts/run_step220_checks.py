#!/usr/bin/env python3
"""Validate Step 220 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step220_phi_max_joint_scan_artifacts")

REQUIRED = [
    "step220_results_summary.md",
    "step220_schema.json",
    "content_classification_step220.csv",
    "nonclaim_boundary_step220.md",
    "step220_phi_max_joint_scan.tex",
    "compute_phi_max_step220.py",
    "run_step220_checks.py",
    "phi_grid_step220.csv",
    "phi_max_refined_step220.csv",
    "robustness_step220.csv",
    "residual_tree_step220.csv",
    "route_status_step220.csv",
    "construction_tasks_step220.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step220_schema.json").read_text())
    assert schema["step"] == 220
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_phi_max_bounded_below_one"

    grid = rows("phi_grid_step220.csv")
    refined = rows("phi_max_refined_step220.csv")
    if len(grid) != 100 or len(refined) != 25:
        raise SystemExit("unexpected grid sizes")
    best = max(float(r["Phi"]) for r in refined)
    if not (0.48 < best < 0.5):
        raise SystemExit(f"unexpected refined max {best}")
    robust = rows("robustness_step220.csv")
    if len(robust) < 7:
        raise SystemExit("missing robustness rows")

    print("Step 220 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_phi_max_bounded_below_one")


if __name__ == "__main__":
    main()
