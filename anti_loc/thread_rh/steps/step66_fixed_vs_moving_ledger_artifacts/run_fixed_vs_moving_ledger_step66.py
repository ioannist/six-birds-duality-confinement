import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path('/mnt/data/anti_localization_step66_fixed_ledger')
out.mkdir(parents=True, exist_ok=True)

N = 80
n = np.arange(1, N+1)

# Fixed squeeze: a fixed nonzero ledger A=a cannot be bounded by B_n=1/n forever.
a_fixed = 0.1
B_fixed = 1.0 / n
valid_fixed = B_fixed >= a_fixed
fixed_df = pd.DataFrame({
    'n': n,
    'fixed_nonzero_ledger_trace': a_fixed,
    'budget_trace_1_over_n': B_fixed,
    'certificate_valid_for_nonzero_A': valid_fixed,
})
fixed_df.to_csv(out/'fixed_squeeze_countercheck_step66.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.plot(n, B_fixed, label=r'budget trace $1/n$')
plt.axhline(a_fixed, linestyle='--', label='fixed nonzero trace(A)=0.1')
plt.xlabel('stage n')
plt.ylabel('trace')
plt.title('Fixed ledger: a nonzero object cannot be squeezed forever')
plt.legend()
plt.tight_layout()
plt.savefig(out/'fixed_squeeze_countercheck_step66.png', dpi=180)
plt.close()

# Infinite fixed squeeze allowed: A=0 can be bounded by shrinking budgets.
zero_df = pd.DataFrame({
    'n': n,
    'fixed_zero_ledger_trace': np.zeros_like(n, dtype=float),
    'budget_trace_1_over_n': B_fixed,
    'certificate_valid': np.ones_like(n, dtype=bool),
})
zero_df.to_csv(out/'fixed_zero_squeeze_step66.csv', index=False)

# Moving-ledger failure: each stage sees coordinate n with tiny mass 2^-n, but completed trace is 1.
B_move = 2.0 ** (-n)
completed_trace = np.ones_like(n, dtype=float)
partial_seen_trace = B_move
moving_df = pd.DataFrame({
    'n': n,
    'moving_stage_budget_trace_2_minus_n': B_move,
    'moving_stage_visible_trace': partial_seen_trace,
    'hidden_completed_ledger_trace': completed_trace,
})
moving_df.to_csv(out/'moving_ledger_tail_failure_step66.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.semilogy(n, B_move, label=r'moving visible budget $2^{-n}$')
plt.axhline(1.0, linestyle='--', label='hidden completed trace = 1')
plt.xlabel('stage n')
plt.ylabel('trace (log scale)')
plt.title('Moving ledger: shrinking visible slices do not squeeze a completed ledger')
plt.legend()
plt.tight_layout()
plt.savefig(out/'moving_ledger_tail_failure_step66.png', dpi=180)
plt.close()

# Exhaustive ledger success/failure budget model.
# Good case: visible bound + tail -> 0.
B_good = 1.0 / (n**2)
T_good = 1.0 / (n**2)
total_good = B_good + T_good
# Bad tail: visible bound -> 0, tail remains 0.2.
T_bad = 0.2 * np.ones_like(n, dtype=float)
total_bad = B_good + T_bad
exh_df = pd.DataFrame({
    'n': n,
    'visible_budget_good': B_good,
    'tail_good': T_good,
    'total_good': total_good,
    'visible_budget_bad_tail': B_good,
    'tail_bad': T_bad,
    'total_bad_tail': total_bad,
})
exh_df.to_csv(out/'exhaustive_vs_failed_tail_step66.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.semilogy(n, total_good, label='exhaustive total budget $1/n^2+1/n^2$')
plt.semilogy(n, total_bad, label='failed tail total $1/n^2+0.2$')
plt.xlabel('stage n')
plt.ylabel('trace budget (log scale)')
plt.title('Exhaustive squeeze requires visible budget and tail to vanish')
plt.legend()
plt.tight_layout()
plt.savefig(out/'exhaustive_vs_failed_tail_step66.png', dpi=180)
plt.close()

# Optimized obstruction budget (sqrt(a)+sqrt(b))^2.
Lambda = n.astype(float)
EF = 1.0 / (n**2)
Esrc = 1.0 / (n**1.5)
Theta_trace = 1.0
a = Theta_trace / Lambda + Esrc
b = EF
opt = (np.sqrt(a)+np.sqrt(b))**2
# Nonzero EF tail counterexample
EF_bad = 0.05*np.ones_like(n, dtype=float)
opt_bad = (np.sqrt(a)+np.sqrt(EF_bad))**2
obs_df = pd.DataFrame({
    'n': n,
    'Lambda': Lambda,
    'a_source_trace': a,
    'b_EF_trace': b,
    'optimized_budget_trace': opt,
    'b_EF_bad_trace': EF_bad,
    'optimized_budget_bad_EF_tail': opt_bad,
})
obs_df.to_csv(out/'optimized_obstruction_budget_step66.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(n, opt, label='optimized obstruction, vanishing EF/source')
plt.loglog(n, opt_bad, label='optimized obstruction, nonzero EF tail')
plt.xlabel('stage n')
plt.ylabel('optimized trace obstruction')
plt.title('Exact confinement needs all obstruction terms to vanish')
plt.legend()
plt.tight_layout()
plt.savefig(out/'optimized_obstruction_budget_step66.png', dpi=180)
plt.close()

# Status table
status_rows = [
    {'status':'finite_completion','sufficient_for_exact_confinement':True,'required_record':'finite stage proves A_Z=0 on completed ledger'},
    {'status':'fixed_ledger','sufficient_for_exact_confinement':True,'required_record':'same A_Z dominated by vanishing budgets'},
    {'status':'exhaustive_ledger','sufficient_for_exact_confinement':True,'required_record':'partial ledgers plus vanishing tail dominate A_Z'},
    {'status':'moving_ledger_support_only','sufficient_for_exact_confinement':False,'required_record':'missing tail/exhaustivity bridge'},
    {'status':'failed_tail','sufficient_for_exact_confinement':False,'required_record':'tail budget does not vanish'},
    {'status':'failed_visibility','sufficient_for_exact_confinement':False,'required_record':'zero readout fails to separate fixed locus'},
    {'status':'failed_budget_collapse','sufficient_for_exact_confinement':False,'required_record':'EF/source/coercivity defects do not vanish'},
]
pd.DataFrame(status_rows).to_csv(out/'ledger_status_table_step66.csv', index=False)

# Gate table
rows = [
    {'gate':'completed zero ledger', 'question':'Is A_Z a fixed completed object rather than a moving truncation?', 'failure_status':'moving_ledger_support_only'},
    {'gate':'explicit-formula domination', 'question':'Does each budget dominate the same ledger or an exhaustive subledger?', 'failure_status':'failed_domination'},
    {'gate':'tail/exhaustivity', 'question':'Do omitted zero-side directions have vanishing tail budget?', 'failure_status':'failed_tail'},
    {'gate':'budget collapse', 'question':'Do optimized obstruction traces tend to zero?', 'failure_status':'failed_budget_collapse'},
    {'gate':'zero visibility', 'question':'Does zero-side readout separate the anti-linear fixed locus?', 'failure_status':'failed_visibility'},
]
pd.DataFrame(rows).to_csv(out/'fixed_moving_gate_table_step66.csv', index=False)

print('Step 66 checks written to', out)
