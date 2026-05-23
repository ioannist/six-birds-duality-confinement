#!/usr/bin/env python3
"""Validate Step 324 artifact contract."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step324_gamma_vs_zero_spacing_artifacts")
REQUIRED = [
    "compute_d_k_step324.py",
    "gamma_vs_d_k_step324.csv",
    "correlation_fits_step324.csv",
    "multivariate_fit_step324.csv",
    "step324_results_summary.md",
    "step324_schema.json",
    "nonclaim_boundary_step324.md",
    "run_step324_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    missing = [p for p in REQUIRED if not (ART / p).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")
    data = rows("gamma_vs_d_k_step324.csv")
    if len(data) != 15:
        raise SystemExit(f"expected 15 gamma-gap rows, found {len(data)}")
    fits = rows("correlation_fits_step324.csv")
    if len(fits) != 4:
        raise SystemExit(f"expected 4 one-variable fits, found {len(fits)}")
    multi = rows("multivariate_fit_step324.csv")
    if len(multi) < 2:
        raise SystemExit("missing multivariate fit rows")
    schema = json.loads((ART / "step324_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 324:
        raise SystemExit("schema step incorrect")
    if "RH" not in (ART / "nonclaim_boundary_step324.md").read_text(encoding="utf-8"):
        raise SystemExit("nonclaim boundary missing RH")
    print("STEP324_CHECKS_PASS")


if __name__ == "__main__":
    main()
