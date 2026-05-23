import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step63_layer_dissolving_master')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(6301)

def psd(n, scale=1.0):
    A = rng.normal(size=(n,n))
    return scale * (A @ A.T) / max(1,n)

def spd(n, shift=0.5):
    return psd(n) + shift*np.eye(n)

def sqrtm_psd(A):
    w,V=np.linalg.eigh((A+A.T)/2)
    w=np.clip(w,0,None)
    return V@np.diag(np.sqrt(w))@V.T

def invsqrt_psd(A, tol=1e-10):
    w,V=np.linalg.eigh((A+A.T)/2)
    winv=np.array([1/np.sqrt(x) if x>tol else 0 for x in w])
    return V@np.diag(winv)@V.T

def pinv(A):
    return np.linalg.pinv((A+A.T)/2, rcond=1e-10)

def maxeig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2)[-1])

def mineig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2)[0])

rows=[]
for trial in range(80):
    n = int(rng.integers(5,12))
    ydim = int(rng.integers(2,6))
    zdim = int(rng.integers(2,6))
    C = spd(n, shift=0.4)
    Ci = np.linalg.inv(C)
    L = rng.normal(size=(ydim,n))
    D = rng.normal(size=(zdim,n))
    KLL = L@Ci@L.T
    KDL = D@Ci@L.T
    KDD = D@Ci@D.T
    Astar = KDL@pinv(KLL)
    Xi = KDD - Astar@KLL@Astar.T
    Xi=(Xi+Xi.T)/2
    slackY = 0.05*np.eye(ydim) + 0.05*psd(ydim)
    slackZ = 0.05*np.eye(zdim) + 0.05*psd(zdim)
    ThetaY = KLL + slackY
    Omega = Xi + slackZ
    ThetaD = Astar@ThetaY@Astar.T + Omega
    diff = ThetaD - KDD
    # Deliberately underbudget to get a witness
    ThetaD_bad = ThetaD - 0.5*sqrtm_psd(slackZ)@sqrtm_psd(slackZ).T - 0.1*np.eye(zdim)
    viol = maxeig(KDD - ThetaD_bad)
    rows.append({
        'trial': trial,
        'n': n,
        'native_dim': ydim,
        'dissolving_dim': zdim,
        'min_eig_master_slack': mineig(diff),
        'max_eig_master_violation': maxeig(KDD-ThetaD),
        'xi_min_eig': mineig(Xi),
        'xi_trace': float(np.trace(Xi)),
        'bad_budget_max_violation': viol,
        'bad_budget_has_witness': bool(viol>1e-8),
    })

pd.DataFrame(rows).to_csv(OUT/'master_theorem_random_checks_step63.csv', index=False)

# Predictive propagation toy
rows=[]
K=np.array([[0.5,0.1],[0.1,0.4]])
Theta=np.eye(2)*2.0
for j in range(1,101):
    eps=0.01/(j*j)
    E=np.eye(2)*0.002/(j*j)
    K=(1+eps)*K + E
    rows.append({'stage':j,'lambda_max_K':maxeig(K),'lambda_max_K_minus_Theta':maxeig(K-Theta),'eps':eps,'defect_trace':float(np.trace(E))})
pd.DataFrame(rows).to_csv(OUT/'predictive_propagation_success_step63.csv', index=False)

# Non-summable failure toy
rows=[]
K=np.array([[0.1]])
Theta=np.array([[2.0]])
for j in range(1,501):
    E=np.array([[1.0/j]])
    K=K+E
    rows.append({'stage':j,'K':float(K[0,0]),'K_minus_Theta':float(K[0,0]-Theta[0,0]),'defect':float(E[0,0])})
pd.DataFrame(rows).to_csv(OUT/'predictive_nonsummable_failure_step63.csv', index=False)

# Hidden adequacy failure example
rows=[]
for M in np.logspace(0,5,40):
    C=np.eye(2)
    L=np.array([[1.0,0.0]])
    D=np.array([[0.0,M]])
    Ci=C
    KLL=L@Ci@L.T
    KDL=D@Ci@L.T
    KDD=D@Ci@D.T
    Xi=KDD - KDL@pinv(KLL)@KDL.T
    rows.append({'M':M,'native_currency':float(KLL[0,0]),'dissolving_currency':float(KDD[0,0]),'xi':float(Xi[0,0])})
pd.DataFrame(rows).to_csv(OUT/'hidden_adequacy_obstruction_step63.csv', index=False)
print('created step63 checks')
