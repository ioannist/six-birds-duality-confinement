import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(56)
out = Path('/mnt/data/anti_localization_step56_proof_polish')


def pinv_psd(A, tol=1e-10):
    w, V = np.linalg.eigh((A + A.T)/2)
    wi = np.array([1/x if x > tol else 0.0 for x in w])
    return (V * wi) @ V.T


def sqrt_psd(A, tol=1e-10):
    w, V = np.linalg.eigh((A + A.T)/2)
    return (V * np.sqrt(np.maximum(w, 0))) @ V.T


def rand_spd(n):
    A = rng.normal(size=(n,n))
    return A.T @ A + 0.5*np.eye(n)

# Singular cost duality checks on quotient: create C with nullspace and null-legal L.
rows=[]
for trial in range(80):
    n=7; r=5; m=4
    C0 = rand_spd(r)
    C = np.zeros((n,n)); C[:r,:r]=C0
    L0 = rng.normal(size=(m,r))
    L = np.zeros((m,n)); L[:,:r]=L0
    K = L0 @ np.linalg.inv(C0) @ L0.T
    Kp = pinv_psd(K)
    # attainable z = L0 u
    u = rng.normal(size=r)
    z = L0 @ u
    # minimum cost = z^T K^dag z
    cost_formula = float(z.T @ Kp @ z)
    # solve KKT/min norm in v coordinates
    C0_inv_sqrt = np.linalg.inv(sqrt_psd(C0))
    T = L0 @ C0_inv_sqrt
    Tp = np.linalg.pinv(T)
    vmin = Tp @ z
    cost_direct = float(vmin.T @ vmin)
    rows.append(dict(trial=trial, cost_formula=cost_formula, cost_direct=cost_direct, abs_error=abs(cost_formula-cost_direct)))
pd.DataFrame(rows).to_csv(out/'singular_cost_duality_step56.csv', index=False)

# Xi projection and optimal residual checks.
rows=[]
for trial in range(80):
    n=8; ydim=4; zdim=3
    C = rand_spd(n)
    Ci = np.linalg.inv(C)
    L = rng.normal(size=(ydim,n))
    D = rng.normal(size=(zdim,n))
    KLL = L @ Ci @ L.T
    KDL = D @ Ci @ L.T
    KDD = D @ Ci @ D.T
    Xi = KDD - KDL @ pinv_psd(KLL) @ KDL.T
    C_inv_sqrt = np.linalg.inv(sqrt_psd(C))
    TL = L @ C_inv_sqrt
    TD = D @ C_inv_sqrt
    # Projection onto range(TL^T)
    Q, _ = np.linalg.qr(TL.T, mode='reduced')
    # If rank deficient QR may include zero columns; use SVD more robust
    U, s, Vt = np.linalg.svd(TL.T, full_matrices=False)
    rank = (s > 1e-10).sum()
    U = U[:,:rank]
    P = U @ U.T if rank else np.zeros((n,n))
    Xi_proj = TD @ (np.eye(n)-P) @ TD.T
    proj_err = np.linalg.norm(Xi-Xi_proj, ord=2)
    # Optimal residual identity at random A
    A = rng.normal(size=(zdim,ydim))
    Astar = KDL @ pinv_psd(KLL)
    Res = (D-A@L) @ Ci @ (D-A@L).T
    Decomp = Xi + (A-Astar) @ KLL @ (A-Astar).T
    opt_err = np.linalg.norm(Res-Decomp, ord=2)
    mineig_xi = np.linalg.eigvalsh((Xi+Xi.T)/2).min()
    rows.append(dict(trial=trial, projection_error=proj_err, optimal_residual_error=opt_err, min_eig_xi=mineig_xi))
pd.DataFrame(rows).to_csv(out/'xi_projection_residual_checks_step56.csv', index=False)

# Acceptance semantics statuses examples.
status_rows = [
    dict(case='bare_matrix_passes_no_records', matrix_budget='pass', all_six='missing', status='support_only'),
    dict(case='null_mode_seen', matrix_budget='pseudoinverse_zero_possible', all_six='failed P2/null legality', status='failed_null_mode'),
    dict(case='native_passes_adequacy_missing', matrix_budget='native pass', all_six='adequacy missing', status='native_only'),
    dict(case='predictive_transport_missing', matrix_budget='current pass', all_six='failed P4', status='current_only'),
    dict(case='complete_record_and_budget', matrix_budget='pass', all_six='accepted', status='accepted'),
]
pd.DataFrame(status_rows).to_csv(out/'acceptance_semantics_cases_step56.csv', index=False)

print('wrote step56 checks')
