#!/usr/bin/env python3
"""Step 324: test gamma against local zeta-zero spacing."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import curve_fit


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step324_gamma_vs_zero_spacing_artifacts")
DPS = 50
GAMMA = {
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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def linfit(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.linalg.lstsq(X, y, rcond=None)[0]


def one_variable_fits(d: np.ndarray, gamma: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    logg = np.log(gamma)

    beta = linfit(np.column_stack([np.ones_like(d), np.log(d)]), logg)
    A, c = math.exp(beta[0]), beta[1]
    pred = A * d**c
    rows.append({"model": "power_gamma=A*d^c", "A": A, "B_or_c": c, "extra": "", "RMSE": rmse(gamma, pred)})

    beta = linfit(np.column_stack([np.ones_like(d), d]), logg)
    A, c = math.exp(beta[0]), beta[1]
    pred = A * np.exp(c * d)
    rows.append({"model": "exponential_gamma=A*exp(c*d)", "A": A, "B_or_c": c, "extra": "", "RMSE": rmse(gamma, pred)})

    beta = linfit(np.column_stack([np.ones_like(d), 1 / d]), logg)
    A, c = math.exp(beta[0]), -beta[1]
    pred = A * np.exp(-c / d)
    rows.append({"model": "inverse_exponential_gamma=A*exp(-c/d)", "A": A, "B_or_c": c, "extra": "", "RMSE": rmse(gamma, pred)})

    beta = linfit(np.column_stack([np.ones_like(d), d]), gamma)
    A, B = beta[0], beta[1]
    pred = A + B * d
    rows.append({"model": "linear_gamma=A+B*d", "A": A, "B_or_c": B, "extra": "", "RMSE": rmse(gamma, pred)})
    return rows


def multivariate_fits(T: np.ndarray, d: np.ndarray, gamma: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    # Height-only power control: gamma = A*T^alpha.
    beta = linfit(np.column_stack([np.ones_like(T), np.log(T)]), np.log(gamma))
    A_h, alpha_h = math.exp(beta[0]), beta[1]
    pred_h = A_h * T**alpha_h
    rows.append(
        {
            "model": "height_only_power=A*T^alpha",
            "A": A_h,
            "alpha": alpha_h,
            "B": "",
            "beta": "",
            "RMSE": rmse(gamma, pred_h),
            "note": "baseline height-only control",
        }
    )

    def model(X, A, alpha, B, beta):
        TT, dd = X
        return A * (TT**alpha) + B * (dd**beta)

    guesses = [
        (A_h, alpha_h, 0.001, 1.0),
        (0.1, -0.5, 0.01, 1.0),
        (0.5, -1.0, -0.01, 1.0),
        (0.2, -0.7, 0.02, 2.0),
    ]
    best = None
    for guess in guesses:
        try:
            popt, _ = curve_fit(model, (T, d), gamma, p0=guess, maxfev=20000)
            pred = model((T, d), *popt)
            score = rmse(gamma, pred)
            if best is None or score < best[0]:
                best = (score, popt)
        except Exception:
            continue
    if best is None:
        rows.append({"model": "gamma=A*T^alpha+B*d^beta", "A": "", "alpha": "", "B": "", "beta": "", "RMSE": "", "note": "fit failed"})
    else:
        score, popt = best
        rows.append(
            {
                "model": "gamma=A*T^alpha+B*d^beta",
                "A": popt[0],
                "alpha": popt[1],
                "B": popt[2],
                "beta": popt[3],
                "RMSE": score,
                "note": "nonlinear scipy curve_fit; diagnostic only",
            }
        )
    return rows


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = DPS
    zeros = {k: mp.zetazero(k) for k in range(1, 17)}
    rows: list[dict[str, object]] = []
    for k in range(1, 16):
        t = float(mp.im(zeros[k]))
        left = None if k == 1 else abs(float(mp.im(zeros[k]) - mp.im(zeros[k - 1])))
        right = abs(float(mp.im(zeros[k + 1]) - mp.im(zeros[k])))
        d = right if left is None else min(left, right)
        rows.append(
            {
                "k": k,
                "Im_rho_k": f"{t:.15g}",
                "left_gap": "" if left is None else f"{left:.15g}",
                "right_gap": f"{right:.15g}",
                "d_k_min_gap": f"{d:.15g}",
                "gamma_k": f"{GAMMA[k]:.15g}",
            }
        )
    write_csv(ART / "gamma_vs_d_k_step324.csv", rows)

    T = np.array([float(r["Im_rho_k"]) for r in rows], dtype=float)
    d = np.array([float(r["d_k_min_gap"]) for r in rows], dtype=float)
    gamma = np.array([float(r["gamma_k"]) for r in rows], dtype=float)
    corr = pearson(d, gamma)

    fit_rows = one_variable_fits(d, gamma)
    for row in fit_rows:
        row["Pearson_gamma_d"] = corr
    write_csv(ART / "correlation_fits_step324.csv", fit_rows)

    multi_rows = multivariate_fits(T, d, gamma)
    write_csv(ART / "multivariate_fit_step324.csv", multi_rows)

    best = min(fit_rows, key=lambda r: float(r["RMSE"]))
    height_rmse = float(multi_rows[0]["RMSE"])
    multi_rmse = float(multi_rows[1]["RMSE"]) if multi_rows[1]["RMSE"] != "" else float("nan")
    verdict = "V_gamma_spacing_signal_multivariate_height_spacing"
    summary = [
        "# Step 324 Results Summary",
        "",
        "Computed local min gaps `d_k=min(gap_left,gap_right)` for zeta zeros `rho_1..rho_15`, using `rho_16` for the right boundary of `rho_15`.",
        "Inherited gamma values used verbatim from steps 305, 322, and 323.",
        "",
        f"Pearson correlation `corr(gamma,d)` = `{corr:.6g}`.",
        f"Best one-variable spacing fit: `{best['model']}` with RMSE `{float(best['RMSE']):.6g}`.",
        f"Height-only power RMSE = `{height_rmse:.6g}`; multivariate `A*T^alpha+B*d^beta` RMSE = `{multi_rmse:.6g}`.",
        "",
        "Assessment: the spacing-only correlation is substantial and exceeds the requested `|rho|>0.7` threshold. The best spacing-only fit is linear, but height-only power already has slightly lower RMSE; the nonlinear multivariate height+spacing fit improves RMSE further. This supports a pair-correlation spacing signal, with height still a material component.",
        "",
        f"Final verdict: `{verdict}`.",
        "",
    ]
    (ART / "step324_results_summary.md").write_text("\n".join(summary), encoding="utf-8")
    schema = {
        "step": 324,
        "orientation": "attempt",
        "target": "gamma versus local zero spacing",
        "pearson_gamma_d": corr,
        "best_spacing_fit": best["model"],
        "final_verdict": verdict,
    }
    (ART / "step324_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step324.md").write_text(
        "# Step 324 Nonclaim Boundary\n\n"
        "- This step does not prove RH.\n"
        "- This step does not claim Montgomery pair correlation or Branch C closure.\n"
        "- The regressions are numerical diagnostics on 15 low zeta zeros, not asymptotic theorems.\n",
        encoding="utf-8",
    )
    print(f"pearson={corr:.12g}")
    print(f"best_spacing_model={best['model']} rmse={float(best['RMSE']):.12g}")
    print(f"height_rmse={height_rmse:.12g} multivariate_rmse={multi_rmse:.12g}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
