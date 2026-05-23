import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

out = Path('/mnt/data/anti_localization_step44_type_promotion')
out.mkdir(exist_ok=True, parents=True)

def eigmax(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).max())

def eigmin(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

# Section diagonal overread: K=[[1,rho],[rho,1]], diagonal budgets pass, full fails.
rows=[]
rhos=np.linspace(0,0.99,100)
for rho in rhos:
    K=np.array([[1.0,rho],[rho,1.0]])
    rows.append({
        'rho':rho,
        'diag_max':max(K[0,0],K[1,1]),
        'lambda_max_full':eigmax(K),
        'recombination_capacity':float(np.array([1,1])@K@np.array([1,1])/2),
        'passes_diagonal_budget_1': max(K[0,0],K[1,1])<=1+1e-12,
        'passes_full_budget_I': eigmax(K)<=1+1e-12
    })
pd.DataFrame(rows).to_csv(out/'section_diagonal_overread_step44.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot(rhos,[r['lambda_max_full'] for r in rows],label='full lambda_max')
plt.plot(rhos,[1]*len(rhos),'--',label='budget 1')
plt.xlabel('cross-section correlation rho')
plt.ylabel('largest intrinsic currency eigenvalue')
plt.title('Section diagonal budgets do not promote')
plt.legend()
plt.tight_layout()
plt.savefig(out/'section_promotion_failure_step44.png',dpi=160)
plt.close()

# Bundle uniformity: fiber finite but unbounded.
ns=np.arange(1,101)
rows=[]
for n in ns:
    rows.append({'fiber_index':int(n),'fiber_currency':float(n),'running_sup':float(n),'fiber_finite':True})
pd.DataFrame(rows).to_csv(out/'bundle_uniformity_failure_step44.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot(ns,ns,label='running uniform budget')
plt.xlabel('fiber index')
plt.ylabel('required uniform budget')
plt.title('Fiberwise finite does not imply uniform bundle membrane')
plt.tight_layout()
plt.savefig(out/'bundle_uniformity_failure_step44.png',dpi=160)
plt.close()

# Protocol duplication: diagonal route budgets pass, stacked fails.
rows=[]
for scale in np.linspace(0,1,51):
    K=np.array([[1.0,scale],[scale,1.0]])
    rows.append({
        'mixed_route_correlation':float(scale),
        'route_diag_budget':1.0,
        'stacked_lambda_max':eigmax(K),
        'passes_route_diagonal':True,
        'passes_stacked_budget_I':eigmax(K)<=1+1e-12
    })
pd.DataFrame(rows).to_csv(out/'protocol_promotion_failure_step44.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot([r['mixed_route_correlation'] for r in rows],[r['stacked_lambda_max'] for r in rows])
plt.axhline(1,color='gray',linestyle='--')
plt.xlabel('mixed protocol correlation')
plt.ylabel('stacked protocol lambda_max')
plt.title('Protocol-local budgets do not promote')
plt.tight_layout()
plt.savefig(out/'protocol_promotion_failure_step44.png',dpi=160)
plt.close()

# Exact promotion random checks.
rng=np.random.default_rng(44)
rows=[]
for trial in range(50):
    ny=3; nz=5
    # full-column J
    J=rng.normal(size=(nz,ny))
    while np.linalg.matrix_rank(J)<ny:
        J=rng.normal(size=(nz,ny))
    R=np.linalg.inv(J.T@J)@J.T
    # random PSD K_y
    A=rng.normal(size=(ny,ny)); Ky=A@A.T
    Kz=J@Ky@J.T
    Theta_z=Kz + 0.1*np.eye(nz)  # typed budget
    promoted=R@Theta_z@R.T
    diff=promoted-Ky
    rows.append({
        'trial':trial,
        'RJ_error':float(np.linalg.norm(R@J-np.eye(ny))),
        'min_eig_promoted_minus_KY':eigmin(diff),
        'frame_lower_bound':eigmin(J.T@J)
    })
pd.DataFrame(rows).to_csv(out/'exact_promotion_random_checks_step44.csv',index=False)

# Defective promotion check: construct residual E and verify bound.
rows=[]
for trial in range(50):
    nE=4; ny=3; nz=5
    C=np.eye(nE)
    L=rng.normal(size=(ny,nE))
    J=rng.normal(size=(nz,ny))
    while np.linalg.matrix_rank(J)<ny:
        J=rng.normal(size=(nz,ny))
    R=np.linalg.inv(J.T@J)@J.T
    # perturb reconstruction to make residual by using noisy R_bad
    Rbad=R + 0.05*rng.normal(size=R.shape)
    Lz=J@L
    Kz=Lz@Lz.T
    E=L-Rbad@J@L
    Ke=E@E.T
    Ky=L@L.T
    t=1.0
    bound=(1+t)*Rbad@Kz@Rbad.T + (1+1/t)*Ke
    rows.append({
        'trial':trial,
        'residual_norm':float(np.linalg.norm(E)),
        'min_eig_bound_minus_KY':eigmin(bound-Ky)
    })
pd.DataFrame(rows).to_csv(out/'defective_promotion_checks_step44.csv',index=False)

# Hidden-kernel public shadow overread: J forgets y2.
rows=[]
for k in np.linspace(1,50,50):
    Ky=np.diag([1.0,k])
    J=np.array([[1.0,0.0]])
    Kz=J@Ky@J.T
    rows.append({'hidden_capacity':float(k),'public_shadow_capacity':float(Kz[0,0]),'intrinsic_lambda_max':eigmax(Ky)})
pd.DataFrame(rows).to_csv(out/'hidden_kernel_shadow_overread_step44.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot([r['hidden_capacity'] for r in rows],[r['intrinsic_lambda_max'] for r in rows],label='intrinsic hidden direction')
plt.plot([r['hidden_capacity'] for r in rows],[r['public_shadow_capacity'] for r in rows],label='public shadow')
plt.xlabel('hidden native currency')
plt.ylabel('observed budget')
plt.title('Nonfaithful presentation hides needles')
plt.legend()
plt.tight_layout()
plt.savefig(out/'hidden_kernel_shadow_overread_step44.png',dpi=160)
plt.close()

print('done step44 checks')
