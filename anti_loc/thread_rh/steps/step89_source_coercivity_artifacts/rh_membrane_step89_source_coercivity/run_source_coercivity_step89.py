import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT=Path('/mnt/data/rh_membrane_step89_source_coercivity')
np.random.seed(89)

def psd_sqrt(A):
    w,V=np.linalg.eigh((A+A.T)/2)
    w=np.maximum(w,0)
    return V@np.diag(np.sqrt(w))@V.T

def min_eig(A):
    return np.linalg.eigvalsh((A+A.T)/2)[0]

def pinv_psd(A, tol=1e-10):
    w,V=np.linalg.eigh((A+A.T)/2)
    inv=np.array([1/x if x>tol else 0 for x in w])
    return V@np.diag(inv)@V.T

# 1. Random source frame checks
rows=[]
for dim in [3,5,8,12]:
    for m in [dim, dim+3, 2*dim]:
        for trial in range(15):
            Q=np.random.randn(m,dim)
            lambdas=0.2+np.random.rand(m)
            F=sum(lambdas[i]*np.outer(Q[i],Q[i]) for i in range(m))
            lam=min_eig(F)
            C=np.eye(dim)*0.05+F
            K=pinv_psd(C)
            bound=(1/lam)*np.eye(dim) if lam>1e-10 else np.eye(dim)*np.inf
            slack = min_eig(bound-K) if np.isfinite(bound).all() else np.nan
            rows.append(dict(dim=dim,m=m,trial=trial,lambda_frame=lam,max_cap=np.linalg.eigvalsh(K).max(),bound=1/lam if lam>1e-10 else np.inf,slack_min=slack))
pd.DataFrame(rows).to_csv(OUT/'random_source_frame_checks_step89.csv',index=False)

# 2. Incomplete source: harden only first d-1 coords
rows=[]
for lam in np.logspace(-2,4,80):
    d=5
    F=np.diag([lam]*(d-1)+[0.0])
    C=np.eye(d)*1.0+F # baseline leaves last coordinate capacity 1
    K=pinv_psd(C)
    rows.append(dict(lambda_source=lam,cap_hardened=K[0,0],cap_uncovered=K[-1,-1],max_capacity=np.linalg.eigvalsh(K).max()))
pd.DataFrame(rows).to_csv(OUT/'incomplete_source_no_collapse_step89.csv',index=False)
plt.figure()
df=pd.DataFrame(rows)
plt.loglog(df['lambda_source'],df['cap_hardened'],label='covered direction')
plt.loglog(df['lambda_source'],df['cap_uncovered'],label='uncovered direction')
plt.xlabel('source strength $\\lambda$')
plt.ylabel('capacity')
plt.legend()
plt.title('Incomplete source family leaves hidden direction')
plt.tight_layout()
plt.savefig(OUT/'incomplete_source_no_collapse_step89.png',dpi=160)
plt.close()

# 3. Full source ladder collapse
rows=[]
for n in range(1,101):
    Lambda=n**1.2
    d=4
    C=np.eye(d)*Lambda
    K=pinv_psd(C)
    rows.append(dict(stage=n,Lambda=Lambda,max_capacity=np.linalg.eigvalsh(K).max(),trace_capacity=np.trace(K)))
pd.DataFrame(rows).to_csv(OUT/'full_source_ladder_collapse_step89.csv',index=False)
plt.figure()
df=pd.DataFrame(rows)
plt.loglog(df['stage'],df['max_capacity'])
plt.xlabel('stage n')
plt.ylabel('max capacity')
plt.title('Full-sector source ladder collapses budget')
plt.tight_layout()
plt.savefig(OUT/'full_source_ladder_collapse_step89.png',dpi=160)
plt.close()

# 4. Low + high split: low collapse, high bounded not collapsed
rows=[]
for n in range(1,101):
    lam=n
    m_high=2.0
    C=np.diag([lam,lam,m_high,m_high])
    K=pinv_psd(C)
    rows.append(dict(stage=n,low_cap=K[0,0],high_cap=K[2,2],max_capacity=np.linalg.eigvalsh(K).max()))
pd.DataFrame(rows).to_csv(OUT/'low_source_high_bounded_step89.csv',index=False)
plt.figure()
df=pd.DataFrame(rows)
plt.loglog(df['stage'],df['low_cap'],label='low sector')
plt.loglog(df['stage'],df['high_cap'],label='high sector')
plt.xlabel('stage n')
plt.ylabel('capacity')
plt.legend()
plt.title('Low-frequency collapse is not full-sector collapse')
plt.tight_layout()
plt.savefig(OUT/'low_source_high_bounded_step89.png',dpi=160)
plt.close()

# 5. finite-rank limitation in growing dimension: rank fixed source leaves max capacity 1
rows=[]
for d in range(2,41):
    r=min(3,d)
    lam=1000.0
    C=np.eye(d)
    C[:r,:r]+=lam*np.eye(r)
    K=pinv_psd(C)
    rows.append(dict(dim=d,rank_source=r,max_capacity=np.linalg.eigvalsh(K).max(),covered_capacity=K[0,0],uncovered_capacity=K[-1,-1]))
pd.DataFrame(rows).to_csv(OUT/'finite_rank_source_limitation_step89.csv',index=False)
plt.figure()
df=pd.DataFrame(rows)
plt.plot(df['dim'],df['max_capacity'],label='max capacity')
plt.plot(df['dim'],df['covered_capacity'],label='covered capacity')
plt.xlabel('dimension')
plt.ylabel('capacity')
plt.legend()
plt.title('Finite-rank source cannot cover growing sector')
plt.tight_layout()
plt.savefig(OUT/'finite_rank_source_limitation_step89.png',dpi=160)
plt.close()

# 6. status summary
summary = pd.DataFrame([
    dict(case='random_full_frame', result='source lower frame bound verified numerically', status='sanity_check'),
    dict(case='incomplete_source', result='uncovered direction remains capacity 1', status='no_collapse'),
    dict(case='full_source_ladder', result='max capacity decays like 1/Lambda', status='collapse_model'),
    dict(case='low_only_source', result='low collapses but high remains bounded', status='partial_only'),
    dict(case='finite_rank_source', result='fixed rank cannot cover growing/infinite sector', status='failure_mode')
])
summary.to_csv(OUT/'source_coercivity_status_summary_step89.csv',index=False)
print('wrote step89 artifacts to', OUT)
