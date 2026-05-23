#!/usr/bin/env python3
"""Validate Step 328 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step328_hecke_H4_constructive_subfamily_artifacts")
REQUIRED = [
    "compute_H4_constructive_subfamily_step328.py",
    "kappa_chi_values_step328.csv",
    "P_infty_chi_step328.csv",
    "H4_finite_matrix_residual_step328.csv",
    "step328_results_summary.md",
    "step328_schema.json",
    "nonclaim_boundary_step328.md",
    "run_step328_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    kappa = rows("kappa_chi_values_step328.csv")
    if len(kappa) != 84:
        raise SystemExit(f"expected 84 kappa rows, found {len(kappa)}")
    p_rows = rows("P_infty_chi_step328.csv")
    if len(p_rows) != 4:
        raise SystemExit(f"expected 4 projection rows, found {len(p_rows)}")
    residual = rows("H4_finite_matrix_residual_step328.csv")
    if len(residual) != 36:
        raise SystemExit(f"expected 36 residual matrix rows, found {len(residual)}")
    schema = json.loads((ART / "step328_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 328:
        raise SystemExit("schema step incorrect")
    if "GRH" not in (ART / "nonclaim_boundary_step328.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing GRH")
    print("STEP328_CHECKS_PASS")


if __name__ == "__main__":
    main()
