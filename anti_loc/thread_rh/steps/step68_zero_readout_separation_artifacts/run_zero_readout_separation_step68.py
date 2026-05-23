#!/usr/bin/env python3
"""Small algebra checks for Step 68.
These are not Six Birds simulations; they only illustrate zero-readout separation, fixed-ledger squeeze,
exhaustive tail promotion, and nonseparating readout failure.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step68_zero_readout')
OUT.mkdir(parents=True, exist_ok=True)

# 1. RH centered readout: zeros with displacements x_i. A_Z = sum w x_i^2.
rng = np.random.default_rng(68)
xs = np.array([0.0, 0.10, -0.25, 0.03, 0.0])
weights = np.array([1.0, 2.0, 1.5, 0.7, 3.0])
A_scalar = float(np.sum(weights * xs**2))
finite_rows = []
for i, (x,w) in enumerate(zip(xs, weights)):
    finite_rows.append({
        'zero_index': i,
        'centered_real_displacement_x': x,
        'weight': w,
        'contribution_w_x2': w*x*x,
        'on_fixed_locus': abs(x) < 1e-14
    })
pd.DataFrame(finite_rows).to_csv(OUT/'rh_centered_readout_finite_ledger_step68.csv', index=False)

# 2. Fixed squeeze: A fixed positive number a <= 1/n for all n impossible unless a=0.
# Use a = 0 and a = 1e-3 diagnostic.
ns = np.arange(1, 1001)
B = 1.0/ns
rows = []
for a in [0.0, 1e-3, 1e-2]:
    last_valid = int(np.max(ns[B >= a])) if np.any(B >= a) else 0
    rows.append({'fixed_A': a, 'valid_for_all_1_to_1000': bool(np.all(a <= B)), 'last_n_with_A_le_1/n': last_valid})
pd.DataFrame(rows).to_csv(OUT/'fixed_squeeze_diagnostic_step68.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(ns, B, label='budget B_n=1/n')
plt.axhline(1e-3, linestyle='--', label='fixed A=1e-3')
plt.axhline(0.0, linestyle='-', label='fixed A=0')
plt.xlabel('n')
plt.ylabel('trace budget')
plt.title('Fixed-ledger squeeze: positive A cannot stay below B_n -> 0')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'fixed_squeeze_step68.png', dpi=160)
plt.close()

# 3. Exhaustive ledger: finite-window budget plus tail.
ns2 = np.arange(1, 501)
B_good = 1/(ns2**2)
T_good = 1/(ns2**2)
B_bad = 1/(ns2**2)
T_bad = np.full_like(ns2, 0.05, dtype=float)
ex_rows=[]
for n, bg, tg, bb, tb in zip(ns2, B_good, T_good, B_bad, T_bad):
    ex_rows.append({'n': int(n), 'good_total': bg+tg, 'bad_total': bb+tb, 'B_good': bg, 'T_good': tg, 'B_bad': bb, 'T_bad': tb})
pd.DataFrame(ex_rows).to_csv(OUT/'exhaustive_tail_diagnostic_step68.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(ns2, B_good+T_good, label='exhaustive total B_n+T_n -> 0')
plt.loglog(ns2, B_bad+T_bad, label='failed tail: B_n -> 0 but T_n not -> 0')
plt.xlabel('n')
plt.ylabel('trace bound')
plt.title('Exhaustive finite windows require vanishing tail')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'exhaustive_tail_step68.png', dpi=160)
plt.close()

# 4. Nonseparating readout: psi_- ignores x for one direction; zero ledger can be nonzero off fixed but A=0.
# In RH centered coordinates (x,t), bad readout psi_-=0 or psi_-=x for only visible subset.
M_vals = np.logspace(0, 5, 80)
nonsep_rows=[]
for M in M_vals:
    # off-fixed zero with x=M, bad psi=0 -> A=0 despite off-fixed displacement.
    nonsep_rows.append({'off_fixed_displacement': M, 'bad_readout_A': 0.0, 'good_readout_A': M*M})
pd.DataFrame(nonsep_rows).to_csv(OUT/'nonseparating_readout_countermodel_step68.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(M_vals, [r['good_readout_A'] for r in nonsep_rows], label='separating readout A=x^2')
plt.loglog(M_vals, [1e-30]*len(M_vals), label='nonseparating readout A=0')
plt.xlabel('off-fixed displacement |x|')
plt.ylabel('zero-side ledger contribution')
plt.title('Nonseparating readout can miss arbitrary off-fixed displacement')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'nonseparating_readout_countermodel_step68.png', dpi=160)
plt.close()

# 5. Optimized obstruction budget: (sqrt(a)+sqrt(b))^2
n3 = np.arange(1, 501)
a = 1/n3**2
b = 1/n3**3
opt = (np.sqrt(a)+np.sqrt(b))**2
pd.DataFrame({'n':n3, 'a':a, 'b':b, 'optimized_trace_budget':opt}).to_csv(OUT/'optimized_obstruction_budget_step68.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.loglog(n3, a, label='a_n')
plt.loglog(n3, b, label='b_n')
plt.loglog(n3, opt, label='(sqrt(a_n)+sqrt(b_n))^2')
plt.xlabel('n')
plt.ylabel('trace budget')
plt.title('Optimized root-composite obstruction budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'optimized_obstruction_budget_step68.png', dpi=160)
plt.close()

print('Step 68 checks completed. A_scalar=', A_scalar)
