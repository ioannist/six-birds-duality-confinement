import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT=Path('/mnt/data/anti_localization_step63_layer_dissolving_master')
rng=np.random.default_rng(63063)

def spd(n, shift=0.5):
    A=rng.normal(size=(n,n))
    return A.T@A + shift*np.eye(n)

def psd_sqrt_inv(C):
    w,V=np.linalg.eigh(C)
    return V @ np.diag(1/np.sqrt(w)) @ V.T

def pinv_psd(K, tol=1e-10):
    w,V=np.linalg.eigh((K+K.T)/2)
    return V @ np.diag([1/x if x>tol else 0.0 for x in w]) @ V.T

def xi_blocks(C,L,D):
    Ci=np.linalg.inv(C)
    KLL=L@Ci@L.T
    KDL=D@Ci@L.T
    KDD=D@Ci@D.T
    KLLp=pinv_psd(KLL)
    A=KDL@KLLp
    Xi=KDD-KDL@KLLp@KDL.T
    return KLL,KDL,KDD,A,(Xi+Xi.T)/2

# random exact master identity checks
rows=[]
for trial in range(80):
    n=int(rng.integers(5,12))
    y=int(rng.integers(2,6))
    z=int(rng.integers(2,6))
    C=spd(n, shift=0.3)
    L=rng.normal(size=(y,n))
    D=rng.normal(size=(z,n))
    S=rng.normal(size=(z,z))
    KLL,KDL,KDD,A,Xi=xi_blocks(C,L,D)
    identity=A@KLL@A.T+Xi
    id_err=np.linalg.norm(KDD-identity,2)
    ThetaY=KLL + spd(y, shift=0.1) # ensures KLL <= ThetaY
    Omega=Xi + spd(z, shift=0.1)
    rhs=A@ThetaY@A.T+Omega
    eig=np.linalg.eigvalsh((rhs-KDD+ (rhs-KDD).T)/2).min()
    transported=S@KDD@S.T
    target=S@rhs@S.T
    eig_trans=np.linalg.eigvalsh((target-transported+(target-transported).T)/2).min()
    rows.append({
        'trial':trial,'n':n,'native_dim':y,'dissolving_dim':z,
        'identity_error_opnorm':id_err,
        'min_eig_rhs_minus_kdd':eig,
        'min_eig_transported_bound':eig_trans,
        'trace_KLL':np.trace(KLL),'trace_Xi':np.trace(Xi),'trace_KDD':np.trace(KDD)
    })

pd.DataFrame(rows).to_csv(OUT/'master_theorem_random_checks_step63.csv',index=False)

# predictive stages simulated from fixed D/L budgets
rows=[]
Zdim=3
ThetaD=10*np.eye(Zdim)
for j in range(1,31):
    n=8; y=4; z=3
    C=spd(n, shift=0.5+0.05*j)
    L=rng.normal(size=(y,n))/np.sqrt(j)
    D=rng.normal(size=(z,n))/np.sqrt(j)
    S=np.eye(z)
    KLL,KDL,KDD,A,Xi=xi_blocks(C,L,D)
    ThetaY=KLL+0.2*np.eye(y)
    Omega=Xi+0.2*np.eye(z)
    stage_bound=S@(A@ThetaY@A.T+Omega)@S.T
    # Compare to a fixed common budget 10 I.
    max_rel=float(np.linalg.eigvalsh(stage_bound)[-1]/10.0)
    rows.append({'stage':j,'lambda_max_KD':np.linalg.eigvalsh(KDD)[-1],
                 'lambda_max_certified_stage_bound':np.linalg.eigvalsh(stage_bound)[-1],
                 'passes_common_budget_ThetaD_10I':np.linalg.eigvalsh(stage_bound-ThetaD).max()<=1e-9,
                 'trace_native':np.trace(KLL),'trace_xi':np.trace(Xi),'trace_dissolving':np.trace(KDD), 'max_relative_to_10I':max_rel})

pd.DataFrame(rows).to_csv(OUT/'predictive_layer_dissolving_checks_step63.csv',index=False)

# blind spot example: native L sees first coord, dissolving D sees hidden coord
rows=[]
for M in np.logspace(0,5,80):
    C=np.eye(2)
    L=np.array([[1.,0.]])
    D=np.array([[0.,M]])
    KLL,KDL,KDD,A,Xi=xi_blocks(C,L,D)
    rows.append({'M':M,'native_currency':KLL[0,0],'dissolving_currency':KDD[0,0],
                 'xi_blindspot':Xi[0,0], 'A_star':A[0,0]})
pd.DataFrame(rows).to_csv(OUT/'layer_dissolving_blindspot_sweep_step63.csv',index=False)

# plot blindspot
blind=pd.DataFrame(rows)
plt.figure(figsize=(6,4))
plt.loglog(blind['M'], blind['dissolving_currency'], label='dissolving currency')
plt.loglog(blind['M'], blind['xi_blindspot'], '--', label='Xi blind spot')
plt.axhline(1, color='gray', linestyle=':', label='native currency')
plt.xlabel('hidden dissolving scale M')
plt.ylabel('currency / residual')
plt.title('Layer-dissolving blind spot despite native membrane')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'layer_dissolving_blindspot_step63.png', dpi=200)
plt.close()

# plot predictive traces
pred=pd.read_csv(OUT/'predictive_layer_dissolving_checks_step63.csv')
plt.figure(figsize=(6,4))
plt.plot(pred['stage'], pred['trace_native'], label='native trace')
plt.plot(pred['stage'], pred['trace_xi'], label='Xi trace')
plt.plot(pred['stage'], pred['trace_dissolving'], label='dissolving trace')
plt.xlabel('stage')
plt.ylabel('trace')
plt.title('Stagewise native + adequacy controls dissolving currency')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'predictive_dissolving_currency_step63.png', dpi=200)
plt.close()
