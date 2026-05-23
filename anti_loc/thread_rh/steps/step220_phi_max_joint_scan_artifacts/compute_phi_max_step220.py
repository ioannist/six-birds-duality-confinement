#!/usr/bin/env python3
"""Step 220 joint scan for Phi_max over Gaussian wavepacket parameters."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import mpmath as mp


mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step220_phi_max_joint_scan_artifacts"
STEP218_SCRIPT = ROOT / "anti_loc/thread/steps/step218_wavepacket_extended_large_T_artifacts/compute_wavepacket_large_T_step218.py"

ERROR = 7.5e-2


def load_step218_module():
    spec = importlib.util.spec_from_file_location("step218_large_T", STEP218_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step218 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step218_large_T"] = mod
    spec.loader.exec_module(mod)
    return mod


def compute(mod, sigma: float, ell: float, T: float = 10000.0, pswf_terms: int = 24, dps: int = 80) -> float:
    old_terms = mod.N_PSWF_TERMS
    old_dps = mp.mp.dps
    mod.N_PSWF_TERMS = pswf_terms
    mp.mp.dps = dps
    try:
        return float(mod.norm_at_T(T, sigma=sigma, ell=ell))
    finally:
        mod.N_PSWF_TERMS = old_terms
        mp.mp.dps = old_dps


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    mod = load_step218_module()

    sigmas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5]
    ell_cases = [
        ("0.3", 0.3),
        ("0.5", 0.5),
        ("0.7", 0.7),
        ("log2", math.log(2.0)),
        ("1.0", 1.0),
        ("log3", math.log(3.0)),
        ("1.5", 1.5),
        ("pi/2", math.pi / 2.0),
        ("2.0", 2.0),
        ("2.5", 2.5),
    ]

    grid_rows = []
    for sigma in sigmas:
        for ell_label, ell in ell_cases:
            phi = compute(mod, sigma, ell)
            grid_rows.append(
                {
                    "sigma": f"{sigma:.8f}",
                    "ell_label": ell_label,
                    "ell": f"{ell:.17e}",
                    "Phi": f"{phi:.17e}",
                    "error_bound": f"{ERROR:.1e}",
                    "T": "10000.00000000",
                    "pswf_terms": "24",
                }
            )
        print(f"coarse sigma={sigma:.2f} done")

    with (BASE / "phi_grid_step220.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
        writer.writeheader()
        writer.writerows(grid_rows)

    best = max(grid_rows, key=lambda r: float(r["Phi"]))
    sigma0 = float(best["sigma"])
    ell0 = float(best["ell"])
    refined_sigmas = [max(0.05, sigma0 + 0.05 * k) for k in [-2, -1, 0, 1, 2]]
    refined_ells = [max(0.05, ell0 + 0.05 * k) for k in [-2, -1, 0, 1, 2]]
    refined_rows = []
    for sigma in refined_sigmas:
        for ell in refined_ells:
            phi = compute(mod, sigma, ell)
            refined_rows.append(
                {
                    "sigma": f"{sigma:.8f}",
                    "ell": f"{ell:.17e}",
                    "Phi": f"{phi:.17e}",
                    "error_bound": f"{ERROR:.1e}",
                    "T": "10000.00000000",
                    "pswf_terms": "24",
                }
            )

    with (BASE / "phi_max_refined_step220.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(refined_rows[0].keys()))
        writer.writeheader()
        writer.writerows(refined_rows)

    best_refined = max(refined_rows, key=lambda r: float(r["Phi"]))
    sigma_star = float(best_refined["sigma"])
    ell_star = float(best_refined["ell"])
    phi_star = float(best_refined["Phi"])
    lower = max(0.0, phi_star - ERROR)
    if phi_star >= 0.9:
        verdict = "V_phi_max_near_one"
    elif phi_star < 1.0:
        verdict = "V_phi_max_bounded_below_one"
    else:
        verdict = "V_phi_max_inconclusive"

    robustness_cases = []
    for T in [1000.0, 5000.0, 10000.0]:
        for pswf in [24, 48]:
            phi = compute(mod, sigma_star, ell_star, T=T, pswf_terms=pswf, dps=80)
            robustness_cases.append(
                {
                    "T": f"{T:.8f}",
                    "sigma": f"{sigma_star:.8f}",
                    "ell": f"{ell_star:.17e}",
                    "pswf_terms": str(pswf),
                    "dps": "80",
                    "Phi": f"{phi:.17e}",
                    "status": "robustness_T_pswf",
                }
            )
    phi_dps100 = compute(mod, sigma_star, ell_star, T=10000.0, pswf_terms=24, dps=100)
    robustness_cases.append(
        {
            "T": "10000.00000000",
            "sigma": f"{sigma_star:.8f}",
            "ell": f"{ell_star:.17e}",
            "pswf_terms": "24",
            "dps": "100",
            "Phi": f"{phi_dps100:.17e}",
            "status": "robustness_dps",
        }
    )
    with (BASE / "robustness_step220.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_cases[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_cases)

    with (BASE / "compute_phi_max_output_step220.txt").open("w") as f:
        f.write("Step 220 Phi max scan\n")
        f.write(f"coarse_best={best}\n")
        f.write(f"refined_best={best_refined}\n")
        f.write(f"lower_after_error={lower:.17e}\n")
        f.write(f"verdict={verdict}\n")
    print((BASE / "compute_phi_max_output_step220.txt").read_text())


if __name__ == "__main__":
    main()
