#!/usr/bin/env python3
"""Derive the k=2 Burnol reproducing-kernel anti-holomorphic derivative."""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step249_branch_C_k2_proper_artifacts")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "object": "Burnol kernel",
            "formula": "K_a^Gamma(z,w)=(E(z) Ebar(w)-E(1-z) Ebar(1-w))/(z+w-1)",
            "status": "inherited Burnol 2002 eq. 1 convention",
        },
        {
            "object": "first derivative",
            "formula": "partial_wbar K=[E(z)conj(E'(w))+E(1-z)conj(E'(1-w))]/(z+w-1)",
            "status": "step247 formula",
        },
        {
            "object": "second derivative",
            "formula": "partial_wbar^2 K=[E(z)conj(E''(w))-E(1-z)conj(E''(1-w))]/(z+w-1)",
            "status": "corrected chain-rule sign; denominator derivative vanishes under z+w-1 convention",
        },
        {
            "object": "E_second",
            "formula": "E''=P''B+2P'B'+PB''; P''/P=0.25*polygamma(1,w/2)+(-0.5*log(pi)+0.5*digamma(w/2))^2; B''=(log(lambda))^2 lambda^(1/2-w)+(sqrt(lambda)/2) int psi_diff(t)t^(-w)(log t)^2 dt",
            "status": "analytic second derivative of Burnol 2002 Theorem 8",
        },
        {
            "object": "Branch_C_operational_pairing",
            "formula": "L_{rho,2}(G)=(-i d/dgamma)^2 [(P_infty M_zeta G)(1/2+i gamma)]_{gamma=Im rho}",
            "status": "step196/247 convention extended to k=2",
        },
    ]
    with (BASE / "k2_kernel_derivation_step249.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "derive_k2_kernel_output_step249.txt").write_text(
        "\n".join(f"{r['object']}: {r['formula']}" for r in rows) + "\n"
    )
    print((BASE / "derive_k2_kernel_output_step249.txt").read_text())


if __name__ == "__main__":
    main()
