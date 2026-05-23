import numpy as np
import pandas as pd
from pathlib import Path
rng=np.random.default_rng(56)
out=Path('/mnt/data/anti_localization_step56_proof_polish')

def psd_rank(n,r):
    A=rng.normal(size=(n,r))
    return A@A.T

def pinv(A,tol=1e-10):
    return np.linalg.pinv(A,rcond=tol)

# singular cost duality checks
rows=[]
for trial in range(40):
    n=8; r=5; m=4
    U,_=np.linalg.qr(rng.normal(size=(n,n)))
    vals=np.r_[rng.uniform(0.3,3.0,size=r), np.zeros(n-r)]
    C=U@np.diag(vals)@U.T
    Q=U[:,:r]
    C0=Q.T@C@Q
    L0=rng.normal(size=(m,r))
    L=L0@Q.T
    K=L@pinv(C)@L.T
    # choose z in range L0 by z=L0 a
    a=rng.normal(size=r)
    z=L0@a
    cost=z@pinv(K)@z
    # solve min u C u subject L u=z via transformed least norm
    T=L0@np.linalg.inv(np.linalg.cholesky(C0)).T  # L0 C0^{-1/2} (not exact if chol) actually use eig
    w,V=np.linalg.eigh(C0)
    C0_half_inv=V@np.diag(1/np.sqrt(w))@V.T
    T=L0@C0_half_inv
    x=np.linalg.pinv(T)@z
    cost_direct=x@x
    rows.append({'trial':trial,'cost_formula':cost,'cost_direct':cost_direct,'abs_err':abs(cost-cost_direct)})
pd.DataFrame(rows).to_csv(out/'singular_cost_duality_step56.csv',index=False)

# Xi identities checks
rows=[]
for trial in range(40):
    n=9; r=7; m=4; q=3; wdim=2
    U,_=np.linalg.qr(rng.normal(size=(n,n)))
    vals=np.r_[rng.uniform(0.2,4.0,size=r),np.zeros(n-r)]
    C=U@np.diag(vals)@U.T
    Q=U[:,:r]
    C0=Q.T@C@Q
    L0=rng.normal(size=(m,r))
    D0=rng.normal(size=(q,r))
    # blocks on quotient
    C0i=np.linalg.inv(C0)
    KLL=L0@C0i@L0.T
    KDL=D0@C0i@L0.T
    KDD=D0@C0i@D0.T
    Xi=KDD-KDL@pinv(KLL)@KDL.T
    Astar=KDL@pinv(KLL)
    A=rng.normal(size=(q,m))
    Res=(D0-A@L0)@C0i@(D0-A@L0).T
    RHS=Xi+(A-Astar)@KLL@(A-Astar).T
    err=np.linalg.norm(Res-RHS,ord=2)
    # extension
    M0=rng.normal(size=(wdim,r))
    Lp=np.vstack([L0,M0])
    Kpp=Lp@C0i@Lp.T
    KDp=D0@C0i@Lp.T
    Xip=KDD-KDp@pinv(Kpp)@KDp.T
    decrease=Xi-Xip
    min_eig=np.min(np.linalg.eigvalsh((decrease+decrease.T)/2))
    rows.append({'trial':trial,'optimal_residual_err':err,'min_eig_Xi_minus_Xi_ext':min_eig,'Xi_trace':np.trace(Xi),'Xi_ext_trace':np.trace(Xip)})
pd.DataFrame(rows).to_csv(out/'xi_identity_and_extension_checks_step56.csv',index=False)

# acceptance semantics table
pd.DataFrame([
    {'statement':'K <= Theta','meaning':'mathematical membrane / no native recombination witness','six_birds_status':'support evidence unless audit gates supplied'},
    {'statement':'accepted all-six membrane','meaning':'formed closure + exact package + null legality + native family + adequacy/predictive/all-six records + K <= Theta','six_birds_status':'accepted scoped membrane'},
    {'statement':'public shadow K_pub <= Theta_pub','meaning':'visible/readout membrane only','six_birds_status':'does not promote without reconstruction/defect bridge'},
    {'statement':'native K_L <= Theta with Xi unbounded','meaning':'native probes priced but layer-dissolving blind spot remains','six_birds_status':'native-only / failed adequacy'},
]).to_csv(out/'acceptance_semantics_step56.csv',index=False)
