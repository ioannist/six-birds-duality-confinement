#!/usr/bin/env python3
"""Finite algebra checks for Step 62 adequacy-aware membrane transfer.
These are sanity checks of PSD inequalities, not Six Birds simulations.
"""
import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step62_adequacy_transfer')
rng = np.random.default_rng(62062)

def psd_sqrt_inv(A, tol=1e-10):
    w, V = np.linalg.eigh((A + A.T)/2)
    wi = np.array([1/np.sqrt(x) if x > tol else 0.0 for x in w])
    return V @ np.diag(wi) @ V.T

def pinv(A, tol=1e-10):
    return np.linalg.pinv((A + A.T)/2, rcond=tol)

def min_eig(A):
    return float(np.linalg.eigvalsh((A + A.T)/2).min())

def max_eig(A):
    return float(np.linalg.eigvalsh((A + A.T)/2).max())

def make_spd(n, floor=0.5):
    X = rng.normal(size=(n,n))
    return X.T @ X + floor*np.eye(n)

def xi(C, L, D):
    Cinv = np.linalg.inv(C)
    KLL = L @ Cinv @ L.T
    KDL = D @ Cinv @ L.T
    KDD = D @ Cinv @ D.T
    Xi = KDD - KDL @ pinv(KLL) @ KDL.T
    return (Xi+Xi.T)/2, KLL, KDL, KDD

# 1 exact transfer equality in simple exact reducing bridge
exact_rows = []
for trial in range(50):
    n=6; y=4; z=3; zp=2
    C = make_spd(n, 1.0)
    L = rng.normal(size=(y,n))
    D = rng.normal(size=(z,n))
    B = rng.normal(size=(zp,z))
    Cprime = C.copy(); P=np.eye(n); Dprime=B@D
    Xisrc,KLL,KDL,KDD = xi(C,L,D)
    Xitgt,_,_,_ = xi(Cprime,L,Dprime)
    err = np.linalg.norm(Xitgt - B@Xisrc@B.T, ord=2)
    exact_rows.append({'trial':trial,'exact_xi_transfer_error':err})
pd.DataFrame(exact_rows).to_csv(OUT/'exact_xi_transfer_checks_step62.csv', index=False)

# 2 dissolving budget theorem random checks
budget_rows=[]
for trial in range(80):
    n=7; y=4; z=3; zp=3
    C=make_spd(n,1.0)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    Xi,KLL,KDL,KDD=xi(C,L,D)
    Astar=KDL@pinv(KLL)
    ThetaY=KLL + 0.2*np.eye(y)
    XiZ=Xi + 0.2*np.eye(z)
    source_budget=Astar@ThetaY@Astar.T+XiZ
    # target with same space and exact bridge + residual
    B=rng.normal(size=(zp,z))/np.sqrt(z)
    R=rng.normal(size=(zp,n))*0.05
    Dp=B@D+R
    Cp=C.copy()
    Kp=Dp@np.linalg.inv(Cp)@Dp.T
    ED=R@np.linalg.inv(Cp)@R.T
    t=1.0
    bound=(1+t)*B@source_budget@B.T+(1+1/t)*ED
    budget_rows.append({
        'trial':trial,
        'min_eig_bound_minus_actual':min_eig(bound-Kp),
        'actual_maxeig':max_eig(Kp),
        'bound_maxeig':max_eig(bound),
        'residual_trace':float(np.trace(ED))
    })
pd.DataFrame(budget_rows).to_csv(OUT/'dissolving_budget_transfer_checks_step62.csv', index=False)

# 3 adequacy residual transfer with native reconstruction
res_rows=[]
for trial in range(80):
    n=6; y=4; yp=5; z=3; zp=3
    C=make_spd(n,1.0)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    Xi,KLL,KDL,KDD=xi(C,L,D)
    Astar=KDL@pinv(KLL)
    # target native L' contains L plus a small extra, so R reconstructs L exactly
    extra=rng.normal(size=(yp-y,n))*0.2
    Lp=np.vstack([L,extra])
    Rrec=np.hstack([np.eye(y), np.zeros((y,yp-y))])
    B=rng.normal(size=(zp,z))/np.sqrt(z)
    Rd=rng.normal(size=(zp,n))*0.03
    Dp=B@D+Rd
    Xitgt,_,_,_=xi(C,Lp,Dp)
    ED=Rd@np.linalg.inv(C)@Rd.T
    bound=3*B@(Xi+1e-12*np.eye(z))@B.T + 3*ED  # E_L = 0
    res_rows.append({
        'trial':trial,
        'min_eig_bound_minus_xi_target':min_eig(bound-Xitgt),
        'xi_target_trace':float(np.trace(Xitgt)),
        'bound_trace':float(np.trace(bound))
    })
pd.DataFrame(res_rows).to_csv(OUT/'adequacy_residual_transfer_checks_step62.csv', index=False)

# 4 public shadow overread
shadow_rows=[]
for M in [1,3,10,30,100,300,1000,3000,10000]:
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,M],[0.0,0.0]])  # two response coordinates, second zero
    Xi_full,_,_,_=xi(C,L,D)
    F=np.array([[0.0,1.0]]) # public readout forgets dangerous first response coordinate
    Xi_pub=F@Xi_full@F.T
    shadow_rows.append({
        'M':M,
        'intrinsic_xi_maxeig':max_eig(Xi_full),
        'public_xi':float(Xi_pub[0,0])
    })
pd.DataFrame(shadow_rows).to_csv(OUT/'public_shadow_overread_step62.csv', index=False)

# 5 native reconstruction failure: target native coarsens source; xi can grow
coarse_rows=[]
for rho in np.linspace(0,1,21):
    C=np.eye(2)
    L=np.eye(2)
    D=np.eye(2)
    A=np.array([[1.0, rho]]) # coarsened native family one row
    Xi_full,_,_,_=xi(C,L,D)
    Xi_coarse,_,_,_=xi(C,A@L,D)
    coarse_rows.append({
        'rho':rho,
        'xi_full_maxeig':max_eig(Xi_full),
        'xi_coarse_maxeig':max_eig(Xi_coarse),
        'increase':max_eig(Xi_coarse-Xi_full)
    })
pd.DataFrame(coarse_rows).to_csv(OUT/'native_coarsening_failure_step62.csv', index=False)

print('Step 62 checks complete.')
