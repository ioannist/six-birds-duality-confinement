#!/usr/bin/env python3
"""Step 383: extended close-pair law validation over first 100 zeta zeros."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step383_extended_close_pair_validation_artifacts")
STEP292 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py")
DPS = 80
FIT_K = [5, 10, 15, 20, 30]
N = 100
WORKERS = int(os.environ.get("STEP383_WORKERS", "4"))

_STEP292_MOD: Any = None
_GEN: Any = None


def init_worker() -> None:
    global _STEP292_MOD, _GEN
    spec = importlib.util.spec_from_file_location("step292_for_step383_worker", STEP292)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {STEP292}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    _STEP292_MOD = mod
    _GEN = mod.GENERATORS["G_star"]


def fit_gamma(values: dict[int, mp.mpf]) -> tuple[dict[str, mp.mpf], mp.mpf]:
    # Step 323/324 saddle form:
    # log|delta_Dk| = log A + alpha log k + b k + gamma k log k.
    X = mp.matrix(len(FIT_K), 4)
    y = mp.matrix(len(FIT_K), 1)
    for i, k in enumerate(FIT_K):
        kk = mp.mpf(k)
        X[i, 0] = 1
        X[i, 1] = mp.log(kk)
        X[i, 2] = kk
        X[i, 3] = kk * mp.log(kk)
        y[i] = mp.log(values[k])
    beta = mp.lu_solve(X.T * X, X.T * y)
    residuals = X * beta - y
    rmse = mp.sqrt(mp.fsum([residuals[i] ** 2 for i in range(len(FIT_K))]) / len(FIT_K))
    return {"A": mp.e ** beta[0], "alpha": beta[1], "b": beta[2], "gamma": beta[3]}, rmse


def compute_one(args: tuple[int, str, str]) -> dict[str, object]:
    if _STEP292_MOD is None:
        init_worker()
    j, T_str, s_min_str = args
    mp.mp.dps = DPS
    T = mp.mpf(T_str)
    s_min = mp.mpf(s_min_str)
    zds = _STEP292_MOD.zeta_derivatives(T, max(FIT_K), DPS)
    mds = _STEP292_MOD.mellin_derivatives(_GEN, T, max(FIT_K), DPS)
    vals = {k: abs(_STEP292_MOD.delta_from_derivatives(zds, mds, k)) for k in FIT_K}
    params, fit_rmse = fit_gamma(vals)
    gamma = params["gamma"]
    A_pred = mp.pi / mp.log(T / (2 * mp.pi))
    R = gamma * T - A_pred
    row: dict[str, object] = {
        "j": j,
        "T": mp.nstr(T, 30),
        "s_min": mp.nstr(s_min, 30),
        "inv_s_min": mp.nstr(1 / s_min, 30),
        "gamma_zeta_G_star": mp.nstr(gamma, 30),
        "A_pred_pi_over_log": mp.nstr(A_pred, 30),
        "R_gamma_T_minus_A_pred": mp.nstr(R, 30),
        "abs_R": mp.nstr(abs(R), 30),
        "fit_log_RMSE": mp.nstr(fit_rmse, 30),
        "fit_model": "log|delta_Dk|=logA+alpha*log(k)+b*k+gamma*k*log(k)",
        "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho)",
    }
    for k in FIT_K:
        row[f"k{k}_abs_delta_proxy"] = mp.nstr(vals[k], 30)
    return row


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, object]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def fit_ols(y: np.ndarray, cols: list[np.ndarray], names: list[str], model_name: str) -> dict[str, object]:
    X = np.column_stack([np.ones_like(y)] + cols)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    resid = y - pred
    n, p = X.shape
    rmse = float(np.sqrt(np.mean(resid**2)))
    sse = float(np.sum(resid**2))
    sigma2 = sse / max(n - p, 1)
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    tstats = beta / se
    pvals = ["p_not_computed"] * len(beta)
    try:
        from scipy import stats  # type: ignore

        pvals = [f"{2 * stats.t.sf(abs(float(t)), n - p):.17e}" for t in tstats]
    except Exception:
        pass
    out: dict[str, object] = {
        "model": model_name,
        "n": n,
        "RMSE": rmse,
        "intercept_a": beta[0],
        "intercept_se": se[0],
        "intercept_t": tstats[0],
        "intercept_p": pvals[0],
    }
    for idx, name in enumerate(names, start=1):
        out[f"{name}_coef"] = beta[idx]
        out[f"{name}_se"] = se[idx]
        out[f"{name}_t"] = tstats[idx]
        out[f"{name}_p"] = pvals[idx]
    if "inv_s" in names:
        b = beta[names.index("inv_s") + 1]
        out["slope_b_inv_s"] = b
        out["slope_rel_err_vs_pi2"] = abs(b - math.pi**2) / math.pi**2
    if len(names) == 1 and names[0] == "inv_s":
        out["pearson_r"] = float(np.corrcoef(cols[0], y)[0, 1])
        out["offset_rel_err_vs_minus_3pi_over_2"] = abs(beta[0] - (-3 * math.pi / 2)) / abs(-3 * math.pi / 2)
    return out


def main() -> None:
    mp.mp.dps = DPS
    BASE.mkdir(parents=True, exist_ok=True)

    zeros = {j: mp.zetazero(j) for j in range(1, N + 2)}
    tasks: list[tuple[int, str, str]] = []
    for j in range(1, N + 1):
        T = mp.im(zeros[j])
        s_fwd = mp.im(zeros[j + 1]) - T
        s_bwd = T - mp.im(zeros[j - 1]) if j > 1 else s_fwd
        s_min = min(s_fwd, s_bwd)
        tasks.append((j, mp.nstr(T, 80), mp.nstr(s_min, 80)))

    table_path = BASE / "gamma_R_table_100_zeros_step383.csv"
    if table_path.exists():
        existing = read_csv(table_path)
        if len(existing) == N:
            results = existing
            print(f"loaded existing {N}-row gamma table", flush=True)
        else:
            results = []
    else:
        results = []

    if not results:
        with ProcessPoolExecutor(max_workers=WORKERS, initializer=init_worker) as pool:
            futs = {pool.submit(compute_one, task): task[0] for task in tasks}
            for fut in as_completed(futs):
                row = fut.result()
                results.append(row)
                print(f"computed {len(results)}/{N}: j={row['j']}", flush=True)

        results.sort(key=lambda r: int(r["j"]))
        write_csv(table_path, results)

    inv_s = np.array([float(r["inv_s_min"]) for r in results], dtype=float)
    T_arr = np.array([float(r["T"]) for r in results], dtype=float)
    y = np.array([float(r["R_gamma_T_minus_A_pred"]) for r in results], dtype=float)

    fit_rows = [
        fit_ols(y, [inv_s], ["inv_s"], "R=a+b/s_min"),
        fit_ols(y, [inv_s, inv_s**2], ["inv_s", "inv_s2"], "R=a+b/s_min+c/s_min^2"),
        fit_ols(y, [inv_s, 1 / T_arr], ["inv_s", "inv_T"], "R=a+b/s_min+d/T"),
    ]
    write_csv(BASE / "fits_step383.csv", fit_rows)

    main_fit = fit_rows[0]
    quad_fit = fit_rows[1]
    height_fit = fit_rows[2]
    slope_rel = float(main_fit["slope_rel_err_vs_pi2"])
    offset_rel = float(main_fit["offset_rel_err_vs_minus_3pi_over_2"])
    if slope_rel < 0.01 and offset_rel < 0.01:
        verdict = "theorem_confidence_empirical_validation"
    elif slope_rel < 0.03 and offset_rel < 0.05:
        verdict = "stable_3_percent_slope_5_percent_offset"
    elif float(quad_fit.get("inv_s2_p", "1") if quad_fit.get("inv_s2_p", "p_not_computed") != "p_not_computed" else "1") < 0.05 or float(height_fit.get("inv_T_p", "1") if height_fit.get("inv_T_p", "p_not_computed") != "p_not_computed" else "1") < 0.05:
        verdict = "higher_order_refinement_direction"
    else:
        verdict = "slope_or_offset_drift_reformulate"

    summary = f"""# Step 383 Results Summary

