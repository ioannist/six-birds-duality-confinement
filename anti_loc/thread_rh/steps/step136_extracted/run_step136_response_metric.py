import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json, math, os
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step136_response_metric_incidence')
out.mkdir(parents=True, exist_ok=True)

# Simple prime generator
def primes_upto(n):
    sieve = np.ones(n+1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n**0.5)+1):
        if sieve[p]:
            sieve[p*p:n+1:p] = False
    return np.nonzero(sieve)[0].tolist()

# One-prime incidence singular value for H_sigma metric where weight of p-included coordinate is p^-sigma.
def sigma_p(p, sigma):
    eps = p**(-sigma/2.0)
    lam_max = 1 + eps*eps/2 + eps*math.sqrt(1 + eps*eps/4)
    lam_min = 1 + eps*eps/2 - eps*math.sqrt(1 + eps*eps/4)
    return math.sqrt(lam_max), math.sqrt(lam_min)

phi = (1+5**0.5)/2
ys = list(range(10, 2001, 10))
sigmas = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
rows=[]
for y in ys:
    ps = primes_upto(y)
    k = len(ps)
    raw_log = k * math.log(phi)
    sum_p_inv_sqrt = sum(p**-0.5 for p in ps)
    sum_p_inv = sum(p**-1 for p in ps)
    row = {'y':y,'num_primes':k,'raw_log_norm':raw_log,'sum_p_inv_sqrt':sum_p_inv_sqrt,'sum_p_inv':sum_p_inv}
    for sigma in sigmas:
        lognorm = 0.0
        loginv = 0.0
        for p in ps:
            smax,smin = sigma_p(p, sigma)
            lognorm += math.log(smax)
            loginv += -math.log(smin) # condition contribution maybe same for det 1? For triangular det 1 singulars reciprocal.
        row[f'log_norm_sigma_{sigma}'] = lognorm
        row[f'norm_sigma_{sigma}'] = math.exp(min(lognorm, 700))
    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(out/'incidence_metric_norms_step136.csv', index=False)

# one-prime singular values table
p_list = primes_upto(200)
rows2=[]
for p in p_list:
    row={'p':p}
    for sigma in sigmas:
        smax,smin=sigma_p(p,sigma)
        row[f'smax_sigma_{sigma}']=smax
        row[f'smin_sigma_{sigma}']=smin
        row[f'eps_sigma_{sigma}']=p**(-sigma/2.0)
    rows2.append(row)
pd.DataFrame(rows2).to_csv(out/'one_prime_singular_values_step136.csv', index=False)

# Tail competition scenario: seed tail = exp(-c sqrt(y)/log y) or exp(-c y/log y) compare post-Z tail.
scen=[]
for y in ys:
    ps=primes_upto(y)
    log_norm_H1=sum(math.log(sigma_p(p,1.0)[0]) for p in ps)
    log_norm_raw=len(ps)*math.log(phi)
    scale_sqrt = math.sqrt(y)/max(math.log(y),1)
    scale_prime_count = y/max(math.log(y),1)
    for c in [0.5,1.0,2.0,4.0]:
        log_seed = -c*scale_sqrt
        scen.append({'y':y,'tail_model':'exp(-c sqrt(y)/log y)','c':c,'log_seed_tail':log_seed,'log_after_H1':log_seed+log_norm_H1,'log_after_raw':log_seed+log_norm_raw,'after_H1':math.exp(min(log_seed+log_norm_H1,700)),'after_raw':math.exp(min(log_seed+log_norm_raw,700))})
    for c in [0.05,0.1,0.2,0.5]:
        log_seed = -c*scale_prime_count
        scen.append({'y':y,'tail_model':'exp(-c y/log y)','c':c,'log_seed_tail':log_seed,'log_after_H1':log_seed+log_norm_H1,'log_after_raw':log_seed+log_norm_raw,'after_H1':math.exp(min(log_seed+log_norm_H1,700)),'after_raw':math.exp(min(log_seed+log_norm_raw,700))})

pd.DataFrame(scen).to_csv(out/'tail_amplification_scenarios_step136.csv', index=False)

