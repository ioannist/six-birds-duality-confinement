
import numpy as np
import csv
from pathlib import Path

base = Path(__file__).resolve().parent

def psd(A, tol=1e-9):
    return np.linalg.eigvalsh((A+A.T)/2).min() >= -tol

def douglas_gate(A,K):
    return psd(K-A)

# Trace-not-domination
A = np.diag([2.0,0.0])
K = np.eye(2)
rows = [{
    "case": "trace_equal_not_domination",
    "trace_A": np.trace(A),
    "trace_K": np.trace(K),
    "min_eig_K_minus_A": np.linalg.eigvalsh(K-A).min(),
    "domination": douglas_gate(A,K)
}]
with open(base/"trace_not_domination_step73.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# test-subspace positivity
D = np.diag([1.0,-1.0])
rows = []
for theta in np.linspace(0, np.pi, 101):
    y = np.array([np.cos(theta), np.sin(theta)])
    q = y @ D @ y
    rows.append({"theta":theta, "quadratic":q})
with open(base/"test_subspace_insufficiency_step73.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# random PSD domination and contraction norm
rng = np.random.default_rng(73)
rows=[]
for i in range(50):
    B = rng.normal(size=(4,4))
    A = B.T@B
    R = rng.normal(size=(4,4))
    E = R.T@R
    K = A + E
    # contraction norm for V=T W can be represented by || A^{1/2} K^{-1/2} || if A,K SPD
    evals, U = np.linalg.eigh(K)
    Kminushalf = U @ np.diag(1/np.sqrt(np.maximum(evals,1e-12))) @ U.T
    evala, Ua = np.linalg.eigh(A)
    Ahalf = Ua @ np.diag(np.sqrt(np.maximum(evala,0))) @ Ua.T
    norm = np.linalg.svd(Ahalf @ Kminushalf, compute_uv=False)[0]
    rows.append({
        "trial": i,
        "min_eig_K_minus_A": np.linalg.eigvalsh(K-A).min(),
        "contraction_norm": norm,
        "passes": norm <= 1 + 1e-8
    })
with open(base/"douglas_contraction_random_step73.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# signed component repair: K = P - N + C. Need C >= N to make positive grouping
rows=[]
for c in np.linspace(0,2,21):
    P = np.diag([1.0,0.5])
    N = np.diag([0.0,1.0])
    C = c*np.eye(2)
    Ksigned = P - N + C
    rows.append({"completion_c": c, "min_eig_signed_total": np.linalg.eigvalsh(Ksigned).min(), "positive": psd(Ksigned)})
with open(base/"signed_component_repair_step73.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
