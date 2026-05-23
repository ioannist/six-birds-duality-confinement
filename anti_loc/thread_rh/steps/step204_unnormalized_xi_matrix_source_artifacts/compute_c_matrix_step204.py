#!/usr/bin/env python3
"""Step 204 unnormalized c_ij attempt.

This script assembles the corrected Step 204 Gram matrix, including the
off-diagonal convention K(rho_j, conjugate(rho_i)), and records the attempted
c_ij integral.  The c_ij values are not certified because the available Burnol
records give kappa symbolically as T_a^*K(.,rho), but do not yet provide a
numerically certified boundary-line sampling formula for T_a^*K(.,rho) suitable
for the K_infty^op commutator quadrature.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step204_unnormalized_xi_matrix_source_artifacts")
STEP202 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts")
STEP203 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step203_diagonal_gram_correction_artifacts")
MP_DPS = 90


def load_e() -> tuple[dict[str, mp.mpc], dict[str, mp.mpf], dict[str, mp.mpc]]:
    vals: dict[str, mp.mpc] = {}
    errs: dict[str, mp.mpf] = {}
    ws: dict[str, mp.mpc] = {}
    with (STEP202 / "E_half_values_step202.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            label = row["label"]
            vals[label] = mp.mpc(mp.mpf(row["E_real"]), mp.mpf(row["E_imag"]))
            errs[label] = mp.mpf(row["error_bound"])
            ws[label] = mp.mpc(mp.mpf(row["w_real"]), mp.mpf(row["w_imag"]))
    return vals, errs, ws


def load_diag() -> dict[int, tuple[mp.mpf, mp.mpf]]:
    out: dict[int, tuple[mp.mpf, mp.mpf]] = {}
    with (STEP203 / "G_diagonal_corrected_step203.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[int(row["rho_index"])] = (mp.mpf(row["G_chosen"]), mp.mpf(row["error_bound"]))
    return out


def main() -> None:
    mp.mp.dps = MP_DPS
    BASE.mkdir(parents=True, exist_ok=True)
    vals, errs, ws = load_e()
    diag = load_diag()
    gammas = {i: mp.im(ws[f"rho_{i}"]) for i in range(1, 4)}

    g_rows = []
    g_numeric = [[mp.mpc(0) for _ in range(3)] for __ in range(3)]
    for i in range(1, 4):
        for j in range(1, 4):
            if i == j:
                val = mp.mpc(diag[i][0], 0)
                err = diag[i][1]
                status = "diagonal_from_step203_LHopital"
                source = "Step203 LHopital K(conj(rho_i),rho_i)"
            else:
                # Step 204 off-diagonal convention:
                # G_ij = K(rho_j, conjugate(rho_i)), denominator i(gamma_j-gamma_i).
                e_rho_j = vals[f"rho_{j}"]
                e_rho_i = vals[f"rho_{i}"]
                e_1_rho_j = vals[f"one_minus_rho_{j}"]
                e_1_rho_i = vals[f"one_minus_rho_{i}"]
                denom = mp.j * (gammas[j] - gammas[i])
                val = (e_rho_j * e_rho_i - e_1_rho_j * e_1_rho_i) / denom
                err = (
                    errs[f"rho_{j}"] * abs(e_rho_i)
                    + abs(e_rho_j) * errs[f"rho_{i}"]
                    + errs[f"one_minus_rho_{j}"] * abs(e_1_rho_i)
                    + abs(e_1_rho_j) * errs[f"one_minus_rho_{i}"]
                ) / abs(denom)
                status = "off_diagonal_step204_conjugate_convention"
                source = "Burnol 2002 equation 1 with z1=rho_j,z2=conj(rho_i)"
            g_numeric[i - 1][j - 1] = val
            g_rows.append({
                "i": i,
                "j": j,
                "G_real": mp.nstr(mp.re(val), 40),
                "G_imag": mp.nstr(mp.im(val), 40),
                "G_abs": mp.nstr(abs(val), 40),
                "error_bound": mp.nstr(err, 40),
                "status": status,
                "source": source,
            })
    with (BASE / "G_matrix_step204.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(g_rows[0].keys()))
        writer.writeheader()
        writer.writerows(g_rows)

    # Conditioning diagnostics for the nominal G values.
    G = mp.matrix(g_numeric)
    try:
        det_g = mp.det(G)
        inv_g = G ** -1
        fro_inv = mp.sqrt(sum(abs(inv_g[r, c]) ** 2 for r in range(3) for c in range(3)))
        gram_status = "nominal_inverse_computed"
    except Exception as exc:
        det_g = mp.nan
        fro_inv = mp.nan
        gram_status = f"inversion_failed:{exc}"

    c_rows = []
    for i in range(1, 4):
        for j in range(1, 4):
            c_rows.append({
                "i": i,
                "j": j,
                "ell": "log(2)",
                "c_real": "",
                "c_imag": "",
                "c_abs": "",
                "error_bound": "not_certified",
                "status": "not_evaluated_certified",
                "formula": "<kappa_i,(I-P_infty)M_{m_ell}P_infty kappa_j>",
                "reason": "requires concrete certified samples of kappa_i(tau)=T_{1/2}^*K(.,rho_i)(1/2+i tau) and full K_infty^op PSWF quadrature; Burnol E kernel gives K-pairings but not this boundary-line vector numerically",
            })
    with (BASE / "c_matrix_step204.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(c_rows[0].keys()))
        writer.writeheader()
        writer.writerows(c_rows)

    robustness_rows = [
        {
            "test": "G_nominal_det",
            "value": mp.nstr(det_g, 40),
            "status": gram_status,
            "notes": "computed from Step203 diagonal plus Step204 off-diagonal convention",
        },
        {
            "test": "G_inverse_frobenius_norm",
            "value": mp.nstr(fro_inv, 40),
            "status": gram_status,
            "notes": "small diagonal and dominant diagonal error make inverse numerically fragile",
        },
        {
            "test": "c_matrix",
            "value": "not_certified",
            "status": "blocked",
            "notes": "unnormalized formulation removes sqrt(G_ii) division but not the need for kappa boundary samples",
        },
    ]
    with (BASE / "robustness_step204.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_rows)

    payload = {
        "G_matrix": g_rows,
        "G_det": mp.nstr(det_g, 50),
        "G_inverse_frobenius_norm": mp.nstr(fro_inv, 50),
        "c_matrix_status": "not_evaluated_certified",
    }
    (BASE / "compute_c_matrix_payload_step204.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("Step 204 unnormalized c_ij attempt")
    print("G off-diagonal convention: K(rho_j,conj(rho_i))")
    print(f"nominal det(G)={mp.nstr(det_g, 12)}")
    print(f"nominal ||G^-1||_F={mp.nstr(fro_inv, 12)}")
    print("c_matrix: not evaluated certified")


if __name__ == "__main__":
    main()
