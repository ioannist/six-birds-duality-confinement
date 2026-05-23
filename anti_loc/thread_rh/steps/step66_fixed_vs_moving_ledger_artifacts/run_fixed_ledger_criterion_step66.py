import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

out = Path('/mnt/data/anti_localization_step66_fixed_ledger')
out.mkdir(parents=True, exist_ok=True)

# 1. Fixed ledger squeeze: if A>0, eventually B_n=1/n cannot dominate it.
rows=[]
A_vals=[0.0,0.05,0.1,0.2]
for A in A_vals:
    for n in [1,2,3,5,10,20,50,100,200,500,1000]:
        B=1.0/n
        slack=B-A
        rows.append({'case':'fixed_squeeze_scalar','A':A,'n':n,'B_n':B,'slack_B_minus_A':slack,'dominates':slack>=-1e-12})
pd.DataFrame(rows).to_csv(out/'fixed_squeeze_scalar_step66.csv', index=False)

# Plot fixed squeeze: B_n and fixed A thresholds
n_grid=np.arange(1,501)
plt.figure(figsize=(7,4.5))
plt.plot(n_grid,1/n_grid,label='B_n=1/n')
for A in [0.05,0.1,0.2]:
    plt.axhline(A, linestyle='--', label=f'A={A}')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('budget / fixed ledger size')
plt.title('Fixed ledger squeeze: positive A cannot stay below B_n→0')
plt.legend()
plt.tight_layout()
plt.savefig(out/'fixed_ledger_squeeze_step66.png', dpi=180)
plt.close()

# 2. Exhaustive ledger: A_tail_n + B_n -> 0 implies full A=0 only if A_n covers all positive mass.
# We model upper bound on full ledger mass: tr(A) <= tr(B_n)+tau_n
rows=[]
for p in [0.25,0.5,1.0,2.0]:
    for n in [1,2,5,10,20,50,100,200,500,1000]:
        B=1.0/n
        tau=1.0/(n**p)
        total=B+tau
        rows.append({'case':'exhaustive_tail_bound','tail_decay_p':p,'n':n,'B_n_trace':B,'tail_bound_tau_n':tau,'certified_full_trace_bound':total})
pd.DataFrame(rows).to_csv(out/'exhaustive_tail_bound_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
for p in [0.25,0.5,1.0,2.0]:
    n=n_grid
    total=1/n + 1/(n**p)
    plt.plot(n,total,label=f'p={p}')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('certified tr(A_Z) bound')
plt.title('Exhaustive ledger squeeze: budget + tail bound')
plt.legend()
plt.tight_layout()
plt.savefig(out/'exhaustive_ledger_tail_squeeze_step66.png', dpi=180)
plt.close()

# 3. Moving ledger failure: A_n=0 squeezed while hidden A=1 remains outside the ledger.
rows=[]
for n in [1,2,5,10,20,50,100,200,500,1000]:
    A_hidden=1.0
    A_n=0.0
    B_n=1.0/n
    rows.append({'case':'moving_ledger_failure','n':n,'visible_A_n':A_n,'B_n':B_n,'hidden_full_A':A_hidden,'visible_dominates':A_n<=B_n,'full_confinement':False})
pd.DataFrame(rows).to_csv(out/'moving_ledger_failure_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(n_grid,1/n_grid,label='visible budget B_n')
plt.axhline(1.0, linestyle='--', label='hidden full A_Z')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('trace')
plt.title('Moving-ledger failure: visible squeeze misses hidden tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'moving_ledger_failure_step66.png', dpi=180)
plt.close()

# 4. Status classifier examples.
def classify(fixed=False, exhaustive=False, finite_completion=False, tail=False, budget_to_zero=False):
    if finite_completion:
        return 'finite_completion_exact'
    if fixed and budget_to_zero:
        return 'fixed_ledger_exact_squeeze'
    if exhaustive and tail and budget_to_zero:
        return 'exhaustive_ledger_exact_squeeze'
    if budget_to_zero and not (fixed or exhaustive):
        return 'moving_ledger_support_only'
    return 'insufficient_or_quantitative_only'

cases=[
    {'case':'finite zero budget at N','fixed':True,'exhaustive':True,'finite_completion':True,'tail':True,'budget_to_zero':True},
    {'case':'same full zero ledger squeezed by B_n','fixed':True,'exhaustive':False,'finite_completion':False,'tail':False,'budget_to_zero':True},
    {'case':'truncated zero ledger with tail bound','fixed':False,'exhaustive':True,'finite_completion':False,'tail':True,'budget_to_zero':True},
    {'case':'truncated ledger only no tail','fixed':False,'exhaustive':False,'finite_completion':False,'tail':False,'budget_to_zero':True},
    {'case':'fixed ledger bounded by nonzero budget','fixed':True,'exhaustive':False,'finite_completion':False,'tail':False,'budget_to_zero':False},
]
for c in cases:
    c['status']=classify(c['fixed'],c['exhaustive'],c['finite_completion'],c['tail'],c['budget_to_zero'])
pd.DataFrame(cases).to_csv(out/'ledger_status_cases_step66.csv', index=False)

# 5. Optimized budget example from Step65: (sqrt(a)+sqrt(b))^2.
rows=[]
for p in [0.5,1.0,2.0]:
    for q in [0.5,1.0,2.0]:
        for n in [10,100,1000,10000]:
            a=1/(n**p)
            b=1/(n**q)
            opt=(np.sqrt(a)+np.sqrt(b))**2
            t=np.sqrt(b/a) if a>0 else 1.0
            rows.append({'case':'optimized_budget','p_a':p,'q_b':q,'n':n,'a_n':a,'b_n':b,'t_star':t,'optimized_trace_bound':opt})
pd.DataFrame(rows).to_csv(out/'optimized_budget_step66.csv', index=False)

# Plot optimized budget for selected cases
plt.figure(figsize=(7,4.5))
for (p,q) in [(1,1),(1,2),(2,1),(0.5,1)]:
    n=n_grid
    a=1/(n**p)
    b=1/(n**q)
    opt=(np.sqrt(a)+np.sqrt(b))**2
    plt.plot(n,opt,label=f'a~n^-{p}, b~n^-{q}')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('optimized trace bound')
plt.title('Optimized explicit-formula/source obstruction bound')
plt.legend()
plt.tight_layout()
plt.savefig(out/'optimized_budget_step66.png', dpi=180)
plt.close()

print('created step66 artifacts in', out)
