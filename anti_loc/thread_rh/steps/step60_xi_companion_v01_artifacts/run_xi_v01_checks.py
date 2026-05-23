import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(600)
out = Path('/mnt/data/anti_localization_step60_xi_v01')

def psd(n):
    A = rng.normal(size=(n,n))
    return A.T @ A + 0.5*np.eye(n)

def pinv(A):
    return np.linalg.pinv(A, rcond=1e-11)

def sqrt_inv(C):
    w, V = np.linalg.eigh(C)
    return V @ np.diag(1/np.sqrt(w)) @ V.T

def proj_from_rows(T):
    # projection onto range(T.T)
    return T.T @ pinv(T @ T.T) @ T

def xi(C,L,D):
    Ci = np.linalg.inv(C)
    KLL = L @ Ci @ L.T
    KDL = D @ Ci @ L.T
    KLD = KDL.T
    KDD = D @ Ci @ D.T
    return KDD - KDL @ pinv(KLL) @ KLD

def max_abs(A): return float(np.max(np.abs(A)))

rows=[]
for trial in range(80):
    n=8; y=4; z=3; w=2
    C=psd(n)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    M=rng.normal(size=(w,n))
    Xi=xi(C,L,D)
    Cih=sqrt_inv(C)
    TL=L@Cih; TD=D@Cih
    P=proj_from_rows(TL)
    Xi_proj=TD@(np.eye(n)-P)@TD.T
    proj_err=max_abs(Xi-Xi_proj)
    # optimal residual identity
    KLL=L@np.linalg.inv(C)@L.T
    KDL=D@np.linalg.inv(C)@L.T
    Astar=KDL@pinv(KLL)
    A=Astar+rng.normal(size=Astar.shape)*0.3
    residual=(D-A@L)@np.linalg.inv(C)@(D-A@L).T
    rhs=Xi+(A-Astar)@KLL@(A-Astar).T
    opt_err=max_abs(residual-rhs)
    # strict extension chain rule
    Lp=np.vstack([L,M])
    Xip=xi(C,Lp,D)
    # conditional blocks
    Ci=np.linalg.inv(C)
    KMM=M@Ci@M.T
    KML=M@Ci@L.T
    KLM=KML.T
    KDM=D@Ci@M.T
    KMD=KDM.T
    KMM_L=KMM-KML@pinv(KLL)@KLM
    KDM_L=KDM-KDL@pinv(KLL)@KLM
    KMD_L=KDM_L.T
    Xip_rhs=Xi-KDM_L@pinv(KMM_L)@KMD_L
    chain_err=max_abs(Xip-Xip_rhs)
    # monotonicity min eigen of Xi-Xip
    mineig=float(np.linalg.eigvalsh((Xi-Xip+Xi.T-Xip.T)/2).min())
    rows.append({"trial":trial,"projection_error":proj_err,"optimal_error":opt_err,"chain_error":chain_err,"min_eig_Xi_minus_Xi_extended":mineig})

pd.DataFrame(rows).to_csv(out/'xi_v01_identity_checks.csv',index=False)

# public shadow overread sweep
rows=[]
for Mval in [1,3,10,30,100,300,1000,3000,10000]:
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,Mval]])
    F=np.array([[0.0]]) # forget all dissolving readout
    full=float(xi(C,L,D)[0,0])
    # public readout dimension 1 zero row, Xi=0
    public=0.0
    rows.append({"M":Mval,"intrinsic_Xi":full,"public_Xi":public})
pd.DataFrame(rows).to_csv(out/'xi_v01_public_shadow_sweep.csv',index=False)

# strict extension visibility sweep: new probe M_alpha = alpha x2
rows=[]
Mval=100.0
C=np.eye(2)
L=np.array([[1.0,0.0]])
D=np.array([[0.0,Mval]])
base=float(xi(C,L,D)[0,0])
for alpha in np.linspace(0,1,21):
    Mprobe=np.array([[0.0,alpha]])
    Lp=np.vstack([L,Mprobe])
    val=float(xi(C,Lp,D)[0,0])
    rows.append({"alpha":float(alpha),"Xi":val,"reduction":base-val})
pd.DataFrame(rows).to_csv(out/'xi_v01_strict_extension_sweep.csv',index=False)
