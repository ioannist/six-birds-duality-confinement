import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step151_direct_residual_exclusion')
OUT.mkdir(parents=True, exist_ok=True)

# Toy finite model for the adjoint criterion.
# H = C^n, P = Sonin/prolate projection, tau = unitary shift, J^*Y are evaluator samples.
rng = np.random.default_rng(151)
n = 80
rank = 34
# Random orthogonal projection P.
Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
P = Q[:, :rank] @ Q[:, :rank].T
I = np.eye(n)

# Unit cyclic shift as tau_ell.
shift = 7
Tau = np.roll(np.eye(n), shift, axis=0)
Tau_minus = Tau.T

# Evaluator dictionary with decreasing singular-like envelope.
m = 30
Y = rng.normal(size=(n, m))
Y = Y / np.linalg.norm(Y, axis=0, keepdims=True)
# Add a co-Poisson-factored control: evaluators in kernel of adjoint block.
# Generic residual vectors:
Adj = (I - P) @ Tau_minus @ P @ Y
residual_norms = np.linalg.norm(Adj, axis=0)

# Tuned control: force Y into orthogonal complement of P Tau (I-P) range approximately.
B = P @ Tau @ (I - P)
U, s, Vt = np.linalg.svd(B.T, full_matrices=True)
# Null basis of B^T (vectors annihilated by B^*) lives in the right singular vectors.
null_dim = max(1, n - np.linalg.matrix_rank(B.T, tol=1e-10))
V = Vt.T
Y_control = V[:, -min(m, null_dim):]
if Y_control.shape[1] < m:
    # pad with projected random null-ish vectors
    pad = rng.normal(size=(n, m - Y_control.shape[1]))
    A = B.T
    pad = pad - A.T @ np.linalg.pinv(A @ A.T) @ (A @ pad)
    pad = pad / np.maximum(np.linalg.norm(pad, axis=0, keepdims=True), 1e-12)
    Y_control = np.column_stack([Y_control, pad])
Adj_control = (I - P) @ Tau_minus @ P @ Y_control
control_norms = np.linalg.norm(Adj_control, axis=0)

# Xi spectra for generic and controlled dictionaries
Xi_generic = Adj @ Adj.T
Xi_control = Adj_control @ Adj_control.T
sg = np.linalg.eigvalsh(Xi_generic)[::-1]
sc = np.linalg.eigvalsh(Xi_control)[::-1]

# Scenario curves: how residual can behave under three mechanisms.
N = np.arange(1, 61)
exact = np.zeros_like(N, dtype=float)
controlled = np.exp(-N/12)
positive_floor = 0.18 + 0.35*np.exp(-N/10)
no_exclusion = 0.55 + 0.05*np.sin(N/5)
scenario_df = pd.DataFrame({
    'N': N,
    'exact_exclusion': exact,
    'controlled_budget': controlled,
    'positive_floor_residual': positive_floor,
    'no_exclusion': no_exclusion,
})
scenario_df.to_csv(OUT/'direct_residual_scenarios_step151.csv', index=False)

# Save evaluator residual norms.
norm_df = pd.DataFrame({
    'index': np.arange(m),
    'generic_adjoint_evaluator_norm': residual_norms,
    'controlled_adjoint_evaluator_norm': control_norms[:m],
})
norm_df.to_csv(OUT/'adjoint_evaluator_norms_step151.csv', index=False)

spec_df = pd.DataFrame({
    'index': np.arange(n),
    'Xi_BC_generic_eigenvalue': sg,
    'Xi_BC_controlled_eigenvalue': sc,
})
spec_df.to_csv(OUT/'xi_bc_spectrum_toy_step151.csv', index=False)

# Plot 1: adjoint evaluator norms
plt.figure(figsize=(8, 5))
plt.semilogy(norm_df['index'], norm_df['generic_adjoint_evaluator_norm'] + 1e-16, marker='o', label='generic transported evaluators')
plt.semilogy(norm_df['index'], norm_df['controlled_adjoint_evaluator_norm'] + 1e-16, marker='s', label='control: annihilating subspace')
plt.xlabel('zero-evaluator sample index')
plt.ylabel(r'$\|(I-P)\tau_{-\ell}PJ_a^*Y\|$')
plt.title('Step 151 adjoint zero-evaluator test (toy)')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'adjoint_zero_evaluator_test_step151.png', dpi=200)
plt.close()

# Plot 2: Xi spectrum
plt.figure(figsize=(8, 5))
plt.semilogy(np.arange(1, n+1), sg + 1e-16, label=r'generic $\Xi^{BC}$')
plt.semilogy(np.arange(1, n+1), sc + 1e-16, label=r'controlled $\Xi^{BC}$')
plt.xlabel('eigenvalue index')
plt.ylabel('eigenvalue')
plt.title(r'Step 151 $\Xi^{BC}$ spectrum sanity check')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'xi_bc_spectrum_step151.png', dpi=200)
plt.close()

# Plot 3: scenario trichotomy
plt.figure(figsize=(8, 5))
for col in ['exact_exclusion', 'controlled_budget', 'positive_floor_residual', 'no_exclusion']:
    plt.plot(N, scenario_df[col], label=col.replace('_', ' '))
plt.axhline(1.0, linestyle='--', linewidth=1, label='budget failure threshold')
plt.xlabel('finite residual window N')
plt.ylabel(r'residual level $\delta_N$')
plt.title('Step 151 direct exclusion trichotomy')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'direct_exclusion_trichotomy_step151.png', dpi=200)
plt.close()

# Plot 4: route pivot map
routes = ['trace squeeze', 'source budget', 'direct exclusion', 'Xi budget', 'scoped nonclaim']
scores = [0.2, 0.1, 0.65, 0.45, 0.35]
plt.figure(figsize=(8, 4.8))
plt.bar(routes, scores)
plt.xticks(rotation=25, ha='right')
plt.ylabel('proof-producing viability score')
plt.title('Step 151 route pivot status')
plt.tight_layout()
plt.savefig(OUT/'route_pivot_status_step151.png', dpi=200)
plt.close()

# Checks
checks = {
    'projection_idempotence_error': float(np.linalg.norm(P@P - P)),
    'projection_selfadjoint_error': float(np.linalg.norm(P.T - P)),
    'tau_unitary_error': float(np.linalg.norm(Tau.T@Tau - I)),
    'generic_max_residual_norm': float(residual_norms.max()),
    'controlled_max_residual_norm': float(control_norms.max()),
    'xi_generic_trace': float(np.trace(Xi_generic)),
    'xi_control_trace': float(np.trace(Xi_control)),
}
(OUT/'step151_check_results.json').write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
