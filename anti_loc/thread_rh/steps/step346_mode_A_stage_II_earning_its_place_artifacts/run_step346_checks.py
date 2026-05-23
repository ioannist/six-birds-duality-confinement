#!/usr/bin/env python3
"""Validate Step 346 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step346_mode_A_stage_II_earning_its_place_artifacts")
REQUIRED = [
    "M_flat_realization_compute_step346.py",
    "stage_II_reproduction_table_step346.csv",
    "ablation_test_step346.csv",
    "step346_results_summary.md",
    "step346_schema.json",
    "nonclaim_boundary_step346.md",
    "run_step346_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step346_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 346
    assert schema["dps"] >= 80
    assert schema["reproduction_rows"] == 100
    assert schema["passed_under_1pct"] == 100
    assert schema["ablation_rows_broken"] == 100
    assert schema["omega_retained"] is True
    assert schema["bridge_claimed"] is False

    repro = rows("stage_II_reproduction_table_step346.csv")
    assert len(repro) == 100
    assert all(float(r["relative_error"]) < 0.01 for r in repro)
    assert sum(1 for r in repro if r["realization"] == "R_H") == 70
    assert sum(1 for r in repro if r["realization"] == "R_zeta") == 30
    assert any("Omega" in r["defect_ledger"] and "retained" in r["defect_ledger"] for r in repro)

    ablation = rows("ablation_test_step346.csv")
    broken = [r for r in ablation if r["breaks_reproduction"] == "yes"]
    assert len(broken) == 100
    assert any(r["breaks_reproduction"] == "no_numeric_break_but_sau_fail" for r in ablation)

    summary = (ART / "step346_results_summary.md").read_text(encoding="utf-8")
    assert "100/100" in summary
    nonclaim = (ART / "nonclaim_boundary_step346.md").read_text(encoding="utf-8")
    assert "No H6 bridge theorem is claimed" in nonclaim
    print("Step 346 validator: PASS")


if __name__ == "__main__":
    main()
