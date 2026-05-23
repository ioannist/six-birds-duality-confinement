#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np

mp.mp.dps = 80

OUT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step368_branch_C_residual_structure_artifacts")

GAMMA_G_STAR = {
    1: 0.2046, 2: 0.1379, 3: 0.1002, 4: 0.0819, 5: 0.0521,
    6: 0.0738, 7: 0.0087, 8: 0.0353, 9: 0.0459, 10: 0.0461,
    11: 0.0163, 12: 0.0012, 13: 0.0316, 14: 0.0236, 15: 0.0167,
}


def zeta_derivative(z, n):
    return mp.diff(lambda w: mp.zeta(w), z, n)


def rankdata(values):
    # Average ranks for ties.
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for m in range(i, j + 1):
            ranks[order[m]] = avg_rank
        i = j + 1
    return ranks


def pearson(xs, ys):
    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    return pearson(rankdata(xs), rankdata(ys))


def linfit(xs, ys):
    X = np.column_stack([np.ones(len(xs)), np.array(xs, dtype=float)])
    y = np.array(ys, dtype=float)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot else 0.0
    return coef, pred, r2


def rel_err(pred_Aeff, Aeff, Apred):
    # Use the Step 367 denominator convention: divide by |A_pred|.
    return abs(pred_Aeff - Aeff) / abs(Apred)


