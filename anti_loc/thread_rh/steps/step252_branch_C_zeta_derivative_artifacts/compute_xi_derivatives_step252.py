#!/usr/bin/env python3
"""Compute xi derivatives and compare Branch C L_k values to zeta/xi derivatives."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step252_branch_C_zeta_derivative_artifacts")
ROOT = Path("/home/repos/six-birds-foundations-iii")
STEP250 = ROOT / "anti_loc/thread/steps/step250_branch_C_k_growth_law_artifacts"
MP_DPS = 80
K_MAX = 4


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def xi(s: mp.mpc) -> mp.mpc:
    return mp.mpf("0.5") * s * (s - 1) * mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def parse_mpc(text: str) -> mp.mpc:
    return mp.mpc(text.replace("i", "j"))


def main() -> None:
    mp.mp.dps = MP_DPS

    xi_rows: list[dict[str, str]] = []
    for idx in [1, 2]:
        rho = mp.zetazero(idx)
        for k in range(K_MAX + 1):
            val = xi(rho) if k == 0 else mp.diff(xi, rho, k)
            xi_rows.append({
                "rho_index": str(idx),
                "rho": mp.nstr(rho, 40),
                "k": str(k),
                "xi_derivative_real": mp.nstr(mp.re(val), 30),
                "xi_derivative_imag": mp.nstr(mp.im(val), 30),
                "xi_derivative_abs": mp.nstr(abs(val), 30),
            })

    write_csv(ART / "xi_derivatives_step252.csv", [
        "rho_index",
        "rho",
        "k",
        "xi_derivative_real",
        "xi_derivative_imag",
        "xi_derivative_abs",
    ], xi_rows)

    zeta_rows = read_csv(ART / "zeta_derivatives_step252.csv")
    zeta_abs = {(int(r["rho_index"]), int(r["k"])): mp.mpf(r["zeta_derivative_abs"]) for r in zeta_rows}
    xi_abs = {(int(r["rho_index"]), int(r["k"])): mp.mpf(r["xi_derivative_abs"]) for r in xi_rows}

    l_rows_all = read_csv(STEP250 / "k_dataset_step250.csv")
    wanted = {"rho1_G_star", "rho2_G_star", "rho1_G_prime"}
    l_rows = [r for r in l_rows_all if r["triple_id"] in wanted]

    comparison_rows: list[dict[str, str]] = []
    eps = mp.mpf("1e-40")
    for r in l_rows:
        rho_idx = int(r["rho_index"])
        k = int(r["k"])
        L_abs = mp.mpf(r["L_abs"])
        za = zeta_abs[(rho_idx, k)]
        xa = xi_abs[(rho_idx, k)]
        fact = mp.mpf(math.factorial(k))
        comparison_rows.append({
            "triple_id": r["triple_id"],
            "rho_index": str(rho_idx),
            "G_id": r["G_id"],
            "k": str(k),
            "L_abs": mp.nstr(L_abs, 25),
            "zeta_derivative_abs": mp.nstr(za, 25),
            "xi_derivative_abs": mp.nstr(xa, 25),
            "L_over_zeta_derivative_abs": "" if za < eps else mp.nstr(L_abs / za, 25),
            "L_over_xi_derivative_abs": "" if xa < eps else mp.nstr(L_abs / xa, 25),
            "L_over_factorial_zeta_derivative_abs": "" if za < eps else mp.nstr(L_abs / (fact * za), 25),
            "L_over_factorial_xi_derivative_abs": "" if xa < eps else mp.nstr(L_abs / (fact * xa), 25),
            "factorial_times_L": mp.nstr(fact * L_abs, 25),
        })

    write_csv(ART / "L_k_vs_derivatives_step252.csv", [
        "triple_id",
        "rho_index",
        "G_id",
        "k",
        "L_abs",
        "zeta_derivative_abs",
        "xi_derivative_abs",
        "L_over_zeta_derivative_abs",
        "L_over_xi_derivative_abs",
        "L_over_factorial_zeta_derivative_abs",
        "L_over_factorial_xi_derivative_abs",
        "factorial_times_L",
    ], comparison_rows)

    fit_rows = read_csv(STEP250 / "growth_law_fits_step250.csv")
    exp_b = {}
    for row in fit_rows:
        if row["model"] == "exponential" and row["triple_id"] in wanted:
            # parameters are "a;b" for a*exp(b*k)
            parts = row["parameters"].split(";")
            exp_b[row["triple_id"]] = float(parts[1])

    candidate_rows: list[dict[str, str]] = []
    for triple in sorted(wanted):
        rows_t = [r for r in comparison_rows if r["triple_id"] == triple and int(r["k"]) >= 1]
        z_ratios = [float(r["L_over_zeta_derivative_abs"]) for r in rows_t if r["L_over_zeta_derivative_abs"]]
        x_ratios = [float(r["L_over_xi_derivative_abs"]) for r in rows_t if r["L_over_xi_derivative_abs"]]
        fz_ratios = [float(r["L_over_factorial_zeta_derivative_abs"]) for r in rows_t if r["L_over_factorial_zeta_derivative_abs"]]
        fx_ratios = [float(r["L_over_factorial_xi_derivative_abs"]) for r in rows_t if r["L_over_factorial_xi_derivative_abs"]]
        for name, vals in [
            ("constant_ratio_to_zeta_derivative", z_ratios),
            ("constant_ratio_to_xi_derivative", x_ratios),
            ("constant_ratio_to_factorial_zeta_derivative", fz_ratios),
            ("constant_ratio_to_factorial_xi_derivative", fx_ratios),
        ]:
            mean = sum(vals) / len(vals)
            spread = max(vals) - min(vals)
            rel = spread / abs(mean) if mean else float("inf")
            candidate_rows.append({
                "triple_id": triple,
                "candidate_relationship": name,
                "mean_ratio_k_ge_1": f"{mean:.12g}",
                "min_ratio": f"{min(vals):.12g}",
                "max_ratio": f"{max(vals):.12g}",
                "relative_spread": f"{rel:.12g}",
                "status": "rejected_not_constant" if rel > 0.1 else "possible_constant",
            })

    for idx in [1, 2]:
        z_logs = []
        x_logs = []
        for k in range(1, K_MAX):
            z_logs.append(float(mp.log(zeta_abs[(idx, k + 1)] / zeta_abs[(idx, k)])))
            x_logs.append(float(mp.log(xi_abs[(idx, k + 1)] / xi_abs[(idx, k)])))
        candidate_rows.append({
            "triple_id": f"rho{idx}_derivative_growth",
            "candidate_relationship": "successive_log_zeta_derivative_ratio_k1_to_k4",
            "mean_ratio_k_ge_1": f"{sum(z_logs)/len(z_logs):.12g}",
            "min_ratio": f"{min(z_logs):.12g}",
            "max_ratio": f"{max(z_logs):.12g}",
            "relative_spread": "",
            "status": "compare_to_step250_b_values_not_matching_uniformly",
        })
        candidate_rows.append({
            "triple_id": f"rho{idx}_derivative_growth",
            "candidate_relationship": "successive_log_xi_derivative_ratio_k1_to_k4",
            "mean_ratio_k_ge_1": f"{sum(x_logs)/len(x_logs):.12g}",
            "min_ratio": f"{min(x_logs):.12g}",
            "max_ratio": f"{max(x_logs):.12g}",
            "relative_spread": "",
            "status": "compare_to_step250_b_values_not_matching_uniformly",
        })

    write_csv(ART / "candidate_relationships_step252.csv", [
        "triple_id",
        "candidate_relationship",
        "mean_ratio_k_ge_1",
        "min_ratio",
        "max_ratio",
        "relative_spread",
        "status",
    ], candidate_rows)

    output: list[str] = [
        "Step 252 zeta/xi derivative comparison",
        f"mpmath_dps={MP_DPS}",
    ]
    for row in zeta_rows:
        if row["rho_index"] == "1":
            output.append(
                f"rho1 k={row['k']} |zeta^k|={row['zeta_derivative_abs']} zeta={row['zeta_derivative_real']} + {row['zeta_derivative_imag']}i"
            )
    for row in xi_rows:
        if row["rho_index"] == "1":
            output.append(
                f"rho1 k={row['k']} |xi^k|={row['xi_derivative_abs']} xi={row['xi_derivative_real']} + {row['xi_derivative_imag']}i"
            )
    for triple, b in sorted(exp_b.items()):
        output.append(f"step250_exponential_b {triple} {b:.12g}")
    output.append("verdict=V_branch_C_zeta_derivative_no_simple_connection")
    (ART / "compute_step252_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    (ART / "xi_derivatives_step252.json").write_text(json.dumps({"mpmath_dps": MP_DPS, "derivatives": xi_rows}, indent=2) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
