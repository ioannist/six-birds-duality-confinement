"""Small algebraic sanity checks for Step 23.

This is not a Six Birds substrate simulation. It only illustrates the finite
matrix theorem: diagonal scalar capacities do not control recombinations.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step23_probe_family')
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for m in range(1, 33):
    one = np.ones((m, 1))
    K = one @ one.T  # realized by H=C, C=1, L u = u * 1
    diag_max = float(np.diag(K).max())
    eigvals = np.linalg.eigvalsh(K)
    lambda_max = float(eigvals[-1])
    y = np.ones(m) / np.sqrt(m)
    recomb_cap = float(y @ K @ y)
    rows.append({
        'm': m,
        'max_scalar_diagonal_capacity': diag_max,
        'largest_family_capacity_eigenvalue': lambda_max,
        'normalized_all_ones_recombination_capacity': recomb_cap,
        'family_bound_I_passes': bool(lambda_max <= 1 + 1e-12),
        'diagonal_bound_I_passes': bool(diag_max <= 1 + 1e-12),
    })

csv_path = OUT / 'probe_family_recombination_countermodel_step23.csv'
with csv_path.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

plt.figure(figsize=(7, 4.5))
plt.plot([r['m'] for r in rows], [r['max_scalar_diagonal_capacity'] for r in rows], marker='o', label='max scalar diagonal capacity')
plt.plot([r['m'] for r in rows], [r['largest_family_capacity_eigenvalue'] for r in rows], marker='o', label='family recombination capacity')
plt.xlabel('number of declared probes m')
plt.ylabel('capacity')
plt.title('Diagonal scalar bounds miss recombination needles')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'recombination_capacity_growth_step23.png', dpi=180)
plt.close()

# A second example: correlated two-probe family K_rho.
rows2 = []
for rho in np.linspace(0, 0.99, 100):
    K = np.array([[1.0, rho], [rho, 1.0]])
    rows2.append({
        'rho': float(rho),
        'diag_capacity_1': 1.0,
        'diag_capacity_2': 1.0,
        'largest_eigenvalue': float(np.linalg.eigvalsh(K)[-1]),
        'sum_recombination_capacity': float(np.array([1, 1]) / np.sqrt(2) @ K @ (np.array([1, 1]) / np.sqrt(2))),
        'difference_recombination_capacity': float(np.array([1, -1]) / np.sqrt(2) @ K @ (np.array([1, -1]) / np.sqrt(2))),
    })

csv_path2 = OUT / 'two_probe_correlation_countermodel_step23.csv'
with csv_path2.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows2[0].keys()))
    writer.writeheader()
    writer.writerows(rows2)

plt.figure(figsize=(7, 4.5))
plt.plot([r['rho'] for r in rows2], [r['sum_recombination_capacity'] for r in rows2], label='sum recombination')
plt.plot([r['rho'] for r in rows2], [r['difference_recombination_capacity'] for r in rows2], label='difference recombination')
plt.plot([r['rho'] for r in rows2], [1 for _ in rows2], linestyle='--', label='scalar diagonal bound')
plt.xlabel('correlation rho')
plt.ylabel('capacity')
plt.title('Off-diagonal compliance controls recombination')
plt.legend()
plt.tight_layout()
plt.savefig(OUT / 'two_probe_recombination_step23.png', dpi=180)
plt.close()

print(f'wrote {csv_path}')
print(f'wrote {csv_path2}')
