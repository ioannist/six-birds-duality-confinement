#!/usr/bin/env python3
"""Step 369: per-zero Branch C local refit attempt.

The requested model needs a defect-order axis d=0..5.  The inherited Branch C
evaluator exposed in Step 292 has no defect-order argument; it computes the raw
delta proxy

    (zeta * M(G))^(k)(rho)

from zeta_derivatives(gamma, max_k, dps), mellin_derivatives(G, gamma, max_k,
dps), and delta_from_derivatives(zds, mds, k).  This script therefore computes
the supported d=0-only evaluator grid and records that A_j in

    gamma_j(d) = A_j/T_j + B_j d^beta_j

is not identifiable from the available cascade routine.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step369_per_zero_local_refit_artifacts"
STEP292_SCRIPT = ROOT / "anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py"

DPS = 80
RHO_INDICES = list(range(1, 16))
K_VALUES = [5, 10, 15, 20, 30]
REQUESTED_D_VALUES = [0, 1, 2, 3, 4, 5]
SUPPORTED_D_VALUES = [0]
G_ID = "G_star"

INHERITED_GAMMA_G_STAR = {
    1: 0.2046,
    2: 0.1379,
    3: 0.1002,
    4: 0.0819,
    5: 0.0521,
    6: 0.0738,
    7: 0.0087,
    8: 0.0353,
    9: 0.0459,
    10: 0.0461,
    11: 0.0163,
    12: 0.0012,
    13: 0.0316,
    14: 0.0236,
    15: 0.0167,
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


def cstr(z: mp.mpc, digits: int = 30) -> str:
    sign = "+" if mp.im(z) >= 0 else ""
    return f"{mp.nstr(mp.re(z), digits)}{sign}{mp.nstr(mp.im(z), digits)}j"


def fit_saddle(values: list[tuple[int, float]]) -> dict[str, float]:
    rows = []
    y = []
    for k, value in values:
        kk = float(k)
        rows.append([1.0, math.log(kk), kk, kk * math.log(kk)])
        y.append(math.log(value))
    x = np.array(rows, dtype=float)
    yy = np.array(y, dtype=float)
    beta, *_ = np.linalg.lstsq(x, yy, rcond=None)
    pred = x @ beta
    rmse = math.sqrt(float(np.mean((pred - yy) ** 2)))
    return {
        "log_A": float(beta[0]),
        "A_fit_prefactor": float(math.exp(beta[0])),
        "alpha": float(beta[1]),
        "b": float(beta[2]),
        "gamma": float(beta[3]),
        "log_RMSE": rmse,
    }


def a_predicted(T: float) -> float:
    return math.pi / math.log(T / (2.0 * math.pi))


def stats(values: list[float]) -> dict[str, float]:
    arr = np.array(values, dtype=float)
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "max": float(np.max(arr)),
        "std": float(np.std(arr)),
    }


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    step292 = load_module("step292_for_step369", STEP292_SCRIPT)
    gen = step292.GENERATORS[G_ID]
    max_k = max(K_VALUES)

    raw_rows: list[dict[str, object]] = []
    fit_rows: list[dict[str, object]] = []
    compare_rows: list[dict[str, object]] = []

    for idx in RHO_INDICES:
        rho = mp.zetazero(idx)
        T_mp = mp.im(rho)
        T = float(T_mp)
        zds = step292.zeta_derivatives(T_mp, max_k, DPS)
        mds = step292.mellin_derivatives(gen, T_mp, max_k, DPS)
        fit_values: list[tuple[int, float]] = []
        for k in K_VALUES:
            delta = step292.delta_from_derivatives(zds, mds, k)
            abs_delta = abs(delta)
            fit_values.append((k, float(abs_delta)))
            raw_rows.append(
                {
                    "rho_index": idx,
                    "rho": cstr(mp.mpc(mp.mpf("0.5"), T_mp), 34),
                    "T": mp.nstr(T_mp, 30),
                    "G_id": G_ID,
                    "defect_order_d": 0,
                    "requested_defect_orders": ";".join(str(d) for d in REQUESTED_D_VALUES),
                    "defect_order_evaluator_support": "unsupported_by_step292_no_d_argument",
                    "k": k,
                    "L_k_abs_raw_delta_proxy": mp.nstr(abs_delta, 30),
                    "L_k_complex_raw_delta_proxy": cstr(delta, 30),
                    "evaluator_routine": "step292.zeta_derivatives(gamma,max_k,dps)+step292.mellin_derivatives(G,gamma,max_k,dps)+step292.delta_from_derivatives(zds,mds,k)",
                    "dps": DPS,
                    "note": "supported d=0-only raw Branch C delta proxy; no defect-order sweep available",
                }
            )

        fit = fit_saddle(fit_values)
        ap = a_predicted(T)
        a_eff = fit["gamma"] * T
        inherited_gamma = INHERITED_GAMMA_G_STAR[idx]
        inherited_a_eff = inherited_gamma * T
        fit_rows.append(
            {
                "rho_index": idx,
                "T": f"{T:.15f}",
                "G_id": G_ID,
                "supported_defect_orders": "0",
                "requested_defect_orders": ";".join(str(d) for d in REQUESTED_D_VALUES),
                "A_j_status": "not_identifiable_no_d_variation",
                "A_j": "",
                "B_j": "",
                "beta_j": "",
                "gamma_fit_d0_only": f"{fit['gamma']:.12e}",
                "gamma_inherited_manager_log": f"{inherited_gamma:.12e}",
                "gamma_fit_minus_inherited": f"{fit['gamma'] - inherited_gamma:.12e}",
                "A_effective_gamma_fit_times_T": f"{a_eff:.12e}",
                "A_effective_inherited_gamma_times_T": f"{inherited_a_eff:.12e}",
                "A_fit_prefactor_saddle_model": f"{fit['A_fit_prefactor']:.12e}",
                "alpha_saddle_model": f"{fit['alpha']:.12e}",
                "b_saddle_model": f"{fit['b']:.12e}",
                "log_RMSE_saddle_model": f"{fit['log_RMSE']:.12e}",
                "k_values": ";".join(str(k) for k in K_VALUES),
                "fit_model": "log|L_k|=logA+alpha*log(k)+b*k+gamma*k*log(k), d=0 only",
                "identifiability_note": "requested A_j/T+B_j*d^beta_j needs multiple d values; Step292 evaluator exposes no d argument",
            }
        )
        compare_rows.append(
            {
                "rho_index": idx,
                "T": f"{T:.15f}",
                "A_pred_pi_over_log": f"{ap:.12e}",
                "A_j_status": "not_identifiable_no_d_variation",
                "A_j": "",
                "rel_err_A_j_vs_pi_over_log": "",
                "A_effective_gamma_fit_times_T": f"{a_eff:.12e}",
                "rel_err_A_effective_fit_vs_pi_over_log": f"{abs(a_eff - ap) / abs(ap):.12e}",
                "A_effective_inherited_gamma_times_T": f"{inherited_a_eff:.12e}",
                "rel_err_A_effective_inherited_vs_pi_over_log": f"{abs(inherited_a_eff - ap) / abs(ap):.12e}",
                "A_j_model_comparison_status": "blocked_no_d_sweep",
                "comparison_note": "A_j cannot be compared; d=0 saddle gamma*T is included only as closest supported diagnostic",
            }
        )

    write_csv(ART / "L_k_per_zero_per_d_step369.csv", raw_rows)
    write_csv(ART / "per_zero_fits_step369.csv", fit_rows)
    write_csv(ART / "A_j_vs_pi_over_log_step369.csv", compare_rows)

    rel_fit = [float(r["rel_err_A_effective_fit_vs_pi_over_log"]) for r in compare_rows]
    rel_inherited = [float(r["rel_err_A_effective_inherited_vs_pi_over_log"]) for r in compare_rows]
    fit_stats = stats(rel_fit)
    inherited_stats = stats(rel_inherited)

    summary = [
        "# Step 369 Results Summary",
        "",
        "Evaluator used:",
        "- `anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py`.",
        "- Routine signature used: `zeta_derivatives(gamma, max_k, dps)`, `mellin_derivatives(GENERATORS['G_star'], gamma, max_k, dps)`, `delta_from_derivatives(zds, mds, k)`.",
        "- This is the inherited raw Branch C proxy `(zeta*M(G_star))^(k)(rho)`, using the `t^{-s}` Mellin convention.",
        "",
        "Defect-order support:",
        "- Requested defect orders: `d=0..5`.",
        "- Actual evaluator support: `unsupported_by_step292_no_d_argument`.",
        "- Therefore only `d=0` raw evaluator rows were produced. The requested local model `gamma_j(d)=A_j/T_j+B_j*d^beta_j` is not identifiable per zero.",
        "",
        f"Raw coverage: `{len(raw_rows)}` rows = 15 zeros x 1 supported d x {len(K_VALUES)} k-values.",
        f"Closest supported diagnostic `A_eff = gamma_fit(d=0)*T` vs `pi/log(T/(2*pi))`: mean rel err `{fit_stats['mean']:.6g}`, median `{fit_stats['median']:.6g}`, max `{fit_stats['max']:.6g}`, std `{fit_stats['std']:.6g}`.",
        f"Inherited manager-log `gamma*T` vs `pi/log(T/(2*pi))`: mean rel err `{inherited_stats['mean']:.6g}`, median `{inherited_stats['median']:.6g}`, max `{inherited_stats['max']:.6g}`, std `{inherited_stats['std']:.6g}`.",
        "",
        "Cited inherited results:",
        "- Step 324: `gamma ~= A*T^alpha + B*d^beta` with `A=4.118`, `alpha ~= -1`, `B=-0.039`, `beta=0.409`, `RMSE=0.014`, `G_star`.",
        "- Step 366: `A_predicted(T)=pi/log(T/(2*pi))` matched the smooth Step 324 coefficient at rho_1 within 5.9%.",
        "- Step 367: per-zero `gamma_j*T_j` comparison had 34% mean relative error for `G_star`.",
        "- Step 368: first-neighbor spacing correction reduced 34% to 27%, still structurally insufficient.",
        "",
        "Verdict: the per-zero `A_j` refit cannot be performed with the current cascade evaluator because the defect-order axis is absent. The available data support only the smoothed-coefficient interpretation, not a rigorous per-zero local `A_j` confirmation.",
    ]
    (ART / "step369_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 369,
        "orientation": "attempt",
        "target": "per-zero local A_j refit over defect orders",
        "dps": DPS,
        "G_id": G_ID,
        "rho_indices": RHO_INDICES,
        "k_values": K_VALUES,
        "requested_d_values": REQUESTED_D_VALUES,
        "supported_d_values": SUPPORTED_D_VALUES,
        "defect_order_supported": False,
        "per_zero_Aj_identifiable": False,
        "raw_rows": len(raw_rows),
        "fit_rows": len(fit_rows),
        "comparison_rows": len(compare_rows),
        "evaluator": str(STEP292_SCRIPT),
        "evaluator_routines": [
            "zeta_derivatives(gamma,max_k,dps)",
            "mellin_derivatives(G,gamma,max_k,dps)",
            "delta_from_derivatives(zds,mds,k)",
        ],
        "closest_supported_Aeff_fit_rel_err_stats": fit_stats,
        "inherited_gammaT_rel_err_stats": inherited_stats,
        "final_verdict": "blocked_no_defect_order_sweep_smoothed_coefficient_only",
    }
    (ART / "step369_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")

    (ART / "nonclaim_boundary_step369.md").write_text(
        "# Step 369 Nonclaim Boundary\n\n"
        "- This step does not prove RH or Branch C closure.\n"
        "- The requested per-zero `A_j` fit is explicitly not claimed, because the available Branch C evaluator has no defect-order parameter.\n"
        "- The raw values are the inherited Step 292 raw delta proxy `(zeta*M(G_star))^(k)(rho)`, not an exact projected `L_k` with `I_k` and `R_k` corrections.\n"
        "- Comparisons using `gamma*T` are diagnostic only and do not replace the missing `d=0..5` sweep.\n",
        encoding="utf-8",
    )

    print("STEP369_COMPUTE_DONE")
    print(f"raw_rows={len(raw_rows)}")
    print("defect_order_supported=false")
    print(f"fit_rel_err_mean={fit_stats['mean']:.12e}")
    print(f"inherited_rel_err_mean={inherited_stats['mean']:.12e}")


if __name__ == "__main__":
    main()
