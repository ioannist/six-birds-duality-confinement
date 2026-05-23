import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step113_burnol_density')
OUT.mkdir(parents=True, exist_ok=True)

# Deterministic model for residual decomposition:
# total residual = atom exhaustion residual + irreducible boundary-outside-Pa residual.
N = np.array([4,8,12,16,24,32,48,64,96,128], dtype=float)
atom = np.array([0.52,0.36,0.25,0.175,0.09,0.048,0.018,0.006,0.0015,0.0004])
outside = np.full_like(N, 0.12)
total = atom + outside
c = 1 - total

df = pd.DataFrame({
    'N': N.astype(int),
    'atom_exhaustion_residual': atom,
    'boundary_outside_Pa_residual': outside,
    'total_visibility_residual_squared': total,
    'c_N': c,
})
df.to_csv(OUT/'residual_decomposition_step113.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.plot(N, atom, marker='o', label='within-P_a atom exhaustion residual')
plt.plot(N, outside, marker='o', label='boundary outside P_a residual')
plt.plot(N, total, marker='o', label='total residual squared')
plt.xlabel('Declared atom count N')
plt.ylabel('Residual contribution')
plt.title('Step 113 residual decomposition')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'residual_decomposition_step113.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(N, c, marker='o')
plt.xlabel('Declared atom count N')
plt.ylabel('visibility constant c_N')
plt.title('Visibility saturates below 1 if boundary has component outside P_a')
plt.tight_layout()
plt.savefig(OUT/'visibility_components_step113.png', dpi=180)
plt.close()

# Compare two scenarios: inclusion true vs inclusion false.
atom2 = 0.8*np.exp(-N/24)
c_inclusion = 1 - atom2
c_no_inclusion = 1 - (atom2 + 0.12)
scenario = pd.DataFrame({
    'N': N.astype(int),
    'c_N_if_boundary_in_Pa': c_inclusion,
    'c_N_if_boundary_outside_Pa_residual_0p12': c_no_inclusion
})
scenario.to_csv(OUT/'finite_atom_exhaustion_scenarios_step113.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(N, c_inclusion, marker='o', label='B subset P_a')
plt.plot(N, c_no_inclusion, marker='o', label='B has outside-P_a component')
plt.xlabel('Declared atom count N')
plt.ylabel('visibility constant c_N')
plt.title('Atom exhaustion closes visibility only if boundary lands in P_a')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'finite_atom_exhaustion_step113.png', dpi=180)
plt.close()

# Algebra identity sanity check with random finite projections.
rng = np.random.default_rng(113)
rows = []
for trial in range(20):
    Hdim = 40
    Bdim = 6
    Pdim = 18
    # random boundary synthesis M
    M = rng.normal(size=(Hdim, Bdim))
    G = M.T @ M
    G_invhalf = np.linalg.inv(np.linalg.cholesky(G)).T
    # random atom projection P_N rank Pdim
    Q, _ = np.linalg.qr(rng.normal(size=(Hdim, Pdim)))
    P = Q @ Q.T
    R = (np.eye(Hdim)-P) @ M @ G_invhalf
    eps2_direct = np.linalg.norm(R, 2)**2
    cval = 1 - eps2_direct
    # identity: M^T P M = G - E^T E, whitened eigen min = c
    E = (np.eye(Hdim)-P) @ M
    lhs = M.T @ P @ M
    rhs = G - E.T @ E
    err = np.linalg.norm(lhs-rhs)
    whitened = G_invhalf.T @ lhs @ G_invhalf
    eigmin = np.linalg.eigvalsh((whitened+whitened.T)/2)[0]
    rows.append({'trial': trial, 'identity_error': err, 'c_from_norm': cval, 'c_from_eigmin': eigmin, 'diff': abs(cval-eigmin)})
check = pd.DataFrame(rows)
check.to_csv(OUT/'projection_identity_checks_step113.csv', index=False)
print(check.describe().to_string())
