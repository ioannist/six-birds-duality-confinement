#!/usr/bin/env python3
"""Validate Step 221 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step221_cross_track_BSD_CTMT_test_artifacts")

REQUIRED = [
    "step221_results_summary.md",
    "step221_schema.json",
    "content_classification_step221.csv",
    "nonclaim_boundary_step221.md",
    "step221_cross_track_BSD_CTMT_test.tex",
    "run_step221_checks.py",
    "BSD_records_summary_step221.csv",
    "literature_audit_step221.csv",
    "CTMT_recursion_layers_step221.csv",
    "cross_track_implication_step221.csv",
    "residual_tree_step221.csv",
    "route_status_step221.csv",
    "construction_tasks_step221.csv",
    "classical_theorems_cited_step221.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step221_schema.json").read_text())
    assert schema["step"] == 221
    assert schema["orientation"] == "cross-track-framework-validation"
    assert schema["final_verdict"] == "V_bsd_CTMT_recursion_verified"

    lit = rows("literature_audit_step221.csv")
    if len(lit) < 8:
        raise SystemExit("literature audit missing candidate sources")
    layers = rows("CTMT_recursion_layers_step221.csv")
    if len(layers) < 6:
        raise SystemExit("recursion layer table too short")
    implication = rows("cross_track_implication_step221.csv")[0]
    if "verified_on_2_track" not in implication["after_step221"]:
        raise SystemExit("framework upgrade status mismatch")

    print("Step 221 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_bsd_CTMT_recursion_verified")


if __name__ == "__main__":
    main()
