"""Step 100 sanity checks for semilocal carrier instantiation.

These are algebra/diagnostic plots only. They are not RH evidence.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step100_semilocal_instantiation')
OUT.mkdir(parents=True, exist_ok=True)

# Semilocal finite-place measure ratio for a finite set of added primes.
def lp_abs_sq(p, xi):
    return 1.0 / (1.0 + 1.0/p - 2.0 / math.sqrt(p) * np.cos(xi * math.log(p)))

xis = np.linspace(-30, 30, 1201)
primes = [2, 3, 5]
ratios = {str(p): lp_abs_sq(p, xis) for p in primes}
prod_ratio = np.ones_like(xis)
for p in primes:
    prod_ratio *= ratios[str(p)]

with open(OUT / 'semilocal_measure_ratio_step100.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['xi'] + [f'p_{p}_ratio' for p in primes] + ['product_ratio'])
    for i, xi in enumerate(xis):
        w.writerow([xi] + [ratios[str(p)][i] for p in primes] + [prod_ratio[i]])

plt.figure(figsize=(7, 4))
plt.plot(xis, prod_ratio)
plt.xlabel(r'$\xi$')
plt.ylabel('finite-place measure ratio')
plt.title('Semilocal measure deformation by primes 2,3,5')
plt.tight_layout()
plt.savefig(OUT / 'semilocal_measure_ratio_step100.png', dpi=160)
plt.close()

# Tail model for spectral windows. Toy density to demonstrate gate behavior.
T_values = np.linspace(1, 80, 160)
# Tail for density (1+xi^2)^-2 outside [-T,T], proportional to 1/T^3 asymptotically.
tail = []
for T in T_values:
    # numerical integration on a large grid for illustration
    x = np.linspace(T, 500, 4000)
    val = 2 * np.trapz((1 + x*x)**-2, x)
    tail.append(val)
tail = np.array(tail)

with open(OUT / 'spectral_tail_model_step100.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['T', 'tail_trace_model'])
    for T, val in zip(T_values, tail):
        w.writerow([T, val])

plt.figure(figsize=(7, 4))
plt.loglog(T_values, tail)
plt.xlabel('spectral window T')
plt.ylabel('toy tail trace')
plt.title('Spectral-window tail model')
plt.tight_layout()
plt.savefig(OUT / 'spectral_tail_model_step100.png', dpi=160)
plt.close()

# Abstract lower-frame promotion model: budget <= 1/Lambda + tail.
n = np.arange(1, 101)
Lambda = n.astype(float)
vanishing_tail = 1.0 / (n.astype(float) ** 2)
nonvanishing_tail = 0.05 + 1.0 / (n.astype(float) ** 2)
budget_good = 1.0 / Lambda + vanishing_tail
budget_bad = 1.0 / Lambda + nonvanishing_tail

with open(OUT / 'lower_frame_tail_budget_step100.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['n', 'Lambda', 'vanishing_tail', 'nonvanishing_tail', 'budget_with_vanishing_tail', 'budget_with_nonvanishing_tail'])
    for row in zip(n, Lambda, vanishing_tail, nonvanishing_tail, budget_good, budget_bad):
        w.writerow(row)

plt.figure(figsize=(7, 4))
plt.plot(n, budget_good, label='vanishing tail')
plt.plot(n, budget_bad, label='nonvanishing tail')
plt.xlabel('refinement n')
plt.ylabel('budget model')
plt.title('Lower-frame collapse requires vanishing tail')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'lower_frame_tail_budget_step100.png', dpi=160)
plt.close()

# Character-native status diagnostic as JSON.
status = {
    'pure_semilocal_KS_invariant': {
        'hosts_Delta_S': True,
        'hosts_full_character_source_frame': False,
        'reason': 'K_S-invariant reduction suppresses nontrivial compact-character modes'
    },
    'augmented_semilocal': {
        'hosts_Delta_S': True,
        'hosts_full_character_source_frame': 'possible with K_S Fourier modes and Plancherel record'
    },
    'hecke_idele_carrier': {
        'hosts_Delta_S': 'via descent/extension',
        'hosts_full_character_source_frame': 'natural but requires descent to zeta ledger'
    }
}
with open(OUT / 'character_native_status_step100.json', 'w') as f:
    json.dump(status, f, indent=2)

print('Step 100 sanity artifacts written to', OUT)
