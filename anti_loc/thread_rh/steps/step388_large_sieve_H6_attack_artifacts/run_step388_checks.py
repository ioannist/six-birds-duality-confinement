#!/usr/bin/env python3
"""Validate Step 388 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step388_large_sieve_H6_attack_artifacts")
REQUIRED = [
    "large_sieve_bridge_attempt_step388.md",
    "hecke_linear_form_step388.csv",
    "family_averaged_comparison_step388.csv",
    "step388_results_summary.md",
    "step388_schema.json",
    "nonclaim_boundary_step388.md",
    "run_step388_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")

    schema = json.loads((ART / "step388_schema.json").read_text())
    if schema.get("step") != 388:
        raise SystemExit("wrong step")
    if schema.get("mpmath_dps", 0) < 50:
        raise SystemExit("mpmath precision below requirement")
    if schema.get("verdict") != "mismatch_large_sieve_common_alpha_condition_fails":
        raise SystemExit("unexpected verdict")

    coeff = rows("hecke_linear_form_step388.csv")
    fam = rows("family_averaged_comparison_step388.csv")
    if len(coeff) < 100:
        raise SystemExit("too few coefficient rows")
    if len(fam) != 5:
        raise SystemExit("expected five family-average k rows")
    if not all("fails_common_alpha_condition" in row["large_sieve_hypothesis_status"] for row in coeff):
        raise SystemExit("coefficient rows must record common-alpha failure")
    for row in fam:
        float(row["hecke_empirical_mean_abs2"])
        float(row["zeta_empirical_mean_abs2"])
        float(row["hecke_over_zeta_mean_abs2"])
        if "inapplicable" not in row["status"]:
            raise SystemExit("family comparison rows must be diagnostic/inapplicable")

    md = (ART / "large_sieve_bridge_attempt_step388.md").read_text()
    if "Conrey-Iwaniec-Soundararajan 2011" not in md:
        raise SystemExit("external anchor missing")
    if "alpha_n^{(chi,k)}" not in md:
        raise SystemExit("linear form formula missing")
    if "No RH claim" not in (ART / "nonclaim_boundary_step388.md").read_text():
        raise SystemExit("nonclaim boundary missing")

    print("step388 checks passed")


if __name__ == "__main__":
    main()
