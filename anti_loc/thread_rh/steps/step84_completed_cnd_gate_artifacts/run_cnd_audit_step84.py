import json, math, csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step84_cnd_audit')
OUT.mkdir(parents=True, exist_ok=True)

# Basic arithmetic weights for a toy prime-power cutoff.
def von_mangoldt(n: int) -> float:
    # Return log p if n is a prime power p^k, else 0.
    m = n
    # trial factorization small n
    factors = []
    d = 2
    while d*d <= m:
        count = 0
        while m % d == 0:
            m //= d
            count += 1
        if count:
            factors.append((d,count))
        d += 1 if d == 2 else 2
    if m > 1:
        factors.append((m,1))
    if len(factors) == 1:
        return math.log(factors[0][0])
    return 0.0

def prime_shift_weights(L=8.0):
    weights=[]
    nmax=int(math.floor(math.exp(L)))
    for n in range(2,nmax+1):
        lam=von_mangoldt(n)
        if lam<=0: continue
        a=math.log(n)
        alpha=max(0.0, 1.0 - a/L)**2
        if alpha==0: continue
        w=lam/math.sqrt(n)*alpha
        if w>0: weights.append((a,w,n))
    return weights

def psi_from_discrete(weights, xi):
    xi=np.asarray(xi)
    val=np.zeros_like(xi,dtype=float)
    for a,w,*_ in weights:
        val += 2*w*(1-np.cos(a*xi))
    return val

# Gamma symbol using numerical quadrature over t in [eps,T].
def gamma_kernel(t):
    return 0.5*np.exp(-t/4.0)/(1-np.exp(-t))

def psi_gamma_grid(xi, eps=1e-5, T=80.0, N=50000):
    # integrate gamma feature: int kappa(t)(1-cos(xi*t/2))*2? Need consistent paired feature.
    # In previous convention Psi_gamma = 1/2 int e^{-t/4}/(1-e^{-t})(1-cos(xi*t/2)) dt.
    # That equals int kappa(t)(1-cos(...)) dt where kappa=.5*...
    t=np.linspace(eps,T,N)
    k=gamma_kernel(t)
    xi=np.asarray(xi)
    # chunk to avoid memory blow up
    res=[]
    for x in xi:
        res.append(np.trapz(k*(1-np.cos(x*t/2.0)),t))
    return np.array(res)

# CND matrix check: for a symmetric function psi on R with psi(0)=0, psi is CND if
# c^T [psi(x_i-x_j)] c <=0 for all sum(c)=0. We sample random x/c.
def cnd_check(psi_func, trials=200, m=8, seed=0):
    rng=np.random.default_rng(seed)
    max_quad=-np.inf
    failures=0
    records=[]
    for tr in range(trials):
        xs=np.sort(rng.uniform(-5,5,size=m))
        M=np.zeros((m,m))
        for i in range(m):
            for j in range(m):
                M[i,j]=psi_func(np.array([xs[i]-xs[j]]))[0]
        c=rng.normal(size=m)
        c=c-c.mean()
        q=float(c@M@c)
        max_quad=max(max_quad,q)
        if q>1e-8:
            failures+=1
        if tr<10:
            records.append({'trial':tr,'quad':q,'sum_c':float(c.sum()),'max_abs_x':float(np.max(np.abs(xs)))})
    return max_quad, failures, records

# Define symbols.
weights=prime_shift_weights(8.0)
xis=np.linspace(-10,10,401)
psi_pr=psi_from_discrete(weights,xis)
psi_gam=psi_gamma_grid(xis, eps=1e-4, T=60, N=20000)
psi_sum=psi_pr+psi_gam
# Non-CND but nonnegative example: xi^4 / (1+xi^2) still often not CND; use xi^4 explicitly bounded range.
def psi_non_cnd(x):
    x=np.asarray(x)
    return x**4/(1+x**2)

def psi_pr_func(x): return psi_from_discrete(weights,np.asarray(x))
def psi_g_func(x): return psi_gamma_grid(np.asarray(x), eps=1e-4, T=60, N=12000)
def psi_sum_func(x): return psi_pr_func(x)+psi_g_func(x)

def psi_abs_func(x): return np.abs(np.asarray(x)) # CND baseline

