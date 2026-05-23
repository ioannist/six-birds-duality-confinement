#!/usr/bin/env python3
"""Step 331: fit gamma(T,d) for G_prime over zeta zeros rho_1..rho_5."""

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
ART = ROOT / "anti_loc/thread/steps/step331_G_prime_gamma_fit_artifacts"
STEP292_SCRIPT = ROOT / "anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py"
DPS = 80
K_VALUES = [5, 10, 15, 20, 30]
RHO_INDICES = [1, 2, 3, 4, 5]
D_GAPS = {
    1: 6.88731449703686,
    2: 3.98881794137413,
    3: 3.98881794137413,
    4: 2.51018546187968,
    5: 2.51018546187968,
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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cstr(z: mp.mpc, digits: int = 28) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def fit_saddle(values: list[tuple[int, float]]) -> dict[str, float]:
    x = []
    y = []
    for k, val in values:
        x.append([1.0, math.log(k), float(k), float(k) * math.log(k)])
        y.append(math.log(val))
    X = np.array(x, dtype=float)
    Y = np.array(y, dtype=float)
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    pred = X @ beta
    rmse = math.sqrt(float(np.mean((pred - Y) ** 2)))
    return {
        "log_A": float(beta[0]),
        "A": float(math.exp(beta[0])),
        "alpha": float(beta[1]),
        "b": float(beta[2]),
        "gamma": float(beta[3]),
        "log_RMSE": rmse,
    }


def fit_multivariate(gamma_rows: list[dict[str, object]]) -> dict[str, float]:
    T = np.array([float(r["Im_rho"]) for r in gamma_rows], dtype=float)
    d = np.array([float(r["d_min_gap"]) for r in gamma_rows], dtype=float)
    gamma = np.array([float(r["gamma"]) for r in gamma_rows], dtype=float)

    def model(xdata, A, alpha, B, beta):
        T_, d_ = xdata
        return A * (T_ ** alpha) + B * (d_ ** beta)

    popt, _ = curve_fit(
        model,
        (T, d),
        gamma,
        p0=[4.0, -1.0, -0.04, 0.4],
        maxfev=100000,
    )
    pred = model((T, d), *popt)
    rmse = math.sqrt(float(np.mean((pred - gamma) ** 2)))
    return {
        "A": float(popt[0]),
        "alpha": float(popt[1]),
        "B": float(popt[2]),
        "beta": float(popt[3]),
        "RMSE": rmse,
    }


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step292 = load_module("step292_for_step331", STEP292_SCRIPT)
    gen = step292.GENERATORS["G_prime"]
    max_k = max(K_VALUES)

    l_rows: list[dict[str, object]] = []
    gamma_rows: list[dict[str, object]] = []

    for idx in RHO_INDICES:
        gamma_t = mp.im(mp.zetazero(idx))
        zds = step292.zeta_derivatives(gamma_t, max_k, DPS)
        mds = step292.mellin_derivatives(gen, gamma_t, max_k, DPS)
        fit_values: list[tuple[int, float]] = []
        for k in K_VALUES:
            delta = step292.delta_from_derivatives(zds, mds, k)
            abs_delta = abs(delta)
            fit_values.append((k, float(abs_delta)))
            l_rows.append(
                {
                    "rho_index": idx,
                    "rho": cstr(mp.mpc(mp.mpf("0.5"), gamma_t), 30),
                    "Im_rho": mp.nstr(gamma_t, 24),
                    "G_id": "G_prime",
                    "k": k,
                    "L_k_abs_raw_delta_proxy": mp.nstr(abs_delta, 24),
                    "L_k_complex_raw_delta_proxy": cstr(delta, 24),
                    "dps": DPS,
                    "note": "raw delta proxy (zeta*M(G_prime))^(k)(rho), Step331 naming follows inherited Branch C convention",
                }
            )
        fit = fit_saddle(fit_values)
        gamma_rows.append(
            {
                "rho_index": idx,
                "Im_rho": mp.nstr(gamma_t, 24),
                "d_min_gap": f"{D_GAPS[idx]:.14f}",
                "A_per_rho": f"{fit['A']:.12e}",
                "alpha_per_rho": f"{fit['alpha']:.12e}",
                "b_per_rho": f"{fit['b']:.12e}",
                "gamma": f"{fit['gamma']:.12e}",
                "log_RMSE": f"{fit['log_RMSE']:.12e}",
                "k_values": ";".join(str(k) for k in K_VALUES),
            }
        )

    multi = fit_multivariate(gamma_rows)
    multi_rows = [
        {
            "G_id": "G_prime",
            "model": "gamma=A*T^alpha+B*d^beta",
            "A": f"{multi['A']:.12e}",
            "alpha": f"{multi['alpha']:.12e}",
            "B": f"{multi['B']:.12e}",
            "beta": f"{multi['beta']:.12e}",
            "RMSE": f"{multi['RMSE']:.12e}",
            "n_points": len(gamma_rows),
        }
    ]
    ratio = multi["A"] / G_STAR_FIT["A"] if G_STAR_FIT["A"] else float("nan")
    comp_rows = [
        {
            "G_id": "G_star",
            "A": f"{G_STAR_FIT['A']:.12e}",
            "alpha": f"{G_STAR_FIT['alpha']:.12e}",
            "B": f"{G_STAR_FIT['B']:.12e}",
            "beta": f"{G_STAR_FIT['beta']:.12e}",
            "RMSE": f"{G_STAR_FIT['RMSE']:.12e}",
            "source": "step324",
        },
        {
            "G_id": "G_prime",
            "A": f"{multi['A']:.12e}",
            "alpha": f"{multi['alpha']:.12e}",
            "B": f"{multi['B']:.12e}",
            "beta": f"{multi['beta']:.12e}",
            "RMSE": f"{multi['RMSE']:.12e}",
            "source": "step331",
        },
        {
            "G_id": "ratio_G_prime_over_G_star",
            "A": f"{ratio:.12e}",
            "alpha": "",
            "B": "",
            "beta": "",
            "RMSE": "",
            "source": "derived",
        },
    ]

    write_csv(ART / "L_k_G_prime_step331.csv", l_rows)
    write_csv(ART / "gamma_per_rho_G_prime_step331.csv", gamma_rows)
    write_csv(ART / "multivariate_fit_G_prime_step331.csv", multi_rows)
    write_csv(ART / "comparison_G_star_vs_G_prime_step331.csv", comp_rows)

    assessment = "A_test_function_dependent" if abs(ratio - 1.0) > 0.3 else "A_roughly_universal_across_test_functions"
    summary_lines = [
        "# Step 331 Results Summary",
        "",
        "Inherited citations:",
        "- Step 305: `(zeta*M(G))^(k)(rho)` values for `rho_1,G_prime` gave `gamma = 0.2545` as a single instance.",
        "- Step 324: `G_star` multivariate fit had `A_G_star = 4.118`, `alpha = -0.997`, `B = -0.039`, `beta = 0.409`, `RMSE = 0.014`.",
        "",
        "Computed `G_prime` gamma values:",
    ]
    for row in gamma_rows:
        summary_lines.append(f"- `rho_{row['rho_index']}` T=`{row['Im_rho']}` gamma=`{row['gamma']}`.")
    summary_lines.extend(
        [
            "",
            f"Multivariate `G_prime` fit: A=`{multi['A']:.6g}`, alpha=`{multi['alpha']:.6g}`, B=`{multi['B']:.6g}`, beta=`{multi['beta']:.6g}`, RMSE=`{multi['RMSE']:.6g}`.",
            f"Comparison: A_G_prime/A_G_star = `{ratio:.6g}`.",
            f"Verdict: `{assessment}`.",
        ]
    )
    (ART / "step331_results_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    schema = {
        "step": 331,
        "orientation": "attempt",
        "target": "G_prime gamma-vs-height/spacing fit over zeta rho_1..rho_5",
        "dps": DPS,
        "k_values": K_VALUES,
        "rho_indices": RHO_INDICES,
        "A_G_star_step324": G_STAR_FIT["A"],
        "A_G_prime_step331": multi["A"],
        "A_ratio_G_prime_over_G_star": ratio,
        "final_verdict": assessment,
    }
    (ART / "step331_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step331.md").write_text(
        "# Step 331 Nonclaim Boundary\n\n"
        "- This step computes Branch C raw delta-proxy values and fit parameters only.\n"
        "- It does not prove RH or close Branch C.\n"
        "- The 5-point, 4-parameter multivariate fit is diagnostic and should not be treated as a theorem.\n",
        encoding="utf-8",
    )
    print("STEP331_COMPUTE_DONE")
    print(f"A_G_prime={multi['A']:.12e}")
    print(f"A_ratio={ratio:.12e}")
    print(f"verdict={assessment}")


if __name__ == "__main__":
    main()
