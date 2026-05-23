#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step238_lindelof_hypothesis_pivot_artifacts")

REQUIRED = [
    "step238_results_summary.md",
    "step238_schema.json",
    "content_classification_step238.csv",
    "nonclaim_boundary_step238.md",
    "step238_lindelof_hypothesis_pivot.tex",
    "derive_lindelof_residual_step238.py",
    "run_step238_checks.py",
    "lindelof_declaration_step238.csv",
    "subconvexity_history_step238.csv",
    "density_equivalence_step238.csv",
    "classification_step238.csv",
    "residual_tree_step238.csv",
    "route_status_step238.csv",
    "construction_tasks_step238.csv",
    "classical_theorems_cited_step238.csv",
]


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ROOT / "step238_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 238
    assert schema["orientation"] == "adequacy"
    assert schema["primary_carrier"] == "Lindelof hypothesis"
    assert schema["final_verdict"] == "V_lindelof_outside_dichotomy_sub_conjecture"
    assert "13/84" in schema["best_subconvexity_bound"]["bound"]
    assert "outside scope" in schema["classification"]["under_Riemann_RH_Dichotomy"]
    assert "generalized CRCFT-TE" in schema["classification"]["under_generalized_subconjecture_Dichotomy"]

    assert len(rows("lindelof_declaration_step238.csv")) >= 5
    assert any("Bourgain" in row["source"] for row in rows("subconvexity_history_step238.csv"))
    assert any("Backlund" in row["form"] for row in rows("density_equivalence_step238.csv"))

    summary = (ROOT / "step238_results_summary.md").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step238.md").read_text(encoding="utf-8")
    for token in ["Xi_Lindelof", "Bourgain", "V_lindelof_outside_dichotomy_sub_conjecture"]:
        assert token in summary
    assert "does not claim" in nonclaim

    print("step238 checks passed: Lindelof carrier classified as outside RH Dichotomy and generalized CRCFT-TE within Lindelof family.")


if __name__ == "__main__":
    main()
