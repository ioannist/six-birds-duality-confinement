#!/usr/bin/env python3
"""Step 246 Phi(sigma, ell) grid using the Step 217-220 wavepacket pipeline.

The numerical operator pipeline is the inherited local-window approximation:
K_infty^op = delta - sinc - PSWF, with the same 3 sigma truncated Gaussian
wavepacket convention used in steps 217-220.  mpmath is set to 100 dps for
high-precision constants and analytic comparison values; the inherited
quadrature/operator implementation is NumPy double precision, as in steps
217-220.
"""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


mp.mp.dps = 100

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step246_phi_max_analytical_refinement_artifacts"
STEP215_SCRIPT = ROOT / "anti_loc/thread/steps/step215_branch_A_weyl_extended_artifacts/compute_weyl_extended_step215.py"

T_CENTER = 10000.0
N_GRID = 1400
LOCAL_WINDOW = 80.0
N_PSWF_TERMS = 24
LAMBDA = 1.0


def load_step215_module():
    spec = importlib.util.spec_from_file_location("step215_weyl", STEP215_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step215 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step215_weyl"] = mod
    spec.loader.exec_module(mod)
    return mod


def sinc_kernel(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1e-12
    out[mask] = LAMBDA / math.pi
    out[~mask] = np.sin(LAMBDA * arr[~mask]) / (math.pi * arr[~mask])
    if np.isscalar(x):
        return float(out)
    return out


def l2_inner(f: np.ndarray, g: np.ndarray, weights: np.ndarray) -> complex:
    return complex(np.sum(weights * np.conjugate(f) * g) / (2.0 * math.pi))


def l2_norm(f: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(max(0.0, l2_inner(f, f, weights).real))


def local_grid(center: float = T_CENTER, window: float = LOCAL_WINDOW) -> tuple[np.ndarray, np.ndarray]:
    x, w = leggauss(N_GRID)
    tau = center + window * x
    weights = window * w
    return tau, weights


def packet(tau: np.ndarray, weights: np.ndarray, center: float, sigma: float) -> np.ndarray:
    z = np.exp(-((tau - center) ** 2) / (2.0 * sigma * sigma))
    z[np.abs(tau - center) > 3.0 * sigma] = 0.0
    nrm = l2_norm(z.astype(np.complex128), weights)
    return (z / max(nrm, 1e-300)).astype(np.complex128)


def make_p_operator(tau: np.ndarray, weights: np.ndarray, psis: np.ndarray):
    sinc_mat = sinc_kernel(tau[:, None] - tau[None, :])
    psi_conj = np.conjugate(psis)

    def p_operator(f: np.ndarray) -> np.ndarray:
        sinc_part = sinc_mat.dot(weights * f)
        inner = psi_conj.dot(weights * f)
        pswf_part = psis.T.dot(inner)
        return f - sinc_part - pswf_part

    return p_operator


def band_shift_model(sigma: float, ell: float) -> mp.mpf:
    """Untruncated-Gaussian high-pass/low-pass overlap model.

    For 0 <= ell <= 2, this is sqrt(1/2 [erf(sigma(1+ell))-erf(sigma)]).
    For ell >= 2, the overlap band is [ell-1, ell+1].
    """
    s = mp.mpf(str(sigma))
    e = mp.mpf(str(ell))
    if e <= 2:
        val2 = mp.mpf("0.5") * (mp.erf(s * (1 + e)) - mp.erf(s))
    else:
        val2 = mp.mpf("0.5") * (mp.erf(s * (1 + e)) - mp.erf(s * (e - 1)))
    return mp.sqrt(max(mp.mpf("0"), val2))


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    mod = load_step215_module()
    tau, weights = local_grid()
    psis = mod.build_psi_matrix(tau, n_terms=N_PSWF_TERMS)
    p_operator = make_p_operator(tau, weights, psis)

    sigmas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    ell_cases = [
        ("0.5", 0.5),
        ("log2", float(mp.log(2))),
        ("1.0", 1.0),
        ("log3", float(mp.log(3))),
        ("1.5", 1.5),
        ("log5", float(mp.log(5))),
        ("2.0", 2.0),
        ("log10/4", float(mp.log(10) / 4)),
        ("2.5", 2.5),
    ]

    rows = []
    for sigma in sigmas:
        u = packet(tau, weights, T_CENTER, sigma)
        pk = p_operator(u)
        pk_norm = l2_norm(pk, weights)
        for ell_label, ell in ell_cases:
            phase = np.exp(1j * ell * tau)
            h = phase * pk - p_operator(phase * pk)
            phi = l2_norm(h, weights)
            model = band_shift_model(sigma, ell)
            rows.append(
                {
                    "sigma": f"{sigma:.8f}",
                    "ell_label": ell_label,
                    "ell": f"{ell:.17e}",
                    "Phi": f"{phi:.17e}",
                    "band_shift_model": mp.nstr(model, 25),
                    "abs_residual_band_shift": f"{abs(phi - float(model)):.17e}",
                    "P_u_norm": f"{pk_norm:.17e}",
                    "T": f"{T_CENTER:.8f}",
                    "mpmath_dps": "100",
                    "quadrature": f"GL{N_GRID}_double_local_window",
                    "pswf_terms": str(N_PSWF_TERMS),
                }
            )
        print(f"sigma={sigma:.2f} complete")

    with (BASE / "phi_grid_step246.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    best = max(rows, key=lambda r: float(r["Phi"]))
    max_resid = max(float(r["abs_residual_band_shift"]) for r in rows)
    rmse = math.sqrt(sum(float(r["abs_residual_band_shift"]) ** 2 for r in rows) / len(rows))
    with (BASE / "compute_phi_grid_output_step246.txt").open("w") as f:
        f.write("Step 246 Phi grid complete\n")
        f.write(f"grid_size={len(rows)}\n")
        f.write(f"best_grid={best}\n")
        f.write(f"band_shift_rmse={rmse:.17e}\n")
        f.write(f"band_shift_max_abs={max_resid:.17e}\n")

    print((BASE / "compute_phi_grid_output_step246.txt").read_text())


if __name__ == "__main__":
    main()
