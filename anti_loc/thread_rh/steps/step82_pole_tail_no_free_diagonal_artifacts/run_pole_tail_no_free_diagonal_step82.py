import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step82_pole_tail_no_free_diagonal')
OUT.mkdir(exist_ok=True)

# 1. finite rank pole cannot dominate identity as dimension grows
rows=[]
rank=5
rng=np.random.default_rng(82)
for N in [8,12,16,24,32,48,64,96,128]:
    U,_=np.linalg.qr(rng.normal(size=(N,rank)))
    vals=np.linspace(1.0,2.0,rank)
    P=U@np.diag(vals)@U.T
    eig=np.linalg.eigvalsh(P)
    rows.append({'N':N,'rank':rank,'min_eig':eig[0],'max_eig':eig[-1],'num_zero_like':int(np.sum(eig < 1e-10))})
pd.DataFrame(rows).to_csv(OUT/'finite_rank_no_diagonal_step82.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot([r['N'] for r in rows],[r['min_eig'] for r in rows],marker='o')
plt.xlabel('dimension N')
plt.ylabel('min eigenvalue')
plt.title('Finite-rank pole feature cannot pay full diagonal')
plt.tight_layout(); plt.savefig(OUT/'finite_rank_no_diagonal_step82.png',dpi=180); plt.close()

# 2. pole+tail lower frame
rows=[]; N=80; rank=5
U,_=np.linalg.qr(rng.normal(size=(N,rank)))
Pproj=U@U.T; Qproj=np.eye(N)-Pproj
for delta_tail in [0,1e-4,1e-3,1e-2,0.05,0.1,0.25,0.5,1.0]:
    K=Pproj+delta_tail*Qproj
    eig=np.linalg.eigvalsh(K)
    rows.append({'delta_tail':delta_tail,'min_eig':eig[0],'predicted_min':min(1.0,delta_tail),'max_eig':eig[-1]})
pd.DataFrame(rows).to_csv(OUT/'tail_lower_frame_payment_step82.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot([r['delta_tail'] for r in rows],[r['min_eig'] for r in rows],marker='o',label='actual min eig')
plt.plot([r['delta_tail'] for r in rows],[r['predicted_min'] for r in rows],linestyle='--',label='predicted')
plt.xscale('symlog',linthresh=1e-4)
plt.xlabel('tail lower-frame strength')
plt.ylabel('combined lower bound')
plt.title('Tail/coercive source pays infinite complement')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'tail_lower_frame_payment_step82.png',dpi=180); plt.close()

# 3. diagonal growth obstruction using sieve for von Mangoldt
def von_mangoldt_array(N):
    lam=np.zeros(N+1)
    isprime=np.ones(N+1,dtype=bool); isprime[:2]=False
    for p in range(2,N+1):
        if isprime[p]:
            for m in range(p*p,N+1,p):
                isprime[m]=False
            pk=p
            while pk<=N:
                lam[pk]=np.log(p)
                if pk> N//p: break
                pk*=p
    return lam
maxL=12
maxN=int(np.exp(maxL))+1
lam=von_mangoldt_array(maxN)
logs=np.log(np.arange(maxN+1,dtype=float)); logs[0]=0
rows=[]
for L in [3,4,5,6,8,10,12]:
    maxn=int(np.exp(L))
    n=np.arange(2,maxn+1)
    a=logs[n]
    alpha=np.maximum(0.0,1-a/L)**2
    total=float(np.sum(lam[n]/np.sqrt(n)*alpha))
    dpr=2*total
    rows.append({'L':L,'sum_w':total,'d_pr':dpr,'lower_norm_bound':dpr})
pd.DataFrame(rows).to_csv(OUT/'prime_diagonal_growth_obstruction_step82.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot([r['L'] for r in rows],[r['d_pr'] for r in rows],marker='o')
plt.xlabel('prime cutoff L')
plt.ylabel('d_pr = 2 sum w_a')
plt.title('Separated prime diagonal repair grows with cutoff')
plt.tight_layout(); plt.savefig(OUT/'prime_diagonal_growth_obstruction_step82.png',dpi=180); plt.close()

# 4. paired singular kernel: truncated diagonal diverges while paired form finite
rows=[]
for eps in np.logspace(-6,-1,20):
    separated_diag=0.5*np.log(1/eps)
    paired_local=0.25*(1-eps**2)
    rows.append({'epsilon':eps,'separated_diagonal':separated_diag,'paired_local_model':paired_local})
pd.DataFrame(rows).to_csv(OUT/'paired_singular_kernel_step82.csv',index=False)
plt.figure(figsize=(6,4))
plt.plot([r['epsilon'] for r in rows],[r['separated_diagonal'] for r in rows],marker='o',label='separated diagonal')
plt.plot([r['epsilon'] for r in rows],[r['paired_local_model'] for r in rows],marker='s',label='paired difference model')
plt.xscale('log'); plt.gca().invert_xaxis()
plt.xlabel('near-zero cutoff epsilon')
plt.ylabel('size')
plt.title('Singular paired form: finite pair, divergent diagonal')
plt.legend(); plt.tight_layout(); plt.savefig(OUT/'paired_singular_kernel_step82.png',dpi=180); plt.close()
print('done')
