#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step244_hecke_frontier_collective_synthesis_artifacts")

REQUIRED = [
    "step244_results_summary.md",
    "step244_schema.json",
    "content_classification_step244.csv",
    "nonclaim_boundary_step244.md",
    "step244_hecke_frontier_collective.tex",
    "run_step244_checks.py",
    "gate_summary_step244.csv",
    "external_requirements_step244.csv",
    "framework_implications_step244.csv",
    "residual_tree_step244.csv",
    "route_status_step244.csv",
    "construction_tasks_step244.csv",
]


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ROOT / "step244_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 244
    assert schema["orientation"] == "synthesis-case-3"
    assert schema["target"] == "Hecke H1-H5 collective frontier blockage"
    assert schema["final_verdict"] == "V_hecke_frontier_collectively_blocked"
    assert len(schema["gate_summary_table"]) == 6

    gate_rows = rows("gate_summary_step244.csv")
    assert len(gate_rows) == 6
    assert {row["gate"] for row in gate_rows} == {"H1", "H2", "H3", "H4", "H5", "H6"}
    assert all("blocked external" in row["verdict"] or "V-NC" in row["verdict"] for row in gate_rows)

    req_rows = rows("external_requirements_step244.csv")
    assert len(req_rows) == 6
    assert any(row["gate"] == "H4" and "kappa_chi" in row["precisely_typed_requirement"] for row in req_rows)

    summary = (ROOT / "step244_results_summary.md").read_text(encoding="utf-8")
    nonclaim = (ROOT / "nonclaim_boundary_step244.md").read_text(encoding="utf-8")
    for token in ["Hecke Frontier Collective Blockage", "V_hecke_frontier_collectively_blocked", "H6"]:
        assert token in summary
    assert "does not claim" in nonclaim

    print("step244 checks passed: Hecke H1-H5 collective blockage synthesized with H6 BF retained.")


if __name__ == "__main__":
    main()
