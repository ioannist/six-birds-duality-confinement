import numpy as np
import pandas as pd
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step72_feature_maps')
rng = np.random.default_rng(72)

# 1. Shift symbol positivity sanity: Psi(xi)=sum w_a |e^{ia xi}-1|^2 >=0
rows=[]
for trial in range(20):
    shifts = rng.uniform(0.05, 4.0, size=12)
    weights = rng.uniform(0.01, 2.0, size=12)
    xis = np.linspace(-10,10,2001)
    psi = np.zeros_like(xis)
    for a,w in zip(shifts,weights):
        psi += w*np.abs(np.exp(1j*a*xis)-1.0)**2
    rows.append({
        'trial': trial,
        'min_symbol': float(psi.min()),
        'max_symbol': float(psi.max()),
        'positive_within_tol': bool(psi.min() >= -1e-12)
    })
pd.DataFrame(rows).to_csv(out/'shift_symbol_positivity_checks_step72.csv', index=False)

# 2. Trace equality not domination countermodels
rows=[]
for scale in [1,2,5,10,50,100]:
    A = np.diag([scale, 1/scale])
    K = np.eye(2) * ((scale + 1/scale)/2)
    # same trace, but A <= K fails if scale > average
    eig = np.linalg.eigvalsh(K-A)
    rows.append({
        'scale': scale,
        'trace_A': float(np.trace(A)),
        'trace_K': float(np.trace(K)),
        'min_eig_K_minus_A': float(eig.min()),
        'loewner_domination': bool(eig.min() >= -1e-12)
    })
pd.DataFrame(rows).to_csv(out/'trace_not_domination_countermodel_step72.csv', index=False)

# 3. Signed-piece repair algebra: signed S=P-N. Positive carrier needs P plus defect N if S is to dominate a positive target.
rows=[]
for trial in range(20):
    X = rng.normal(size=(4,4)); P = X.T@X
    Y = rng.normal(size=(4,4)); N = Y.T@Y
    S = P-N
    # If a target A is <= S, not generally possible if S indefinite. Repair P dominates S plus N.
    eigS = np.linalg.eigvalsh(S)
    eigPminusS = np.linalg.eigvalsh(P-S) # = N
    rows.append({
        'trial': trial,
        'min_eig_signed_piece': float(eigS.min()),
        'signed_piece_psd': bool(eigS.min() >= -1e-12),
        'min_eig_repair_P_minus_signed': float(eigPminusS.min()),
        'repair_defect_psd': bool(eigPminusS.min() >= -1e-12)
    })
pd.DataFrame(rows).to_csv(out/'signed_component_repair_checks_step72.csv', index=False)

print('wrote step72 sanity CSVs')
