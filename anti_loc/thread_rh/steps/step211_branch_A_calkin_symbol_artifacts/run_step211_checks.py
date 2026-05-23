#!/usr/bin/env python3
"""Validate Step 211 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step211_branch_A_calkin_symbol_artifacts")

REQUIRED = [
    "step211_results_summary.md",
    "step211_schema.json",
    "content_classification_step211.csv",
    "nonclaim_boundary_step211.md",
    "step211_branch_A_calkin_symbol.tex",
    "derive_calkin_symbol_step211.py",
    "run_step211_checks.py",
    "algebra_construction_step211.csv",
    "faithful_symbol_step211.csv",
    "normal_form_step211.csv",
    "lower_faithfulness_step211.csv",
    "compact_remainder_step211.csv",
    "residual_tree_step211.csv",
    "route_status_step211.csv",
    "construction_tasks_step211.csv",
    "classical_theorems_cited_step211.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step211_schema.json").read_text())
    assert schema["step"] == 211
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_branch_A_calkin_symbol_not_faithful"

    alg = rows("algebra_construction_step211.csv")
    if not any(r["object"] == "finite_P_eta" and r["status"] == "compact" for r in alg):
        raise SystemExit("finite P_eta compact audit missing")
    if not any(r["object"] == "full_P_eta" and r["status"] == "infinite_carrier_open" for r in alg):
        raise SystemExit("full P_eta open audit missing")

    g2 = rows("faithful_symbol_step211.csv")
    if not any(r["status"] == "not_constructed" for r in g2):
        raise SystemExit("G2 missing not_constructed status")

    print("Step 211 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_branch_A_calkin_symbol_not_faithful")


if __name__ == "__main__":
    main()
