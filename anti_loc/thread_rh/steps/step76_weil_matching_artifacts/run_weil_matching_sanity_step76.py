import math, csv, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step76_weil_matching')
OUT.mkdir(parents=True, exist_ok=True)

def von_mangoldt(n:int)->float:
    # log p if n is p^k, else 0
    m=n
    p=2
    factors=[]
    d=2
    temp=n
    p=2
    while p*p<=temp:
        if temp%p==0:
            c=0
            while temp%p==0:
                temp//=p; c+=1
            factors.append((p,c))
        p += 1 if p==2 else 2
    if temp>1:
        factors.append((temp,1))
    if len(factors)==1:
        return math.log(factors[0][0])
    return 0.0

def alpha_L(logn,L):
    if logn>=L: return 0.0
    return max(0.0, 1.0-logn/L)

# prime diagonal mass sweep
rows=[]
for L in np.linspace(2,14,25):
    N=int(math.exp(L))
    s=0.0
    s_un=0.0
    for n in range(2,N+1):
        lam=von_mangoldt(n)
        if lam==0: continue
        a=alpha_L(math.log(n),L)
        w=lam/math.sqrt(n)*a*a
        s += w
        s_un += lam/math.sqrt(n)
    rows.append({'L':L,'N':N,'diag_mass_cutoff':2*s,'sum_weights_cutoff':s,'diag_mass_unwindowed_to_expL':2*s_un})
with open(OUT/'prime_diagonal_mass_step76.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

plt.figure()
plt.plot([r['L'] for r in rows],[r['diag_mass_cutoff'] for r in rows],marker='o',label='windowed diagonal mass')
plt.plot([r['L'] for r in rows],[r['diag_mass_unwindowed_to_expL'] for r in rows],marker='x',label='unwindowed to exp(L)')
plt.xlabel('L')
plt.ylabel('D_pr,L = 2 sum Lambda(n)/sqrt(n) alpha_L^2')
plt.title('Prime-shift feature diagonal mass')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'prime_diagonal_mass_step76.png',dpi=160)
plt.close()

# finite discrete shift expansion check
rng=np.random.default_rng(71)
N=64
f=rng.normal(size=N)+1j*rng.normal(size=N)
rows2=[]
for shift in [1,2,3,5,8,13,21]:
    tau=np.roll(f,-shift) # t+a
    lhs=np.vdot(tau-f,tau-f).real
    rhs=2*np.vdot(f,f).real-2*np.vdot(f,tau).real
    rows2.append({'shift':shift,'lhs_norm_difference':lhs,'rhs_diag_minus_corr':rhs,'abs_error':abs(lhs-rhs)})
with open(OUT/'shift_expansion_check_step76.csv','w',newline='') as fcsv:
    w=csv.DictWriter(fcsv,fieldnames=rows2[0].keys()); w.writeheader(); w.writerows(rows2)

# Signed component repair toy: A signed correlation can be represented by positive feature only after adding diagonal mass.
rhos=np.linspace(-0.95,0.95,39)
rows3=[]
for rho in rhos:
    # signed 2x2 correlation form Q = [[0,-rho],[-rho,0]] not PSD generally;
    # add diagonal d I, find minimal d for PSD = |rho|.
    Q=np.array([[0,-rho],[-rho,0]],float)
    eig=np.linalg.eigvalsh(Q)
    d=max(0,-eig[0])
    repaired=Q+d*np.eye(2)
    rows3.append({'rho':rho,'min_eig_signed':eig[0],'diag_repair_needed':d,'min_eig_repaired':np.linalg.eigvalsh(repaired)[0]})
with open(OUT/'signed_correlation_repair_step76.csv','w',newline='') as fcsv:
    w=csv.DictWriter(fcsv,fieldnames=rows3[0].keys()); w.writeheader(); w.writerows(rows3)

plt.figure()
plt.plot([r['rho'] for r in rows3],[r['diag_repair_needed'] for r in rows3],marker='o')
plt.xlabel('signed correlation rho')
plt.ylabel('minimal diagonal repair')
plt.title('Signed correlation requires diagonal/completion repair')
plt.tight_layout()
plt.savefig(OUT/'signed_correlation_repair_step76.png',dpi=160)
plt.close()

print('wrote step76 sanity artifacts')
