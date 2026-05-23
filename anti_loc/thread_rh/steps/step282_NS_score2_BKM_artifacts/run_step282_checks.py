#!/usr/bin/env python3
"""Validate Step 282 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step282_NS_score2_BKM_artifacts")
FINDINGS = Path("/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md")


REQUIRED = [
    "step282_results_summary.md",
    "step282_schema.json",
    "content_classification_step282.csv",
    "nonclaim_boundary_step282.md",
    "step282_NS_score2_BKM.tex",
    "BKM_paper_extract_step282.md",
    "derive_NS_bridge_step282.py",
    "run_step282_checks.py",
    "BKM_verbatim_step282.csv",
    "criterion_vs_closure_step282.csv",
    "cascade_need_vs_supplied_step282.csv",
    "six_of_six_pattern_step282.csv",
    "residual_tree_step282.csv",
    "route_status_step282.csv",
    "construction_tasks_step282.csv",
    "classical_theorems_cited_step282.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step282_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 282
    assert schema["orientation"] == "cross_track_score2_audit"
    assert schema["final_verdict"] == "V_BKM_NS_bridge_blocked"

    verbatim = "\n".join(row["verbatim"] for row in read_csv("BKM_verbatim_step282.csv"))
    for needle in ["vorticity", "breakdown", "integral_0^T"]:
        assert needle in verbatim, f"missing BKM token: {needle}"

    distinction = read_csv("criterion_vs_closure_step282.csv")
    assert any(row["assessment"] == "criterion_not_closure" for row in distinction)
    assert any(row["assessment"] == "missing_bound" for row in distinction)

    comparison = read_csv("cascade_need_vs_supplied_step282.csv")
    assert any(row["status"] == "not_derivable" for row in comparison)
    assert any("global 3D NS" in row["cascade_need"] for row in comparison)

    pattern = read_csv("six_of_six_pattern_step282.csv")
    assert len(pattern) == 6
    assert all(row["audited_score"] == "1" for row in pattern)
    assert pattern[-1]["candidate"] == "BKM blowup criterion"

    findings = FINDINGS.read_text(encoding="utf-8")
    assert "steps 267-282" in findings
    assert "BKM blowup criterion" in findings
    assert "6-of-6" in findings

    print("Step 282 checks passed")


if __name__ == "__main__":
    main()
