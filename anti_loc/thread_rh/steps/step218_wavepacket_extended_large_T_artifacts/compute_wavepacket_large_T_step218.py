#!/usr/bin/env python3
"""Step 218 large-T Gaussian wavepacket extension for C_l P_infty."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step218_wavepacket_extended_large_T_artifacts"
STEP215_SCRIPT = ROOT / "anti_loc/thread/steps/step215_branch_A_weyl_extended_artifacts/compute_weyl_extended_step215.py"

T_VALUES = [300.0, 1000.0, 3000.0, 10000.0]
N_GRID = 1400
LOCAL_WINDOW = 80.0
N_PSWF_TERMS = 24
ERROR = 7.5e-2


def load_step215_module():
    spec = importlib.util.spec_from_file_location("step215_weyl", STEP215_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step215 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step215_weyl"] = mod
    spec.loader.exec_module(mod)
    return mod


def l2_inner(f: np.ndarray, g: np.ndarray, weights: np.ndarray) -> complex:
    return complex(np.sum(weights * np.conjugate(f) * g) / (2.0 * math.pi))


def l2_norm(f: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(max(0.0, l2_inner(f, f, weights).real))


def local_grid(center: float, window: float = LOCAL_WINDOW) -> tuple[np.ndarray, np.ndarray]:
    x, w = leggauss(N_GRID)
    tau = center + window * x
    weights = window * w
    return tau, weights


def packet(tau: np.ndarray, weights: np.ndarray, center: float, sigma: float) -> np.ndarray:
    z = np.exp(-((tau - center) ** 2) / (2.0 * sigma * sigma))
    z[np.abs(tau - center) > 3.0 * sigma] = 0.0
    nrm = l2_norm(z.astype(np.complex128), weights)
    return (z / max(nrm, 1e-300)).astype(np.complex128)


def c_action(f: np.ndarray, tau: np.ndarray, weights: np.ndarray, psis: np.ndarray, mod, ell: float) -> np.ndarray:
    pk = mod.p_operator(f, tau, weights, psis)
    phase = np.exp(1j * ell * tau)
    return phase * pk - mod.p_operator(phase * pk, tau, weights, psis)


def norm_at_T(center: float, sigma: float, ell: float, window: float = LOCAL_WINDOW) -> float:
    mod = load_step215_module()
    old_terms = getattr(mod, "N_PSWF_TERMS", N_PSWF_TERMS)
    mod.N_PSWF_TERMS = N_PSWF_TERMS
    tau, weights = local_grid(center, window)
    psis = mod.build_psi_matrix(tau, n_terms=N_PSWF_TERMS)
    u = packet(tau, weights, center, sigma)
    val = l2_norm(c_action(u, tau, weights, psis, mod, ell), weights)
    mod.N_PSWF_TERMS = old_terms
    return val


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    ell_log2 = math.log(2.0)
    ell_log3 = math.log(3.0)

    primary_rows = []
    for T in T_VALUES:
        val = norm_at_T(T, sigma=1.0, ell=ell_log2)
        primary_rows.append(
            {
                "T": f"{T:.8f}",
                "sigma": "1.00000000",
                "ell": f"{ell_log2:.17e}",
                "C_l_u_T_norm": f"{val:.17e}",
                "error_bound": f"{ERROR:.1e}",
                "window": f"{LOCAL_WINDOW:.8f}",
                "status": "large_T_local_window_C_l_P_infty",
            }
        )
        print(f"T={T:.1f} sigma=1 ell=log2 norm={val:.17e}")

    with (BASE / "wavepacket_large_T_step218.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(primary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(primary_rows)

    vals = [float(r["C_l_u_T_norm"]) for r in primary_rows]
    lower = max(0.0, min(vals) - ERROR)
    drift = max(vals) - min(vals)
    ratio = vals[-1] / vals[0] if vals[0] else float("nan")
    if lower > 0.15 and drift < 0.02:
        verdict = "V_wavepacket_large_T_constant"
        trend = "flat_constant"
    elif lower > 0.1:
        verdict = "V_wavepacket_large_T_lim_inf_certified"
        trend = "bounded_below_with_drift"
    elif vals[-1] < vals[0] / 3.0:
        verdict = "V_wavepacket_large_T_slow_decay"
        trend = "decay"
    else:
        verdict = "V_wavepacket_large_T_precision_limited"
        trend = "precision_limited"

    with (BASE / "lim_inf_trend_step218.csv").open("w", newline="") as f:
        fieldnames = [
            "min_norm",
            "max_norm",
            "drift",
            "T10000_over_T300_ratio",
            "lower_after_error",
            "trend",
            "verdict",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "min_norm": f"{min(vals):.17e}",
                "max_norm": f"{max(vals):.17e}",
                "drift": f"{drift:.17e}",
                "T10000_over_T300_ratio": f"{ratio:.17e}",
                "lower_after_error": f"{lower:.17e}",
                "trend": trend,
                "verdict": verdict,
                "notes": "Large-T local-window test for C_l P_infty, not C_l P_eta.",
            }
        )

    robustness_cases = []
    for sigma in [0.5, 1.0]:
        for ell_name, ell in [("log2", ell_log2), ("log3", ell_log3)]:
            for T in [1000.0, 10000.0]:
                val = norm_at_T(T, sigma=sigma, ell=ell)
                robustness_cases.append(
                    {
                        "T": f"{T:.8f}",
                        "sigma": f"{sigma:.8f}",
                        "ell_label": ell_name,
                        "ell": f"{ell:.17e}",
                        "C_l_u_T_norm": f"{val:.17e}",
                        "window": f"{LOCAL_WINDOW:.8f}",
                        "status": "bounded_below" if val - ERROR > 0.1 else "near_zero_or_uncertain",
                    }
                )
                print(f"robust T={T:.1f} sigma={sigma} ell={ell_name} norm={val:.17e}")

    # Local window sensitivity at T=10000.
    for window in [40.0, 80.0, 120.0]:
        val = norm_at_T(10000.0, sigma=1.0, ell=ell_log2, window=window)
        robustness_cases.append(
            {
                "T": "10000.00000000",
                "sigma": "1.00000000",
                "ell_label": "log2_window_check",
                "ell": f"{ell_log2:.17e}",
                "C_l_u_T_norm": f"{val:.17e}",
                "window": f"{window:.8f}",
                "status": "window_sensitivity",
            }
        )

    with (BASE / "robustness_step218.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_cases[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_cases)

    with (BASE / "compute_wavepacket_large_T_output_step218.txt").open("w") as f:
        f.write("Step 218 large-T wavepacket test\n")
        for r in primary_rows:
            f.write(f"T={r['T']} norm={r['C_l_u_T_norm']}\n")
        f.write(f"lower_after_error={lower:.17e}\n")
        f.write(f"drift={drift:.17e}\n")
        f.write(f"ratio={ratio:.17e}\n")
        f.write(f"verdict={verdict}\n")

    print((BASE / "compute_wavepacket_large_T_output_step218.txt").read_text())


if __name__ == "__main__":
    main()
