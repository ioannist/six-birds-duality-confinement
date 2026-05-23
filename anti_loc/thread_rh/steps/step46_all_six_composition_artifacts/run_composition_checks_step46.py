import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/anti_localization_step46_composition')
np.random.seed(46)

def psd_sqrt(A):
    w,V=np.linalg.eigh((A+A.T)/2)
    return V @ np.diag(np.sqrt(np.maximum(w,0))) @ V.T

def psd_inv_sqrt(A, tol=1e-10):
    w,V=np.linalg.eigh((A+A.T)/2)
    return V @ np.diag([1/np.sqrt(x) if x>tol else 0 for x in w]) @ V.T

def rand_spd(n, floor=0.5):
    A=np.random.randn(n,n)
    return A.T@A+floor*np.eye(n)

def k_matrix(C,L):
    return L @ np.linalg.pinv(C) @ L.T

def min_eig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).min())

def max_eig(A):
    return float(np.linalg.eigvalsh((A+A.T)/2).max())

# Exact composition checks
rows=[]
for trial in range(60):
    n0,n1,n2=5,4,3
    y0,y1,y2=3,3,3
    C0=rand_spd(n0, floor=1.0)
    L0=np.random.randn(y0,n0)
    P01=np.random.randn(n0,n1)/np.sqrt(n0)
    A01=np.random.randn(y1,y0)/np.sqrt(y0)
    P12=np.random.randn(n1,n2)/np.sqrt(n1)
    A12=np.random.randn(y2,y1)/np.sqrt(y1)
    C1=P01.T@C0@P01 + rand_spd(n1, floor=0.4)
    L1=A01@L0@P01
    C2=P12.T@C1@P12 + rand_spd(n2, floor=0.4)
    L2=A12@L1@P12
    K0=k_matrix(C0,L0)
    K1=k_matrix(C1,L1)
    K2=k_matrix(C2,L2)
    B1=A01@K0@A01.T-K1
    A02=A12@A01
    B2=A02@K0@A02.T-K2
    rows.append({
        'trial':trial,
        'min_eig_AK0A_minus_K1':min_eig(B1),
        'min_eig_composed_AK0A_minus_K2':min_eig(B2),
        'trace_K0':np.trace(K0),
        'trace_K2':np.trace(K2)
    })
pd.DataFrame(rows).to_csv(OUT/'exact_composition_checks_step46.csv', index=False)

# Defective composition checks with t values
rows=[]
for trial in range(50):
    n0,n1,n2=5,4,3
    y0,y1,y2=3,3,3
    C0=rand_spd(n0, floor=1.0)
    L0=np.random.randn(y0,n0)
    P01=np.random.randn(n0,n1)/np.sqrt(n0)
    A01=np.random.randn(y1,y0)/np.sqrt(y0)
    R01=0.08*np.random.randn(y1,n1)
    C1=P01.T@C0@P01 + rand_spd(n1, floor=0.8)
    L1=A01@L0@P01 + R01
    P12=np.random.randn(n1,n2)/np.sqrt(n1)
    A12=np.random.randn(y2,y1)/np.sqrt(y1)
    R12=0.08*np.random.randn(y2,n2)
    C2=P12.T@C1@P12 + rand_spd(n2, floor=0.8)
    L2=A12@L1@P12 + R12
    K0=k_matrix(C0,L0)
    K2=k_matrix(C2,L2)
    E01=R01@np.linalg.pinv(C1)@R01.T
    E12=R12@np.linalg.pinv(C2)@R12.T
    t=0.5; s=0.7
    bound=(1+s)*(1+t)*(A12@A01@K0@(A12@A01).T) + (1+s)*(1+1/t)*(A12@E01@A12.T) + (1+1/s)*E12
    rows.append({
        'trial':trial,
        'min_eig_bound_minus_actual':min_eig(bound-K2),
        'trace_actual_K2':np.trace(K2),
        'trace_bound':np.trace(bound),
        'trace_residual_01':np.trace(E01),
        'trace_residual_12':np.trace(E12)
    })
pd.DataFrame(rows).to_csv(OUT/'defective_composition_checks_step46.csv', index=False)

# Chain propagation common-space
rows=[]
K=np.array([[0.20,0.03],[0.03,0.10]])
Theta=np.array([[1.0,0.0],[0.0,0.8]])
Pprod=1.0
Dsum=np.zeros((2,2))
for j in range(1,81):
    eps=0.015/(j**1.4)
    d=0.003/(j**1.5)
    D=d*np.array([[1.0,0.2],[0.2,0.8]])
    K=(1+eps)*K+D
    Pprod*=1+eps
    Dsum+=D
    rows.append({
        'stage':j,
        'epsilon':eps,
        'defect_trace':np.trace(D),
        'lambda_max_K':max_eig(K),
        'budget_slack_min_eig':min_eig(Theta-K),
        'Pprod':Pprod,
        'Dsum_trace':np.trace(Dsum)
    })
