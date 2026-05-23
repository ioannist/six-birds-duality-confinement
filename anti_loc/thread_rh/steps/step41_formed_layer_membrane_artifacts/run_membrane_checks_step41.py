import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step41_membrane')

rng = np.random.default_rng(41)

# 1. Finite eigenvalue certificate checks
rows=[]
for trial in range(50):
    n=5
    A=rng.normal(size=(n,n))
    K=A@A.T
    # make theta by scaling around K, alternately pass/fail
    scale = 1.25 if trial % 2 == 0 else 0.75
    Theta = scale * (K + 0.1*np.eye(n))
    # generalized eigenvalues via congruence
    w,V=np.linalg.eigh(Theta)
    Tinvsqrt=V@np.diag(1/np.sqrt(w))@V.T
    M=Tinvsqrt@K@Tinvsqrt
    lam=np.linalg.eigvalsh(M)[-1]
    rows.append({
        'trial':trial,
        'scale':scale,
        'lambda_max_Theta_inv_half_K':lam,
        'passes_membrane': bool(lam <= 1+1e-10)
    })
pd.DataFrame(rows).to_csv(OUT/'finite_eigen_certificate_checks_step41.csv', index=False)

# 2. Predictive failure vs propagation
rows=[]
Theta=np.eye(2)
for j in range(1,21):
    K=np.diag([1.0, j/5.0])
    lam=np.linalg.eigvalsh(K)[-1]
    rows.append({'model':'predictive_failure','j':j,'lambda_max':lam,'passes': bool(lam<=1+1e-12)})
# propagation model with summable defects
K=np.array([[0.2,0.0],[0.0,0.25]])
D_total=np.zeros((2,2))
for j in range(1,21):
    eps=0.02/(j*j)
    D=(0.01/(j*j))*np.eye(2)
    K=(1+eps)*K+D
    lam=np.linalg.eigvalsh(K)[-1]
    rows.append({'model':'summable_propagation','j':j,'lambda_max':lam,'passes': bool(lam<=1+1e-12)})
pd.DataFrame(rows).to_csv(OUT/'predictive_membrane_checks_step41.csv', index=False)

# 3. Critical-pair witness: diagonal passes but family fails
rows=[]
for m in range(2,21):
    K=np.ones((m,m))
    Theta=np.eye(m)
    eig=np.linalg.eigvalsh(K-Theta)[-1]
    diag_pass=np.all(np.diag(K)<=np.diag(Theta)+1e-12)
    y=np.ones(m)/np.sqrt(m)
    witness=float(y@(K-Theta)@y)
    rows.append({'m':m,'diagonal_pass':bool(diag_pass),'max_violation_eigenvalue':eig,'all_ones_witness':witness})
pd.DataFrame(rows).to_csv(OUT/'membrane_recombination_witness_step41.csv', index=False)

print('Step 41 checks written')
