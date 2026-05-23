import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step115_zeta_factorization')
out.mkdir(parents=True, exist_ok=True)

# Toy model: boundary block B, zero-evaluator projection Y.
# We model the factorization residual Xi_BC = B^* Pi_Y B.
rng = np.random.default_rng(115)
Ns = np.arange(8, 81, 8)
rows = []
for N in Ns:
    # boundary dimension grows; zero evaluator rank grows slower
    d = N
    r = max(1, N//5)
    # B has noncompact-like plateau plus decaying compact part
    plateau = np.ones(min(d//3, 16))
    tail = np.linspace(0.9, 0.05, d-len(plateau)) if d>len(plateau) else np.array([])
    svals = np.concatenate([plateau, tail])
    # random singular vectors
    U,_ = np.linalg.qr(rng.normal(size=(d,d)))
    V,_ = np.linalg.qr(rng.normal(size=(d,d)))
    B = U @ np.diag(svals) @ V.T
    Y,_ = np.linalg.qr(rng.normal(size=(d,r)))
    Pi = Y @ Y.T
    Xi = B.T @ Pi @ B
    ev = np.linalg.eigvalsh(Xi)
    rows.append({
        'N': N,
        'boundary_dim': d,
        'zero_eval_rank': r,
        'residual_trace': float(np.trace(Xi)),
        'residual_op_norm': float(ev[-1]),
        'residual_min_pos_eig': float(ev[ev>1e-12][0]) if np.any(ev>1e-12) else 0.0,
        'rank_Xi_tol': int(np.sum(ev>1e-10)),
    })

pd.DataFrame(rows).to_csv(out/'boundary_copoisson_residual_step115.csv', index=False)

# Factorization obstruction model: shift multiplier m_l(s)=exp(l(1-s)) is nonzero on sample grid.
ells = [np.log(2), np.log(3), np.log(5)]
t = np.linspace(-40, 40, 801)
fac_rows=[]
for ell in ells:
    s = 0.5 + 1j*t
    m = np.exp(ell*(1-s))
    fac_rows.append(pd.DataFrame({
        'ell': ell,
        't': t,
        'abs_shift_multiplier': np.abs(m),
        'arg_shift_multiplier': np.angle(m),
        'min_abs_over_grid': np.min(np.abs(m))
    }))
pd.concat(fac_rows, ignore_index=True).to_csv(out/'shift_multiplier_nonzero_step115.csv', index=False)

# Source absorption model: residual trace decays only if source lower frame grows.
steps=np.arange(1,101)
residual_norm=1/(1+0.03*steps) + 0.1 # nonvanishing if not sourced
Lambda=np.log1p(steps)**2
absorbed=residual_norm/(1+Lambda)
pd.DataFrame({'step':steps,'residual_norm_before_source':residual_norm,'source_Lambda':Lambda,'residual_norm_after_source':absorbed}).to_csv(out/'source_absorption_of_xiBC_step115.csv', index=False)

# Plot residual norm
plt.figure(figsize=(6,4))
df=pd.read_csv(out/'boundary_copoisson_residual_step115.csv')
plt.plot(df['N'], df['residual_op_norm'], marker='o')
plt.xlabel('finite boundary dimension N')
plt.ylabel(r'$\|\Xi^{BC}\|$ toy residual')
plt.title('Boundary-to-co-Poisson residual persists in toy model')
plt.tight_layout()
plt.savefig(out/'boundary_copoisson_residual_step115.png', dpi=180)
plt.close()

# Plot shift multiplier abs
plt.figure(figsize=(6,4))
dfm=pd.read_csv(out/'shift_multiplier_nonzero_step115.csv')
for ell in ells:
    sub=dfm[np.isclose(dfm['ell'], ell)]
    plt.plot(sub['t'], sub['abs_shift_multiplier'], label=f'ell={ell:.3f}')
plt.xlabel(r'$t$ on $s=1/2+it$')
plt.ylabel(r'$|e^{\ell(1-s)}|$')
plt.title('Multiplicative shift multiplier is nonzero')
plt.legend()
plt.tight_layout()
plt.savefig(out/'shift_multiplier_nonzero_step115.png', dpi=180)
plt.close()

# Plot source absorption
plt.figure(figsize=(6,4))
dfs=pd.read_csv(out/'source_absorption_of_xiBC_step115.csv')
plt.plot(dfs['step'], dfs['residual_norm_before_source'], label='before source')
plt.plot(dfs['step'], dfs['residual_norm_after_source'], label='after source')
plt.xlabel('source ladder stage')
plt.ylabel('toy residual norm')
plt.title('Source absorption can charge residual if lower frame grows')
plt.legend()
plt.tight_layout()
plt.savefig(out/'source_absorption_of_xiBC_step115.png', dpi=180)
plt.close()

# Projection identity sanity checks
check_rows=[]
for seed in range(10):
    rng=np.random.default_rng(seed)
    d=20; r=6
    B=rng.normal(size=(d,d))
    Y,_=np.linalg.qr(rng.normal(size=(d,r)))
    Pi=Y@Y.T
    Xi=B.T@Pi@B
    # Xi PSD and equal to (Pi B)^*(Pi B)
    X2=(Pi@B).T@(Pi@B)
    err=np.linalg.norm(Xi-X2)
    mineig=float(np.min(np.linalg.eigvalsh((Xi+Xi.T)/2)))
    check_rows.append({'seed':seed,'identity_error':err,'min_eigenvalue':mineig})
pd.DataFrame(check_rows).to_csv(out/'projection_residual_identity_checks_step115.csv', index=False)
print('Step 115 artifacts generated at', out)
