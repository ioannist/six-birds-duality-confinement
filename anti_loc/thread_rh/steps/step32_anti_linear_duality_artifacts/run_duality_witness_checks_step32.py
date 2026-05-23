import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step32_duality')
OUT.mkdir(parents=True, exist_ok=True)

N = 12
weights = np.geomspace(1.0, 0.05, N)
eps_values = np.geomspace(2.0, 1e-4, 60)
rows = []
for eps in eps_values:
    violations = weights > eps
    max_violation = np.max(weights - eps)
    rows.append({
        'epsilon_budget': eps,
        'trace_budget': N * eps,
        'max_weight': float(weights.max()),
        'num_orbits_with_weight_above_budget': int(np.sum(violations)),
        'max_additive_violation': float(max_violation),
        'total_weight': float(weights.sum()),
        'leakage_bound_trace': float(N * eps)
    })

df = pd.DataFrame(rows)
df.to_csv(OUT/'finite_orbit_confinement_step32.csv', index=False)

rows2 = []
for n in range(1, 101):
    eps = 1.0/(n*n)
    trace = N*eps
    rows2.append({
        'n': n,
        'epsilon': eps,
        'trace_budget': trace,
        'max_number_unit_witnesses_allowed': np.floor(trace)
    })
pd.DataFrame(rows2).to_csv(OUT/'budget_tightening_confinement_step32.csv', index=False)

K_pair = np.array([[1.0, 0.0],[0.0,1.0]])
y_minus = np.array([1.0, -1.0]) / np.sqrt(2)
y_plus = np.array([1.0, 1.0]) / np.sqrt(2)
rows3 = []
for theta_minus in [1.0, 0.5, 0.1, 0.01, 0.0]:
    Pp = np.outer(y_plus, y_plus)
    Pm = np.outer(y_minus, y_minus)
    Theta = Pp + theta_minus*Pm
    val_minus_K = y_minus @ K_pair @ y_minus
    val_minus_Theta = y_minus @ Theta @ y_minus
    rows3.append({
        'theta_minus': theta_minus,
        'anti_invariant_capacity': val_minus_K,
        'anti_invariant_budget': val_minus_Theta,
        'violates': bool(val_minus_K > val_minus_Theta + 1e-12)
    })
pd.DataFrame(rows3).to_csv(OUT/'single_pair_anti_invariant_budget_step32.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(df['epsilon_budget'], df['trace_budget'], label='trace anti-invariant budget')
plt.axhline(weights.sum(), linestyle='--', label='total off-fixed witness weight')
plt.gca().invert_xaxis()
plt.xlabel('uniform anti-invariant budget epsilon')
plt.ylabel('weight / budget')
plt.title('Vanishing anti-invariant budget forces off-fixed leakage to zero')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'anti_invariant_budget_confinement_step32.png', dpi=200)
plt.close()

plt.figure(figsize=(7,4.5))
plt.semilogx(df['epsilon_budget'], df['num_orbits_with_weight_above_budget'])
plt.gca().invert_xaxis()
plt.xlabel('uniform anti-invariant budget epsilon')
plt.ylabel('orbits whose witness exceeds budget')
plt.title('Off-fixed witnesses become impossible as anti-invariant budget tightens')
plt.tight_layout()
plt.savefig(OUT/'off_fixed_witness_violations_step32.png', dpi=200)
plt.close()

print('wrote step32 finite checks')
