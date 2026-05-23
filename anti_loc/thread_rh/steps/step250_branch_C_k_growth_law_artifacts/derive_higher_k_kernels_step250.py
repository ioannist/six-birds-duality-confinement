#!/usr/bin/env python3
"""Higher-k symbolic derivative pattern for Branch C."""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step250_branch_C_k_growth_law_artifacts")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "order": "general",
            "kernel_formula": "partial_wbar^k K_a^Gamma(z,w)=[E(z)conj(E^(k)(w))+(-1)^(k+1)E(1-z)conj(E^(k)(1-w))]/(z+w-1)",
            "operational_formula": "L_{rho,k}(G)=(-i d/dgamma)^k[(P_infty M_zeta G)(1/2+i gamma)]",
            "note": "denominator derivative vanishes under inherited z+w-1 convention",
        },
        {
            "order": "3",
            "kernel_formula": "partial_wbar^3 K=[E(z)conj(E'''(w))+E(1-z)conj(E'''(1-w))]/(z+w-1)",
            "operational_formula": "D^3 with D=-i d/dgamma applied to delta-sinc-PSWF expression",
            "note": "sign alternates back to plus",
        },
        {
            "order": "4",
            "kernel_formula": "partial_wbar^4 K=[E(z)conj(E''''(w))-E(1-z)conj(E''''(1-w))]/(z+w-1)",
            "operational_formula": "D^4 with D=-i d/dgamma applied to delta-sinc-PSWF expression",
            "note": "sign alternates to minus",
        },
    ]
    with (BASE / "higher_k_kernel_derivation_step250.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "derive_higher_k_kernels_output_step250.txt").write_text(
        "\n".join(f"k={r['order']}: {r['kernel_formula']}" for r in rows) + "\n"
    )
    print((BASE / "derive_higher_k_kernels_output_step250.txt").read_text())


if __name__ == "__main__":
    main()
