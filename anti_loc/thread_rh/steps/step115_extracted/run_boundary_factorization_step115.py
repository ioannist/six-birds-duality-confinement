#!/usr/bin/env python3
"""Finite sanity checks for Step 115.

These checks do not model RH. They illustrate the exact linear algebra of
boundary-to-co-Poisson residuals:
  Xi = B^* E^* E B.
A generic boundary block B is not annihilated by a zero-evaluator map E.
Projecting B into ker(E) gives a toy 'zeta-factorized' repair.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(115)

def psd_sqrt_inv(G, tol=1e-10):
    w, V = np.linalg.eigh((G + G.T.conj())/2)
    w = np.maximum(w, tol)
    return V @ np.diag(1/np.sqrt(w)) @ V.T.conj()

def orth_proj_ker(E, tol=1e-10):
    # Projection onto ker(E) in Euclidean metric.
    U, s, Vh = np.linalg.svd(E, full_matrices=True)
    rank = np.sum(s > tol)
    V = Vh.T.conj()
    K = V[:, rank:]
    return K @ K.T.conj()

def run():
    d = 80       # ambient finite Burnol/Sonine carrier dimension
    r = 18       # finite zero-evaluator window dimension
    m = 28       # legal input dimension
    E = rng.normal(size=(r, d)) / np.sqrt(d)
    B = rng.normal(size=(d, m)) / np.sqrt(m)
    G = B.T @ B + 1e-8*np.eye(m)
    Ghi = psd_sqrt_inv(G)
    Xi = B.T @ E.T @ E @ B
    norm_resid = np.linalg.norm(E @ B @ Ghi, 2)

    Pker = orth_proj_ker(E)
    Brep = Pker @ B
    Xi_rep = Brep.T @ E.T @ E @ Brep
    repaired_resid = np.linalg.norm(E @ Brep @ psd_sqrt_inv(Brep.T @ Brep + 1e-8*np.eye(m)), 2)

    # Partial repair sweep: interpolate B_alpha = ((1-alpha)I + alpha Pker)B.
    alphas = np.linspace(0, 1, 41)
    rows = []
    for a in alphas:
        Ba = ((1-a)*np.eye(d) + a*Pker) @ B
        Ga = Ba.T @ Ba + 1e-8*np.eye(m)
        eps = np.linalg.norm(E @ Ba @ psd_sqrt_inv(Ga), 2)
        eigmax = np.linalg.eigvalsh((Ba.T @ E.T @ E @ Ba + (Ba.T @ E.T @ E @ Ba).T)/2).max()
        rows.append({"alpha_projection_to_kernel": a, "normalized_residual_eps": eps, "max_Xi_eigenvalue": eigmax})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "factorization_residual_sweep_step115.csv", index=False)

    # Source absorption model: residual budget after source strength Lambda.
    Lambdas = np.logspace(0, 4, 80)
    base_resid = np.linalg.eigvalsh((Xi + Xi.T)/2).max()
    absorb_rows = []
    for L in Lambdas:
        # Toy budget: if source frame is L times identity on the residual sector, remaining effective cost ~ base/(1+L).
        absorb_rows.append({"Lambda": L, "unabsorbed_residual_model": base_resid/(1+L), "budget_collapse_model": 1/L})
    pd.DataFrame(absorb_rows).to_csv(OUT / "source_absorption_residual_step115.csv", index=False)

    # Plot residual sweep.
    plt.figure(figsize=(7,4.5))
    plt.plot(df["alpha_projection_to_kernel"], df["normalized_residual_eps"], marker="o", markersize=3)
    plt.xlabel("Projection strength toward ker(E)")
    plt.ylabel("normalized zero-evaluator residual")
    plt.title("Zeta-factorization toy: annihilation requires projection into ker(E)")
    plt.tight_layout()
    plt.savefig(OUT / "factorization_residual_sweep_step115.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7,4.5))
    plt.loglog(Lambdas, [r["unabsorbed_residual_model"] for r in absorb_rows], label="unabsorbed residual")
    plt.loglog(Lambdas, [r["budget_collapse_model"] for r in absorb_rows], label="1/Lambda budget")
    plt.xlabel("source lower-frame strength Lambda")
    plt.ylabel("toy residual/budget")
    plt.title("Source absorption model for Xi_BC")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "source_absorption_residual_step115.png", dpi=180)
    plt.close()

    # Spectrum plot of residual operator.
    vals = np.linalg.eigvalsh((Xi + Xi.T)/2)
    vals = vals[vals > 1e-12]
    plt.figure(figsize=(7,4.5))
    plt.semilogy(np.arange(1, len(vals)+1), vals[::-1], marker="o", markersize=3)
    plt.xlabel("index")
    plt.ylabel("positive eigenvalue of Xi_BC")
    plt.title("Finite zero-evaluator residual spectrum")
    plt.tight_layout()
    plt.savefig(OUT / "xi_bc_residual_spectrum_step115.png", dpi=180)
    plt.close()

    summary = {
        "ambient_dimension": d,
        "zero_window_dimension": r,
        "input_dimension": m,
        "generic_normalized_residual": float(norm_resid),
        "repaired_normalized_residual": float(repaired_resid),
        "max_Xi_eigenvalue": float(base_resid),
        "interpretation": "Generic B is not zero-annihilated; projection into ker(E) is a toy factorization repair."
    }
    (OUT / "finite_residual_sanity_step115.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    run()
