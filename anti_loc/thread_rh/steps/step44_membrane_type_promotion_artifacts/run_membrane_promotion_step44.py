import json, csv, math, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step44_type_promotion')
OUT.mkdir(parents=True, exist_ok=True)

def eigmax(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).max())

def psd_pass(K, Theta, tol=1e-10):
    return eigmax(K-Theta) <= tol

# Section countermodel: K=[[1,rho],[rho,1]], diagonal passes, global fails when rho>0.
rows=[]
rhos=np.linspace(0,0.99,100)
for rho in rhos:
    K=np.array([[1,rho],[rho,1.0]])
    Theta=np.eye(2)
    rows.append({
        'rho':rho,
        'diagonal_capacity_1':K[0,0],
        'diagonal_capacity_2':K[1,1],
        'full_lambda_max':eigmax(K),
        'global_violation':eigmax(K-Theta),
        'diagonal_passes': True,
        'full_passes': psd_pass(K,Theta)
    })
with open(OUT/'section_promotion_countermodel_step44.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(7,4.5))
plt.plot([r['rho'] for r in rows],[r['full_lambda_max'] for r in rows],label='full block max eigenvalue')
plt.axhline(1,linestyle='--',label='diagonal budget')
plt.xlabel('cross-section correlation rho')
plt.ylabel('budget eigenvalue')
plt.title('Section diagonals pass while cross-section recombination fails')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'section_promotion_countermodel_step44.png',dpi=180); plt.close()

# Bundle integrated vs uniform.
rows=[]
ns=np.arange(2,101)
for n in ns:
    weights=np.array([1-1/n,1/n])
    K_fibers=np.array([1.0,float(n)])
    integrated=float((weights*K_fibers).sum())
    uniform=float(K_fibers.max())
    rows.append({'n':int(n),'fiber_1_capacity':1.0,'fiber_2_capacity':float(n),'weight_fiber_2':1/n,'integrated_shadow':integrated,'uniform_budget_needed':uniform})
with open(OUT/'bundle_promotion_countermodel_step44.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(7,4.5))
plt.plot([r['n'] for r in rows],[r['integrated_shadow'] for r in rows],label='integrated/public shadow')
plt.plot([r['n'] for r in rows],[r['uniform_budget_needed'] for r in rows],label='uniform bundle budget')
plt.xlabel('n')
plt.ylabel('budget')
plt.yscale('log')
plt.title('Integrated bundle shadow does not promote to uniform membrane')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'bundle_promotion_countermodel_step44.png',dpi=180); plt.close()

# Protocol duplicate model with p protocols.
rows=[]
for p in range(1,51):
    K=np.ones((p,p))
    Theta=np.eye(p)
    rows.append({'protocol_count':p,'route_local_capacity':1.0,'stacked_lambda_max':eigmax(K),'global_violation':eigmax(K-Theta),'diagonal_passes':True,'full_passes':psd_pass(K,Theta)})
with open(OUT/'protocol_promotion_countermodel_step44.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(7,4.5))
plt.plot([r['protocol_count'] for r in rows],[r['stacked_lambda_max'] for r in rows],label='stacked protocol max eigenvalue')
plt.axhline(1,linestyle='--',label='route-local budget')
plt.xlabel('number of duplicated protocols')
plt.ylabel('budget eigenvalue')
plt.title('Route-local budgets do not promote to protocol-union membrane')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'protocol_promotion_countermodel_step44.png',dpi=180); plt.close()

# Defective promotion bound check random.
rng=np.random.default_rng(44)
rows=[]
for i in range(80):
    z=4; y=3
    A=rng.normal(size=(z,z)); Kz=A@A.T
    B=rng.normal(size=(z,z)); Thetaz=Kz + B@B.T + 0.5*np.eye(z)
    G=rng.normal(size=(z,y))
    R=rng.normal(size=(y,y)); E=0.05*(R@R.T)
    Ky=G.T@Kz@G + E
    Thetay=G.T@Thetaz@G + E + 0.01*np.eye(y)
    old_minus_new=Thetay-Ky
    rows.append({'trial':i,'lambda_max_Kz_minus_Thetaz':eigmax(Kz-Thetaz),'lambda_max_Ky_minus_Thetay':eigmax(Ky-Thetay),'min_eig_margin':float(np.linalg.eigvalsh((old_minus_new+old_minus_new.T)/2).min())})
