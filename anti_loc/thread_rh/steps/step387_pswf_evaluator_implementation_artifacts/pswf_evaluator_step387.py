#!/usr/bin/env python3
"""Step 387: constructive PSWF evaluator implementation.

This is a deliberately scoped numerical implementation of the missing Step 173
T174_3/T174_4 coefficient path.  It computes PSWFs on [-1,1] with SciPy,
uses a local cusp-coordinate proxy for the transported Sonine coordinate, and
uses the punctured-disc Bergman kernel model from Step 372 for the pulled
kernel derivative.

The exact U_infty transport from the cascade records is still unavailable, so
all projected quantities are labelled as a "standard-coordinate proxy".
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.special import pro_ang1


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step387_pswf_evaluator_implementation_artifacts")
DPS = 60
T1 = mp.mpf("14.1347251417346937904572519836")
RHO_LABEL = "rho_1"
K_VALUES = [5, 10, 15]
N_PSWF = 10
QUAD_N = 256
MELLIN_N = 96
HEIGHT_WINDOW = 1 / (2 * math.pi)
BANDWIDTH = float(mp.pi * T1)
ELL_MAX = 40


def beta_bump_np(u: np.ndarray) -> np.ndarray:
    out = np.zeros_like(u, dtype=float)
    mask = np.abs(u) < 1
    out[mask] = np.exp(-1.0 / (1.0 - u[mask] ** 2))
    return out


def g_star_quadrature() -> tuple[np.ndarray, np.ndarray]:
    centers = np.array([1.5, 2.5, 3.5], dtype=float)
    eps = 0.20
    coeffs = np.array([1.0, -3.3409952306131084085969211508, 2.3409952306131084085969211508])
    all_t: list[np.ndarray] = []
    all_wg: list[np.ndarray] = []
    nodes, weights = np.polynomial.legendre.leggauss(MELLIN_N)
    for c, a in zip(centers, coeffs):
        t = c + eps * nodes
        w = eps * weights
        G = a * beta_bump_np((t - c) / eps)
        all_t.append(t)
        all_wg.append(w * G)
    return np.concatenate(all_t), np.concatenate(all_wg)


def mellin_g_star(s: np.ndarray) -> np.ndarray:
    t, wg = g_star_quadrature()
    logt = np.log(t)
    return np.exp(-np.outer(s, logt)) @ wg


def normalize_pswfs(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    psi = np.zeros((N_PSWF, len(x)), dtype=float)
    for n in range(N_PSWF):
        vals = np.array([float(pro_ang1(0, n, BANDWIDTH, float(xx))[0]) for xx in x], dtype=float)
        norm = math.sqrt(float(np.sum(w * vals * vals)))
        if norm == 0 or not math.isfinite(norm):
            raise RuntimeError(f"bad PSWF norm for n={n}")
        psi[n, :] = vals / norm
    return psi


def bergman_R_derivative(R: mp.mpf, p: int, k: int) -> mp.mpf:
    """d^k/dR^k of Step 372 corrected local model.

    B_p^{D*}(R) = R^p / (2*pi*(p-2)!) * sum_{ell>=1} ell^(p-1) exp(-R*ell).
    """
    total = mp.mpf("0")
    pref = 1 / (2 * mp.pi * mp.factorial(p - 2))
    for ell_i in range(1, ELL_MAX + 1):
        ell = mp.mpf(ell_i)
        inner = mp.mpf("0")
        for a in range(0, min(k, p) + 1):
            falling = mp.factorial(p) / mp.factorial(p - a)
            inner += mp.binomial(k, a) * falling * (R ** (p - a)) * ((-ell) ** (k - a))
        total += (ell ** (p - 1)) * mp.e ** (-R * ell) * inner
    return pref * total


def eta_kernel_values(x: np.ndarray, k: int) -> np.ndarray:
    p = k + 2
    vals = []
    for xx in x:
        Tloc = T1 + mp.mpf(str(HEIGHT_WINDOW * float(xx)))
        R = 4 * mp.pi * Tloc
        dR = bergman_R_derivative(R, p, k)
        vals.append(complex((2 * mp.pi * 1j) ** k * complex(dR)))
    return np.array(vals, dtype=complex)


def sinc_project(eta: np.ndarray, x: np.ndarray, w: np.ndarray) -> np.ndarray:
    diff = x[:, None] - x[None, :]
    kernel = np.empty_like(diff, dtype=float)
    mask = np.abs(diff) < 1e-14
    kernel[mask] = BANDWIDTH / math.pi
    kernel[~mask] = np.sin(BANDWIDTH * diff[~mask]) / (math.pi * diff[~mask])
    return kernel @ (w * eta)


def fit_gamma(k_values: list[int], abs_values: list[float]) -> tuple[float, float]:
    # Three k-values are available, so use the two-parameter linear-in-k form.
    y = np.log(np.maximum(np.array(abs_values, dtype=float), 1e-300))
    X = np.column_stack([np.ones(len(k_values)), -np.array(k_values, dtype=float)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    rmse = float(np.sqrt(np.mean((pred - y) ** 2)))
    return float(beta[1]), rmse


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    mp.mp.dps = DPS
    ART.mkdir(parents=True, exist_ok=True)

    x, w = np.polynomial.legendre.leggauss(QUAD_N)
    psi = normalize_pswfs(x, w)

    T_offsets = np.array([float(T1) + HEIGHT_WINDOW * xx for xx in x])
    s_grid = 0.5 + 1j * T_offsets
    zeta_vals = np.array([complex(mp.zeta(mp.mpc(0.5, float(t)))) for t in T_offsets], dtype=complex)
    F_vals = zeta_vals * mellin_g_star(s_grid)

    D = np.array([np.sum(w * F_vals * np.conjugate(psi[n, :])) for n in range(N_PSWF)])

    d_rows = []
    for n, val in enumerate(D):
        d_rows.append({
            "n": n,
            "lambda_bandwidth_c": f"{BANDWIDTH:.17g}",
            "D_n_real": f"{val.real:.17e}",
            "D_n_imag": f"{val.imag:.17e}",
            "abs_D_n": f"{abs(val):.17e}",
            "normalization": "PSWF L2[-1,1] normalized by 256-node Gauss-Legendre quadrature",
            "transport_status": "standard_coordinate_proxy_not_U_infty_transport",
        })

    c_rows = []
    component_rows = []
    L_abs: list[float] = []
    for k in K_VALUES:
        eta = eta_kernel_values(x, k)
        P_eta = sinc_project(eta, x, w)
        A_k = np.sum(w * F_vals * np.conjugate(eta))
        B_k = np.sum(w * F_vals * np.conjugate(P_eta))

        c = np.array([np.sum(w * eta * np.conjugate(psi[n, :])) for n in range(N_PSWF)])
        pswf_sum = np.sum(D * np.conjugate(c))
        L_proj = A_k - B_k - pswf_sum
        L_abs.append(float(abs(L_proj)))

        for n, val in enumerate(c):
            c_rows.append({
                "rho_label": RHO_LABEL,
                "T": mp.nstr(T1, 30),
                "k": k,
                "n": n,
                "lambda_bandwidth_c": f"{BANDWIDTH:.17g}",
                "c_n_k_real": f"{val.real:.17e}",
                "c_n_k_imag": f"{val.imag:.17e}",
                "abs_c_n_k": f"{abs(val):.17e}",
                "kernel_model": "Auvray-Ma-Marinescu punctured-disc B_p proxy with p=k+2",
                "transport_status": "standard_coordinate_proxy_not_U_infty_transport",
            })

        component_rows.append({
            "rho_label": RHO_LABEL,
            "T": mp.nstr(T1, 30),
            "k": k,
            "A_k_real": f"{A_k.real:.17e}",
            "A_k_imag": f"{A_k.imag:.17e}",
            "B_k_real": f"{B_k.real:.17e}",
            "B_k_imag": f"{B_k.imag:.17e}",
            "pswf_sum_real": f"{pswf_sum.real:.17e}",
            "pswf_sum_imag": f"{pswf_sum.imag:.17e}",
            "L_projected_real": f"{L_proj.real:.17e}",
            "L_projected_imag": f"{L_proj.imag:.17e}",
            "abs_L_projected": f"{abs(L_proj):.17e}",
        })

    gamma, fit_rmse = fit_gamma(K_VALUES, L_abs)
    gamma_struct = float(mp.pi / (T1 * mp.log(T1 / (2 * mp.pi))))
    rel_err = abs(gamma - gamma_struct) / abs(gamma_struct)

    write_csv(ART / "D_n_step387.csv", d_rows)
    write_csv(ART / "c_n_k_rho1_step387.csv", c_rows)
    write_csv(ART / "L_projected_components_step387.csv", component_rows)

    verdict = (
        "proxy_mismatch_structural_law_not_reproduced"
        if rel_err > 0.20
        else "proxy_reproduces_structural_law_within_20_percent"
    )
    md = [
        "# Step 387 Projected Gamma at rho_1",
        "",
        "## Implementation",
        "- PSWFs: `scipy.special.pro_ang1(0,n,c,x)` with `c=pi*T_1`, normalized on 256 Gauss-Legendre nodes over `[-1,1]`.",
        "- Kernel: Auvray-Ma-Marinescu punctured-disc proxy `B_p^{D*}(R)=R^p/(2*pi*(p-2)!)*sum ell^(p-1) exp(-R ell)` with `p=k+2`.",
        "- Coordinate: standard local PSWF coordinate with height window `1/(2*pi)`; exact `U_infty` Sonine/Mellin transport is not applied.",
        "",
        "## Components",
    ]
    for row in component_rows:
        md.append(f"- k={row['k']}: |L_projected_proxy|={row['abs_L_projected']}")
    md += [
        "",
        f"Fitted proxy gamma from `log|L|=a-gamma*k`: `{gamma:.17e}`.",
        f"Fit RMSE in log-space: `{fit_rmse:.17e}`.",
        f"Structural comparator `pi/(T_1 log(T_1/(2pi)))`: `{gamma_struct:.17e}`.",
        f"Relative error: `{rel_err:.17e}`.",
        "",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "projected_gamma_rho1_step387.md").write_text("\n".join(md) + "\n")

    summary = [
        "# Step 387 Results Summary",
        "",
        "Implemented the requested missing PSWF evaluator path at proxy level.",
        "",
        "Citations from inherited records used verbatim:",
        "- Step 173: `K_infty^op = delta - sinc - sum_n Psi_n Psi_n^*`.",
        "- Step 173 TODO path: `T174_3 numerical_PSWF_implementation` and `T174_4 evaluator_pairings`.",
        "- Step 372: `B_p^{D*}(R) = R^p/[2*pi*(p-2)!] * sum_{ell>=1} ell^(p-1) exp(-R ell)`.",
        "- Step 386: blocked at missing `Psi_n^lambda`, `D_n`, and `c_{n,k}(rho)` evaluators.",
        "",
        f"Computed `c_n,k(rho_1)` cells: `{len(c_rows)}`.",
        f"Computed `D_n` cells: `{len(d_rows)}`.",
        f"Proxy gamma: `{gamma:.17e}`.",
        f"Structural comparator: `{gamma_struct:.17e}`.",
        f"Relative error: `{rel_err:.17e}`.",
        "",
        "The implementation replaces the purely blocked Step 386 artifact with a concrete numerical proxy, but it does not close the exact cascade problem because the inherited `U_infty` transport is still absent.",
        f"Verdict: `{verdict}`.",
    ]
    (ART / "step387_results_summary.md").write_text("\n".join(summary) + "\n")

    schema = {
        "step": 387,
        "mode": "ATTEMPT",
        "artifact_dir": str(ART),
        "pswf_backend": "scipy.special.pro_ang1",
        "mpmath_dps": DPS,
        "rho": RHO_LABEL,
        "T": mp.nstr(T1, 30),
        "bandwidth_c": BANDWIDTH,
        "quad_nodes": QUAD_N,
        "mellin_nodes_per_bump": MELLIN_N,
        "k_values": K_VALUES,
        "n_values": list(range(N_PSWF)),
        "c_cells": len(c_rows),
        "D_cells": len(d_rows),
        "gamma_projected_proxy": gamma,
        "gamma_struct": gamma_struct,
        "relative_error": rel_err,
        "verdict": verdict,
        "known_approximation": "standard_coordinate_proxy_not_exact_U_infty_transport",
    }
    (ART / "step387_schema.json").write_text(json.dumps(schema, indent=2) + "\n")

    (ART / "nonclaim_boundary_step387.md").write_text(
        "# Nonclaim Boundary - Step 387\n\n"
        "No RH claim is made. This is a numerical proxy implementation of the "
        "PSWF evaluator path, not an exact Burnol/Sonine `U_infty` transported "
        "projector computation. A mismatch against the structural law is not a "
        "disproof of that law; it identifies the remaining transport-normalization "
        "gap.\n"
    )

    print(f"gamma_proxy={gamma:.17e}")
    print(f"gamma_struct={gamma_struct:.17e}")
    print(f"rel_err={rel_err:.17e}")
    print(verdict)


if __name__ == "__main__":
    main()
