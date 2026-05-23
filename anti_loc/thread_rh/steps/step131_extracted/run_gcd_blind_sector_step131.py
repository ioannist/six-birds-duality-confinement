import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json, math, zipfile

out = Path('/mnt/data/rh_membrane_step131_gcd_blind_sector')
out.mkdir(parents=True, exist_ok=True)

def primes_first(k):
    ps=[]; n=2
    while len(ps)<k:
        ok=True
        for p in ps:
            if p*p>n: break
            if n%p==0: ok=False; break
        if ok: ps.append(n)
        n+=1
    return np.array(ps, dtype=float)

def fwht(a):
    a = np.array(a, dtype=float).copy()
    n = a.shape[0]
    h=1
    while h<n:
        for i in range(0,n,2*h):
            x=a[i:i+h].copy(); y=a[i+h:i+2*h].copy()
            a[i:i+h]=x+y
            a[i+h:i+2*h]=x-y
        h*=2
    return a/np.sqrt(n)

def fast_zeta_subset(b, k):
    a=np.array(b,dtype=float).copy()
    n=1<<k
    for i in range(k):
        bit=1<<i
        for mask in range(n):
            if mask & bit:
                a[mask]+=a[mask^bit]
    return a

def popcounts(k):
    n=1<<k
    return np.array([m.bit_count() for m in range(n)])

def eigvals_gcd_log(k, logq=80.0):
    ps=primes_first(k)
    n=1<<k
    vals=[]
    negcounts=[]
    for mask in range(n):
        lam=1.0
        deriv_log_sum=0.0
        for i,p in enumerate(ps):
            r=p**-0.5
            sign=-1.0 if (mask>>i)&1 else 1.0
            local=1.0+sign*r
            lam*=local
            deriv_log_sum += (-sign*r*np.log(p))/local
        kappa=lam*(logq + deriv_log_sum)
        vals.append(kappa)
        negcounts.append(mask.bit_count())
    return np.array(vals), np.array(negcounts)

def blind_project_fraction(a, eigvals, bottom_frac=0.10):
    coeff=fwht(a)
    n=len(a)
    idx=np.argsort(eigvals)[:max(1,int(bottom_frac*n))]
    total=np.sum(coeff**2)
    return float(np.sum(coeff[idx]**2)/total), coeff, idx

def allminus_projection_formula_check(k, seed):
    a=fast_zeta_subset(seed,k)
    coeff=fwht(a)
    allminus=(1<<k)-1
    # FWHT coefficient allminus equals 2^{-k/2} sum_mask (-1)^{popcount(mask)} a[mask]
    top=seed[allminus]
    predicted=(((-1)**k)*top)/np.sqrt(1<<k)
    return coeff[allminus], predicted

