#!/usr/bin/env python3
"""Validate Step 289 artifact contract."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step289_branch_B_high_precision_artifacts")
REQUIRED = [
    "step289_results_summary.md",
    "step289_schema.json",
    "content_classification_step289.csv",
    "nonclaim_boundary_step289.md",
    "step289_branch_B_precision_wall.tex",
    "reconstruct_G_step289.py",
    "invert_G_techniques_step289.py",
    "compute_step289_output.txt",
    "run_step289_checks.py",
    "G_provenance_step289.csv",
    "condition_number_vs_dps_step289.csv",
    "inversion_techniques_step289.csv",
    "next_layer_stability_step289.csv",
    "residual_tree_step289.csv",
    "route_status_step289.csv",
    "construction_tasks_step289.csv",
]


def fail(msg: str) -> None:
    print(f"Step 289 check failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if not ART.is_dir():
        fail(f"artifact directory missing: {ART}")
    for name in REQUIRED:
        path = ART / name
        if not path.exists():
            fail(f"missing {name}")
        if path.stat().st_size == 0:
            fail(f"empty {name}")

    schema = json.loads((ART / "step289_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 289:
        fail("schema step mismatch")
    if schema.get("final_verdict") != "V_branch_B_G_inv_partial":
        fail("unexpected final verdict")
    if "Step208 G_matrix_step208.csv" not in schema.get("inherited_G_provenance", ""):
        fail("schema missing G provenance")

    cond = rows("condition_number_vs_dps_step289.csv")
    if {r["dps"] for r in cond} != {"80", "200", "500", "1000"}:
        fail("condition table missing requested dps values")
    if not all(r["status"] == "stable_from_preserved_decimal_G" for r in cond):
        fail("condition table status not stable")

    inv = rows("inversion_techniques_step289.csv")
    techniques = {r["technique"] for r in inv}
    for needed in {"direct_inverse", "lu_solve_columns", "svd_pseudoinverse", "tikhonov_lambda_1e-80", "tikhonov_lambda_1e-30", "newton_refinement", "qr_column_pivoting", "cholesky_regularized"}:
        if needed not in techniques:
            fail(f"missing technique {needed}")

    stability = rows("next_layer_stability_step289.csv")
    if not any(r["candidate"] == "CAND1" and r["decisive_against_error_bound"] == "False" for r in stability):
        fail("CAND1 dominance-by-error not recorded")
    if not any(r["candidate"] == "CAND2" and r["decisive_against_error_bound"] == "False" for r in stability):
        fail("CAND2 dominance-by-error not recorded")

    out = (ART / "compute_step289_output.txt").read_text(encoding="utf-8")
    if "final_verdict=V_branch_B_G_inv_partial" not in out:
        fail("compute output missing final verdict")

    print("Step 289 checks passed")


if __name__ == "__main__":
    main()
