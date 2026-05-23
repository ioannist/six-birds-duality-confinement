#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step240_hecke_H2_source_frame_tail_artifacts")

REQUIRED = [
    "step240_results_summary.md",
    "step240_schema.json",
    "content_classification_step240.csv",
    "nonclaim_boundary_step240.md",
    "step240_hecke_H2_source_frame_tail.tex",
    "run_step240_checks.py",
    "H2_specification_step240.csv",
    "inherited_records_step240.csv",
    "no_go_check_step240.csv",
    "literature_audit_step240.csv",
    "hecke_H2_classification_step240.csv",
    "residual_tree_step240.csv",
    "route_status_step240.csv",
    "construction_tasks_step240.csv",
    "classical_theorems_cited_step240.csv",
]


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ROOT / "step240_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 240
    assert schema["orientation"] == "adequacy"
    assert schema["target"] == "Hecke H2 source lower-frame + Plancherel tail"
    assert schema["final_verdict"] == "V_hecke_H2_blocked_external"
    assert schema["hecke_H2_verdict"] == "V_hecke_H2_blocked_external"
    assert "Lambda_n" in schema["H2_specification"]["lower_frame"]
    assert len(schema["no_go_check"]) == 3

    assert any(row["record"].startswith("step92") for row in rows("inherited_records_step240.csv"))
    assert any("incomplete character spectrum" in row["no_go"] for row in rows("no_go_check_step240.csv"))
    assert any("Iwaniec" in row["source"] for row in rows("literature_audit_step240.csv"))
    assert any(row["candidate_verdict"] == "V_hecke_H2_blocked_external" and row["applies"] == "true" for row in rows("hecke_H2_classification_step240.csv"))

    summary = (ROOT / "step240_results_summary.md").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step240.md").read_text(encoding="utf-8")
    for token in ["H2", "Plancherel", "V_hecke_H2_blocked_external"]:
        assert token in summary
    assert "does not claim" in nonclaim

    print("step240 checks passed: Hecke H2 audited and classified as blocked_external with retained no-gos.")


if __name__ == "__main__":
    main()
