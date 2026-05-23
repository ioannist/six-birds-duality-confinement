import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json

out = Path('/mnt/data/rh_membrane_step115_zeta_factorization')
out.mkdir(parents=True, exist_ok=True)
np.random.seed(115)

# Finite toy model for the logical gate, not RH evidence.
# H_N = C^N. P is a discrete Sonin-like projection: intersection of time/frequency complements.
def fourier_matrix(N):
    j,k = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    return np.exp(2j*np.pi*j*k/N)/np.sqrt(N)

def proj_from_cols(cols, N):
    if len(cols)==0:
        return np.zeros((N,N), dtype=complex)
    Q = np.eye(N, dtype=complex)[:, cols]
    return Q @ Q.conj().T

def shift_matrix(N, m):
    T = np.zeros((N,N), dtype=complex)
    for i in range(N):
        T[(i+m)%N, i] = 1.0
    return T

def projection_onto_colspace(A, tol=1e-10):
    U, s, Vh = np.linalg.svd(A, full_matrices=False)
    r = np.sum(s>tol)
    if r==0:
        return np.zeros((A.shape[0], A.shape[0]), dtype=complex), s, 0
    U = U[:, :r]
    return U @ U.conj().T, s, r

def rand_orthonormal_in_complement(P_range, d):
    N = P_range.shape[0]
    vecs = []
    trials = 0
    while len(vecs)<d and trials<10000:
        z = np.random.randn(N)+1j*np.random.randn(N)
        # remove range component and already selected components
        z = z - P_range @ z
        for v in vecs:
            z = z - v*np.vdot(v,z)
        n = np.linalg.norm(z)
        if n>1e-9:
            vecs.append(z/n)
        trials += 1
    if len(vecs)==0:
        return np.zeros((N,0), dtype=complex)
    return np.column_stack(vecs)

