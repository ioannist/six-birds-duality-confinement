#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step241_hecke_H3_calkin_bridge_artifacts")

REQUIRED = [
    "step241_results_summary.md",
    "step241_schema.json",
    "content_classification_step241.csv",
    "nonclaim_boundary_step241.md",
    "step241_hecke_H3_calkin_bridge.tex",
    "run_step241_checks.py",
    "H3_specification_step241.csv",
    "inherited_records_step241.csv",
    "no_go_check_step241.csv",
    "literature_audit_step241.csv",
    "hecke_H3_classification_step241.csv",
    "residual_tree_step241.csv",
    "route_status_step241.csv",
    "construction_tasks_step241.csv",
    "classical_theorems_cited_step241.csv",
]


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ROOT / "step241_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 241
    assert schema["orientation"] == "adequacy"
    assert schema["target"] == "Hecke H3 Calkin bridge"
    assert schema["final_verdict"] == "V_hecke_H3_blocked_external"
    assert schema["hecke_H3_verdict"] == "V_hecke_H3_blocked_external"
    assert "A_eta,Hecke" in schema["H3_specification"]["hecke_calkin_algebra"]

    inherited = rows("inherited_records_step241.csv")
    assert any(row["record"] == "step211" for row in inherited)
    assert any("H6" in row["quoted_or_summarized_content"] for row in inherited)
    assert any("Bost-Connes" in row["source"] for row in rows("literature_audit_step241.csv"))
    assert any(row["candidate_verdict"] == "V_hecke_H3_blocked_external" and row["applies"] == "true" for row in rows("hecke_H3_classification_step241.csv"))

    summary = (ROOT / "step241_results_summary.md").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step241.md").read_text(encoding="utf-8")
    for token in ["H3", "Calkin", "V_hecke_H3_blocked_external"]:
        assert token in summary
    assert "does not claim" in nonclaim

    print("step241 checks passed: Hecke H3 audited and classified as blocked_external with retained no-gos.")


if __name__ == "__main__":
    main()
