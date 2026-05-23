#!/usr/bin/env python3
"""Validate Step 285 artifacts and v4 synthesis."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step285_framework_v4_final_artifacts"
V4 = ROOT / "anti_loc/findings_framework_v4_final.md"
MASTER = ROOT / "anti_loc/findings_framework.md"


REQUIRED = [
    "step285_results_summary.md",
    "step285_schema.json",
    "content_classification_step285.csv",
    "nonclaim_boundary_step285.md",
    "step285_framework_v4.tex",
    "run_step285_checks.py",
    "v4_findings_catalog_step285.csv",
    "v4_eight_of_eight_table_step285.csv",
    "v4_branch_state_step285.csv",
    "v4_corpus_integration_step285.csv",
    "residual_tree_step285.csv",
    "route_status_step285.csv",
    "construction_tasks_step285.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")
    if not V4.exists():
        raise SystemExit(f"missing v4 document: {V4}")

    schema = json.loads((ART / "step285_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 285
    assert schema["final_verdict"] == "V_framework_v4_final"
    assert schema["document_size_lines"] >= 150

    v4 = V4.read_text(encoding="utf-8")
    for needle in [
        "Framework Findings - Final v4 Consolidated Synthesis",
        "8-of-8 Cross-Track Empirical Downgrade Pattern",
        "QUE",
        "Phi_max(0.35,2.0)=0.490476620030",
        "Conrey 1989",
        "v4",
    ]:
        assert needle in v4, f"missing v4 content: {needle}"

    findings = read_csv("v4_findings_catalog_step285.csv")
    assert len(findings) == 10
    assert any(row["finding"] == "Attack Foreclosure Conjecture" and "8-of-8" in row["status"] for row in findings)

    eight = read_csv("v4_eight_of_eight_table_step285.csv")
    assert len(eight) == 8
    assert eight[-1]["step"] == "284"
    assert "falsification" in eight[-1]["downgrade_verdict"]

    branches = read_csv("v4_branch_state_step285.csv")
    assert len(branches) == 3
    assert any(row["branch"] == "Branch A" and "0.490476620030" in row["state"] for row in branches)

    master = MASTER.read_text(encoding="utf-8")
    assert "step 285 v4 final synthesis" in master
    assert "findings_framework_v4_final.md" in master

    print("Step 285 checks passed")


if __name__ == "__main__":
    main()
