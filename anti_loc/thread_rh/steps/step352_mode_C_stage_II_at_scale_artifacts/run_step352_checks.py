#!/usr/bin/env python3
"""Validator for Step 352 Mode C Stage-II at-scale artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step352_mode_C_stage_II_at_scale_artifacts")

REQUIRED = [
    "mode_C_stage_II_at_scale_step352.py",
    "reproduction_table_step352.csv",
    "ablation_at_scale_step352.csv",
    "stage_III_readiness_step352.md",
    "step352_results_summary.md",
    "step352_schema.json",
    "nonclaim_boundary_step352.md",
    "run_step352_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step352_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 352
    assert schema["total_cells"] == 280
    assert schema["hecke_reproduction_cells"] == 70
    assert schema["zeta_descent_cells"] == 210
    assert schema["hecke_reproduction_pass_count"] == 70
    assert schema["zeta_OL_block_pass_count"] == 210
    assert schema["drop_OL_descent_decisions_changed"] == 210
    assert schema["mode_A_retract_count"] == 3
    assert schema["mode_C_retract_count"] == 0
    assert schema["stage_III_ready"] is True
    assert schema["final_verdict"] == "V_mode_C_stage_II_passes_at_scale_stage_III_ready"

    rows = read_csv("reproduction_table_step352.csv")
    assert len(rows) == 280
    hecke = [row for row in rows if row["cell_type"] == "hecke_reproduction"]
    zeta = [row for row in rows if row["cell_type"] == "zeta_descent_attempt"]
    assert len(hecke) == 70
    assert len(zeta) == 210
    assert all(row["cell_pass"] == "yes" for row in rows)
    assert all(row["relative_error"] == "0" for row in hecke)
    assert all(float(row["lambda_obs"]) > 0.0 for row in zeta)
    assert all(row["expected_behavior"] == "blocked_by_OL" for row in zeta)

    stats = read_csv("ablation_at_scale_step352.csv")
    assert len(stats) == 1
    stat = stats[0]
    assert int(stat["false_descent_cell_count"]) == 210
    assert int(stat["descent_decisions_changed"]) == 210
    assert float(stat["mean_relative_error"]) > 1.0
    assert float(stat["max_relative_error"]) > 50.0

    readiness = (BASE / "stage_III_readiness_step352.md").read_text(encoding="utf-8")
    assert "Affine log-normalizer" in readiness
    assert "Kernel-preserving transfer" in readiness

    boundary = (BASE / "nonclaim_boundary_step352.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary

    print("Step 352 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
