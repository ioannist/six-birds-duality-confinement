#!/usr/bin/env python3
"""Fit Step 246 Phi grid against several analytical candidate forms."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.optimize import curve_fit, minimize_scalar
from scipy.special import erf, voigt_profile


mp.mp.dps = 100
BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step246_phi_max_analytical_refinement_artifacts")


def load_grid():
    with (BASE / "phi_grid_step246.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    sigma = np.array([float(r["sigma"]) for r in rows])
    ell = np.array([float(r["ell"]) for r in rows])
    phi = np.array([float(r["Phi"]) for r in rows])
    return rows, sigma, ell, phi


def rmse(y, pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(y) - np.asarray(pred)) ** 2)))


def maxabs(y, pred) -> float:
    return float(np.max(np.abs(np.asarray(y) - np.asarray(pred))))


def band_shift(sigma, ell):
    sigma = np.asarray(sigma, dtype=float)
    ell = np.asarray(ell, dtype=float)
    a = np.where(ell <= 2.0, 1.0, ell - 1.0)
    val2 = 0.5 * (erf(sigma * (1.0 + ell)) - erf(sigma * a))
    return np.sqrt(np.maximum(val2, 0.0))


def fit_record(name, params, y, pred, status):
    return {
        "formula": name,
        "parameters": params,
        "rmse": f"{rmse(y, pred):.17e}",
        "max_abs_residual": f"{maxabs(y, pred):.17e}",
        "status": status,
    }


def main() -> None:
    rows, sigma, ell, phi = load_grid()
    records = []

    # (d) Specific two-erf band shift, no fit. This is the theorem-adjacent
    # model from the exact high-pass/low-pass Fourier overlap for an
    # untruncated Gaussian.
    pred = band_shift(sigma, ell)
    records.append(
        fit_record(
            "two_erf_band_shift_no_fit",
            "Phi^2=0.5*(erf(sigma*(1+ell))-erf(sigma*a)); a=1 for ell<=2 else ell-1",
            phi,
            pred,
            "closed_form_candidate_untruncated_gaussian",
        )
    )

    # Same model with a global scale and effective sigma correction.
    def scaled_band(x, c, eta):
        s, e = x
        return c * band_shift(eta * s, e)

    popt, _ = curve_fit(
        scaled_band,
        (sigma, ell),
        phi,
        p0=(1.0, 1.0),
        bounds=([0.0, 0.1], [2.0, 5.0]),
        maxfev=50000,
    )
    pred = scaled_band((sigma, ell), *popt)
    records.append(fit_record("two_erf_band_shift_scaled_sigma", f"c={popt[0]:.12g};eta={popt[1]:.12g}", phi, pred, "two_parameter_fit"))

    # (a) Pure erf shift with affine g(ell).
    def pure_erf_affine(x, c, a, b):
        s, e = x
        return c * np.sqrt(np.maximum(erf(s * np.maximum(0.0, a * e + b)), 0.0))

    popt, _ = curve_fit(
        pure_erf_affine,
        (sigma, ell),
        phi,
        p0=(0.5, 0.5, 0.2),
        bounds=([0.0, -10.0, -10.0], [5.0, 10.0, 10.0]),
        maxfev=50000,
    )
    pred = pure_erf_affine((sigma, ell), *popt)
    records.append(fit_record("pure_erf_shift_affine_g", f"c={popt[0]:.12g};a={popt[1]:.12g};b={popt[2]:.12g}", phi, pred, "generic_fit"))

    # (b) Voigt profile against sigma with ell-dependent center proxy.
    def voigt_candidate(x, c, gamma, eta):
        s, e = x
        return c * voigt_profile(s - eta / (1.0 + e), 1.0, gamma)

    popt, _ = curve_fit(
        voigt_candidate,
        (sigma, ell),
        phi,
        p0=(1.0, 0.5, 0.5),
        bounds=([0.0, 1e-4, -10.0], [20.0, 10.0, 10.0]),
        maxfev=50000,
    )
    pred = voigt_candidate((sigma, ell), *popt)
    records.append(fit_record("voigt_sigma_centered_by_ell", f"c={popt[0]:.12g};gamma={popt[1]:.12g};eta={popt[2]:.12g}", phi, pred, "generic_fit"))

    # (c) Sinc-related.
    def sinc_candidate(x, c, h, d):
        s, e = x
        return np.abs(c * np.sinc(h * s * e / math.pi)) + d

    popt, _ = curve_fit(
        sinc_candidate,
        (sigma, ell),
        phi,
        p0=(0.2, 1.0, 0.2),
        bounds=([-5.0, -20.0, -5.0], [5.0, 20.0, 5.0]),
        maxfev=50000,
    )
    pred = sinc_candidate((sigma, ell), *popt)
    records.append(fit_record("sinc_sigma_ell", f"c={popt[0]:.12g};h={popt[1]:.12g};d={popt[2]:.12g}", phi, pred, "generic_fit"))

    # Flexible two-erf affine edge model.
    def two_erf_affine_edges(x, c, a0, a1, b0, b1):
        s, e = x
        lo = np.maximum(0.0, a0 + a1 * e)
        hi = np.maximum(lo + 1e-9, b0 + b1 * e)
        val2 = np.maximum(0.0, erf(s * hi) - erf(s * lo))
        return c * np.sqrt(val2)

    popt, _ = curve_fit(
        two_erf_affine_edges,
        (sigma, ell),
        phi,
        p0=(0.7, 1.0, 0.0, 1.0, 1.0),
        bounds=([0.0, -10.0, -10.0, -10.0, -10.0], [5.0, 10.0, 10.0, 10.0, 10.0]),
        maxfev=100000,
    )
    pred = two_erf_affine_edges((sigma, ell), *popt)
    records.append(
        fit_record(
            "two_erf_affine_edges",
            "c={:.12g};a0={:.12g};a1={:.12g};b0={:.12g};b1={:.12g}".format(*popt),
            phi,
            pred,
            "flexible_fit_not_closed_form",
        )
    )

    # Known constants and Phi_max lookups.
    phi_max_inherited = mp.mpf("0.4904766190")
    sigma_star_exact = mp.sqrt(mp.log(3) / 8)
    phi_max_band = mp.sqrt(mp.mpf("0.5") * (mp.erf(3 * sigma_star_exact) - mp.erf(sigma_star_exact)))
    constants = [
        ("inherited_phi_max_step220", phi_max_inherited, "numeric target"),
        ("1/2", mp.mpf("0.5"), "simple constant"),
        ("2log2/pi", 2 * mp.log(2) / mp.pi, "simple constant"),
        ("zeta2_over_2pi", (mp.pi**2 / 6) / (2 * mp.pi), "simple constant"),
        ("1/pi", 1 / mp.pi, "simple constant"),
        ("band_model_max_sigma_sqrt_log3_over_8", phi_max_band, "derived from two-erf band model at ell=2"),
    ]
    const_rows = []
    for name, value, source in constants:
        const_rows.append(
            {
                "constant_or_formula": name,
                "value": mp.nstr(value, 30),
                "abs_residual_vs_step220_phi_max": mp.nstr(abs(value - phi_max_inherited), 30),
                "source": source,
            }
        )

    # Local symbolic check: no low-complexity elementary constant was found.
    # The best structured expression is parametric, not a standalone constant.
    best = min(records, key=lambda r: float(r["rmse"]))
    verdict = "V_phi_closed_form_found" if float(best["rmse"]) < 1e-4 and best["formula"].startswith("two_erf_band_shift_no_fit") else (
        "V_phi_alternative_fit_better" if float(best["rmse"]) < 1e-3 else "V_phi_no_simple_closed_form"
    )

    with (BASE / "alternative_fits_step246.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    with (BASE / "constant_lookup_step246.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(const_rows[0].keys()))
        writer.writeheader()
        writer.writerows(const_rows)

    with (BASE / "fit_phi_output_step246.txt").open("w") as f:
        f.write(f"best_fit={best}\n")
        f.write(f"verdict_prelim={verdict}\n")
        f.write(f"band_model_max_sigma={mp.nstr(sigma_star_exact, 30)}\n")
        f.write(f"band_model_max_phi={mp.nstr(phi_max_band, 30)}\n")

    print((BASE / "fit_phi_output_step246.txt").read_text())


if __name__ == "__main__":
    main()
