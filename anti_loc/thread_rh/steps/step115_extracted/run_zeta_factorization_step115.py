import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step115_zeta_factorization')
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(115)

# Finite-dimensional sanity model.
# H_in -> L_a, with Y_a a finite zero-evaluator subspace.
# B is the shifted boundary block. Xi_BC = B^* Pi_Y B.

def orthonormal(n, k):
    A = rng.normal(size=(n, k))
    Q, _ = np.linalg.qr(A)
    return Q[:, :k]

n = 96      # ambient Burnol/Sonine model dimension
m = 48      # input boundary dimension
rank_y = 24 # zero-evaluator window dimension
Y = orthonormal(n, rank_y)
PiY = Y @ Y.T
B_base = rng.normal(size=(n, m)) / np.sqrt(n)

# Construct a path from co-Poisson inclusion (small Y residual) to generic raw shift.
rows = []
for theta in np.linspace(0, 1, 21):
    # B = sqrt(1-theta) mostly in P_a + sqrt(theta) generic residual
    P_component = (np.eye(n) - PiY) @ B_base
    Y_component = PiY @ rng.normal(size=(n, m)) / np.sqrt(n)
    B = np.sqrt(max(0, 1-theta)) * P_component + np.sqrt(theta) * Y_component
    G = B.T @ B
    Xi = B.T @ PiY @ B
    # normalized residual = largest generalized eigenvalue Xi <= eps^2 G
    reg = 1e-10 * np.eye(m)
    vals = np.linalg.eigvalsh(np.linalg.pinv(G + reg) @ Xi)
    eps2 = float(max(0, np.max(np.real(vals))))
    trace_frac = float(np.trace(Xi) / max(np.trace(G), 1e-12))
    rows.append({"theta_raw_shift_residual": theta, "epsilon2_max": eps2, "trace_fraction": trace_frac})

pd.DataFrame(rows).to_csv(OUT/'zeta_factorization_residual_sweep_step115.csv', index=False)

# Source absorption toy: source frame grows on the Y-residual sector.
rows2 = []
Xi_norm = 1.0
for N in range(1, 61):
    Lambda = np.log(N+2) ** 2
    tail = 1 / (N+1)**0.75
    bound = Xi_norm / max(Lambda, 1e-9) + tail
    rows2.append({"N": N, "Lambda_N": Lambda, "tail": tail, "absorbed_residual_bound": bound})
pd.DataFrame(rows2).to_csv(OUT/'xi_bc_source_absorption_model_step115.csv', index=False)

# Finite zero-window promotion model: if zero-window tail decreases, finite residual promotes.
rows3 = []
for M in range(5, 105, 5):
    finite_res = np.exp(-M/30)
    tail = 1 / np.sqrt(M)
    total = finite_res + tail
    rows3.append({"zero_window_M": M, "finite_residual": finite_res, "tail": tail, "promoted_residual": total})
pd.DataFrame(rows3).to_csv(OUT/'finite_zero_window_residual_model_step115.csv', index=False)

# Plot 1: residual sweep
fig, ax = plt.subplots(figsize=(7,4.5))
df = pd.DataFrame(rows)
ax.plot(df['theta_raw_shift_residual'], df['epsilon2_max'], marker='o', label='worst normalized residual')
ax.plot(df['theta_raw_shift_residual'], df['trace_fraction'], marker='s', label='trace residual fraction')
ax.set_xlabel('raw-shift residual mixing parameter')
ax.set_ylabel('boundary-to-zero residual')
ax.set_title('Zeta-factorization residual sweep')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUT/'zeta_factorization_residual_sweep_step115.png', dpi=180)
plt.close(fig)

# Plot 2: source absorption
fig, ax = plt.subplots(figsize=(7,4.5))
df2 = pd.DataFrame(rows2)
ax.plot(df2['N'], df2['absorbed_residual_bound'], marker='o')
ax.set_xlabel('source ladder index N')
ax.set_ylabel('residual bound')
ax.set_title('Source absorption of Xi_BC residual')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUT/'xi_bc_source_absorption_step115.png', dpi=180)
plt.close(fig)

# Plot 3: finite zero-window residual promotion
fig, ax = plt.subplots(figsize=(7,4.5))
df3 = pd.DataFrame(rows3)
ax.plot(df3['zero_window_M'], df3['finite_residual'], marker='o', label='finite zero-window residual')
ax.plot(df3['zero_window_M'], df3['tail'], marker='s', label='tail')
ax.plot(df3['zero_window_M'], df3['promoted_residual'], marker='^', label='promoted residual')
ax.set_xlabel('zero window M')
ax.set_ylabel('residual/tail')
ax.set_title('Finite zero-window residual needs tail promotion')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUT/'finite_zero_window_residual_step115.png', dpi=180)
plt.close(fig)

# Structural LaTeX balance check.
tex = (OUT/'zeta_factorization_attempt_step115.tex').read_text()
check = {
    'begin_document': tex.count('\\begin{document}'),
    'end_document': tex.count('\\end{document}'),
    'begin_equation_like': tex.count('\\['),
    'end_equation_like': tex.count('\\]'),
    'status': 'pass' if tex.count('\\begin{document}') == tex.count('\\end{document}') and tex.count('\\[') == tex.count('\\]') else 'check'
}
(OUT/'latex_structure_check_step115.json').write_text(json.dumps(check, indent=2))
print(json.dumps(check, indent=2))
