#!/usr/bin/env python3
"""Small algebra checks for Step 47.
These are sanity checks for scalar/matrix recurrences, not Six Birds simulations.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step47_reflexive_ladder')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Contractive recurrence delta_{j+1} <= q delta_j + e_j
rows = []
q = 0.72
delta = 2.0
for j in range(1, 81):
    e = 0.15/(j**1.4)
    delta_next = q*delta + e
    rows.append({'j': j, 'q': q, 'e_j': e, 'delta_j': delta, 'delta_next': delta_next})
    delta = delta_next
pd.DataFrame(rows).to_csv(OUT/'contractive_defect_recurrence_step47.csv', index=False)

plt.figure()
plt.plot([r['j'] for r in rows], [r['delta_j'] for r in rows], marker='o', markersize=2)
plt.xlabel('stage j')
plt.ylabel('scalar violation delta_j')
plt.title('Contractive defect recurrence: asymptotic improvement')
plt.tight_layout()
plt.savefig(OUT/'contractive_defect_recurrence_step47.png', dpi=180)
plt.close()

# 2. Monotone nontermination: delta_j = 1/j
rows = []
for j in range(1, 101):
    rows.append({'j': j, 'delta_j': 1.0/j, 'accepted_exact_budget': False})
pd.DataFrame(rows).to_csv(OUT/'monotone_nontermination_step47.csv', index=False)
plt.figure()
plt.plot([r['j'] for r in rows], [r['delta_j'] for r in rows])
plt.xlabel('stage j')
plt.ylabel('delta_j = 1/j')
plt.title('Monotone improvement without finite completion')
plt.tight_layout()
plt.savefig(OUT/'monotone_nontermination_step47.png', dpi=180)
plt.close()

# 3. Fixed-package saturation under unitary relabeling
rng = np.random.default_rng(47)
n = 5
m = 3
A = rng.normal(size=(n,n)); C = A.T@A + np.eye(n)
L = rng.normal(size=(m,n))
K = L @ np.linalg.inv(C) @ L.T
# random orthogonal relabeling U,V
Q,_ = np.linalg.qr(rng.normal(size=(n,n)))
V,_ = np.linalg.qr(rng.normal(size=(m,m)))
Cp = Q.T @ C @ Q
Lp = V @ L @ Q
Kp = Lp @ np.linalg.inv(Cp) @ Lp.T
err = np.linalg.norm(Kp - V@K@V.T, ord=2)
pd.DataFrame([{'operator_error': err, 'status': 'congruent_currency'}]).to_csv(OUT/'fixed_package_saturation_check_step47.csv', index=False)

# 4. Well-founded completion toy: integer witness count decreases
rows=[]
witnesses=7
stage=0
while witnesses>0:
    rows.append({'stage': stage, 'unresolved_witness_count': witnesses, 'accepted': False})
    witnesses-=1
    stage+=1
rows.append({'stage': stage, 'unresolved_witness_count': witnesses, 'accepted': True})
pd.DataFrame(rows).to_csv(OUT/'well_founded_completion_toy_step47.csv', index=False)
plt.figure()
plt.step([r['stage'] for r in rows], [r['unresolved_witness_count'] for r in rows], where='post')
plt.xlabel('strict repair stage')
plt.ylabel('unresolved witness count')
plt.title('Well-founded finite completion toy')
plt.tight_layout()
plt.savefig(OUT/'well_founded_completion_toy_step47.png', dpi=180)
plt.close()

# 5. Energy product degradation beta product
rows=[]
prod=1.0
for j in range(1,81):
    beta = 1.0 - 1.0/(j+2)  # product tends toward 0 slowly
    prod *= beta
    multiplier = 1/prod
    rows.append({'j': j, 'beta_j': beta, 'beta_product': prod, 'capacity_multiplier': multiplier})
pd.DataFrame(rows).to_csv(OUT/'energy_product_degradation_step47.csv', index=False)
plt.figure()
plt.plot([r['j'] for r in rows], [r['capacity_multiplier'] for r in rows])
plt.xlabel('stage j')
plt.ylabel('capacity multiplier 1/prod beta')
plt.title('Vanishing energy product degrades membrane transfer')
plt.tight_layout()
plt.savefig(OUT/'energy_product_degradation_step47.png', dpi=180)
plt.close()

print('Step 47 checks complete; outputs written to', OUT)
