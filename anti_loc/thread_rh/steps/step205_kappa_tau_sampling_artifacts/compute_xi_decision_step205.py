#!/usr/bin/env python3
"""Step 205 Xi decision."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step205_kappa_tau_sampling_artifacts")
STEP204_G = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step204_unnormalized_xi_matrix_source_artifacts/G_matrix_step204.csv")


def main() -> None:
    shutil.copyfile(STEP204_G, BASE / "G_matrix_step205.csv")
    decision = {
        "xi_matrix_source_value": "",
        "xi_matrix_source_error": "not_certified",
        "xi_matrix_source_verdict": "V_kappa_tau_sampling_formula_corrected",
        "reason": "operator-chain audit does not justify kappa_i(tau)=K(1/2+i tau,rho_i); c_ij not computed from uncertified candidate boundary samples",
        "required_record": "explicit T_a^* boundary sampling formula or proof that T_a^*K_a^Gamma(.,rho)=K_a^Gamma(1/2+i tau,rho) in the inherited normalization",
    }
    with (BASE / "xi_decision_step205.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(decision.keys()))
        writer.writeheader()
        writer.writerow(decision)
    robustness_rows = [
        {
            "test": "kappa_formula",
            "parameter": "operator_chain",
            "status": "failed_verification",
            "observation": "T_a^*=U_infty J_a^*M_Gamma^* is not identity on K_a^Gamma in inherited records",
        },
        {
            "test": "tau_grid",
            "parameter": "N=200,T=40",
            "status": "candidate_samples_computed",
            "observation": "samples are K-boundary candidate values only",
        },
        {
            "test": "PSWF",
            "parameter": "N=12/24/36",
            "status": "not_run",
            "observation": "not lawful before kappa sampling formula is certified",
        },
        {
            "test": "ell",
            "parameter": "log2/log3/1",
            "status": "not_run",
            "observation": "not lawful before c_ij computation is certified",
        },
    ]
    with (BASE / "robustness_step205.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_rows)
    print("Step 205 Xi decision")
    print("verdict=V_kappa_tau_sampling_formula_corrected")
    print("required_record=explicit T_a^* boundary sampling formula")


if __name__ == "__main__":
    main()
