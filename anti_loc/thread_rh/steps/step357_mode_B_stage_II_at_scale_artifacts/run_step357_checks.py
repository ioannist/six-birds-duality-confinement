#!/usr/bin/env python3
"""Validator for Step 357 Mode B Stage-II at-scale artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step357_mode_B_stage_II_at_scale_artifacts")

REQUIRED = [
    "mode_B_stage_II_at_scale_step357.py",
    "reproduction_at_scale_step357.csv",
    "ablation_at_scale_step357.csv",
    "step357_results_summary.md",
    "step357_schema.json",
    "nonclaim_boundary_step357.md",
    "run_step357_checks.py",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [name for name in REQUIRED if not (BASE / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    with (BASE / "step357_schema.json").open(encoding="utf-8") as f:
        schema = json.load(f)
    assert schema["step"] == 357
    assert schema["total_reproduction_cells"] == 520
    assert schema["hecke_atom_cells"] == 70
    assert schema["zeta_atom_cells"] == 30
    assert schema["compare_cells"] == 210
    assert schema["operator_audit_cells"] == 210
    assert schema["reproduction_pass_count"] == 520
    assert schema["ablation_count"] == 3
    assert schema["ablation_broken_cells_total"] == 630
    assert schema["target_tau_used"] is False
    assert schema["mode_B_retract_count"] == 0
    assert schema["final_verdict"] == "V_mode_B_stage_II_passes_at_scale_substantive"

    rows = read_csv("reproduction_at_scale_step357.csv")
    assert len(rows) == 520
    counts = Counter(row["cell_type"] for row in rows)
    assert counts["hecke_atom"] == 70
    assert counts["zeta_atom"] == 30
    assert counts["compare"] == 210
    assert counts["operator_audit"] == 210
    assert all(row["cell_pass"] == "yes" for row in rows)
    assert all(row["relative_error"] == "0" for row in rows)

    ablations = read_csv("ablation_at_scale_step357.csv")
    assert len(ablations) == 3
    assert all(row["substantive"] == "yes" for row in ablations)
    assert {row["ablation"] for row in ablations} == {"remove_R_compare", "remove_R_operator_audit", "remove_R_block"}
    assert sum(int(row["broken_cells"]) for row in ablations) == 630

    boundary = (BASE / "nonclaim_boundary_step357.md").read_text(encoding="utf-8")
    assert "No RH" in boundary
    assert "GRH" in boundary
    assert "No H6 bridge" in boundary
    assert "target transfer `tau` is not used" in boundary

    print("Step 357 validator: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
