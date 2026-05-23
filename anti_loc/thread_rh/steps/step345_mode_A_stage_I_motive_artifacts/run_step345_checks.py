#!/usr/bin/env python3
"""Validate Step 345 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step345_mode_A_stage_I_motive_artifacts")
REQUIRED = [
    "virtual_motive_spec_step345.md",
    "finite_algebra_consistency_step345.csv",
    "stage_II_preview_step345.csv",
    "SAU_acceptance_gate_check_step345.csv",
    "step345_results_summary.md",
    "step345_schema.json",
    "nonclaim_boundary_step345.md",
    "run_step345_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step345_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 345
    assert schema["finite_kernel_N"] == 4
    assert schema["F_involution_verified_on_N4"] is True
    assert schema["bridge_claimed"] is False

    consistency = rows("finite_algebra_consistency_step345.csv")
    assert len(consistency) == 12
    assert all(r["equivalent_to_original"] == "yes" for r in consistency)
    assert all(r["defect_preserved"] == "yes" for r in consistency)

    preview = rows("stage_II_preview_step345.csv")
    assert len(preview) == 4
    assert all(float(r["relative_error"]) <= 0.05 for r in preview)
    assert any("Omega_retained" in r["defect_ledger_status"] for r in preview)

    sau = rows("SAU_acceptance_gate_check_step345.csv")
    assert all(r["pass_fail"].startswith("pass") for r in sau)

    nonclaim = (ART / "nonclaim_boundary_step345.md").read_text(encoding="utf-8")
    assert "No H6 bridge theorem is claimed" in nonclaim
    print("Step 345 validator: PASS")


if __name__ == "__main__":
    main()
