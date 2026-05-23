#!/usr/bin/env python3
"""Validate Step 218 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step218_wavepacket_extended_large_T_artifacts")

REQUIRED = [
    "step218_results_summary.md",
    "step218_schema.json",
    "content_classification_step218.csv",
    "nonclaim_boundary_step218.md",
    "step218_wavepacket_extended_large_T.tex",
    "compute_wavepacket_large_T_step218.py",
    "run_step218_checks.py",
    "wavepacket_large_T_step218.csv",
    "lim_inf_trend_step218.csv",
    "robustness_step218.csv",
    "residual_tree_step218.csv",
    "route_status_step218.csv",
    "construction_tasks_step218.csv",
]


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((BASE / "step218_schema.json").read_text())
    assert schema["step"] == 218
    assert schema["orientation"] == "adequacy"
    assert schema["final_verdict"] == "V_wavepacket_large_T_constant"

    vals = [float(r["C_l_u_T_norm"]) for r in rows("wavepacket_large_T_step218.csv")]
    if len(vals) != 4:
        raise SystemExit("expected four primary T values")
    if min(vals) <= 0.25:
        raise SystemExit("large-T lower bound unexpectedly small")
    if max(vals) - min(vals) >= 1e-3:
        raise SystemExit("large-T drift unexpectedly large")

    trend = rows("lim_inf_trend_step218.csv")[0]
    if trend["verdict"] != "V_wavepacket_large_T_constant":
        raise SystemExit("trend verdict mismatch")

    print("Step 218 validation passed")
    print(f"artifact_dir={BASE}")
    print("final_verdict=V_wavepacket_large_T_constant")


if __name__ == "__main__":
    main()
