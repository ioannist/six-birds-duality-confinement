#!/usr/bin/env python3
"""Validate Step 272 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step272_sarnak_mobius_orthogonality_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step272_results_summary.md",
    "step272_schema.json",
    "content_classification_step272.csv",
    "nonclaim_boundary_step272.md",
    "step272_sarnak_mobius.tex",
    "analyze_MO_classification_step272.py",
    "run_step272_checks.py",
    "MO_declaration_step272.csv",
    "classification_step272.csv",
    "subtype_refinement_step272.csv",
    "corpus_inclusion_step272.csv",
    "residual_tree_step272.csv",
    "route_status_step272.csv",
    "construction_tasks_step272.csv",
    "classical_theorems_cited_step272.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step272_schema.json").read_text(encoding="utf-8"))
    for key in [
        "step",
        "orientation",
        "target",
        "MO_carrier_definition",
        "classification_decision",
        "framework_finding_target",
        "retained_nogos",
        "final_verdict",
    ]:
        if key not in schema:
            raise SystemExit(f"schema missing key {key}")
    if schema["step"] != 272:
        raise SystemExit("schema step mismatch")
    if schema["final_verdict"] != "V_sarnak_in_cross_correlation_Ia":
        raise SystemExit("unexpected verdict")

    classifications = read_csv("classification_step272.csv")
    cc = [row for row in classifications if row["candidate_finding"] == "Cross-Correlation Extension"]
    if not cc or cc[0]["decision"] != "Type Ia-arithmetic-dynamical":
        raise SystemExit("Cross-Correlation classification missing")

    subtypes = read_csv("subtype_refinement_step272.csv")
    if "Ia-arithmetic-dynamical" not in {row["type"] for row in subtypes}:
        raise SystemExit("new subtype missing")

    findings_text = FINDINGS.read_text(encoding="utf-8")
    if "Type Ia-arithmetic-dynamical" not in findings_text or "step 272" not in findings_text:
        raise SystemExit("findings_framework.md was not updated")

    print("run_step272_checks.py PASS")


if __name__ == "__main__":
    main()
