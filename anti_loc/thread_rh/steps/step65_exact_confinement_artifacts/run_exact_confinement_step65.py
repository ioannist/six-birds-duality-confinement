import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/anti_localization_step65_exact_confinement')
out.mkdir(exist_ok=True)

# Fixed squeeze: a fixed A>0 cannot be <= 1/n eventually; A=0 can.
rows=[]
for n in range(1,101):
    b=1/n
    for A in [0.0, 0.001, 0.01, 0.1]:
        rows.append({'n':n,'bound':b,'fixed_A':A,'squeeze_holds': A <= b})
pd.DataFrame(rows).to_csv(out/'fixed_squeeze_checks_step65.csv',index=False)

# Monotone nontermination: K_n = 1 + 1/n never <= 1.
rows=[]
for n in range(1,501):
    K=1+1/n
    rows.append({'n':n,'K_n':K,'Theta':1.0,'defect':K-1,'accepted':K<=1})
pd.DataFrame(rows).to_csv(out/'monotone_nontermination_step65.csv',index=False)

# Moving-ledger hidden tail: visible A_n=0, tail=1 means full A=1 missed.
rows=[]
for n in range(1,101):
    rows.append({'n':n,'visible_A_n':0.0,'visible_bound':1/n,'hidden_tail':1.0,'full_A':1.0,'full_bound_without_tail':1/n,'tail_accounted_bound':1+1/n})
pd.DataFrame(rows).to_csv(out/'moving_ledger_tail_failure_step65.csv',index=False)

# Optimized obstruction budget: a_n=1/Lambda_n, b_n examples.
rows=[]
for n in range(1,501):
    Lambda=n
    a=1/Lambda
    b=1/(n*n)
    opt=(np.sqrt(a)+np.sqrt(b))**2
    rows.append({'n':n,'Lambda':Lambda,'a_n':a,'b_n':b,'optimized_trace_bound':opt})
pd.DataFrame(rows).to_csv(out/'optimized_obstruction_budget_step65.csv',index=False)

# Plots
fig,ax=plt.subplots(figsize=(7,4.5))
ns=np.arange(1,101)
ax.plot(ns,1/ns,label='shrinking bound 1/n')
for A in [0.001,0.01,0.1]:
    ax.axhline(A,linestyle='--',label=f'fixed A={A}')
ax.set_xlabel('n')
ax.set_ylabel('PSD scalar bound')
ax.set_title('Fixed-object squeeze: positive A eventually violates 1/n')
ax.legend()
fig.tight_layout()
fig.savefig(out/'fixed_squeeze_step65.png',dpi=200)
plt.close(fig)

fig,ax=plt.subplots(figsize=(7,4.5))
ns=np.arange(1,501)
ax.plot(ns,1+1/ns,label='K_n=1+1/n')
ax.axhline(1,color='black',linestyle='--',label='Theta=1')
ax.set_xlabel('n')
ax.set_ylabel('K_n')
ax.set_title('Monotone improvement without finite completion')
ax.legend()
fig.tight_layout()
fig.savefig(out/'monotone_nontermination_step65.png',dpi=200)
plt.close(fig)

fig,ax=plt.subplots(figsize=(7,4.5))
ns=np.arange(1,101)
ax.plot(ns,1/ns,label='visible bound 1/n')
ax.axhline(1,color='red',linestyle='--',label='hidden tail/full A=1')
ax.set_xlabel('n')
ax.set_ylabel('mass/budget')
ax.set_title('Moving-ledger squeeze fails without tail/exhaustivity')
ax.legend()
fig.tight_layout()
fig.savefig(out/'moving_ledger_tail_failure_step65.png',dpi=200)
plt.close(fig)

fig,ax=plt.subplots(figsize=(7,4.5))
ns=np.arange(1,501)
a=1/ns
b=1/(ns*ns)
opt=(np.sqrt(a)+np.sqrt(b))**2
ax.loglog(ns,opt,label='optimized trace bound')
ax.loglog(ns,a,label='a_n=1/n',linestyle='--')
ax.loglog(ns,b,label='b_n=1/n^2',linestyle='--')
ax.set_xlabel('n')
ax.set_ylabel('bound')
ax.set_title('Optimized obstruction budget tends to zero')
ax.legend()
fig.tight_layout()
fig.savefig(out/'optimized_obstruction_budget_step65.png',dpi=200)
plt.close(fig)
