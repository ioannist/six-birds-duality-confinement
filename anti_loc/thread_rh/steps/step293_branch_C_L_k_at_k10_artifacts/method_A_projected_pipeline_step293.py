#!/usr/bin/env python3
"""Step 293 Method A plus component/cross-method computation.

Computes rho1_G_star projected L_k for k=8,9,10 using the inherited
Step269 projected pipeline, then splits L_k = delta_Dk - I_k - R_k.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import simpson


ART = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step293_branch_C_L_k_at_k10_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP269_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/compute_branch_C_k_5_6_7_step269.py")
STEP270_CLOSED = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step270_branch_C_stationary_phase_artifacts/closed_identity_step270.csv")
STEP269_POLY = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step269_branch_C_k_extension_artifacts/polynomial_correction_test_step269.csv")

MP_DPS = 80
TRIPLE_ID = "rho1_G_star"
RHO_INDEX = 1
G_ID = "G_star"
K_EXTEND = [8, 9, 10]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    names = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def cfmt(z: complex) -> str:
    return f"{z.real:+.16e}{z.imag:+.16e}j"


def load_fit() -> dict[str, float]:
    for row in read_csv(STEP269_POLY):
        if row["triple_id"] == TRIPLE_ID:
            return {
                "a": float(row["a"]),
                "b": float(row["b"]),
                "c": float(row["c"]),
                "rmse": float(row["rmse_k0_7"]),
            }
    raise KeyError(TRIPLE_ID)


def fit_pred(params: dict[str, float], k: int) -> float:
    return params["a"] * ((k + 1.0) ** params["c"]) * math.exp(params["b"] * k)


def projected_components(step269, gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, quad_data, k: int, n_terms: int) -> tuple[complex, complex, complex, complex]:
    delta = step269.delta_Dk(gamma, quad_data, k)
    I = complex(simpson(((-1j) ** k) * step269.sinc_derivative_n(gamma - u_grid, k) * F, x=u_grid))
    R = 0j
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_Dk = step269.psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        R += psi_Dk * J_n
    L = delta - I - R
    return delta, I, R, L


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    step196 = load_module("step196_for_step293", STEP196_SCRIPT)
    step269 = load_module("step269_for_step293", STEP269_SCRIPT)
    step196.MP_DPS = MP_DPS
    step269.MP_DPS = MP_DPS
    params = load_fit()

    t0 = time.time()
    u_grid = np.linspace(-step196.U_MAX, step196.U_MAX, int(round(2 * step196.U_MAX / step196.H)) + 1)
    zeta_grid = step196.zeta_values(u_grid)
    pswf = step196.precompute_pswf(u_grid, step196.N_PSWF_PRIMARY, step269.N_TERMS_TAIL)
    pswf_half = step196.precompute_pswf(u_grid[::2], step196.N_PSWF_ALT, step269.N_TERMS_TAIL)
    pswf_alt = step196.precompute_pswf(u_grid, step196.N_PSWF_ALT, step269.N_TERMS_TAIL)
    spec = step196.GENERATORS[G_ID]
    moments = step196.compute_moments(spec)
    G_primary, _, quad_data = step196.mellin_values(u_grid, spec, moments, step196.N_T_PRIMARY)
    G_coarse, _, _ = step196.mellin_values(u_grid, spec, moments, step196.N_T_COARSE)
    F = zeta_grid * G_primary
    gd = {"F": F, "F_coarse": zeta_grid * G_coarse, "quad_data": quad_data}
    gamma = step196.ZEROS[RHO_INDEX]

    method_a_rows: list[dict[str, object]] = []
    method_b_rows: list[dict[str, object]] = []
    method_c_rows: list[dict[str, object]] = []
    ratio_rows: list[dict[str, object]] = []
    compare_rows: list[dict[str, object]] = []
    output = [
        "Step293 rho1_G_star k=8..10 projected discrepancy resolution",
        f"setup_time_seconds={time.time()-t0:.3f}",
    ]

    # Step270/269 certified history k=1..7.
    for row in read_csv(STEP270_CLOSED):
        if row["triple_id"] != TRIPLE_ID:
            continue
        k = int(row["k"])
        if 1 <= k <= 7:
            delta_abs = float(row["raw_abs"])
            L_abs = float(row["projected_abs_recomputed"])
            ratio_rows.append({
                "k": k,
                "delta_abs": f"{delta_abs:.16e}",
                "L_abs": f"{L_abs:.16e}",
                "delta_over_L": f"{delta_abs / L_abs:.16e}",
                "L_over_delta": f"{L_abs / delta_abs:.16e}",
                "source": "step270_closed_identity",
            })

    for k in K_EXTEND:
        k_start = time.time()
        delta, I, R, L_b = projected_components(step269, gamma, F, u_grid, pswf, quad_data, k, step269.N_TERMS_VALUE)
        L_a = step269.projected_k(gamma, F, u_grid, pswf, quad_data, k, step269.N_TERMS_VALUE)
        err, comps = step269.k_error(gamma, gd, u_grid, pswf, pswf_half, pswf_alt, k)
        pred = fit_pred(params, k)
        method_a_rows.append({
            "triple_id": TRIPLE_ID,
            "k": k,
            "method": "A_step269_projected_pipeline",
            "L_complex": cfmt(L_a),
            "L_abs": f"{abs(L_a):.16e}",
            "fit_predicted": f"{pred:.16e}",
            "absolute_residual_vs_step269_fit": f"{abs(L_a) - pred:.16e}",
            "relative_residual_vs_L": f"{(abs(L_a) - pred)/abs(L_a):.16e}",
            "error_bound": f"{err:.16e}",
            "half_grid_delta": f"{comps['half_grid_delta']:.16e}",
            "coarse_G_delta": f"{comps['coarse_G_delta']:.16e}",
            "pswf_alt_delta": f"{comps['pswf_alt_delta']:.16e}",
            "tail_reserve": f"{comps['tail_reserve']:.16e}",
            "runtime_seconds": f"{time.time() - k_start:.6f}",
        })
        method_b_rows.append({
            "triple_id": TRIPLE_ID,
            "k": k,
            "method": "B_component_split_delta_minus_I_minus_R",
            "delta_complex": cfmt(delta),
            "delta_abs": f"{abs(delta):.16e}",
            "I_complex": cfmt(I),
            "I_abs": f"{abs(I):.16e}",
            "R_complex": cfmt(R),
            "R_abs": f"{abs(R):.16e}",
            "L_complex": cfmt(L_b),
            "L_abs": f"{abs(L_b):.16e}",
            "delta_over_L": f"{abs(delta)/abs(L_b):.16e}",
            "L_over_delta": f"{abs(L_b)/abs(delta):.16e}",
        })
        method_c_rows.append({
            "triple_id": TRIPLE_ID,
            "k": k,
            "method": "C_step270_extension_same_projected_formula",
            "L_complex": cfmt(L_a),
            "L_abs": f"{abs(L_a):.16e}",
            "delta_abs": f"{abs(delta):.16e}",
            "delta_over_L": f"{abs(delta)/abs(L_a):.16e}",
            "L_over_delta": f"{abs(L_a)/abs(delta):.16e}",
            "source_formula": "Step270 derive_stationary_phase.py calls step269.projected_k",
        })
        ratio_rows.append({
            "k": k,
            "delta_abs": f"{abs(delta):.16e}",
            "L_abs": f"{abs(L_a):.16e}",
            "delta_over_L": f"{abs(delta) / abs(L_a):.16e}",
            "L_over_delta": f"{abs(L_a) / abs(delta):.16e}",
            "source": "step293_extension",
        })
        compare_rows.append({
            "triple_id": TRIPLE_ID,
            "k": k,
            "A_L_abs": f"{abs(L_a):.16e}",
            "B_L_abs": f"{abs(L_b):.16e}",
            "C_L_abs": f"{abs(L_a):.16e}",
            "A_minus_B_abs": f"{abs(L_a - L_b):.16e}",
            "A_minus_C_abs": f"{0.0:.16e}",
            "agreement": "A_equals_B_equals_C" if abs(L_a - L_b) < max(1e-8, 1e-10 * abs(L_a)) else "methods_disagree",
        })
        output.append(
            f"k={k} |delta|={abs(delta):.8e} |I|={abs(I):.8e} |R|={abs(R):.8e} "
            f"|L|={abs(L_a):.8e} delta/L={abs(delta)/abs(L_a):.6e} L/delta={abs(L_a)/abs(delta):.6e} "
            f"pred={pred:.8e} err_bound={err:.3e}"
        )

    write_csv(ART / "L_k_method_A_step293.csv", method_a_rows)
    write_csv(ART / "L_k_method_B_step293.csv", method_b_rows)
    write_csv(ART / "L_k_method_C_step293.csv", method_c_rows)
    write_csv(ART / "cross_method_comparison_step293.csv", compare_rows)
    write_csv(ART / "L_k_over_delta_Dk_ratio_step293.csv", sorted(ratio_rows, key=lambda r: int(r["k"])))
    (ART / "compute_step293_output.txt").write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\n".join(output))


if __name__ == "__main__":
    main()
