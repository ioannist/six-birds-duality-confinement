#!/usr/bin/env python3
"""Step 215 extended Branch A Weyl diagnostic."""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss


mp.mp.dps = 70

ROOT = Path("/home/repos/six-birds-foundations-iii")
BASE = ROOT / "anti_loc/thread/steps/step215_branch_A_weyl_extended_artifacts"
STEP202_SCRIPT = ROOT / "anti_loc/thread/steps/step202_xi_matrix_source_numerical_artifacts/compute_E_half_step202.py"

T_MAX = 100.0
N_GRID = 140
N_ZEROS_CAND1 = 20
N_ZEROS_CAND2 = 10
N_PSWF_EIGEN = 280
N_PSWF_TERMS = 24
ELL = math.log(2.0)
LAMBDA = 1.0


def load_step202_module():
    spec = importlib.util.spec_from_file_location("step202_E", STEP202_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Step202 E module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["step202_E"] = mod
    spec.loader.exec_module(mod)
    return mod


def sinc_kernel(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1e-12
    out[mask] = LAMBDA / math.pi
    out[~mask] = np.sin(LAMBDA * arr[~mask]) / (math.pi * arr[~mask])
    if np.isscalar(x):
        return float(out)
    return out


def pswf_eigensystem(n_nodes: int = N_PSWF_EIGEN):
    x, w = leggauss(n_nodes)
    sw = np.sqrt(w)
    k = sinc_kernel(x[:, None] - x[None, :])
    mat = sw[:, None] * k * sw[None, :]
    vals, vecs = np.linalg.eigh(mat)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    phi = vecs / sw[:, None]
    return x, w, vals, phi


def psi_from_phi(tau: np.ndarray, x_nodes: np.ndarray, weights: np.ndarray, mu: float, phi_values: np.ndarray) -> np.ndarray:
    int_k = sinc_kernel(tau[:, None] - x_nodes[None, :]).dot(weights * phi_values)
    inside = np.abs(tau) <= LAMBDA
    psi = np.empty_like(int_k, dtype=np.complex128)
    psi[~inside] = -int_k[~inside] / math.sqrt(max(1e-300, 1 - mu))
    psi[inside] = (math.sqrt(max(1e-300, 1 - mu)) / mu) * int_k[inside]
    return psi


def build_psi_matrix(tau: np.ndarray, n_terms: int = N_PSWF_TERMS) -> np.ndarray:
    x, w, vals, phi = pswf_eigensystem()
    return np.array([psi_from_phi(tau, x, w, float(vals[n]), phi[:, n]) for n in range(n_terms)])


def p_operator(f: np.ndarray, tau: np.ndarray, weights: np.ndarray, psis: np.ndarray) -> np.ndarray:
    sinc_part = sinc_kernel(tau[:, None] - tau[None, :]).dot(weights * f)
    pswf_part = np.zeros_like(f, dtype=np.complex128)
    for psi in psis:
        inner = np.sum(weights * np.conjugate(psi) * f)
        pswf_part += psi * inner
    return f - sinc_part - pswf_part


def l2_inner(f: np.ndarray, g: np.ndarray, weights: np.ndarray) -> complex:
    return complex(np.sum(weights * np.conjugate(f) * g) / (2 * math.pi))


def l2_norm(f: np.ndarray, weights: np.ndarray) -> float:
    return math.sqrt(max(0.0, l2_inner(f, f, weights).real))


def c_norm_for(kappa: np.ndarray, tau: np.ndarray, weights: np.ndarray, psis: np.ndarray, ell: float = ELL) -> float:
    pk = p_operator(kappa, tau, weights, psis)
    phase = np.exp(1j * ell * tau)
    h = phase * pk - p_operator(phase * pk, tau, weights, psis)
    return l2_norm(h, weights) / max(l2_norm(kappa, weights), 1e-300)


def zeros(nmax: int) -> dict[int, mp.mpc]:
    return {n: mp.zetazero(n) for n in range(1, nmax + 1)}


def cand1_kappas(tau: np.ndarray, zetas: dict[int, mp.mpc]) -> dict[int, np.ndarray]:
    mod = load_step202_module()
    data = mod.build_resolvent(100)
    e_grid = []
    for tv in tau:
        s = mp.mpc(mp.mpf("0.5"), mp.mpf(str(float(tv))))
        val, _, _ = mod.e_lambda(s, data)
        e_grid.append(complex(val))
    e_grid = np.array(e_grid, dtype=np.complex128)
    e_1_grid = np.conjugate(e_grid)
    s_grid = 0.5 + 1j * tau
    out = {}
    for n, rho in zetas.items():
        erho, _, _ = mod.e_lambda(rho, data)
        erho_c = complex(erho)
        rho_c = complex(float(mp.re(rho)), float(mp.im(rho)))
        out[n] = (e_grid * erho_c - e_1_grid * np.conjugate(erho_c)) / (s_grid + rho_c - 1.0)
    return out


def zeta_prime(s: mp.mpc) -> mp.mpc:
    return mp.diff(lambda z: mp.zeta(z), s)


def cand2_kappas(tau: np.ndarray, zetas: dict[int, mp.mpc]) -> dict[int, np.ndarray]:
    s_values = [mp.mpc(mp.mpf("0.5"), mp.mpf(str(float(tv)))) for tv in tau]
    zeta_grid = [mp.zeta(s) for s in s_values]
    out = {}
    for n, rho in zetas.items():
        zp = zeta_prime(rho)
        comp = mp.power(mp.pi, -rho / 2) * mp.gamma(rho / 2)
        vals = []
        for s, zeta_s in zip(s_values, zeta_grid, strict=True):
            vals.append(complex(zeta_s / ((s - rho) * zp * comp)))
        out[n] = np.array(vals, dtype=np.complex128)
    return out


def normalized_inner_products(kappas: dict[int, np.ndarray], weights: np.ndarray) -> list[dict[str, object]]:
    norms = {n: l2_norm(k, weights) for n, k in kappas.items()}
    rows = []
    keys = sorted(kappas)
    for a_idx, i in enumerate(keys):
        ui = kappas[i] / max(norms[i], 1e-300)
        for j in keys[a_idx + 1 :]:
            uj = kappas[j] / max(norms[j], 1e-300)
            ip = l2_inner(ui, uj, weights)
            rows.append(
                {
                    "i": i,
                    "j": j,
                    "inner_real": f"{ip.real:.17e}",
                    "inner_imag": f"{ip.imag:.17e}",
                    "inner_abs": f"{abs(ip):.17e}",
                    "status": "finite_grid_CAND1_normalized_inner_product",
                }
            )
    return rows


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    raw_x, raw_w = leggauss(N_GRID)
    tau = T_MAX * raw_x
    weights = T_MAX * raw_w
    z20 = zeros(N_ZEROS_CAND1)
    psis = build_psi_matrix(tau)

    c1 = cand1_kappas(tau, z20)
    z10 = {n: z20[n] for n in range(1, N_ZEROS_CAND2 + 1)}
    c2 = cand2_kappas(tau, z10)

    rows = []
    for n in range(1, N_ZEROS_CAND1 + 1):
        gamma = float(mp.im(z20[n]))
        norm_c1 = c_norm_for(c1[n], tau, weights, psis)
        norm_c2 = c_norm_for(c2[n], tau, weights, psis) if n in c2 else None
        rows.append(
            {
                "n": n,
                "gamma_n": f"{gamma:.15f}",
                "CAND1_C_l_u_n_norm": f"{norm_c1:.17e}",
                "CAND2_C_l_u_n_norm": f"{norm_c2:.17e}" if norm_c2 is not None else "",
                "error_bound": "5.0e-2",
                "status": "diagnostic_finite_grid",
            }
        )
    with (BASE / "weyl_extended_step215.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    ip_rows = normalized_inner_products(c1, weights)
    with (BASE / "weak_null_inner_products_step215.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ip_rows[0].keys()))
        writer.writeheader()
        writer.writerows(ip_rows)

    c1_vals = np.array([float(r["CAND1_C_l_u_n_norm"]) for r in rows])
    c2_vals = np.array([float(r["CAND2_C_l_u_n_norm"]) for r in rows[:N_ZEROS_CAND2]])
    tail_vals = c1_vals[10:]
    lower_c1 = max(0.0, float(np.min(c1_vals) - 0.05))
    lower_c1_tail = max(0.0, float(np.min(tail_vals) - 0.05))
    lower_c2 = max(0.0, float(np.min(c2_vals) - 0.05))
    max_ip_all = max(float(r["inner_abs"]) for r in ip_rows)
    max_ip_tail = max(float(r["inner_abs"]) for r in ip_rows if int(r["i"]) >= 11 and int(r["j"]) >= 11)

    if lower_c1 > 0.5 and lower_c2 > 0.5 and max_ip_tail < 0.25:
        verdict = "V_weyl_extended_obstruction_certified"
    elif lower_c1 > 0.5 and lower_c2 > 0.1:
        verdict = "V_weyl_extended_obstruction_diagnostic"
    elif c1_vals[-1] < c1_vals[0] / 5:
        verdict = "V_weyl_extended_decay"
    else:
        verdict = "V_weyl_extended_partial"

    trend = "tail_bounded_below" if lower_c1_tail > 0.5 else "tail_uncertain"
    with (BASE / "lim_inf_analysis_step215.csv").open("w", newline="") as f:
        fieldnames = [
            "CAND1_min_1_20",
            "CAND1_lower_after_error",
            "CAND1_tail_min_11_20",
            "CAND1_tail_lower_after_error",
            "CAND2_min_1_10",
            "CAND2_lower_after_error",
            "max_inner_abs_all",
            "max_inner_abs_tail_11_20",
            "trend",
            "verdict",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "CAND1_min_1_20": f"{float(np.min(c1_vals)):.17e}",
                "CAND1_lower_after_error": f"{lower_c1:.17e}",
                "CAND1_tail_min_11_20": f"{float(np.min(tail_vals)):.17e}",
                "CAND1_tail_lower_after_error": f"{lower_c1_tail:.17e}",
                "CAND2_min_1_10": f"{float(np.min(c2_vals)):.17e}",
                "CAND2_lower_after_error": f"{lower_c2:.17e}",
                "max_inner_abs_all": f"{max_ip_all:.17e}",
                "max_inner_abs_tail_11_20": f"{max_ip_tail:.17e}",
                "trend": trend,
                "verdict": verdict,
                "notes": "Certified here means finite-grid/candidate-model diagnostic; full theorem still requires transport and weak-null proof.",
            }
        )

    print("Step 215 extended Weyl diagnostic")
    for r in rows:
        print(
            f"n={int(r['n']):02d} gamma={float(r['gamma_n']):.6f} "
            f"CAND1={float(r['CAND1_C_l_u_n_norm']):.6e} "
            f"CAND2={r['CAND2_C_l_u_n_norm'] or 'NA'}"
        )
    print(f"CAND1 lower after error={lower_c1:.8e}, tail lower={lower_c1_tail:.8e}")
    print(f"CAND2 lower after error={lower_c2:.8e}")
    print(f"max inner all={max_ip_all:.8e}, tail={max_ip_tail:.8e}")
    print(f"verdict={verdict}")


if __name__ == "__main__":
    main()
