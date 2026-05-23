#!/usr/bin/env python3
"""Validator for Step 331 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step331_G_prime_gamma_fit_artifacts")
REQUIRED = [
    "compute_L_k_G_prime_step331.py",
    "L_k_G_prime_step331.csv",
    "gamma_per_rho_G_prime_step331.csv",
    "multivariate_fit_G_prime_step331.csv",
    "comparison_G_star_vs_G_prime_step331.csv",
    "step331_results_summary.md",
    "step331_schema.json",
    "nonclaim_boundary_step331.md",
]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"missing artifacts: {missing}")
    schema = json.loads((ART / "step331_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 331:
        raise SystemExit("schema step mismatch")
    l_rows = read_csv("L_k_G_prime_step331.csv")
    gamma_rows = read_csv("gamma_per_rho_G_prime_step331.csv")
    multi = read_csv("multivariate_fit_G_prime_step331.csv")
    comp = read_csv("comparison_G_star_vs_G_prime_step331.csv")
    if len(l_rows) != 25:
        raise SystemExit(f"expected 25 L_k rows, got {len(l_rows)}")
    if len(gamma_rows) != 5:
        raise SystemExit(f"expected 5 gamma rows, got {len(gamma_rows)}")
    if not multi or float(multi[0]["A"]) == 0:
        raise SystemExit("missing/zero multivariate A")
    if not any(row["G_id"] == "ratio_G_prime_over_G_star" for row in comp):
        raise SystemExit("missing comparison ratio row")
    print("STEP331_CHECKS_PASS")
    print(f"gamma_rows={len(gamma_rows)} A_G_prime={float(multi[0]['A']):.6g}")


if __name__ == "__main__":
    main()