with open(OUT/'defective_promotion_random_checks_step44.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# Gate table / theorem map / schema
schemas = {
  'step': 44,
  'name': 'Membrane Type Promotion Theorem',
  'core_bridge': 'K_Y <= G^* K_Z G + E_G',
  'promotion_condition': 'K_Z <= Theta_Z and G^*Theta_ZG + E_G <= Theta_Y',
  'types': ['intrinsic','sectioned','bundle_fiber','protocol_indexed','public_shadow'],
  'statuses': {
    'accepted_promotion': 'bridge exact or defective with budgeted residual',
    'local_only': 'typed membrane without gluing to intrinsic response space',
    'shadow_only': 'public or integrated shadow without faithful bridge',
    'support_only': 'diagnostic evidence without block currency domination',
    'overread': 'weaker membrane claimed as intrinsic without bridge'
  }
}
with open(OUT/'membrane_type_promotion_schema_step44.json','w') as f:
    json.dump(schemas,f,indent=2)

with open(OUT/'promotion_gate_table_step44.csv','w',newline='') as f:
    fields=['gate','required_record','failure_status','countermodel']
    rows=[
        {'gate':'section_gluing','required_record':'full section block K_sec and gluing map G_sec','failure_status':'local_only/overread','countermodel':'K=[[1,rho],[rho,1]] diagonal passes full fails'},
        {'gate':'bundle_uniformity','required_record':'uniform or block bundle budget plus gluing map','failure_status':'shadow_only','countermodel':'rare high-capacity fiber'},
        {'gate':'protocol_union','required_record':'stacked protocol block K and readout agreement','failure_status':'route_local_overread','countermodel':'duplicated protocols'},
        {'gate':'defect_budget','required_record':'E_G with G^*Theta_ZG+E_G <= Theta_Y','failure_status':'support_only/provisional','countermodel':'unbudgeted residual'},
        {'gate':'nonclaim','required_record':'explicit statement excluding cross-type recombinations if not native','failure_status':'smuggled_native_family','countermodel':'cross-section witness treated as absent'}]
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

with open(OUT/'theorem_map_step44.csv','w',newline='') as f:
    fields=['theorem','inputs','conclusion','role']
    rows=[
        {'theorem':'Exact type promotion','inputs':'K_Y=G^*K_ZG, K_Z<=Theta_Z, G^*Theta_ZG<=Theta_Y','conclusion':'K_Y<=Theta_Y','role':'promote typed membrane to intrinsic'},
        {'theorem':'Defective type promotion','inputs':'K_Y<=G^*K_ZG+E, K_Z<=Theta_Z, G^*Theta_ZG+E<=Theta_Y','conclusion':'K_Y<=Theta_Y','role':'promotion with residual budget'},
        {'theorem':'Sectioned promotion','inputs':'full section block matrix and section gluing','conclusion':'sectioned -> intrinsic','role':'blocks diagonal-only overread'},
        {'theorem':'Bundle promotion','inputs':'bundle block/uniform budget and fiber gluing','conclusion':'bundle -> intrinsic','role':'blocks integrated-shadow overread'},
        {'theorem':'Protocol promotion','inputs':'stacked protocol block and readout agreement','conclusion':'protocol-indexed -> intrinsic','role':'blocks route-local overread'},
        {'theorem':'Predictive promotion','inputs':'stagewise promotion bridges with uniform/summable defects','conclusion':'predictive intrinsic membrane','role':'stability across refinements'}]
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

# Summary markdown
summary = r'''# Step 44 — Membrane Type Promotion Theorem

This proof step formalizes when a weaker membrane type can be promoted to an intrinsic membrane.

## Core theorem

Let `Z` be a typed membrane response space and `Y` the intended intrinsic response space. A promotion bridge is a gluing map

```math
G:Y\to Z
```

with either exact currency identity

```math
K_Y = G^*K_ZG
```

or defective domination

```math
K_Y \preceq G^*K_ZG+E_G.
```

If

```math
K_Z\preceq \Theta_Z
```

and

```math
G^*\Theta_ZG+E_G\preceq\Theta_Y,
```

then

```math
K_Y\preceq\Theta_Y.
```

Thus typed membranes promote only through an audited bridge.

## Type-specific promotions

- Sectioned → intrinsic requires the full section block matrix, not only diagonal sections.
- Bundle/fiber → intrinsic requires uniform/block bundle control, not only an integrated shadow.
- Protocol-indexed → intrinsic requires the stacked protocol-union matrix and readout agreement, not route-local diagonals.
- Predictive promotion requires stagewise bridges and uniform or summably budgeted defects.

## Countermodels

1. Section diagonal bounds fail for `K=[[1,rho],[rho,1]]`.
2. Integrated bundle shadows fail when a rare fiber has large capacity.
3. Route-local protocol budgets fail for duplicated protocols.
4. Public-shadow success does not imply intrinsic success without bridge.

## Layman version

A local membrane can become a global membrane only if the local pieces are glued with the full price table. Checking each section, fiber, or protocol separately is not enough. The hidden danger is always a recombination across the pieces.
'''
with open(OUT/'step44_results_summary.md','w') as f:
    f.write(summary)
