#!/usr/bin/env python3
"""Step 204 symbolic derivation of the unnormalized finite residual formula."""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step204_unnormalized_xi_matrix_source_artifacts")


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "stage": "finite_basis",
            "formula": "H_eta_fin=span{kappa_1,kappa_2,kappa_3}; G_ij=<kappa_i,kappa_j>",
            "conclusion": "G is the coordinate metric for the nonorthonormal basis",
            "citation": "Step162 P_eta projection onto H_eta; Step177 Rho_fin finite carrier",
        },
        {
            "stage": "orthogonal_projection",
            "formula": "P_eta x=sum_{i,j} kappa_i (G^{-1})_{ij}<kappa_j,x>",
            "conclusion": "valid if G is nonsingular and the Hilbert-pairing convention is fixed",
            "citation": "finite-dimensional Hilbert projection formula",
        },
        {
            "stage": "full_HS_norm",
            "formula": "||C P_eta||_HS^2=tr_Heta(C^*C)=tr(G^{-1} H), H_ij=<C kappa_i,C kappa_j>",
            "conclusion": "the full finite Hilbert-Schmidt residual requires H_ij, not only c_ij",
            "citation": "operator trace in nonorthonormal basis",
        },
        {
            "stage": "compressed_matrix",
            "formula": "c_ij=<kappa_i,C kappa_j>; ||P_eta C P_eta||_HS^2=tr(G^{-1} c^* G^{-1} c)",
            "conclusion": "the c-only trace identity is for the compressed operator P_eta C P_eta",
            "citation": "Step177 c_ij matrix entries; finite-dimensional compression",
        },
        {
            "stage": "identity_verdict",
            "formula": "tr(c G^{-1} c^* G^{-1}) != ||C P_eta||_HS^2 unless C(H_eta) subset H_eta or the range projection is intended",
            "conclusion": "Step204 cannot decide the full HS residual from c alone; it can only decide the compressed finite diagnostic if c is computed",
            "citation": "symbolic verification of requested identity",
        },
    ]
    with (BASE / "xi_formula_derivation_step204.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("Step 204 symbolic identity derivation")
    for row in rows:
        print(f"{row['stage']}: {row['conclusion']}")


if __name__ == "__main__":
    main()
