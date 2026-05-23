import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step51_proof_tightening')

def pinv_psd(A, tol=1e-12):
    w, V = np.linalg.eigh((A+A.T)/2)
    wi = np.array([1/x if x > tol else 0.0 for x in w])
    return (V*wi) @ V.T

def sqrt_pinv(A, tol=1e-12):
    w, V = np.linalg.eigh((A+A.T)/2)
    wi = np.array([1/np.sqrt(x) if x > tol else 0.0 for x in w])
    return (V*wi) @ V.T

def min_spend(C,L,z):
    # Brute via legal quotient; assume L kills nulls.
    w,V = np.linalg.eigh((C+C.T)/2)
    mask = w > 1e-10
    V0 = V[:,mask]
    C0 = np.diag(w[mask])
    L0 = L @ V0
    # solve min ||u||^2 s.t. L0 C0^{-1/2} u = z
    A = L0 @ np.diag(1/np.sqrt(w[mask]))
    K = A @ A.T
    # feasibility
    proj = K @ pinv_psd(K)
    err = np.linalg.norm(proj @ z - z)
    if err > 1e-8:
        return np.inf, K
    return float(z.T @ pinv_psd(K) @ z), K

rows=[]
# singular legal cost example: C diag(0,1,4), L kills null and reads both legal coords
C=np.diag([0.0,1.0,4.0])
L=np.array([[0.0,1.0,0.0],[0.0,0.0,2.0]])
for z in [np.array([1.0,0.0]), np.array([0.0,1.0]), np.array([1.0,2.0])]:
    cost,K=min_spend(C,L,z)
    rows.append({'case':'singular_legal_cost','z':str(z.tolist()),'cost':cost,'K_trace':float(np.trace(K)),'feasible':np.isfinite(cost)})
# infeasible response
z=np.array([1.0,0.0,1.0])
L2=np.vstack([L, np.zeros((1,3))])
cost,K=min_spend(C,L2,z)
rows.append({'case':'singular_infeasible_response','z':str(z.tolist()),'cost':cost,'K_trace':float(np.trace(K)),'feasible':np.isfinite(cost)})
# null-mode failure example
Cnull=np.diag([0.0,1.0])
Lnull=np.array([[1.0,0.0]])
K_pinv=Lnull @ pinv_psd(Cnull) @ Lnull.T
rows.append({'case':'null_mode_fake_zero','z':'[1]','cost':'zero via null direction / capacity infinite','K_trace':float(np.trace(K_pinv)),'feasible':True})

pd.DataFrame(rows).to_csv(OUT/'singular_minimum_spend_checks_step51.csv', index=False)

# Adequacy residual checks
rng=np.random.default_rng(51)
rows=[]
for n in [4,6,8]:
    for trial in range(20):
        A=rng.normal(size=(n,n))
        C=A.T@A + np.eye(n)*0.5
        Cinv=np.linalg.inv(C)
        ydim=3; zdim=2; wdim=2
        L=rng.normal(size=(ydim,n))
        D=rng.normal(size=(zdim,n))
        M=rng.normal(size=(wdim,n))
        KLL=L@Cinv@L.T
        KDL=D@Cinv@L.T
        KLD=KDL.T
        KDD=D@Cinv@D.T
        Xi=KDD-KDL@pinv_psd(KLL)@KLD
        Lp=np.vstack([L,M])
        Kpp=Lp@Cinv@Lp.T
        KDp=D@Cinv@Lp.T
        Xip=KDD-KDp@pinv_psd(Kpp)@KDp.T
        diff=Xi-Xip
        eigdiff=np.linalg.eigvalsh((diff+diff.T)/2).min()
        eigXi=np.linalg.eigvalsh((Xi+Xi.T)/2).min()
        # optimality test for random Amap
        Astar=KDL@pinv_psd(KLL)
        Amap=Astar + rng.normal(size=Astar.shape)
        R=(D-Amap@L)
        KR=R@Cinv@R.T
        bound=Xi + (Amap-Astar)@KLL@(Amap-Astar).T
        err=np.linalg.norm(KR-bound)
        rows.append({'n':n,'trial':trial,'min_eig_Xi':eigXi,'min_eig_Xi_minus_Xip':eigdiff,'optimality_error':err})

pd.DataFrame(rows).to_csv(OUT/'adequacy_residual_checks_step51.csv', index=False)

# Gate implication statuses table
statuses=[
 ('all gates + K<=Theta','accepted'),
 ('K<=Theta but no null-mode legality','failed_null_mode_or_support_only'),
 ('K<=Theta on public shadow only','public_shadow_only'),
 ('K<=Theta route-local not stacked','local_only_protocol_overread'),
 ('K<=Theta native but adequacy residual nonzero','native_only_failed_adequacy'),
 ('K<=Theta current level only','current_only_not_predictive'),
]
pd.DataFrame(statuses, columns=['condition','honest_status']).to_csv(OUT/'acceptance_gate_implication_status_step51.csv', index=False)
print('wrote step51 checks')
