#!/usr/bin/env python3
"""Validator for Step 309 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step309_leibniz_j_distribution_artifacts")
REQUIRED = [
    "compute_zeta_derivatives_step309.py",
    "compute_leibniz_terms_step309.py",
    "zeta_derivatives_at_rho1_step309.csv",
    "leibniz_j_distribution_k10_step309.csv",
    "leibniz_j_distribution_k20_step309.csv",
    "leibniz_j_distribution_k30_step309.csv",
    "leibniz_j_distribution_k50_step309.csv",
    "dominant_j_and_interference_step309.csv",
    "step309_results_summary.md",
    "step309_schema.json",
    "nonclaim_boundary_step309.md",
    "run_step309_checks.py",
]


def rows(name: str) -> list[dict[str, str]]:
    with (ART / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    missing = [name for name in REQUIRED if not (ART / name).exists()]
    if missing:
        raise SystemExit(f"MISSING_STEP309_ARTIFACTS {missing}")
    zrows = rows("zeta_derivatives_at_rho1_step309.csv")
    if len(zrows) != 51 or {int(r["j"]) for r in zrows} != set(range(51)):
        raise SystemExit("BAD_ZETA_J_SET")
    for k in [10, 20, 30, 50]:
        dist = rows(f"leibniz_j_distribution_k{k}_step309.csv")
        if len(dist) != k + 1:
            raise SystemExit(f"BAD_TERM_COUNT k={k}")
    dom = rows("dominant_j_and_interference_step309.csv")
    if {int(r["k"]) for r in dom} != {10, 20, 30, 50}:
        raise SystemExit("BAD_DOM_K_SET")
    if any(float(r["interference_ratio_full_over_sum_abs"]) <= 0 for r in dom):
        raise SystemExit("BAD_INTERFERENCE")
    schema = json.loads((ART / "step309_schema.json").read_text(encoding="utf-8"))
    if schema.get("step") != 309:
        raise SystemExit("BAD_SCHEMA_STEP")
    print("STEP309_CHECKS_PASS")


if __name__ == "__main__":
    main()
