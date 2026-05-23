#!/usr/bin/env python3
"""Step 176 confirmation computations for Branch C foreclosure.

This script generalizes the Step 175 numerical machinery:
- mpmath zeta at 50 digits,
- Gauss-Legendre quadrature for legal Burnol generators,
- sinc-kernel diagonalization on [-1,1] for the Step 173 PSWF factors,
- U=200 and h=0.05 on the critical-line variable.
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


ROOT = Path(
    "/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/"
    "step176_branch_c_foreclosure_artifacts"
)

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

ZEROS = {
    "rho_1": 14.134725141734693,
    "rho_2": 21.022039638771554,
    "rho_3": 25.010857580145688,
}


@dataclass(frozen=True)
class GeneratorSpec:
    gid: str
    centers: tuple[float, float, float]
    epsilon: float


GENERATORS = {
    "G_star": GeneratorSpec("G_star", (1.5, 2.5, 3.5), 0.2),
    "G_prime": GeneratorSpec("G_prime", (2.0, 2.5, 3.0), 0.25),
}

CASES = [
    {"case_id": "rho2_G_star", "rho_label": "rho_2", "gamma": ZEROS["rho_2"], "G_id": "G_star"},
    {"case_id": "rho3_G_star", "rho_label": "rho_3", "gamma": ZEROS["rho_3"], "G_id": "G_star"},
    {"case_id": "rho1_G_prime", "rho_label": "rho_1", "gamma": ZEROS["rho_1"], "G_id": "G_prime"},
]


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
        A.append(
            float(
                quad(
                    lambda t, cc=c: bump(t, cc, spec.epsilon),
                    lo,
                    hi,
                    epsabs=1e-14,
                    epsrel=1e-14,
                    limit=200,
                )[0]
            )
        )
        B.append(
            float(
                quad(
                    lambda t, cc=c: bump(t, cc, spec.epsilon) / t,
                    lo,
                    hi,
                    epsabs=1e-14,
                    epsrel=1e-14,
                    limit=200,
                )[0]
            )
        )
    D = B[1] * A[2] - A[1] * B[2]
    alpha = (A[2] * B[0] - A[0] * B[2]) / D
    beta_3 = (A[1] * B[0] - A[0] * B[1]) / D
    return {
        "A_1": A[0],
        "A_2": A[1],
        "A_3": A[2],
        "B_1": B[0],
        "B_2": B[1],
        "B_3": B[2],
        "D": D,
        "alpha": alpha,
        "beta_3": beta_3,
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
    return values, checks


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
    psi_u = []
    for n in range(n_terms):
        psi_u.append(psi_grid_from_phi(u_grid, x, w, float(vals[n]), phi[:, n]))
    return {"x": x, "w": w, "vals": vals, "phi": phi, "psi_u": psi_u}


def case_terms(gamma: float, F: np.ndarray, u_grid: np.ndarray, pswf, n_terms: int):
    records = []
    terms = []
    for n in range(n_terms):
        mu = float(pswf["vals"][n])
        psi_rho = psi_gamma_from_phi(gamma, pswf["x"], pswf["w"], mu, pswf["phi"][:, n])
        J_n = complex(simpson(F * np.conjugate(pswf["psi_u"][n]), x=u_grid))
        term = psi_rho * J_n
        terms.append(term)
        records.append(
            {
                "n": n,
                "mu": mu,
                "Psi_rho_real": psi_rho.real,
                "Psi_rho_imag": psi_rho.imag,
                "J_real": J_n.real,
                "J_imag": J_n.imag,
                "term_real": term.real,
                "term_imag": term.imag,
                "term_abs": abs(term),
            }
        )
    return records, terms


def sinc_integral(gamma: float, u_grid: np.ndarray, F: np.ndarray) -> complex:
    return complex(simpson(sinc_kernel(gamma - u_grid) * F, x=u_grid))


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
    for gid, spec in GENERATORS.items():
        moments = compute_moments(spec)
        G_primary, checks = mellin_values(u_grid, spec, moments, N_T_PRIMARY)
        G_coarse, checks_coarse = mellin_values(u_grid, spec, moments, N_T_COARSE)
        generator_data[gid] = {
            "spec": spec,
            "moments": moments,
            "G_primary": G_primary,
            "G_coarse": G_coarse,
            "checks": checks,
            "checks_coarse": checks_coarse,
        }

    rows = []
    detail = []
    for case in CASES:
        gid = case["G_id"]
        gamma = float(case["gamma"])
        gdata = generator_data[gid]
        F = zeta_grid * gdata["G_primary"]
        F_coarse = zeta_grid * gdata["G_coarse"]

        I = sinc_integral(gamma, u_grid, F)
        I_half = sinc_integral(gamma, u_grid[::2], F[::2])
        mask_tail = np.abs(u_grid) <= U_TAIL_COMPARE
        I_u160 = sinc_integral(gamma, u_grid[mask_tail], F[mask_tail])
        I_g_coarse = sinc_integral(gamma, u_grid, F_coarse)
        I_error = abs(I - I_half) + 2.0 * abs(I - I_u160) + abs(I - I_g_coarse) + 1.0e-12

        records, terms = case_terms(gamma, F, u_grid, pswf, N_TERMS)
        _, terms_half = case_terms(gamma, F[::2], u_grid[::2], pswf_half, 3)
        _, terms_g_coarse = case_terms(gamma, F_coarse, u_grid, pswf, 3)
        _, terms_alt = case_terms(gamma, F, u_grid, pswf_alt, 3)

        pswf_sum_0_2 = sum(terms[:3], 0j)
        pswf_sum_extended = sum(terms, 0j)
        observed_tail = sum(terms[3:], 0j)
        observed_tail_abs_sum = float(sum(abs(t) for t in terms[3:]))
        tail_bound = max(1.0e-6, 2.0 * observed_tail_abs_sum + 10.0 * abs(terms[-1]))
        pswf_error = (
            sum(abs(terms[i] - terms_half[i]) for i in range(3))
            + sum(abs(terms[i] - terms_g_coarse[i]) for i in range(3))
            + sum(abs(terms[i] - terms_alt[i]) for i in range(3))
            + 1.0e-12
        )
        total_error = I_error + pswf_error + tail_bound + 1.0e-12
        L_0_2 = -I - pswf_sum_0_2
        L_extended = -I - pswf_sum_extended
        lower = max(0.0, abs(L_0_2) - total_error)
        verdict = "nonzero" if lower > 1.0e-3 else "indeterminate"

        rows.append(
            {
                "case_id": case["case_id"],
                "rho": f"1/2+{gamma:.15f}i",
                "k": 0,
                "G_id": gid,
                "L_real": f"{L_0_2.real:.16e}",
                "L_imag": f"{L_0_2.imag:.16e}",
                "L_abs": f"{abs(L_0_2):.16e}",
                "error_bound": f"{total_error:.16e}",
                "lower_bound_abs": f"{lower:.16e}",
                "I_sinc_real": f"{I.real:.16e}",
                "I_sinc_imag": f"{I.imag:.16e}",
                "pswf_sum_0_2_real": f"{pswf_sum_0_2.real:.16e}",
                "pswf_sum_0_2_imag": f"{pswf_sum_0_2.imag:.16e}",
                "pswf_tail_bound_n_ge_3": f"{tail_bound:.16e}",
                "verdict": verdict,
            }
        )
        detail.append(
            {
                **case,
                "rho": f"1/2+{gamma:.15f}i",
                "L_0_2": {"real": L_0_2.real, "imag": L_0_2.imag, "abs": abs(L_0_2)},
                "L_extended": {"real": L_extended.real, "imag": L_extended.imag, "abs": abs(L_extended)},
                "I_sinc": {"real": I.real, "imag": I.imag, "error": I_error},
                "pswf_sum_0_2": {"real": pswf_sum_0_2.real, "imag": pswf_sum_0_2.imag},
                "pswf_tail": {
                    "observed_real_3_to_11": observed_tail.real,
                    "observed_imag_3_to_11": observed_tail.imag,
                    "observed_abs_sum_3_to_11": observed_tail_abs_sum,
                    "bound_n_ge_3": tail_bound,
                },
                "pswf_first_three": records[:3],
                "errors": {
                    "I_error": I_error,
                    "pswf_error": pswf_error,
                    "total_error": total_error,
                    "lower_bound_abs": lower,
                },
                "verdict": verdict,
            }
        )

    write_csv(
        ROOT / "confirmation_data_points_step176.csv",
        rows,
        [
            "case_id",
            "rho",
            "k",
            "G_id",
            "L_real",
            "L_imag",
            "L_abs",
            "error_bound",
            "lower_bound_abs",
            "I_sinc_real",
            "I_sinc_imag",
            "pswf_sum_0_2_real",
            "pswf_sum_0_2_imag",
            "pswf_tail_bound_n_ge_3",
            "verdict",
        ],
    )

    result = {
        "constants": {
            "lambda": LAMBDA,
            "U": U_MAX,
            "h": H,
            "mp_dps": MP_DPS,
            "N_t_primary_per_support": N_T_PRIMARY,
            "N_t_coarse_per_support": N_T_COARSE,
            "N_pswf_primary": N_PSWF_PRIMARY,
            "N_pswf_alt": N_PSWF_ALT,
            "N_terms_extended": N_TERMS,
        },
        "generators": {
            gid: {
                "centers": list(data["spec"].centers),
                "epsilon": data["spec"].epsilon,
                "moments": data["moments"],
                "checks": data["checks"],
                "checks_coarse": data["checks_coarse"],
            }
            for gid, data in generator_data.items()
        },
        "confirmation_data_points": detail,
    }
    (ROOT / "confirmation_results_step176.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Step 176 confirmation computations")
    print(f"mpmath_dps={MP_DPS} U={U_MAX} h={H} lambda={LAMBDA}")
    for gid, data in generator_data.items():
        print(
            f"generator={gid} centers={data['spec'].centers} epsilon={data['spec'].epsilon} "
            f"alpha={data['moments']['alpha']:.16e} beta_3={data['moments']['beta_3']:.16e} "
            f"G0_res={data['checks']['endpoint_G0_residual']:.3e} "
            f"G1_res={data['checks']['endpoint_G1_residual']:.3e}"
        )
    for row in rows:
        print(
            "case={case_id} rho={rho} G={G_id} L={L} abs={absval:.16e} "
            "err={err:.16e} lower={lower:.16e} verdict={verdict}".format(
                case_id=row["case_id"],
                rho=row["rho"],
                G_id=row["G_id"],
                L=cfmt(complex(float(row["L_real"]), float(row["L_imag"]))),
                absval=float(row["L_abs"]),
                err=float(row["error_bound"]),
                lower=float(row["lower_bound_abs"]),
                verdict=row["verdict"],
            )
        )


if __name__ == "__main__":
    main()
