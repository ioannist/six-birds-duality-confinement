"""Step 66 sanity checks for fixed vs moving zero-ledger criteria.
These are algebra/ledger illustrations only, not Six Birds simulations.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/anti_localization_step66_fixed_ledger')
OUT.mkdir(parents=True, exist_ok=True)

# Fixed squeeze: A <= 1/n for all n => A must be 0; finite illustration uses a hidden A value.
ns = np.arange(1, 501)
B = 1.0/ns
A_zero = np.zeros_like(B)
A_nonzero = 0.02*np.ones_like(B)
fixed = pd.DataFrame({'n': ns, 'B_n_trace': B, 'A_zero_trace': A_zero, 'A_nonzero_trace': A_nonzero, 'nonzero_violates_after_n': A_nonzero > B})
fixed.to_csv(OUT/'fixed_squeeze_checks_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(ns, B, label='trace bound B_n = 1/n')
plt.plot(ns, A_nonzero, linestyle='--', label='hypothetical fixed A trace = 0.02')
plt.xlabel('n')
plt.ylabel('trace')
plt.yscale('log')
plt.title('Fixed ledger squeeze: any positive fixed A eventually violates B_n')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'fixed_ledger_squeeze_step66.png', dpi=200)
plt.close()

# Moving ledger failure: visible A_n=0, B_n=0, hidden tail=1.
mov = pd.DataFrame({'n': ns, 'visible_A_n_trace': np.zeros_like(ns, dtype=float), 'B_n_trace': np.zeros_like(ns, dtype=float), 'hidden_tail_T_n_trace': np.ones_like(ns, dtype=float), 'completed_A_trace': np.ones_like(ns, dtype=float)})
mov.to_csv(OUT/'moving_ledger_failure_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(ns, np.zeros_like(ns), label='visible bound B_n = 0')
plt.plot(ns, np.ones_like(ns), label='hidden completed A_Z = 1')
plt.xlabel('n')
plt.ylabel('trace')
plt.title('Moving ledger failure: visible ledgers squeeze while hidden tail remains')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'moving_ledger_failure_step66.png', dpi=200)
plt.close()

# Exhaustive ledger examples: visible bound 1/n and tail 1/n^2 succeeds; tail non-vanishing fails.
B_vis = 1.0/ns
T_success = 1.0/(ns**2)
T_fail = 0.1*np.ones_like(ns, dtype=float)
exh = pd.DataFrame({'n': ns, 'B_visible_trace': B_vis, 'T_success_trace': T_success, 'total_success_trace': B_vis+T_success, 'T_fail_trace': T_fail, 'total_fail_trace': B_vis+T_fail})
exh.to_csv(OUT/'exhaustive_ledger_tail_checks_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(ns, B_vis+T_success, label='vanishing visible + tail')
plt.plot(ns, B_vis+T_fail, label='nonvanishing tail')
plt.xlabel('n')
plt.ylabel('total trace budget')
plt.yscale('log')
plt.title('Exhaustive ledger: exact squeeze requires vanishing tail')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'exhaustive_ledger_tail_step66.png', dpi=200)
plt.close()

# Optimized obstruction budget: a_n = 1/Lambda_n + E_src, b_n=E_EF, optimized trace=(sqrt(a)+sqrt(b))^2.
Lambda = ns.astype(float)
a_good = 1/Lambda + 1/(ns**2)
b_good = 1/(ns**2)
opt_good = (np.sqrt(a_good)+np.sqrt(b_good))**2
a_bad = 1/Lambda + 0.05
b_bad = 1/(ns**2)
opt_bad = (np.sqrt(a_bad)+np.sqrt(b_bad))**2
obs = pd.DataFrame({'n': ns, 'Lambda_n': Lambda, 'a_good': a_good, 'b_good': b_good, 'optimized_good': opt_good, 'a_nonvanishing_source': a_bad, 'b_good2': b_bad, 'optimized_with_source_defect': opt_bad})
obs.to_csv(OUT/'optimized_obstruction_budget_step66.csv', index=False)
plt.figure(figsize=(7,4.5))
plt.plot(ns, opt_good, label='vanishing defects')
plt.plot(ns, opt_bad, label='nonvanishing source defect')
plt.xlabel('n')
plt.ylabel('optimized trace budget')
plt.yscale('log')
plt.title('Root-composite obstruction budget: exact squeeze needs all terms vanish')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'optimized_budget_step66.png', dpi=200)
plt.close()

# Status table
status = pd.DataFrame([
    {'status':'fixed_ledger','has_completed_AZ':True,'has_tail_record':False,'bounds_same_object':True,'can_prove_exact_if_budget_vanishes':True,'note':'one fixed zero-side displacement matrix is squeezed at every stage'},
    {'status':'exhaustive_ledger','has_completed_AZ':True,'has_tail_record':True,'bounds_same_object':True,'can_prove_exact_if_budget_vanishes':True,'note':'visible ledgers plus vanishing tail exhaust completed zero ledger'},
    {'status':'moving_ledger_support_only','has_completed_AZ':False,'has_tail_record':False,'bounds_same_object':False,'can_prove_exact_if_budget_vanishes':False,'note':'stagewise ledgers can vanish while hidden completed tail remains'},
    {'status':'finite_completion','has_completed_AZ':True,'has_tail_record':'n/a','bounds_same_object':True,'can_prove_exact_if_budget_vanishes':True,'note':'finite stage closes ledger directly'},
    {'status':'tail_defect','has_completed_AZ':True,'has_tail_record':True,'bounds_same_object':True,'can_prove_exact_if_budget_vanishes':False,'note':'nonvanishing tail gives quantitative allowance only'},
])
status.to_csv(OUT/'fixed_moving_ledger_status_table_step66.csv', index=False)
