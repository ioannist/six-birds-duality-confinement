#!/usr/bin/env python3
"""Validate Step 214 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step214_branch_A_weyl_sequence_artifacts")

REQUIRED = [
    "step214_results_summary.md",
    "step214_schema.json",
    "content_classification_step214.csv",
    "nonclaim_boundary_step214.md",
    "step214_branch_A_weyl_sequence.tex",
    "compute_weyl_norms_step214.py",
    "run_step214_checks.py",
    "weyl_sequence_step214.csv",
    "lim_inf_analysis_step214.csv",
    "robustness_step214.csv",
    "residual_tree_step214.csv",
    "route_status_step214.csv",
    "construction_tasks_step214.csv",
    "classical_theorems_cited_step214.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step214_schema.json").read_text())
    assert schema["step"] == 214
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_branch_A_weyl_essential_obstruction"

    weyl = rows("weyl_sequence_step214.csv")
    if len(weyl) != 10:
        raise SystemExit(f"expected 10 Weyl rows, got {len(weyl)}")
    vals = [float(r["C_l_u_n_norm"]) for r in weyl]
    if min(vals) <= 0.7:
        raise SystemExit("Weyl lower-bound diagnostic unexpectedly small")

    lim = rows("lim_inf_analysis_step214.csv")[0]
    if lim["verdict"] != "V_branch_A_weyl_essential_obstruction":
        raise SystemExit("lim-inf verdict mismatch")

    print("Step 214 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_branch_A_weyl_essential_obstruction")


if __name__ == "__main__":
    main()
