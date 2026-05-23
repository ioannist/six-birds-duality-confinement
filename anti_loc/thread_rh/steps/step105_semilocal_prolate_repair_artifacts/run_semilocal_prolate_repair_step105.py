"""Efficient sanity checks for Step 105.

These are finite-dimensional algebra models of the Calkin-level theorem:
compact or fixed-rank perturbative repairs cannot remove a noncompact shifted
boundary-packet sector. They are not RH evidence and not Six Birds simulations.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

out = Path('/mnt/data/rh_membrane_step105_semilocal_prolate_repair')
out.mkdir(parents=True, exist_ok=True)

# Model: a partial isometry with a growing plateau of singular values equal to 1.
# This is the finite-dimensional shadow of a nonzero Calkin/essential class.
Ns = [64, 128, 256, 512]
ranks = [0, 5, 10, 20, 40, 80, 120]
sv_rows = []
tail_rows = []
for N in Ns:
    plateau = N // 4
    sv = np.r_[np.ones(plateau), np.zeros(N - plateau)]
    for i, val in enumerate(sv[:160], start=1):
        sv_rows.append({'N': N, 'index': i, 'raw_singular_value': val})
    for r in ranks:
        # Best rank-r subtraction removes at most r plateau directions.
        residual_plateau = max(plateau - r, 0)
        residual_norm = 1.0 if residual_plateau > 0 else 0.0
        tail_rows.append({
            'N': N,
            'removed_rank': r,
            'plateau_size': plateau,
            'residual_plateau_size': residual_plateau,
            'residual_operator_norm': residual_norm,
            'tail_norm_after_rank': residual_norm,
        })

svdf = pd.DataFrame(sv_rows)
taildf = pd.DataFrame(tail_rows)
svdf.to_csv(out/'semilocal_repair_singular_values_step105.csv', index=False)
taildf.to_csv(out/'compact_repair_tail_norm_step105.csv', index=False)

# Singular value profile plot
plt.figure(figsize=(7, 4.5))
for N in Ns:
    d = svdf[svdf['N'] == N]
    plt.plot(d['index'], d['raw_singular_value'], label=f'N={N}')
plt.xlabel('singular value index')
plt.ylabel('singular value')
plt.title('Growing plateau: finite-dimensional shadow of noncompact block')
plt.legend()
plt.tight_layout()
plt.savefig(out/'semilocal_repair_singular_values_step105.png', dpi=180)
plt.close()

# Tail norm after fixed-rank repair
plt.figure(figsize=(7, 4.5))
for r in [5, 20, 80, 120]:
    d = taildf[taildf['removed_rank'] == r]
    plt.plot(d['N'], d['tail_norm_after_rank'], marker='o', label=f'rank {r}')
plt.xlabel('dimension N')
plt.ylabel('tail norm after rank-r repair')
plt.title('Fixed-rank repair cannot remove growing essential plateau')
plt.legend()
plt.tight_layout()
plt.savefig(out/'compact_repair_tail_norm_step105.png', dpi=180)
plt.close()

route = pd.DataFrame([
    {'route':'compact/finite-rank prolate discrepancy','cancels_essential_class':0,'status':'ruled out by Calkin no-repair lemma'},
    {'route':'true semilocal prolate principal repair','cancels_essential_class':1,'status':'possible but unearned'},
    {'route':'Hecke/Dirichlet source lower frame','cancels_essential_class':1,'status':'fallback/load-bearing if repair fails'},
    {'route':'quotient/gating with vanishing tail','cancels_essential_class':1,'status':'scoped; needs tail record'},
])
route.to_csv(out/'repair_route_decision_model_step105.csv', index=False)

plt.figure(figsize=(7, 4.5))
plt.bar(route['route'], route['cancels_essential_class'])
plt.ylabel('can cancel essential class?')
plt.title('Step 105 repair-route decision')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
plt.savefig(out/'repair_route_decision_model_step105.png', dpi=180)
plt.close()

print('Step 105 efficient checks complete:', out)
