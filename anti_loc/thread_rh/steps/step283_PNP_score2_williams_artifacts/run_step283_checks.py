#!/usr/bin/env python3
"""Validate Step 283 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step283_PNP_score2_williams_artifacts")
FINDINGS = Path("/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md")


REQUIRED = [
    "step283_results_summary.md",
    "step283_schema.json",
    "content_classification_step283.csv",
    "nonclaim_boundary_step283.md",
    "step283_PNP_score2_williams.tex",
    "williams_paper_extract_step283.md",
    "derive_PNP_bridge_step283.py",
    "run_step283_checks.py",
    "williams_verbatim_step283.csv",
    "scale_gap_step283.csv",
    "cascade_need_vs_supplied_step283.csv",
    "seven_of_seven_pattern_step283.csv",
    "residual_tree_step283.csv",
    "route_status_step283.csv",
    "construction_tasks_step283.csv",
    "classical_theorems_cited_step283.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step283_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 283
    assert schema["orientation"] == "cross_track_score2_audit"
    assert schema["final_verdict"] == "V_williams_ACC_PNP_bridge_blocked"

    verbatim = "\n".join(row["verbatim"] for row in read_csv("williams_verbatim_step283.csv"))
    for needle in ["NEXP", "ACC", "NTIME[2^n]", "P != NP"]:
        assert needle in verbatim, f"missing Williams token: {needle}"

    scale_gap = read_csv("scale_gap_step283.csv")
    assert any(row["assessment"] == "too_high_in_time_hierarchy" for row in scale_gap)
    assert any(row["assessment"] == "too_restricted_model" for row in scale_gap)
    assert any(row["assessment"] == "missing_scale_bridge" for row in scale_gap)

    comparison = read_csv("cascade_need_vs_supplied_step283.csv")
    assert any(row["status"] == "not_derivable" for row in comparison)
    assert any("P != NP" in row["cascade_need"] for row in comparison)

    pattern = read_csv("seven_of_seven_pattern_step283.csv")
    assert len(pattern) == 7
    assert all(row["audited_score"] == "1" for row in pattern)
    assert pattern[-1]["candidate"] == "Williams ACC lower bound"

    findings = FINDINGS.read_text(encoding="utf-8")
    assert "steps 267-283" in findings
    assert "Williams ACC lower bound" in findings
    assert "7-of-7" in findings

    print("Step 283 checks passed")


if __name__ == "__main__":
    main()
