#!/usr/bin/env python3
"""Step 332: extend G_prime gamma fit to zeta zeros rho_1..rho_15."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import curve_fit


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step332_G_prime_full_height_fit_artifacts"
STEP292_SCRIPT = ROOT / "anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py"
STEP331_GAMMA = ROOT / "anti_loc/thread/steps/step331_G_prime_gamma_fit_artifacts/gamma_per_rho_G_prime_step331.csv"
STEP324_GSTAR = ROOT / "anti_loc/thread/steps/step324_gamma_vs_zero_spacing_artifacts/gamma_vs_d_k_step324.csv"
DPS = 80
K_VALUES = [5, 10, 15, 20, 30]
RHO_COMPUTE = list(range(6, 16))
D_GAPS = {
    1: 6.88731449703686,
    2: 3.98881794137413,
    3: 3.98881794137413,
    4: 2.51018546187968,
    5: 2.51018546187968,
    6: 3.33254085332182,
    7: 2.40835426876750,
    8: 2.40835426876750,
    9: 1.76868159650514,
    10: 1.76868159650514,
    11: 3.19648900004216,
    12: 2.90079630553896,
    13: 1.48473452200746,
    14: 1.48473452200746,
    15: 1.96726648141257,
}
G_STAR_FIT = {"A": 4.118419256684808, "alpha": -0.996854915495847, "B": -0.039179497004447894, "beta": 0.4086679154653991, "RMSE": 0.014046213677353668}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fit_saddle(values: list[tuple[int, float]]) -> dict[str, float]:
    X = []
    Y = []
    for k, val in values:
        X.append([1.0, math.log(k), float(k), float(k) * math.log(k)])
        Y.append(math.log(val))
    Xn = np.array(X, dtype=float)
    Yn = np.array(Y, dtype=float)
    beta, *_ = np.linalg.lstsq(Xn, Yn, rcond=None)
    pred = Xn @ beta
    rmse = math.sqrt(float(np.mean((pred - Yn) ** 2)))
    return {
        "A_per_rho": float(math.exp(beta[0])),
        "alpha_per_rho": float(beta[1]),
        "b_per_rho": float(beta[2]),
        "gamma": float(beta[3]),
        "log_RMSE": rmse,
    }


def fit_multivariate(rows: list[dict[str, object]]) -> dict[str, float]:
    T = np.array([float(r["Im_rho"]) for r in rows], dtype=float)
    d = np.array([float(r["d_min_gap"]) for r in rows], dtype=float)
    gamma = np.array([float(r["gamma_G_prime"]) for r in rows], dtype=float)

    def model(xdata, A, alpha, B, beta):
        T_, d_ = xdata
        return A * (T_ ** alpha) + B * (d_ ** beta)

    popt, _ = curve_fit(model, (T, d), gamma, p0=[5.0, -1.0, -0.04, 0.4], maxfev=200000)
    pred = model((T, d), *popt)
    rmse = math.sqrt(float(np.mean((pred - gamma) ** 2)))
    return {"A": float(popt[0]), "alpha": float(popt[1]), "B": float(popt[2]), "beta": float(popt[3]), "RMSE": rmse}


def pearson(xs: list[float], ys: list[float]) -> float:
    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    return float(np.corrcoef(x, y)[0, 1])


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step292 = load_module("step292_for_step332", STEP292_SCRIPT)
    gen = step292.GENERATORS["G_prime"]
    max_k = max(K_VALUES)

    inherited_rows = []
    for row in read_csv(STEP331_GAMMA):
        idx = int(row["rho_index"])
        inherited_rows.append(
            {
                "source": "inherited_step331",
                "rho_index": idx,
                "Im_rho": row["Im_rho"],
                "d_min_gap": row["d_min_gap"],
                "A_per_rho": row["A_per_rho"],
                "alpha_per_rho": row["alpha_per_rho"],
                "b_per_rho": row["b_per_rho"],
                "gamma_G_prime": row["gamma"],
                "log_RMSE": row["log_RMSE"],
                "k_values": row["k_values"],
            }
        )

    computed_rows: list[dict[str, object]] = []
    for idx in RHO_COMPUTE:
        gamma_t = mp.im(mp.zetazero(idx))
        zds = step292.zeta_derivatives(gamma_t, max_k, DPS)
        mds = step292.mellin_derivatives(gen, gamma_t, max_k, DPS)
        fit_values: list[tuple[int, float]] = []
        for k in K_VALUES:
            delta = step292.delta_from_derivatives(zds, mds, k)
            fit_values.append((k, float(abs(delta))))
        fit = fit_saddle(fit_values)
        computed_rows.append(
            {
                "source": "computed_step332",
                "rho_index": idx,
                "Im_rho": mp.nstr(gamma_t, 24),
                "d_min_gap": f"{D_GAPS[idx]:.14f}",
                "A_per_rho": f"{fit['A_per_rho']:.12e}",
                "alpha_per_rho": f"{fit['alpha_per_rho']:.12e}",
                "b_per_rho": f"{fit['b_per_rho']:.12e}",
                "gamma_G_prime": f"{fit['gamma']:.12e}",
                "log_RMSE": f"{fit['log_RMSE']:.12e}",
                "k_values": ";".join(str(k) for k in K_VALUES),
            }
        )

    all_rows = sorted(inherited_rows + computed_rows, key=lambda r: int(r["rho_index"]))
    multi = fit_multivariate(all_rows)

    gstar_rows = read_csv(STEP324_GSTAR)
    star_by_idx = {int(r["k"]): float(r["gamma_k"]) for r in gstar_rows}
    gp_by_idx = {int(r["rho_index"]): float(r["gamma_G_prime"]) for r in all_rows}
    star_vals = [star_by_idx[i] for i in range(1, 16)]
    prime_vals = [gp_by_idx[i] for i in range(1, 16)]
    corr = pearson(star_vals, prime_vals)

    cross_rows = []
    for idx in range(1, 16):
        cross_rows.append(
            {
                "rho_index": idx,
                "T": next(r["Im_rho"] for r in all_rows if int(r["rho_index"]) == idx),
                "d_min_gap": f"{D_GAPS[idx]:.14f}",
                "gamma_G_star": f"{star_by_idx[idx]:.12e}",
                "gamma_G_prime": f"{gp_by_idx[idx]:.12e}",
                "gamma_prime_minus_star": f"{gp_by_idx[idx] - star_by_idx[idx]:.12e}",
                "gamma_prime_over_star": f"{(gp_by_idx[idx] / star_by_idx[idx] if star_by_idx[idx] else float('nan')):.12e}",
                "A": "",
                "alpha": "",
                "B": "",
                "beta": "",
                "RMSE": "",
                "pearson_gamma_star_prime": "",
            }
        )
    cross_rows.extend(
        [
            {
                "rho_index": "FIT_G_star",
                "T": "",
                "d_min_gap": "",
                "gamma_G_star": "",
                "gamma_G_prime": "",
                "gamma_prime_minus_star": "",
                "gamma_prime_over_star": "",
                "A": f"{G_STAR_FIT['A']:.12e}",
                "alpha": f"{G_STAR_FIT['alpha']:.12e}",
                "B": f"{G_STAR_FIT['B']:.12e}",
                "beta": f"{G_STAR_FIT['beta']:.12e}",
                "RMSE": f"{G_STAR_FIT['RMSE']:.12e}",
                "pearson_gamma_star_prime": f"{corr:.12e}",
            },
            {
                "rho_index": "FIT_G_prime",
                "T": "",
                "d_min_gap": "",
                "gamma_G_star": "",
                "gamma_G_prime": "",
                "gamma_prime_minus_star": "",
                "gamma_prime_over_star": "",
                "A": f"{multi['A']:.12e}",
                "alpha": f"{multi['alpha']:.12e}",
                "B": f"{multi['B']:.12e}",
                "beta": f"{multi['beta']:.12e}",
                "RMSE": f"{multi['RMSE']:.12e}",
                "pearson_gamma_star_prime": f"{corr:.12e}",
            },
        ]
    )

    multi_rows = [
        {
            "G_id": "G_prime",
            "model": "gamma=A*T^alpha+B*d^beta",
            "A": f"{multi['A']:.12e}",
            "alpha": f"{multi['alpha']:.12e}",
            "B": f"{multi['B']:.12e}",
            "beta": f"{multi['beta']:.12e}",
            "RMSE": f"{multi['RMSE']:.12e}",
            "n_points": len(all_rows),
        }
    ]

    write_csv(ART / "gamma_G_prime_all_zeros_step332.csv", all_rows)
    write_csv(ART / "multivariate_fit_G_prime_15_step332.csv", multi_rows)
    write_csv(ART / "cross_G_universality_step332.csv", cross_rows)

    a_ratio = multi["A"] / G_STAR_FIT["A"]
    alpha_close = abs(multi["alpha"] - G_STAR_FIT["alpha"])
    verdict = "A_roughly_universal_scale_4_to_5" if abs(a_ratio - 1) <= 0.3 and alpha_close <= 0.3 else "A_test_function_dependent"
    summary = [
        "# Step 332 Results Summary",
        "",
        "Inherited citations:",
        "- Step 323 supplied the 15-point `G_star` gamma-vs-height data for zeta zeros.",
        "- Step 324 fit `G_star` with `A=4.118`, `alpha=-0.997`, `B=-0.039`, `beta=0.409`, `RMSE=0.014`.",
        "- Step 331 fit `G_prime` on rho_1..rho_5 with `A=5.155`, `alpha=-1.126`; this step extends to rho_15.",
        "",
        "New `G_prime` gamma values for rho_6..rho_15:",
    ]
    for row in computed_rows:
        summary.append(f"- `rho_{row['rho_index']}` T=`{row['Im_rho']}` gamma=`{row['gamma_G_prime']}`.")
    summary.extend(
        [
            "",
            f"15-point `G_prime` fit: A=`{multi['A']:.6g}`, alpha=`{multi['alpha']:.6g}`, B=`{multi['B']:.6g}`, beta=`{multi['beta']:.6g}`, RMSE=`{multi['RMSE']:.6g}`.",
            f"Cross-G Pearson correlation gamma_G_star vs gamma_G_prime: `{corr:.6g}`.",
            f"A ratio G_prime/G_star: `{a_ratio:.6g}`.",
            f"Verdict: `{verdict}`.",
        ]
    )
    (ART / "step332_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    schema = {
        "step": 332,
        "orientation": "attempt",
        "target": "G_prime 15-point gamma height/spacing fit",
        "dps": DPS,
        "computed_rho_indices": RHO_COMPUTE,
        "A_G_star_step324": G_STAR_FIT["A"],
        "A_G_prime_step332": multi["A"],
        "A_ratio_G_prime_over_G_star": a_ratio,
        "pearson_gamma_star_prime": corr,
        "final_verdict": verdict,
    }
    (ART / "step332_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step332.md").write_text(
        "# Step 332 Nonclaim Boundary\n\n"
        "- This step computes Branch C raw delta-proxy fits only.\n"
        "- It does not prove RH or close Branch C.\n"
        "- The multivariate fit is a diagnostic finite-data model, not a theorem.\n",
        encoding="utf-8",
    )
    print("STEP332_COMPUTE_DONE")
    print(f"A_G_prime={multi['A']:.12e}")
    print(f"alpha_G_prime={multi['alpha']:.12e}")
    print(f"pearson={corr:.12e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
