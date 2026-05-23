#!/usr/bin/env python3
"""Proper k=1 Branch C values by analytic differentiation of Step 196 formula."""

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


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step247_branch_C_k1_proper_artifacts")
STEP196 = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP196_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/dataset_triples_step196.csv")

MP_DPS = 80
N_TERMS_VALUE = 3
N_TERMS_TAIL = 12


def load_step196_module():
    spec = importlib.util.spec_from_file_location("step196_branch_c", STEP196)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step196 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step196_branch_c"] = mod
    spec.loader.exec_module(mod)
    mod.MP_DPS = MP_DPS
    return mod


def sinc_derivative(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-8
    out[mask] = -arr[mask] / (3.0 * math.pi)
    xm = arr[~mask]
    out[~mask] = (xm * np.cos(xm) - np.sin(xm)) / (math.pi * xm * xm)
    if np.isscalar(x):
        return float(out)
    return out


def mellin_gamma_derivative(gamma: float, quad_data) -> complex:
    t = quad_data["t"]
    w = quad_data["w"]
    g = quad_data["g"]
    amp = w * g * t ** (-0.5)
    return complex((-1j * np.log(t) * np.exp(-1j * gamma * np.log(t))).dot(amp))


def zeta_prime_at_s(gamma: float) -> complex:
    mp.mp.dps = MP_DPS
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(gamma)))
    return complex(mp.diff(lambda zz: mp.zeta(zz), s))


def sinc_integral_derivative(gamma: float, u_grid: np.ndarray, F: np.ndarray) -> complex:
    return complex(simpson(sinc_derivative(gamma - u_grid) * F, x=u_grid))


def psi_gamma_derivative_from_phi(gamma: float, x: np.ndarray, w: np.ndarray, mu: float, phi_n: np.ndarray) -> complex:
    int_k_prime = sinc_derivative(gamma - x).dot(w * phi_n)
    return complex(-int_k_prime / math.sqrt(1.0 - mu))


def derivative_terms(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, n_terms: int):
    terms = []
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_prime = psi_gamma_derivative_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n])
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        terms.append(psi_prime * J_n)
    return terms


def projected_k1_proper(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, quad_data, mod, n_terms: int = N_TERMS_VALUE) -> complex:
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(gamma)))
    zeta_val = complex(mp.zeta(s))
    G_val = mod.mellin_at_gamma(gamma, quad_data)
    G_gamma_prime = mellin_gamma_derivative(gamma, quad_data)
    # -i d/dgamma [zeta(s(gamma)) G(gamma)].
    delta_k1 = zeta_prime_at_s(gamma) * G_val + (-1j) * zeta_val * G_gamma_prime
    I_k1 = -1j * sinc_integral_derivative(gamma, u_grid, F)
    R_k1 = -1j * sum(derivative_terms(gamma, F, u_grid, pswf, n_terms), 0j)
    return delta_k1 - I_k1 - R_k1


def k1_error(gamma: float, gd: dict, u_grid: np.ndarray, pswf, pswf_half, pswf_alt, mod) -> tuple[float, dict[str, float]]:
    primary = projected_k1_proper(gamma, gd["F"], u_grid, pswf, gd["quad_data"], mod, N_TERMS_VALUE)
    half = projected_k1_proper(gamma, gd["F"][::2], u_grid[::2], pswf_half, gd["quad_data"], mod, N_TERMS_VALUE)
    coarse = projected_k1_proper(gamma, gd["F_coarse"], u_grid, pswf, gd["quad_data"], mod, N_TERMS_VALUE)
    alt = projected_k1_proper(gamma, gd["F"], u_grid, pswf_alt, gd["quad_data"], mod, N_TERMS_VALUE)
    tail_terms = derivative_terms(gamma, gd["F"], u_grid, pswf, N_TERMS_TAIL)
    tail = float(sum(abs(t) for t in tail_terms[N_TERMS_VALUE:]) * 2.0 + 10.0 * abs(tail_terms[-1]))
    components = {
        "half_grid_delta": abs(primary - half),
        "coarse_G_delta": abs(primary - coarse),
        "pswf_alt_delta": abs(primary - alt),
        "tail_reserve": tail,
    }
    return float(sum(components.values()) + 1e-9), components


