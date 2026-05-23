#!/usr/bin/env python3
"""Derive the k=1 Burnol reproducing-kernel anti-holomorphic derivative."""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step247_branch_C_k1_proper_artifacts")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "object": "Burnol kernel",
            "formula": "K_a^Gamma(z,w)=(E(z) Ebar(w)-E(1-z) Ebar(1-w))/(z+w-1)",
            "status": "inherited Burnol 2002 eq. 1 convention",
        },
        {
            "object": "E_lambda",
            "formula": "E_lambda(w)=pi^(-w/2) Gamma(w/2) [lambda^(1/2-w)+(sqrt(lambda)/2) int_lambda^infty (psi_+-psi_-)(t)t^(-w)dt]",
            "status": "Burnol 2002 Theorem 8 formula used symbolically",
        },
        {
            "object": "E_lambda_prime",
            "formula": "E'(w)=P'(w)B(w)+P(w)B'(w), P'/P=-0.5 log(pi)+0.5 digamma(w/2), B'=-log(lambda)lambda^(1/2-w)-(sqrt(lambda)/2) int psi_diff(t)t^(-w)log(t)dt",
            "status": "analytic derivative of Theorem 8 expression",
        },
        {
            "object": "anti_holomorphic_kernel_derivative",
            "formula": "partial_wbar K(z,w)=[E(z) conj(E'(w))+E(1-z) conj(E'(1-w))]/(z+w-1)",
            "status": "denominator derivative is zero under the inherited z+w-1 convention; sign comes from partial_wbar conj(E(1-w))=-conj(E'(1-w))",
        },
        {
            "object": "Branch_C_operational_pairing",
            "formula": "L_{rho,1}(G)=<M_zeta G,P_infty y_{rho,1}> = -i d/dgamma [(P_infty M_zeta G)(1/2+i gamma)]_{gamma=Im rho}",
            "status": "step 153 pulled-evaluator identity plus step 196 convention; step247 differentiates this expression analytically instead of finite differencing",
        },
    ]
    with (BASE / "k1_kernel_derivation_step247.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "derive_k1_kernel_output_step247.txt").write_text(
        "\n".join(f"{r['object']}: {r['formula']}" for r in rows) + "\n"
    )
    print((BASE / "derive_k1_kernel_output_step247.txt").read_text())


if __name__ == "__main__":
    main()
