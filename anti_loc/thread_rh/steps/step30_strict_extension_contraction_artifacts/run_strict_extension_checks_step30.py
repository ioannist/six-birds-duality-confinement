import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step30_strictextension')
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(3001)

def spd(n, ridge=0.5):
    A = rng.normal(size=(n,n))
    return A.T @ A + ridge*np.eye(n)

def psd_sqrt(A):
    w, V = np.linalg.eigh((A+A.T)/2)
    return V @ np.diag(np.sqrt(np.maximum(w,0))) @ V.T

def inv(A):
    return np.linalg.inv((A+A.T)/2)

# 1 audit strengthening random trials
rows=[]
for trial in range(80):
    n=6; m=4
    C = spd(n, ridge=0.4)
    D0 = rng.normal(size=(n,n)); D = D0.T@D0 * (0.01 + trial/80)
    L = rng.normal(size=(m,n))
    K = L @ inv(C) @ L.T
    Kp = L @ inv(C+D) @ L.T
    eigdiff = np.linalg.eigvalsh((K-Kp + (K-Kp).T)/2)
    rel_drop = np.linalg.norm(K-Kp,2)/max(np.linalg.norm(K,2),1e-12)
    rows.append({
        'trial':trial,
        'min_eig_K_minus_Kplus':float(eigdiff.min()),
        'max_eig_K_minus_Kplus':float(eigdiff.max()),
        'relative_operator_drop':float(rel_drop),
        'status':'pass' if eigdiff.min() > -1e-9 else 'fail'
    })
pd.DataFrame(rows).to_csv(OUT/'audit_strengthening_checks_step30.csv', index=False)

# 2 same package coordinate invariance
rows=[]
for trial in range(50):
    n=5; m=3
    C=spd(n, ridge=0.5)
    L=rng.normal(size=(m,n))
    # random orthogonal U,V
    U,_ = np.linalg.qr(rng.normal(size=(n,n)))
    V,_ = np.linalg.qr(rng.normal(size=(m,m)))
    C2 = U.T @ C @ U
    L2 = V @ L @ U
    K = L @ inv(C) @ L.T
    K2 = L2 @ inv(C2) @ L2.T
    err = np.linalg.norm(K2 - V @ K @ V.T, ord=2)
    rows.append({'trial':trial,'coordinate_invariance_error':float(err)})
pd.DataFrame(rows).to_csv(OUT/'same_package_saturation_checks_step30.csv', index=False)

# 3 witness resolution under rank-one audit strengthening
n=4; m=2
C = np.diag([0.05, 1.0, 2.0, 3.0])
L = np.array([[1.0,0,0,0],[0,1.0,0,0]])
Theta = np.eye(m)
mu_values=np.logspace(-3,3,80)
rows=[]
for mu in mu_values:
    r=np.array([1.0,0,0,0])
    D=mu*np.outer(r,r)
    K=L@inv(C)@L.T
    Kp=L@inv(C+D)@L.T
    Ddef=Kp-Theta
    eig=np.linalg.eigvalsh((Ddef+Ddef.T)/2)
    rows.append({'mu':float(mu),'cap_probe1':float(Kp[0,0]),'cap_probe2':float(Kp[1,1]),'lambda_max_defect':float(max(eig.max(),0))})
pd.DataFrame(rows).to_csv(OUT/'rank_one_audit_contraction_step30.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(mu_values, [r['cap_probe1'] for r in rows], label='probe 1 capacity')
plt.loglog(mu_values, [r['lambda_max_defect'] for r in rows], label='positive defect')
plt.xlabel('rank-one audit strength $\\mu$')
plt.ylabel('value')
plt.title('Rank-one strict audit extension contracts the targeted witness')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'rank_one_audit_contraction_step30.png', dpi=180)
plt.close()

# 4 monotone nontermination and budget completion
N=np.arange(1,201)
defect=1/N
pd.DataFrame({'n':N,'K_n':1+defect,'Theta':1.0,'positive_defect':defect}).to_csv(OUT/'strict_extension_monotone_nontermination_step30.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(N, defect)
plt.xlabel('iteration n')
plt.ylabel('positive defect')
plt.title('Monotone improvement without finite completion')
plt.tight_layout()
plt.savefig(OUT/'strict_extension_monotone_nontermination_step30.png', dpi=180)
plt.close()

# 5 finite budget completion spectrum
A=rng.normal(size=(5,5)); D=A.T@A - 2*np.eye(5)
w,V=np.linalg.eigh((D+D.T)/2)
Dp=V@np.diag(np.maximum(w,0))@V.T
Drepaired=D-Dp
pd.DataFrame({
    'eigenvalue_original_defect':w,
    'eigenvalue_repaired_defect':np.linalg.eigvalsh((Drepaired+Drepaired.T)/2)
}).to_csv(OUT/'budget_completion_spectrum_step30.csv', index=False)

print('Step 30 checks complete')