def load_step196_rows() -> list[dict[str, str]]:
    with STEP196_CSV.open(newline="") as f:
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

    step196_rows = load_step196_rows()
    out_rows = []
    comparison_rows = []
    for row in step196_rows:
        if int(row["k"]) == 0:
            out_rows.append({
                "case_id": row["case_id"],
                "rho_index": row["rho_index"],
                "gamma": row["gamma"],
                "k": row["k"],
                "G_id": row["G_id"],
                "proper_L_real": row["L_real"],
                "proper_L_imag": row["L_imag"],
                "proper_L_abs": row["L_abs"],
                "proper_error_bound": row["error_bound"],
                "proper_lower_bound_abs": row["lower_bound_abs"],
                "step196_L_abs": row["L_abs"],
                "abs_difference_vs_step196": "0.0000000000000000e+00",
                "method": "step196_k0_carried_forward",
                "verdict": row["verdict"],
            })
            continue
        gamma = float(row["gamma"])
        gd = generator_data[row["G_id"]]
        proper = projected_k1_proper(gamma, gd["F"], u_grid, pswf, gd["quad_data"], mod, N_TERMS_VALUE)
        err, components = k1_error(gamma, gd, u_grid, pswf, pswf_half, pswf_alt, mod)
        lower = max(0.0, abs(proper) - err)
        step196_val = complex(float(row["L_real"]), float(row["L_imag"]))
        diff = abs(proper - step196_val)
        verdict = "nonzero" if lower > 1e-3 else "indeterminate"
        out_rows.append({
            "case_id": row["case_id"],
            "rho_index": row["rho_index"],
            "gamma": row["gamma"],
            "k": row["k"],
            "G_id": row["G_id"],
            "proper_L_real": f"{proper.real:.16e}",
            "proper_L_imag": f"{proper.imag:.16e}",
            "proper_L_abs": f"{abs(proper):.16e}",
            "proper_error_bound": f"{err:.16e}",
            "proper_lower_bound_abs": f"{lower:.16e}",
            "step196_L_abs": row["L_abs"],
            "abs_difference_vs_step196": f"{diff:.16e}",
            "method": "analytic_derivative_of_projected_value",
            "verdict": verdict,
        })
        comparison_rows.append({
            "case_id": row["case_id"],
            "rho_index": row["rho_index"],
            "G_id": row["G_id"],
            "step196_finite_diff_real": row["L_real"],
            "step196_finite_diff_imag": row["L_imag"],
            "step196_abs": row["L_abs"],
            "proper_real": f"{proper.real:.16e}",
            "proper_imag": f"{proper.imag:.16e}",
            "proper_abs": f"{abs(proper):.16e}",
            "proper_error": f"{err:.16e}",
            "proper_lower": f"{lower:.16e}",
            "abs_difference": f"{diff:.16e}",
            "half_grid_delta": f"{components['half_grid_delta']:.16e}",
            "coarse_G_delta": f"{components['coarse_G_delta']:.16e}",
            "pswf_alt_delta": f"{components['pswf_alt_delta']:.16e}",
            "tail_reserve": f"{components['tail_reserve']:.16e}",
            "comparison_status": "consistent" if diff <= max(err, float(row["error_bound"])) else "different_but_same_nonzero_verdict",
        })

    with (BASE / "k1_proper_dataset_step247.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    k1_rows = [r for r in out_rows if r["k"] == "1"]
    min_abs = min(float(r["proper_L_abs"]) for r in k1_rows)
    min_lower = min(float(r["proper_lower_bound_abs"]) for r in k1_rows)
    max_diff = max(float(r["abs_difference_vs_step196"]) for r in k1_rows)
    status = "V_branch_C_k1_proper_foreclosure" if min_lower > 1e-3 else "V_branch_C_k1_proper_partial"
    status_rows = [
        {"metric": "k1_count", "value": str(len(k1_rows)), "comment": "proper k=1 rows recomputed"},
        {"metric": "k1_min_abs", "value": f"{min_abs:.16e}", "comment": "minimum proper |L| over k=1 rows"},
        {"metric": "k1_min_lower_bound", "value": f"{min_lower:.16e}", "comment": "minimum |L|-error over k=1 rows"},
        {"metric": "max_abs_difference_vs_step196_fd", "value": f"{max_diff:.16e}", "comment": "proper analytic derivative vs old central finite difference"},
        {"metric": "verdict", "value": status, "comment": "proper k=1 status"},
    ]
    with (BASE / "branch_C_k1_status_step247.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(status_rows[0].keys()))
        writer.writeheader()
        writer.writerows(status_rows)

    with (BASE / "robustness_step247.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(comparison_rows[0].keys()))
        writer.writeheader()
        writer.writerows(comparison_rows)

    payload = {
        "mpmath_dps": MP_DPS,
        "u_max": mod.U_MAX,
        "h": mod.H,
        "n_terms_value": N_TERMS_VALUE,
        "n_terms_tail": N_TERMS_TAIL,
        "k1_rows": comparison_rows,
        "status": status_rows,
    }
    (BASE / "k1_proper_results_step247.json").write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "Step 247 Branch C k=1 proper analytic derivative",
        f"mpmath_dps={MP_DPS} k1_count={len(k1_rows)}",
    ]
    for r in comparison_rows:
        lines.append(
            f"case={r['case_id']} rho{r['rho_index']} G={r['G_id']} "
            f"proper={float(r['proper_real']):+.10e}{float(r['proper_imag']):+.10e}j "
            f"abs={float(r['proper_abs']):.10e} err={float(r['proper_error']):.3e} "
            f"lower={float(r['proper_lower']):.10e} diff_vs_fd={float(r['abs_difference']):.3e}"
        )
    lines.append(f"verdict={status}")
    (BASE / "compute_step247_output.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
