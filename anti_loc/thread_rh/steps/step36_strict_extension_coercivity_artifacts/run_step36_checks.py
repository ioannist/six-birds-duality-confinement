import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step36_coercivity')
np.random.seed(3601)

def psd_sqrt_inv(A, tol=1e-10):
    w,V=np.linalg.eigh((A+A.T)/2)
    wi=np.array([1/np.sqrt(x) if x>tol else 0 for x in w])
    return V@np.diag(wi)@V.T

def maxeig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).max())

def mineig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

def pinv(A, tol=1e-10):
    w,V=np.linalg.eigh((A+A.T)/2)
    wi=np.array([1/x if x>tol else 0 for x in w])
    return V@np.diag(wi)@V.T

# 1 Exact factorization source checks
rows=[]
for trial in range(80):
    n=8; p=5; m=3
    R=np.random.randn(p,n)
    A=np.random.randn(m,p)
    L=A@R
    kappa=maxeig(A.T@A)  # theta=I
    for lam in [0.1,0.3,1.0,3.0,10.0,30.0]:
        C=lam*(R.T@R)+0.05*np.eye(n)
        K=L@pinv(C)@L.T
        ratio=maxeig(K) / (kappa/lam)
        rows.append(dict(trial=trial,lambda_val=lam,kappa=kappa,maxeig_K=maxeig(K),bound=kappa/lam,ratio=ratio,pass_check=ratio<=1+1e-8))
exact_df=pd.DataFrame(rows)
exact_df.to_csv(OUT/'exact_factorization_checks_step36.csv',index=False)

# 2 Accumulating threshold audit: divergent vs finite cumulative hardening
rows=[]
for n in range(1,501):
    Lambda_h=sum(1/k for k in range(1,n+1))
    Lambda_p2=sum(1/(k*k) for k in range(1,n+1))
    # model C = I + Lambda L^T L, L=I in two anti-invariant dimensions; K=(1+Lambda)^-1 I
    rows.append(dict(n=n,Lambda_harmonic=Lambda_h,maxK_harmonic=1/(1+Lambda_h),Lambda_p2=Lambda_p2,maxK_p2=1/(1+Lambda_p2)))
thr_df=pd.DataFrame(rows)
thr_df.to_csv(OUT/'threshold_accumulation_step36.csv',index=False)

# 3 Partial hardening failure
rows=[]
for lam in np.logspace(-3,4,80):
    C=np.diag([1+lam,1.0])
    L=np.eye(2)
    K=L@pinv(C)@L.T
    rows.append(dict(lambda_val=lam,k1=K[0,0],k2=K[1,1],maxeig_K=maxeig(K)))
partial_df=pd.DataFrame(rows)
partial_df.to_csv(OUT/'partial_hardening_failure_step36.csv',index=False)

# 4 Defective factorization checks L=AR+E. Bound uses L*L <= 2kappa R*R + 2 E*E.
rows=[]
for trial in range(50):
    n=7; p=4; m=3
    R=np.random.randn(p,n)
    A=np.random.randn(m,p)
    E=0.2*np.random.randn(m,n)
    L=A@R+E
    kappa=maxeig(A.T@A)
    alpha=2*kappa
    beta=2.0
    for lam in [0.5,1,2,5,10,20]:
        for mu in [0.5,1,2,5,10,20]:
            C=lam*(R.T@R)+mu*(E.T@E)+0.02*np.eye(n)
            K=L@pinv(C)@L.T
            bound=max(alpha/lam,beta/mu)
            rows.append(dict(trial=trial,lambda_R=lam,mu_E=mu,kappa=kappa,alpha=alpha,beta=beta,maxeig_K=maxeig(K),bound=bound,ratio=maxeig(K)/bound,pass_check=maxeig(K)<=bound+1e-8))
def_df=pd.DataFrame(rows)
def_df.to_csv(OUT/'defective_factorization_checks_step36.csv',index=False)

