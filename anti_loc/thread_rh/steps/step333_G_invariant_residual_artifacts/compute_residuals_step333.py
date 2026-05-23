#!/usr/bin/env python3
"""Step 333: subtract per-G height trends and test common d-spacing residual."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step333_G_invariant_residual_artifacts"
STEP332_CROSS = ROOT / "anti_loc/thread/steps/step332_G_prime_full_height_fit_artifacts/cross_G_universality_step332.csv"


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


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return math.sqrt(float(np.mean((y - pred) ** 2)))


def height_fit(T: np.ndarray, gamma: np.ndarray) -> dict[str, float]:
    def model(T_, A, alpha):
        return A * (T_ ** alpha)

    popt, _ = curve_fit(model, T, gamma, p0=[4.0, -1.0], maxfev=100000)
    pred = model(T, *popt)
    return {"A": float(popt[0]), "alpha": float(popt[1]), "RMSE": rmse(gamma, pred), "pred": pred}


def fit_residual_models(d: np.ndarray, residual: np.ndarray, G_id: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    # Linear: c0 + c1 d
    X = np.vstack([np.ones_like(d), d]).T
    beta, *_ = np.linalg.lstsq(X, residual, rcond=None)
    pred = X @ beta
    rows.append({
        "G_id": G_id,
        "model": "linear_R=c0+c1*d",
        "p0_or_c0": f"{beta[0]:.12e}",
        "p1_or_c1": f"{beta[1]:.12e}",
        "RMSE": f"{rmse(residual, pred):.12e}",
    })

    # Exponential: a exp(b d), sign allowed through a.
    def exp_model(d_, a, b):
        return a * np.exp(b * d_)

    try:
        popt, _ = curve_fit(exp_model, d, residual, p0=[float(np.mean(residual)) or 1e-3, 0.1], maxfev=100000)
        pred = exp_model(d, *popt)
        rows.append({
            "G_id": G_id,
            "model": "exponential_R=a*exp(b*d)",
            "p0_or_c0": f"{popt[0]:.12e}",
            "p1_or_c1": f"{popt[1]:.12e}",
            "RMSE": f"{rmse(residual, pred):.12e}",
        })
    except Exception as exc:
        rows.append({"G_id": G_id, "model": "exponential_R=a*exp(b*d)", "p0_or_c0": "fit_failed", "p1_or_c1": str(exc), "RMSE": "nan"})

    # Power: a d^b, sign allowed through a.
    def pow_model(d_, a, b):
        return a * (d_ ** b)

    try:
        popt, _ = curve_fit(pow_model, d, residual, p0=[float(np.mean(residual)) or 1e-3, 1.0], maxfev=100000)
        pred = pow_model(d, *popt)
        rows.append({
            "G_id": G_id,
            "model": "power_R=a*d^b",
            "p0_or_c0": f"{popt[0]:.12e}",
            "p1_or_c1": f"{popt[1]:.12e}",
            "RMSE": f"{rmse(residual, pred):.12e}",
        })
    except Exception as exc:
        rows.append({"G_id": G_id, "model": "power_R=a*d^b", "p0_or_c0": "fit_failed", "p1_or_c1": str(exc), "RMSE": "nan"})
    return rows


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    base_rows = [r for r in read_csv(STEP332_CROSS) if r["rho_index"].isdigit()]
    T = np.array([float(r["T"]) for r in base_rows], dtype=float)
    d = np.array([float(r["d_min_gap"]) for r in base_rows], dtype=float)
    gamma_star = np.array([float(r["gamma_G_star"]) for r in base_rows], dtype=float)
    gamma_prime = np.array([float(r["gamma_G_prime"]) for r in base_rows], dtype=float)

    fit_star = height_fit(T, gamma_star)
    fit_prime = height_fit(T, gamma_prime)
    R_star = gamma_star - fit_star["pred"]
    R_prime = gamma_prime - fit_prime["pred"]
    diff = R_star - R_prime
    residual_corr = pearson(R_star, R_prime)

    height_rows = [
        {"G_id": "G_star", "model": "gamma=A*T^alpha", "A": f"{fit_star['A']:.12e}", "alpha": f"{fit_star['alpha']:.12e}", "RMSE": f"{fit_star['RMSE']:.12e}", "source": "step333_refit_from_step332_cross_table"},
        {"G_id": "G_prime", "model": "gamma=A*T^alpha", "A": f"{fit_prime['A']:.12e}", "alpha": f"{fit_prime['alpha']:.12e}", "RMSE": f"{fit_prime['RMSE']:.12e}", "source": "step333_refit_from_step332_cross_table"},
    ]
    residual_rows = []
    for i, row in enumerate(base_rows):
        residual_rows.append({
            "rho_index": row["rho_index"],
            "T": row["T"],
            "d_min_gap": row["d_min_gap"],
            "gamma_G_star": f"{gamma_star[i]:.12e}",
            "height_pred_G_star": f"{fit_star['pred'][i]:.12e}",
            "R_G_star": f"{R_star[i]:.12e}",
            "gamma_G_prime": f"{gamma_prime[i]:.12e}",
            "height_pred_G_prime": f"{fit_prime['pred'][i]:.12e}",
            "R_G_prime": f"{R_prime[i]:.12e}",
            "R_star_minus_R_prime": f"{diff[i]:.12e}",
        })

    fit_rows = []
    fit_rows.extend(fit_residual_models(d, R_star, "G_star"))
    fit_rows.extend(fit_residual_models(d, R_prime, "G_prime"))

    # Best-model parameter comparison by minimum RMSE per G.
    best_star = min([r for r in fit_rows if r["G_id"] == "G_star" and r["RMSE"] != "nan"], key=lambda r: float(r["RMSE"]))
    best_prime = min([r for r in fit_rows if r["G_id"] == "G_prime" and r["RMSE"] != "nan"], key=lambda r: float(r["RMSE"]))
    verdict = "G_invariant_spacing_residual" if residual_corr > 0.8 and best_star["model"] == best_prime["model"] else "residuals_remain_G_dependent"
    corr_rows = [
        {
            "metric": "Pearson_R_G_star_R_G_prime",
            "value": f"{residual_corr:.12e}",
            "mean_R_star_minus_R_prime": f"{float(np.mean(diff)):.12e}",
            "std_R_star_minus_R_prime": f"{float(np.std(diff)):.12e}",
            "best_model_G_star": best_star["model"],
            "best_model_G_prime": best_prime["model"],
            "best_RMSE_G_star": best_star["RMSE"],
            "best_RMSE_G_prime": best_prime["RMSE"],
            "verdict": verdict,
            "G_id": "",
            "model": "",
            "p0_or_c0": "",
            "p1_or_c1": "",
            "RMSE": "",
        }
    ] + fit_rows

    write_csv(ART / "height_fits_per_G_step333.csv", height_rows)
    write_csv(ART / "residuals_per_G_step333.csv", residual_rows)
    write_csv(ART / "residual_correlation_step333.csv", corr_rows)

    summary = [
        "# Step 333 Results Summary",
        "",
        "Inherited citations:",
        "- Step 324: `G_star` 15-point fit was `A=4.118`, `alpha=-0.997`, `B=-0.039`, `beta=0.409`, `RMSE=0.014`.",
        "- Step 332: `G_prime` 15-point fit was `A=346.615`, `alpha=-2.443`, `B=-1.795e-4`, `beta=3.803`, `RMSE=0.0283`, and Pearson gamma-star/gamma-prime was `0.867`.",
        "",
        f"Height-only refit: `G_star` A=`{fit_star['A']:.6g}`, alpha=`{fit_star['alpha']:.6g}`, RMSE=`{fit_star['RMSE']:.6g}`.",
        f"Height-only refit: `G_prime` A=`{fit_prime['A']:.6g}`, alpha=`{fit_prime['alpha']:.6g}`, RMSE=`{fit_prime['RMSE']:.6g}`.",
        f"Residual Pearson correlation: `{residual_corr:.6g}`.",
        f"Residual difference mean/std: `{float(np.mean(diff)):.6g}` / `{float(np.std(diff)):.6g}`.",
        f"Best residual model for G_star: `{best_star['model']}` with RMSE `{best_star['RMSE']}`.",
        f"Best residual model for G_prime: `{best_prime['model']}` with RMSE `{best_prime['RMSE']}`.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step333_results_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    schema = {
        "step": 333,
        "orientation": "attempt",
        "target": "G-invariant residual after height subtraction",
        "residual_pearson": residual_corr,
        "mean_residual_difference": float(np.mean(diff)),
        "std_residual_difference": float(np.std(diff)),
        "final_verdict": verdict,
    }
    (ART / "step333_schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")
    (ART / "nonclaim_boundary_step333.md").write_text(
        "# Step 333 Nonclaim Boundary\n\n"
        "- This step is a finite-data residual analysis only.\n"
        "- It does not prove RH or close Branch C.\n"
        "- The fitted residual functions of zero spacing are diagnostic, not theorem-grade.\n",
        encoding="utf-8",
    )
    print("STEP333_COMPUTE_DONE")
    print(f"residual_pearson={residual_corr:.12e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
