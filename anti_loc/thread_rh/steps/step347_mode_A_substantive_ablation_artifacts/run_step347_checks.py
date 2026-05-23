#!/usr/bin/env python3
"""Validate Step 347 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step347_mode_A_substantive_ablation_artifacts")
REQUIRED = [
    "ablation_A_dropping_omega_from_FH_step347.csv",
    "ablation_B_dropping_omega_from_FZ_step347.csv",
    "ablation_C_dropping_F_omega_sign_step347.csv",
    "ablation_D_replacing_FH_with_Zprime_step347.csv",
    "compute_ablations_step347.py",
    "step347_results_summary.md",
    "step347_schema.json",
    "nonclaim_boundary_step347.md",
    "run_step347_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step347_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 347
    assert schema["final_verdict"] == "V_mode_A_stage_II_substantive_ablation_fails_algebra_decorative"
    assert schema["ablation_A_changed"] == 0
    assert schema["ablation_B_changed"] == 0
    assert schema["ablation_C_changed"] == 0
    assert schema["ablation_D_changed"] == 30

    for name in REQUIRED[:4]:
        data = rows(name)
        assert len(data) == 100

    a = rows("ablation_A_dropping_omega_from_FH_step347.csv")
    b = rows("ablation_B_dropping_omega_from_FZ_step347.csv")
    c = rows("ablation_C_dropping_F_omega_sign_step347.csv")
    d = rows("ablation_D_replacing_FH_with_Zprime_step347.csv")
    assert all(r["output_changed"] == "no" for r in a)
    assert all(r["output_changed"] == "no" for r in b)
    assert all(r["output_changed"] == "no" for r in c)
    assert sum(1 for r in c if r["F2_identity_preserved"] == "no") == 30
    assert sum(1 for r in d if r["output_changed"] == "yes") == 30
    assert sum(1 for r in d if r["reproduction_breaks"] == "yes") == 29

    summary = (ART / "step347_results_summary.md").read_text(encoding="utf-8")
    assert "algebra_decorative" in summary
    nonclaim = (ART / "nonclaim_boundary_step347.md").read_text(encoding="utf-8")
    assert "No RH or GRH claim" in nonclaim
    print("Step 347 validator: PASS")


if __name__ == "__main__":
    main()
