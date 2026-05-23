import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step51_proof_tightening')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(51)

def psd_from_rank(n, rank, floor=0.5):
    Q, _ = np.linalg.qr(rng.normal(size=(n,n)))
    vals = np.zeros(n)
    vals[:rank] = floor + rng.random(rank) * 2.0
    return Q @ np.diag(vals) @ Q.T, Q, vals

def pinv_sqrt(C, tol=1e-10):
    vals, vecs = np.linalg.eigh(C)
    invsqrt = np.zeros_like(vals)
    for i,v in enumerate(vals):
        if v > tol:
            invsqrt[i] = 1/np.sqrt(v)
    return vecs @ np.diag(invsqrt) @ vecs.T

def sqrt_mat(C, tol=1e-10):
    vals, vecs = np.linalg.eigh(C)
    sq = np.where(vals>tol, np.sqrt(vals), 0.0)
    return vecs @ np.diag(sq) @ vecs.T

def pinv(C, tol=1e-10):
    vals, vecs = np.linalg.eigh(C)
    inv = np.where(vals>tol, 1/vals, 0.0)
    return vecs @ np.diag(inv) @ vecs.T

# 1. Singular minimum-spend duality checks
rows=[]
for trial in range(80):
    n=7; r=5; m=4
    C, Q, vals = psd_from_rank(n, r)
    # Null-legal L: define arbitrary on range subspace, zero on null by L = G Q_range^T Q_range? Use spectral projection
    eigvals, eigvecs = np.linalg.eigh(C)
    range_basis = eigvecs[:, eigvals>1e-10]
    L0 = rng.normal(size=(m, range_basis.shape[1]))
    L = L0 @ range_basis.T
    Cdag = pinv(C)
    K = L @ Cdag @ L.T
    A = L @ pinv_sqrt(C)
    # choose z in range A
    x = rng.normal(size=n)
    z = A @ x
    # min norm x for A x = z
    x_min = np.linalg.pinv(A) @ z
    cost_lstsq = float(x_min @ x_min)
    cost_formula = float(z @ np.linalg.pinv(K) @ z)
    # capacity for random y
    y = rng.normal(size=m)
    cap_formula = float(y @ K @ y)
    cap_direct = float(np.linalg.norm(A.T @ y)**2)
    rows.append({
        'trial': trial,
        'rank_C': r,
        'cost_formula': cost_formula,
        'cost_lstsq': cost_lstsq,
        'cost_abs_error': abs(cost_formula-cost_lstsq),
        'cap_formula': cap_formula,
        'cap_direct': cap_direct,
        'cap_abs_error': abs(cap_formula-cap_direct),
        'null_legality_norm': float(np.linalg.norm(L @ eigvecs[:, eigvals<=1e-10]))
    })
pd.DataFrame(rows).to_csv(OUT/'singular_duality_checks_step51.csv', index=False)

# 2. Adequacy residual optimality and exact adequacy checks
rows=[]
for trial in range(80):
    n=8; r=6; m=4; k=3
    C, Q, vals = psd_from_rank(n, r)
    eigvals, eigvecs = np.linalg.eigh(C)
    range_basis = eigvecs[:, eigvals>1e-10]
    L0 = rng.normal(size=(m, r))
    D0 = rng.normal(size=(k, r))
    L = L0 @ range_basis.T
    D = D0 @ range_basis.T
    Cdag = pinv(C)
    KLL = L @ Cdag @ L.T
    KDL = D @ Cdag @ L.T
    KLD = KDL.T
    KDD = D @ Cdag @ D.T
    Xi = KDD - KDL @ np.linalg.pinv(KLL) @ KLD
    Astar = KDL @ np.linalg.pinv(KLL)
    A_rand = rng.normal(size=(k,m))
    Rrand = D - A_rand @ L
    Krand = Rrand @ Cdag @ Rrand.T
    diff = Krand - (Xi + (A_rand-Astar) @ KLL @ (A_rand-Astar).T)
    eigXi = np.linalg.eigvalsh((Xi+Xi.T)/2)
    rows.append({
        'trial': trial,
        'min_eig_Xi': float(eigXi.min()),
        'identity_error_fro': float(np.linalg.norm(diff, ord='fro')),
        'random_residual_minus_Xi_min_eig': float(np.linalg.eigvalsh((Krand-Xi + (Krand-Xi).T)/2).min())
    })
pd.DataFrame(rows).to_csv(OUT/'adequacy_residual_checks_step51.csv', index=False)

# 3. Strict extension monotonicity checks
rows=[]
for trial in range(80):
    n=10; r=8; m=3; q=2; k=3
    C, Q, vals = psd_from_rank(n, r)
    eigvals, eigvecs = np.linalg.eigh(C)
    range_basis = eigvecs[:, eigvals>1e-10]
    L = rng.normal(size=(m, r)) @ range_basis.T
    M = rng.normal(size=(q, r)) @ range_basis.T
    D = rng.normal(size=(k, r)) @ range_basis.T
    Cdag = pinv(C)
    def Xi_for(Lmat):
        KLL = Lmat @ Cdag @ Lmat.T
        KDL = D @ Cdag @ Lmat.T
        KDD = D @ Cdag @ D.T
        return KDD - KDL @ np.linalg.pinv(KLL) @ KDL.T
    XiL = Xi_for(L)
    XiPlus = Xi_for(np.vstack([L, M]))
    dec = XiL - XiPlus
    rows.append({
        'trial': trial,
        'trace_Xi_before': float(np.trace(XiL)),
        'trace_Xi_after': float(np.trace(XiPlus)),
        'trace_decrease': float(np.trace(dec)),
        'min_eig_decrease': float(np.linalg.eigvalsh((dec+dec.T)/2).min())
    })
pd.DataFrame(rows).to_csv(OUT/'strict_extension_adequacy_checks_step51.csv', index=False)

# 4. Acceptance tightening table
acceptance = pd.DataFrame([
    {'claim_form':'K <= Theta only','mathematical_budget':'yes','all_six_accepted':'no','proper_status':'support_only'},
    {'claim_form':'K <= Theta + null legality + exact package','mathematical_budget':'yes','all_six_accepted':'partial','proper_status':'candidate_or_scoped'},
    {'claim_form':'K <= Theta + all-six gates + completed witness ledger','mathematical_budget':'yes','all_six_accepted':'yes','proper_status':'accepted_membrane'},
    {'claim_form':'diagonal probe capacities only','mathematical_budget':'no','all_six_accepted':'no','proper_status':'failed_recombination_gate'},
    {'claim_form':'native membrane without adequacy for D','mathematical_budget':'native_only','all_six_accepted':'no for dissolving claim','proper_status':'native_only_or_failed_adequacy'},
])
acceptance.to_csv(OUT/'acceptance_semantics_table_step51.csv', index=False)

# summary
summary = {
    'singular_duality_max_cost_error': [pd.read_csv(OUT/'singular_duality_checks_step51.csv')['cost_abs_error'].max()],
    'singular_duality_max_cap_error': [pd.read_csv(OUT/'singular_duality_checks_step51.csv')['cap_abs_error'].max()],
    'adequacy_identity_max_error': [pd.read_csv(OUT/'adequacy_residual_checks_step51.csv')['identity_error_fro'].max()],
    'strict_extension_min_decrease_eig_min': [pd.read_csv(OUT/'strict_extension_adequacy_checks_step51.csv')['min_eig_decrease'].min()],
}
pd.DataFrame(summary).to_csv(OUT/'step51_check_summary.csv', index=False)
print('Step 51 checks written to', OUT)
