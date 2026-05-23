#!/usr/bin/env python3
"""Validate Step 212 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step212_connes_consani_audit_artifacts")
SOURCE = Path("/tmp/burnol_audit/connes_weil_archimedean.txt")

REQUIRED = [
    "step212_results_summary.md",
    "step212_schema.json",
    "content_classification_step212.csv",
    "nonclaim_boundary_step212.md",
    "step212_connes_consani_audit.tex",
    "analyze_connes_consani_step212.py",
    "run_step212_checks.py",
    "connes_consani_theorems_step212.csv",
    "translation_table_step212.csv",
    "branch_A_supplied_status_step212.csv",
    "relation_to_step_184_step212.csv",
    "residual_tree_step212.csv",
    "route_status_step212.csv",
    "construction_tasks_step212.csv",
    "classical_theorems_cited_step212.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"missing source text: {SOURCE}")
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step212_schema.json").read_text())
    assert schema["step"] == 212
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_connes_consani_related_but_not_sufficient"

    supplied = rows("branch_A_supplied_status_step212.csv")
    if not any(r["branch_A_gate"] == "G2 faithful boundary symbol" and r["connes_consani_supply"] == "not supplied" for r in supplied):
        raise SystemExit("G2 not-supplied status missing")
    trans = rows("translation_table_step212.csv")
    if not any(r["cascade_object"].startswith("q_eta") and r["match_status"] == "not_identified" for r in trans):
        raise SystemExit("translation mismatch for q_eta object missing")

    print("Step 212 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_connes_consani_related_but_not_sufficient")


if __name__ == "__main__":
    main()
