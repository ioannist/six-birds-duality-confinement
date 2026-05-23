import numpy as np
import csv, os
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step71_weil_douglas')
np.random.seed(71)

def psd_sqrt(A, tol=1e-12):
    A = (A + A.T)/2
    w, V = np.linalg.eigh(A)
    w = np.maximum(w, 0)
    return V @ np.diag(np.sqrt(w)) @ V.T

def psd_inv_sqrt(A, tol=1e-10):
    A = (A + A.T)/2
    w, V = np.linalg.eigh(A)
    inv = np.zeros_like(w)
    inv[w > tol] = 1/np.sqrt(w[w > tol])
    return V @ np.diag(inv) @ V.T

def max_eig(A):
    return float(np.linalg.eigvalsh((A + A.T)/2).max())

def min_eig(A):
    return float(np.linalg.eigvalsh((A + A.T)/2).min())

# 1. Douglas checks: A <= K iff minimal contraction norm <=1
rows=[]
for n in [3,5,8,12]:
    for trial in range(20):
        B=np.random.randn(n,n)
        K=B@B.T + 0.5*np.eye(n)
        # Build A <= K by A = S K S, with contraction in K metric
        R=np.random.randn(n,n)
        U,_,Vt=np.linalg.svd(R, full_matrices=False)
        s=np.linspace(0.1,0.95,n)
        C=U@np.diag(s)@Vt
        Ks=psd_sqrt(K)
        A=Ks@C.T@C@Ks
        # minimal norm proxy K^{-1/2} A K^{-1/2}
        ratio=max_eig(psd_inv_sqrt(K)@A@psd_inv_sqrt(K))
        slack=min_eig(K-A)
        rows.append([n,trial,ratio,slack,'pass' if ratio <= 1+1e-8 and slack >= -1e-8 else 'fail'])
with open(OUT/'douglas_random_checks_step71.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['dim','trial','max_eig_K_inv_half_A','min_eig_K_minus_A','status']); wr.writerows(rows)

# 2. Trace equality does not imply Loewner domination
rows=[]
for r in [1.05,1.25,1.5,2,5,10]:
    A=np.diag([r, 1/r])
    K=np.eye(2)
    rows.append([r, np.trace(A), np.trace(K), min_eig(K-A), max_eig(A-K), 'trace_equal_but_not_dominated' if min_eig(K-A)<0 else 'dominated'])
with open(OUT/'trace_not_domination_countermodel_step71.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['r','trace_A','trace_K','min_eig_K_minus_A','max_eig_A_minus_K','status']); wr.writerows(rows)

# 3. Four feature decomposition: PSD components concatenate; signed components require repair
rows=[]
for trial in range(50):
    n=5
    comps=[]
    for _ in range(4):
        X=np.random.randn(n,n)
        comps.append(X@X.T)
    K=sum(comps)
    A=0.4*K
    slack=min_eig(K-A)
    rows.append([trial, min_eig(K), min_eig(A), slack, 'accepted_positive_features' if slack>=-1e-9 else 'failed'])
with open(OUT/'four_feature_positive_decomposition_step71.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['trial','min_eig_K','min_eig_A','min_eig_K_minus_A','status']); wr.writerows(rows)

# Signed components: sum can be PSD or not; individual signed terms are not feature maps.
rows=[]
for a in [0.0,0.1,0.25,0.5,0.75,1.0,1.25]:
    P=np.diag([2.0,1.0])
    N=np.array([[0.0,0.0],[0.0,a]])
    K=P-N
    A=np.diag([1.0,0.25])
    rows.append([a,min_eig(K),min_eig(K-A),'accepted_total_psd' if min_eig(K-A)>=-1e-9 else 'defect_needed'])
with open(OUT/'signed_component_repair_step71.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['negative_component_strength','min_eig_total_K','min_eig_K_minus_A','status']); wr.writerows(rows)

print('wrote step71 checks')
