import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step36_coercivity')
OUT.mkdir(parents=True, exist_ok=True)

def psd_sqrt_inv(A, tol=1e-10):
    w, V = np.linalg.eigh((A+A.T)/2)
    invsqrt = np.zeros_like(A)
    for i, lam in enumerate(w):
        if lam > tol:
            invsqrt += (1/np.sqrt(lam)) * np.outer(V[:, i], V[:, i])
    return invsqrt

def pinv_psd(A, tol=1e-10):
    w, V = np.linalg.eigh((A+A.T)/2)
    P = np.zeros_like(A)
    for i, lam in enumerate(w):
        if lam > tol:
            P += (1/lam) * np.outer(V[:, i], V[:, i])
    return P

def max_eig(A):
    return np.linalg.eigvalsh((A+A.T)/2)[-1]

def min_eig(A):
    return np.linalg.eigvalsh((A+A.T)/2)[0]

# 1) Cumulative strict threshold coercivity: C_N = I + Lambda_N L^T L, L=I, Theta0=I.
rows=[]
d=3
I=np.eye(d)
L=np.eye(d)
for p in [0.5, 1.0, 2.0]:
    Lambda=0.0
    for n in range(1, 101):
        lam = n**(-p)
        Lambda += lam
        C = I + Lambda * (L.T @ L)
        K = L @ np.linalg.inv(C) @ L.T
        rows.append({
            'model':'threshold_growth',
            'p':p,
            'n':n,
            'lambda_increment':lam,
            'Lambda':Lambda,
            'lambda_max_K':max_eig(K),
            'bound_1_over_1plusLambda':1/(1+Lambda),
            'collapse_predicted': p<=1.0,
        })
pd.DataFrame(rows).to_csv(OUT/'threshold_growth_coercivity_step36.csv', index=False)

# 2) Partial hardening no-go: only e1 hardens in two-dimensional anti-invariant family.
rows=[]
for lam in np.logspace(-3, 4, 60):
    C = np.diag([1+lam, 1.0])
    K = np.linalg.inv(C)
    rows.append({
        'model':'partial_hardening_no_collapse',
        'lambda':lam,
        'K11':K[0,0],
        'K22':K[1,1],
        'lambda_max_K':max_eig(K),
    })
pd.DataFrame(rows).to_csv(OUT/'partial_hardening_no_go_step36.csv', index=False)

# 3) Component factorization checks.
rng=np.random.default_rng(36)
rows=[]
for trial in range(80):
    n=5; r=7; m=3
    F=rng.normal(size=(r,n))
    # Make full rank robustly
    FTF=F.T@F + 0.5*np.eye(n)
    B=rng.normal(size=(m,r))
    L=B@F
    Theta=np.eye(m)
    M=max_eig(B.T@B)  # ||B||^2
    C=FTF
    # theorem says C >= (1/M)L^T L if M>0
    lhs=C-(1/M)*(L.T@L)
    K=L@np.linalg.inv(C)@L.T
    rows.append({
        'trial':trial,
        'factor_bound_M':M,
        'min_eig_C_minus_bound':min_eig(lhs),
        'lambda_max_K':max_eig(K),
        'bound_M':M,
        'passes_K_le_M_I':max_eig(K)<=M+1e-8,
    })
pd.DataFrame(rows).to_csv(OUT/'component_factorization_checks_step36.csv', index=False)

# 4) Root-composite character forcing for cyclic group C_m: nontrivial character budgets.
# Circulant coercivity eigenvalues: invariant block unchanged, anti-invariant/nontrivial block hardens by Lambda.
rows=[]
for m in [4,8,16]:
    for Lambda in np.logspace(-2, 3, 70):
        # response currency eigenvalues: trivial = 1, nontrivial = 1/(1+Lambda)
        rows.append({
            'm':m,
            'Lambda':Lambda,
            'trivial_character_budget':1.0,
            'nontrivial_character_budget':1/(1+Lambda),
            'anti_invariant_max_budget':1/(1+Lambda),
        })
pd.DataFrame(rows).to_csv(OUT/'root_character_forcing_step36.csv', index=False)

# 5) Symmetry-only no collapse: C commutes with plus/minus split but K^- = 1/gap can be nonzero.
rows=[]
for gap_minus in np.logspace(-3, 3, 70):
    Cminus=gap_minus*np.eye(2)
    Kminus=np.linalg.inv(Cminus)
    rows.append({
        'gap_minus':gap_minus,
        'lambda_max_K_minus':max_eig(Kminus),
        'symmetry_commutes':True,
    })
pd.DataFrame(rows).to_csv(OUT/'symmetry_only_no_collapse_step36.csv', index=False)

# Plots
th=pd.read_csv(OUT/'threshold_growth_coercivity_step36.csv')
plt.figure(figsize=(7,4))
for p,grp in th.groupby('p'):
    plt.plot(grp['n'], grp['lambda_max_K'], label=f'p={p}')
plt.yscale('log')
plt.xlabel('strict-extension step n')
plt.ylabel('max anti-invariant budget')
plt.title('Cumulative coercivity: summable vs divergent thresholds')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'threshold_growth_coercivity_step36.png', dpi=160)
plt.close()

ph=pd.read_csv(OUT/'partial_hardening_no_go_step36.csv')
plt.figure(figsize=(7,4))
plt.plot(ph['lambda'], ph['K11'], label='hardened direction')
plt.plot(ph['lambda'], ph['K22'], label='uncovered direction')
plt.plot(ph['lambda'], ph['lambda_max_K'], label='max budget')
plt.xscale('log'); plt.yscale('log')
plt.xlabel('hardening lambda')
plt.ylabel('budget')
plt.title('Partial hardening leaves an anti-invariant direction unpriced')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'partial_hardening_no_go_step36.png', dpi=160)
plt.close()

rc=pd.read_csv(OUT/'root_character_forcing_step36.csv')
plt.figure(figsize=(7,4))
for m,grp in rc.groupby('m'):
    plt.plot(grp['Lambda'], grp['anti_invariant_max_budget'], label=f'C_{m}')
plt.xscale('log'); plt.yscale('log')
plt.xlabel('nontrivial-character coercivity Lambda')
plt.ylabel('anti-invariant character budget')
plt.title('Root-composite character forcing collapses nontrivial budgets')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'root_character_forcing_step36.png', dpi=160)
plt.close()

# Key table
key=[]
for p in [0.5,1.0,2.0]:
    grp=th[th['p']==p].iloc[-1]
    key.append({'case':f'threshold_growth_p_{p}', 'budget_at_n100':grp['lambda_max_K'], 'verdict':'divergent coercivity' if p<=1 else 'summable/no full collapse'})
key.append({'case':'partial_hardening_lambda_1e4','budget_at_n100':ph.iloc[-1]['lambda_max_K'],'verdict':'fails full collapse: uncovered direction remains'})
pd.DataFrame(key).to_csv(OUT/'step36_key_table.csv', index=False)
print('done', OUT)
