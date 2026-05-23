import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/rh_membrane_step96_delta_status_audit')
out.mkdir(exist_ok=True)

# Toy model 1: compact-after-quotient eigenvalue tail
n = np.arange(1,201)
compact_eigs = 2/(n**1.5)
finite_rank_20 = compact_eigs.copy(); finite_rank_20[20:] = 0
unresolved_floor = compact_eigs + 0.05
pd.DataFrame({'n': n, 'compact_after_quotient': compact_eigs, 'finite_rank_window_20': finite_rank_20, 'unresolved_floor': unresolved_floor}).to_csv(out/'delta_status_eigen_models_step96.csv', index=False)
plt.figure(figsize=(6,4))
plt.semilogy(n, compact_eigs, label='compact tail')
plt.semilogy(n, finite_rank_20 + 1e-8, label='finite window')
plt.semilogy(n, unresolved_floor, label='unresolved floor')
plt.xlabel('mode index')
plt.ylabel('model eigenvalue')
plt.title('Delta_S status models')
plt.legend()
plt.tight_layout()
plt.savefig(out/'delta_status_eigen_models_step96.png', dpi=200)
plt.close()

# Toy source absorption ladder
stages = np.arange(1,101)
Lambda = stages**1.1
Esrc = 1/(stages**1.4)
budget = 1/Lambda + Esrc
pd.DataFrame({'stage': stages, 'Lambda': Lambda, 'source_defect': Esrc, 'budget': budget}).to_csv(out/'source_absorption_budget_step96.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(stages, 1/Lambda, label='1/Lambda')
plt.plot(stages, Esrc, label='source defect')
plt.plot(stages, budget, label='total source budget')
plt.xlabel('source stage')
plt.ylabel('budget')
plt.title('Toy source absorption budget')
plt.legend()
plt.tight_layout()
plt.savefig(out/'source_absorption_budget_step96.png', dpi=200)
plt.close()

# Tail promotion model: finite window with and without tail
N = np.arange(1,101)
finite_bound = 1/(N**1.3)
vanishing_tail = 1/(N**1.2)
nonvanishing_tail = 0.15 + 1/(N**1.2)
pd.DataFrame({'N': N, 'finite_bound': finite_bound, 'vanishing_tail': vanishing_tail, 'nonvanishing_tail': nonvanishing_tail, 'exhaustive_total': finite_bound+vanishing_tail, 'support_only_total': finite_bound+nonvanishing_tail}).to_csv(out/'tail_promotion_model_step96.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(N, finite_bound+vanishing_tail, label='exhaustive total')
plt.plot(N, finite_bound+nonvanishing_tail, label='support-only total')
plt.xlabel('window size')
plt.ylabel('ledger bound')
plt.title('Tail bridge distinguishes proof from support')
plt.legend()
plt.tight_layout()
plt.savefig(out/'tail_promotion_model_step96.png', dpi=200)
plt.close()

# Structural LaTeX balance check
tex = (out/'semilocal_delta_status_step96.tex').read_text()
checks=[]
for env in ['document','enumerate']:
    checks.append({'env': env, 'begin': tex.count('\\begin{'+env+'}'), 'end': tex.count('\\end{'+env+'}'), 'balanced': tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}')})
pd.DataFrame(checks).to_csv(out/'latex_structure_check_step96.csv', index=False)
print('done')
