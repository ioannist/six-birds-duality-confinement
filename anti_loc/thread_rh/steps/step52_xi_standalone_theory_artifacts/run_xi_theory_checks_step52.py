import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step52_xi_theory')
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(52052)

def psd_sqrt_inv(C, tol=1e-10):
    w, V = np.linalg.eigh((C + C.T.conj())/2)
    pos = w > tol
    inv = V[:, pos] @ np.diag(1/w[pos]) @ V[:, pos].T.conj()
    inv_sqrt = V[:, pos] @ np.diag(1/np.sqrt(w[pos])) @ V[:, pos].T.conj()
    return inv, inv_sqrt, pos.sum()

def xi_blocks(C, L, D, tol=1e-10):
    # assumes C positive definite for checks
    Cinv = np.linalg.inv(C)
    KLL = L @ Cinv @ L.T
    KDL = D @ Cinv @ L.T
    KLD = KDL.T
    KDD = D @ Cinv @ D.T
    Xi = KDD - KDL @ np.linalg.pinv(KLL, rcond=tol) @ KLD
    return KLL, KDL, KLD, KDD, (Xi+Xi.T)/2

def rand_spd(n, cond=20):
    Q, _ = np.linalg.qr(rng.normal(size=(n,n)))
    vals = np.geomspace(1, cond, n)
    return Q @ np.diag(vals) @ Q.T

# 1. residual identity checks
rows=[]
for trial in range(80):
    n=8; y=4; z=3
    C=rand_spd(n, cond=50)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    KLL,KDL,KLD,KDD,Xi=xi_blocks(C,L,D)
    Astar=KDL @ np.linalg.pinv(KLL)
    Cinv=np.linalg.inv(C)
    max_err=0.0
    min_eig_decrease=None
    for _ in range(10):
        A=rng.normal(size=(z,y))
        R=(D-A@L)@Cinv@(D-A@L).T
        RHS=Xi+(A-Astar)@KLL@(A-Astar).T
        err=np.linalg.norm(R-RHS, ord=2)
        max_err=max(max_err,err)
    eigs=np.linalg.eigvalsh(Xi)
    rows.append(dict(trial=trial, residual_identity_max_error=max_err, xi_min_eig=eigs.min(), xi_trace=np.trace(Xi)))
pd.DataFrame(rows).to_csv(OUT/'xi_residual_identity_checks_step52.csv', index=False)

# 2. chain rule/strict extension checks
rows=[]
for trial in range(80):
    n=10; y=3; w=2; z=4
    C=rand_spd(n, cond=30)
    L=rng.normal(size=(y,n))
    M=rng.normal(size=(w,n))
    D=rng.normal(size=(z,n))
    KLL,KDL,KLD,KDD,Xi_L=xi_blocks(C,L,D)
    Lp=np.vstack([L,M])
    _,_,_,_,Xi_LM=xi_blocks(C,Lp,D)
    decrease=(Xi_L-Xi_LM + (Xi_L-Xi_LM).T)/2
    rows.append(dict(trial=trial, min_eig_decrease=np.linalg.eigvalsh(decrease).min(), trace_before=np.trace(Xi_L), trace_after=np.trace(Xi_LM), trace_drop=np.trace(decrease)))
pd.DataFrame(rows).to_csv(OUT/'xi_chain_rule_checks_step52.csv', index=False)

# 3. strict extension ladder: add probes toward hidden coordinate.
Mvals=np.geomspace(1,1e4,80)
rows=[]
for Mscale in Mvals:
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,Mscale]])
    _,_,_,_,Xi0=xi_blocks(C,L,D)
    # add native probe alpha * x2, where alpha grows
    alpha=np.sqrt(Mscale)  # growing native visibility, not full equality
    Lp=np.array([[1.0,0.0],[0.0,alpha]])
    _,_,_,_,Xi1=xi_blocks(C,Lp,D)
    rows.append(dict(M=Mscale, xi_before=Xi0[0,0], alpha=alpha, xi_after=Xi1[0,0]))
pd.DataFrame(rows).to_csv(OUT/'strict_extension_residual_ladder_step52.csv', index=False)

