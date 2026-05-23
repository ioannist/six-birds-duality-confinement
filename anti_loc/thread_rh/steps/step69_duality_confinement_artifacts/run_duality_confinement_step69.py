import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/anti_localization_step69_duality_confinement')

# 1. fixed ledger squeeze: A fixed scalar object A <= 1/n for all n implies A=0.
ns = np.arange(1, 201)
B = 1.0 / ns
A_fixed = np.zeros_like(B)  # only possible fixed A under all bounds as n->infty
fixed_df = pd.DataFrame({'n': ns, 'bound_Bn': B, 'forced_A': A_fixed})
fixed_df.to_csv(out/'fixed_ledger_squeeze_step69.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(ns, B, label='B_n=1/n')
plt.plot(ns, A_fixed, label='forced fixed A=0')
plt.xlabel('n')
plt.ylabel('trace bound')
plt.title('Fixed-ledger squeeze')
plt.legend()
plt.tight_layout()
plt.savefig(out/'fixed_ledger_squeeze_step69.png', dpi=160)
plt.close()

# 2. moving ledger failure: each measured window has zero, tail remains one.
tail = np.ones_like(ns, dtype=float)
window_bound = 1.0/ns**2
completed_total_upper = window_bound + tail
moving_df = pd.DataFrame({'n': ns, 'window_bound': window_bound, 'missing_tail': tail, 'completed_upper': completed_total_upper})
moving_df.to_csv(out/'moving_ledger_failure_step69.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(ns, window_bound, label='window bound -> 0')
plt.plot(ns, tail, label='uncontrolled tail')
plt.plot(ns, completed_total_upper, label='completed upper bound')
plt.xlabel('n')
plt.ylabel('mass/bound')
plt.title('Moving ledger without tail is support-only')
plt.legend()
plt.tight_layout()
plt.savefig(out/'moving_ledger_failure_step69.png', dpi=160)
plt.close()

# 3. exhaustive ledger: window bound and tail vanish.
tail_good = 1.0/(ns+1)**1.5
window_good = 1.0/ns**2
exhaustive_total = tail_good + window_good
exh_df = pd.DataFrame({'n': ns, 'window_bound': window_good, 'tail_bound': tail_good, 'completed_upper': exhaustive_total})
exh_df.to_csv(out/'exhaustive_ledger_squeeze_step69.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(ns, window_good, label='window bound')
plt.plot(ns, tail_good, label='tail bound')
plt.plot(ns, exhaustive_total, label='completed bound')
plt.xlabel('n')
plt.ylabel('bound')
plt.title('Exhaustive finite-ledger squeeze')
plt.legend()
plt.tight_layout()
plt.savefig(out/'exhaustive_ledger_squeeze_step69.png', dpi=160)
plt.close()

# 4. optimized obstruction budget.
Lambda = ns.astype(float)
Theta_trace = 1.0
E_src = 1.0/(ns**1.4)
E_bridge = 1.0/(ns**1.2)
a = Theta_trace/Lambda + E_src
b = E_bridge
opt = (np.sqrt(a)+np.sqrt(b))**2
budget_df = pd.DataFrame({'n': ns, 'Lambda': Lambda, 'a_source': a, 'b_bridge': b, 'optimized_trace_budget': opt})
budget_df.to_csv(out/'optimized_budget_step69.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(ns, a, label='a_n')
plt.plot(ns, b, label='b_n')
plt.plot(ns, opt, label='optimized budget')
plt.xlabel('n')
plt.ylabel('trace')
plt.title('Optimized obstruction budget')
plt.legend()
plt.tight_layout()
plt.savefig(out/'optimized_obstruction_budget_step69.png', dpi=160)
plt.close()

# 5. non-separating readout countermodel: psi_- = 0 for all x, yet off-fixed mass exists.
# Two points: fixed point f and off-fixed point o. readout zero on both.
sep_df = pd.DataFrame({
    'case': ['separating_readout', 'nonseparating_readout'],
    'off_fixed_mass': [0.0, 1.0],
    'trace_A': [0.0, 0.0],
    'status': ['confinement_valid', 'readout_failure']
})
sep_df.to_csv(out/'nonseparating_readout_countermodel_step69.csv', index=False)

print('Step 69 checks complete:', out)
