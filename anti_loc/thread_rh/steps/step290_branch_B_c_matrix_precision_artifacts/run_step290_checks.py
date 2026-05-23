#!/usr/bin/env python3
"""Validate Step 290 artifact contract."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step290_branch_B_c_matrix_precision_artifacts")
REQUIRED = [
    "step290_results_summary.md",
    "step290_schema.json",
    "content_classification_step290.csv",
    "nonclaim_boundary_step290.md",
    "step290_branch_B_c_matrix.tex",
    "reconstruct_c_matrix_step290.py",
    "refine_c_matrix_grid_step290.py",
    "analytical_c_matrix_step290.py",
    "compute_step290_output.txt",
    "run_step290_checks.py",
    "c_matrix_provenance_step290.csv",
    "c_matrix_entries_inherited_step290.csv",
    "c_matrix_entries_refined_step290.csv",
    "c_matrix_entries_analytical_step290.csv",
    "uncertainty_reduction_step290.csv",
    "CAND1_CAND2_step290.csv",
    "residual_tree_step290.csv",
    "route_status_step290.csv",
    "construction_tasks_step290.csv",
]


def fail(msg: str) -> None:
    print(f"Step 290 check failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if not ART.is_dir():
        fail(f"missing artifact directory: {ART}")
    for name in REQUIRED:
        path = ART / name
        if not path.exists():
            fail(f"missing {name}")
        if path.stat().st_size == 0:
            fail(f"empty {name}")

    schema = json.loads((ART / "step290_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 290:
        fail("schema step mismatch")
    if schema.get("final_verdict") != "V_branch_B_c_matrix_refined_disagrees_hard_block":
        fail("unexpected final verdict")
    if schema.get("avenue_A_grid_refinement", {}).get("grid_nodes") != 2000:
        fail("avenue A grid was not 2000 nodes")
    if schema.get("avenue_A_grid_refinement", {}).get("ten_order_target_met") is not False:
        fail("schema should record 10-order target not met")

    refined = rows("c_matrix_entries_refined_step290.csv")
    if len(refined) != 18:
        fail(f"expected 18 refined c entries, found {len(refined)}")
    if not all(r["grid_nodes"] == "2000" for r in refined):
        fail("not all refined entries are from 2000-node grid")

    analytical = rows("c_matrix_entries_analytical_step290.csv")
    if not any(r["quad_dps"] == "200" and "completed" in r["burnol_kernel_probe_status"] for r in analytical):
        fail("analytical dps=200 probe not recorded")
    if not all(r["status"].startswith("blocked_no_closed_projected") for r in analytical):
        fail("analytical full c-entry block not recorded")

    cand = {r["candidate"]: r for r in rows("CAND1_CAND2_step290.csv")}
    if set(cand) != {"CAND1", "CAND2"}:
        fail("CAND comparison missing candidates")
    if cand["CAND1"]["decisive_against_proxy_error"] != "False":
        fail("CAND1 proxy decisiveness should be false")
    if cand["CAND2"]["decisive_against_proxy_error"] != "True":
        fail("CAND2 proxy decisiveness should be true")

    output = (ART / "compute_step290_output.txt").read_text(encoding="utf-8")
    for needle in ["grid_nodes=2000", "mpmath_quad_probe_completed", "full_c_matrix_status=blocked"]:
        if needle not in output:
            fail(f"compute output missing {needle!r}")

    print("Step 290 checks passed")


if __name__ == "__main__":
    main()