N = 192
F = fourier_matrix(N)
# time window and frequency window sizes
w = 32
center = N//2
# interval around center for time cutoff; use grid as circle for toy
T_cols = list(range(center-w//2, center+w//2))
PT = proj_from_cols(T_cols, N)
# frequency window: columns in Fourier basis near low frequency
freq_cols = list(range(0,w//2)) + list(range(N-w//2, N))
PF = F.conj().T @ proj_from_cols(freq_cols, N) @ F
# Sonin-like projection onto intersection of complements: nullspace of stacked [PT; PF]
# Since PT, PF projections, intersection complement projection = nullspace of [PT; PF]
A = np.vstack([PT, PF])
U, s, Vh = np.linalg.svd(A, full_matrices=True)
rank = np.sum(s>1e-9)
Qnull = Vh.conj().T[:, rank:]
P = Qnull @ Qnull.conj().T

# one log-shift proxy
m_shift = 11
Tau = shift_matrix(N, m_shift)
B = P @ Tau @ (np.eye(N)-P)
PB, sing_B, rank_B = projection_onto_colspace(B)

# Construct two zero-evaluator models: a generic finite zero window and an annihilating control.
# Generic zero-evaluator span Y_d is random, not arranged to annihilate boundary packets.
dims = np.arange(1, 81)
rows = []
for d in dims:
    # Generic Y projection
    Q = np.random.randn(N,d)+1j*np.random.randn(N,d)
    Q, _ = np.linalg.qr(Q)
    PY = Q @ Q.conj().T
    Xi = B.conj().T @ PY @ B
    eigs = np.linalg.eigvalsh((Xi+Xi.conj().T)/2)
    trace = np.trace(Xi).real
    norm = max(eigs.max(), 0)
    rows.append({"model":"generic_zero_window","zero_window_dim":int(d),"xi_trace":trace,"xi_norm":norm,"annihilation_error":np.linalg.norm(PY@B,2)})
    # Annihilating control: choose Y in complement of range(B) when possible.
    Qc = rand_orthonormal_in_complement(PB, min(d, max(0,N-rank_B)))
    PYc = Qc @ Qc.conj().T
    Xic = B.conj().T @ PYc @ B
    eigsc = np.linalg.eigvalsh((Xic+Xic.conj().T)/2)
    rows.append({"model":"annihilating_control","zero_window_dim":int(Qc.shape[1]),"xi_trace":np.trace(Xic).real,"xi_norm":max(eigsc.max() if len(eigsc)>0 else 0,0),"annihilation_error":np.linalg.norm(PYc@B,2) if Qc.shape[1]>0 else 0.0})

df = pd.DataFrame(rows)
df.to_csv(out/'boundary_zero_annihilation_sweep_step115.csv', index=False)

plt.figure(figsize=(7,4.5))
for model, sub in df.groupby('model'):
    plt.plot(sub['zero_window_dim'], sub['xi_norm'], marker='o', markersize=2, linewidth=1, label=model.replace('_',' '))
plt.xlabel('finite zero-evaluator window dimension')
plt.ylabel(r'$\|\Xi^{BC}_{\ell}\|$ (toy)')
plt.title('Boundary-to-zero residual: generic vs annihilating control')
plt.yscale('symlog', linthresh=1e-14)
plt.legend()
plt.tight_layout()
plt.savefig(out/'boundary_zero_residual_sweep_step115.png', dpi=180)
plt.close()

# Factorization proxy: random linear functional zero evaluations on range(B). Determine if all vanish.
# Choose d=24 and compute rows of evaluation matrix E B.
d=24
E = np.random.randn(d,N)+1j*np.random.randn(d,N)
# normalize rows
E = E/np.linalg.norm(E, axis=1, keepdims=True)
EB = E @ B
sv_EB = np.linalg.svd(EB, compute_uv=False)
pd.DataFrame({'index':np.arange(len(sv_EB)), 'singular_value':sv_EB}).to_csv(out/'zero_evaluator_boundary_matrix_singular_values_step115.csv', index=False)
plt.figure(figsize=(6,4))
plt.semilogy(np.arange(len(sv_EB)), sv_EB, marker='o', linewidth=1)
plt.xlabel('index')
plt.ylabel('singular value of zero-evaluator boundary matrix')
plt.title('Generic annihilation matrix is not zero')
plt.tight_layout()
plt.savefig(out/'zero_evaluator_boundary_matrix_step115.png', dpi=180)
plt.close()

# Source absorption model for residual Xi: if source frame covers range(PYB) with growth Lambda, residual is absorbed.
Lambda_vals = np.geomspace(1, 1e4, 80)
xi_norm0 = float(np.linalg.norm(EB,2)**2)
compact_tail = 0.04/(1+np.arange(80))
abs_rows=[]
for j,Lam in enumerate(Lambda_vals):
    # effective residual after source strength Lam; toy bound xi/(1+Lam) + tail
    rem = xi_norm0/(1+Lam) + compact_tail[j]
    abs_rows.append({'stage':j+1,'Lambda':Lam,'initial_xi_norm':xi_norm0,'tail':compact_tail[j],'absorbed_residual_bound':rem})
abs_df=pd.DataFrame(abs_rows)
abs_df.to_csv(out/'source_absorption_of_boundary_residual_step115.csv', index=False)
plt.figure(figsize=(6.5,4))
plt.loglog(abs_df['Lambda'], abs_df['absorbed_residual_bound'], linewidth=2)
plt.xlabel(r'source lower-frame strength $\Lambda$')
plt.ylabel('residual bound after absorption (toy)')
plt.title(r'Source absorption of $\Xi^{BC}$ if lower frame is earned')
plt.tight_layout()
plt.savefig(out/'source_absorption_boundary_residual_step115.png', dpi=180)
plt.close()

# Inclusion logic table
logic = [
    {"gate":"zero_evaluator_annihilation","mathematical_test":"Pi_Ya B_l = 0","status":"unearned/generic failure","repair":"prove zeta-factorization or absorb Xi_BC"},
    {"gate":"zeta_factorization","mathematical_test":"M(B_l u)(s)=zeta(s) alpha_{l,u}(s)","status":"not visible for raw shifted Sonin block","repair":"derive from co-Poisson synthesis or record failure"},
    {"gate":"boundary_residual","mathematical_test":"Xi_BC = B_l^* Pi_Ya B_l","status":"accepted residual object","repair":"Hecke/Dirichlet source lower frame on residual range"},
    {"gate":"fixed_exhaustive_promotion","mathematical_test":"finite zero windows + vanishing tail","status":"required","repair":"Burnol completeness/minimality + tail record"},
]
pd.DataFrame(logic).to_csv(out/'zeta_factorization_gate_table_step115.csv', index=False)

# Theorem map
thm = [
    {"name":"Zero-evaluator criterion","claim":"Ran(B_l) subset P_a iff Pi_Ya B_l=0","status":"proved as projection identity"},
    {"name":"Factorization sufficiency","claim":"M(B_l u)=zeta alpha_u implies Ran(B_l) subset P_a","status":"proved conditional on growth/support legality"},
    {"name":"Generic failure witness","claim":"If Pi_Ya B_l nonzero then zeta-factorization fails for that input","status":"proved by evaluator obstruction"},
    {"name":"Residual absorption theorem","claim":"Xi_BC <= F_n+E_n with lower-frame growth absorbs boundary residual","status":"conditional framework theorem"},
]
pd.DataFrame(thm).to_csv(out/'theorem_map_step115.csv', index=False)

# schema
schema={
    "step":115,
    "title":"Zeta-factorization attempt for shifted boundary packets",
    "objects":["B_l=J_a P_infty tau_l (I-P_infty)","Y_a zero-evaluator span","P_a co-Poisson complement","Xi_BC=B_l^*Pi_Ya B_l"],
    "verdict":"raw zeta-factorization not earned; route reduces to zero-evaluator annihilation or source absorption",
    "next_step":"Hecke/Dirichlet source absorption of Xi_BC residual"
}
(out/'step115_schema.json').write_text(json.dumps(schema, indent=2))

# simple structural checks output
checks = {
    "N":N,
    "sonin_like_projection_rank":int(np.linalg.matrix_rank(P, tol=1e-8)),
    "boundary_block_rank":int(rank_B),
    "boundary_block_norm":float(np.linalg.norm(B,2)),
    "generic_EB_norm_squared":xi_norm0,
    "identity_description":"Finite toy model only; tests projection identities, not RH."
}
(out/'finite_model_sanity_step115.json').write_text(json.dumps(checks, indent=2))
