#!/usr/bin/env python3
"""Validator for Step 275 QUE classification artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step275_QUE_classification_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"


REQUIRED = [
    "step275_results_summary.md",
    "step275_schema.json",
    "content_classification_step275.csv",
    "nonclaim_boundary_step275.md",
    "step275_QUE_classification.tex",
    "analyze_QUE_step275.py",
    "run_step275_checks.py",
    "QUE_declaration_step275.csv",
    "classification_step275.csv",
    "watson_bridge_step275.csv",
    "corpus_inclusion_step275.csv",
    "residual_tree_step275.csv",
    "route_status_step275.csv",
    "construction_tasks_step275.csv",
    "classical_theorems_cited_step275.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step275_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 275
    assert schema["orientation"] == "adequacy"
    assert schema["target"] == "QUE classification within framework"
    assert schema["final_verdict"] == "V_que_in_subconvexity"
    for key in [
        "QUE_carrier_definition",
        "classification_decision",
        "watson_bridge",
        "framework_finding_target",
        "retained_nogos",
    ]:
        assert key in schema, key

    classification = read_csv("classification_step275.csv")
    assert any(row["candidate_finding"] == "Subconvexity Extension" and row["fit"] == "primary" for row in classification)
    assert any(row["candidate_finding"] == "Cross-Correlation Extension" and row["fit"] == "secondary" for row in classification)
    assert any(row["candidate_finding"] == "SCDG" and row["fit"] == "no" for row in classification)
    assert any(row["candidate_finding"] == "new_11th_finding" and row["fit"] == "not_needed" for row in classification)

    watson = "\n".join(",".join(row.values()) for row in read_csv("watson_bridge_step275.csv"))
    assert "central" in watson and "L-value" in watson
    assert "Subconvexity Type alpha" in watson

    sources = read_csv("classical_theorems_cited_step275.csv")
    source_blob = "\n".join(row["source"] for row in sources)
    for needle in [
        "Rudnick",
        "Watson",
        "Lindenstrauss",
        "Soundararajan",
        "Holowinsky",
    ]:
        assert needle in source_blob, needle

    findings = FINDINGS.read_text(encoding="utf-8")
    assert "QUE / Watson bridge carrier" in findings
    assert "QUE secondary bridge note" in findings
    assert "verified-on-5-growth-rate-or-subconvexity-bridge-instances" in findings

    print("run_step275_checks.py PASS")


if __name__ == "__main__":
    main()
