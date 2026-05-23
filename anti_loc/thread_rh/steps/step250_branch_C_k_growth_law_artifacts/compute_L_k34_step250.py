#!/usr/bin/env python3
"""Compute Branch C k=3 and k=4 values and assemble k=0..4 dataset."""

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


BASE = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step250_branch_C_k_growth_law_artifacts")
STEP196_SCRIPT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/compute_branch_C_dataset_step196.py")
STEP196_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/dataset_triples_step196.csv")
STEP247_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step247_branch_C_k1_proper_artifacts/k1_proper_dataset_step247.csv")
STEP249_CSV = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step249_branch_C_k2_proper_artifacts/k2_proper_dataset_step249.csv")

MP_DPS = 80
N_TERMS_VALUE = 3
N_TERMS_TAIL = 12
TARGETS = [
    ("rho1_G_star", "1", "G_star"),
    ("rho2_G_star", "2", "G_star"),
    ("rho1_G_prime", "1", "G_prime"),
]


def load_step196_module():
    spec = importlib.util.spec_from_file_location("step196_branch_c", STEP196_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step196 module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step196_branch_c"] = mod
    spec.loader.exec_module(mod)
    mod.MP_DPS = MP_DPS
    return mod


def sinc_derivative_n(x: np.ndarray | float, n: int) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-5
    xm = arr[~mask]
    if n == 0:
        out[mask] = 1.0 / math.pi - arr[mask] ** 2 / (6 * math.pi) + arr[mask] ** 4 / (120 * math.pi)
        out[~mask] = np.sin(xm) / (math.pi * xm)
    elif n == 1:
        out[mask] = -arr[mask] / (3 * math.pi) + arr[mask] ** 3 / (30 * math.pi)
        out[~mask] = (xm * np.cos(xm) - np.sin(xm)) / (math.pi * xm ** 2)
    elif n == 2:
        out[mask] = -1.0 / (3 * math.pi) + arr[mask] ** 2 / (10 * math.pi) - arr[mask] ** 4 / (168 * math.pi)
        out[~mask] = (-xm * xm * np.sin(xm) - 2 * xm * np.cos(xm) + 2 * np.sin(xm)) / (math.pi * xm ** 3)
    elif n == 3:
        out[mask] = arr[mask] / (5 * math.pi) - arr[mask] ** 3 / (42 * math.pi) + arr[mask] ** 5 / (1080 * math.pi)
        out[~mask] = -(xm ** 3 * np.cos(xm) - 3 * xm ** 2 * np.sin(xm) - 6 * xm * np.cos(xm) + 6 * np.sin(xm)) / (math.pi * xm ** 4)
    elif n == 4:
        out[mask] = 1.0 / (5 * math.pi) - arr[mask] ** 2 / (14 * math.pi) + arr[mask] ** 4 / (216 * math.pi)
        out[~mask] = (xm ** 4 * np.sin(xm) + 4 * xm ** 3 * np.cos(xm) - 12 * xm ** 2 * np.sin(xm) - 24 * xm * np.cos(xm) + 24 * np.sin(xm)) / (math.pi * xm ** 5)
    else:
        raise ValueError("n must be 0..4")
    if np.isscalar(x):
        return float(out)
    return out


def zeta_derivative_at_s(gamma: float, order: int) -> complex:
    mp.mp.dps = MP_DPS
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(gamma)))
    return complex(mp.diff(lambda zz: mp.zeta(zz), s, order))


def mellin_s_derivative(gamma: float, quad_data, order: int) -> complex:
    # D=-i d/dgamma acts as d/ds on G(s)=int g(t)t^-s dt.
    t = quad_data["t"]
    w = quad_data["w"]
    g = quad_data["g"]
    amp = w * g * t ** (-0.5)
    factor = (-np.log(t)) ** order
    return complex((factor * np.exp(-1j * gamma * np.log(t))).dot(amp))


def delta_Dk(gamma: float, quad_data, k: int) -> complex:
    total = 0j
    for j in range(k + 1):
        total += math.comb(k, j) * zeta_derivative_at_s(gamma, j) * mellin_s_derivative(gamma, quad_data, k - j)
    return total


def psi_derivative_n_from_phi(gamma: float, x: np.ndarray, w: np.ndarray, mu: float, phi_n: np.ndarray, order: int) -> complex:
    int_val = sinc_derivative_n(gamma - x, order).dot(w * phi_n)
    return complex(((-1j) ** order) * (-int_val / math.sqrt(1.0 - mu)))


