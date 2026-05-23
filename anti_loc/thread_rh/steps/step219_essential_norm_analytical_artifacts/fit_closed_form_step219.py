#!/usr/bin/env python3
"""Fit closed-form candidates for Step 219 Phi data."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit
from scipy.special import erf


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step219_essential_norm_analytical_artifacts")


def load_rows():
    with (BASE / "phi_values_step219.csv").open(newline="") as f:
        return list(csv.DictReader(f))


def rmse(y, pred) -> float:
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def maxabs(y, pred) -> float:
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    return float(np.max(np.abs(y - pred)))


def band_shift_phi(sigma, ell):
    """Gaussian high-pass shifted into the sinc low-pass window |xi|<1."""
    sigma = np.asarray(sigma, dtype=float)
    ell = np.asarray(ell, dtype=float)
    a = np.where(ell <= 2.0, 1.0, ell - 1.0)
    b = 1.0 + ell
    val2 = 0.5 * (erf(sigma * b) - erf(sigma * a))
    return np.sqrt(np.maximum(val2, 0.0))


def main() -> None:
    rows = load_rows()
    ell_rows = [r for r in rows if r["sweep"] == "ell"]
    sigma_rows = [r for r in rows if r["sweep"] == "sigma"]
    x = np.array([float(r["ell"]) for r in ell_rows])
    y = np.array([float(r["Phi"]) for r in ell_rows])
    sig = np.array([float(r["sigma"]) for r in sigma_rows])
    ys = np.array([float(r["Phi"]) for r in sigma_rows])
    ell_log2 = math.log(2.0)

    candidates = []

    fit_specs = [
        ("power_c_l_alpha", lambda t, c, a: c * np.power(t, a), (0.3, 0.5)),
        ("log_c_log_1_plus_l", lambda t, c: c * np.log1p(t), (0.4,)),
        ("saturating_c_1_exp_minus_l", lambda t, c: c * (1 - np.exp(-t)), (0.5,)),
        ("sinc_like_abs_c_sin_l2_over_l2", lambda t, c: np.abs(c * np.sinc(t / (2 * math.pi))), (0.3,)),
        ("sigmoid_c_l_sqrt_l2_d2", lambda t, c, d: c * t / np.sqrt(t * t + d * d), (0.5, 1.0)),
    ]
    for name, func, p0 in fit_specs:
        try:
            popt, _ = curve_fit(func, x, y, p0=p0, maxfev=20000)
            pred = func(x, *popt)
            candidates.append(
                {
                    "formula": name,
                    "parameters": ";".join(f"{p:.12g}" for p in np.atleast_1d(popt)),
                    "rmse": f"{rmse(y, pred):.17e}",
                    "max_abs_residual": f"{maxabs(y, pred):.17e}",
                    "status": "generic_fit",
                }
            )
        except Exception as exc:
            candidates.append(
                {
                    "formula": name,
                    "parameters": "fit_failed",
                    "rmse": "nan",
                    "max_abs_residual": "nan",
                    "status": str(exc),
                }
            )

    pred_band = band_shift_phi(1.0, x)
    candidates.append(
        {
            "formula": "band_shift_erf_sigma1_piecewise",
            "parameters": "Phi^2=0.5*(erf(b)-erf(a)); a=1 if ell<=2 else ell-1; b=ell+1",
            "rmse": f"{rmse(y, pred_band):.17e}",
            "max_abs_residual": f"{maxabs(y, pred_band):.17e}",
            "status": "derived_sinc_projection_model",
        }
    )
    try:
        popt, _ = curve_fit(lambda t, c, s: c * band_shift_phi(s, t), x, y, p0=(1.0, 1.0), bounds=([0.0, 0.0], [10.0, 10.0]), maxfev=20000)
        pred = popt[0] * band_shift_phi(popt[1], x)
        candidates.append(
            {
                "formula": "band_shift_erf_scaled_sigma_eff",
                "parameters": f"scale={popt[0]:.12g};sigma_eff={popt[1]:.12g}",
                "rmse": f"{rmse(y, pred):.17e}",
                "max_abs_residual": f"{maxabs(y, pred):.17e}",
                "status": "two_parameter_band_shift_fit",
            }
        )
    except Exception as exc:
        candidates.append(
            {
                "formula": "band_shift_erf_scaled_sigma_eff",
                "parameters": "fit_failed",
                "rmse": "nan",
                "max_abs_residual": "nan",
                "status": str(exc),
            }
        )

    # Sigma fits at fixed ell=log2.
    sigma_candidates = []
    sigma_specs = [
        ("sigma_power_c_s_alpha", lambda s, c, a: c * np.power(s, a), (0.3, -0.2)),
        ("sigma_exp_decay_c_exp_minus_d_s", lambda s, c, d: c * np.exp(-d * s), (0.6, 0.4)),
        ("sigma_band_shift_erf_log2", lambda s: band_shift_phi(s, ell_log2), None),
    ]
    for item in sigma_specs:
        name = item[0]
        if item[2] is None:
            pred = item[1](sig)
            sigma_candidates.append(
                {
                    "formula": name,
                    "parameters": "no fit; ell=log2 band-shift model",
                    "rmse": f"{rmse(ys, pred):.17e}",
                    "max_abs_residual": f"{maxabs(ys, pred):.17e}",
                    "status": "derived_sinc_projection_model",
                }
            )
        else:
            func = item[1]
            popt, _ = curve_fit(func, sig, ys, p0=item[2], maxfev=20000)
            pred = func(sig, *popt)
            sigma_candidates.append(
                {
                    "formula": name,
                    "parameters": ";".join(f"{p:.12g}" for p in np.atleast_1d(popt)),
                    "rmse": f"{rmse(ys, pred):.17e}",
                    "max_abs_residual": f"{maxabs(ys, pred):.17e}",
                    "status": "generic_fit",
                }
            )

    # Separable test: compare Phi(sigma, ell) to f_sigma * g_ell using only
    # the available cross values at log2 and sigma=1. This is limited, but
    # the band-shift model is explicitly nonseparable.
    separable_rows = [
        {
            "test": "band_shift_nonseparable_diagnostic",
            "result": "not_separable",
            "notes": "Derived model depends on erf(sigma*(1+ell))-erf(sigma*a(ell)), not f(sigma)g(ell). Available grid is cross-shaped, not full matrix.",
        }
    ]

    constants = [
        ("log2_over_pi", math.log(2) / math.pi),
        ("zeta2_over_2pi", (math.pi * math.pi / 6.0) / (2.0 * math.pi)),
        ("ln2_over_2sqrt2", math.log(2.0) / (2.0 * math.sqrt(2.0))),
        ("1_over_pi", 1.0 / math.pi),
        ("1_over_4", 0.25),
        ("band_shift_log2_sigma1", float(band_shift_phi(1.0, ell_log2))),
    ]
    phi_log2 = float([r["Phi"] for r in ell_rows if r["ell_label"] == "log2"][0])
    const_rows = []
    for name, val in constants:
        const_rows.append(
            {
                "formula": name,
                "value": f"{val:.17e}",
                "residual_vs_Phi_sigma1_log2": f"{abs(val - phi_log2):.17e}",
            }
        )

    with (BASE / "ell_fits_step219.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(candidates[0].keys()))
        writer.writeheader()
        writer.writerows(candidates)

    with (BASE / "sigma_fits_step219.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(sigma_candidates[0].keys()))
        writer.writeheader()
        writer.writerows(sigma_candidates)

    with (BASE / "closed_form_candidates_step219.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(const_rows[0].keys()))
        writer.writeheader()
        writer.writerows(const_rows)

    with (BASE / "separable_test_step219.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(separable_rows[0].keys()))
        writer.writeheader()
        writer.writerows(separable_rows)

    best = min(candidates, key=lambda r: float(r["rmse"]) if r["rmse"] != "nan" else float("inf"))
    best_sigma = min(sigma_candidates, key=lambda r: float(r["rmse"]) if r["rmse"] != "nan" else float("inf"))
    with (BASE / "fit_closed_form_output_step219.txt").open("w") as f:
        f.write(f"best_ell_fit={best}\n")
        f.write(f"best_sigma_fit={best_sigma}\n")

    print((BASE / "fit_closed_form_output_step219.txt").read_text())


if __name__ == "__main__":
    main()
