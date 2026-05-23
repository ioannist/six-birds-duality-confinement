#!/usr/bin/env python3
"""Step 214 finite-grid Weyl sequence diagnostic.

Weyl vectors:
    u_n = kappa_{rho_n}/||kappa_{rho_n}||

Here kappa is sampled by the Burnol-boundary kernel candidate
K_{1/2}^Gamma(1/2+i tau,rho_n), the same model tested in Steps 205/207/208.
This is a diagnostic for the Branch A Weyl attack, not a proof of the
transport-sampling theorem.
"""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


mp.mp.dps = 60

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step214_branch_A_weyl_sequence_artifacts"
STEP202_SCRIPT = ROOT / "anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/compute_E_half_step202.py"

T_MAX = 80.0
N_GRID = 120
N_ZEROS = 10
N_PSWF_EIGEN = 280
N_PSWF_MAIN = 24
ELL_MAIN = math.log(2.0)
LAMBDA = 1.0


def load_step202_module():
    spec = importlib.util.spec_from_file_location("step202_E", STEP202_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step202 E module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step202_E"] = mod
    spec.loader.exec_module(mod)
    return mod


def sinc_kernel(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-12
    out[mask] = LAMBDA / math.pi
    out[~mask] = np.sin(LAMBDA * arr[~mask]) / (math.pi * arr[~mask])
    if np.isscalar(x):
        return float(out)
    return out


def pswf_eigensystem(n_nodes: int = N_PSWF_EIGEN):
    x, w = leggauss(n_nodes)
    sw = np.sqrt(w)
    d = x[:, None] - x[None, :]
    k = sinc_kernel(d)
    mat = sw[:, None] * k * sw[None, :]
    vals, vecs = np.linalg.eigh(mat)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    phi = vecs / sw[:, None]
    return x, w, vals, phi


def psi_from_phi(tau: np.ndarray, x_nodes: np.ndarray, weights: np.ndarray, mu: float, phi_values: np.ndarray) -> np.ndarray:
    d = tau[:, None] - x_nodes[None, :]
    int_k = sinc_kernel(d).dot(weights * phi_values)
    inside = np.abs(tau) <= LAMBDA
    psi = np.empty_like(int_k, dtype=np.complex128)
    psi[~inside] = -int_k[~inside] / math.sqrt(max(1e-300, 1.0 - mu))
    psi[inside] = (math.sqrt(max(1e-300, 1.0 - mu)) / mu) * int_k[inside]
    return psi


def build_psi_matrix(tau: np.ndarray, n_terms: int) -> np.ndarray:
    x, w, vals, phi = pswf_eigensystem()
    return np.array(
        [psi_from_phi(tau, x, w, float(vals[n]), phi[:, n]) for n in range(n_terms)],
        dtype=np.complex128,
    )


def p_operator(f: np.ndarray, tau: np.ndarray, weights: np.ndarray, psis: np.ndarray) -> np.ndarray:
    sinc_part = sinc_kernel(tau[:, None] - tau[None, :]).dot(weights * f)
    pswf_part = np.zeros_like(f, dtype=np.complex128)
    for psi in psis:
        inner = np.sum(weights * np.conjugate(psi) * f)
        pswf_part += psi * inner
    return f - sinc_part - pswf_part


def l2_norm(f: np.ndarray, weights: np.ndarray) -> float:
    return float(math.sqrt(max(0.0, np.sum(weights * np.abs(f) ** 2).real / (2.0 * math.pi))))


@dataclass
class WeylResult:
    n: int
    gamma: float
    kappa_norm: float
    c_norm: float


def compute_operator_norms(kappas: dict[int, np.ndarray], tau: np.ndarray, weights: np.ndarray, n_terms: int, ell: float) -> dict[int, float]:
    psis = build_psi_matrix(tau, n_terms)
    phase = np.exp(1j * ell * tau)
    out = {}
    for n, kappa in kappas.items():
        pk = p_operator(kappa, tau, weights, psis)
        h = phase * pk - p_operator(phase * pk, tau, weights, psis)
        out[n] = l2_norm(h, weights) / max(l2_norm(kappa, weights), 1e-300)
    return out


def compute_kappas() -> tuple[np.ndarray, np.ndarray, dict[int, float], dict[int, np.ndarray], dict[int, float]]:
    mod = load_step202_module()
    data = mod.build_resolvent(100)
    raw_x, raw_w = leggauss(N_GRID)
    tau = T_MAX * raw_x
    weights = T_MAX * raw_w

    e_grid = []
    for tv in tau:
        s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(float(tv))))
        val, _, _ = mod.e_lambda(s, data)
        e_grid.append(complex(val))
    e_grid = np.array(e_grid, dtype=np.complex128)
    e_1_minus_grid = np.conjugate(e_grid)

    gammas: dict[int, float] = {}
    e_rho: dict[int, complex] = {}
    kappas: dict[int, np.ndarray] = {}
    kappa_norms: dict[int, float] = {}
    for n in range(1, N_ZEROS + 1):
        rho = mp.zetazero(n)
        gamma = float(mp.im(rho))
        gammas[n] = gamma
        val, _, _ = mod.e_lambda(rho, data)
        e_rho[n] = complex(val)
        e_1_minus_rho = np.conjugate(e_rho[n])
        s_grid = 0.5 + 1j * tau
        rho_c = 0.5 + 1j * gamma
        kappa = (e_grid * e_rho[n] - e_1_minus_grid * e_1_minus_rho) / (s_grid + rho_c - 1.0)
        kappas[n] = kappa
        kappa_norms[n] = l2_norm(kappa, weights)
    return tau, weights, gammas, kappas, kappa_norms


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    tau, weights, gammas, kappas, kappa_norms = compute_kappas()
    main_norms = compute_operator_norms(kappas, tau, weights, N_PSWF_MAIN, ELL_MAIN)

    # Robustness: PSWF terms and ell values.  Error is max deviation at fixed ell
    # over PSWF terms; ell variants are reported separately.
    pswf_variants = {terms: compute_operator_norms(kappas, tau, weights, terms, ELL_MAIN) for terms in [12, 24, 36]}
    ell_variants = {
        "log2": main_norms,
        "log3": compute_operator_norms(kappas, tau, weights, N_PSWF_MAIN, math.log(3.0)),
        "1.0": compute_operator_norms(kappas, tau, weights, N_PSWF_MAIN, 1.0),
    }

    rows = []
    for n in range(1, N_ZEROS + 1):
        # PSWF truncation variation is tiny in this finite-grid model.  Add a
        # conservative absolute discretization floor to reflect finite tau
        # cutoff, approximate E_lambda values, and the unresolved transport
        # theorem.
        err = max(abs(pswf_variants[t][n] - main_norms[n]) for t in [12, 24, 36]) + 5.0e-2
        rows.append(
            {
                "n": n,
                "gamma_n": f"{gammas[n]:.15f}",
                "kappa_norm": f"{kappa_norms[n]:.17e}",
                "C_l_u_n_norm": f"{main_norms[n]:.17e}",
                "error_bound": f"{err:.17e}",
                "status": "diagnostic_Burnol_boundary_kappa_finite_grid",
            }
        )
    with (BASE / "weyl_sequence_step214.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    vals = np.array([main_norms[n] for n in range(1, N_ZEROS + 1)])
    errs = np.array([float(r["error_bound"]) for r in rows])
    liminf = float(np.min(vals))
    lower = float(max(0.0, np.min(vals - errs)))
    if lower > 1e-6:
        verdict = "V_branch_A_weyl_essential_obstruction"
        pattern = "bounded_below"
    elif vals[-1] < vals[0] and vals[-1] < 1e-6:
        verdict = "V_branch_A_weyl_consistent_with_compact"
        pattern = "small_or_decaying"
    else:
        verdict = "V_branch_A_weyl_inconclusive"
        pattern = "precision_or_pattern_limited"

    with (BASE / "lim_inf_analysis_step214.csv").open("w", newline="") as f:
        fieldnames = ["N", "lim_inf_estimate", "lower_bound_after_error", "pattern", "verdict", "notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "N": N_ZEROS,
                "lim_inf_estimate": f"{liminf:.17e}",
                "lower_bound_after_error": f"{lower:.17e}",
                "pattern": pattern,
                "verdict": verdict,
                "notes": "Finite-grid diagnostic using CAND1/Burnol-boundary kappa; does not prove compactness/noncompactness.",
            }
        )

    robustness_rows = []
    for terms, data in pswf_variants.items():
        robustness_rows.append(
            {
                "test": "N_PSWF",
                "parameter": terms,
                "ell": "log2",
                "min_norm": f"{min(data.values()):.17e}",
                "max_norm": f"{max(data.values()):.17e}",
                "status": "computed",
            }
        )
    for label, data in ell_variants.items():
        robustness_rows.append(
            {
                "test": "ell",
                "parameter": label,
                "ell": label,
                "min_norm": f"{min(data.values()):.17e}",
                "max_norm": f"{max(data.values()):.17e}",
                "status": "computed",
            }
        )
    with (BASE / "robustness_step214.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_rows)

    print("Step 214 Weyl diagnostic")
    print(f"N={N_ZEROS}, tau_grid={N_GRID}, T_MAX={T_MAX}, N_PSWF={N_PSWF_MAIN}")
    for n in range(1, N_ZEROS + 1):
        print(f"n={n:02d} gamma={gammas[n]:.6f} ||kappa||={kappa_norms[n]:.6e} ||C u||={main_norms[n]:.6e}")
    print(f"liminf_estimate={liminf:.8e}, lower_after_error={lower:.8e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
