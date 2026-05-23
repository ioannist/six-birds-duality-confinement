#!/usr/bin/env python3
"""Validate Step 273 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step273_chowla_conjecture_artifacts"
FINDINGS = ROOT / "anti_loc/findings_framework.md"

REQUIRED = [
    "step273_results_summary.md",
    "step273_schema.json",
    "content_classification_step273.csv",
    "nonclaim_boundary_step273.md",
    "step273_chowla_conjecture.tex",
    "analyze_chowla_step273.py",
    "run_step273_checks.py",
    "chowla_declaration_step273.csv",
    "classification_step273.csv",
    "sub_sub_type_refinement_step273.csv",
    "corpus_inclusion_step273.csv",
    "residual_tree_step273.csv",
    "route_status_step273.csv",
    "construction_tasks_step273.csv",
    "classical_theorems_cited_step273.csv",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step273_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 273:
        raise SystemExit("schema step mismatch")
    if schema.get("final_verdict") != "V_chowla_in_Ia_pure_arithmetic_k_correlation":
        raise SystemExit("unexpected verdict")
    for key in [
        "orientation",
        "target",
        "chowla_carrier_definition",
        "classification_decision",
        "sub_sub_type_refinement",
        "framework_finding_target",
        "retained_nogos",
    ]:
        if key not in schema:
            raise SystemExit(f"schema missing key {key}")

    refinements = read_csv("sub_sub_type_refinement_step273.csv")
    if "k-correlation / multi-shift" not in {row["sub_sub_type"] for row in refinements}:
        raise SystemExit("k-correlation subtype missing")

    findings_text = FINDINGS.read_text(encoding="utf-8")
    if "Chowla multi-shift" not in findings_text or "Type-Ia refined and sub-subtyped" not in findings_text:
        raise SystemExit("findings_framework.md update missing")

    print("run_step273_checks.py PASS")


if __name__ == "__main__":
    main()
