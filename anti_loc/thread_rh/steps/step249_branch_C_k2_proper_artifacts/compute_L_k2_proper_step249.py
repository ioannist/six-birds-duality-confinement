#!/usr/bin/env python3
"""Proper k=2 Branch C values by analytic second differentiation."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import simpson


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step249_branch_C_k2_proper_artifacts")
STEP196 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP247_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step247_branch_C_k1_proper_artifacts/k1_proper_dataset_step247.csv")

MP_DPS = 80
N_TERMS_VALUE = 3
N_TERMS_TAIL = 12
K2_DH = 0.02


def load_step196_module():
    spec = importlib.util.spec_from_file_location("step196_branch_c", STEP196)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step196 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step196_branch_c"] = mod
    spec.loader.exec_module(mod)
    mod.MP_DPS = MP_DPS
    return mod


def sinc_second(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-6
    out[mask] = -1.0 / (3.0 * math.pi) + (arr[mask] ** 2) / (10.0 * math.pi)
    xm = arr[~mask]
    out[~mask] = (-xm * xm * np.sin(xm) - 2.0 * xm * np.cos(xm) + 2.0 * np.sin(xm)) / (math.pi * xm ** 3)
    if np.isscalar(x):
        return float(out)
    return out


def mellin_gamma_derivative(gamma: float, quad_data, order: int) -> complex:
    t = quad_data["t"]
    w = quad_data["w"]
    g = quad_data["g"]
    amp = w * g * t ** (-0.5)
    factor = (-1j * np.log(t)) ** order
    return complex((factor * np.exp(-1j * gamma * np.log(t))).dot(amp))


def zeta_derivative_at_s(gamma: float, order: int) -> complex:
    mp.mp.dps = MP_DPS
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(gamma)))
    return complex(mp.diff(lambda zz: mp.zeta(zz), s, order))


def sinc_integral_second(gamma: float, u_grid: np.ndarray, F: np.ndarray) -> complex:
    return complex(simpson(sinc_second(gamma - u_grid) * F, x=u_grid))


def psi_gamma_second_from_phi(gamma: float, x: np.ndarray, w: np.ndarray, mu: float, phi_n: np.ndarray) -> complex:
    int_k_second = sinc_second(gamma - x).dot(w * phi_n)
    return complex(-int_k_second / math.sqrt(1.0 - mu))


def second_terms(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, n_terms: int):
    terms = []
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_second = psi_gamma_second_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n])
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        terms.append(psi_second * J_n)
    return terms


def projected_k2_proper(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, quad_data, mod, n_terms: int = N_TERMS_VALUE) -> complex:
    mp.mp.dps = MP_DPS
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(gamma)))
    zeta_val = complex(mp.zeta(s))
    zp = zeta_derivative_at_s(gamma, 1)
    zpp = zeta_derivative_at_s(gamma, 2)
    G0 = mod.mellin_at_gamma(gamma, quad_data)
    G1 = mellin_gamma_derivative(gamma, quad_data, 1)
    G2 = mellin_gamma_derivative(gamma, quad_data, 2)
    # D^2 = (-i d/dgamma)^2 = -d^2/dgamma^2.
    # d^2[zeta(s(gamma))G]/dgamma^2 = -zeta''G + 2i zeta'G' + zeta G''.
    delta_k2 = zpp * G0 - 2j * zp * G1 - zeta_val * G2
    I_k2 = sinc_integral_second(gamma, u_grid, F)
    R_k2 = sum(second_terms(gamma, F, u_grid, pswf, n_terms), 0j)
    return delta_k2 + I_k2 + R_k2


def k2_error(gamma: float, gd: dict, u_grid: np.ndarray, pswf, pswf_half, pswf_alt, mod) -> tuple[float, dict[str, float]]:
    primary = projected_k2_proper(gamma, gd["F"], u_grid, pswf, gd["quad_data"], mod, N_TERMS_VALUE)
    half = projected_k2_proper(gamma, gd["F"][::2], u_grid[::2], pswf_half, gd["quad_data"], mod, N_TERMS_VALUE)
    coarse = projected_k2_proper(gamma, gd["F_coarse"], u_grid, pswf, gd["quad_data"], mod, N_TERMS_VALUE)
    alt = projected_k2_proper(gamma, gd["F"], u_grid, pswf_alt, gd["quad_data"], mod, N_TERMS_VALUE)
    tail_terms = second_terms(gamma, gd["F"], u_grid, pswf, N_TERMS_TAIL)
    tail = float(sum(abs(t) for t in tail_terms[N_TERMS_VALUE:]) * 2.0 + 10.0 * abs(tail_terms[-1]))
    comps = {
        "half_grid_delta": abs(primary - half),
        "coarse_G_delta": abs(primary - coarse),
        "pswf_alt_delta": abs(primary - alt),
        "tail_reserve": tail,
    }
    return float(sum(comps.values()) + 1e-8), comps


def finite_difference_k2(gamma: float, gd: dict, u_grid: np.ndarray, pswf, mod) -> complex:
    lp = mod.projected_value(gamma + K2_DH, gd["F"], u_grid, pswf, gd["quad_data"], N_TERMS_VALUE)
    l0 = mod.projected_value(gamma, gd["F"], u_grid, pswf, gd["quad_data"], N_TERMS_VALUE)
    lm = mod.projected_value(gamma - K2_DH, gd["F"], u_grid, pswf, gd["quad_data"], N_TERMS_VALUE)
    return -(lp - 2.0 * l0 + lm) / (K2_DH * K2_DH)


def load_step247_rows():
    with STEP247_CSV.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    mp.mp.dps = MP_DPS
    mod = load_step196_module()

    u_grid = np.linspace(-mod.U_MAX, mod.U_MAX, int(round(2 * mod.U_MAX / mod.H)) + 1)
    zeta_grid = mod.zeta_values(u_grid)
    pswf = mod.precompute_pswf(u_grid, mod.N_PSWF_PRIMARY, N_TERMS_TAIL)
    pswf_half = mod.precompute_pswf(u_grid[::2], mod.N_PSWF_PRIMARY, N_TERMS_VALUE)
    pswf_alt = mod.precompute_pswf(u_grid, mod.N_PSWF_ALT, N_TERMS_VALUE)

    generator_data = {}
    for gid, spec in mod.GENERATORS.items():
        moments = mod.compute_moments(spec)
        G_primary, _, quad_data = mod.mellin_values(u_grid, spec, moments, mod.N_T_PRIMARY)
        G_coarse, _, _ = mod.mellin_values(u_grid, spec, moments, mod.N_T_COARSE)
        generator_data[gid] = {
            "F": zeta_grid * G_primary,
            "F_coarse": zeta_grid * G_coarse,
            "quad_data": quad_data,
        }

    k1_rows = [r for r in load_step247_rows() if r["k"] == "1"]
    out_rows = []
    robust_rows = []
    for idx, src in enumerate(k1_rows, start=19):
        gamma = float(src["gamma"])
        gd = generator_data[src["G_id"]]
        proper = projected_k2_proper(gamma, gd["F"], u_grid, pswf, gd["quad_data"], mod, N_TERMS_VALUE)
        err, comps = k2_error(gamma, gd, u_grid, pswf, pswf_half, pswf_alt, mod)
        lower = max(0.0, abs(proper) - err)
        fd = finite_difference_k2(gamma, gd, u_grid, pswf, mod)
        fd_diff = abs(proper - fd)
        verdict = "nonzero" if lower > 1e-3 else "indeterminate"
        case_id = f"C{idx:02d}"
        out_rows.append({
            "case_id": case_id,
            "rho_index": src["rho_index"],
            "gamma": src["gamma"],
            "k": "2",
            "G_id": src["G_id"],
            "proper_L_real": f"{proper.real:.16e}",
            "proper_L_imag": f"{proper.imag:.16e}",
            "proper_L_abs": f"{abs(proper):.16e}",
            "proper_error_bound": f"{err:.16e}",
            "proper_lower_bound_abs": f"{lower:.16e}",
            "source_k1_case": src["case_id"],
            "finite_difference_k2_abs": f"{abs(fd):.16e}",
            "abs_difference_vs_fd_k2": f"{fd_diff:.16e}",
            "method": "analytic_second_derivative_of_projected_value",
            "verdict": verdict,
        })
        robust_rows.append({
            "case_id": case_id,
            "rho_index": src["rho_index"],
            "G_id": src["G_id"],
            "finite_difference_k2_real": f"{fd.real:.16e}",
            "finite_difference_k2_imag": f"{fd.imag:.16e}",
            "finite_difference_k2_abs": f"{abs(fd):.16e}",
            "proper_real": f"{proper.real:.16e}",
            "proper_imag": f"{proper.imag:.16e}",
            "proper_abs": f"{abs(proper):.16e}",
            "proper_error": f"{err:.16e}",
            "proper_lower": f"{lower:.16e}",
            "abs_difference_fd": f"{fd_diff:.16e}",
            "half_grid_delta": f"{comps['half_grid_delta']:.16e}",
            "coarse_G_delta": f"{comps['coarse_G_delta']:.16e}",
            "pswf_alt_delta": f"{comps['pswf_alt_delta']:.16e}",
            "tail_reserve": f"{comps['tail_reserve']:.16e}",
            "comparison_status": "same_nonzero_verdict" if lower > 1e-3 and abs(fd) > 1e-3 else "check",
        })

    with (BASE / "k2_proper_dataset_step249.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    with (BASE / "robustness_step249.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robust_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robust_rows)

    min_abs = min(float(r["proper_L_abs"]) for r in out_rows)
    min_lower = min(float(r["proper_lower_bound_abs"]) for r in out_rows)
    max_fd_diff = max(float(r["abs_difference_vs_fd_k2"]) for r in out_rows)
    status = "V_branch_C_k2_proper_foreclosure" if min_lower > 1e-3 else "V_branch_C_k2_proper_partial"
    status_rows = [
        {"metric": "k2_count", "value": str(len(out_rows)), "comment": "proper k=2 rows computed"},
        {"metric": "k2_min_abs", "value": f"{min_abs:.16e}", "comment": "minimum proper |L| over k=2 rows"},
        {"metric": "k2_min_lower_bound", "value": f"{min_lower:.16e}", "comment": "minimum |L|-error over k=2 rows"},
        {"metric": "max_abs_difference_vs_fd_k2", "value": f"{max_fd_diff:.16e}", "comment": "analytic second derivative vs central finite difference k2"},
        {"metric": "verdict", "value": status, "comment": "proper k=2 status"},
    ]
    with (BASE / "branch_C_k2_status_step249.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(status_rows[0].keys()))
        writer.writeheader()
        writer.writerows(status_rows)

    payload = {
        "mpmath_dps": MP_DPS,
        "u_max": mod.U_MAX,
        "h": mod.H,
        "n_terms_value": N_TERMS_VALUE,
        "n_terms_tail": N_TERMS_TAIL,
        "k2_rows": robust_rows,
        "status": status_rows,
    }
    (BASE / "k2_proper_results_step249.json").write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "Step 249 Branch C k=2 proper analytic second derivative",
        f"mpmath_dps={MP_DPS} k2_count={len(out_rows)}",
    ]
    for r in out_rows:
        lines.append(
            f"case={r['case_id']} rho{r['rho_index']} G={r['G_id']} "
            f"proper={float(r['proper_L_real']):+.10e}{float(r['proper_L_imag']):+.10e}j "
            f"abs={float(r['proper_L_abs']):.10e} err={float(r['proper_error_bound']):.3e} "
            f"lower={float(r['proper_lower_bound_abs']):.10e} fd_diff={float(r['abs_difference_vs_fd_k2']):.3e}"
        )
    lines.append(f"verdict={status}")
    (BASE / "compute_step249_output.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