# Effective source strength with delta post-incidence and gamma = log q, q = exp(omega log T maybe). Model gamma=logQ and delta=min(0.99, after_H1).
rows3=[]
for y in ys:
    log_norm_H1=float(df.loc[df.y==y,'log_norm_sigma_1.0'].iloc[0])
    log_norm_raw=float(df.loc[df.y==y,'raw_log_norm'].iloc[0])
    for gamma_scale in [1,2,5,10]:
        gamma=gamma_scale*math.log(max(y,3))
        for c in [1.0,2.0,4.0]:
            log_seed=-c*math.sqrt(y)/max(math.log(y),1)
            delta_H1=min(0.999999, math.exp(min(log_seed+log_norm_H1, 0))) if log_seed+log_norm_H1<0 else 0.999999
            delta_raw=min(0.999999, math.exp(min(log_seed+log_norm_raw, 0))) if log_seed+log_norm_raw<0 else 0.999999
            rows3.append({'y':y,'gamma_scale':gamma_scale,'c':c,'gamma':gamma,'delta_H1':delta_H1,'delta_raw':delta_raw,'effective_H1':gamma*(1-delta_H1**2),'effective_raw':gamma*(1-delta_raw**2)})
pd.DataFrame(rows3).to_csv(out/'restricted_source_strength_metric_step136.csv', index=False)

# Plots.
plt.figure(figsize=(8,5))
plt.plot(df['y'], df['raw_log_norm'], label='raw ℓ²: log ||Z|| = π(y) log φ')
for sigma in [0.5,1.0,1.5,2.0]:
    plt.plot(df['y'], df[f'log_norm_sigma_{sigma}'], label=f'H_σ, σ={sigma}')
plt.xlabel('prime cutoff y')
plt.ylabel('log incidence norm')
plt.title('Response metric reduces incidence amplification')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'incidence_metric_norms_step136.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
pdf = pd.DataFrame(rows2)
for sigma in [0.5,1.0,1.5,2.0]:
    plt.plot(pdf['p'], pdf[f'smax_sigma_{sigma}'], label=f'σ={sigma}')
plt.axhline(phi, linestyle='--', label='raw one-prime φ')
plt.xlabel('prime p')
plt.ylabel('one-prime singular value')
plt.title('One-prime incidence singular value under H_σ')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'one_prime_singular_values_step136.png', dpi=180)
plt.close()

# Tail amplification plot for c=2 sqrt model
sdf = pd.DataFrame(scen)
sub = sdf[(sdf['tail_model']=='exp(-c sqrt(y)/log y)') & (sdf['c']==2.0)]
plt.figure(figsize=(8,5))
plt.plot(sub['y'], sub['log_seed_tail'], label='seed log tail')
plt.plot(sub['y'], sub['log_after_H1'], label='after H1 incidence')
plt.plot(sub['y'], sub['log_after_raw'], label='after raw incidence')
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('prime cutoff y')
plt.ylabel('log tail / amplified tail')
plt.title('Seed tail must beat incidence amplification')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'tail_amplification_step136.png', dpi=180)
plt.close()

# effective source strength plot for gamma_scale=5, c=2
edf=pd.DataFrame(rows3)
sub=edf[(edf.gamma_scale==5)&(edf.c==2.0)]
plt.figure(figsize=(8,5))
plt.plot(sub['y'], sub['effective_H1'], label='effective source with H1 metric')
plt.plot(sub['y'], sub['effective_raw'], label='effective source with raw metric')
plt.xlabel('prime cutoff y')
plt.ylabel('γ(1-δ²)')
plt.title('Metric-normalized restricted source strength')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'restricted_source_strength_metric_step136.png', dpi=180)
plt.close()

# Check JSON for formula validation numerical one-prime exact
checks=[]
for p in [2,3,5,11,101]:
    for sigma in [0,1,2]:
        eps=p**(-sigma/2) if sigma!=0 else 1.0
        A=np.array([[1,0],[eps,1.0]])
        sv=np.linalg.svd(A, compute_uv=False)
        smax,smin=sigma_p(p,sigma)
        checks.append({'p':p,'sigma':sigma,'svd_max':float(sv[0]),'formula_max':smax,'abs_err_max':abs(sv[0]-smax),'svd_min':float(sv[1]),'formula_min':smin,'abs_err_min':abs(sv[1]-smin)})
with open(out/'formula_checks_step136.json','w') as f:
    json.dump({'one_prime_formula_checks':checks, 'max_abs_error':max(max(c['abs_err_max'],c['abs_err_min']) for c in checks)}, f, indent=2)

print('created', len(list(out.iterdir())), 'files in', out)
