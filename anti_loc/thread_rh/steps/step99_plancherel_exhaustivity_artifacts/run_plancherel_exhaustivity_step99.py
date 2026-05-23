import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step99_plancherel_exhaustivity')
out.mkdir(exist_ok=True)

# 1. Finite window tail model: trace-class ledger with eigenvalues j^-p
ns = np.arange(1, 101)
rows=[]
for p in [1.2, 1.5, 2.0, 3.0]:
    eig = np.array([(j+1)**(-p) for j in range(50000)])
    total = eig.sum()
    for n in ns:
        tail = eig[n:].sum()
        rows.append({'p':p,'n':n,'tail_trace':tail,'tail_fraction':tail/total})
df_tail=pd.DataFrame(rows)
df_tail.to_csv(out/'plancherel_tail_trace_model_step99.csv', index=False)
plt.figure(figsize=(7,4.5))
for p,grp in df_tail.groupby('p'):
    plt.plot(grp['n'], grp['tail_fraction'], label=f'p={p}')
plt.yscale('log')
plt.xlabel('window size n')
plt.ylabel('tail fraction of trace-class ledger')
plt.title('Exhaustive tail for trace-class zero ledger')
plt.legend()
plt.tight_layout()
plt.savefig(out/'plancherel_tail_trace_model_step99.png', dpi=160)
plt.close()

# 2. Moving window failure: moving projection covers unit vector e_n, missing fixed vector e_0
nmax=80
rows=[]
for n in range(1,nmax+1):
    covered_fixed = 1.0 if n==1 else 0.0 # moving singleton window not exhaustive for e0 after n>1
    rows.append({'stage':n,'visible_window_bound':1/n,'fixed_direction_covered':covered_fixed,'hidden_tail':1-covered_fixed})
df_move=pd.DataFrame(rows)
df_move.to_csv(out/'moving_window_failure_step99.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(df_move['stage'], df_move['visible_window_bound'], label='visible finite-window bound')
plt.plot(df_move['stage'], df_move['hidden_tail'], label='uncovered fixed direction')
plt.xlabel('stage')
plt.ylabel('value')
plt.title('Moving-window support-only failure')
plt.legend()
plt.tight_layout()
plt.savefig(out/'moving_window_failure_step99.png', dpi=160)
plt.close()

# 3. Lower frame budget collapse if Lambda grows and tail decays
rows=[]
for alpha in [0.5, 1.0, 1.5]:
    for beta in [0.5, 1.0, 2.0]:
        for n in ns:
            Lambda = n**alpha
            tail = n**(-beta)
            budget = 1/Lambda + tail
            rows.append({'alpha_Lambda':alpha,'beta_tail':beta,'n':n,'Lambda':Lambda,'tail':tail,'budget':budget})
df_budget=pd.DataFrame(rows)
df_budget.to_csv(out/'completed_lower_frame_budget_step99.csv', index=False)
plt.figure(figsize=(7,4.5))
for (alpha,beta),grp in df_budget.groupby(['alpha_Lambda','beta_tail']):
    if (alpha,beta) in [(1.0,1.0),(1.0,2.0),(0.5,1.0),(1.5,0.5)]:
        plt.plot(grp['n'], grp['budget'], label=f'Lambda=n^{alpha}, tail=n^-{beta}')
plt.yscale('log')
plt.xlabel('stage n')
plt.ylabel('certified budget 1/Lambda + tail')
plt.title('Completed lower-frame budget collapse requires both growth and tail')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(out/'completed_lower_frame_budget_step99.png', dpi=160)
plt.close()

# 4. Upper bound does not imply lower frame: matrix eigenvalues with bounded max but zero min
rows=[]
for n in range(2,101):
    eigs=np.ones(n)
    eigs[-1]=0.0
    rows.append({'dimension':n,'upper_bound_max_eigenvalue':eigs.max(),'lower_frame_min_eigenvalue':eigs.min()})
df_upper=pd.DataFrame(rows)
df_upper.to_csv(out/'upper_not_lower_frame_step99.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(df_upper['dimension'], df_upper['upper_bound_max_eigenvalue'], label='upper bound')
plt.plot(df_upper['dimension'], df_upper['lower_frame_min_eigenvalue'], label='lower frame')
plt.xlabel('dimension')
plt.ylabel('eigenvalue')
plt.title('Upper-frame control does not give lower-frame coercivity')
plt.legend()
plt.tight_layout()
plt.savefig(out/'upper_not_lower_frame_step99.png', dpi=160)
plt.close()

# LaTeX balance check
tex = (out/'semilocal_plancherel_exhaustivity_step99.tex').read_text()
checks=[]
for env in ['theorem','lemma','definition','proposition','corollary','warning','enumerate']:
    checks.append({'environment':env,'begin_count':tex.count('\\begin{'+env+'}'),'end_count':tex.count('\\end{'+env+'}')})
pd.DataFrame(checks).to_csv(out/'latex_structure_check_step99.csv', index=False)
print('created Step 99 artifacts in', out)
