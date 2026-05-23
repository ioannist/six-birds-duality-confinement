#!/usr/bin/env python3
"""Validator for Step 279 Burnol a<1 audit artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step279_burnol_a_lt_1_audit_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step279_results_summary.md",
    "step279_schema.json",
    "content_classification_step279.csv",
    "nonclaim_boundary_step279.md",
    "step279_burnol_a_lt_1.tex",
    "burnol_2004_section_6_extract_step279.md",
    "derive_a_lt_1_form_step279.py",
    "run_step279_checks.py",
    "burnol_section_6_verbatim_step279.csv",
    "gap_assessment_step279.csv",
    "cand1_cand2_disagreement_step279.csv",
    "three_of_three_pattern_step279.csv",
    "residual_tree_step279.csv",
    "route_status_step279.csv",
    "construction_tasks_step279.csv",
    "classical_theorems_cited_step279.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step279_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 279
    assert schema["orientation"] == "paper_grounded_audit"
    assert schema["final_verdict"] == "V_burnol_a_lt_1_form_blocked"
    assert schema["burnol_section_6_audit"]["lambda_lt_1_span"] == "Z_lambda does not span K_lambda"
    assert "score-1" in schema["gap_assessment"]

    verbatim = "\n".join(row["verbatim"] for row in read_csv("burnol_section_6_verbatim_step279.csv"))
    assert "if and only if lambda>=1" in verbatim
    assert "do not span K_lambda if lambda<1" in verbatim

    gaps = read_csv("gap_assessment_step279.csv")
    assert any(row["score"] == "1" and row["gap_type"] == "blocked" for row in gaps)

    pattern = read_csv("three_of_three_pattern_step279.csv")
    assert len(pattern) == 3
    assert all(row["audited_score"] == "1" for row in pattern)

    findings = FINDINGS.read_text(encoding="utf-8")
    assert "Empirical score-2 downgrade pattern" in findings
    assert "Burnol `a<1` linear-combination form" in findings

    print("run_step279_checks.py PASS")


if __name__ == "__main__":
    main()
