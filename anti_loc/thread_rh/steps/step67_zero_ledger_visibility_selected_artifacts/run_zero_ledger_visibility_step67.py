import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/anti_localization_step67_zero_ledger')
out.mkdir(parents=True, exist_ok=True)

# Fixed squeeze: fixed scalar A <= 1/n forces A=0; any positive A eventually violates
ns = np.arange(1, 501)
B = 1.0 / ns
fixed_A_positive = 0.05
passes_positive = fixed_A_positive <= B
fixed_df = pd.DataFrame({
    'n': ns,
    'B_n_trace': B,
    'positive_A_trace': fixed_A_positive,
    'positive_A_passes': passes_positive.astype(int),
    'zero_A_passes': np.ones_like(ns),
})
fixed_df.to_csv(out/'fixed_squeeze_status_step67.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot(ns, B, label='budget B_n=1/n')
plt.axhline(fixed_A_positive, linestyle='--', label='fixed A_Z=0.05')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('trace')
plt.title('Fixed ledger squeeze: positive A eventually violates shrinking budget')
plt.legend()
plt.tight_layout()
plt.savefig(out/'fixed_ledger_squeeze_step67.png', dpi=160)
plt.close()

# Exhaustive versus failed tail
n = ns
Bwin = 1.0/(n**2)
T_good = 1.0/(n**2)
T_bad = 0.1*np.ones_like(n, dtype=float)
total_good = Bwin + T_good
total_bad = Bwin + T_bad
exh_df = pd.DataFrame({'n': n, 'window_budget': Bwin, 'tail_good': T_good, 'tail_bad': T_bad, 'total_good': total_good, 'total_bad': total_bad})
exh_df.to_csv(out/'exhaustive_tail_status_step67.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot(n, total_good, label='exhaustive total B_n+T_n -> 0')
plt.plot(n, total_bad, label='failed tail B_n+T_n -> 0.1')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('trace budget')
plt.title('Exhaustive finite ledgers need vanishing tail')
plt.legend()
plt.tight_layout()
plt.savefig(out/'exhaustive_tail_step67.png', dpi=160)
plt.close()

# Moving ledger support-only: finite window has zero but completed A is fixed positive
moving_visible = np.zeros_like(n, dtype=float)
completed_tail_hidden = np.ones_like(n, dtype=float)
moving_df = pd.DataFrame({'n': n, 'moving_window_budget': moving_visible, 'hidden_completed_tail': completed_tail_hidden})
moving_df.to_csv(out/'moving_ledger_support_only_step67.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot(n, moving_visible+1e-12, label='moving window ledger budget ~0')
plt.plot(n, completed_tail_hidden, label='hidden completed mass')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('trace')
plt.title('Moving ledger can miss fixed off-locus mass')
plt.legend()
plt.tight_layout()
plt.savefig(out/'moving_ledger_support_only_step67.png', dpi=160)
plt.close()

# Optimized obstruction budget: a_n, b_n and (sqrt(a)+sqrt(b))^2
Lambda = n.astype(float)
a = 2.0/Lambda + 1.0/(n**1.5) # source+lambda budget
b = 1.0/(n**1.25) # EF defect
opt = (np.sqrt(a)+np.sqrt(b))**2
obs_df = pd.DataFrame({'n': n, 'a_n': a, 'b_n': b, 'optimized_trace_budget': opt})
obs_df.to_csv(out/'optimized_obstruction_budget_step67.csv', index=False)
plt.figure(figsize=(7,4))
plt.plot(n, a, label='a_n')
plt.plot(n, b, label='b_n')
plt.plot(n, opt, label='optimized (sqrt a + sqrt b)^2')
plt.yscale('log')
plt.xlabel('n')
plt.ylabel('trace budget')
plt.title('Optimized RH-style obstruction budget')
plt.legend()
plt.tight_layout()
plt.savefig(out/'optimized_obstruction_budget_step67.png', dpi=160)
plt.close()

# Fixed-locus readout separation example on scalar displacement d=Re(s)-1/2
# If sum w d^2 <= eps, mass above delta <= eps/delta^2
budgets = np.array([1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001])
deltas = [0.1, 0.2, 0.5]
rows = []
for eps in budgets:
    for delta in deltas:
        rows.append({'trace_A_bound': eps, 'delta': delta, 'mass_bound': eps/(delta**2)})
sep_df = pd.DataFrame(rows)
sep_df.to_csv(out/'separation_mass_bounds_step67.csv', index=False)

print('Step 67 checks/artifacts generated in', out)