def main():
    zeros = {k: float(abs(mp.im(mp.zetazero(k)))) for k in range(1, 17)}
    rows = []
    for k in range(1, 16):
        T = zeros[k]
        gamma = GAMMA_G_STAR[k]
        A_eff = gamma * T
        A_pred = math.pi / math.log(T / (2 * math.pi))
        R = A_eff - A_pred
        fwd = zeros[k + 1] - zeros[k] if k < 15 else None
        bwd = zeros[k] - zeros[k - 1] if k > 1 else None
        if fwd is not None and bwd is not None:
            s_mean = 2 * fwd * bwd / (fwd + bwd)
            s_min = min(fwd, bwd)
            asym = fwd - bwd
        else:
            s_mean = fwd if fwd is not None else bwd
            s_min = s_mean
            asym = None

        rho = mp.zetazero(k)
        zpp = zeta_derivative(rho, 2)
        re_zpp = float(mp.re(zpp))
        eta = 1 if re_zpp > 0 else -1 if re_zpp < 0 else 0
        abs_zpp = float(abs(zpp))
        rows.append({
            "rho_index": k,
            "T": T,
            "gamma_G_star": gamma,
            "A_pred": A_pred,
            "A_eff": A_eff,
            "R": R,
            "s_fwd": fwd,
            "s_bwd": bwd,
            "s_mean": s_mean,
            "s_min": s_min,
            "spacing_asym": asym,
            "defect_order_d": 0,
            "eta_sign_Re_zeta2": eta,
            "abs_zeta2": abs_zpp,
            "m_sign_gamma": 1 if gamma > 0 else -1 if gamma < 0 else 0,
        })

    with (OUT / "residuals_and_predictors_step368.csv").open("w", newline="") as f:
        fields = [
            "rho_index", "T", "gamma_G_star", "A_pred", "A_eff", "R",
            "s_fwd", "s_bwd", "s_mean", "s_min", "spacing_asym",
            "defect_order_d", "eta_sign_Re_zeta2", "abs_zeta2", "m_sign_gamma"
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else f"{v:.15g}" if isinstance(v, float) else v) for k, v in r.items()})

    variables = ["s_fwd", "s_bwd", "s_mean", "s_min", "spacing_asym", "defect_order_d", "eta_sign_Re_zeta2", "abs_zeta2", "m_sign_gamma"]
    corr_rows = []
    fit_records = {}
    for var in variables:
        valid = [r for r in rows if r[var] is not None]
        xs = [r[var] for r in valid]
        ys = [r["R"] for r in valid]
        p = pearson(xs, ys)
        s = spearman(xs, ys)
        if p is None:
            corr_rows.append({
                "variable": var, "valid_count": len(valid), "pearson_r": "undefined_constant_or_too_few",
                "spearman_rho": "undefined_constant_or_too_few", "alpha": "", "beta": "", "R2": "",
                "mean_rel_err_after_correction": "",
            })
            continue
        coef, pred_R, r2 = linfit(xs, ys)
        errs = []
        for rr, pr in zip(valid, pred_R):
            pred_Aeff = rr["A_pred"] + float(pr)
            errs.append(rel_err(pred_Aeff, rr["A_eff"], rr["A_pred"]))
        mean_err = float(np.mean(errs))
        fit_records[var] = (mean_err, valid, coef, pred_R, r2)
        corr_rows.append({
            "variable": var,
            "valid_count": len(valid),
            "pearson_r": f"{p:.15g}",
            "spearman_rho": f"{s:.15g}",
            "alpha": f"{coef[0]:.15g}",
            "beta": f"{coef[1]:.15g}",
            "R2": f"{r2:.15g}",
            "mean_rel_err_after_correction": f"{mean_err:.15g}",
        })

    with (OUT / "correlations_step368.csv").open("w", newline="") as f:
        fields = ["variable", "valid_count", "pearson_r", "spearman_rho", "alpha", "beta", "R2", "mean_rel_err_after_correction"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(corr_rows)

    # Best single by mean error among nonconstant variables.
    best_single_var = min(fit_records, key=lambda v: fit_records[v][0])
    best_single = fit_records[best_single_var]

    # Two-variable search.
    pair_records = {}
    nonconstant_vars = list(fit_records.keys())
    for i, v1 in enumerate(nonconstant_vars):
        for v2 in nonconstant_vars[i + 1:]:
            valid = [r for r in rows if r[v1] is not None and r[v2] is not None]
            if len(valid) < 5:
                continue
            X = np.column_stack([
                np.ones(len(valid)),
                np.array([r[v1] for r in valid], dtype=float),
                np.array([r[v2] for r in valid], dtype=float),
            ])
            y = np.array([r["R"] for r in valid], dtype=float)
            if np.linalg.matrix_rank(X) < 3:
                continue
            coef, *_ = np.linalg.lstsq(X, y, rcond=None)
            pred = X @ coef
            errs = [rel_err(r["A_pred"] + float(pr), r["A_eff"], r["A_pred"]) for r, pr in zip(valid, pred)]
            ymean = np.mean(y)
            ss_res = float(np.sum((y - pred) ** 2))
            ss_tot = float(np.sum((y - ymean) ** 2))
            r2 = 1.0 - ss_res / ss_tot if ss_tot else 0.0
            pair_records[(v1, v2)] = (float(np.mean(errs)), valid, coef, r2)

    best_pair_vars = min(pair_records, key=lambda p: pair_records[p][0])
    best_pair = pair_records[best_pair_vars]

    baseline_err = float(np.mean([abs(r["A_pred"] - r["A_eff"]) / abs(r["A_pred"]) for r in rows]))

    rows_out = [
        {
            "fit_type": "baseline_no_correction",
            "variables": "none",
            "valid_count": len(rows),
            "formula": "A_eff ~= A_pred",
            "coefficients": "",
            "R2": "",
            "mean_rel_err": f"{baseline_err:.15g}",
        },
        {
            "fit_type": "best_single",
            "variables": best_single_var,
            "valid_count": len(best_single[1]),
            "formula": f"A_eff ~= A_pred + alpha + beta*{best_single_var}",
            "coefficients": f"alpha={best_single[2][0]:.15g}; beta={best_single[2][1]:.15g}",
            "R2": f"{best_single[4]:.15g}",
            "mean_rel_err": f"{best_single[0]:.15g}",
        },
        {
            "fit_type": "best_pair",
            "variables": f"{best_pair_vars[0]} + {best_pair_vars[1]}",
            "valid_count": len(best_pair[1]),
            "formula": f"A_eff ~= A_pred + a + b*{best_pair_vars[0]} + c*{best_pair_vars[1]}",
            "coefficients": f"a={best_pair[2][0]:.15g}; b={best_pair[2][1]:.15g}; c={best_pair[2][2]:.15g}",
            "R2": f"{best_pair[3]:.15g}",
            "mean_rel_err": f"{best_pair[0]:.15g}",
        },
    ]
    with (OUT / "best_fit_corrections_step368.csv").open("w", newline="") as f:
        fields = ["fit_type", "variables", "valid_count", "formula", "coefficients", "R2", "mean_rel_err"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows_out)

    schema = {
        "step": 368,
        "orientation": "Branch C residual structure",
        "mpmath_dps": 80,
        "baseline_mean_rel_err": baseline_err,
        "best_single_variable": best_single_var,
        "best_single_mean_rel_err": best_single[0],
        "best_pair_variables": list(best_pair_vars),
        "best_pair_mean_rel_err": best_pair[0],
        "final_verdict": "partial_improvement_residual_remains_structurally_complex",
    }
    (OUT / "step368_schema.json").write_text(json.dumps(schema, indent=2) + "\n")


if __name__ == "__main__":
    main()
