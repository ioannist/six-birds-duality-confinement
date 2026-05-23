"""Finite-dimensional algebra sanity checks for Step 38.

These are not Six Birds simulations and not RH evidence. They only verify the
PSD algebra appearing in the root-composite obligation theorem.
"""
import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(38)
out = Path('/mnt/data/anti_localization_step38_rhobligation')

def psd_sqrt(A):
    w, V = np.linalg.eigh((A + A.T) / 2)
    w = np.maximum(w, 0)
    return V @ np.diag(np.sqrt(w)) @ V.T

def rand_psd(n, scale=1.0):
    X = rng.normal(size=(n,n))
    return scale * (X.T @ X) / n

rows=[]
for trial in range(80):
    n=4
    Theta0 = np.eye(n) + rand_psd(n, 0.2)
    Lambda = 0.5 + 5*rng.random()
    E_src = rand_psd(n, 0.02)
    E_EF = rand_psd(n, 0.01)
    t = 0.5 + 2*rng.random()
    # Construct K below Lambda^{-1}Theta0 + E_src
    K_bound = (1/Lambda)*Theta0 + E_src
    # A below defective bound
    A_bound = (1+t)*K_bound + (1+1/t)*E_EF
    # choose contractions by scaling PSD roots to generate A <= A_bound
    S = psd_sqrt(A_bound)
    U = rng.normal(size=(n,n))
    # normalize op norm <= .7
    op = np.linalg.norm(U,2)
    U = 0.7*U/op
    A = S @ U.T @ U @ S
    # check A <= bound
    lam = np.linalg.eigvalsh((A_bound - A + (A_bound - A).T)/2).min()
    eps = 0.2
    mass_bound = np.trace(A_bound)/(eps**2)
    rows.append({
        'trial':trial,
        'Lambda':Lambda,
        't':t,
        'min_eig_bound_minus_A':lam,
        'trace_A':np.trace(A),
        'trace_bound':np.trace(A_bound),
        'offfixed_mass_bound_eps_0p2':mass_bound,
        'status':'pass' if lam > -1e-10 else 'fail'
    })

pd.DataFrame(rows).to_csv(out/'step38_psd_obligation_checks.csv', index=False)

# simple convergence ledger with Lambda_n -> infinity, defects -> 0
rows=[]
for n in range(1,101):
    Lambda=n
    trTheta=3.0
    tr_Esrc=1/n**2
    tr_EEF=1/n**2
    t=1.0
    eps=0.1
    trace_budget=(1+t)*((1/Lambda)*trTheta+tr_Esrc)+(1+1/t)*tr_EEF
    mass_bound=trace_budget/(eps**2)
    rows.append({'n':n,'Lambda':Lambda,'trace_budget':trace_budget,'offfixed_mass_bound_eps_0p1':mass_bound})
pd.DataFrame(rows).to_csv(out/'step38_confinement_ladder.csv', index=False)

print('wrote Step 38 check CSVs')
