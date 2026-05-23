#!/usr/bin/env python3
"""Validate Step 384 Riemann-Siegel derivation artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step384_riemann_siegel_gamma_derivation_artifacts")


def rows(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(newline="") as fh:
        return list(csv.DictReader(fh))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"STEP384_CHECK_FAIL: {msg}")


def main() -> None:
    required = [
        "riemann_siegel_derivation_step384.md",
        "derived_gamma_vs_empirical_step384.csv",
        "step384_results_summary.md",
        "step384_schema.json",
        "nonclaim_boundary_step384.md",
        "run_step384_checks.py",
    ]
    for name in required:
        require((BASE / name).exists(), f"missing {name}")

    data = rows("derived_gamma_vs_empirical_step384.csv")
    require(len(data) == 15, f"expected 15 rows, got {len(data)}")
    schema = json.loads((BASE / "step384_schema.json").read_text())
    require(schema["dps"] >= 80, "dps below hard constraint")
    require(schema["derived_gamma_formula"] == "gamma_RS(T)=1-log(log(T/(2*pi)))", "formula mismatch")
    require(schema["rmse_RS_direct"] > 10 * schema["rmse_branch_C_structural"], "RS formula not clearly worse than Branch C structural law")
    require(schema["verdict"] == "different_formula_projection_missing", "verdict mismatch")

    deriv = (BASE / "riemann_siegel_derivation_step384.md").read_text()
    require("theta(t) = (t/2)log(t/(2pi))" in deriv, "missing Riemann-Siegel theta asymptotic")
    require("r_* ~ k/log(T/(2pi))" in deriv, "missing saddle equation")
    require("Burnol/Sonine projector" in deriv, "missing projector gap")

    boundary = (BASE / "nonclaim_boundary_step384.md").read_text().lower()
    require("does not prove rh" in boundary, "missing RH nonclaim")
    require("unprojected" in boundary, "missing unprojected caveat")

    print("STEP384_CHECK_PASS")
    print(f"rows={len(data)}")
    print(f"rmse_RS={schema['rmse_RS_direct']:.12g}")
    print(f"rmse_struct={schema['rmse_branch_C_structural']:.12g}")
    print(f"verdict={schema['verdict']}")


if __name__ == "__main__":
    main()
