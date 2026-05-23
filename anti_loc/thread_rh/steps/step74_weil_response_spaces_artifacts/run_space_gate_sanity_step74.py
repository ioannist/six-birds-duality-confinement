"""Finite sanity checks for Step 74.
These are not zeta simulations. They only illustrate why finite/core/shadow distinctions matter.
"""
import numpy as np
import pandas as pd
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step74_spaces')
rng = np.random.default_rng(74)

# 1. Finite-subspace insufficiency: K-A positive on first coordinate, fails on second.
rows = []
A = np.diag([0.5, 2.0])  # zero-side
K = np.eye(2)            # carrier-side
for subspace in ['span_e1','full']:
    if subspace == 'span_e1':
        P = np.array([[1.0],[0.0]])
        min_eig = np.linalg.eigvalsh(P.T @ (K-A) @ P).min()
    else:
        min_eig = np.linalg.eigvalsh(K-A).min()
    rows.append({'case':'finite_subspace_insufficiency','space':subspace,'min_eig_K_minus_A':min_eig,'passes':min_eig>=-1e-12})
pd.DataFrame(rows).to_csv(out/'finite_subspace_insufficiency_step74.csv', index=False)

# 2. Trace equality doesn't imply Loewner domination.
A = np.diag([2.0,0.0])
K = np.diag([1.0,1.0])
trace_equal = abs(np.trace(A)-np.trace(K)) < 1e-12
min_eig = np.linalg.eigvalsh(K-A).min()
pd.DataFrame([{'trace_A':np.trace(A),'trace_K':np.trace(K),'trace_equal':trace_equal,'min_eig_K_minus_A':min_eig,'loewner_passes':min_eig>=-1e-12}]).to_csv(out/'trace_not_domination_step74.csv', index=False)

# 3. Null form legality: qcmp null direction but qZ sees it.
K = np.diag([1.0,0.0])
A = np.diag([0.0,1.0])
rows=[]
for vec_name, v in [('energy_seen',np.array([1.0,0.0])),('null_seen_by_zero',np.array([0.0,1.0]))]:
    qcmp = v @ K @ v
    qz = v @ A @ v
    rows.append({'vec':vec_name,'q_cmp':qcmp,'q_Z':qz,'null_legality_violation': qcmp==0 and qz>0})
pd.DataFrame(rows).to_csv(out/'null_form_legality_step74.csv', index=False)

# 4. Random Douglas checks: A <= K iff contraction norm <= 1 in finite positive definite case.
rows=[]
for i in range(40):
    W = rng.normal(size=(5,3))
    K = W.T @ W + 0.2*np.eye(3)
    # choose contraction T to construct V=T W
    T = rng.normal(size=(4,5))
    # scale to norm <= .9
    smax = np.linalg.svd(T, compute_uv=False)[0]
    T = 0.9*T/smax
    V = T @ W
    A = V.T @ V
    min_eig = np.linalg.eigvalsh(K-A).min()
    # reconstruct minimal contraction candidate V W^dagger on ran W (finite full rank)
    T_candidate = V @ np.linalg.pinv(W)
    tc_norm = np.linalg.svd(T_candidate, compute_uv=False)[0]
    rows.append({'trial':i,'min_eig_K_minus_A':min_eig,'candidate_T_norm':tc_norm,'passes':min_eig>=-1e-10 and tc_norm<=1+1e-8})
pd.DataFrame(rows).to_csv(out/'douglas_core_random_checks_step74.csv', index=False)
print('Step 74 sanity artifacts written to', out)
