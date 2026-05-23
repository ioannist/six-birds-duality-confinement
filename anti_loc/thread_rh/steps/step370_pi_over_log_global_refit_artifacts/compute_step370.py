#!/usr/bin/env python3
"""Step 370: global validation of the pi/log structural height term."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step370_pi_over_log_global_refit_artifacts"
DATA = ROOT / "anti_loc/thread/steps/step324_gamma_vs_zero_spacing_artifacts/gamma_vs_d_k_step324.csv"

STEP324_BASELINE = {
    "A": 4.118419256684808,
    "alpha": -0.996854915495847,
    "B": -0.039179497004447894,
    "beta": 0.4086679154653991,
    "RMSE": 0.014046213677353668,
}
STEP324_HEIGHT_ONLY = {"A": 59.25627400823022, "alpha": -2.025096547538233, "RMSE": 0.02555236988922006}


def read_rows() -> list[dict[str, str]]:
    with DATA.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def h_pi_over_log(T: np.ndarray) -> np.ndarray:
    return math.pi / (T * np.log(T / (2.0 * math.pi)))


def A_pi_over_log(T: np.ndarray) -> np.ndarray:
    return math.pi / np.log(T / (2.0 * math.pi))


def rel_stats(values: list[float]) -> dict[str, float]:
    arr = np.array(values, dtype=float)
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "max": float(np.max(arr)),
        "std": float(np.std(arr)),
    }


def fit_curve(name: str, func, xdata, ydata: np.ndarray, guesses: list[tuple[float, ...]]) -> tuple[np.ndarray, np.ndarray, float]:
    best: tuple[float, np.ndarray, np.ndarray] | None = None
    for guess in guesses:
        try:
            popt, _ = curve_fit(func, xdata, ydata, p0=guess, maxfev=200000)
            pred = func(xdata, *popt)
            score = rmse(ydata, pred)
            if best is None or score < best[0]:
                best = (score, popt, pred)
        except Exception:
            continue
    if best is None:
        raise RuntimeError(f"all curve_fit attempts failed for {name}")
    return best[1], best[2], best[0]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    data_rows = read_rows()
    k = np.array([int(r["k"]) for r in data_rows], dtype=int)
    T = np.array([float(r["Im_rho_k"]) for r in data_rows], dtype=float)
    d = np.array([float(r["d_k_min_gap"]) for r in data_rows], dtype=float)
    gamma = np.array([float(r["gamma_k"]) for r in data_rows], dtype=float)

    def m1(xdata, A, alpha, B, beta):
        TT, dd = xdata
        return A * (TT**alpha) + B * (dd**beta)

    def m2(xdata, B, beta):
        TT, dd = xdata
        return h_pi_over_log(TT) + B * (dd**beta)

    def m3(xdata, C, B, beta):
        TT, dd = xdata
        return C * h_pi_over_log(TT) + B * (dd**beta)

    popt1, pred1, rmse1 = fit_curve(
        "M1",
        m1,
        (T, d),
        gamma,
        [
            (STEP324_BASELINE["A"], STEP324_BASELINE["alpha"], STEP324_BASELINE["B"], STEP324_BASELINE["beta"]),
            (4.0, -1.0, -0.04, 0.4),
            (1.0, -0.8, -0.02, 1.0),
            (60.0, -2.0, 0.01, 1.0),
        ],
    )
    popt2, pred2, rmse2 = fit_curve(
        "M2",
        m2,
        (T, d),
        gamma,
        [
            (STEP324_BASELINE["B"], STEP324_BASELINE["beta"]),
            (-0.04, 0.4),
            (-0.02, 1.0),
            (0.01, -1.0),
            (-0.1, 0.1),
        ],
    )
    popt3, pred3, rmse3 = fit_curve(
        "M3",
        m3,
        (T, d),
        gamma,
        [
            (1.0, STEP324_BASELINE["B"], STEP324_BASELINE["beta"]),
            (0.75, -0.04, 0.4),
            (1.5, -0.05, 0.5),
            (0.5, -0.02, 1.0),
            (2.0, -0.1, 0.1),
        ],
    )

    fit_rows = [
        {
            "model": "M1_constant_A_baseline",
            "formula": "gamma=A*T^alpha+B*d^beta",
            "A_or_C": f"{popt1[0]:.15e}",
            "alpha": f"{popt1[1]:.15e}",
            "B": f"{popt1[2]:.15e}",
            "beta": f"{popt1[3]:.15e}",
            "RMSE": f"{rmse1:.15e}",
            "RMSE_ratio_vs_M1": "1.000000000000000e+00",
            "note": "refit of Step 324 baseline",
        },
        {
            "model": "M2_bare_pi_over_log",
            "formula": "gamma=pi/(T*log(T/(2*pi)))+B*d^beta",
            "A_or_C": "1.000000000000000e+00",
            "alpha": "",
            "B": f"{popt2[0]:.15e}",
            "beta": f"{popt2[1]:.15e}",
            "RMSE": f"{rmse2:.15e}",
            "RMSE_ratio_vs_M1": f"{rmse2 / rmse1:.15e}",
            "note": "bare structural pi/log term; only spacing term fitted",
        },
        {
            "model": "M3_scaled_pi_over_log",
            "formula": "gamma=C*pi/(T*log(T/(2*pi)))+B*d^beta",
            "A_or_C": f"{popt3[0]:.15e}",
            "alpha": "",
            "B": f"{popt3[1]:.15e}",
            "beta": f"{popt3[2]:.15e}",
            "RMSE": f"{rmse3:.15e}",
            "RMSE_ratio_vs_M1": f"{rmse3 / rmse1:.15e}",
            "note": "scaled structural pi/log term",
        },
        {
            "model": "Step324_reported_constant_A",
            "formula": "gamma=A*T^alpha+B*d^beta",
            "A_or_C": f"{STEP324_BASELINE['A']:.15e}",
            "alpha": f"{STEP324_BASELINE['alpha']:.15e}",
            "B": f"{STEP324_BASELINE['B']:.15e}",
            "beta": f"{STEP324_BASELINE['beta']:.15e}",
            "RMSE": f"{STEP324_BASELINE['RMSE']:.15e}",
            "RMSE_ratio_vs_M1": f"{STEP324_BASELINE['RMSE'] / rmse1:.15e}",
            "note": "reported inherited Step 324 value",
        },
    ]
    write_csv(ART / "three_model_fits_step370.csv", fit_rows)

    pred_rows: list[dict[str, object]] = []
    A_pred = A_pi_over_log(T)
    for i in range(len(k)):
        for model_name, pred in [
            ("M1_constant_A_baseline", pred1),
            ("M2_bare_pi_over_log", pred2),
            ("M3_scaled_pi_over_log", pred3),
        ]:
            pred_rows.append(
                {
                    "rho_index": int(k[i]),
                    "T": f"{T[i]:.15f}",
                    "d_min_gap": f"{d[i]:.15f}",
                    "gamma_actual": f"{gamma[i]:.15e}",
                    "model": model_name,
                    "gamma_pred": f"{pred[i]:.15e}",
                    "residual": f"{gamma[i] - pred[i]:.15e}",
                    "abs_residual": f"{abs(gamma[i] - pred[i]):.15e}",
                }
            )
    write_csv(ART / "per_zero_predictions_step370.csv", pred_rows)

    B0 = STEP324_BASELINE["B"]
    beta0 = STEP324_BASELINE["beta"]
    A_local = T * (gamma - B0 * (d**beta0))
    rel_local = np.abs(A_local - A_pred) / np.abs(A_pred)
    local_stats = rel_stats([float(x) for x in rel_local])
    local_rows: list[dict[str, object]] = []
    for i in range(len(k)):
        local_rows.append(
            {
                "rho_index": int(k[i]),
                "T": f"{T[i]:.15f}",
                "d_min_gap": f"{d[i]:.15f}",
                "gamma_actual": f"{gamma[i]:.15e}",
                "B_step324": f"{B0:.15e}",
                "beta_step324": f"{beta0:.15e}",
                "A_j_local_solved": f"{A_local[i]:.15e}",
                "A_pi_over_log": f"{A_pred[i]:.15e}",
                "rel_err": f"{rel_local[i]:.15e}",
                "equation": "A_j=T*(gamma-B_step324*d^beta_step324)",
            }
        )
    write_csv(ART / "per_zero_A_j_local_step370.csv", local_rows)

    if rmse2 < 0.025 and local_stats["mean"] < 0.20:
        verdict = "pi_over_log_structural_derivation_supported"
    elif rmse3 <= 1.5 * rmse1 and 0.5 <= popt3[0] <= 2.0:
        verdict = "scaled_pi_over_log_shape_supported"
    elif rmse2 >= 3.0 * rmse1 and rmse3 >= 3.0 * rmse1:
        verdict = "pi_over_log_single_zero_coincidence"
    else:
        verdict = "partial_pi_over_log_signal_not_decisive"

    summary = [
        "# Step 370 Results Summary",
        "",
        "Dataset: exact Step 324 `gamma_vs_d_k_step324.csv` with 15 rows. Here `d` is the minimum neighboring-zero gap, not a defect order.",
        "",
        "Inherited citations:",
        "- Step 324: constant-A model `gamma = 4.118419*T^-0.996855 - 0.039179*d^0.408668`, RMSE `0.014046`.",
        "- Step 366: proposed `A_predicted(T)=pi/log(T/(2*pi))` after the rho_1 coefficient match.",
        "- Step 367: per-zero `gamma*T` comparison was ambiguous and scattered.",
        "- Step 369: no defect-order axis exists in the Branch C evaluator; Step 324's `d` is a zero-gap variable.",
        "",
        f"M1 refit RMSE: `{rmse1:.6g}`.",
        f"M2 bare pi/log RMSE: `{rmse2:.6g}`; ratio vs M1 `{rmse2 / rmse1:.6g}`.",
        f"M3 scaled pi/log RMSE: `{rmse3:.6g}`; ratio vs M1 `{rmse3 / rmse1:.6g}`; fitted C `{popt3[0]:.6g}`.",
        "",
        f"Corrected local `A_j` comparison using Step 324 B,beta: mean rel err `{local_stats['mean']:.6g}`, median `{local_stats['median']:.6g}`, max `{local_stats['max']:.6g}`, std `{local_stats['std']:.6g}`.",
        "",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step370_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    schema = {
        "step": 370,
        "orientation": "attempt",
        "dataset": str(DATA),
        "n_rows": int(len(gamma)),
        "models": ["M1", "M2", "M3"],
        "M1_RMSE": rmse1,
        "M2_RMSE": rmse2,
        "M3_RMSE": rmse3,
        "M2_RMSE_ratio_vs_M1": rmse2 / rmse1,
        "M3_RMSE_ratio_vs_M1": rmse3 / rmse1,
        "M3_C": float(popt3[0]),
        "local_Aj_rel_err_stats": local_stats,
        "final_verdict": verdict,
    }
    (ART / "step370_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")

    (ART / "nonclaim_boundary_step370.md").write_text(
        "# Step 370 Nonclaim Boundary\n\n"
        "- This step does not prove RH or Branch C closure.\n"
        "- All models are nonlinear least-squares diagnostics on the 15-row Step 324 dataset.\n"
        "- The `pi/log` term is tested as a structural hypothesis only; a good or bad fit is not a theorem about zeta zeros.\n"
        "- The corrected local `A_j` calculation uses Step 324's fitted `B,beta` and is model-dependent.\n",
        encoding="utf-8",
    )

    print("STEP370_COMPUTE_DONE")
    print(f"M1_RMSE={rmse1:.12e}")
    print(f"M2_RMSE={rmse2:.12e}")
    print(f"M3_RMSE={rmse3:.12e}")
    print(f"M3_C={popt3[0]:.12e}")
    print(f"local_Aj_mean_rel_err={local_stats['mean']:.12e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
