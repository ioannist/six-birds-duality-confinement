#!/usr/bin/env python3
"""Small finite matrix checks for Step 33.

These are not RH simulations. They only verify the algebraic countermodels
and witness identities used in the explicit-formula domination schema.
"""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent


def lammax(M: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((M + M.T.conj()) / 2)[-1])


def psd_leq(A: np.ndarray, B: np.ndarray, tol: float = 1e-10) -> bool:
    return lammax(A - B) <= tol


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def trace_shadow_countermodel():
    # Y = Y+ ⊕ Y-. Invariant sector passes, anti-invariant fails.
    K = np.eye(2)
    Theta = np.eye(2)
    A = np.diag([0.0, 2.0])  # only anti-invariant displacement
    Pplus = np.diag([1.0, 0.0])
    Pminus = np.diag([0.0, 1.0])
    rows = []
    rows.append({
        "case": "trace_shadow",
        "lambda_max_A_minus_K": lammax(A - K),
        "full_domination_passes": psd_leq(A, K),
        "invariant_shadow_lammax": lammax(Pplus @ (A - K) @ Pplus),
        "invariant_shadow_passes": psd_leq(Pplus @ A @ Pplus, Pplus @ K @ Pplus),
        "anti_invariant_lammax": lammax(Pminus @ (A - K) @ Pminus),
        "anti_invariant_passes": psd_leq(Pminus @ A @ Pminus, Pminus @ K @ Pminus),
    })
    write_csv(OUT / "trace_shadow_countermodel_step33.csv", rows)


def raw_shadow_countermodel():
    # Completed K sees A, raw K does not.
    rows = []
    A = np.array([[2.0]])
    K_raw = np.array([[1.0]])
    K_completion = np.array([[1.0]])
    K_full = K_raw + K_completion
    rows.append({
        "case": "raw_shadow",
        "A": float(A[0,0]),
        "K_raw": float(K_raw[0,0]),
        "K_completion": float(K_completion[0,0]),
        "K_full": float(K_full[0,0]),
        "full_domination_passes": psd_leq(A, K_full),
        "raw_domination_passes": psd_leq(A, K_raw),
        "raw_defect_lambda": lammax(A - K_raw),
    })
    write_csv(OUT / "raw_shadow_countermodel_step33.csv", rows)


def domination_witness_sweep():
    rows = []
    # A is anti-invariant displacement, K is carrier currency, Xi defect.
    # Sweep Xi to see when domination is accepted.
    A = np.diag([0.2, 1.4, 0.7])
    K = np.diag([0.5, 0.8, 0.8])
    for xi in np.linspace(0.0, 1.0, 21):
        Xi = xi * np.eye(3)
        D = A - K - Xi
        vals, vecs = np.linalg.eigh((D + D.T) / 2)
        idx = np.argmax(vals)
        y = vecs[:, idx]
        rows.append({
            "xi_scalar": float(xi),
            "lambda_max_defect": float(vals[idx]),
            "accepted": bool(vals[idx] <= 1e-10),
            "witness_y0": float(y[0]),
            "witness_y1": float(y[1]),
            "witness_y2": float(y[2]),
        })
    write_csv(OUT / "domination_witness_sweep_step33.csv", rows)


def off_fixed_mass_bound():
    rows = []
    # Visible root ledger with anti-invariant displacements and weights.
    displacements = np.array([0.0, 0.02, 0.05, 0.1, 0.3, 0.7])
    weights = np.array([10.0, 4.0, 3.0, 2.0, 1.0, 0.5])
    trace_A = float(np.sum(weights * displacements**2))
    for eps in [0.01, 0.05, 0.1, 0.2, 0.5]:
        actual = float(np.sum(weights[displacements >= eps]))
        bound = trace_A / (eps**2)
        rows.append({
            "epsilon": eps,
            "actual_mass_delta_ge_eps": actual,
            "trace_A": trace_A,
            "trace_bound": bound,
            "bound_valid": actual <= bound + 1e-12,
        })
    write_csv(OUT / "off_fixed_mass_bound_check_step33.csv", rows)


def main():
    trace_shadow_countermodel()
    raw_shadow_countermodel()
    domination_witness_sweep()
    off_fixed_mass_bound()

if __name__ == "__main__":
    main()
