#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step242_hecke_H4_per_character_diagnostics_artifacts")

REQUIRED = [
    "step242_results_summary.md",
    "step242_schema.json",
    "content_classification_step242.csv",
    "nonclaim_boundary_step242.md",
    "step242_hecke_H4_per_character_diagnostics.tex",
    "run_step242_checks.py",
    "H4_specification_step242.csv",
    "inherited_records_step242.csv",
    "no_go_check_step242.csv",
    "literature_audit_step242.csv",
    "hecke_H4_classification_step242.csv",
    "residual_tree_step242.csv",
    "route_status_step242.csv",
    "construction_tasks_step242.csv",
    "classical_theorems_cited_step242.csv",
]


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ROOT / "step242_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 242
    assert schema["orientation"] == "adequacy"
    assert schema["target"] == "Hecke H4 per-character finite-carrier diagnostics"
    assert schema["final_verdict"] == "V_hecke_H4_blocked_external"
    assert schema["hecke_H4_verdict"] == "V_hecke_H4_blocked_external"
    assert "kappa_chi" in schema["H4_specification"]["matrix_entry"]

    inherited = rows("inherited_records_step242.csv")
    assert any(row["record"] == "step201" for row in inherited)
    assert any("Burnol" in row["quoted_or_summarized_content"] for row in inherited)
    assert any("auxiliary-GRH" in row["no_go"] for row in rows("no_go_check_step242.csv"))
    assert any("Conrey" in row["source"] for row in rows("literature_audit_step242.csv"))
    assert any(row["candidate_verdict"] == "V_hecke_H4_blocked_external" and row["applies"] == "true" for row in rows("hecke_H4_classification_step242.csv"))

    summary = (ROOT / "step242_results_summary.md").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step242.md").read_text(encoding="utf-8")
    for token in ["H4", "kappa", "V_hecke_H4_blocked_external"]:
        assert token in summary
    assert "does not claim" in nonclaim

    print("step242 checks passed: Hecke H4 audited and classified as blocked_external diagnostic-only.")


if __name__ == "__main__":
    main()
