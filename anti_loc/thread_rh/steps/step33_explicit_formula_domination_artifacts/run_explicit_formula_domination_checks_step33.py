"""Small finite checks for Step 33.
This is not an RH simulation. It only verifies finite-dimensional Douglas-style
factorization examples and trace-shadow countermodels.
"""
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step33_explicit_formula')

def psd_sqrt(A):
    w, V = np.linalg.eigh((A + A.T) / 2)
    return V @ np.diag(np.sqrt(np.maximum(w, 0))) @ V.T

def maxeig(A):
    return float(np.linalg.eigvalsh((A + A.T) / 2).max())

rng = np.random.default_rng(33)
rows=[]
for n in [2,3,5,8]:
    for trial in range(20):
        R = rng.normal(size=(n, n+2))
        K = R @ R.T
        # Choose contraction Omega by taking a small random matrix and normalizing op norm
        Om = rng.normal(size=(n+2, n+1))
        op = np.linalg.svd(Om, compute_uv=False)[0]
        Om = 0.7 * Om / op
        D = R @ Om
        A = D @ D.T
        gap = maxeig(A - K)
        rows.append({"n": n, "trial": trial, "maxeig_A_minus_K": gap, "status": "passes" if gap <= 1e-8 else "fails"})
pd.DataFrame(rows).to_csv(OUT/'douglas_domination_random_checks_step33.csv', index=False)

# Trace-shadow countermodel
K = np.diag([0.5, 2.0])
Theta = np.eye(2)
Pplus = np.diag([1.0, 0.0])
Pminus = np.diag([0.0, 1.0])
shadow = maxeig(Pplus @ (K-Theta) @ Pplus)
full = maxeig(K-Theta)
anti = maxeig(Pminus @ (K-Theta) @ Pminus)
pd.DataFrame([{
    "invariant_shadow_maxeig": shadow,
    "anti_invariant_maxeig": anti,
    "full_maxeig": full,
    "invariant_shadow_passes": shadow <= 1e-12,
    "full_budget_passes": full <= 1e-12
}]).to_csv(OUT/'trace_shadow_countermodel_step33.csv', index=False)

# Defect mass bound toy
rows=[]
for theta_trace in [0.0, 0.01, 0.05, 0.1, 0.25]:
    for ef_trace in [0.0, 0.01, 0.05]:
        for eps in [0.1, 0.25, 0.5, 1.0]:
            rows.append({
                "trace_Theta_minus": theta_trace,
                "trace_E_EF": ef_trace,
                "epsilon": eps,
                "mass_bound": (theta_trace + ef_trace)/(eps**2)
            })
pd.DataFrame(rows).to_csv(OUT/'zero_confinement_mass_bounds_step33.csv', index=False)

print('wrote Step 33 check CSVs')
