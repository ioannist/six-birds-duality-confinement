#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step243_hecke_H5_explicit_formula_records_artifacts")

REQUIRED = [
    "step243_results_summary.md",
    "step243_schema.json",
    "content_classification_step243.csv",
    "nonclaim_boundary_step243.md",
    "step243_hecke_H5_explicit_formula_records.tex",
    "run_step243_checks.py",
    "H5_specification_step243.csv",
    "inherited_records_step243.csv",
    "no_go_check_step243.csv",
    "literature_audit_step243.csv",
    "hecke_H5_classification_step243.csv",
    "residual_tree_step243.csv",
    "route_status_step243.csv",
    "construction_tasks_step243.csv",
    "classical_theorems_cited_step243.csv",
]


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ROOT / "step243_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 243
    assert schema["orientation"] == "adequacy"
    assert schema["target"] == "Hecke H5 auxiliary explicit-formula records"
    assert schema["final_verdict"] == "V_hecke_H5_blocked_external"
    assert schema["hecke_H5_verdict"] == "V_hecke_H5_blocked_external"
    assert "conductor" in schema["H5_specification"]["required_fields"]
    assert "root number" in schema["H5_specification"]["required_fields"]

    assert any(row["record"].startswith("step92") for row in rows("inherited_records_step243.csv"))
    assert any("auxiliary-GRH" in row["no_go"] for row in rows("no_go_check_step243.csv"))
    assert any("Tate" in row["source"] for row in rows("literature_audit_step243.csv"))
    assert any("Hecke" in row["source"] or "Hecke" in row["audited_content"] for row in rows("literature_audit_step243.csv"))
    assert any(row["candidate_verdict"] == "V_hecke_H5_blocked_external" and row["applies"] == "true" for row in rows("hecke_H5_classification_step243.csv"))

    summary = (ROOT / "step243_results_summary.md").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step243.md").read_text(encoding="utf-8")
    for token in ["H5", "explicit-formula", "V_hecke_H5_blocked_external"]:
        assert token in summary
    assert "does not claim" in nonclaim

    print("step243 checks passed: Hecke H5 audited and classified as blocked_external explicit-formula records.")


if __name__ == "__main__":
    main()
