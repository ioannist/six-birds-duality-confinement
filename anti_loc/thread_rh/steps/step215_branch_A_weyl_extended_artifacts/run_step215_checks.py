#!/usr/bin/env python3
"""Validate Step 215 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step215_branch_A_weyl_extended_artifacts")

REQUIRED = [
    "step215_results_summary.md",
    "step215_schema.json",
    "content_classification_step215.csv",
    "nonclaim_boundary_step215.md",
    "step215_branch_A_weyl_extended.tex",
    "compute_weyl_extended_step215.py",
    "run_step215_checks.py",
    "weyl_extended_step215.csv",
    "weak_null_inner_products_step215.csv",
    "lim_inf_analysis_step215.csv",
    "residual_tree_step215.csv",
    "route_status_step215.csv",
    "construction_tasks_step215.csv",
    "classical_theorems_cited_step215.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step215_schema.json").read_text())
    assert schema["step"] == 215
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_weyl_extended_obstruction_diagnostic"

    weyl = rows("weyl_extended_step215.csv")
    if len(weyl) != 20:
        raise SystemExit(f"expected 20 Weyl rows, got {len(weyl)}")
    c1 = [float(r["CAND1_C_l_u_n_norm"]) for r in weyl]
    c2 = [float(r["CAND2_C_l_u_n_norm"]) for r in weyl if r["CAND2_C_l_u_n_norm"]]
    if min(c1) <= 0.7:
        raise SystemExit("CAND1 lower-bound diagnostic unexpectedly small")
    if len(c2) != 10 or min(c2) <= 0.18:
        raise SystemExit("CAND2 comparison lower-bound diagnostic unexpectedly small")

    lim = rows("lim_inf_analysis_step215.csv")[0]
    if lim["verdict"] != "V_weyl_extended_obstruction_diagnostic":
        raise SystemExit("lim-inf verdict mismatch")
    if float(lim["max_inner_abs_tail_11_20"]) < 0.9:
        raise SystemExit("weak-null caveat unexpectedly disappeared")

    print("Step 215 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_weyl_extended_obstruction_diagnostic")


if __name__ == "__main__":
    main()
