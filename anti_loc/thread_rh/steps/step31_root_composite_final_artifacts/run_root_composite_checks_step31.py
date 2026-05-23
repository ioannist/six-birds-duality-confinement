#!/usr/bin/env python3
"""Step 31 small algebraic/root-composite sanity checks.

These are not Six Birds simulations.  They are finite-dimensional checks of the
linear algebra used in the root-composite capacity theorems.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent


def eigmax(A):
    return float(np.linalg.eigvalsh((A + A.conj().T) / 2)[-1].real)


def c2_trace_antitrace_sweep():
    rows = []
    Ms = np.logspace(-2, 4, 61)
    D_trace = np.array([[1.0, 1.0]]) / math.sqrt(2)
    y_trace = np.array([1.0, 1.0]) / math.sqrt(2)
    y_anti = np.array([1.0, -1.0]) / math.sqrt(2)
    for M in Ms:
        K = M * np.array([[1.0, -1.0], [-1.0, 1.0]])
        trace_cap = float(y_trace @ K @ y_trace)
        anti_cap = float(y_anti @ K @ y_anti)
        descended = float((D_trace @ K @ D_trace.T)[0, 0])
        rows.append({
            "M": M,
            "trace_sector_capacity": trace_cap,
            "anti_trace_sector_capacity": anti_cap,
            "descended_trace_shadow": descended,
            "max_eigenvalue": eigmax(K),
        })
    return rows


def c2_correlation_sweep():
    rows = []
    rhos = np.linspace(0, 0.999, 101)
    y_trace = np.array([1.0, 1.0]) / math.sqrt(2)
    y_anti = np.array([1.0, -1.0]) / math.sqrt(2)
    for rho in rhos:
        K = np.array([[1.0, -rho], [-rho, 1.0]])
        rows.append({
            "rho": rho,
            "individual_capacity_probe_1": K[0,0],
            "individual_capacity_probe_2": K[1,1],
            "trace_sector_capacity": float(y_trace @ K @ y_trace),
            "anti_trace_sector_capacity": float(y_anti @ K @ y_anti),
            "max_eigenvalue": eigmax(K),
        })
    return rows


def circulant_from_eigs(lambdas):
    # For C_m: K = F^* diag(lambdas) F, normalized DFT.
    m = len(lambdas)
    omega = np.exp(2j * np.pi / m)
    F = np.array([[omega ** (j * k) / math.sqrt(m) for k in range(m)] for j in range(m)])
    K = F @ np.diag(lambdas) @ F.conj().T
    return (K + K.conj().T) / 2


def cyclic_character_examples():
    rows = []
    for m in range(3, 13):
        lambdas = np.ones(m)
        lambdas[0] = 1.0  # trace/trivial sector
        lambdas[1] = float(m**2)  # one nontrivial algebraic sector needle
        K = circulant_from_eigs(lambdas)
        trace_vector = np.ones(m) / math.sqrt(m)
        trace_cap = float(np.real(trace_vector.conj() @ K @ trace_vector))
        rows.append({
            "group": f"C_{m}",
            "m": m,
            "trace_sector_capacity": trace_cap,
            "largest_nontrivial_sector_capacity": float(m**2),
            "max_eigenvalue_numeric": eigmax(K),
            "diagonal_capacity_mean": float(np.real(np.trace(K))/m),
            "diagonal_capacity_max": float(np.max(np.real(np.diag(K)))),
            "trace_shadow_passes_budget_1": trace_cap <= 1.0000001,
            "family_budget_I_fails": eigmax(K) > 1.0000001,
        })
    return rows


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_plots(trace_rows, corr_rows, cyc_rows):
    # Plot 1: trace shadow failure
    fig, ax = plt.subplots(figsize=(7, 4.5))
    M = np.array([r["M"] for r in trace_rows])
    anti = np.array([r["anti_trace_sector_capacity"] for r in trace_rows])
    shadow = np.array([r["descended_trace_shadow"] for r in trace_rows])
    ax.loglog(M, anti, label="anti-trace sector capacity")
    ax.loglog(M, shadow + 1e-16, label="trace shadow capacity")
    ax.set_xlabel("M")
    ax.set_ylabel("capacity")
    ax.set_title("Trace shadow can vanish while anti-trace capacity grows")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "trace_shadow_failure_step31.png", dpi=180)
    plt.close(fig)

    # Plot 2: two-conjugate sector capacities
    fig, ax = plt.subplots(figsize=(7, 4.5))
    rho = np.array([r["rho"] for r in corr_rows])
    trace_cap = np.array([r["trace_sector_capacity"] for r in corr_rows])
    anti_cap = np.array([r["anti_trace_sector_capacity"] for r in corr_rows])
    ax.plot(rho, trace_cap, label="trace sector")
    ax.plot(rho, anti_cap, label="anti-trace sector")
    ax.set_xlabel("correlation parameter rho")
    ax.set_ylabel("capacity")
    ax.set_title("Scalar conjugate checks miss nontrivial sector growth")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "c2_sector_capacity_step31.png", dpi=180)
    plt.close(fig)

    # Plot 3: cyclic character examples
    fig, ax = plt.subplots(figsize=(7, 4.5))
    m = np.array([r["m"] for r in cyc_rows])
    trace = np.array([r["trace_sector_capacity"] for r in cyc_rows])
    nontriv = np.array([r["largest_nontrivial_sector_capacity"] for r in cyc_rows])
    diagmax = np.array([r["diagonal_capacity_max"] for r in cyc_rows])
    ax.plot(m, trace, marker="o", label="trace sector")
    ax.plot(m, nontriv, marker="o", label="largest nontrivial sector")
    ax.plot(m, diagmax, marker="o", label="max coordinate diagonal")
    ax.set_xlabel("cyclic group order m")
    ax.set_ylabel("capacity")
    ax.set_title("Character-sector needles invisible to trace descent")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "cyclic_character_sectors_step31.png", dpi=180)
    plt.close(fig)


def main():
    trace_rows = c2_trace_antitrace_sweep()
    corr_rows = c2_correlation_sweep()
    cyc_rows = cyclic_character_examples()
    write_csv(OUT / "trace_shadow_countermodel_step31.csv", trace_rows)
    write_csv(OUT / "two_conjugate_correlation_step31.csv", corr_rows)
    write_csv(OUT / "cyclic_character_sector_step31.csv", cyc_rows)
    make_plots(trace_rows, corr_rows, cyc_rows)
    schema = {
        "step": 31,
        "name": "Root-composite / algebraic-extension anti-localization profile",
        "central_matrix": "K_G = L_G Gamma (Gamma^* C Gamma)^dagger Gamma^* L_G^*",
        "descent_dpi": "K_G <= Theta implies D K_G D^* <= D Theta D^*",
        "overread_warning": "trace/norm/symmetric descent can pass while nontrivial conjugate sectors fail",
        "sector_rule": "for finite abelian equivariant records, K_G diagonalizes by characters; trace controls only the trivial character",
        "rh_status": "obligation only, not proof",
    }
    with open(OUT / "root_composite_schema_step31.json", "w") as f:
        json.dump(schema, f, indent=2)

if __name__ == "__main__":
    main()
