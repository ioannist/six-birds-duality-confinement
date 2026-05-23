import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step57_xi_paper')
rng = np.random.default_rng(57)

def psd_sqrt_inv(C):
    w,V=np.linalg.eigh(C)
    return V @ np.diag(1/np.sqrt(w)) @ V.T

def pinv(A,tol=1e-10):
    return np.linalg.pinv(A, rcond=tol)

def xi(C,L,D):
    Ci=np.linalg.inv(C)
    KLL=L@Ci@L.T
    KDL=D@Ci@L.T
    KDD=D@Ci@D.T
    return KDD - KDL@pinv(KLL)@KDL.T

def residual(C,L,D,A):
    Ci=np.linalg.inv(C)
    return (D-A@L)@Ci@(D-A@L).T

rows=[]
for trial in range(60):
    n=8; y=4; z=3; wdim=3
    A0=rng.normal(size=(n,n)); C=A0.T@A0 + 0.5*np.eye(n)
    L=rng.normal(size=(y,n)); D=rng.normal(size=(z,n)); M=rng.normal(size=(wdim,n))
    Ci2=psd_sqrt_inv(C)
    TL=L@Ci2; TD=D@Ci2; TM=M@Ci2
    # projection onto Ran(TL.T)
    U, s, Vt=np.linalg.svd(TL.T, full_matrices=False)
    rank=(s>1e-10).sum()
    P=U[:,:rank]@U[:,:rank].T if rank else np.zeros((n,n))
    Xi=xi(C,L,D)
    Xi_proj=TD@(np.eye(n)-P)@TD.T
    proj_err=np.linalg.norm(Xi-Xi_proj, ord=2)
    KLL=L@np.linalg.inv(C)@L.T
    KDL=D@np.linalg.inv(C)@L.T
    Astar=KDL@pinv(KLL)
    Atest=rng.normal(size=(z,y))
    left=residual(C,L,D,Atest)
    right=Xi+(Atest-Astar)@KLL@(Atest-Astar).T
    opt_err=np.linalg.norm(left-right,ord=2)
    Lplus=np.vstack([L,M])
    Xi_plus=xi(C,Lplus,D)
    # conditional chain term
    Ci=np.linalg.inv(C)
    KMM=M@Ci@M.T; KML=M@Ci@L.T; KDM=D@Ci@M.T
    KMM_L=KMM-KML@pinv(KLL)@KML.T
    KDM_L=KDM-KDL@pinv(KLL)@KML.T
    chain=Xi-KDM_L@pinv(KMM_L)@KDM_L.T
    chain_err=np.linalg.norm(Xi_plus-chain,ord=2)
    decrease_min=np.min(np.linalg.eigvalsh((Xi-Xi_plus+ (Xi-Xi_plus).T)/2))
    rows.append(dict(trial=trial, projection_err=proj_err, optimal_residual_err=opt_err, chain_rule_err=chain_err, decrease_min_eig=decrease_min))
pd.DataFrame(rows).to_csv(OUT/'xi_standalone_identity_checks_step57.csv', index=False)

# Hidden blind spot sweep
sweep=[]
for Mscale in np.logspace(0,5,31):
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,Mscale]])
    Xi=xi(C,L,D)[0,0]
    sweep.append(dict(M=Mscale, K_native=1.0, Xi=Xi, K_dissolving=Xi))
pd.DataFrame(sweep).to_csv(OUT/'xi_hidden_blind_spot_sweep_step57.csv', index=False)
print('wrote Step 57 checks')
