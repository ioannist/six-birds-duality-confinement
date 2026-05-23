import math, csv, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step77_autocorr_prime')
OUT.mkdir(exist_ok=True)

def von_mangoldt(n:int)->float:
    # log p if n is p^k, else 0
    m=n
    for p in range(2,int(math.sqrt(n))+1):
        if m%p==0:
            k=0
            while m%p==0:
                m//=p; k+=1
            if m==1:
                return math.log(p)
            return 0.0
    return math.log(n) if n>=2 else 0.0

def weights(L=6.0):
    N=int(math.exp(L))
    data=[]
    for n in range(2,N+1):
        lam=von_mangoldt(n)
        if lam>0:
            a=math.log(n)
            alpha=max(0.0,1.0-a/L)
            if alpha>0:
                w=lam/(math.sqrt(n))*alpha**2
                data.append((n,a,w))
    return data

def symbol_vals(data, xis, c=None):
    W=sum(w for _,_,w in data)
    if c is None:
        c=2*W
    signed=np.array([-2*sum(w*math.cos(a*x) for _,a,w in data) for x in xis])
    repaired=np.array([c-2*sum(w*math.cos(a*x) for _,a,w in data) for x in xis])
    shift=np.array([sum(w*(2-2*math.cos(a*x)) for _,a,w in data) for x in xis])
    return W, signed, repaired, shift

# Prime slot symbols
L=6.0
data=weights(L)
xis=np.linspace(0,20,1200)
W,signed,repaired,shift=symbol_vals(data,xis)
with open(OUT/'prime_slot_symbol_step77.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['xi','signed_prime_symbol','sharp_repaired_symbol','shift_difference_symbol'])
    for x,s,r,sh in zip(xis,signed,repaired,shift):
        wr.writerow([x,s,r,sh])
with open(OUT/'prime_slot_summary_step77.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['quantity','value'])
    wr.writerow(['L',L]); wr.writerow(['num_prime_power_shifts',len(data)]); wr.writerow(['sum_weights',W]); wr.writerow(['sharp_diagonal_repair',2*W]); wr.writerow(['min_signed_symbol',float(np.min(signed))]); wr.writerow(['min_repaired_symbol',float(np.min(repaired))]); wr.writerow(['max_abs_repaired_minus_shift',float(np.max(np.abs(repaired-shift)))])
plt.figure(figsize=(8,5))
plt.plot(xis,signed,label='signed prime autocorrelation symbol')
plt.plot(xis,repaired,label='after sharp diagonal repair')
plt.axhline(0,linewidth=0.8)
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.title('Prime signed term vs positive shift-difference repair')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'prime_signed_vs_repaired_step77.png',dpi=180)
plt.close()

# Diagonal threshold sweep
cs=np.linspace(0,2.5*W,200)
mins=[]
for c in cs:
    _,_,rep,_=symbol_vals(data,xis,c=c)
    mins.append(float(np.min(rep)))
with open(OUT/'diagonal_repair_threshold_step77.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['c','min_symbol','passes_grid'])
    for c,m in zip(cs,mins):
        wr.writerow([c,m,m>=-1e-8])
plt.figure(figsize=(7,4.5))
plt.plot(cs,mins)
plt.axvline(2*W,linestyle='--',label=r'$2\sum w_a$')
plt.axhline(0,linewidth=0.8)
plt.xlabel('diagonal coefficient c')
plt.ylabel('min symbol on grid')
plt.title('Minimum diagonal repair threshold')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'diagonal_repair_threshold_step77.png',dpi=180)
plt.close()

# Autocorrelation identity test on periodic discretization
rng=np.random.default_rng(77)
N=512
xgrid=np.linspace(-math.pi,math.pi,N,endpoint=False)
f=rng.normal(size=N)+1j*rng.normal(size=N)
# use unitary FFT convention for finite cyclic test
F=np.fft.fft(f)/math.sqrt(N)
# cyclic autocorrelation via inverse FFT of |F|^2 times sqrt? With unitary conv, autocorr sequence below direct.
def shift(arr,k): return np.roll(arr,-k)
rows=[]
for k in [1,2,5,17,83]:
    h=np.vdot(f,shift(f,k))  # <f, tau_k f> numpy vdot conjugates first; convention not exact but real identity works
    diff=np.linalg.norm(shift(f,k)-f)**2
    rhs=2*np.linalg.norm(f)**2 - 2*np.real(h)
    rows.append((k,float(diff),float(rhs),float(abs(diff-rhs))))
with open(OUT/'autocorrelation_difference_identity_step77.csv','w',newline='') as fcsv:
    wr=csv.writer(fcsv); wr.writerow(['shift_k','norm_shift_minus_f_sq','2h0_minus_h_minus_hminus','abs_error'])
    wr.writerows(rows)

# Trace-not-domination mini counterexample
A=np.diag([2.0,0.0])
K=np.diag([1.0,1.0])
with open(OUT/'trace_not_domination_countermodel_step77.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['tr_A','tr_K','trace_equal_or_less','lambda_max_A_minus_K','loewner_domination'])
    wr.writerow([np.trace(A),np.trace(K),np.trace(A)<=np.trace(K),np.linalg.eigvalsh(A-K).max(),np.linalg.eigvalsh(K-A).min()>=-1e-12])
