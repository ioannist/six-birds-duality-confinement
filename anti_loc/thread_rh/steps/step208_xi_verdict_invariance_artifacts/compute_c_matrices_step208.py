#!/usr/bin/env python3
"""Step 208: compute c_ij under both kappa candidates.

This is a diagnostic finite-grid implementation of Step 173:

    P f = f - sinc*f - sum_n Psi_n <Psi_n,f>
    C f = (I-P) M_{m_l} P f,  M_{m_l}(tau)=exp(i*l*tau).

The input kappa samples are the Step 207 CAND1/CAND2 grids.  No claim is made
that either candidate is the true transport sample.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path("/home/repos/six-birds-foundations-iii")
STEP207 = ROOT / "anti_loc/thread/steps/step207_kappa_candidates_comparison_artifacts"
BASE = ROOT / "anti_loc/thread/steps/step208_xi_verdict_invariance_artifacts"

T_MAX = 40.0
N_GRID_MAIN = 200
LAMBDA = 1.0
ELL_MAIN = math.log(2.0)
N_PSWF_MAIN = 24
N_PSWF_EIGEN = 320


def sinc_kernel(x: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(x, dtype=float)
    out = np.empty_like(arr, dtype=float)
    mask = np.abs(arr) < 1.0e-12
    out[mask] = LAMBDA / math.pi
    out[~mask] = np.sin(LAMBDA * arr[~mask]) / (math.pi * arr[~mask])
    if np.isscalar(x):
        return float(out)
    return out


def pswf_eigensystem(n_nodes: int = N_PSWF_EIGEN) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x, w = leggauss(n_nodes)
    sw = np.sqrt(w)
    d = x[:, None] - x[None, :]
    k = sinc_kernel(d)
    mat = sw[:, None] * k * sw[None, :]
    vals, vecs = np.linalg.eigh(mat)
    order = np.argsort(vals)[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    phi = vecs / sw[:, None]
    return x, w, vals, phi


def psi_from_phi(
    tau: np.ndarray,
    x_nodes: np.ndarray,
    weights: np.ndarray,
    mu: float,
    phi_values: np.ndarray,
) -> np.ndarray:
    d = tau[:, None] - x_nodes[None, :]
    int_k = sinc_kernel(d).dot(weights * phi_values)
    inside = np.abs(tau) <= LAMBDA
    psi = np.empty_like(int_k, dtype=np.complex128)
    psi[~inside] = -int_k[~inside] / math.sqrt(max(1.0e-300, 1.0 - mu))
    psi[inside] = (math.sqrt(max(1.0e-300, 1.0 - mu)) / mu) * int_k[inside]
    return psi


@dataclass
class CandidateResult:
    candidate: str
    c: np.ndarray
    c_abs_max: float
    c_fro: float
    n_pswf_terms: int
    grid_nodes: int
    ell: float


def load_samples(name: str) -> tuple[np.ndarray, dict[int, np.ndarray]]:
    path = STEP207 / f"{name}_samples_step207.csv"
    rows = list(csv.DictReader(path.open(newline="")))
    by_i: dict[int, list[complex]] = {1: [], 2: [], 3: []}
    tau_by_i: dict[int, list[float]] = {1: [], 2: [], 3: []}
    real_col = f"{name}_real"
    imag_col = f"{name}_imag"
    for row in rows:
        idx = int(row["rho_index"])
        tau_by_i[idx].append(float(row["tau"]))
        by_i[idx].append(complex(float(row[real_col]), float(row[imag_col])))
    tau = np.array(tau_by_i[1], dtype=float)
    out = {i: np.array(by_i[i], dtype=np.complex128) for i in [1, 2, 3]}
    return tau, out


def gl_weights_for_grid(n: int, t_max: float = T_MAX) -> tuple[np.ndarray, np.ndarray]:
    x, w = leggauss(n)
    return t_max * x, t_max * w


def align_weights(tau: np.ndarray) -> np.ndarray:
    # Step 207/205 used T_MAX*leggauss(200).  Recreate weights and check order.
    full_tau, full_w = gl_weights_for_grid(N_GRID_MAIN)
    if len(tau) == N_GRID_MAIN and np.allclose(tau, full_tau, rtol=0, atol=5e-14):
        return full_w
    # Subsample fallback: use nearest inherited full weights.
    weights = []
    for t in tau:
        j = int(np.argmin(np.abs(full_tau - t)))
        weights.append(full_w[j])
    return np.array(weights, dtype=float)


def build_psi_matrix(tau: np.ndarray, n_terms: int) -> np.ndarray:
    x, w, vals, phi = pswf_eigensystem()
    psis = []
    for n in range(n_terms):
        psis.append(psi_from_phi(tau, x, w, float(vals[n]), phi[:, n]))
    return np.array(psis, dtype=np.complex128)


def p_operator(f: np.ndarray, tau: np.ndarray, weights: np.ndarray, psis: np.ndarray) -> np.ndarray:
    d = tau[:, None] - tau[None, :]
    sinc_part = sinc_kernel(d).dot(weights * f)
    pswf_part = np.zeros_like(f, dtype=np.complex128)
    for psi in psis:
        inner = np.sum(weights * np.conjugate(psi) * f)
        pswf_part += psi * inner
    return f - sinc_part - pswf_part


def c_matrix_for_samples(
    samples: dict[int, np.ndarray],
    tau: np.ndarray,
    weights: np.ndarray,
    n_pswf_terms: int,
    ell: float,
) -> np.ndarray:
    psis = build_psi_matrix(tau, n_pswf_terms)
    pk = {}
    h = {}
    phase = np.exp(1j * ell * tau)
    for j in [1, 2, 3]:
        pk[j] = p_operator(samples[j], tau, weights, psis)
        g = phase * pk[j]
        pg = p_operator(g, tau, weights, psis)
        h[j] = g - pg
    c = np.zeros((3, 3), dtype=np.complex128)
    for i in [1, 2, 3]:
        for j in [1, 2, 3]:
            c[i - 1, j - 1] = np.sum(weights * np.conjugate(samples[i]) * h[j]) / (2.0 * math.pi)
    return c


def compute_candidate(name: str, n_pswf_terms: int, grid_nodes: int, ell: float) -> CandidateResult:
    tau_full, samples_full = load_samples(name)
    if grid_nodes == len(tau_full):
        tau = tau_full
        samples = samples_full
    else:
        # centered uniform-index subsample from the inherited grid
        idx = np.linspace(0, len(tau_full) - 1, grid_nodes).round().astype(int)
        tau = tau_full[idx]
        samples = {i: samples_full[i][idx] for i in [1, 2, 3]}
    weights = align_weights(tau)
    c = c_matrix_for_samples(samples, tau, weights, n_pswf_terms, ell)
    return CandidateResult(
        candidate=name,
        c=c,
        c_abs_max=float(np.max(np.abs(c))),
        c_fro=float(np.linalg.norm(c)),
        n_pswf_terms=n_pswf_terms,
        grid_nodes=grid_nodes,
        ell=ell,
    )


def write_c_csv(path: Path, result: CandidateResult, error_matrix: np.ndarray) -> None:
    rows = []
    for i in range(3):
        for j in range(3):
            val = result.c[i, j]
            rows.append(
                {
                    "candidate": result.candidate,
                    "i": i + 1,
                    "j": j + 1,
                    "ell": result.ell,
                    "n_pswf_terms": result.n_pswf_terms,
                    "grid_nodes": result.grid_nodes,
                    "c_real": f"{val.real:.17e}",
                    "c_imag": f"{val.imag:.17e}",
                    "c_abs": f"{abs(val):.17e}",
                    "error_bound": f"{error_matrix[i, j]:.17e}",
                    "status": "diagnostic_finite_grid_step173_K_infty_op",
                }
            )
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    main_results = {}
    variant_results: list[CandidateResult] = []
    for name in ["CAND1", "CAND2"]:
        main_result = compute_candidate(name, N_PSWF_MAIN, N_GRID_MAIN, ELL_MAIN)
        main_results[name] = main_result
        for n_terms in [12, 24, 36]:
            variant_results.append(compute_candidate(name, n_terms, N_GRID_MAIN, ELL_MAIN))
        variant_results.append(compute_candidate(name, N_PSWF_MAIN, 100, ELL_MAIN))
        for ell in [math.log(3.0), 1.0]:
            variant_results.append(compute_candidate(name, N_PSWF_MAIN, N_GRID_MAIN, ell))

    for name, result in main_results.items():
        same_candidate = [
            r for r in variant_results
            if r.candidate == name
            and r.c.shape == result.c.shape
            and abs(r.ell - result.ell) < 1e-15
        ]
        diffs = [
            np.abs(r.c - result.c)
            for r in same_candidate
            if not (r.n_pswf_terms == result.n_pswf_terms and r.grid_nodes == result.grid_nodes)
        ]
        err = np.max(np.stack(diffs), axis=0) if diffs else np.zeros_like(result.c.real)
        write_c_csv(BASE / f"c_matrix_{name}_step208.csv", result, err)

    robustness_rows = []
    for r in variant_results:
        robustness_rows.append(
            {
                "candidate": r.candidate,
                "n_pswf_terms": r.n_pswf_terms,
                "grid_nodes": r.grid_nodes,
                "ell": f"{r.ell:.17e}",
                "c_abs_max": f"{r.c_abs_max:.17e}",
                "c_fro": f"{r.c_fro:.17e}",
                "status": "computed",
            }
        )
    with (BASE / "robustness_step208.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(robustness_rows[0].keys()))
        writer.writeheader()
        writer.writerows(robustness_rows)

    print("Step 208 c-matrix computation")
    for name, result in main_results.items():
        print(f"{name}: max|c|={result.c_abs_max:.8e}, ||c||_F={result.c_fro:.8e}")
        print(result.c)
    print("robustness rows written:", len(robustness_rows))


if __name__ == "__main__":
    main()
