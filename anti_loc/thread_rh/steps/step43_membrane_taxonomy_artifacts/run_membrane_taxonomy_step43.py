import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step43_taxonomy')
OUT.mkdir(parents=True, exist_ok=True)

def eigmax(A): return float(np.linalg.eigvalsh((A+A.T)/2).max())
def eigmin(A): return float(np.linalg.eigvalsh((A+A.T)/2).min())

rows=[]
# section diagonal pass / global fail
for rho in np.linspace(0,1,21):
    K=np.array([[1,rho],[rho,1.0]])
    Theta=np.eye(2)
    y=np.array([1,1])/np.sqrt(2)
    rows.append({
        'case':'sectioned_diagonal_pass_global_fail',
        'parameter':rho,
        'diagonal_max':max(K[0,0],K[1,1]),
        'global_lambda_max':eigmax(K),
        'witness_capacity':float(y@K@y),
        'budget_lambda_max':1.0,
        'violation':eigmax(K-Theta),
        'status':'fails_global' if rho>1e-12 else 'passes_global'
    })
section_df=pd.DataFrame(rows)
section_df.to_csv(OUT/'section_countermodel_step43.csv',index=False)

# protocol duplication
rows=[]
for m in range(1,21):
    K=np.ones((m,m))
    y=np.ones(m)/np.sqrt(m)
    rows.append({
        'case':'protocol_duplicated_routes',
        'm_protocols':m,
        'diagonal_capacity':1.0,
        'block_lambda_max':eigmax(K),
        'normalized_all_routes_capacity':float(y@K@y),
        'violation_vs_identity':eigmax(K-np.eye(m)),
        'status':'fails_protocol_union' if m>1 else 'passes'
    })
protocol_df=pd.DataFrame(rows)
protocol_df.to_csv(OUT/'protocol_duplication_countermodel_step43.csv',index=False)

# bundle fiberwise finite / no uniform sup
rows=[]
for n in range(1,41):
    rows.append({'fiber':n,'fiber_currency':float(n),'finite_each_fiber':True,'running_sup':float(n)})
bundle_df=pd.DataFrame(rows)
bundle_df.to_csv(OUT/'bundle_uniformity_countermodel_step43.csv',index=False)

# public shadow overread: compress projection F only sees first coordinate, hidden second violates
K=np.diag([0.5,2.0])
Theta=np.eye(2)
F=np.array([[1.0,0.0]])
shadow_K=F@K@F.T
shadow_Theta=F@Theta@F.T
public_shadow_rows=[{
    'case':'public_shadow_pass_hidden_fail',
    'full_lambda_max_KminusTheta':eigmax(K-Theta),
    'shadow_lambda_max_KminusTheta':eigmax(shadow_K-shadow_Theta),
    'full_status':'fails_full_membrane',
    'shadow_status':'passes_public_shadow'
}]
pd.DataFrame(public_shadow_rows).to_csv(OUT/'public_shadow_taxonomy_countermodel_step43.csv',index=False)

# defective bridge: old budget=I, residual eps I, bound function vs t
rows=[]
eps=0.05
for t in np.logspace(-2,2,100):
    trace_bound=(1+t)*2+(1+1/t)*2*eps
    rows.append({'t':t,'trace_bound':trace_bound,'eps':eps})
defect_df=pd.DataFrame(rows)
defect_df.to_csv(OUT/'defective_transfer_bound_step43.csv',index=False)

# exact transfer random checks: F K F^* <= F Theta F^* if K<=Theta
rng=np.random.default_rng(43)
rows=[]
for trial in range(50):
    n=5; m=3
    A=rng.normal(size=(n,n))
    Theta=A@A.T+np.eye(n)
    B=rng.normal(size=(n,n))
    K=0.25*(B@B.T)
    # scale K to ensure <= Theta roughly by generalized eig bound
    lam=eigmax(np.linalg.solve(np.linalg.cholesky(Theta), K) @ np.linalg.inv(np.linalg.cholesky(Theta)).T) if False else None
    # use K = Theta^(1/2) S Theta^(1/2) with S<=I
    vals, vecs=np.linalg.eigh(Theta)
    Thalf=vecs@np.diag(np.sqrt(vals))@vecs.T
    S=rng.normal(size=(n,n)); S=S@S.T
    S=S/(2*eigmax(S)+1e-12)
    K=Thalf@S@Thalf
    F=rng.normal(size=(m,n))
    diff=F@(Theta-K)@F.T
    rows.append({'trial':trial,'min_eig_transfer_slack':eigmin(diff),'status':'passes' if eigmin(diff)>-1e-9 else 'fails'})
transfer_df=pd.DataFrame(rows)
transfer_df.to_csv(OUT/'exact_transfer_random_checks_step43.csv',index=False)

# plots
plt.figure(figsize=(6,4))
plt.plot(section_df['parameter'], section_df['global_lambda_max'], marker='o')
plt.axhline(1, linestyle='--')
plt.xlabel('section cross-correlation rho')
plt.ylabel('global max eigenvalue')
plt.title('Section-local budgets do not imply global membrane')
plt.tight_layout(); plt.savefig(OUT/'section_countermodel_step43.png', dpi=200); plt.close()

plt.figure(figsize=(6,4))
plt.plot(protocol_df['m_protocols'], protocol_df['block_lambda_max'], marker='o')
plt.axhline(1, linestyle='--')
plt.xlabel('number of duplicated protocols')
plt.ylabel('stacked block max eigenvalue')
plt.title('Protocol-local budgets do not imply protocol union')
plt.tight_layout(); plt.savefig(OUT/'protocol_duplication_step43.png', dpi=200); plt.close()

plt.figure(figsize=(6,4))
plt.plot(bundle_df['fiber'], bundle_df['running_sup'], marker='o')
plt.xlabel('fiber index')
plt.ylabel('running essential sup budget')
plt.title('Fiberwise finite does not imply uniform bundle membrane')
plt.tight_layout(); plt.savefig(OUT/'bundle_uniformity_step43.png', dpi=200); plt.close()

plt.figure(figsize=(6,4))
plt.semilogx(defect_df['t'], defect_df['trace_bound'])
plt.xlabel('defect tradeoff parameter t')
plt.ylabel('trace bound')
plt.title('Defective membrane transfer budget')
plt.tight_layout(); plt.savefig(OUT/'defective_transfer_bound_step43.png', dpi=200); plt.close()

print('wrote step43 checks')
