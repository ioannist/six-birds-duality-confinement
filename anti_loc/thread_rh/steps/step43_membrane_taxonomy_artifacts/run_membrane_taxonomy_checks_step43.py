import csv
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step43_taxonomy')
OUT.mkdir(parents=True, exist_ok=True)

def lammax(M):
    return float(np.linalg.eigvalsh(M).max())

def write_csv(path, rows, fields):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

# Simple failure examples by membrane type.
rows = []
# Intrinsic/public shadow: shadow sees first coordinate only.
K_full = np.diag([0.5, 2.0])
Theta_full = np.eye(2)
F = np.array([[1.0, 0.0]])
K_shadow = F @ K_full @ F.T
Theta_shadow = F @ Theta_full @ F.T
rows.append({
    'case': 'public_shadow_overread',
    'full_lambda_max_theta_norm': lammax(K_full),
    'shadow_lambda_max_theta_norm': lammax(K_shadow),
    'full_passes': lammax(K_full) <= 1 + 1e-12,
    'shadow_passes': lammax(K_shadow) <= 1 + 1e-12,
    'interpretation': 'public shadow passes but hidden response direction fails'
})
# Sectioned cross recombination.
K_section = np.array([[1.0, 1.0], [1.0, 1.0]])
rows.append({
    'case': 'section_cross_recombination',
    'full_lambda_max_theta_norm': lammax(K_section),
    'shadow_lambda_max_theta_norm': 1.0,
    'full_passes': lammax(K_section) <= 1 + 1e-12,
    'shadow_passes': True,
    'interpretation': 'each section diagonal passes but cross-section all-ones recombination fails'
})
# Protocol duplicate.
K_protocol = K_section.copy()
rows.append({
    'case': 'protocol_duplicate_route',
    'full_lambda_max_theta_norm': lammax(K_protocol),
    'shadow_lambda_max_theta_norm': 1.0,
    'full_passes': lammax(K_protocol) <= 1 + 1e-12,
    'shadow_passes': True,
    'interpretation': 'each protocol passes alone but stacked protocol matrix fails'
})
# Bundle unbounded fiber growth.
N = 20
max_fiber = N
rows.append({
    'case': 'bundle_unbounded_fiber',
    'full_lambda_max_theta_norm': float(max_fiber),
    'shadow_lambda_max_theta_norm': 1.0,
    'full_passes': max_fiber <= 1 + 1e-12,
    'shadow_passes': True,
    'interpretation': 'each named low fiber can pass but no uniform bundle budget exists as fibers grow'
})

write_csv(OUT/'taxonomy_counterchecks_step43.csv', rows, ['case','full_lambda_max_theta_norm','shadow_lambda_max_theta_norm','full_passes','shadow_passes','interpretation'])

# Bundle growth sequence.
seq_rows = []
for n in range(1, 41):
    seq_rows.append({'n_fibers': n, 'max_fiber_budget': n, 'uniform_budget_required': n})
write_csv(OUT/'bundle_growth_countermodel_step43.csv', seq_rows, ['n_fibers','max_fiber_budget','uniform_budget_required'])

# Plot failure eigenvalues.
cases = [r['case'] for r in rows]
vals_full = [r['full_lambda_max_theta_norm'] for r in rows]
vals_shadow = [r['shadow_lambda_max_theta_norm'] for r in rows]
x = np.arange(len(cases))
width = 0.35
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.bar(x - width/2, vals_shadow, width, label='visible/local check')
ax.bar(x + width/2, vals_full, width, label='full membrane check')
ax.axhline(1.0, linestyle='--', linewidth=1, label='budget threshold')
ax.set_xticks(x)
ax.set_xticklabels(cases, rotation=30, ha='right')
ax.set_ylabel('largest normalized eigenvalue')
ax.set_title('Membrane taxonomy: local/shadow checks vs full checks')
ax.legend()
fig.tight_layout()
fig.savefig(OUT/'membrane_taxonomy_failure_eigenvalues_step43.png', dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.2, 4.5))
ax.plot([r['n_fibers'] for r in seq_rows], [r['uniform_budget_required'] for r in seq_rows], marker='o', markersize=3)
ax.axhline(1.0, linestyle='--', linewidth=1)
ax.set_xlabel('number of fibers')
ax.set_ylabel('uniform budget required')
ax.set_title('Bundle/fiber failure: no global membrane without uniform budget')
fig.tight_layout()
fig.savefig(OUT/'bundle_growth_countermodel_step43.png', dpi=180)
plt.close(fig)

# Exact transfer sanity check.
rng = np.random.default_rng(43)
transfer_rows = []
for i in range(20):
    n = 5
    m = 3
    C = rng.standard_normal((n, n))
    C = C.T @ C + np.eye(n)
    L = rng.standard_normal((m, n))
    K = L @ np.linalg.inv(C) @ L.T
    A = rng.standard_normal((2, m))
    K_target = A @ K @ A.T
    budget = A @ (K + 0.2*np.eye(m)) @ A.T
    min_slack = float(np.linalg.eigvalsh(budget - K_target).min())
    transfer_rows.append({'trial': i, 'min_slack': min_slack, 'passes': min_slack >= -1e-9})
write_csv(OUT/'exact_transfer_sanity_step43.csv', transfer_rows, ['trial','min_slack','passes'])

print(json.dumps({'status':'ok','out':str(OUT)}, indent=2))
