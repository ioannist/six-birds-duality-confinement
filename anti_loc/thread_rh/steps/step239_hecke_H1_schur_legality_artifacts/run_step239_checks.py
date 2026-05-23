#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step239_hecke_H1_schur_legality_artifacts")

REQUIRED = [
    "step239_results_summary.md",
    "step239_schema.json",
    "content_classification_step239.csv",
    "nonclaim_boundary_step239.md",
    "step239_hecke_H1_schur_legality.tex",
    "derive_hecke_H1_step239.py",
    "run_step239_checks.py",
    "H1_specification_step239.csv",
    "inherited_records_step239.csv",
    "no_go_check_step239.csv",
    "literature_audit_step239.csv",
    "hecke_H1_classification_step239.csv",
    "residual_tree_step239.csv",
    "route_status_step239.csv",
    "construction_tasks_step239.csv",
    "classical_theorems_cited_step239.csv",
]


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ROOT / "step239_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 239
    assert schema["orientation"] == "adequacy"
    assert schema["target"] == "Hecke H1 direct-integral Schur legality"
    assert schema["final_verdict"] == "V_hecke_H1_blocked_external"
    assert schema["hecke_H1_verdict"] == "V_hecke_H1_blocked_external"
    assert "Moore-Penrose" in " ".join(schema["H1_specification"]["legality_requirements"])
    assert len(schema["no_go_check"]) == 3

    assert any(row["record"] == "step167" for row in rows("inherited_records_step239.csv"))
    assert any("auxiliary-GRH" in row["no_go"] for row in rows("no_go_check_step239.csv"))
    assert any("Tate" in row["source"] for row in rows("literature_audit_step239.csv"))
    assert any(row["candidate_verdict"] == "V_hecke_H1_blocked_external" and row["applies"] == "true" for row in rows("hecke_H1_classification_step239.csv"))

    summary = (ROOT / "step239_results_summary.md").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step239.md").read_text(encoding="utf-8")
    for token in ["H1", "V_hecke_H1_blocked_external", "direct-integral"]:
        assert token in summary
    assert "does not claim" in nonclaim

    print("step239 checks passed: Hecke H1 audited and classified as blocked_external with retained no-gos.")


if __name__ == "__main__":
    main()
