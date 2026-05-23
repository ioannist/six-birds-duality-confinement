#!/usr/bin/env python3
"""Avenue A: 10x grid refinement for Branch B c-matrices."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
import time
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path("/home/repos/six-birds-foundations-iii")
ART = ROOT / "anti_loc/thread/steps/step290_branch_B_c_matrix_precision_artifacts"
STEP202_SCRIPT = ROOT / "anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/compute_E_half_step202.py"
STEP202_VALUES = ROOT / "anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/E_half_values_step202.csv"
STEP208_SCRIPT = ROOT / "anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts/compute_c_matrices_step208.py"
STEP208 = ROOT / "anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts"
STEP289 = ROOT / "anti_loc/thread/steps/step289_branch_B_high_precision_artifacts"

MP_DPS = 80
N_GRID_REFINED = 2000
N_PSWF_TERMS = 24
T_MAX = 40.0
ELL = math.log(2.0)


RHO = {
    1: mp.mpc(mp.mpf("0.5"), mp.mpf("14.134725141734693790457251983562470270784257115699")),
    2: mp.mpc(mp.mpf("0.5"), mp.mpf("21.022039638771554992628479593896902777334340524903")),
    3: mp.mpc(mp.mpf("0.5"), mp.mpf("25.010857580145688763213790992562821818659549672558")),
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def read_E_rho_values() -> dict[str, mp.mpc]:
    vals = {}
    with STEP202_VALUES.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vals[row["label"]] = mp.mpc(mp.mpf(row["E_real"]), mp.mpf(row["E_imag"]))
    return vals


def kernel_candidate(s: mp.mpc, rho: mp.mpc, e_s: mp.mpc, e_1s: mp.mpc, e_rho: mp.mpc, e_1rho: mp.mpc) -> mp.mpc:
    return (e_s * e_rho - e_1s * e_1rho) / (s + rho - 1)


def zeta_prime(s: mp.mpc) -> mp.mpc:
    return mp.diff(lambda z: mp.zeta(z), s)


def build_samples(tau: np.ndarray) -> tuple[dict[int, np.ndarray], dict[int, np.ndarray]]:
    step202 = load_module(STEP202_SCRIPT, "step202_for_step290")
    mp.mp.dps = MP_DPS
    data = step202.build_resolvent(120)
    e_rho = read_E_rho_values()
    cand1_lists: dict[int, list[complex]] = {1: [], 2: [], 3: []}
    cand2_lists: dict[int, list[complex]] = {1: [], 2: [], 3: []}

    deriv = {i: zeta_prime(rho) for i, rho in RHO.items()}
    completion = {i: mp.power(mp.pi, -rho / 2) * mp.gamma(rho / 2) for i, rho in RHO.items()}

    for tv_float in tau:
        tv = mp.mpf(str(float(tv_float)))
        s = mp.mpc(mp.mpf("0.5"), tv)
        e_s, _, _ = step202.e_lambda(s, data)
        e_1s, _, _ = step202.e_lambda(1 - s, data)
        zeta_s = mp.zeta(s)
        for i, rho in RHO.items():
            v1 = kernel_candidate(
                s,
                rho,
                e_s,
                e_1s,
                e_rho[f"rho_{i}"],
                e_rho[f"one_minus_rho_{i}"],
            )
            denom = (s - rho) * deriv[i] * completion[i]
            v2 = zeta_s / denom
            cand1_lists[i].append(complex(float(mp.re(v1)), float(mp.im(v1))))
            cand2_lists[i].append(complex(float(mp.re(v2)), float(mp.im(v2))))

    return (
        {i: np.array(vals, dtype=np.complex128) for i, vals in cand1_lists.items()},
        {i: np.array(vals, dtype=np.complex128) for i, vals in cand2_lists.items()},
    )


def read_inherited(candidate: str) -> dict[tuple[int, int], dict[str, str]]:
    path = STEP208 / f"c_matrix_{candidate}_step208.csv"
    out = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[(int(row["i"]), int(row["j"]))] = row
    return out


def read_g_inv_fro() -> mp.mpf:
    with (STEP289 / "condition_number_vs_dps_step289.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["dps"] == "500":
                return mp.mpf(row["fro_norm_G_inv"])
    raise RuntimeError("missing dps=500 row")


def write_refined(candidate: str, c: np.ndarray, seconds: float) -> None:
    inherited = read_inherited(candidate)
    gi = read_g_inv_fro()
    rows = []
    reduction_rows = []
    for i in range(3):
        for j in range(3):
            old = inherited[(i + 1, j + 1)]
            old_val = complex(float(old["c_real"]), float(old["c_imag"]))
            old_err = mp.mpf(old["error_bound"])
            new_val = c[i, j]
            diff = abs(new_val - old_val)
            reduction = old_err / mp.mpf(str(diff)) if diff != 0 else mp.inf
            amplified_new = gi**2 * mp.mpf(str(diff))
            rows.append(
                {
                    "candidate": candidate,
                    "i": i + 1,
                    "j": j + 1,
                    "grid_nodes": N_GRID_REFINED,
                    "ell": f"{ELL:.17e}",
                    "n_pswf_terms": N_PSWF_TERMS,
                    "c_real": f"{new_val.real:.17e}",
                    "c_imag": f"{new_val.imag:.17e}",
                    "c_abs": f"{abs(new_val):.17e}",
                    "inherited_c_abs": old["c_abs"],
                    "abs_difference_vs_inherited": f"{diff:.17e}",
                    "inherited_error_bound": old["error_bound"],
                    "nominal_error_reduction_factor": mp.nstr(reduction, 20),
                    "amplified_difference_by_Ginv2": mp.nstr(amplified_new, 20),
                    "compute_seconds_total": f"{seconds:.6f}",
                    "status": "refined_2000_node_grid_diagnostic_not_transport_certification",
                }
            )
            reduction_rows.append(
                {
                    "avenue": "A_grid_refinement",
                    "candidate": candidate,
                    "i": i + 1,
                    "j": j + 1,
                    "before_error": old["error_bound"],
                    "after_proxy_error": f"{diff:.17e}",
                    "reduction_factor": mp.nstr(reduction, 20),
                    "target_10_orders_met": str(reduction >= mp.mpf("1e10")),
                    "dominant_remaining_source": "comparison-only proxy; unresolved transport and PSWF truncation remain",
                }
            )
    path = ART / "c_matrix_entries_refined_step290.csv"
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if not exists:
            writer.writeheader()
        writer.writerows(rows)
    red_path = ART / "uncertainty_reduction_step290.csv"
    exists = red_path.exists()
    with red_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(reduction_rows[0].keys()))
        if not exists:
            writer.writeheader()
        writer.writerows(reduction_rows)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    if (ART / "c_matrix_entries_refined_step290.csv").exists():
        (ART / "c_matrix_entries_refined_step290.csv").unlink()
    if (ART / "uncertainty_reduction_step290.csv").exists():
        (ART / "uncertainty_reduction_step290.csv").unlink()

    step208 = load_module(STEP208_SCRIPT, "step208_for_step290")
    raw_x, raw_w = leggauss(N_GRID_REFINED)
    tau = T_MAX * raw_x
    weights = T_MAX * raw_w

    t0 = time.perf_counter()
    cand1, cand2 = build_samples(tau)
    psis = step208.build_psi_matrix(tau, N_PSWF_TERMS)
    c1 = step208.c_matrix_for_samples(cand1, tau, weights, N_PSWF_TERMS, ELL)
    c2 = step208.c_matrix_for_samples(cand2, tau, weights, N_PSWF_TERMS, ELL)
    seconds = time.perf_counter() - t0

    write_refined("CAND1", c1, seconds)
    write_refined("CAND2", c2, seconds)

    print("Step 290 grid refinement")
    print(f"grid_nodes={N_GRID_REFINED} compute_seconds={seconds:.3f}")
    print(f"CAND1 max_abs={np.max(np.abs(c1)):.8e} fro={np.linalg.norm(c1):.8e}")
    print(f"CAND2 max_abs={np.max(np.abs(c2)):.8e} fro={np.linalg.norm(c2):.8e}")


if __name__ == "__main__":
    main()
