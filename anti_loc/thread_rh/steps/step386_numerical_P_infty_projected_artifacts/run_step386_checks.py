#!/usr/bin/env python3
"""Validate Step 386 artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step386_numerical_P_infty_projected_artifacts")
REQUIRED = [
    "c_n_k_rho_grid_step386.csv",
    "L_k_projected_step386.csv",
    "gamma_projected_comparison_step386.csv",
    "step386_results_summary.md",
    "step386_schema.json",
    "nonclaim_boundary_step386.md",
    "run_step386_checks.py",
]


def read_rows(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    missing = [name for name in REQUIRED if not (OUT / name).exists()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    schema = json.loads((OUT / "step386_schema.json").read_text())
    if schema.get("step") != 386:
        raise SystemExit("schema step mismatch")
    if schema.get("verdict") != "blocked_missing_numerical_c_nk_Dn_evaluator":
        raise SystemExit("unexpected verdict")

    c_rows = read_rows("c_n_k_rho_grid_step386.csv")
    if len(c_rows) != 620:
        raise SystemExit(f"expected 620 attempted c-grid rows, found {len(c_rows)}")
    if any(row["status"] != "blocked" for row in c_rows):
        raise SystemExit("all c-grid rows must be blocked")
    if any(row["abs_c_n_k_rho"] for row in c_rows):
        raise SystemExit("blocked c-grid rows must not contain fabricated magnitudes")

    l_rows = read_rows("L_k_projected_step386.csv")
    if len(l_rows) != 20:
        raise SystemExit(f"expected 20 L rows, found {len(l_rows)}")
    if any(row["status"] != "blocked_projected_sum" for row in l_rows):
        raise SystemExit("all L rows must be blocked projected sums")
    if any(row["L_k_projected_abs"] for row in l_rows):
        raise SystemExit("blocked projected rows must not contain fabricated L values")

    g_rows = read_rows("gamma_projected_comparison_step386.csv")
    if len(g_rows) != 4:
        raise SystemExit(f"expected 4 gamma rows, found {len(g_rows)}")
    if any(row["status"] != "blocked" for row in g_rows):
        raise SystemExit("all projected gamma rows must be blocked")
    if any(row["gamma_projected"] for row in g_rows):
        raise SystemExit("blocked projected gamma rows must not contain fabricated gamma values")

    summary = (OUT / "step386_results_summary.md").read_text()
    if "Numeric c_{n,k}(rho) cells computed: 0" not in summary:
        raise SystemExit("summary must state zero numeric coefficient cells")
    if "No RH claim" not in (OUT / "nonclaim_boundary_step386.md").read_text():
        raise SystemExit("nonclaim boundary missing RH statement")

    print("step386 checks passed")


if __name__ == "__main__":
    main()
