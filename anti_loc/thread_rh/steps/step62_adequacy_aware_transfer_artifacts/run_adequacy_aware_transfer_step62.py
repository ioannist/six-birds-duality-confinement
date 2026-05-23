import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step62_adequacy_transfer')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(62062)

def spd(n, ridge=1.0):
    A = rng.normal(size=(n, n))
    return A.T @ A + ridge * np.eye(n)

def pinv_psd(A, tol=1e-10):
    A = (A + A.T) / 2
    w, V = np.linalg.eigh(A)
    wp = np.array([1.0 / x if x > tol else 0.0 for x in w])
    return V @ np.diag(wp) @ V.T

def xi(C, L, D):
    Cinv = pinv_psd(C)
    KLL = L @ Cinv @ L.T
    KDL = D @ Cinv @ L.T
    KDD = D @ Cinv @ D.T
    X = KDD - KDL @ pinv_psd(KLL) @ KDL.T
    return (X + X.T) / 2

def cur(C, L):
    Cinv = pinv_psd(C)
    X = L @ Cinv @ L.T
    return (X + X.T)/2

def min_eig(A):
    return float(np.min(np.linalg.eigvalsh((A + A.T) / 2)))

def max_eig(A):
    return float(np.max(np.linalg.eigvalsh((A + A.T) / 2)))

# Exact adequacy-aware transfer with faithful native response.
rows = []
for trial in range(80):
    n, m, r = 8, 4, 3
    C = spd(n, 0.8)
    L = rng.normal(size=(m, n))
    D = rng.normal(size=(r, n))
    U, _, Vt = np.linalg.svd(rng.normal(size=(m, m)))
    J = U @ np.diag(np.linspace(1.0, 2.0, m)) @ Vt  # invertible faithful native map
    B = rng.normal(size=(r, r))
    beta = 10 ** rng.uniform(-1, 1)
    Cp = beta * C
    Lp = J @ L
    Dp = B @ D
    Xi = xi(C, L, D)
    Xip = xi(Cp, Lp, Dp)
    bound = beta**-1 * B @ Xi @ B.T
    rows.append({
        'trial': trial,
        'beta': beta,
        'min_eig_bound_minus_actual': min_eig(bound - Xip),
        'actual_trace': float(np.trace(Xip)),
        'bound_trace': float(np.trace(bound)),
        'operator_error_exact_when_C_scaled': float(np.linalg.norm(bound - Xip, 2)),
    })
pd.DataFrame(rows).to_csv(OUT / 'exact_adequacy_aware_transfer_step62.csv', index=False)

# Defective bridge bound.
rows = []
for trial in range(80):
    n, m, r = 8, 4, 3
    C = spd(n, 0.5)
    L = rng.normal(size=(m, n))
    D = rng.normal(size=(r, n))
    B = rng.normal(size=(r, r))
    Rdef = 0.15 * rng.normal(size=(r, n))
    Dp = B @ D + Rdef
    Xip = xi(C, L, Dp)
    Xi_src = xi(C, L, D)
    Xi_R = xi(C, L, Rdef)
    for s in [0.25, 0.5, 1.0, 2.0, 4.0]:
        bound = (1 + s) * B @ Xi_src @ B.T + (1 + 1/s) * Xi_R
        rows.append({
            'trial': trial,
            's': s,
            'min_eig_bound_minus_actual': min_eig(bound - Xip),
            'actual_trace': float(np.trace(Xip)),
            'bound_trace': float(np.trace(bound)),
        })
pd.DataFrame(rows).to_csv(OUT / 'defective_adequacy_aware_transfer_step62.csv', index=False)

# Native coarsening: target native map not faithful; Xi can increase.
rows = []
for trial in range(80):
    n, m, r = 7, 3, 2
    C = spd(n, 0.5)
    L = rng.normal(size=(m, n))
    D = rng.normal(size=(r, n))
    A = np.array([[1., 0., 0.], [0., 1., 0.]])
    Xi_full = xi(C, L, D)
    Xi_coarse = xi(C, A @ L, D)
    rows.append({
        'trial': trial,
        'min_eig_coarse_minus_full': min_eig(Xi_coarse - Xi_full),
        'full_trace': float(np.trace(Xi_full)),
        'coarse_trace': float(np.trace(Xi_coarse)),
    })
pd.DataFrame(rows).to_csv(OUT / 'native_coarsening_failure_step62.csv', index=False)

# Public shadow overread.
rows = []
for M in np.logspace(0, 5, 60):
    C = np.eye(2)
    L = np.array([[1., 0.]])
    D = np.array([[0., M], [1., 0.]])
    F = np.array([[0., 1.]])
    Xi_full = xi(C, L, D)
    Xi_pub = xi(C, L, F @ D)
    rows.append({
        'M': M,
        'intrinsic_xi_max': max_eig(Xi_full),
        'public_xi': float(Xi_pub[0, 0]),
    })
pub = pd.DataFrame(rows)
pub.to_csv(OUT / 'public_shadow_xi_overread_step62.csv', index=False)

# Plots
plt.figure(figsize=(7, 4))
plt.loglog(pub['M'], pub['intrinsic_xi_max'], label='intrinsic Xi')
plt.loglog(pub['M'], np.maximum(pub['public_xi'], 1e-16), label='public-shadow Xi')
plt.xlabel('hidden blind-spot scale M')
plt.ylabel('Xi')
plt.title('Public shadow can hide intrinsic adequacy residual')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'public_shadow_xi_overread_step62.png', dpi=180)
plt.close()

coarse = pd.read_csv(OUT / 'native_coarsening_failure_step62.csv')
plt.figure(figsize=(7,4))
plt.scatter(coarse['full_trace'], coarse['coarse_trace'], s=16)
mx = max(coarse['full_trace'].max(), coarse['coarse_trace'].max())
plt.plot([0,mx],[0,mx])
plt.xlabel('Xi trace with full native family')
plt.ylabel('Xi trace after native coarsening')
plt.title('Native coarsening can enlarge blind spot')
plt.tight_layout()
plt.savefig(OUT / 'native_coarsening_failure_step62.png', dpi=180)
plt.close()

defect = pd.read_csv(OUT / 'defective_adequacy_aware_transfer_step62.csv')
plt.figure(figsize=(7,4))
for s, grp in defect.groupby('s'):
    plt.scatter(grp['actual_trace'], grp['bound_trace'], s=10, label=f's={s}')
mx = max(defect['actual_trace'].max(), defect['bound_trace'].max())
plt.plot([0,mx],[0,mx])
plt.xlabel('actual target Xi trace')
plt.ylabel('defect-paid bound trace')
plt.title('Defective adequacy-aware bridge bound')
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig(OUT / 'defective_adequacy_transfer_bound_step62.png', dpi=180)
plt.close()

print('wrote step62 adequacy-aware transfer checks')
