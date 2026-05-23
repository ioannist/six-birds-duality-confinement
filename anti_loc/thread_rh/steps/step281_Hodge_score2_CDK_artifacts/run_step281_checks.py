#!/usr/bin/env python3
"""Validate Step 281 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step281_Hodge_score2_CDK_artifacts")
FINDINGS = Path("/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md")


REQUIRED = [
    "step281_results_summary.md",
    "step281_schema.json",
    "content_classification_step281.csv",
    "nonclaim_boundary_step281.md",
    "step281_Hodge_score2_CDK.tex",
    "CDK_paper_extract_step281.md",
    "derive_Hodge_bridge_step281.py",
    "run_step281_checks.py",
    "CDK_verbatim_step281.csv",
    "locus_vs_class_distinction_step281.csv",
    "cascade_need_vs_supplied_step281.csv",
    "five_of_five_pattern_step281.csv",
    "residual_tree_step281.csv",
    "route_status_step281.csv",
    "construction_tasks_step281.csv",
    "classical_theorems_cited_step281.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step281_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 281
    assert schema["orientation"] == "cross_track_score2_audit"
    assert schema["final_verdict"] == "V_CDK_Hodge_bridge_blocked"

    verbatim = "\n".join(row["verbatim"] for row in read_csv("CDK_verbatim_step281.csv"))
    for needle in ["S(K) is an algebraic variety", "germ", "algebraic subvariety"]:
        assert needle in verbatim, f"missing CDK theorem token: {needle}"

    distinction = read_csv("locus_vs_class_distinction_step281.csv")
    assert any(row["assessment"] == "different typed object" for row in distinction)
    assert any("does not promote" in row["assessment"] for row in distinction)

    comparison = read_csv("cascade_need_vs_supplied_step281.csv")
    assert any(row["status"] == "not_derivable" for row in comparison)
    assert any("cycle-class" in row["cascade_need"] for row in comparison)

    pattern = read_csv("five_of_five_pattern_step281.csv")
    assert len(pattern) == 5
    assert all(row["audited_score"] == "1" for row in pattern)
    assert pattern[-1]["candidate"] == "CDK Hodge-locus bridge"

    findings = FINDINGS.read_text(encoding="utf-8")
    assert "steps 267-281" in findings
    assert "CDK Hodge-locus bridge" in findings
    assert "5-of-5" in findings

    print("Step 281 checks passed")


if __name__ == "__main__":
    main()
