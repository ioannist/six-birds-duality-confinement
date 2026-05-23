#!/usr/bin/env python3
"""Validator for Step 332 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step332_G_prime_full_height_fit_artifacts")
REQUIRED = [
    "compute_L_k_G_prime_high_step332.py",
    "gamma_G_prime_all_zeros_step332.csv",
    "multivariate_fit_G_prime_15_step332.csv",
    "cross_G_universality_step332.csv",
    "step332_results_summary.md",
    "step332_schema.json",
    "nonclaim_boundary_step332.md",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")
    schema = json.loads((ART / "step332_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 332:
        raise SystemExit("schema step mismatch")
    gamma_rows = read_csv("gamma_G_prime_all_zeros_step332.csv")
    fit_rows = read_csv("multivariate_fit_G_prime_15_step332.csv")
    cross_rows = read_csv("cross_G_universality_step332.csv")
    if len(gamma_rows) != 15:
        raise SystemExit(f"expected 15 gamma rows, got {len(gamma_rows)}")
    if len([r for r in gamma_rows if r["source"] == "computed_step332"]) != 10:
        raise SystemExit("expected 10 newly computed rows")
    if not fit_rows or float(fit_rows[0]["A"]) == 0:
        raise SystemExit("missing multivariate fit")
    if not any(r["rho_index"] == "FIT_G_prime" for r in cross_rows):
        raise SystemExit("missing FIT_G_prime row")
    print("STEP332_CHECKS_PASS")
    print(f"gamma_rows={len(gamma_rows)} A_G_prime={float(fit_rows[0]['A']):.6g}")


if __name__ == "__main__":
    main()
