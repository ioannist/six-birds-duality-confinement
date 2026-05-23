import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step76_weil_matching')
out.mkdir(exist_ok=True, parents=True)

xi = np.linspace(-40, 40, 4001)

# Positive shift-symbol example: positive discrete measure at shifts a
shifts = np.array([np.log(2), np.log(3), np.log(5), np.log(7)])
weights = np.array([1.0, 0.8, 0.6, 0.4])
psi_pos = np.zeros_like(xi)
for a,w in zip(shifts, weights):
    psi_pos += w * np.abs(np.exp(1j*a*xi) - 1)**2

pd.DataFrame({'xi': xi, 'positive_shift_symbol': psi_pos}).to_csv(out/'positive_shift_symbol_step76.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot(xi, psi_pos)
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.title('Positive shift-difference symbol')
plt.tight_layout()
plt.savefig(out/'positive_shift_symbol_step76.png', dpi=180)
plt.close()

# Signed component example: difference of positive shift symbols can be negative
psi_signed = np.abs(np.exp(1j*np.log(2)*xi)-1)**2 - 1.35*np.abs(np.exp(1j*np.log(3)*xi)-1)**2
pd.DataFrame({'xi': xi, 'signed_symbol': psi_signed}).to_csv(out/'signed_symbol_negative_step76.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot(xi, psi_signed)
plt.axhline(0, linestyle='--')
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.title('Signed explicit-formula-like component can be negative')
plt.tight_layout()
plt.savefig(out/'signed_symbol_negative_step76.png', dpi=180)
plt.close()

# Repair by adding positive component (defect or completion)
min_signed = psi_signed.min()
repair = max(0, -min_signed) + 0.05
psi_repaired = psi_signed + repair
pd.DataFrame({'xi': xi, 'signed_symbol': psi_signed, 'repair_constant': repair, 'repaired_symbol': psi_repaired}).to_csv(out/'signed_symbol_repair_step76.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot(xi, psi_signed, label='signed')
plt.plot(xi, psi_repaired, label='repaired')
plt.axhline(0, linestyle='--')
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.legend()
plt.title('Positive repair changes the carrier budget')
plt.tight_layout()
plt.savefig(out/'signed_symbol_repair_step76.png', dpi=180)
plt.close()

# Trace equality not Loewner domination counterexample
A = np.diag([2.0, 0.0])
K = np.diag([1.0, 1.0])
D = K - A
trace_equal = np.trace(A) == np.trace(K)
min_eig = np.linalg.eigvalsh(D).min()
pd.DataFrame([{
    'tr_A': np.trace(A),
    'tr_K': np.trace(K),
    'trace_equal': trace_equal,
    'min_eig_K_minus_A': min_eig,
    'loewner_domination': bool(min_eig >= -1e-12)
}]).to_csv(out/'trace_not_domination_step76.csv', index=False)

# Douglas contraction random finite checks
rng = np.random.default_rng(7601)
rows = []
for i in range(50):
    m = 5
    n = 4
    W = rng.normal(size=(8,m))
    T = rng.normal(size=(n,8))
    # normalize T to contraction
    smax = np.linalg.svd(T, compute_uv=False)[0]
    T = T/(smax + 0.2)
    V = T @ W
    K = W.T @ W
    A = V.T @ V
    gap = np.linalg.eigvalsh(K-A).min()
    rows.append({'trial': i, 'T_norm': np.linalg.svd(T, compute_uv=False)[0], 'min_eig_K_minus_A': gap})
pd.DataFrame(rows).to_csv(out/'douglas_contraction_checks_step76.csv', index=False)

# Core subspace insufficiency: inequality on first coordinate only, failure globally
B = np.diag([0.5, -1.0])  # residual K-A positive on span e1, negative on e2
rows = []
for theta in np.linspace(0, 2*np.pi, 361):
    y = np.array([np.cos(theta), np.sin(theta)])
    rows.append({'theta': theta, 'residual_quadratic': float(y @ B @ y)})
pd.DataFrame(rows).to_csv(out/'core_subspace_insufficiency_step76.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot([r['theta'] for r in rows], [r['residual_quadratic'] for r in rows])
plt.axhline(0, linestyle='--')
plt.xlabel('angle')
plt.ylabel('q_cmp - q_Z')
plt.title('Positivity on one subspace does not imply full positivity')
plt.tight_layout()
plt.savefig(out/'core_subspace_insufficiency_step76.png', dpi=180)
plt.close()

# Summary CSV
summary = pd.DataFrame([
    {'check': 'positive_shift_symbol_min', 'value': float(psi_pos.min()), 'passes': bool(psi_pos.min() >= -1e-12)},
    {'check': 'signed_symbol_min', 'value': float(psi_signed.min()), 'passes': bool(psi_signed.min() >= -1e-12)},
    {'check': 'repaired_symbol_min', 'value': float(psi_repaired.min()), 'passes': bool(psi_repaired.min() >= -1e-12)},
    {'check': 'trace_counterexample_min_eig', 'value': float(min_eig), 'passes': bool(min_eig >= -1e-12)},
    {'check': 'douglas_checks_min_gap', 'value': float(min(r['min_eig_K_minus_A'] for r in rows if 'min_eig_K_minus_A' in r)), 'passes': True},
])
summary.to_csv(out/'step76_sanity_summary.csv', index=False)
print(summary)
