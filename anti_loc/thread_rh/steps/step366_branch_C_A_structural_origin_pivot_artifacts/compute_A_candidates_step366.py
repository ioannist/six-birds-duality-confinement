#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

import mpmath as mp

mp.mp.dps = 80

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step366_branch_C_A_structural_origin_pivot_artifacts")

GAMMA_G_STAR = {
    1: mp.mpf("0.2046"),
    2: mp.mpf("0.1379"),
    3: mp.mpf("0.10021"),
    4: mp.mpf("0.08190"),
    5: mp.mpf("0.05208"),
}

A_GLOBAL_G_STAR = mp.mpf("4.118")
A_G_PRIME_5PT = mp.mpf("5.155")


def zeta_derivative(z, n):
    return mp.diff(lambda w: mp.zeta(w), z, n)


def main():
    pred_rows = []
    comp_rows = []
    for n in range(1, 6):
        rho = mp.zetazero(n)
        T = abs(mp.im(rho))
        gamma = GAMMA_G_STAR[n]
        A_emp = gamma * T

        density = mp.log(T / (2 * mp.pi)) / (2 * mp.pi)
        mean_spacing = 1 / density
        half_spacing = mean_spacing / 2
        full_spacing = mean_spacing

        zp = zeta_derivative(rho, 1)
        zpp = zeta_derivative(rho, 2)
        zeta_prime_inv = 1 / abs(zp)
        zeta_second_ratio_inv = 1 / abs(zpp / zp)

        candidates = [
            ("local_zero_density_half_spacing", half_spacing, "pi/log(T/(2*pi))"),
            ("plancherel_inverse_density", full_spacing, "2*pi/log(T/(2*pi))"),
            ("zeta_prime_inverse", zeta_prime_inv, "1/abs(zeta'(rho))"),
            ("zeta_second_over_first_inverse", zeta_second_ratio_inv, "1/abs(zeta''(rho)/zeta'(rho))"),
        ]
        for name, value, formula in candidates:
            rel_err = abs(value - A_emp) / abs(A_emp)
            pred_rows.append({
                "rho_index": n,
                "T": mp.nstr(T, 30),
                "candidate": name,
                "formula": formula,
                "A_candidate": mp.nstr(value, 30),
                "density_or_derivative_aux": (
                    mp.nstr(density, 30) if "density" in name or "spacing" in name
                    else mp.nstr(abs(zp), 30) if name == "zeta_prime_inverse"
                    else mp.nstr(abs(zpp / zp), 30)
                ),
            })
            comp_rows.append({
                "rho_index": n,
                "T": mp.nstr(T, 30),
                "gamma_G_star": mp.nstr(gamma, 20),
                "A_empirical_gamma_times_T": mp.nstr(A_emp, 30),
                "A_global_G_star_step324": mp.nstr(A_GLOBAL_G_STAR, 20),
                "A_G_prime_5pt_step331": mp.nstr(A_G_PRIME_5PT, 20),
                "candidate": name,
                "A_candidate": mp.nstr(value, 30),
                "relative_error": mp.nstr(rel_err, 30),
                "relative_error_vs_A_global_G_star_rho1_only": (
                    mp.nstr(abs(value - A_GLOBAL_G_STAR) / A_GLOBAL_G_STAR, 30) if n == 1 else ""
                ),
                "relative_error_vs_A_G_prime_5pt_rho1_only": (
                    mp.nstr(abs(value - A_G_PRIME_5PT) / A_G_PRIME_5PT, 30) if n == 1 else ""
                ),
                "within_20_percent": "yes" if rel_err <= mp.mpf("0.20") else "no",
            })

    with (OUT / "numerical_predictions_step366.csv").open("w", newline="") as f:
        fields = ["rho_index", "T", "candidate", "formula", "A_candidate", "density_or_derivative_aux"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(pred_rows)

    with (OUT / "comparison_to_empirical_step366.csv").open("w", newline="") as f:
        fields = [
            "rho_index", "T", "gamma_G_star", "A_empirical_gamma_times_T",
            "A_global_G_star_step324", "A_G_prime_5pt_step331",
            "candidate", "A_candidate", "relative_error",
            "relative_error_vs_A_global_G_star_rho1_only",
            "relative_error_vs_A_G_prime_5pt_rho1_only",
            "within_20_percent"
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(comp_rows)

    # Aggregate table for summary.
    best = {}
    for row in comp_rows:
        cand = row["candidate"]
        best.setdefault(cand, []).append(float(row["relative_error"]))
    aggregate = {
        cand: {
            "mean_rel_error": sum(vals) / len(vals),
            "max_rel_error": max(vals),
            "within20_count": sum(1 for v in vals if v <= 0.20),
        }
        for cand, vals in best.items()
    }

    schema = {
        "step": 366,
        "orientation": "Branch C structural-origin pivot",
        "mpmath_dps": 80,
        "empirical_fit_step324": "gamma ~= 4.118/T - 0.039*d^0.409",
        "candidates": list(best.keys()),
        "aggregate_relative_errors": aggregate,
        "best_candidate": min(aggregate, key=lambda k: aggregate[k]["mean_rel_error"]),
        "final_verdict": "partial_local_zero_density_half_spacing_candidate"
    }
    (OUT / "step366_schema.json").write_text(json.dumps(schema, indent=2) + "\n")


if __name__ == "__main__":
    main()
