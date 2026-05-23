#!/usr/bin/env python3
"""Step 202 assembly of the finite Branch-B matrix-source residual.

The script consumes the numerical Burnol E_{1/2} values from
compute_E_half_step202.py and assembles the closed symbolic/numerical Gram
matrix G_ij = K_{1/2}^Gamma(rho_j,rho_i).  It then records the obstruction to a
certified c_ij matrix: the inherited record fixes kappa as T_a^*K(.,w), but a
certified quadrature for the transported boundary vector and the full
K_infty^op commutator is not obtained in this run.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts")
MP_DPS = 70
ELL_VALUES = [
    ("log2", mp.log(2)),
    ("log3", mp.log(3)),
    ("one", mp.mpf(1)),
]


def load_e_values() -> tuple[dict[str, mp.mpc], dict[str, mp.mpf], dict[str, mp.mpc]]:
    mp.mp.dps = MP_DPS
    values: dict[str, mp.mpc] = {}
    errors: dict[str, mp.mpf] = {}
    ws: dict[str, mp.mpc] = {}
    with (BASE / "E_half_values_step202.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            label = row["label"]
            values[label] = mp.mpc(mp.mpf(row["E_real"]), mp.mpf(row["E_imag"]))
            errors[label] = mp.mpf(row["error_bound"])
            ws[label] = mp.mpc(mp.mpf(row["w_real"]), mp.mpf(row["w_imag"]))
    return values, errors, ws


def kernel_value(z1: mp.mpc, z2: mp.mpc, e1: mp.mpc, e2: mp.mpc, e1_reflect: mp.mpc, e2_reflect: mp.mpc) -> mp.mpc:
    return (e1 * mp.conj(e2) - e1_reflect * mp.conj(e2_reflect)) / (z1 + z2 - 1)


def kernel_error(z1: mp.mpc, z2: mp.mpc, e1: mp.mpc, e2: mp.mpc, e1r: mp.mpc, e2r: mp.mpc, de1: mp.mpf, de2: mp.mpf, de1r: mp.mpf, de2r: mp.mpf) -> mp.mpf:
    denom = abs(z1 + z2 - 1)
    if denom == 0:
        return mp.inf
    # First-order product perturbation bound.
    num_err = de1 * abs(e2) + abs(e1) * de2 + de1r * abs(e2r) + abs(e1r) * de2r
    return num_err / denom


def main() -> None:
    mp.mp.dps = MP_DPS
    values, errors, ws = load_e_values()
    zeros = {i: ws[f"rho_{i}"] for i in range(1, 4)}

    g_rows = []
    g_matrix: list[list[dict[str, str]]] = []
    print("Step 202 G-matrix assembly")
    for i in range(1, 4):
        row_payload = []
        for j in range(1, 4):
            z1 = zeros[j]
            z2 = zeros[i]
            e1 = values[f"rho_{j}"]
            e2 = values[f"rho_{i}"]
            e1r = values[f"one_minus_rho_{j}"]
            e2r = values[f"one_minus_rho_{i}"]
            g = kernel_value(z1, z2, e1, e2, e1r, e2r)
            ge = kernel_error(
                z1,
                z2,
                e1,
                e2,
                e1r,
                e2r,
                errors[f"rho_{j}"],
                errors[f"rho_{i}"],
                errors[f"one_minus_rho_{j}"],
                errors[f"one_minus_rho_{i}"],
            )
            status = "finite_cutoff_value_not_certified"
            out = {
                "i": i,
                "j": j,
                "G_real": mp.nstr(mp.re(g), 30),
                "G_imag": mp.nstr(mp.im(g), 30),
                "G_abs": mp.nstr(abs(g), 30),
                "error_bound": mp.nstr(ge, 30),
                "status": status,
                "formula": "K_{1/2}^Gamma(rho_j,rho_i) from Burnol 2002 equation 1",
            }
            g_rows.append(out)
            row_payload.append(out)
            print(f"G[{i},{j}]={mp.nstr(mp.re(g), 12)}{mp.nstr(mp.im(g), 12)}j  err<={mp.nstr(ge, 6)}")
        g_matrix.append(row_payload)

    with (BASE / "G_matrix_step202.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(g_rows[0].keys()))
        writer.writeheader()
        writer.writerows(g_rows)

    # The commutator entries are explicit after Step 201 but not certified here.
    c_rows = []
    for ell_name, ell in ELL_VALUES:
        for i in range(1, 4):
            for j in range(1, 4):
                c_rows.append({
                    "i": i,
                    "j": j,
                    "ell_label": ell_name,
                    "ell_value": mp.nstr(ell, 30),
                    "c_real": "",
                    "c_imag": "",
                    "c_abs": "",
                    "error_bound": "not_certified",
                    "status": "not_evaluated_certified",
                    "reason": "requires certified boundary samples of kappa_i=T_{1/2}^*K(.,rho_i) and full K_infty^op PSWF correction; Step 202 only certifies E/G layer",
                    "formula": "<e_i,(I-P_infty)M_{m_ell}P_infty e_j>",
                })
    with (BASE / "c_matrix_step202.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(c_rows[0].keys()))
        writer.writeheader()
        writer.writerows(c_rows)

    diagonal_status = "literal_K_rho_j_rho_i_diagonal_zero"
    decision = {
        "xi_matrix_source_value": "",
        "xi_matrix_source_error": "not_certified",
        "xi_matrix_source_verdict": "V_xi_matrix_source_partial",
        "reason": "E_{1/2} values and the literal finite Gram formula were numerically assembled; the literal K(rho_j,rho_i) convention gives zero diagonal entries on the critical line, so e_i=kappa_i/sqrt(G_ii) cannot be normalized without the correct diagonal/reproducing-kernel limit convention. The commutator matrix c_ij also needs certified transported-boundary kappa quadrature and the full K_infty^op PSWF correction.",
        "new_subresidual": "fix_Branches_B_kernel_inner_product_convention_and_certified_commutator_quadrature",
        "diagonal_status": diagonal_status,
    }
    with (BASE / "xi_matrix_source_decision_step202.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(decision.keys()))
        writer.writeheader()
        writer.writerow(decision)

    robustness_rows = [
        {
            "component": "E_half_resolvent",
            "N_PSWF_or_resolvent": "160",
            "dps": str(MP_DPS),
            "ell": "",
            "status": "computed",
            "observation": "finite cosine-resolvent layer assembled; dominant uncertainty is cutoff/tail comparison",
        },
        {
            "component": "E_half_resolvent",
            "N_PSWF_or_resolvent": "240",
            "dps": "not_run",
            "ell": "",
            "status": "not_completed",
            "observation": "reserved for certification pass; current run does not claim stability across 240 nodes",
        },
        {
            "component": "E_half_resolvent",
            "N_PSWF_or_resolvent": "320",
            "dps": "not_run",
            "ell": "",
            "status": "not_completed",
            "observation": "reserved for certification pass; current run does not claim stability across 320 nodes",
        },
    ]
    for ell_name, ell in ELL_VALUES:
        robustness_rows.append({
            "component": "commutator_c_matrix",
            "N_PSWF_or_resolvent": "requires full K_infty^op",
            "dps": "not_certified",
            "ell": f"{ell_name}={mp.nstr(ell, 18)}",
            "status": "blocked_after_E_G_layer",
            "observation": "ell sensitivity cannot be evaluated before c_ij certified quadrature is available",
        })
    with (BASE / "robustness_step202.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_rows)

    (BASE / "xi_matrix_source_payload_step202.json").write_text(json.dumps({
        "G_matrix": g_matrix,
        "c_matrix_status": "not_evaluated_certified",
        "xi_matrix_source": decision,
        "diagonal_status": diagonal_status,
        "robustness": robustness_rows,
    }, indent=2) + "\n", encoding="utf-8")

    print(f"diagonal_status: {diagonal_status}")
    print("c_matrix: not evaluated certified")
    print("Xi_matrix_source verdict: V_xi_matrix_source_partial")


if __name__ == "__main__":
    main()
