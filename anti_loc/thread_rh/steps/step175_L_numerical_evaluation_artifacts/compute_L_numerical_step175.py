#!/usr/bin/env python3
"""Numerical Step 175 evaluation of L_{rho_1,0}(G_*).

The computation follows Step 174:

    L = - I_sinc - sum_n Psi_n(rho_1) J_n.

The Mellin transform of G_* is computed by Gauss-Legendre quadrature on the
three compact bump supports.  The PSWF factors are computed from the Step 173
operational identity by diagonalizing the sinc kernel on [-1,1]:

    K(x,y) = sin(x-y)/(pi (x-y)).

This avoids relying on a library-specific PSWF normalization.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, simpson


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step175_L_numerical_evaluation_artifacts"
)

GAMMA_1 = 14.134725141734693
RHO_1 = complex(0.5, GAMMA_1)
EPSILON = 0.2
CENTERS = [1.5, 2.5, 3.5]
LAMBDA = 1.0

MP_DPS = 50
U_MAX = 200.0
H = 0.05
U_TAIL_COMPARE = 160.0
N_T_PRIMARY = 280
N_T_COARSE = 180
N_PSWF_PRIMARY = 320
N_PSWF_ALT = 240
N_PSWF_TERMS = 12


def beta_bump(u: float | np.ndarray) -> float | np.ndarray:
    arr = np.asarray(u)
    out = np.zeros_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0
    out[mask] = np.exp(-1.0 / (1.0 - arr[mask] * arr[mask]))
    if np.isscalar(u):
        return float(out)
    return out


def bump(t: float | np.ndarray, center: float) -> float | np.ndarray:
    return beta_bump((np.asarray(t) - center) / EPSILON)


def sinc_kernel(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-12
    out[mask] = 1.0 / math.pi
    out[~mask] = np.sin(arr[~mask]) / (math.pi * arr[~mask])
    if np.isscalar(x):
        return float(out)
    return out


def compute_moments() -> dict[str, float]:
    A = []
    B = []
    for c in CENTERS:
        lo = c - EPSILON
        hi = c + EPSILON
        a_val = quad(
            lambda t, cc=c: bump(t, cc), lo, hi, epsabs=1e-14, epsrel=1e-14, limit=200
        )[0]
        b_val = quad(
            lambda t, cc=c: bump(t, cc) / t,
            lo,
            hi,
            epsabs=1e-14,
            epsrel=1e-14,
            limit=200,
        )[0]
        A.append(float(a_val))
        B.append(float(b_val))

    D = B[1] * A[2] - A[1] * B[2]
    alpha = (A[2] * B[0] - A[0] * B[2]) / D
    beta_3 = (A[1] * B[0] - A[0] * B[1]) / D
    return {
        "A_1": A[0],
        "A_2": A[1],
        "A_3": A[2],
        "B_1": B[0],
        "B_2": B[1],
        "B_3": B[2],
        "D": D,
        "alpha": alpha,
        "beta_3": beta_3,
    }


def build_t_quadrature(moments: dict[str, float], n_per_support: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xg, wg = leggauss(n_per_support)
    coeffs = [1.0, -moments["alpha"], moments["beta_3"]]
    all_t = []
    all_w = []
    all_g = []
    for coeff, center in zip(coeffs, CENTERS):
        lo = center - EPSILON
        hi = center + EPSILON
        t = 0.5 * (hi - lo) * xg + 0.5 * (hi + lo)
        w = 0.5 * (hi - lo) * wg
        g = coeff * bump(t, center)
        all_t.append(t)
        all_w.append(w)
        all_g.append(g)
    return np.concatenate(all_t), np.concatenate(all_w), np.concatenate(all_g)


def mellin_values(u_grid: np.ndarray, moments: dict[str, float], n_per_support: int) -> tuple[np.ndarray, dict[str, float]]:
    t, w, g = build_t_quadrature(moments, n_per_support)
    amp = w * g * t ** (-0.5)
    log_t = np.log(t)
    values = np.exp(-1j * np.outer(u_grid, log_t)).dot(amp)
    checks = {
        "endpoint_G0_residual": float(np.sum(w * g)),
        "endpoint_G1_residual": float(np.sum(w * g / t)),
        "quadrature_nodes": int(t.size),
    }
    return values, checks


def zeta_values(u_grid: np.ndarray) -> np.ndarray:
    mp.mp.dps = MP_DPS
    return np.array([complex(mp.zeta(mp.mpc(0.5, float(u)))) for u in u_grid], dtype=np.complex128)


def sinc_integral(u_grid: np.ndarray, F: np.ndarray) -> complex:
    return complex(simpson(sinc_kernel(GAMMA_1 - u_grid) * F, x=u_grid))


def pswf_eigensystem(n_nodes: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x, w = leggauss(n_nodes)
    sw = np.sqrt(w)
    d = x[:, None] - x[None, :]
    K = sinc_kernel(d)
    mat = sw[:, None] * K * sw[None, :]
    vals, vecs = np.linalg.eigh(mat)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    phi = vecs / sw[:, None]
    return x, w, vals, phi


def psi_from_phi(
    u_grid: np.ndarray,
    x_nodes: np.ndarray,
    weights: np.ndarray,
    mu: float,
    phi_values: np.ndarray,
) -> np.ndarray:
    d = u_grid[:, None] - x_nodes[None, :]
    int_k = sinc_kernel(d).dot(weights * phi_values)
    inside = np.abs(u_grid) <= LAMBDA
    psi = np.empty_like(int_k, dtype=np.complex128)
    psi[~inside] = -int_k[~inside] / math.sqrt(1.0 - mu)
    psi[inside] = (math.sqrt(1.0 - mu) / mu) * int_k[inside]
    return psi


def psi_at_gamma(x_nodes: np.ndarray, weights: np.ndarray, mu: float, phi_values: np.ndarray) -> complex:
    int_k = sinc_kernel(GAMMA_1 - x_nodes).dot(weights * phi_values)
    return complex(-int_k / math.sqrt(1.0 - mu))


def pswf_terms(
    u_grid: np.ndarray,
    F: np.ndarray,
    n_nodes: int,
    n_terms: int,
) -> tuple[list[dict[str, object]], list[complex]]:
    x, w, vals, phi = pswf_eigensystem(n_nodes)
    records: list[dict[str, object]] = []
    terms: list[complex] = []
    for n in range(n_terms):
        mu = float(vals[n])
        phi_n = phi[:, n]
        psi_u = psi_from_phi(u_grid, x, w, mu, phi_n)
        psi_rho = psi_at_gamma(x, w, mu, phi_n)
        J_n = complex(simpson(F * np.conjugate(psi_u), x=u_grid))
        term = psi_rho * J_n
        terms.append(term)
        records.append(
            {
                "n": n,
                "mu": mu,
                "Psi_rho_real": psi_rho.real,
                "Psi_rho_imag": psi_rho.imag,
                "J_real": J_n.real,
                "J_imag": J_n.imag,
                "term_real": term.real,
                "term_imag": term.imag,
                "term_abs": abs(term),
            }
        )
    return records, terms


def cfmt(z: complex) -> str:
    return f"{z.real:.16e}{z.imag:+.16e}j"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    moments = compute_moments()

    n_points = int(round(2 * U_MAX / H)) + 1
    u_grid = np.linspace(-U_MAX, U_MAX, n_points)
    G_primary, g_checks = mellin_values(u_grid, moments, N_T_PRIMARY)
    G_coarse, coarse_checks = mellin_values(u_grid, moments, N_T_COARSE)
    zeta_grid = zeta_values(u_grid)
    F_primary = zeta_grid * G_primary
    F_coarse_g = zeta_grid * G_coarse

    I_sinc = sinc_integral(u_grid, F_primary)
    I_sinc_half_grid = sinc_integral(u_grid[::2], F_primary[::2])
    tail_mask = np.abs(u_grid) <= U_TAIL_COMPARE
    I_sinc_u160 = sinc_integral(u_grid[tail_mask], F_primary[tail_mask])
    I_sinc_g_coarse = sinc_integral(u_grid, F_coarse_g)

    I_grid_error = abs(I_sinc - I_sinc_half_grid)
    I_tail_shell = abs(I_sinc - I_sinc_u160)
    I_g_error = abs(I_sinc - I_sinc_g_coarse)
    I_error_radius = I_grid_error + 2.0 * I_tail_shell + I_g_error + 1.0e-12

    pswf_records, terms = pswf_terms(u_grid, F_primary, N_PSWF_PRIMARY, N_PSWF_TERMS)
    pswf_records_alt, terms_alt = pswf_terms(u_grid, F_primary, N_PSWF_ALT, 4)
    _, terms_half = pswf_terms(u_grid[::2], F_primary[::2], N_PSWF_PRIMARY, 3)
    _, terms_g_coarse = pswf_terms(u_grid, F_coarse_g, N_PSWF_PRIMARY, 3)

    pswf_sum_0_2 = sum(terms[:3], 0j)
    pswf_sum_extended = sum(terms, 0j)
    pswf_tail_3_to_last = sum(terms[3:], 0j)
    pswf_tail_abs_3_to_last = float(sum(abs(t) for t in terms[3:]))
    last_tail_abs = float(abs(terms[-1]))
    pswf_tail_bound_n_ge_3 = max(1.0e-6, 2.0 * pswf_tail_abs_3_to_last + 10.0 * last_tail_abs)

    term_grid_error = float(sum(abs(terms[i] - terms_half[i]) for i in range(3)))
    term_g_error = float(sum(abs(terms[i] - terms_g_coarse[i]) for i in range(3)))
    term_pswf_discretization_error = float(sum(abs(terms[i] - terms_alt[i]) for i in range(3)))
    pswf_0_2_error = term_grid_error + term_g_error + term_pswf_discretization_error + 1.0e-12

    L_0_2 = -I_sinc - pswf_sum_0_2
    L_extended = -I_sinc - pswf_sum_extended
    total_error_radius = I_error_radius + pswf_0_2_error + pswf_tail_bound_n_ge_3 + 1.0e-12
    L_abs_lower_bound = max(0.0, abs(L_0_2) - total_error_radius)

    verdict = "V_L_numerical_nonzero" if L_abs_lower_bound > 1.0e-3 else "V_L_quadrature_indeterminate"

    moment_rows = [
        {"quantity": key, "value": f"{moments[key]:.16e}"}
        for key in ["A_1", "A_2", "A_3", "B_1", "B_2", "B_3", "alpha", "beta_3"]
    ]
    write_csv(ROOT / "G_star_moments_step175.csv", moment_rows, ["quantity", "value"])

    sinc_rows = [
        {
            "quantity": "I_sinc",
            "real": f"{I_sinc.real:.16e}",
            "imag": f"{I_sinc.imag:.16e}",
            "abs": f"{abs(I_sinc):.16e}",
            "error_radius": f"{I_error_radius:.16e}",
            "U": U_MAX,
            "h": H,
            "mp_dps": MP_DPS,
            "G_quadrature_nodes": g_checks["quadrature_nodes"],
            "grid_error": f"{I_grid_error:.16e}",
            "tail_shell_160_200": f"{I_tail_shell:.16e}",
            "G_quadrature_error": f"{I_g_error:.16e}",
        }
    ]
    write_csv(
        ROOT / "sinc_quadrature_step175.csv",
        sinc_rows,
        [
            "quantity",
            "real",
            "imag",
            "abs",
            "error_radius",
            "U",
            "h",
            "mp_dps",
            "G_quadrature_nodes",
            "grid_error",
            "tail_shell_160_200",
            "G_quadrature_error",
        ],
    )

    pswf_rows = [
        {
            "n": rec["n"],
            "mu": f"{float(rec['mu']):.16e}",
            "Psi_rho_real": f"{float(rec['Psi_rho_real']):.16e}",
            "Psi_rho_imag": f"{float(rec['Psi_rho_imag']):.16e}",
            "J_real": f"{float(rec['J_real']):.16e}",
            "J_imag": f"{float(rec['J_imag']):.16e}",
            "term_real": f"{float(rec['term_real']):.16e}",
            "term_imag": f"{float(rec['term_imag']):.16e}",
            "term_abs": f"{float(rec['term_abs']):.16e}",
        }
        for rec in pswf_records[:3]
    ]
    write_csv(
        ROOT / "pswf_evaluations_step175.csv",
        pswf_rows,
        [
            "n",
            "mu",
            "Psi_rho_real",
            "Psi_rho_imag",
            "J_real",
            "J_imag",
            "term_real",
            "term_imag",
            "term_abs",
        ],
    )

    L_rows = [
        {
            "quantity": "L_using_n_0_2",
            "real": f"{L_0_2.real:.16e}",
            "imag": f"{L_0_2.imag:.16e}",
            "abs": f"{abs(L_0_2):.16e}",
            "total_error_radius": f"{total_error_radius:.16e}",
            "lower_bound_abs": f"{L_abs_lower_bound:.16e}",
            "I_sinc_error": f"{I_error_radius:.16e}",
            "pswf_0_2_error": f"{pswf_0_2_error:.16e}",
            "pswf_tail_bound_n_ge_3": f"{pswf_tail_bound_n_ge_3:.16e}",
        },
        {
            "quantity": "L_using_n_0_11_diagnostic",
            "real": f"{L_extended.real:.16e}",
            "imag": f"{L_extended.imag:.16e}",
            "abs": f"{abs(L_extended):.16e}",
            "total_error_radius": f"{I_error_radius + pswf_0_2_error + 1.0e-8:.16e}",
            "lower_bound_abs": "",
            "I_sinc_error": f"{I_error_radius:.16e}",
            "pswf_0_2_error": f"{pswf_0_2_error:.16e}",
            "pswf_tail_bound_n_ge_3": f"{pswf_tail_bound_n_ge_3:.16e}",
        },
    ]
    write_csv(
        ROOT / "L_numerical_step175.csv",
        L_rows,
        [
            "quantity",
            "real",
            "imag",
            "abs",
            "total_error_radius",
            "lower_bound_abs",
            "I_sinc_error",
            "pswf_0_2_error",
            "pswf_tail_bound_n_ge_3",
        ],
    )

    sample_indices = np.linspace(0, len(u_grid) - 1, 21, dtype=int)
    sample_rows = [
        {
            "u": f"{u_grid[i]:.8f}",
            "G_real": f"{G_primary[i].real:.16e}",
            "G_imag": f"{G_primary[i].imag:.16e}",
            "zeta_real": f"{zeta_grid[i].real:.16e}",
            "zeta_imag": f"{zeta_grid[i].imag:.16e}",
        }
        for i in sample_indices
    ]
    write_csv(ROOT / "G_zeta_samples_step175.csv", sample_rows, ["u", "G_real", "G_imag", "zeta_real", "zeta_imag"])

    result = {
        "constants": {
            "rho_1": "0.5+14.134725141734693j",
            "gamma_1": GAMMA_1,
            "lambda": LAMBDA,
            "U": U_MAX,
            "h": H,
            "mp_dps": MP_DPS,
            "N_t_primary_per_support": N_T_PRIMARY,
            "N_t_coarse_per_support": N_T_COARSE,
            "N_pswf_primary": N_PSWF_PRIMARY,
            "N_pswf_alt": N_PSWF_ALT,
            "N_pswf_terms_extended": N_PSWF_TERMS,
        },
        "moments": moments,
        "G_checks": g_checks,
        "G_checks_coarse": coarse_checks,
        "I_sinc": {
            "real": I_sinc.real,
            "imag": I_sinc.imag,
            "abs": abs(I_sinc),
            "grid_error": I_grid_error,
            "tail_shell_160_200": I_tail_shell,
            "G_quadrature_error": I_g_error,
            "error_radius": I_error_radius,
        },
        "pswf_first_three": pswf_records[:3],
        "pswf_extended_terms": pswf_records,
        "pswf_sum_0_2": {"real": pswf_sum_0_2.real, "imag": pswf_sum_0_2.imag, "abs": abs(pswf_sum_0_2)},
        "pswf_sum_0_11": {
            "real": pswf_sum_extended.real,
            "imag": pswf_sum_extended.imag,
            "abs": abs(pswf_sum_extended),
        },
        "pswf_tail_3_to_11": {
            "real": pswf_tail_3_to_last.real,
            "imag": pswf_tail_3_to_last.imag,
            "abs_sum": pswf_tail_abs_3_to_last,
            "bound_n_ge_3": pswf_tail_bound_n_ge_3,
        },
        "pswf_errors": {
            "term_grid_error_0_2": term_grid_error,
            "term_G_quadrature_error_0_2": term_g_error,
            "term_pswf_discretization_error_0_2": term_pswf_discretization_error,
            "pswf_0_2_error": pswf_0_2_error,
        },
        "L": {
            "L_0_2_real": L_0_2.real,
            "L_0_2_imag": L_0_2.imag,
            "L_0_2_abs": abs(L_0_2),
            "L_extended_real": L_extended.real,
            "L_extended_imag": L_extended.imag,
            "L_extended_abs": abs(L_extended),
            "total_error_radius": total_error_radius,
            "lower_bound_abs": L_abs_lower_bound,
            "verdict": verdict,
        },
    }
    (ROOT / "numerical_results_step175.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Step 175 numerical evaluation")
    print(f"mpmath_dps={MP_DPS} U={U_MAX} h={H}")
    print("moments")
    for key in ["A_1", "A_2", "A_3", "B_1", "B_2", "B_3", "alpha", "beta_3"]:
        print(f"  {key}={moments[key]:.16e}")
    print(f"endpoint_residual_G0={g_checks['endpoint_G0_residual']:.16e}")
    print(f"endpoint_residual_G1={g_checks['endpoint_G1_residual']:.16e}")
    print(f"I_sinc={cfmt(I_sinc)} abs={abs(I_sinc):.16e} err={I_error_radius:.16e}")
    for rec in pswf_records[:3]:
        print(
            "pswf n={n} mu={mu:.16e} Psi_rho={psi} J={J} term={term} abs={absval:.16e}".format(
                n=rec["n"],
                mu=float(rec["mu"]),
                psi=cfmt(complex(float(rec["Psi_rho_real"]), float(rec["Psi_rho_imag"]))),
                J=cfmt(complex(float(rec["J_real"]), float(rec["J_imag"]))),
                term=cfmt(complex(float(rec["term_real"]), float(rec["term_imag"]))),
                absval=float(rec["term_abs"]),
            )
        )
    print(f"pswf_sum_0_2={cfmt(pswf_sum_0_2)}")
    print(f"pswf_tail_bound_n_ge_3={pswf_tail_bound_n_ge_3:.16e}")
    print(f"L_0_2={cfmt(L_0_2)} abs={abs(L_0_2):.16e}")
    print(f"L_extended_diagnostic={cfmt(L_extended)} abs={abs(L_extended):.16e}")
    print(f"total_error_radius={total_error_radius:.16e}")
    print(f"lower_bound_abs={L_abs_lower_bound:.16e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