rng=np.random.default_rng(20260514)
records=[]
blind_records=[]
exact_records=[]
xi_records=[]
ks=range(3,11)
for k in ks:
    n=1<<k
    pc=popcounts(k)
    logq=80.0 + 5*k
    eig, neg=eigvals_gcd_log(k, logq=logq)
    eig_norm=eig/logq
    for mask in range(n):
        records.append({'k':k,'dim':n,'mask':mask,'neg_count':int(neg[mask]),'eig':eig[mask],'eig_over_logq':eig_norm[mask]})
    # Seeds: raw coefficient vector, zeta convolution of smooth seed, high-divisibility suppressed seed
    raw=rng.normal(size=n)
    raw/=np.linalg.norm(raw)
    smooth_seed=rng.normal(size=n)*(0.35**pc)
    zeta_smooth=fast_zeta_subset(smooth_seed,k)
    zeta_smooth/=np.linalg.norm(zeta_smooth)
    suppressed_seed=rng.normal(size=n)*(0.12**pc)*(1.0/(1+pc)**2)
    zeta_supp=fast_zeta_subset(suppressed_seed,k)
    zeta_supp/=np.linalg.norm(zeta_supp)
    # ideal seed with top-degree coefficients explicitly zeroed for high popcount
    band_seed=rng.normal(size=n)*(0.5**pc)
    band_seed[pc>max(1,k//2)]=0.0
    zeta_band=fast_zeta_subset(band_seed,k)
    zeta_band/=np.linalg.norm(zeta_band)
    scenarios={'raw':raw,'zeta_smooth_seed':zeta_smooth,'zeta_high_div_suppressed_seed':zeta_supp,'zeta_bandlimited_seed':zeta_band}
    for name,a in scenarios.items():
        frac, coeff, idx=blind_project_fraction(a,eig,bottom_frac=0.10)
        allminus=(1<<k)-1
        allminus_frac=float(coeff[allminus]**2/np.sum(coeff**2))
        blind_records.append({'k':k,'dim':n,'scenario':name,'blind_fraction_bottom10':frac,'allminus_fraction':allminus_frac,'min_eig_over_logq':float(eig_norm.min()),'median_eig_over_logq':float(np.median(eig_norm))})
    # formula checks for zeta convolution all-minus
    for trial in range(12):
        seed=rng.normal(size=n)*(0.3**pc)
        coeff, pred=allminus_projection_formula_check(k,seed)
        exact_records.append({'k':k,'trial':trial,'fwht_allminus':coeff,'predicted_top_seed':pred,'abs_error':abs(coeff-pred)})
    # Xi_GCD proxy: residual map image dimension r with zeta convolution seed columns; compute max blind singular overlap
    r=min(8,n//4)
    cols=[]
    for j in range(r):
        seed=rng.normal(size=n)*(0.25**pc)
        if j%2==0:
            seed[pc>k//2]=0.0
        a=fast_zeta_subset(seed,k)
        cols.append(a)
    M=np.stack(cols,axis=1)
    # orthonormalize image columns (domain Gram)
    G=M.T@M
    # avoid singular
    w,V=np.linalg.eigh(G)
    keep=w>1e-10
    Q=M@V[:,keep]@np.diag(1/np.sqrt(w[keep]))
    _,_,blind_idx=blind_project_fraction(np.ones(n)/np.sqrt(n),eig,bottom_frac=0.10)
    # Projection onto blind sector using hadamard basis: P = H^T diag(blind) H; compute Q^T P Q
    # Use fwht on columns; blind energy matrix = C_blind^T C_blind
    C=np.stack([fwht(Q[:,j]) for j in range(Q.shape[1])],axis=1)
    X=C[blind_idx,:].T@C[blind_idx,:]
    xi_norm=float(np.linalg.eigvalsh(X).max()) if X.size else 0.0
    xi_trace=float(np.trace(X)) if X.size else 0.0
    xi_records.append({'k':k,'dim':n,'domain_dim':int(Q.shape[1]),'xi_gcd_operator_norm':xi_norm,'xi_gcd_trace':xi_trace,'blind_rank':int(len(blind_idx))})

pd.DataFrame(records).to_csv(out/'boolean_cube_eigenvalues_step131.csv',index=False)
pd.DataFrame(blind_records).to_csv(out/'blind_overlap_scenarios_step131.csv',index=False)
pd.DataFrame(exact_records).to_csv(out/'mobius_annihilation_checks_step131.csv',index=False)
pd.DataFrame(xi_records).to_csv(out/'xi_gcd_visibility_step131.csv',index=False)

# Plots
rec=pd.DataFrame(records)
plt.figure(figsize=(7,4.5))
for k in [4,6,8,10]:
    sub=rec[rec.k==k].sort_values('eig_over_logq')
    plt.plot(np.arange(len(sub))/len(sub), sub['eig_over_logq'].values, label=f'k={k}')
plt.yscale('log')
plt.xlabel('quantile in Boolean sign basis')
plt.ylabel('eigenvalue / log q')
plt.title('GCD-log kernel near-null spectrum on squarefree cubes')
plt.legend()
plt.tight_layout()
plt.savefig(out/'gcd_blind_eigenvalues_step131.png',dpi=180)
plt.close()

blind=pd.DataFrame(blind_records)
plt.figure(figsize=(7,4.5))
for name in blind['scenario'].unique():
    sub=blind[blind.scenario==name]
    plt.plot(sub.k, sub.blind_fraction_bottom10, marker='o', label=name)
plt.yscale('log')
plt.xlabel('number of small primes in squarefree cube')
plt.ylabel('fraction in bottom 10% GCD-log eigenspaces')
plt.title('Residual coefficient overlap with GCD-log blind sector')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'blind_overlap_scenarios_step131.png',dpi=180)
plt.close()

exact=pd.DataFrame(exact_records)
plt.figure(figsize=(7,4.5))
err=exact.groupby('k')['abs_error'].max().reset_index()
plt.plot(err.k, err.abs_error, marker='o')
plt.yscale('log')
plt.xlabel('k')
plt.ylabel('max |FWHT all-minus - predicted top seed|')
plt.title('Möbius annihilation identity for zeta convolution')
plt.tight_layout()
plt.savefig(out/'mobius_annihilation_step131.png',dpi=180)
plt.close()

xi=pd.DataFrame(xi_records)
plt.figure(figsize=(7,4.5))
plt.plot(xi.k, xi.xi_gcd_operator_norm, marker='o', label='operator norm')
plt.plot(xi.k, xi.xi_gcd_trace/xi.domain_dim, marker='s', label='trace/domain dim')
plt.yscale('log')
plt.xlabel('k')
plt.ylabel('blind-sector residual')
plt.title('Finite Xi_GCD proxy for residual coefficient image')
plt.legend()
plt.tight_layout()
plt.savefig(out/'xi_gcd_visibility_step131.png',dpi=180)
plt.close()

summary={
 'max_mobius_identity_error': float(pd.DataFrame(exact_records)['abs_error'].max()),
 'best_last_k_blind_fraction': blind[blind.k==max(ks)].sort_values('blind_fraction_bottom10').iloc[0].to_dict(),
 'xi_last': xi[xi.k==max(ks)].iloc[0].to_dict()
}
with open(out/'finite_model_sanity_step131.json','w') as f: json.dump(summary,f,indent=2)
