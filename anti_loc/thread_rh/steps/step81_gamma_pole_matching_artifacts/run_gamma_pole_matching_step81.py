import csv, math, os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp

out = Path('/mnt/data/rh_membrane_step81_gamma_pole_matching')
out.mkdir(parents=True, exist_ok=True)

def von_mangoldt(n):
    # naive prime power detection
    m=n
    p=2
    # find if n=p^k
    for p in range(2, int(math.sqrt(n))+1):
        if n % p == 0:
            k=0; tmp=n
            while tmp % p == 0:
                tmp//=p; k+=1
            if tmp==1:
                return math.log(p)
            return 0.0
    # n prime
    return math.log(n)

def prime_weights(L):
    N=int(math.exp(L))
    data=[]
    total=0.0
    for n in range(2,N+1):
        lam=von_mangoldt(n)
        if lam==0: continue
        a=math.log(n)
        alpha=max(0.0, 1.0-a/L)**2
        w=lam/(math.sqrt(n))*alpha
        if w>0:
            data.append((n,a,w))
            total += w
    return data,total

# constants
mp.mp.dps = 50
c_gamma = 0.5*mp.digamma(mp.mpf('0.25')) - 0.5*mp.log(mp.pi)
abs_c_gamma = -c_gamma
with open(out/'gamma_constant_step81.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['quantity','value'])
    w.writerow(['c_gamma', float(c_gamma)])
    w.writerow(['abs_c_gamma', float(abs_c_gamma)])
    w.writerow(['psi_1_4', float(mp.digamma(mp.mpf('0.25')))])
    w.writerow(['0.5_log_pi', float(0.5*mp.log(mp.pi))])

# L sweep for diagonal balance
rows=[]
for L in [3,4,5,6,7,8,9,10,12]:
    _,total=prime_weights(L)
    d_pr=2*total
    rows.append({
        'L':L,
        'sum_w': total,
        'd_prime': d_pr,
        'gamma_constant_c': float(c_gamma),
        'balance_sigma_plus': d_pr - float(c_gamma),
        'balance_sigma_minus': d_pr + float(c_gamma),
        'abs_c_gamma': float(abs_c_gamma),
    })
with open(out/'gamma_pole_constant_balance_step81.csv','w',newline='') as f:
    fieldnames=list(rows[0].keys())
    w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(rows)

# symbol profile for gamma: G, normalized positive, constants
xis=np.linspace(0,30,301)
gamma_rows=[]
for xi in xis:
    G=0.5*mp.re(mp.digamma(mp.mpf('0.25')+0.5j*xi))-0.5*mp.log(mp.pi)
    Psi=G-c_gamma
    gamma_rows.append({'xi':xi,'G_gamma':float(G),'Psi_gamma_positive':float(Psi),'c_gamma':float(c_gamma)})
with open(out/'gamma_constant_symbol_profile_step81.csv','w',newline='') as f:
    fieldnames=list(gamma_rows[0].keys())
    w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(gamma_rows)

# toy pole payment model: pole rank features with diagonal alpha pay balance sigma_plus
rows2=[]
for Lrow in rows:
    L=Lrow['L']; bal=Lrow['balance_sigma_plus']
    for alpha in np.linspace(0, bal*1.5, 16):
        residual=max(0.0, bal-alpha)
        rows2.append({'L':L,'balance_required':bal,'pole_alpha':alpha,'remaining_defect':residual,'paid': alpha>=bal})
with open(out/'pole_payment_sweep_step81.csv','w',newline='') as f:
    fieldnames=list(rows2[0].keys())
    w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader(); w.writerows(rows2)

# plots
Ls=[r['L'] for r in rows]
dpr=[r['d_prime'] for r in rows]
balplus=[r['balance_sigma_plus'] for r in rows]
balminus=[r['balance_sigma_minus'] for r in rows]
plt.figure(figsize=(7,4.5))
plt.plot(Ls,dpr,marker='o',label='prime diagonal repair d_pr')
plt.plot(Ls,balplus,marker='o',label='balance d_pr - c_gamma (sigma=+)')
plt.plot(Ls,balminus,marker='o',label='orientation variant d_pr + c_gamma')
plt.axhline(float(abs_c_gamma),linestyle='--',label='|c_gamma|')
plt.xlabel('cutoff L')
plt.ylabel('diagonal units')
plt.title('Prime and gamma constant balance ledger')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'gamma_pole_balance_step81.png',dpi=180)
plt.close()

plt.figure(figsize=(7,4.5))
plt.plot([r['xi'] for r in gamma_rows],[r['G_gamma'] for r in gamma_rows],label='signed gamma log-derivative G_gamma')
plt.plot([r['xi'] for r in gamma_rows],[r['Psi_gamma_positive'] for r in gamma_rows],label='positive normalized Psi_gamma')
plt.axhline(float(c_gamma),linestyle='--',label='c_gamma')
plt.xlabel('xi')
plt.ylabel('symbol')
plt.title('Gamma symbol: constant plus positive normalized feature')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'gamma_symbol_constant_decomp_step81.png',dpi=180)
plt.close()

# pole payment plot for one L
Lsel=8
subset=[r for r in rows2 if r['L']==Lsel]
plt.figure(figsize=(7,4.5))
plt.plot([r['pole_alpha'] for r in subset],[r['remaining_defect'] for r in subset],marker='o')
plt.axvline(subset[-1]['balance_required']/1.5, alpha=0) # noop
plt.xlabel('pole/completion finite-rank payment alpha')
plt.ylabel('remaining diagonal defect')
plt.title(f'Toy pole/completion payment threshold (L={Lsel})')
plt.tight_layout()
plt.savefig(out/'pole_payment_balance_step81.png',dpi=180)
plt.close()

print('wrote outputs to', out)
