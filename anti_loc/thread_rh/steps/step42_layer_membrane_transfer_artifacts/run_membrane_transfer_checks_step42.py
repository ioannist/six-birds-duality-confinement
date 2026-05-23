import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
out = Path('/mnt/data/anti_localization_step42_transfer')

def psd(n, scale=1.0):
    A = rng.normal(size=(n,n))
    return scale*(A.T@A) + 1e-8*np.eye(n)

def min_eig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

def pinv_sqrt(C):
    vals, vecs = np.linalg.eigh((C+C.T)/2)
    vals = np.maximum(vals, 0)
    inv_sqrt = np.zeros_like(vals)
    mask = vals > 1e-10
    inv_sqrt[mask] = 1/np.sqrt(vals[mask])
    return vecs @ np.diag(inv_sqrt) @ vecs.T

def pinv(C):
    vals, vecs = np.linalg.eigh((C+C.T)/2)
    vals = np.maximum(vals, 0)
    inv = np.zeros_like(vals)
    mask = vals > 1e-10
    inv[mask] = 1/vals[mask]
    return vecs @ np.diag(inv) @ vecs.T

# 1. Witness transfer random checks
rows=[]
for trial in range(60):
    n=5; m=3; mp=4; np_=6
    C = psd(n)
    L = rng.normal(size=(m,n))
    W = pinv_sqrt(C) @ L.T  # n x m
    K = W.T @ W
    R = rng.normal(size=(m,mp))
    U0 = rng.normal(size=(np_, n))
    # scale U so U^T U <= alpha I with alpha known
    op = np.linalg.norm(U0,2)
    alpha = 1.7
    U = U0 / op * np.sqrt(alpha) * 0.8
    D = 0.05*rng.normal(size=(np_,mp))
    Wp = U @ W @ R + D
    Kp = Wp.T @ Wp
    E = D.T @ D
    t=0.7
    bound = (1+t)*alpha*R.T@K@R + (1+1/t)*E
    rows.append({
        'trial': trial,
        'min_eig_bound_minus_Kp': min_eig(bound-Kp),
        'trace_Kp': float(np.trace(Kp)),
        'trace_bound': float(np.trace(bound))
    })
pd.DataFrame(rows).to_csv(out/'witness_transfer_checks_step42.csv', index=False)

# 2. Compression DPI checks
rows=[]
for trial in range(60):
    n=7; m=4; k=3
    C=psd(n)
    L=rng.normal(size=(m,n))
    K=L@pinv(C)@L.T
    # random subspace basis V n x k orthonormal
    Q,_=np.linalg.qr(rng.normal(size=(n,k)))
    Cv=Q.T@C@Q
    Lv=L@Q
    Kv=Lv@pinv(Cv)@Lv.T
    rows.append({'trial': trial, 'min_eig_K_minus_Kv': min_eig(K-Kv), 'trace_K': float(np.trace(K)), 'trace_Kv': float(np.trace(Kv))})
pd.DataFrame(rows).to_csv(out/'compression_dpi_checks_step42.csv', index=False)

# 3. Public shadow no reverse
Ms=[1,10,100,1000,10000]
rows=[]
P=np.array([[1.0,0.0]])
for M in Ms:
    K=np.diag([0.0,M])
    Kpub=P@K@P.T
    rows.append({'M_hidden': M, 'public_currency': float(Kpub[0,0]), 'lawful_max_currency': float(np.linalg.eigvalsh(K).max())})
pd.DataFrame(rows).to_csv(out/'public_shadow_no_reverse_step42.csv', index=False)

# 4. Variational transfer simple scalar check
rows=[]
for eps in [1,0.5,0.1,0.01,0.001]:
    C=np.array([[1.0]])
    Cp=np.array([[eps]])
    L=np.array([[1.0]])
    Lp=np.array([[1.0]])
    K=L@pinv(C)@L.T
    Kp=Lp@pinv(Cp)@Lp.T
    # no energy domination with small eps unless alpha >= 1/eps
    alpha=1/eps
    bound=alpha*K
    rows.append({'eps_target_audit': eps, 'K_source': float(K[0,0]), 'K_target': float(Kp[0,0]), 'needed_alpha': alpha, 'bound': float(bound[0,0])})
pd.DataFrame(rows).to_csv(out/'same_readout_different_audit_step42.csv', index=False)
print('Step 42 checks written.')
