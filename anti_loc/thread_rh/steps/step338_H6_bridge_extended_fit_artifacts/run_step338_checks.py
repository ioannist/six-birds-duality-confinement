#!/usr/bin/env python3
"""Validate Step 338 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts")
REQUIRED = [
    "compute_extended_bridge_step338.py",
    "additional_hecke_evaluators_step338.csv",
    "extended_bridge_fit_step338.csv",
    "cross_validation_step338.csv",
    "step338_results_summary.md",
    "step338_schema.json",
    "nonclaim_boundary_step338.md",
    "run_step338_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step338_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 338
    assert schema["dps"] >= 80
    assert schema["fit_k"] == list(range(1, 11))
    assert schema["holdout_k"] == [11, 12, 15, 20]

    add = rows("additional_hecke_evaluators_step338.csv")
    assert len(add) == 30, f"expected 30 additional evaluator rows, got {len(add)}"
    assert {r["character"] for r in add} == {"chi_7b", "chi_11c", "chi_13a"}
    assert {int(r["k"]) for r in add} == set(range(1, 11))

    fit = rows("extended_bridge_fit_step338.csv")
    coeffs = [r for r in fit if r["row_type"] == "complex_coefficient"]
    train = [r for r in fit if r["row_type"] == "complex_fit_residual"]
    assert len(coeffs) == 7
    assert len(train) == 10
    assert max(float(r["relative_residual"]) for r in train) < 0.01

    hold = rows("cross_validation_step338.csv")
    assert [int(r["k"]) for r in hold] == [11, 12, 15, 20]
    assert any(float(r["relative_residual"]) >= 0.01 for r in hold), "holdout unexpectedly all passed"

    summary = (ART / "step338_results_summary.md").read_text(encoding="utf-8")
    assert "V_hecke_H6_extended_fit_overfit_holdout_fails" in summary
    assert "No RH or GRH claim" in (ART / "nonclaim_boundary_step338.md").read_text(encoding="utf-8")
    print("Step 338 validator: PASS")


if __name__ == "__main__":
    main()
