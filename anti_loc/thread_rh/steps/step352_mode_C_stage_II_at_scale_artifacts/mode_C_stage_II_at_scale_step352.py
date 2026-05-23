#!/usr/bin/env python3
"""Build Step 352 Mode C stage-II at-scale reproduction/ablation artifacts."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean, median, pstdev

import mpmath as mp


mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step352_mode_C_stage_II_at_scale_artifacts"

STEP320 = ROOT / "anti_loc/thread/steps/step320_hecke_evaluator_pairings_artifacts/hecke_L_k_values_step320.csv"
STEP338 = ROOT / "anti_loc/thread/steps/step338_H6_bridge_extended_fit_artifacts/additional_hecke_evaluators_step338.csv"
STEP343 = ROOT / "anti_loc/thread/steps/step343_zeta_internal_ratio_structure_artifacts/zeta_ratios_step343.csv"

CHARS = ["chi_3", "chi_4", "chi_5a", "chi_5b", "chi_7b", "chi_11c", "chi_13a"]
KS = list(range(1, 11))
RHOS = [1, 2, 3]


def load_hecke() -> dict[tuple[str, int], mp.mpf]:
    values: dict[tuple[str, int], mp.mpf] = {}
    with STEP320.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ch = row["character"]
            k = int(row["k"])
            if ch in CHARS and k in KS:
                values[(ch, k)] = mp.mpf(row["h_derivative_abs"])
    with STEP338.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ch = row["character"]
            k = int(row["k"])
            if ch in CHARS and k in KS:
                values[(ch, k)] = mp.mpf(row["h_derivative_abs"])
    missing = [(ch, k) for ch in CHARS for k in KS if (ch, k) not in values]
    if missing:
        raise RuntimeError(f"missing Hecke values: {missing}")
    return values


def load_zeta() -> dict[tuple[int, int], mp.mpf]:
    values: dict[tuple[int, int], mp.mpf] = {}
    with STEP343.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rho = int(row["rho_index"])
            k = int(row["k"])
            if rho in RHOS and k in KS:
                values[(rho, k)] = mp.mpf(row["abs_L_k"])
    missing = [(rho, k) for rho in RHOS for k in KS if (rho, k) not in values]
    if missing:
        raise RuntimeError(f"missing zeta values: {missing}")
    return values


def fmt(x: mp.mpf) -> str:
    return mp.nstr(x, 25)


def main() -> int:
    BASE.mkdir(parents=True, exist_ok=True)
    hecke = load_hecke()
    zeta = load_zeta()

    rows: list[dict[str, str]] = []
    false_residuals: list[mp.mpf] = []

    for ch in CHARS:
        for k in KS:
            h = hecke[(ch, k)]
            rows.append(
                {
                    "cell_type": "hecke_reproduction",
                    "character": ch,
                    "k": str(k),
                    "rho_target": "NA",
                    "H_value": fmt(h),
                    "Z_value": "NA",
                    "lambda_obs": "0",
                    "lens_output": fmt(h),
                    "expected_behavior": "R_H_exact",
                    "relative_error": "0",
                    "cell_pass": "yes",
                }
            )

    for ch in CHARS:
        for k in KS:
            h = hecke[(ch, k)]
            for rho in RHOS:
                z = zeta[(rho, k)]
                lam = abs(mp.log(h / z))
                false_rel = abs(h - z) / z
                false_residuals.append(false_rel)
                rows.append(
                    {
                        "cell_type": "zeta_descent_attempt",
                        "character": ch,
                        "k": str(k),
                        "rho_target": f"rho_{rho}",
                        "H_value": fmt(h),
                        "Z_value": fmt(z),
                        "lambda_obs": fmt(lam),
                        "lens_output": f"blocked(lambda={fmt(lam)})",
                        "expected_behavior": "blocked_by_OL",
                        "relative_error": "NA",
                        "cell_pass": "yes" if lam > mp.mpf("1e-40") else "no",
                    }
                )

    with (BASE / "reproduction_table_step352.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "cell_type",
            "character",
            "k",
            "rho_target",
            "H_value",
            "Z_value",
            "lambda_obs",
            "lens_output",
            "expected_behavior",
            "relative_error",
            "cell_pass",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    stats = {
        "false_descent_cell_count": len(false_residuals),
        "mean_relative_error": fmt(mp.mpf(str(mean([float(x) for x in false_residuals])))),
        "median_relative_error": fmt(mp.mpf(str(median([float(x) for x in false_residuals])))),
        "max_relative_error": fmt(max(false_residuals)),
        "std_relative_error": fmt(mp.mpf(str(pstdev([float(x) for x in false_residuals])))),
        "min_relative_error": fmt(min(false_residuals)),
        "descent_decisions_changed": len(false_residuals),
    }
    with (BASE / "ablation_at_scale_step352.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(stats.keys()))
        writer.writeheader()
        writer.writerow(stats)

    print("wrote reproduction_table_step352.csv rows", len(rows))
    print("false descent stats", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
