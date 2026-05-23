#!/usr/bin/env python3
"""Step 217 Gaussian wavepacket Weyl test for C_l P_infty."""

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
BASE = ROOT / "anti_loc/thread/steps/step217_branch_A_wavepacket_weyl_artifacts"
STEP215_SCRIPT = ROOT / "anti_loc/thread/steps/step215_branch_A_weyl_extended_artifacts/compute_weyl_extended_step215.py"

N_PACKETS = 10
N_GRID = 1200
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


def grid_for_spacing(spacing: float) -> tuple[np.ndarray, np.ndarray]:
    tmax = spacing * N_PACKETS + 4.0 * 2.0 + 60.0
    tmin = -60.0
    x, w = leggauss(N_GRID)
    tau = 0.5 * (tmax - tmin) * x + 0.5 * (tmax + tmin)
    weights = 0.5 * (tmax - tmin) * w
    return tau, weights


def l2_inner(f: np.ndarray, g: np.ndarray, weights: np.ndarray) -> complex:
    return complex(np.sum(weights * np.conjugate(f) * g) / (2.0 * math.pi))


def l2_norm(f: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(max(0.0, l2_inner(f, f, weights).real))


def packet(tau: np.ndarray, weights: np.ndarray, center: float, sigma: float) -> np.ndarray:
    z = np.exp(-((tau - center) ** 2) / (2.0 * sigma * sigma))
    z[np.abs(tau - center) > 3.0 * sigma] = 0.0
    nrm = l2_norm(z.astype(np.complex128), weights)
    return (z / max(nrm, 1e-300)).astype(np.complex128)


def c_action(f: np.ndarray, tau: np.ndarray, weights: np.ndarray, psis: np.ndarray, mod, ell: float) -> np.ndarray:
    pk = mod.p_operator(f, tau, weights, psis)
    phase = np.exp(1j * ell * tau)
    return phase * pk - mod.p_operator(phase * pk, tau, weights, psis)


def run_case(spacing: float, sigma: float, ell: float, label: str, primary: bool = False):
    mod = load_step215_module()
    # Reuse the Step 215 PSWF count, but allow the larger tau grid.
    old_terms = getattr(mod, "N_PSWF_TERMS", N_PSWF_TERMS)
    mod.N_PSWF_TERMS = N_PSWF_TERMS
    tau, weights = grid_for_spacing(spacing)
    psis = mod.build_psi_matrix(tau, n_terms=N_PSWF_TERMS)

    centers = [spacing * n for n in range(1, N_PACKETS + 1)]
    packets = [packet(tau, weights, c, sigma) for c in centers]
    norms = [l2_norm(c_action(u, tau, weights, psis, mod, ell), weights) for u in packets]

    pair_rows = []
    max_pair = 0.0
    for i in range(N_PACKETS):
        for j in range(i + 1, N_PACKETS):
            ip = l2_inner(packets[i], packets[j], weights)
            max_pair = max(max_pair, abs(ip))
            if primary:
                pair_rows.append(
                    {
                        "i": i + 1,
                        "j": j + 1,
                        "center_i": f"{centers[i]:.8f}",
                        "center_j": f"{centers[j]:.8f}",
                        "inner_real": f"{ip.real:.17e}",
                        "inner_imag": f"{ip.imag:.17e}",
                        "inner_abs": f"{abs(ip):.17e}",
                        "analytic_bound": f"{math.exp(-((centers[j]-centers[i])**2)/(4*sigma*sigma)):.17e}",
                    }
                )

    if primary:
        rows = []
        for idx, (center, val) in enumerate(zip(centers, norms, strict=True), start=1):
            rows.append(
                {
                    "n": idx,
                    "T_n": f"{center:.8f}",
                    "sigma": f"{sigma:.8f}",
                    "ell": f"{ell:.17e}",
                    "C_l_u_n_norm": f"{val:.17e}",
                    "error_bound": f"{ERROR:.1e}",
                    "status": "finite_wavepacket_C_l_P_infty_test",
                }
            )
        with (BASE / "wavepacket_step217.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        with (BASE / "weak_null_pairwise_step217.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(pair_rows[0].keys()))
            writer.writeheader()
            writer.writerows(pair_rows)

    mod.N_PSWF_TERMS = old_terms
    return {
        "case": label,
        "spacing": spacing,
        "sigma": sigma,
        "ell": ell,
        "min_norm": min(norms),
        "max_norm": max(norms),
        "first_norm": norms[0],
        "last_norm": norms[-1],
        "max_pairwise_overlap": max_pair,
        "trend": "bounded_below" if min(norms) - ERROR > 0.1 else "near_zero_or_uncertain",
        "norms": norms,
    }


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    ell_log2 = math.log(2.0)
    cases = [
        run_case(30.0, 1.0, ell_log2, "primary_spacing30_sigma1_log2", primary=True),
        run_case(30.0, 0.5, ell_log2, "sigma0.5"),
        run_case(30.0, 2.0, ell_log2, "sigma2.0"),
        run_case(30.0, 1.0, math.log(3.0), "ell_log3"),
        run_case(30.0, 1.0, 1.0, "ell_1.0"),
        run_case(10.0, 1.0, ell_log2, "spacing10"),
        run_case(50.0, 1.0, ell_log2, "spacing50"),
    ]

    primary = cases[0]
    norms = primary["norms"]
    tail = norms[5:]
    lower = max(0.0, min(norms) - ERROR)
    tail_lower = max(0.0, min(tail) - ERROR)
    if primary["max_pairwise_overlap"] < 1e-3 and lower > 0.1:
        verdict = "V_wavepacket_essential_obstruction"
    elif norms[-1] < norms[0] / 5.0:
        verdict = "V_wavepacket_decay_to_zero"
    else:
        verdict = "V_wavepacket_inconclusive"

    with (BASE / "trend_step217.csv").open("w", newline="") as f:
        fieldnames = [
            "min_norm",
            "lower_after_error",
            "tail_min_n6_10",
            "tail_lower_after_error",
            "first_norm",
            "last_norm",
            "weak_null_max_pairwise_overlap",
            "trend",
            "verdict",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "min_norm": f"{min(norms):.17e}",
                "lower_after_error": f"{lower:.17e}",
                "tail_min_n6_10": f"{min(tail):.17e}",
                "tail_lower_after_error": f"{tail_lower:.17e}",
                "first_norm": f"{norms[0]:.17e}",
                "last_norm": f"{norms[-1]:.17e}",
                "weak_null_max_pairwise_overlap": f"{primary['max_pairwise_overlap']:.17e}",
                "trend": primary["trend"],
                "verdict": verdict,
                "notes": "Wavepacket test is for C_l P_infty, not C_l P_eta.",
            }
        )

    robustness_rows = []
    for case in cases:
        robustness_rows.append(
            {
                "case": case["case"],
                "spacing": f"{case['spacing']:.8f}",
                "sigma": f"{case['sigma']:.8f}",
                "ell": f"{case['ell']:.17e}",
                "min_norm": f"{case['min_norm']:.17e}",
                "max_norm": f"{case['max_norm']:.17e}",
                "last_norm": f"{case['last_norm']:.17e}",
                "max_pairwise_overlap": f"{case['max_pairwise_overlap']:.17e}",
                "trend": case["trend"],
            }
        )
    with (BASE / "robustness_step217.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_rows)

    with (BASE / "compute_wavepacket_output_step217.txt").open("w") as f:
        f.write("Step 217 wavepacket Weyl test\n")
        for i, val in enumerate(norms, start=1):
            f.write(f"n={i:02d} T={30*i:.1f} sigma=1.0 norm={val:.17e}\n")
        f.write(f"max_pairwise_overlap={primary['max_pairwise_overlap']:.17e}\n")
        f.write(f"lower_after_error={lower:.17e}\n")
        f.write(f"tail_lower_after_error={tail_lower:.17e}\n")
        f.write(f"verdict={verdict}\n")

    print((BASE / "compute_wavepacket_output_step217.txt").read_text())


if __name__ == "__main__":
    main()