chain_df=pd.DataFrame(rows)
chain_df.to_csv(OUT/'chain_defect_propagation_step46.csv', index=False)

plt.figure(figsize=(7,4))
plt.plot(chain_df['stage'], chain_df['lambda_max_K'], label='lambda_max(K_j)')
plt.plot(chain_df['stage'], [max_eig(Theta)]*len(chain_df), linestyle='--', label='budget max eig')
plt.xlabel('stage')
plt.ylabel('eigenvalue')
plt.title('Step 46: summable defect propagation remains within budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'chain_defect_propagation_step46.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4))
plt.plot(chain_df['stage'], chain_df['budget_slack_min_eig'])
plt.xlabel('stage')
plt.ylabel('min eig(Theta - K_j)')
plt.title('Step 46: propagated membrane slack')
plt.tight_layout()
plt.savefig(OUT/'chain_membrane_slack_step46.png', dpi=180)
plt.close()

# Countermodels for missing channels
counter=[]
# P1 gauge slow mode after rotation
eps=1e-4
C=np.diag([eps,1.0])
L_before=np.array([[0.0,1.0]])
L_after=np.array([[1.0,0.0]])
counter.append({'missing_channel':'P1 rewrite/gauge','model':'slow mode hidden by gauge then exposed','claimed_visible_capacity':float(k_matrix(C,L_before)[0,0]),'lawful_capacity_after_missing_record':float(k_matrix(C,L_after)[0,0]),'violation_factor':float(k_matrix(C,L_after)[0,0]/max(k_matrix(C,L_before)[0,0],1e-12))})
# P2 cancellation
for eps2 in [1e-1,1e-2,1e-3]:
    psi_plus=np.array([np.sqrt(1-eps2**2),eps2])
    psi_minus=np.array([np.sqrt(1-eps2**2),-eps2])
    Gamma=np.stack([psi_plus,psi_minus],axis=1)
    Cg=Gamma.T@Gamma
    L=np.array([[0.0,1.0]])
    Lg=L@Gamma
    actual=float(Lg@np.linalg.pinv(Cg)@Lg.T)
    diag=float(np.sum((Lg.flatten())**2))
    counter.append({'missing_channel':'P2 feasibility/frame','model':f'cancellation channels eps={eps2}', 'claimed_visible_capacity':diag,'lawful_capacity_after_missing_record':actual,'violation_factor':actual/max(diag,1e-12)})
# P3 duplicated routes
K=np.array([[1,1],[1,1]], dtype=float)
counter.append({'missing_channel':'P3 route/protocol','model':'two duplicated protocol readouts','claimed_visible_capacity':1.0,'lawful_capacity_after_missing_record':max_eig(K),'violation_factor':max_eig(K)})
# P4 predictive
for n in [10,100,1000]:
    counter.append({'missing_channel':'P4 staging/refinement','model':f'K_j=diag(1,j), j={n}','claimed_visible_capacity':1.0,'lawful_capacity_after_missing_record':float(n),'violation_factor':float(n)})
# P5 public shadow hidden direction
for M in [10,100,1000]:
    counter.append({'missing_channel':'P5 packaging/witness','model':f'public projection forgets hidden capacity {M}','claimed_visible_capacity':1.0,'lawful_capacity_after_missing_record':float(M),'violation_factor':float(M)})
# P6 diagonal audit misses recombination
rho=0.9
K=np.array([[1,rho],[rho,1]])
counter.append({'missing_channel':'P6 audit/currency','model':'diagonal-only audit misses off-diagonal recombination','claimed_visible_capacity':1.0,'lawful_capacity_after_missing_record':max_eig(K),'violation_factor':max_eig(K)})
cmdf=pd.DataFrame(counter)
cmdf.to_csv(OUT/'composition_channel_countermodels_step46.csv', index=False)

plt.figure(figsize=(8,4.5))
labels=cmdf['missing_channel']
vals=cmdf['violation_factor']
plt.bar(range(len(vals)), vals)
plt.yscale('log')
plt.xticks(range(len(vals)), labels, rotation=60, ha='right')
plt.ylabel('violation factor (log scale)')
plt.title('Step 46: omitting any channel enables an overclaim witness')
plt.tight_layout()
plt.savefig(OUT/'composition_channel_countermodels_step46.png', dpi=180)
plt.close()