# 5 Character forcing toy: cyclic characters with nontrivial weights grow.
rows=[]
m=8
for n in range(1,101):
    lam_non = n/10
    # character budgets: trivial remains 1; nontrivial = 1/(1+lambda)
    for chi in range(m):
        if chi==0:
            budget=1.0; sector='trivial'
        else:
            budget=1/(1+lam_non); sector='nontrivial'
        rows.append(dict(stage=n,character=chi,sector=sector,lambda_nontrivial=lam_non,budget=budget))
char_df=pd.DataFrame(rows)
char_df.to_csv(OUT/'character_forcing_budget_step36.csv',index=False)

# source gate table
sources=[
    ('completion_gamma_pole_positive_feature','C >= lambda W_cmp^* W_cmp and L^- = A W_cmp','accepted only if feature maps are completed, visible, positive','signed explicit-formula terms used as if PSD'),
    ('root_composite_character_forcing','nontrivial character blocks get lambda_chi -> infinity','requires equivariant carrier and declared character family','trace-only or determinant-only descent'),
    ('threshold_refinement_growth','cumulative anti-invariant hardening Lambda_n -> infinity','requires S7/S8 transport and no finite-to-exact overread','finite-stage improvement claimed as limit'),
    ('parity_fixed_readout','L^- Gamma = 0 on legal quotient','exact collapse if native family is parity/fixed-sector only','gating away a real native probe without nonclaim'),
    ('explicit_nonclaim_gating','remove anti-invariant probes from claim scope','lawful only as weakened claim','presented as no-needle theorem'),
    ('partial_hardening','C hardens only selected anti-invariant coordinates','support-only; not collapse','claiming full anti-invariant budget collapse')
]
pd.DataFrame(sources,columns=['source','mathematical_premise','lawful_status','no_smuggling_risk']).to_csv(OUT/'coercivity_source_gate_table_step36.csv',index=False)

# Plots
plt.figure(figsize=(7,4.5))
for lam in [0.1,1,10,30]:
    sub=exact_df[exact_df.lambda_val==lam]
    plt.scatter(sub['kappa']/lam, sub['maxeig_K'], s=10, label=f'lambda={lam}')
mx=max(exact_df['bound'].max(), exact_df['maxeig_K'].max())
plt.plot([0,mx],[0,mx], linestyle='--')
plt.xlabel('bound kappa/lambda')
plt.ylabel('max eigenvalue of K')
plt.title('Exact factorization coercivity bound')
plt.legend(fontsize=8)
plt.tight_layout(); plt.savefig(OUT/'exact_factorization_bound_step36.png',dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
plt.plot(thr_df['n'],thr_df['maxK_harmonic'],label='divergent cumulative audit: sum 1/k')
plt.plot(thr_df['n'],thr_df['maxK_p2'],label='finite cumulative audit: sum 1/k^2')
plt.xlabel('stage n')
plt.ylabel('anti-invariant budget max eigenvalue')
plt.title('Threshold/refinement hardening: divergent vs finite')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'threshold_accumulation_step36.png',dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
plt.loglog(partial_df['lambda_val'], partial_df['k1'], label='hardened coordinate')
plt.loglog(partial_df['lambda_val'], partial_df['k2'], label='unhardened coordinate')
plt.loglog(partial_df['lambda_val'], partial_df['maxeig_K'], '--', label='full budget max')
plt.xlabel('hardening lambda')
plt.ylabel('budget')
plt.title('Partial hardening does not collapse full budget')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'partial_hardening_failure_step36.png',dpi=180); plt.close()

plt.figure(figsize=(7,4.5))
for sector,sub in char_df.groupby('sector'):
    # mean over characters
    avg=sub.groupby('stage')['budget'].mean().reset_index()
    plt.plot(avg['stage'],avg['budget'],label=sector)
plt.xlabel('stage')
plt.ylabel('character-sector budget')
plt.title('Root-composite character forcing')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'character_forcing_budget_step36.png',dpi=180); plt.close()

print('done', OUT)
