"""Step 34 finite algebra checks.

These checks are not Six Birds simulations. They only sanity-check the
operator algebra used in the completed explicit-formula bridge decomposition:
A = V^*V <= W^*W iff V = T W with ||T||<=1, plus the defect inequality.
"""
from __future__ import annotations

import csv
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(34034)


def psd_sqrt(A: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh((A + A.T) / 2)
    vals = np.maximum(vals, 0)
    return vecs @ np.diag(np.sqrt(vals)) @ vecs.T


def op_norm(A: np.ndarray) -> float:
    return float(np.linalg.svd(A, compute_uv=False)[0])


def min_eig(A: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((A + A.T) / 2)[0])


def max_eig(A: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((A + A.T) / 2)[-1])


def random_contraction(out_dim: int, in_dim: int, scale: float = 0.8) -> np.ndarray:
    A = rng.normal(size=(out_dim, in_dim))
    n = op_norm(A)
    return scale * A / max(n, 1e-12)


def check_contract_factorization() -> list[dict[str, float]]:
    rows = []
    for trial in range(60):
        y_dim = 5
        comp_dims = [7, 6, 4, 5]
        z_dim = 6
        Ws = [rng.normal(size=(d, y_dim)) for d in comp_dims]
        W = np.vstack(Ws)
        T = random_contraction(z_dim, W.shape[0], scale=rng.uniform(0.05, 0.98))
        V = T @ W
        A = V.T @ V
        K = W.T @ W
        rows.append({
            "trial": trial,
            "T_norm": op_norm(T),
            "min_eig_K_minus_A": min_eig(K - A),
            "max_eig_A": max_eig(A),
            "max_eig_K": max_eig(K),
            "status": 1.0 if min_eig(K - A) >= -1e-9 else 0.0,
        })
    return rows


def check_defect_bound() -> list[dict[str, float]]:
    rows = []
    for trial in range(60):
        y_dim = 4
        w_dim = 12
        z_dim = 5
        W = rng.normal(size=(w_dim, y_dim))
        T = random_contraction(z_dim, w_dim, scale=rng.uniform(0.1, 0.95))
        R = rng.normal(size=(z_dim, y_dim)) * rng.uniform(0.0, 0.2)
        V = T @ W + R
        A = V.T @ V
        K = W.T @ W
        E = R.T @ R
        for t in [0.25, 0.5, 1.0, 2.0, 4.0]:
            bound = (1 + t) * K + (1 + 1/t) * E
            rows.append({
                "trial": trial,
                "t": t,
                "T_norm": op_norm(T),
                "R_norm": op_norm(R),
                "min_eig_bound_minus_A": min_eig(bound - A),
                "status": 1.0 if min_eig(bound - A) >= -1e-9 else 0.0,
            })
    return rows


def check_trace_counterexample() -> list[dict[str, float]]:
    A = np.diag([2.0, 0.0])
    K = np.eye(2)
    return [{
        "trace_A": float(np.trace(A)),
        "trace_K": float(np.trace(K)),
        "min_eig_K_minus_A": min_eig(K - A),
        "trace_agrees": 1.0 if abs(np.trace(A)-np.trace(K)) < 1e-12 else 0.0,
        "domination_holds": 1.0 if min_eig(K - A) >= -1e-12 else 0.0,
    }]


def write_csv(name: str, rows: list[dict]):
    if not rows:
        return
    path = OUT / name
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    write_csv("contractive_factorization_checks_step34.csv", check_contract_factorization())
    write_csv("defective_bridge_bound_checks_step34.csv", check_defect_bound())
    write_csv("trace_shadow_counterexample_step34.csv", check_trace_counterexample())


if __name__ == "__main__":
    main()
