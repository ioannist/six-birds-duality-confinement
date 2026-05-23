#!/usr/bin/env python3
"""Validate Step 217 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step217_branch_A_wavepacket_weyl_artifacts")

REQUIRED = [
    "step217_results_summary.md",
    "step217_schema.json",
    "content_classification_step217.csv",
    "nonclaim_boundary_step217.md",
    "step217_branch_A_wavepacket_weyl.tex",
    "compute_wavepacket_step217.py",
    "run_step217_checks.py",
    "wavepacket_step217.csv",
    "weak_null_pairwise_step217.csv",
    "trend_step217.csv",
    "robustness_step217.csv",
    "residual_tree_step217.csv",
    "route_status_step217.csv",
    "construction_tasks_step217.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step217_schema.json").read_text())
    assert schema["step"] == 217
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_wavepacket_essential_obstruction"

    wave = rows("wavepacket_step217.csv")
    if len(wave) != 10:
        raise SystemExit(f"expected 10 wavepacket rows, got {len(wave)}")
    vals = [float(r["C_l_u_n_norm"]) for r in wave]
    if min(vals) <= 0.2:
        raise SystemExit("primary wavepacket lower bound unexpectedly small")

    trend = rows("trend_step217.csv")[0]
    if trend["verdict"] != "V_wavepacket_essential_obstruction":
        raise SystemExit("trend verdict mismatch")
    if float(trend["weak_null_max_pairwise_overlap"]) >= 1e-3:
        raise SystemExit("weak-null overlap too large")

    print("Step 217 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_wavepacket_essential_obstruction")


if __name__ == "__main__":
    main()
