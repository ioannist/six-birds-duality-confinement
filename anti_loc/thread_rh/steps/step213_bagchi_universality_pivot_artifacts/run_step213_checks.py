#!/usr/bin/env python3
"""Validate Step 213 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step213_bagchi_universality_pivot_artifacts")

REQUIRED = [
    "step213_results_summary.md",
    "step213_schema.json",
    "content_classification_step213.csv",
    "nonclaim_boundary_step213.md",
    "step213_bagchi_universality_pivot.tex",
    "derive_bagchi_carrier_step213.py",
    "run_step213_checks.py",
    "bagchi_declaration_step213.csv",
    "CRE_audit_step213.csv",
    "classification_step213.csv",
    "derivative_carrier_check_step213.csv",
    "residual_tree_step213.csv",
    "route_status_step213.csv",
    "construction_tasks_step213.csv",
    "classical_theorems_cited_step213.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step213_schema.json").read_text())
    assert schema["step"] == 213
    assert schema["orientation"] == "adequacy"
    assert schema["CRE_status"] == "not_CRE"
    assert schema["final_verdict"] == "V_bagchi_outside_dichotomy"

    cre = rows("CRE_audit_step213.csv")
    if not any(r["claim"].startswith("Xi_Bagchi") and r["status"] == "proved_unconditionally" for r in cre):
        raise SystemExit("missing unconditional closure audit")

    cls = rows("classification_step213.csv")
    if not any(r["classification"] == "outside_dichotomy_scope" and r["status"] == "selected" for r in cls):
        raise SystemExit("missing outside-scope classification")

    print("Step 213 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_bagchi_outside_dichotomy")


if __name__ == "__main__":
    main()
