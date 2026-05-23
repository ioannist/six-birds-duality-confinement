import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step153_pulled_evaluator_kernel')
OUT.mkdir(parents=True, exist_ok=True)

np.random.seed(153)

# Finite toy Sonin/prolate model.
# H_N = C^N, P_T = time-window projection, P_F = low-frequency projection.
# P = projection onto ker P_T ∩ ker P_F.
N = 256
x = np.arange(N)

# Unitary DFT
F = np.fft.fft(np.eye(N)) / np.sqrt(N)

T_width = 48
freq_width = 48
PT = np.zeros((N, N), dtype=complex)
PT[:T_width, :T_width] = np.eye(T_width)
PF_diag = np.zeros(N)
# low frequencies around zero in FFT ordering
low_idx = list(range(freq_width//2)) + list(range(N - freq_width//2, N))
PF_freq = np.diag([1 if i in low_idx else 0 for i in range(N)])
PF = F.conj().T @ PF_freq @ F

# Constraints matrix for ker PT and ker PF. Projection onto nullspace via SVD.
C = np.vstack([PT, PF])
U, svals, Vh = np.linalg.svd(C, full_matrices=True)
rank = np.sum(svals > 1e-10)
Q = Vh.conj().T[:, rank:]
P = Q @ Q.conj().T
I = np.eye(N, dtype=complex)

# Build toy pulled evaluator family: projected ambient Hardy-like kernels.
# Use log-frequency style kernels on the circle and project by P.
gammas = np.linspace(-2.5, 2.5, 11)
width = 0.10
centers = np.linspace(70, 185, len(gammas))
eta_cols = []
profiles = []
for j, (gamma, c) in enumerate(zip(gammas, centers)):
    # Gaussian packet with oscillatory phase; mimics a pulled evaluation kernel.
    v = np.exp(-0.5*((x-c)/(width*N))**2) * np.exp(1j*gamma*x/N*2*np.pi)
    v = v / np.linalg.norm(v)
    eta = P @ v
    if np.linalg.norm(eta) > 1e-12:
        eta = eta / np.linalg.norm(eta)
    eta_cols.append(eta)
    profiles.append(pd.DataFrame({
        'index': x,
        'gamma': gamma,
        'abs_eta': np.abs(eta),
        'real_eta': np.real(eta),
        'imag_eta': np.imag(eta),
    }))
E = np.column_stack(eta_cols)
profiles_df = pd.concat(profiles, ignore_index=True)
profiles_df.to_csv(OUT/'pulled_evaluator_kernel_profiles_step153.csv', index=False)

# Shift operator T_m on discrete circle (toy for log shift).
def shift_matrix(m):
    return np.roll(np.eye(N, dtype=complex), shift=m, axis=0)

# residual by shift for evaluator family
rows = []
for m in range(0, 33):
    Tm = shift_matrix(-m)
    B = (I-P) @ Tm @ P
    R = B @ E
    norms = np.linalg.norm(R, axis=0)
    rows.append({
        'shift': m,
        'mean_residual_norm': float(np.mean(norms)),
        'max_residual_norm': float(np.max(norms)),
        'min_residual_norm': float(np.min(norms)),
        'fro_residual_on_family': float(np.linalg.norm(R, 'fro')),
    })
res_df = pd.DataFrame(rows)
res_df.to_csv(OUT/'adjoint_transport_residual_sweep_step153.csv', index=False)

# singular values of commutator/offdiagonal block for one shift
m0 = 7
B0 = (I-P) @ shift_matrix(-m0) @ P
sv = np.linalg.svd(B0, compute_uv=False)
sv_df = pd.DataFrame({'rank_index': np.arange(1, len(sv)+1), 'singular_value': sv})
sv_df.to_csv(OUT/'commutator_block_singular_values_step153.csv', index=False)

# Xi^BC toy spectrum on the evaluator family: E^* B^* B E
Xi = E.conj().T @ B0.conj().T @ B0 @ E
Xi = (Xi + Xi.conj().T)/2
xi_eigs = np.linalg.eigvalsh(Xi)
xi_df = pd.DataFrame({'eigen_index': np.arange(1, len(xi_eigs)+1), 'xi_eigenvalue': xi_eigs})
xi_df.to_csv(OUT/'xi_bc_toy_spectrum_step153.csv', index=False)

# commutator identity check: (I-P)TP eta vs (I-P)[T,P] eta if eta in range P
checks = []
for m in range(1, 11):
    Tm = shift_matrix(-m)
    for j in range(E.shape[1]):
        eta = E[:, j]
        lhs = (I-P) @ Tm @ P @ eta
        rhs = (I-P) @ (Tm @ P - P @ Tm) @ eta
        checks.append({
            'shift': m,
            'evaluator_index': j,
            'identity_error': float(np.linalg.norm(lhs-rhs)),
            'lhs_norm': float(np.linalg.norm(lhs)),
        })
check_df = pd.DataFrame(checks)
check_df.to_csv(OUT/'commutator_identity_checks_step153.csv', index=False)

# Plots
plt.figure(figsize=(7,4.5))
plt.plot(res_df['shift'], res_df['mean_residual_norm'], marker='o', label='mean')
plt.plot(res_df['shift'], res_df['max_residual_norm'], marker='s', label='max')
plt.xlabel('discrete log-shift')
plt.ylabel('residual norm')
plt.title('Pulled evaluator commutator residual sweep')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'adjoint_transport_residual_sweep_step153.png', dpi=200)
plt.close()

plt.figure(figsize=(7,4.5))
plt.semilogy(sv_df['rank_index'][:80], sv_df['singular_value'][:80], marker='o')
plt.xlabel('singular value index')
plt.ylabel('singular value')
plt.title('Shifted Sonin off-diagonal block singular values')
plt.tight_layout()
plt.savefig(OUT/'commutator_block_singular_values_step153.png', dpi=200)
plt.close()

# kernel profile plot for selected gammas
plt.figure(figsize=(7,4.5))
for gamma in [gammas[0], gammas[len(gammas)//2], gammas[-1]]:
    sub = profiles_df[profiles_df['gamma'] == gamma]
    plt.plot(sub['index'], sub['abs_eta'], label=f'gamma={gamma:.1f}')
plt.xlabel('discrete coordinate')
plt.ylabel('|pulled evaluator toy kernel|')
plt.title('Pulled evaluator kernel profiles after Sonin projection')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'pulled_evaluator_kernel_profiles_step153.png', dpi=200)
plt.close()

plt.figure(figsize=(7,4.5))
plt.semilogy(xi_df['eigen_index'], np.maximum(xi_df['xi_eigenvalue'], 1e-16), marker='o')
plt.xlabel('eigenvalue index')
plt.ylabel('Xi eigenvalue')
plt.title('Toy Xi^BC spectrum on pulled evaluator family')
plt.tight_layout()
plt.savefig(OUT/'xi_bc_toy_spectrum_step153.png', dpi=200)
plt.close()

# scenario diagram data/plot
scenarios = pd.DataFrame({
    'scenario': ['co-Poisson factorization', 'projection reduction', 'generic raw shift', 'scoped residual'],
    'residual_floor': [0.0, 0.0, 0.42, 0.18],
    'status_score': [1.0, 0.9, 0.2, 0.55],
})
scenarios.to_csv(OUT/'direct_exclusion_scenarios_step153.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.bar(scenarios['scenario'], scenarios['residual_floor'])
plt.ylabel('residual floor (schematic)')
plt.title('Direct exclusion route scenarios')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
plt.savefig(OUT/'direct_exclusion_scenarios_step153.png', dpi=200)
plt.close()

# Structure check for tex
tex = (OUT/'pulled_evaluator_kernel_step153.tex').read_text()
check = {
    'tex_exists': (OUT/'pulled_evaluator_kernel_step153.tex').exists(),
    'sections': tex.count('\\section'),
    'boxed_count': tex.count('\\boxed'),
    'has_kernel_formula': 'K_a^\\Gamma' in tex,
    'has_commutator_formula': '[M_{m_\\ell},\\mathsf P_\\infty]' in tex,
    'max_commutator_identity_error': float(check_df['identity_error'].max()),
    'toy_xi_min_eigenvalue': float(xi_eigs.min()),
    'toy_xi_max_eigenvalue': float(xi_eigs.max()),
}
(OUT/'step153_check_results.json').write_text(json.dumps(check, indent=2))

print(json.dumps(check, indent=2))
