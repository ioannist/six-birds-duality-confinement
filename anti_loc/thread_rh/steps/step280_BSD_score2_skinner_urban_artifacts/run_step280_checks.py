#!/usr/bin/env python3
"""Validate Step 280 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step280_BSD_score2_skinner_urban_artifacts")
FINDINGS = Path("/home/repos/six-birds-foundations-iii/anti_loc/findings_framework.md")


REQUIRED = [
    "step280_results_summary.md",
    "step280_schema.json",
    "content_classification_step280.csv",
    "nonclaim_boundary_step280.md",
    "step280_BSD_score2_skinner_urban.tex",
    "skinner_urban_paper_extract_step280.md",
    "derive_BSD_bridge_step280.py",
    "run_step280_checks.py",
    "skinner_urban_verbatim_step280.csv",
    "hypotheses_excluded_step280.csv",
    "cascade_need_vs_supplied_step280.csv",
    "four_of_four_pattern_step280.csv",
    "residual_tree_step280.csv",
    "route_status_step280.csv",
    "construction_tasks_step280.csv",
    "classical_theorems_cited_step280.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step280_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 280
    assert schema["orientation"] == "cross_track_score2_audit"
    assert schema["final_verdict"] == "V_skinner_urban_BSD_bridge_blocked"

    verbatim_text = "\n".join(row["verbatim"] for row in read_csv("skinner_urban_verbatim_step280.csv"))
    for needle in ["ordinary", "irreducible", "q||N", "SL_2"]:
        assert needle in verbatim_text, f"missing Skinner-Urban hypothesis token: {needle}"

    excluded_text = "\n".join(row["excluded_case"] + " " + row["reason"] for row in read_csv("hypotheses_excluded_step280.csv"))
    for needle in ["non-ordinary", "residually reducible", "auxiliary ramification"]:
        assert needle in excluded_text, f"missing excluded case: {needle}"

    comparison = read_csv("cascade_need_vs_supplied_step280.csv")
    assert any(row["status"] == "not_derivable" for row in comparison)
    assert any("all-primes" in row["cascade_need"] for row in comparison)

    pattern = read_csv("four_of_four_pattern_step280.csv")
    assert len(pattern) == 4
    assert all(row["audited_score"] == "1" for row in pattern)
    assert pattern[-1]["candidate"] == "Skinner-Urban GL2 Iwasawa bridge"

    findings = FINDINGS.read_text(encoding="utf-8")
    assert "steps 267-280" in findings
    assert "Skinner-Urban GL2 Iwasawa bridge" in findings
    assert "4-of-4" in findings

    print("Step 280 checks passed")


if __name__ == "__main__":
    main()