# 4. exact adequacy and blind spot table
rows=[]
for Mscale in [1,10,100,1000,10000]:
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D_blind=np.array([[0.0,Mscale]])
    D_seen=np.array([[Mscale,0.0]])
    _,_,_,_,Xi_blind=xi_blocks(C,L,D_blind)
    _,_,_,_,Xi_seen=xi_blocks(C,L,D_seen)
    rows.append(dict(M=Mscale, xi_blind=Xi_blind[0,0], xi_exact_adequate=Xi_seen[0,0]))
pd.DataFrame(rows).to_csv(OUT/'exact_adequacy_and_blind_spot_step52.csv', index=False)

# 5. predictive ladders: summable vs nonsummable residual
N=200
rows_s=[]; rows_n=[]
xi=1.0
for j in range(1,N+1):
    # summable perturbations
    xi = xi + 1/(j+1)**2
    rows_s.append(dict(j=j, xi=xi))
xi=1.0
for j in range(1,N+1):
    xi = xi + 1/(j+1)
    rows_n.append(dict(j=j, xi=xi))
pd.DataFrame(rows_s).to_csv(OUT/'summable_xi_residual_ladder_step52.csv', index=False)
pd.DataFrame(rows_n).to_csv(OUT/'nonsummable_xi_residual_ladder_step52.csv', index=False)

# 6. null mode fake zero
rows=[]
C=np.diag([0.0,1.0])
Cpinv=np.diag([0.0,1.0])
D=np.array([[1.0,0.0]])
pseudo=float((D@Cpinv@D.T)[0,0])
rows.append(dict(case='D sees null mode', pseudoinverse_currency=pseudo, true_variational_capacity='infinite', null_legal=False))
D2=np.array([[0.0,1.0]])
pseudo2=float((D2@Cpinv@D2.T)[0,0])
rows.append(dict(case='D annihilates null mode', pseudoinverse_currency=pseudo2, true_variational_capacity=pseudo2, null_legal=True))
pd.DataFrame(rows).to_csv(OUT/'null_mode_fake_xi_zero_step52.csv', index=False)

# plots
blind=pd.read_csv(OUT/'exact_adequacy_and_blind_spot_step52.csv')
plt.figure(figsize=(6,4))
plt.loglog(blind['M'], blind['xi_blind'], marker='o', label='blind dissolving residual')
plt.loglog(blind['M'], blind['xi_exact_adequate']+1e-30, marker='x', label='exact adequate residual')
plt.xlabel('blind spot scale M')
plt.ylabel(r'$\Xi_C(D\mid L)$')
plt.title('Adequacy residual detects hidden dissolving blind spots')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'xi_hidden_blind_spot_step52.png', dpi=180)
plt.close()

lad=pd.read_csv(OUT/'strict_extension_residual_ladder_step52.csv')
plt.figure(figsize=(6,4))
plt.loglog(lad['M'], lad['xi_before'], label='before native extension')
plt.loglog(lad['M'], lad['xi_after']+1e-30, label='after extension seeing blind spot')
plt.xlabel('dissolving scale M')
plt.ylabel(r'$\Xi$')
plt.title('Strict extension reduces adequacy residual')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'strict_extension_xi_ladder_step52.png', dpi=180)
plt.close()

summ=pd.read_csv(OUT/'summable_xi_residual_ladder_step52.csv')
non=pd.read_csv(OUT/'nonsummable_xi_residual_ladder_step52.csv')
plt.figure(figsize=(6,4))
plt.plot(summ['j'], summ['xi'], label='summable residual defects')
plt.plot(non['j'], non['xi'], label='non-summable residual defects')
plt.xlabel('stage j')
plt.ylabel(r'predictive residual budget')
plt.title('Predictive adequacy: summable vs non-summable residuals')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'predictive_xi_residual_ladders_step52.png', dpi=180)
plt.close()

# print quick summary
print('wrote step52 checks to', OUT)
print('max residual identity error', pd.read_csv(OUT/'xi_residual_identity_checks_step52.csv')['residual_identity_max_error'].max())
print('min chain-rule decrease eig', pd.read_csv(OUT/'xi_chain_rule_checks_step52.csv')['min_eig_decrease'].min())