checks=[]
for name,func in [('prime_discrete',psi_pr_func),('gamma_truncated',psi_g_func),('prime_plus_gamma',psi_sum_func),('abs_x_baseline',psi_abs_func),('nonnegative_non_cnd_candidate',psi_non_cnd)]:
    maxq,fail,recs=cnd_check(func, trials=120, m=7, seed=42)
    checks.append({'symbol':name,'max_conditional_quadratic':maxq,'failures_gt_1e_minus_8':fail,'trials':120})

with open(OUT/'cnd_random_checks_step84.csv','w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(checks[0].keys()))
    wr.writeheader(); wr.writerows(checks)

# Symbol profile CSV
with open(OUT/'candidate_paired_symbols_step84.csv','w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=['xi','psi_prime','psi_gamma','psi_sum','psi_non_cnd'])
    wr.writeheader()
    for x,pp,gg,ss in zip(xis,psi_pr,psi_gam,psi_sum):
        wr.writerow({'xi':x,'psi_prime':pp,'psi_gamma':gg,'psi_sum':ss,'psi_non_cnd':float(psi_non_cnd(np.array([x]))[0])})

# CND gate summary / LK status
summary=[
    {'slot':'prime finite cutoff','candidate_measure':'sum_n Lambda(n)/sqrt(n) alpha_L(log n)^2 delta_{log n}','LK_condition':'finite positive measure','status':'passes CND paired-feature gate at finite cutoff','open_record':'matching to signed prime term and tail completion'},
    {'slot':'gamma archimedean','candidate_measure':'0.5 e^{-t/4}/(1-e^{-t}) dt on t>0 with shift t/2','LK_condition':'positive Levy measure; min(t^2,1) integrable','status':'passes paired-feature gate after renormalized difference pairing','open_record':'exact signed-gamma matching and constants'},
    {'slot':'pole completion','candidate_measure':'finite-rank/killing/quotient feature, not translation shift measure','LK_condition':'not a conservative shift feature','status':'can repair finite-dimensional null/pole modes only','open_record':'cannot pay full-core diagonal'},
    {'slot':'tail support','candidate_measure':'positive tail measure or defect budget','LK_condition':'must satisfy positive measure/tail bound','status':'candidate only','open_record':'fixed/exhaustive ledger tail control'},
    {'slot':'completed paired carrier','candidate_measure':'sum of accepted measures plus finite-rank/pole features','LK_condition':'CND for translation-invariant part plus positive finite-rank part','status':'not yet accepted','open_record':'prove equality/domination vs actual completed Weil form'},
]
with open(OUT/'paired_feature_gate_summary_step84.csv','w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=list(summary[0].keys()))
    wr.writeheader(); wr.writerows(summary)

# Plots.
plt.figure(figsize=(7,4))
plt.plot(xis,psi_pr,label='prime finite shift symbol')
plt.plot(xis,psi_gam,label='gamma paired symbol')
plt.plot(xis,psi_sum,label='sum')
plt.xlabel('xi'); plt.ylabel('symbol')
plt.title('Candidate paired feature symbols')
plt.legend(); plt.tight_layout()
plt.savefig(OUT/'candidate_paired_symbols_step84.png',dpi=160)
plt.close()

plt.figure(figsize=(6,4))
labels=[c['symbol'] for c in checks]
vals=[c['max_conditional_quadratic'] for c in checks]
plt.bar(range(len(vals)),vals)
plt.axhline(0,linewidth=1)
plt.xticks(range(len(vals)),labels,rotation=35,ha='right')
plt.ylabel('max sampled conditional quadratic')
plt.title('CND sample gate: <= 0 passes sampled tests')
plt.tight_layout()
plt.savefig(OUT/'cnd_random_checks_step84.png',dpi=160)
plt.close()

# A finite-dimensional no-go for non-CND symbol: save one explicit matrix violation for non-CND.
rng=np.random.default_rng(7)
violation=None
for tr in range(10000):
    m=5
    xs=np.sort(rng.uniform(-3,3,size=m))
    M=np.array([[psi_non_cnd(np.array([xs[i]-xs[j]]))[0] for j in range(m)] for i in range(m)])
    c=rng.normal(size=m); c=c-c.mean()
    q=float(c@M@c)
    if q>1e-6:
        violation={'trial':tr,'q':q,'xs':xs.tolist(),'c':c.tolist()}
        break
with open(OUT/'non_cnd_explicit_violation_step84.json','w') as f:
    json.dump(violation,f,indent=2)

# Minimal structural TeX balance checker can be done separately.
print('done', OUT)