Computed Branch C `G_star` gamma for `n={len(results)}` zeros with the Step 292 raw proxy:

`delta_Dk=(zeta*M(G_star))^(k)(rho_j)`,

fitted on `k={FIT_K}` using the Step 324 saddle form

`log|delta_Dk| = logA + alpha log(k) + b k + gamma k log(k)`.

Main fit:

- model: `R=a+b/s_min`
- `a={float(main_fit['intercept_a']):.17e}`
- `b={float(main_fit['slope_b_inv_s']):.17e}`
- Pearson `r={float(main_fit['pearson_r']):.17e}`
- RMSE `{float(main_fit['RMSE']):.17e}`
- rel err `b` vs `pi^2`: `{slope_rel:.17e}`
- rel err `a` vs `-3pi/2`: `{offset_rel:.17e}`

Higher-order fits:

- `R=a+b/s+c/s^2`: RMSE `{float(quad_fit['RMSE']):.17e}`, `c={float(quad_fit['inv_s2_coef']):.17e}`, `p={quad_fit.get('inv_s2_p')}`
- `R=a+b/s+d/T`: RMSE `{float(height_fit['RMSE']):.17e}`, `d={float(height_fit['inv_T_coef']):.17e}`, `p={height_fit.get('inv_T_p')}`

Verdict: `{verdict}`.
"""
    (BASE / "step383_results_summary.md").write_text(summary)

    schema = {
        "step": 383,
        "mode": "ATTEMPT",
        "dps": DPS,
        "n_computed": len(results),
        "workers": WORKERS,
        "evaluator": "Step292 raw delta_Dk=(zeta*M(G_star))^(k)(rho)",
        "fit_k": FIT_K,
        "main_fit_a": float(main_fit["intercept_a"]),
        "main_fit_b": float(main_fit["slope_b_inv_s"]),
        "main_fit_pearson_r": float(main_fit["pearson_r"]),
        "main_fit_rmse": float(main_fit["RMSE"]),
        "slope_rel_err_vs_pi2": slope_rel,
        "offset_rel_err_vs_minus_3pi_over_2": offset_rel,
        "quadratic_rmse": float(quad_fit["RMSE"]),
        "height_rmse": float(height_fit["RMSE"]),
        "verdict": verdict,
    }
    (BASE / "step383_schema.json").write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")

    boundary = """# Step 383 Nonclaim Boundary

- This step does not prove RH or a Branch C theorem.
- The evaluator is the Step 292 raw delta proxy, not the fully projected Burnol/Sonine residual.
- The `n=100` fit tests empirical stability of the Step 382 constants only.
- Higher-order p-values, when available, are diagnostic and not proof of a correction law.
"""
    (BASE / "nonclaim_boundary_step383.md").write_text(boundary)

    print("STEP383_COMPUTE_DONE")
    print(f"n={len(results)} a={main_fit['intercept_a']:.12g} b={main_fit['slope_b_inv_s']:.12g} r={main_fit['pearson_r']:.12g}")
    print(f"slope_rel={slope_rel:.12g} offset_rel={offset_rel:.12g}")
    print(f"quad_rmse={quad_fit['RMSE']:.12g} height_rmse={height_fit['RMSE']:.12g} verdict={verdict}")


if __name__ == "__main__":
    main()