def projected_k(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, quad_data, k: int, n_terms: int) -> complex:
    delta = delta_Dk(gamma, quad_data, k)
    I = complex(simpson(((-1j) ** k) * sinc_derivative_n(gamma - u_grid, k) * F, x=u_grid))
    R = 0j
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_Dk = psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        R += psi_Dk * J_n
    return delta - I - R


def k_error(gamma: float, gd: dict, u_grid: np.ndarray, pswf, pswf_half, pswf_alt, mod, k: int):
    primary = projected_k(gamma, gd["F"], u_grid, pswf, gd["quad_data"], k, N_TERMS_VALUE)
    half = projected_k(gamma, gd["F"][::2], u_grid[::2], pswf_half, gd["quad_data"], k, N_TERMS_VALUE)
    coarse = projected_k(gamma, gd["F_coarse"], u_grid, pswf, gd["quad_data"], k, N_TERMS_VALUE)
    alt = projected_k(gamma, gd["F"], u_grid, pswf_alt, gd["quad_data"], k, N_TERMS_VALUE)
    tail_terms = []
    for n in range(N_TERMS_TAIL):
        mu = float(pswf["vals"][n])
        psi_Dk = psi_derivative_n_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n], k)
        J_n = complex(simpson(gd["F"] * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        tail_terms.append(psi_Dk * J_n)
    tail = float(sum(abs(t) for t in tail_terms[N_TERMS_VALUE:]) * 2.0 + 10.0 * abs(tail_terms[-1]))
    comps = {
        "half_grid_delta": abs(primary - half),
        "coarse_G_delta": abs(primary - coarse),
        "pswf_alt_delta": abs(primary - alt),
        "tail_reserve": tail,
    }
    return float(sum(comps.values()) + 1e-7), comps


def load_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def previous_value_for(k: int, rho_index: str, gid: str):
    if k == 0:
        rows = load_csv(STEP196_CSV)
        for r in rows:
            if r["k"] == "0" and r["rho_index"] == rho_index and r["G_id"] == gid:
                return float(r["L_abs"]), float(r["error_bound"])
    if k == 1:
        rows = load_csv(STEP247_CSV)
        for r in rows:
            if r["k"] == "1" and r["rho_index"] == rho_index and r["G_id"] == gid:
                return float(r["proper_L_abs"]), float(r["proper_error_bound"])
    if k == 2:
        rows = load_csv(STEP249_CSV)
        for r in rows:
            if r["k"] == "2" and r["rho_index"] == rho_index and r["G_id"] == gid:
                return float(r["proper_L_abs"]), float(r["proper_error_bound"])
    raise KeyError((k, rho_index, gid))


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

    rows = []
    output_lines = ["Step 250 Branch C k=3,k=4 computation", f"mpmath_dps={MP_DPS}"]
    for triple_id, rho_index, gid in TARGETS:
        gamma = mod.ZEROS[int(rho_index)]
        for k in [0, 1, 2]:
            val, err = previous_value_for(k, rho_index, gid)
            rows.append({
                "triple_id": triple_id,
                "rho_index": rho_index,
                "G_id": gid,
                "k": str(k),
                "L_abs": f"{val:.16e}",
                "error_bound": f"{err:.16e}",
                "lower_bound": f"{max(0.0, val-err):.16e}",
                "method": f"inherited_step_{196 if k==0 else 247 if k==1 else 249}",
            })
        gd = generator_data[gid]
        for k in [3, 4]:
            proper = projected_k(gamma, gd["F"], u_grid, pswf, gd["quad_data"], k, N_TERMS_VALUE)
            err, comps = k_error(gamma, gd, u_grid, pswf, pswf_half, pswf_alt, mod, k)
            lower = max(0.0, abs(proper) - err)
            rows.append({
                "triple_id": triple_id,
                "rho_index": rho_index,
                "G_id": gid,
                "k": str(k),
                "L_abs": f"{abs(proper):.16e}",
                "error_bound": f"{err:.16e}",
                "lower_bound": f"{lower:.16e}",
                "method": "analytic_higher_derivative_projected_value",
            })
            output_lines.append(
                f"triple={triple_id} k={k} L={proper.real:+.10e}{proper.imag:+.10e}j "
                f"abs={abs(proper):.10e} err={err:.3e} lower={lower:.10e}"
            )

    with (BASE / "k_dataset_step250.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (BASE / "compute_step250_output.txt").write_text("\\n".join(output_lines) + "\\n")
    (BASE / "k34_raw_step250.json").write_text(json.dumps({"rows": rows}, indent=2) + "\\n")
    print("\\n".join(output_lines))


if __name__ == "__main__":
    main()
