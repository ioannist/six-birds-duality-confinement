#!/usr/bin/env python3
"""Validate Step 344 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step344_H6_multiplicative_G_prime_artifacts")
REQUIRED = [
    "compute_L_k_chi_G_prime_step344.py",
    "hecke_evaluators_G_prime_step344.csv",
    "multiplicative_fit_G_prime_step344.csv",
    "cross_G_coefficient_comparison_step344.csv",
    "step344_results_summary.md",
    "step344_schema.json",
    "nonclaim_boundary_step344.md",
    "run_step344_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((ART / "step344_schema.json").read_text(encoding="utf-8"))
    assert schema["step"] == 344
    assert schema["dps"] >= 80
    assert schema["final_verdict"] == "V_H6_multiplicative_G_prime_holdout_fails"

    evals = rows("hecke_evaluators_G_prime_step344.csv")
    assert len(evals) == 140
    assert {int(r["k"]) for r in evals} == set(range(1, 21))
    assert len({r["character"] for r in evals}) == 7

    fit = rows("multiplicative_fit_G_prime_step344.csv")
    train = [r for r in fit if r["row_type"] == "training_residual"]
    hold = [r for r in fit if r["row_type"] == "holdout_residual"]
    assert len(train) == 10
    assert len(hold) == 4
    assert max(float(r["relative_residual"]) for r in train) < 0.01
    assert max(float(r["relative_residual"]) for r in hold) > 0.01

    comp = rows("cross_G_coefficient_comparison_step344.csv")
    assert len(comp) == 9
    assert any(r["within_50pct"] == "False" for r in comp if r["parameter"].startswith("a_"))

    summary = (ART / "step344_results_summary.md").read_text(encoding="utf-8")
    assert "All exponents within 50% of G_star coefficients: `False`" in summary
    nonclaim = (ART / "nonclaim_boundary_step344.md").read_text(encoding="utf-8")
    assert "No RH or GRH claim" in nonclaim
    print("Step 344 validator: PASS")


if __name__ == "__main__":
    main()
