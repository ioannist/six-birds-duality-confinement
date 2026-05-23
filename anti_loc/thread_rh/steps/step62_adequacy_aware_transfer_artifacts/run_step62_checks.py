import numpy as np
from pathlib import Path
import csv

OUT = Path('/mnt/data/anti_localization_step62_adequacy_transfer')
rng = np.random.default_rng(62062)

def spd(n, shift=1.0):
    A = rng.normal(size=(n,n))
    return A.T @ A + shift*np.eye(n)

def pinv(A):
    return np.linalg.pinv(A, rcond=1e-10)

def xi(C,L,D):
    Ci = np.linalg.inv(C)
    KLL = L @ Ci @ L.T
    KDL = D @ Ci @ L.T
    KDD = D @ Ci @ D.T
    return KDD - KDL @ pinv(KLL) @ KDL.T

def K(C,L):
    return L @ np.linalg.inv(C) @ L.T

def min_eig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

# exact transfer checks
rows=[]
for trial in range(50):
    n=8; y=4; z=3
    C=spd(n,0.7)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    A=spd(y,0.2)  # invertible native reparam
    B=rng.normal(size=(2,z))
    X=xi(C,L,D)
    Xp=xi(C,A@L,B@D)
    target=B@X@B.T
    err=np.linalg.norm(Xp-target,2)
    rows.append({'trial':trial,'operator_error':err,'min_eig_target_minus_actual':min_eig(target-Xp)})
with open(OUT/'exact_adequacy_transfer_checks_step62.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# defective bridge checks
rows=[]
for trial in range(50):
    n=7; y=3; z=3; zp=2
    C=spd(n,0.8)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    A=spd(y,0.2)
    B=rng.normal(size=(zp,z))
    R=0.25*rng.normal(size=(zp,n))
    t=0.7 + rng.random()
    X=xi(C,L,D)
    Xp=xi(C,A@L,B@D+R)
    XR=xi(C,A@L,R)
    bound=(1+t)*B@X@B.T+(1+1/t)*XR
    rows.append({'trial':trial,'t':t,'min_eig_bound_minus_actual':min_eig(bound-Xp),'trace_actual':np.trace(Xp),'trace_bound':np.trace(bound)})
with open(OUT/'defective_adequacy_transfer_checks_step62.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# adequacy promotion checks
rows=[]
for trial in range(50):
    n=9; y=4; z=3
    C=spd(n,1.0)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    Ci=np.linalg.inv(C)
    KLL=L@Ci@L.T
    KDL=D@Ci@L.T
    KDD=D@Ci@D.T
    X=xi(C,L,D)
    Astar=KDL@pinv(KLL)
    Theta=KLL+0.3*np.eye(y)
    Xi_budget=X+0.2*np.eye(z)
    bound=Astar@Theta@Astar.T+Xi_budget
    rows.append({'trial':trial,'min_eig_bound_minus_KDD':min_eig(bound-KDD),'trace_KDD':np.trace(KDD),'trace_bound':np.trace(bound)})
with open(OUT/'adequacy_promotion_checks_step62.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# public shadow overread example
rows=[]
for M in [1,3,10,30,100,300,1000]:
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,M],[0.0,0.0]])  # one hidden dissolving coord plus zero public coord-ish
    F=np.array([[0.0,1.0]]) # forget first/intrinsic hidden coordinate, see zero coord
    Xi_full=xi(C,L,D)
    Xi_pub=xi(C,L,F@D)
    rows.append({'M':M,'xi_intrinsic_trace':float(np.trace(Xi_full)),'xi_public_trace':float(np.trace(Xi_pub))})
with open(OUT/'public_shadow_adequacy_overread_step62.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

print('step62 checks complete')
