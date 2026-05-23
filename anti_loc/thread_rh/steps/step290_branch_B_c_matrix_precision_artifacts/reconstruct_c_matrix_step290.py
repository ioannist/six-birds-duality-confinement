#!/usr/bin/env python3
"""Reconstruct Branch B c-matrix provenance for Step 290."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step290_branch_B_c_matrix_precision_artifacts"
STEP204 = ROOT / "anti_loc/thread/steps/step204_unnormalized_xi_matrix_source_artifacts"
STEP207 = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"
STEP208 = ROOT / "anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts"
STEP289 = ROOT / "anti_loc/thread/steps/step289_branch_B_high_precision_artifacts"


def load_c(candidate: str) -> list[dict[str, str]]:
    path = STEP208 / f"c_matrix_{candidate}_step208.csv"
    out = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append(
                {
                    "candidate": candidate,
                    "i": row["i"],
                    "j": row["j"],
                    "ell": row["ell"],
                    "n_pswf_terms": row["n_pswf_terms"],
                    "grid_nodes": row["grid_nodes"],
                    "c_real": row["c_real"],
                    "c_imag": row["c_imag"],
                    "c_abs": row["c_abs"],
                    "error_bound": row["error_bound"],
                    "source_file": str(path),
                    "status": row["status"],
                }
            )
    return out


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    inherited = load_c("CAND1") + load_c("CAND2")
    with (ART / "c_matrix_entries_inherited_step290.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(inherited[0].keys()))
        writer.writeheader()
        writer.writerows(inherited)

    # Keep local copies of the exact inherited matrices.
    for name in ["CAND1", "CAND2"]:
        shutil.copyfile(STEP208 / f"c_matrix_{name}_step208.csv", ART / f"c_matrix_{name}_inherited_step290.csv")

    provenance_rows = [
        {
            "object": "CAND1_samples",
            "source": str(STEP207 / "CAND1_samples_step207.csv"),
            "upstream": "Step205 kappa_tau_samples_step205.csv",
            "formula": "K_{1/2}^Gamma(1/2+i tau,rho_i), Burnol 2002 equation (1) + Theorem 8",
            "grid": "200 Gauss-Legendre tau nodes on [-40,40]",
            "dps": "Step205 MP_DPS=70; downstream Step208 c-matrix uses numpy complex128",
        },
        {
            "object": "CAND2_samples",
            "source": str(STEP207 / "CAND2_samples_step207.csv"),
            "upstream": "Step207 zeta-dual formula",
            "formula": "zeta(s)/((s-rho_i) zeta'(rho_i) pi^{-rho_i/2} Gamma(rho_i/2))",
            "grid": "same 200 Gauss-Legendre tau nodes on [-40,40]",
            "dps": "Step207 mpmath dps=70; downstream Step208 c-matrix uses numpy complex128",
        },
        {
            "object": "c_matrix",
            "source": str(STEP208 / "compute_c_matrices_step208.py"),
            "upstream": "Step173 finite-grid K_infty_op diagnostic",
            "formula": "c_ij=sum_tau w(tau) conj(kappa_i(tau))*((I-P) exp(i ell tau) P kappa_j)(tau)/(2*pi)",
            "grid": "200 Gauss-Legendre tau nodes; T_MAX=40; ell=log(2); 24 PSWF terms",
            "dps": "numpy double finite-grid diagnostic",
        },
        {
            "object": "G_inverse_amplification",
            "source": str(STEP289 / "condition_number_vs_dps_step289.csv"),
            "upstream": "Step289 high-precision inverse",
            "formula": "Xi=tr(G^{-1} c^dagger G^{-1} c)",
            "grid": "not grid-dependent",
            "dps": "G inverse stable through dps=1000; ||G^-1||_F about 4.099924785e16",
        },
        {
            "object": "step204_reference",
            "source": str(STEP204),
            "upstream": "Burnol-kernel conjugate convention",
            "formula": "G off-diagonal construction source",
            "grid": "not c-grid",
            "dps": "see Step204 artifacts",
        },
    ]
    with (ART / "c_matrix_provenance_step290.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(provenance_rows[0].keys()))
        writer.writeheader()
        writer.writerows(provenance_rows)

    print("Step 290 c-matrix provenance reconstructed")
    print(f"inherited_entries={len(inherited)}")


if __name__ == "__main__":
    main()
