import json, math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step78_completion_balance')
OUT.mkdir(parents=True, exist_ok=True)

def von_mangoldt(n:int)->float:
    # return log p if n is a prime power, else 0
    x=n
    for p in range(2,int(math.sqrt(n))+1):
        if x%p==0:
            k=0
            while x%p==0:
                x//=p; k+=1
            if x==1:
                return math.log(p)
            return 0.0
    return math.log(n) if n>=2 else 0.0

L=6.0
rows=[]
for n in range(2, int(math.exp(L))+1):
    lam=von_mangoldt(n)
    if lam>0:
        a=math.log(n)
        alpha=max(0.0,1-a/L)**2
        w=lam/math.sqrt(n)*alpha
        if w>0:
            rows.append({'n':n,'Lambda':lam,'a_log_n':a,'alpha_sq':alpha,'weight':w})
prime_df=pd.DataFrame(rows)
prime_df.to_csv(OUT/'prime_weights_step78.csv', index=False)
weights=prime_df['weight'].to_numpy()
a_vals=prime_df['a_log_n'].to_numpy()
d=2*weights.sum()

xis=np.linspace(0,40,2001)
signed=-2*np.sum(weights[:,None]*np.cos(a_vals[:,None]*xis[None,:]),axis=0)
positive=d+signed
pd.DataFrame({'xi':xis,'signed_prime_symbol':signed,'diagonal_repair':d,'positive_prime_symbol':positive}).to_csv(OUT/'prime_signed_positive_symbol_step78.csv', index=False)

# Toy balance problem: signed rest must be paid by gamma/pole/tail positive repairs.
r0=1.20*d
r1=0.35*d
gamma=0.20*d
R_sgn=r0+r1*np.cos(xis)
q_gamma=gamma*(1-np.cos(xis))
# minimal pole diagonal p for balance >= 0
need=R_sgn - d - q_gamma
p_min=max(0.0,float(np.max(need)))
for factor,name in [(0.6,'underpaid'),(1.0,'sharp'),(1.4,'overpaid')]:
    p=factor*p_min
    balance=d+p+q_gamma-R_sgn
    pd.DataFrame({'xi':xis,'balance_symbol':balance,'pole_diag':p,'case':name}).to_csv(OUT/f'balance_symbol_{name}_step78.csv', index=False)

summary=pd.DataFrame([
    {'quantity':'sum_prime_weights','value':weights.sum()},
    {'quantity':'diagonal_repair_d_pr','value':d},
    {'quantity':'toy_R_sgn_r0','value':r0},
    {'quantity':'toy_R_sgn_r1','value':r1},
    {'quantity':'toy_gamma_strength','value':gamma},
    {'quantity':'minimal_pole_diagonal_for_balance','value':p_min},
    {'quantity':'min_positive_prime_symbol','value':float(np.min(positive))},
    {'quantity':'min_signed_prime_symbol','value':float(np.min(signed))},
])
summary.to_csv(OUT/'completion_balance_summary_step78.csv', index=False)

# trace not balance / Loewner counterexample
A=np.diag([2.0,0.0])
K=np.diag([1.0,1.0])
Dmat=K-A
trace_df=pd.DataFrame([
    {'matrix':'A_zero_side','trace':np.trace(A),'lambda_min':np.linalg.eigvalsh(A).min(),'lambda_max':np.linalg.eigvalsh(A).max()},
    {'matrix':'K_carrier','trace':np.trace(K),'lambda_min':np.linalg.eigvalsh(K).min(),'lambda_max':np.linalg.eigvalsh(K).max()},
    {'matrix':'K_minus_A','trace':np.trace(Dmat),'lambda_min':np.linalg.eigvalsh(Dmat).min(),'lambda_max':np.linalg.eigvalsh(Dmat).max()},
])
trace_df.to_csv(OUT/'trace_not_balance_counterexample_step78.csv', index=False)

# plot signed vs positive prime
plt.figure(figsize=(7,4))
plt.plot(xis, signed, label='signed prime symbol')
plt.plot(xis, positive, label='after diagonal repair')
plt.axhline(0, linestyle='--', linewidth=1)
plt.xlabel(r'$\xi$')
plt.ylabel('symbol')
plt.title('Prime slot: signed term vs positive feature')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'prime_signed_positive_step78.png', dpi=180)
plt.close()

plt.figure(figsize=(7,4))
for factor,name in [(0.6,'underpaid'),(1.0,'sharp'),(1.4,'overpaid')]:
    p=factor*p_min
    balance=d+p+q_gamma-R_sgn
    plt.plot(xis, balance, label=f'{name}: p={p:.2g}')
plt.axhline(0, linestyle='--', linewidth=1)
plt.xlabel(r'$\xi$')
plt.ylabel('completion balance')
plt.title('Completion balance needs pole/gamma/tail payment')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'completion_balance_sweep_step78.png', dpi=180)
plt.close()

plt.figure(figsize=(6,4))
ps=np.linspace(0,1.8*p_min,300)
mins=[]
for p in ps:
    balance=d+p+q_gamma-R_sgn
    mins.append(np.min(balance))
plt.plot(ps, mins)
plt.axhline(0, linestyle='--', linewidth=1)
plt.axvline(p_min, linestyle='--', linewidth=1)
plt.xlabel('pole/completion diagonal p')
plt.ylabel('minimum balance')
plt.title('Sharp pole/completion payment threshold')
plt.tight_layout()
plt.savefig(OUT/'pole_payment_threshold_step78.png', dpi=180)
plt.close()

print(json.dumps({'d_pr':d,'p_min':p_min,'n_weights':len(weights)}, indent=2))
