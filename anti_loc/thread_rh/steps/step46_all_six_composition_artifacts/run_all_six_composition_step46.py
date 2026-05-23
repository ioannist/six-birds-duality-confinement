#!/usr/bin/env python3
"""Sanity checks for Step 46 all-six membrane composition.

These are small PSD algebra checks, not Six Birds simulations.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step46_composition')
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(46046)

def psd(n: int, scale: float = 1.0) -> np.ndarray:
    A = rng.normal(size=(n,n))
    return scale * (A @ A.T) / max(n, 1)

def sym(A: np.ndarray) -> np.ndarray:
    return (A + A.T)/2

def min_eig(A: np.ndarray) -> float:
    return float(np.linalg.eigvalsh(sym(A)).min())

def max_eig(A: np.ndarray) -> float:
    return float(np.linalg.eigvalsh(sym(A)).max())

# 1. Random two-step composition checks.
rows = []
for trial in range(100):
    n0 = 4
    n1 = 5
    n2 = 3
    K0 = psd(n0, scale=1.0)
    A01 = rng.normal(size=(n1,n0))/np.sqrt(n0)
    A12 = rng.normal(size=(n2,n1))/np.sqrt(n1)
    alpha01 = 1.0 + 0.2*rng.random()
    alpha12 = 1.0 + 0.2*rng.random()
    E01 = psd(n1, scale=0.05)
    E12 = psd(n2, scale=0.05)
    # Define K1 and K2 below the certified upper bounds by subtracting a small PSD slack.
    U1 = alpha01 * A01 @ K0 @ A01.T + E01
    # choose K1 strictly below the certified upper bound
    K1 = 0.8*U1
    U2 = alpha12 * A12 @ K1 @ A12.T + E12
    K2 = 0.9*U2
    composed = alpha12*alpha01*(A12@A01)@K0@(A12@A01).T + alpha12*A12@E01@A12.T + E12
    gap = composed - K2
    rows.append({
        'trial': trial,
        'alpha01': alpha01,
        'alpha12': alpha12,
        'min_eig_composed_minus_K2': min_eig(gap),
        'max_eig_K2': max_eig(K2),
        'max_eig_composed': max_eig(composed),
        'passed': min_eig(gap) >= -1e-9,
    })

pd.DataFrame(rows).to_csv(OUT/'composition_random_checks_step46.csv', index=False)

# 2. Chain defect propagation scalar example.
rows = []
K = np.array([[1.0]])
Theta0 = np.array([[1.0]])
K_current = K.copy()
prod_alpha = 1.0
prop_bound = Theta0.copy()
for j in range(1, 51):
    eps = 0.02/(j**1.4)
    alpha = 1.0 + eps
    E = np.array([[0.002/(j**1.8)]])
    # Actual K follows a smaller update.
    K_current = 0.95*(alpha*K_current + E)
    # Certified bound follows full update.
    prop_bound = alpha*prop_bound + E
    prod_alpha *= alpha
    rows.append({
        'stage': j,
        'epsilon': eps,
        'defect': float(E[0,0]),
        'actual_K': float(K_current[0,0]),
        'propagated_bound': float(prop_bound[0,0]),
        'product_alpha': prod_alpha,
    })
chain_df = pd.DataFrame(rows)
chain_df.to_csv(OUT/'predictive_chain_defect_propagation_step46.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.plot(chain_df['stage'], chain_df['actual_K'], label='actual currency')
plt.plot(chain_df['stage'], chain_df['propagated_bound'], label='propagated bound')
plt.xlabel('stage')
plt.ylabel('scalar budget')
plt.title('Step 46: predictive defect propagation')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'predictive_defect_propagation_step46.png', dpi=180)
plt.close()

# 3. Public shadow overread: visible passes, hidden intrinsic fails.
rows = []
for M in [1,2,5,10,25,50,100,250,500,1000]:
    K = np.diag([1.0, float(M)])
    Theta = np.eye(2)
    F = np.array([[1.0,0.0]])
    K_shadow = F @ K @ F.T
    Theta_shadow = F @ Theta @ F.T
    rows.append({
        'hidden_capacity_M': M,
        'public_shadow_capacity': float(K_shadow[0,0]),
        'public_shadow_budget': float(Theta_shadow[0,0]),
        'public_shadow_passes': K_shadow[0,0] <= Theta_shadow[0,0] + 1e-12,
        'intrinsic_max_eigen_ratio': max_eig(K),
        'intrinsic_passes': max_eig(K) <= 1 + 1e-12,
    })
shadow_df = pd.DataFrame(rows)
shadow_df.to_csv(OUT/'public_shadow_no_promotion_step46.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.plot(shadow_df['hidden_capacity_M'], shadow_df['intrinsic_max_eigen_ratio'], marker='o', label='intrinsic max capacity')
plt.plot(shadow_df['hidden_capacity_M'], shadow_df['public_shadow_capacity'], marker='o', label='public shadow capacity')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('hidden capacity')
plt.ylabel('reported capacity')
plt.title('Public shadow does not promote to intrinsic membrane')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'public_shadow_no_promotion_step46.png', dpi=180)
plt.close()

# 4. Channel defect allocation monotonicity check.
rows = []
for trial in range(80):
    n = 4
    A = rng.normal(size=(n,n))/np.sqrt(n)
    K = psd(n, 1.0)
    alpha = 1.1
    defects_big = [psd(n, 0.03) for _ in range(7)]
    defects_small = [0.5*D for D in defects_big]
    U_big = alpha*A@K@A.T + sum(defects_big)
    U_small = alpha*A@K@A.T + sum(defects_small)
    rows.append({
        'trial': trial,
        'min_eig_big_minus_small': min_eig(U_big - U_small),
        'trace_big': float(np.trace(U_big)),
        'trace_small': float(np.trace(U_small)),
        'passed': min_eig(U_big-U_small) >= -1e-9,
    })
pd.DataFrame(rows).to_csv(OUT/'channel_defect_allocation_checks_step46.csv', index=False)

# Summary JSON
summary = {
    'composition_random_trials': 100,
    'composition_all_passed': bool(pd.DataFrame(rows).empty)  # overwritten below
}
# Don't rely on rows from channel; read files
comp = pd.read_csv(OUT/'composition_random_checks_step46.csv')
chan = pd.read_csv(OUT/'channel_defect_allocation_checks_step46.csv')
summary = {
    'composition_random_trials': int(len(comp)),
    'composition_all_passed': bool(comp['passed'].all()),
    'composition_min_gap': float(comp['min_eig_composed_minus_K2'].min()),
    'channel_defect_trials': int(len(chan)),
    'channel_defect_all_passed': bool(chan['passed'].all()),
    'channel_defect_min_gap': float(chan['min_eig_big_minus_small'].min()),
    'final_chain_bound': float(chain_df['propagated_bound'].iloc[-1]),
    'final_chain_actual': float(chain_df['actual_K'].iloc[-1]),
    'public_shadow_passes_all': bool(shadow_df['public_shadow_passes'].all()),
    'intrinsic_fails_for_M_gt_1': bool((~shadow_df.loc[shadow_df['hidden_capacity_M']>1,'intrinsic_passes']).all())
}
(OUT/'step46_sanity_summary.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
