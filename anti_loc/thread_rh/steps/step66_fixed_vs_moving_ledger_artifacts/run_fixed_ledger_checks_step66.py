import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/anti_localization_step66_fixed_ledger')
out.mkdir(parents=True, exist_ok=True)

# 1. Fixed squeeze: A fixed scalar A <= 1/n for all n forces A=0; demonstrate shrinking bound.
N = np.arange(1, 501)
B_fixed = 1.0 / N
fixed_df = pd.DataFrame({'n': N, 'B_n_trace': B_fixed, 'fixed_A_must_be_leq': B_fixed})
fixed_df.to_csv(out/'fixed_squeeze_sequence_step66.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(N, B_fixed)
plt.xlabel('stage n')
plt.ylabel('budget trace B_n')
plt.title('Fixed-ledger squeeze: budget tends to zero')
plt.tight_layout()
plt.savefig(out/'fixed_ledger_squeeze_step66.png', dpi=160)
plt.close()

# 2. Exhaustive ledger: B_n + T_n -> 0
T_tail = 1.0 / np.sqrt(N)
B_exh = 1.0 / N**2
exh_df = pd.DataFrame({'n': N, 'B_n_trace': B_exh, 'T_n_trace': T_tail, 'B_plus_T': B_exh+T_tail})
exh_df.to_csv(out/'exhaustive_ledger_sequence_step66.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(N, B_exh, label='visible budget B_n')
plt.plot(N, T_tail, label='tail T_n')
plt.plot(N, B_exh+T_tail, label='B_n + T_n')
plt.xlabel('stage n')
plt.ylabel('trace allowance')
plt.title('Exhaustive-ledger squeeze requires visible budget + tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'exhaustive_ledger_squeeze_step66.png', dpi=160)
plt.close()

# 3. Moving ledger failure: squeeze first n entries but fixed tail remains at index n+1 or invisible.
# Here total hidden mass remains 1 even though visible stage budget is 1/n.
hidden_mass = np.ones_like(N, dtype=float)
visible_budget = 1.0 / N
moving_df = pd.DataFrame({'n': N, 'visible_B_n_trace': visible_budget, 'hidden_completed_tail_mass': hidden_mass})
moving_df.to_csv(out/'moving_ledger_tail_failure_step66.csv', index=False)
plt.figure(figsize=(6,4))
plt.plot(N, visible_budget, label='moving visible budget')
plt.plot(N, hidden_mass, label='hidden completed mass')
plt.xlabel('stage n')
plt.ylabel('trace')
plt.title('Moving-ledger failure: visible squeeze misses completed tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'moving_ledger_tail_failure_step66.png', dpi=160)
plt.close()

# 4. Optimized obstruction budget from Step 65 formula.
Lambda = N.astype(float)
a = 1.0 / Lambda
b = 1.0 / (N**1.5)
opt = (np.sqrt(a)+np.sqrt(b))**2
budget_df = pd.DataFrame({'n': N, 'a_trace': a, 'b_trace': b, 'optimized_trace_budget': opt})
budget_df.to_csv(out/'optimized_obstruction_budget_step66.csv', index=False)
plt.figure(figsize=(6,4))
plt.loglog(N, a, label='a_n = Lambda^{-1} term')
plt.loglog(N, b, label='b_n = EF defect term')
plt.loglog(N, opt, label='optimized obstruction')
plt.xlabel('stage n')
plt.ylabel('trace budget')
plt.title('Optimized obstruction budget tends to zero')
plt.legend()
plt.tight_layout()
plt.savefig(out/'optimized_obstruction_budget_step66.png', dpi=160)
plt.close()

# 5. Summary table
summary = pd.DataFrame([
    {'case':'fixed_ledger_squeeze','visible_budget_at_500':B_fixed[-1], 'tail_or_hidden_mass':0.0, 'accepted_exact_confinement':True},
    {'case':'exhaustive_ledger_squeeze','visible_budget_at_500':B_exh[-1], 'tail_or_hidden_mass':T_tail[-1], 'accepted_exact_confinement':'yes in limit'},
    {'case':'moving_ledger_support_only','visible_budget_at_500':visible_budget[-1], 'tail_or_hidden_mass':hidden_mass[-1], 'accepted_exact_confinement':False},
])
summary.to_csv(out/'step66_check_summary.csv', index=False)
print(summary)
