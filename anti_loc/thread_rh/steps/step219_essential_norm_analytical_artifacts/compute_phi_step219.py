#!/usr/bin/env python3
"""Compute Phi(sigma, ell) values for Step 219."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import mpmath as mp


mp.mp.dps = 80

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step219_essential_norm_analytical_artifacts"
STEP218_SCRIPT = ROOT / "anti_loc/thread/steps/step218_wavepacket_extended_large_T_artifacts/compute_wavepacket_large_T_step218.py"


def load_step218_module():
    spec = importlib.util.spec_from_file_location("step218_large_T", STEP218_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step218 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step218_large_T"] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    mod = load_step218_module()

    ell_cases = [
        ("0.1", 0.1),
        ("0.25", 0.25),
        ("0.5", 0.5),
        ("log2", math.log(2.0)),
        ("log3", math.log(3.0)),
        ("1.0", 1.0),
        ("log5", math.log(5.0)),
        ("pi/2", math.pi / 2.0),
        ("log7", math.log(7.0)),
        ("log10", math.log(10.0)),
        ("2.0", 2.0),
        ("5.0", 5.0),
    ]
    sigma_cases = [0.25, 0.5, 1.0, 2.0, 5.0]

    rows = []
    for label, ell in ell_cases:
        val = mod.norm_at_T(10000.0, sigma=1.0, ell=ell)
        rows.append(
            {
                "sweep": "ell",
                "sigma": "1.00000000",
                "ell_label": label,
                "ell": f"{ell:.17e}",
                "Phi": f"{val:.17e}",
                "error_bound": "7.5e-2",
                "T": "10000.00000000",
            }
        )
        print(f"ell {label:>5} {ell:.10f} Phi={val:.17e}")

    ell_log2 = math.log(2.0)
    for sigma in sigma_cases:
        val = mod.norm_at_T(10000.0, sigma=sigma, ell=ell_log2)
        rows.append(
            {
                "sweep": "sigma",
                "sigma": f"{sigma:.8f}",
                "ell_label": "log2",
                "ell": f"{ell_log2:.17e}",
                "Phi": f"{val:.17e}",
                "error_bound": "7.5e-2",
                "T": "10000.00000000",
            }
        )
        print(f"sigma {sigma:.2f} ell=log2 Phi={val:.17e}")

    with (BASE / "phi_values_step219.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with (BASE / "compute_phi_output_step219.txt").open("w") as f:
        f.write("Step 219 Phi values\n")
        for r in rows:
            f.write(
                f"{r['sweep']} sigma={r['sigma']} ell={r['ell_label']} "
                f"Phi={r['Phi']}\n"
            )


if __name__ == "__main__":
    main()
