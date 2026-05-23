#!/usr/bin/env python3
"""Validate Step 293 artifact contract and numerical decision."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts")

REQUIRED = [
    "step293_results_summary.md",
    "step293_schema.json",
    "content_classification_step293.csv",
    "nonclaim_boundary_step293.md",
    "step293_branch_C_L_k_at_k10.tex",
    "method_A_projected_pipeline_step293.py",
    "method_B_leibniz_corrections_step293.py",
    "method_C_step270_extension_step293.py",
    "compute_step293_output.txt",
    "method_provenance_step293.csv",
    "L_k_method_A_step293.csv",
    "L_k_method_B_step293.csv",
    "L_k_method_C_step293.csv",
    "cross_method_comparison_step293.csv",
    "L_k_over_delta_Dk_ratio_step293.csv",
    "decision_step293.csv",
    "residual_tree_step293.csv",
    "route_status_step293.csv",
    "construction_tasks_step293.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step293_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 293:
        raise SystemExit("schema step mismatch")
    if schema.get("final_verdict") != "V_branch_C_L_k_at_k10_settled_law_breaks":
        raise SystemExit("unexpected final verdict")

    comparisons = rows("cross_method_comparison_step293.csv")
    if len(comparisons) != 3:
        raise SystemExit("expected k=8,9,10 comparison rows")
    if any(row["agreement"] != "A_equals_B_equals_C" for row in comparisons):
        raise SystemExit("methods did not agree")

    ratios = {int(row["k"]): row for row in rows("L_k_over_delta_Dk_ratio_step293.csv")}
    for k in range(1, 11):
        if k not in ratios:
            raise SystemExit(f"missing ratio k={k}")
    if float(ratios[10]["L_over_delta"]) < 80:
        raise SystemExit("k=10 overshoot not captured")

    decision = rows("decision_step293.csv")[0]
    if decision["projected_law_decision"] != "breaks_for_projected_L":
        raise SystemExit("decision row mismatch")

    print("STEP293_CHECKS_PASS")


if __name__ == "__main__":
    main()
