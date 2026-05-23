import numpy as np
import pandas as pd
from pathlib import Path

rng=np.random.default_rng(51)
out=Path('/mnt/data/anti_localization_step51_proof_tightening')

def pinv(A,tol=1e-10):
    return np.linalg.pinv(A, rcond=tol)

rows=[]
# Singular minimum spend check: C diag(0, lambda...), L null-legal
for trial in range(40):
    n=6; k=3; m=3
    lamb=0.5+rng.random(n-k)*4
    C=np.diag(np.r_[np.zeros(k),lamb])
    C0=np.diag(lamb)
    # L annihilates kernel: first k columns zero
    L0=rng.normal(size=(m,n-k))
    L=np.c_[np.zeros((m,k)),L0]
    K=L@pinv(C)@L.T
    # choose z in range L0
    a=rng.normal(size=n-k)
    z=L0@a
    # cost by formula
    cost_formula=float(z.T@pinv(K)@z)
    # solve min ||C0^{1/2}x||^2 s.t. L0 x=z using transformation B=L0 C0^{-1/2}
    B=L0@np.diag(1/np.sqrt(lamb))
    w=pinv(B)@z
    cost_direct=float(w.T@w)
    rows.append(dict(kind='singular_min_spend',trial=trial,error=abs(cost_formula-cost_direct),value=cost_formula))

# Xi residual optimality and monotonicity
for trial in range(40):
    n=7; ydim=3; zdim=2; wdim=2
    A=rng.normal(size=(n,n)); C=A.T@A+np.eye(n)*0.3
    Ci=np.linalg.inv(C)
    L=rng.normal(size=(ydim,n))
    D=rng.normal(size=(zdim,n))
    M=rng.normal(size=(wdim,n))
    KLL=L@Ci@L.T; KDD=D@Ci@D.T; KDL=D@Ci@L.T; KLD=KDL.T
    Xi=KDD-KDL@pinv(KLL)@KLD
    Astar=KDL@pinv(KLL)
    Atest=rng.normal(size=(zdim,ydim))
    Res=(D-Atest@L)@Ci@(D-Atest@L).T
    RHS=Xi+(Atest-Astar)@KLL@(Atest-Astar).T
    opt_error=float(np.linalg.norm(Res-RHS,2))
    # monotonicity with Lplus
    Lp=np.vstack([L,M])
    Kp=Lp@Ci@Lp.T; KDlp=D@Ci@Lp.T
    Xip=KDD-KDlp@pinv(Kp)@KDlp.T
    min_old_minus_new=float(np.linalg.eigvalsh((Xi-Xip + (Xi-Xip).T)/2).min())
    rows.append(dict(kind='xi_identity_monotonicity',trial=trial,error=opt_error,value=min_old_minus_new))

pd.DataFrame(rows).to_csv(out/'step51_identity_checks.csv',index=False)
print(pd.DataFrame(rows).groupby('kind').agg({'error':['max','mean'],'value':['min','max']}))
