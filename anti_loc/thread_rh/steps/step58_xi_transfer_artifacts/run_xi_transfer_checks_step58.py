import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT=Path('/mnt/data/anti_localization_step58_xi_transfer')
OUT.mkdir(exist_ok=True, parents=True)
rng=np.random.default_rng(58)

def psd(n, ridge=0.5):
    A=rng.normal(size=(n,n))
    return A.T@A + ridge*np.eye(n)

def pinv(A, tol=1e-10):
    return np.linalg.pinv(A, rcond=tol)

def sqrt_inv(A):
    w,V=np.linalg.eigh((A+A.T)/2)
    w=np.clip(w,1e-12,None)
    return V@np.diag(1/np.sqrt(w))@V.T

def xi(C,L,D):
    Ci=pinv(C)
    KLL=L@Ci@L.T
    KDL=D@Ci@L.T
    KDD=D@Ci@D.T
    return (KDD - KDL@pinv(KLL)@KDL.T + (KDD - KDL@pinv(KLL)@KDL.T).T)/2

def loewner_min(A):
    return np.min(np.linalg.eigvalsh((A+A.T)/2))

def opnorm(A):
    return np.linalg.norm(A,2)

# 1. post-processing equality Xi(FD|L)=F Xi(D|L) F^T
rows=[]
for trial in range(80):
    n=8; y=4; z=5; z2=3
    C=psd(n)
    L=rng.normal(size=(y,n)); D=rng.normal(size=(z,n)); F=rng.normal(size=(z2,z))
    X=xi(C,L,D); Xp=xi(C,L,F@D); rhs=F@X@F.T
    rows.append({'trial':trial,'fro_error':np.linalg.norm(Xp-rhs,'fro'),'op_error':opnorm(Xp-rhs)})
pd.DataFrame(rows).to_csv(OUT/'postprocess_equality_step58.csv', index=False)

# 2. faithful native presentation invariance: L' = J L, J has left inverse.
rows=[]
for trial in range(80):
    n=8; y=4; yp=7; z=5
    C=psd(n)
    L=rng.normal(size=(y,n)); D=rng.normal(size=(z,n))
    J=rng.normal(size=(yp,y))
    # ensure full column rank
    while np.linalg.matrix_rank(J)<y:
        J=rng.normal(size=(yp,y))
    X=xi(C,L,D); Xp=xi(C,J@L,D)
    rows.append({'trial':trial,'fro_error':np.linalg.norm(Xp-X,'fro'),'op_error':opnorm(Xp-X)})
pd.DataFrame(rows).to_csv(OUT/'faithful_native_presentation_step58.csv', index=False)

# 3. native coarsening can increase Xi: L_full=[e1,e2], L_shadow=e1, D=e2*M
Mvals=np.logspace(0,5,80)
rows=[]
for M in Mvals:
    C=np.eye(2)
    Lfull=np.eye(2)
    Lshadow=np.array([[1.0,0.0]])
    D=np.array([[0.0,M]])
    Xfull=xi(C,Lfull,D)[0,0]
    Xshadow=xi(C,Lshadow,D)[0,0]
    rows.append({'M':M,'xi_full':Xfull,'xi_shadow':Xshadow})
pd.DataFrame(rows).to_csv(OUT/'native_coarsening_blindspot_step58.csv', index=False)
plt.figure(figsize=(6,4))
plt.loglog(Mvals,[r['xi_shadow'] for r in rows], label='coarsened native family')
plt.loglog(Mvals,[max(r['xi_full'],1e-16) for r in rows], label='full native family')
plt.xlabel('hidden dissolving gain M')
plt.ylabel('Xi')
plt.title('Native coarsening can create a blind spot')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'native_coarsening_blindspot_step58.png', dpi=180)
plt.close()

# 4. exact carrier pullback DPI sanity: E target subspace via P, compare Xi_target <= Xi_source
rows=[]
for trial in range(80):
    n=9; m=5; y=4; z=3
    C=psd(n, ridge=1.0)
    P=rng.normal(size=(n,m))
    Cp=P.T@C@P + 0.2*psd(m, ridge=0.1)  # stronger than pullback
    L=rng.normal(size=(y,n)); D=rng.normal(size=(z,n))
    Xs=xi(C,L,D)
    Xt=xi(Cp,L@P,D@P)
    diff=Xs-Xt
    rows.append({'trial':trial,'min_eig_source_minus_target':loewner_min(diff),'norm_target':opnorm(Xt),'norm_source':opnorm(Xs)})
pd.DataFrame(rows).to_csv(OUT/'carrier_pullback_dpi_step58.csv', index=False)

# 5. defective D readout transfer: D' = D + R with Xi bound <= (1+t)Xi + (1+1/t)E_R; choose t=1
rows=[]
for trial in range(80):
    n=8; y=4; z=3
    C=psd(n, ridge=1.0)
    L=rng.normal(size=(y,n)); D=rng.normal(size=(z,n)); R=0.1*rng.normal(size=(z,n))
    X=xi(C,L,D); Xp=xi(C,L,D+R)
    E=R@pinv(C)@R.T
    bound=2*X+2*E
    rows.append({'trial':trial,'min_eig_bound_minus_actual':loewner_min(bound-Xp),'norm_actual':opnorm(Xp),'norm_bound':opnorm(bound)})
pd.DataFrame(rows).to_csv(OUT/'defective_dissolving_transfer_step58.csv', index=False)

# 6. composition of post-processing: F2 F1 equality.
rows=[]
for trial in range(80):
    n=8; y=4; z=5; z1=4; z2=3
    C=psd(n); L=rng.normal(size=(y,n)); D=rng.normal(size=(z,n))
    F1=rng.normal(size=(z1,z)); F2=rng.normal(size=(z2,z1))
    X=xi(C,L,D); X2=xi(C,L,F2@F1@D); rhs=F2@F1@X@F1.T@F2.T
    rows.append({'trial':trial,'fro_error':np.linalg.norm(X2-rhs,'fro')})
pd.DataFrame(rows).to_csv(OUT/'postprocess_composition_step58.csv', index=False)

# 7. Singular null-mode fake transfer example
C=np.diag([0.0,1.0])
L=np.array([[0.0,1.0]])
D_null=np.array([[1.0,0.0]])
# Pseudoinverse expression for D null is zero, but true variational capacity infinite; record.
pd.DataFrame([{'case':'D sees null mode','pseudoinverse_currency':float(D_null@pinv(C)@D_null.T),'true_capacity':'infinite','status':'failed_null_legality'}]).to_csv(OUT/'null_mode_transfer_warning_step58.csv', index=False)
