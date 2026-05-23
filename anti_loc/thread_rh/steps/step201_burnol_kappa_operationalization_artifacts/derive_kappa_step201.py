#!/usr/bin/env python3
"""Step 201 symbolic operationalization of Burnol kappa.

This script does not claim numerical closure.  It records the explicit
paper-grounded formulas now inherited from the manager-led Burnol audit and
derives the symbolic objects needed by Branch A and Branch B.
"""

from pathlib import Path
import json

BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step201_burnol_kappa_operationalization_artifacts")

rho = {
    "rho_1": "1/2 + 14.134725141734693 i",
    "rho_2": "1/2 + 21.022039638771554 i",
    "rho_3": "1/2 + 25.010857580145688 i",
}

lambda_value = "1/2"
ell_value = "log(2)"

E_lambda = (
    "E_lambda(w)=pi^(-w/2) Gamma(w/2) [lambda^(1/2-w) + "
    "(sqrt(lambda)/2) int_lambda^infty (psi_plus^lambda(t)-psi_minus^lambda(t)) t^(-w) dt]"
)

K_lambda = (
    "K_lambda(z,w)=("
    "E_lambda(z) conjugate(E_lambda(w)) - "
    "E_lambda(1-z) conjugate(E_lambda(1-w))"
    ")/(z+w-1)"
)

kappa = (
    "kappa_{a,w,k}(tau) = "
    "(T_a^* partial_{bar w}^k K_lambda(.,w))(1/2+i tau), "
    "T_a=M_Gamma J_a U_infty^{-1}, a=lambda"
)

branch_b_gram = (
    "G_ij=<kappa_i,kappa_j>_{Mellin boundary}="
    "<partial_{bar z}^0 K_lambda(.,rho_i), partial_{bar w}^0 K_lambda(.,rho_j)>_{B(E_lambda)}="
    "K_lambda(rho_j,rho_i) up to the inherited inner-product convention"
)

branch_b_commutator = (
    "c_ij(ell)=<e_i,(I-P_infty) M_{m_ell} P_infty e_j>, "
    "e_i=kappa_{a,rho_i,0}/sqrt(G_ii), "
    "m_ell(s)=exp(-ell(1/2-s)); "
    "P_infty acts by K_infty^op, so c_ij is the double integral "
    "over tau,tau' of conjugate(e_i(tau)) [(I-P_infty)M_m P_infty e_j](tau)."
)

branch_a_matrix = (
    "<eta_i,C_ell P_eta eta_j> = "
    "<kappa_i,(I-P_infty)M_{m_ell}P_infty kappa_j> after T_a pullback; "
    "all entries are explicit functionals of E_lambda, psi_pm^lambda, and K_infty^op."
)

lines = [
    "Step 201 symbolic kappa operationalization",
    "provenance=manager-led Burnol audit 2026-05-16; Burnol 2002 math/0208121 Theorems 4 and 8; Burnol 2004 math/0112254 Section 6",
    f"lambda={lambda_value}",
    f"ell={ell_value}",
    "projection=pi_lambda=P_{K_lambda}=P_{L_a^Gamma} from Burnol 2002 Theorem 4",
    f"E_formula={E_lambda}",
    f"K_formula={K_lambda}",
    f"kappa_formula={kappa}",
    f"branch_B_Gram={branch_b_gram}",
    f"branch_B_commutator={branch_b_commutator}",
    f"branch_A_matrix={branch_a_matrix}",
    "Branch_A_status=kappa-level lifted; compactness/HS/Weyl closure requires downstream summability/essential-norm theorem",
    "Branch_B_status=kernel Gram closed symbolically; Xi_matrix_source not numerically decided in this step",
]

for key, value in rho.items():
    lines.append(f"{key}={value}")
    lines.append(f"kappa_{key}=T_(1/2)^* K_(1/2)^Gamma(.,{value})")

payload = {
    "lambda": lambda_value,
    "ell": ell_value,
    "E_lambda": E_lambda,
    "K_lambda": K_lambda,
    "kappa": kappa,
    "rho": rho,
    "branch_b_gram": branch_b_gram,
    "branch_b_commutator": branch_b_commutator,
    "branch_a_matrix": branch_a_matrix,
    "verdict_support": "kappa_explicit_downstream_residuals_exposed",
}

(BASE / "compute_kappa_output_step201.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
(BASE / "derive_kappa_status_step201.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print("\n".join(lines))

