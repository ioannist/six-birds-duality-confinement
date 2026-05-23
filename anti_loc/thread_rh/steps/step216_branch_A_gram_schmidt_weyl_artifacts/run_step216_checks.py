#!/usr/bin/env python3
"""Validate Step 216 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step216_branch_A_gram_schmidt_weyl_artifacts")

REQUIRED = [
    "step216_results_summary.md",
    "step216_schema.json",
    "content_classification_step216.csv",
    "nonclaim_boundary_step216.md",
    "step216_branch_A_gram_schmidt_weyl.tex",
    "compute_gram_schmidt_step216.py",
    "run_step216_checks.py",
    "gram_schmidt_step216.csv",
    "effective_dimension_step216.csv",
    "robustness_step216.csv",
    "residual_tree_step216.csv",
    "route_status_step216.csv",
    "construction_tasks_step216.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step216_schema.json").read_text())
    assert schema["step"] == 216
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_weyl_gram_schmidt_inconclusive"

    gs = rows("gram_schmidt_step216.csv")
    c1 = [r for r in gs if r["model"] == "CAND1"]
    c2 = [r for r in gs if r["model"] == "CAND2"]
    if len(c1) != 20 or len(c2) != 10:
        raise SystemExit("unexpected Gram-Schmidt row counts")
    if float(c1[1]["C_l_v_n_norm"]) >= 1.4:
        raise SystemExit("CAND1 second orthogonal direction unexpectedly retained Step214 scale")
    if min(float(r["C_l_v_n_norm"]) for r in c2) <= 0.2:
        raise SystemExit("CAND2 comparison lower bound unexpectedly small")

    eff = {r["model"]: r for r in rows("effective_dimension_step216.csv")}
    if eff["CAND1"]["effective_dim_rel_gt_1e-2"] != "3":
        raise SystemExit("CAND1 effective dimension mismatch")
    if eff["CAND2"]["effective_dim_rel_gt_1e-2"] != "10":
        raise SystemExit("CAND2 effective dimension mismatch")

    print("Step 216 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_weyl_gram_schmidt_inconclusive")


if __name__ == "__main__":
    main()
