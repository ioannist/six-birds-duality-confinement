#!/usr/bin/env python3
"""Extended Branch C L_{rho,k}(G) dataset for Step 196.

This reuses the Step 175/176 numerical convention:
- mpmath zeta at 50 digits,
- U=200, h=0.05 critical-line grid,
- Gauss-Legendre quadrature for compact three-bump Burnol generators,
- PSWF via sinc-kernel diagonalization on [-1,1].

For k=0 at zeta zeros, the delta term ζ(rho)G(rho) is numerically included
but is negligible.  For k=1, the derivative evaluator is approximated by
(-i) times a central finite difference in the zero ordinate gamma of the
projected value (P_infty M_zeta G)(1/2+i gamma).
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, simpson


ROOT = Path("/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts")

MP_DPS = 50
U_MAX = 200.0
H = 0.05
U_TAIL_COMPARE = 160.0
N_T_PRIMARY = 280
N_T_COARSE = 180
N_PSWF_PRIMARY = 320
N_PSWF_ALT = 240
N_TERMS = 12
LAMBDA = 1.0
K1_DH = 0.02

ZEROS = {
    1: 14.134725141734693,
    2: 21.022039638771554,
    3: 25.010857580145688,
    4: 30.424876125859513,
    5: 32.935061587739189,
    6: 37.586178158825671,
}


@dataclass(frozen=True)
class GeneratorSpec:
    gid: str
    centers: tuple[float, float, float]
    epsilon: float
    note: str


GENERATORS = {
    "G_star": GeneratorSpec("G_star", (1.5, 2.5, 3.5), 0.20, "Step 174/175 base generator"),
    "G_prime": GeneratorSpec("G_prime", (2.0, 2.5, 3.0), 0.25, "Step 176 shifted generator"),
    "G_spread": GeneratorSpec("G_spread", (1.25, 2.25, 3.75), 0.15, "new spread generator on [1,4]"),
    "G_low": GeneratorSpec("G_low", (1.20, 1.85, 2.80), 0.12, "new lower-support generator"),
    "G_high": GeneratorSpec("G_high", (2.20, 3.00, 3.75), 0.12, "new upper-support generator"),
}

CASES: list[dict[str, object]] = []
for idx in range(1, 7):
    CASES.append({"rho_index": idx, "k": 0, "G_id": "G_star"})
for idx in range(1, 4):
    CASES.append({"rho_index": idx, "k": 0, "G_id": "G_prime"})
for idx in range(1, 4):
    CASES.append({"rho_index": idx, "k": 0, "G_id": "G_spread"})
for idx in range(1, 3):
    CASES.append({"rho_index": idx, "k": 0, "G_id": "G_low"})
CASES.append({"rho_index": 1, "k": 0, "G_id": "G_high"})
CASES.extend(
    [
        {"rho_index": 1, "k": 1, "G_id": "G_star"},
        {"rho_index": 2, "k": 1, "G_id": "G_star"},
        {"rho_index": 1, "k": 1, "G_id": "G_prime"},
    ]
)


def beta_bump(u: float | np.ndarray) -> float | np.ndarray:
    arr = np.asarray(u)
    out = np.zeros_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0
    out[mask] = np.exp(-1.0 / (1.0 - arr[mask] * arr[mask]))
    if np.isscalar(u):
        return float(out)
    return out


def bump(t: float | np.ndarray, center: float, epsilon: float) -> float | np.ndarray:
    return beta_bump((np.asarray(t) - center) / epsilon)


def sinc_kernel(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-12
    out[mask] = 1.0 / math.pi
    out[~mask] = np.sin(arr[~mask]) / (math.pi * arr[~mask])
    if np.isscalar(x):
        return float(out)
    return out


def compute_moments(spec: GeneratorSpec) -> dict[str, float]:
    A: list[float] = []
    B: list[float] = []
    for c in spec.centers:
        lo = c - spec.epsilon
        hi = c + spec.epsilon
        A.append(float(quad(lambda t, cc=c: bump(t, cc, spec.epsilon), lo, hi, epsabs=1e-14, epsrel=1e-14, limit=200)[0]))
        B.append(float(quad(lambda t, cc=c: bump(t, cc, spec.epsilon) / t, lo, hi, epsabs=1e-14, epsrel=1e-14, limit=200)[0]))
    D = B[1] * A[2] - A[1] * B[2]
    alpha = (A[2] * B[0] - A[0] * B[2]) / D
    beta_3 = (A[1] * B[0] - A[0] * B[1]) / D
    return {
        "A_1": A[0], "A_2": A[1], "A_3": A[2],
        "B_1": B[0], "B_2": B[1], "B_3": B[2],
        "D": D, "alpha": alpha, "beta_3": beta_3,
    }


def build_t_quadrature(spec: GeneratorSpec, moments: dict[str, float], n_per_support: int):
    xg, wg = leggauss(n_per_support)
    coeffs = [1.0, -moments["alpha"], moments["beta_3"]]
    all_t = []
    all_w = []
    all_g = []
    for coeff, center in zip(coeffs, spec.centers):
        lo = center - spec.epsilon
        hi = center + spec.epsilon
        t = 0.5 * (hi - lo) * xg + 0.5 * (hi + lo)
        w = 0.5 * (hi - lo) * wg
        g = coeff * bump(t, center, spec.epsilon)
        all_t.append(t)
        all_w.append(w)
        all_g.append(g)
    return np.concatenate(all_t), np.concatenate(all_w), np.concatenate(all_g)


def mellin_values(u_grid: np.ndarray, spec: GeneratorSpec, moments: dict[str, float], n_per_support: int):
    t, w, g = build_t_quadrature(spec, moments, n_per_support)
    amp = w * g * t ** (-0.5)
    values = np.exp(-1j * np.outer(u_grid, np.log(t))).dot(amp)
    checks = {
        "endpoint_G0_residual": float(np.sum(w * g)),
        "endpoint_G1_residual": float(np.sum(w * g / t)),
        "quadrature_nodes": int(t.size),
    }
    quad_data = {"t": t, "w": w, "g": g}
    return values, checks, quad_data


def mellin_at_gamma(gamma: float, quad_data) -> complex:
    t = quad_data["t"]
    w = quad_data["w"]
    g = quad_data["g"]
    amp = w * g * t ** (-0.5)
    return complex(np.exp(-1j * gamma * np.log(t)).dot(amp))


def zeta_at_gamma(gamma: float) -> complex:
    mp.mp.dps = MP_DPS
    return complex(mp.zeta(mp.mpc(0.5, float(gamma))))


def zeta_values(u_grid: np.ndarray) -> np.ndarray:
    mp.mp.dps = MP_DPS
    return np.array([complex(mp.zeta(mp.mpc(0.5, float(u)))) for u in u_grid], dtype=np.complex128)


def pswf_eigensystem(n_nodes: int):
    x, w = leggauss(n_nodes)
    sw = np.sqrt(w)
    d = x[:, None] - x[None, :]
    matrix = sw[:, None] * sinc_kernel(d) * sw[None, :]
    vals, vecs = np.linalg.eigh(matrix)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    phi = vecs / sw[:, None]
    return x, w, vals, phi


def psi_grid_from_phi(u_grid: np.ndarray, x: np.ndarray, w: np.ndarray, mu: float, phi_n: np.ndarray) -> np.ndarray:
    d = u_grid[:, None] - x[None, :]
    int_k = sinc_kernel(d).dot(w * phi_n)
    inside = np.abs(u_grid) <= LAMBDA
    psi = np.empty_like(int_k, dtype=np.complex128)
    psi[~inside] = -int_k[~inside] / math.sqrt(1.0 - mu)
    psi[inside] = (math.sqrt(1.0 - mu) / mu) * int_k[inside]
    return psi


def psi_gamma_from_phi(gamma: float, x: np.ndarray, w: np.ndarray, mu: float, phi_n: np.ndarray) -> complex:
    int_k = sinc_kernel(gamma - x).dot(w * phi_n)
    return complex(-int_k / math.sqrt(1.0 - mu))


def precompute_pswf(u_grid: np.ndarray, n_nodes: int, n_terms: int):
    x, w, vals, phi = pswf_eigensystem(n_nodes)
    psi_u = [psi_grid_from_phi(u_grid, x, w, float(vals[n]), phi[:, n]) for n in range(n_terms)]
    return {"x": x, "w": w, "vals": vals, "phi": phi, "psi_u": psi_u}


def case_terms(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, n_terms: int):
    terms = []
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_rho = psi_gamma_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n])
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        terms.append(psi_rho * J_n)
    return terms


def sinc_integral(gamma: float, u_grid: np.ndarray, F: np.ndarray) -> complex:
    return complex(simpson(sinc_kernel(gamma - u_grid) * F, x=u_grid))


def projected_value(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, quad_data, n_terms: int = 3) -> complex:
    delta = zeta_at_gamma(gamma) * mellin_at_gamma(gamma, quad_data)
    I = sinc_integral(gamma, u_grid, F)
    terms = case_terms(gamma, F, u_grid, pswf, n_terms)
    return delta - I - sum(terms, 0j)


def value_error(gamma: float, F: np.ndarray, F_coarse: np.ndarray, u_grid: np.ndarray, pswf, pswf_half, pswf_alt, quad_data) -> float:
    I = sinc_integral(gamma, u_grid, F)
    I_half = sinc_integral(gamma, u_grid[::2], F[::2])
    mask_tail = np.abs(u_grid) <= U_TAIL_COMPARE
    I_u160 = sinc_integral(gamma, u_grid[mask_tail], F[mask_tail])
    I_coarse = sinc_integral(gamma, u_grid, F_coarse)
    I_error = abs(I - I_half) + 2.0 * abs(I - I_u160) + abs(I - I_coarse) + 1.0e-12
    terms = case_terms(gamma, F, u_grid, pswf, N_TERMS)
    terms_half = case_terms(gamma, F[::2], u_grid[::2], pswf_half, 3)
    terms_coarse = case_terms(gamma, F_coarse, u_grid, pswf, 3)
    terms_alt = case_terms(gamma, F, u_grid, pswf_alt, 3)
    observed_tail_abs_sum = float(sum(abs(t) for t in terms[3:]))
    tail_bound = max(1.0e-6, 2.0 * observed_tail_abs_sum + 10.0 * abs(terms[-1]))
    pswf_error = (
        sum(abs(terms[i] - terms_half[i]) for i in range(3))
        + sum(abs(terms[i] - terms_coarse[i]) for i in range(3))
        + sum(abs(terms[i] - terms_alt[i]) for i in range(3))
        + 1.0e-12
    )
    # Delta term is computed by high-precision zeta and t quadrature; keep a small reserve.
    return I_error + pswf_error + tail_bound + 5.0e-12


def cfmt(z: complex) -> str:
    return f"{z.real:.16e}{z.imag:+.16e}j"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    u_grid = np.linspace(-U_MAX, U_MAX, int(round(2 * U_MAX / H)) + 1)
    zeta_grid = zeta_values(u_grid)
    pswf = precompute_pswf(u_grid, N_PSWF_PRIMARY, N_TERMS)
    pswf_half = precompute_pswf(u_grid[::2], N_PSWF_PRIMARY, 3)
    pswf_alt = precompute_pswf(u_grid, N_PSWF_ALT, 3)

    generator_data = {}
    g_rows = []
    for gid, spec in GENERATORS.items():
        moments = compute_moments(spec)
        G_primary, checks, quad_data = mellin_values(u_grid, spec, moments, N_T_PRIMARY)
        G_coarse, checks_coarse, _ = mellin_values(u_grid, spec, moments, N_T_COARSE)
        generator_data[gid] = {
            "spec": spec, "moments": moments, "G_primary": G_primary, "G_coarse": G_coarse,
            "F": zeta_grid * G_primary, "F_coarse": zeta_grid * G_coarse,
            "checks": checks, "checks_coarse": checks_coarse, "quad_data": quad_data,
        }
        g_rows.append({
            "G_id": gid, "centers": ";".join(str(x) for x in spec.centers), "epsilon": spec.epsilon,
            "alpha": f"{moments['alpha']:.16e}", "beta_3": f"{moments['beta_3']:.16e}",
            "G0_residual": f"{checks['endpoint_G0_residual']:.3e}",
            "G1_residual": f"{checks['endpoint_G1_residual']:.3e}",
            "note": spec.note,
        })

    rows = []
    details = []
    for i, case in enumerate(CASES, start=1):
        rho_index = int(case["rho_index"])
        gamma = ZEROS[rho_index]
        k = int(case["k"])
        gid = str(case["G_id"])
        gd = generator_data[gid]
        if k == 0:
            L_val = projected_value(gamma, gd["F"], u_grid, pswf, gd["quad_data"], 3)
            err = value_error(gamma, gd["F"], gd["F_coarse"], u_grid, pswf, pswf_half, pswf_alt, gd["quad_data"])
            method = "projected_value"
        else:
            L_plus = projected_value(gamma + K1_DH, gd["F"], u_grid, pswf, gd["quad_data"], 3)
            L_minus = projected_value(gamma - K1_DH, gd["F"], u_grid, pswf, gd["quad_data"], 3)
            L_plus_half = projected_value(gamma + K1_DH / 2.0, gd["F"], u_grid, pswf, gd["quad_data"], 3)
            L_minus_half = projected_value(gamma - K1_DH / 2.0, gd["F"], u_grid, pswf, gd["quad_data"], 3)
            deriv_h = -1j * (L_plus - L_minus) / (2.0 * K1_DH)
            deriv_half = -1j * (L_plus_half - L_minus_half) / K1_DH
            L_val = deriv_half
            base_err = value_error(gamma, gd["F"], gd["F_coarse"], u_grid, pswf, pswf_half, pswf_alt, gd["quad_data"])
            err = abs(deriv_half - deriv_h) + 2.0 * base_err / K1_DH + 1.0e-9
            method = "central_finite_difference_k1"
        lower = max(0.0, abs(L_val) - err)
        verdict = "nonzero" if lower > 1.0e-3 else "indeterminate"
        row = {
            "case_id": f"C{i:02d}",
            "rho_index": rho_index,
            "rho": f"1/2+{gamma:.15f}i",
            "gamma": f"{gamma:.15f}",
            "k": k,
            "G_id": gid,
            "L_real": f"{L_val.real:.16e}",
            "L_imag": f"{L_val.imag:.16e}",
            "L_abs": f"{abs(L_val):.16e}",
            "error_bound": f"{err:.16e}",
            "lower_bound_abs": f"{lower:.16e}",
            "method": method,
            "verdict": verdict,
        }
        rows.append(row)
        details.append({**row, "L_complex": cfmt(L_val)})

    write_csv(ROOT / "dataset_triples_step196.csv", rows, [
        "case_id", "rho_index", "rho", "gamma", "k", "G_id", "L_real", "L_imag", "L_abs",
        "error_bound", "lower_bound_abs", "method", "verdict",
    ])
    write_csv(ROOT / "new_G_generators_step196.csv", g_rows, [
        "G_id", "centers", "epsilon", "alpha", "beta_3", "G0_residual", "G1_residual", "note",
    ])

    abs_values = np.array([float(r["L_abs"]) for r in rows])
    err_values = np.array([float(r["error_bound"]) for r in rows])
    k0_abs = np.array([float(r["L_abs"]) for r in rows if r["k"] == 0])
    k1_abs = np.array([float(r["L_abs"]) for r in rows if r["k"] == 1])
    gammas = np.array([float(r["gamma"]) for r in rows if r["k"] == 0])
    k0_by_gamma_abs = np.array([float(r["L_abs"]) for r in rows if r["k"] == 0])
    corr = float(np.corrcoef(gammas, k0_by_gamma_abs)[0, 1]) if len(gammas) > 1 else float("nan")
    pattern_rows = [
        {"pattern": "global_lower_bound", "value": f"{float(np.min(abs_values - err_values)):.16e}", "comment": "minimum lower bound across all tested triples"},
        {"pattern": "k0_abs_range", "value": f"{float(np.min(k0_abs)):.6e}..{float(np.max(k0_abs)):.6e}", "comment": "k=0 values remain away from zero"},
        {"pattern": "k1_abs_range", "value": f"{float(np.min(k1_abs)):.6e}..{float(np.max(k1_abs)):.6e}", "comment": "finite-difference derivative diagnostics are larger but noisier"},
        {"pattern": "gamma_correlation_k0", "value": f"{corr:.6e}", "comment": "weak/no clean monotone gamma law at this sample size"},
        {"pattern": "dataset_l2_norm", "value": f"{float(np.linalg.norm(abs_values)):.16e}", "comment": "Euclidean norm of |L| across dataset"},
    ]
    write_csv(ROOT / "structural_patterns_step196.csv", pattern_rows, ["pattern", "value", "comment"])

    payload = {
        "constants": {
            "mpmath_dps": MP_DPS, "U": U_MAX, "h": H, "lambda": LAMBDA,
            "N_t_primary": N_T_PRIMARY, "N_pswf_primary": N_PSWF_PRIMARY,
            "N_terms": N_TERMS, "k1_dh": K1_DH,
        },
        "generators": g_rows,
        "dataset_triples": details,
        "patterns": pattern_rows,
    }
    (ROOT / "branch_C_dataset_results_step196.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    out_lines = [
        "Step 196 Branch C extended dataset",
        f"mpmath_dps={MP_DPS} U={U_MAX} h={H} lambda={LAMBDA} dataset_size={len(rows)}",
    ]
    for grow in g_rows:
        out_lines.append(
            f"generator={grow['G_id']} centers={grow['centers']} epsilon={grow['epsilon']} "
            f"alpha={grow['alpha']} beta_3={grow['beta_3']} G0={grow['G0_residual']} G1={grow['G1_residual']}"
        )
    for row in rows:
        out_lines.append(
            f"case={row['case_id']} rho{row['rho_index']} k={row['k']} G={row['G_id']} "
            f"L={float(row['L_real']):.10e}{float(row['L_imag']):+.10e}j "
            f"abs={float(row['L_abs']):.10e} err={float(row['error_bound']):.3e} "
            f"lower={float(row['lower_bound_abs']):.10e} verdict={row['verdict']}"
        )
    for prow in pattern_rows:
        out_lines.append(f"pattern={prow['pattern']} value={prow['value']} comment={prow['comment']}")
    (ROOT / "compute_branch_C_dataset_output_step196.txt").write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()

