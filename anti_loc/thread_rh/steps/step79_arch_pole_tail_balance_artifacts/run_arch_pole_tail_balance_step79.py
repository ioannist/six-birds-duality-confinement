"""Sanity checks for Step 79 arch/pole/tail completion balance.
These are algebraic toy checks only, not Six Birds simulations and not zeta evidence.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OUT = Path('/mnt/data/rh_membrane_step79_arch_pole_tail')
OUT.mkdir(exist_ok=True, parents=True)

# Toy prime weights from n <= exp(L), using von Mangoldt, with smooth cutoff.
def von_mangoldt(n: int) -> float:
    # returns log p if n is a prime power, else 0
    import math
    # simple factorization
    x = n
    factors = []
    p = 2
    while p*p <= x:
        if x % p == 0:
            c = 0
            while x % p == 0:
                x //= p; c += 1
            factors.append((p,c))
        p += 1 if p == 2 else 2
    if x > 1:
        factors.append((x,1))
    if len(factors)==1:
        return math.log(factors[0][0])
    return 0.0

L = 6.0
ns = np.arange(2, int(np.floor(np.exp(L)))+1)
logs = np.log(ns)
lam = np.array([von_mangoldt(int(n)) for n in ns])
alpha = np.maximum(0.0, 1.0 - logs/L)**2
weights = lam/np.sqrt(ns)*alpha
mask = weights > 0
logs = logs[mask]
weights = weights[mask]
d_pr = 2*weights.sum()
xis = np.linspace(0, 30, 2000)
P_signed = -2*np.sum(weights[:,None]*np.cos(logs[:,None]*xis[None,:]), axis=0)
q_pr = np.sum(weights[:,None]*np.abs(np.exp(1j*logs[:,None]*xis[None,:])-1)**2, axis=0)
repair = P_signed + d_pr
prime_df = pd.DataFrame({'xi':xis,'signed_prime_symbol':P_signed,'positive_prime_symbol':q_pr,'signed_plus_diagonal':repair})
prime_df.to_csv(OUT/'prime_completion_symbol_step79.csv', index=False)

# Archimedean model kernel kappa(a)=1/(2 sinh(a/2)) with cutoffs; symbol integral numerical.
a = np.linspace(1e-4, 25, 40000)
kappa = 1/(2*np.sinh(a/2))
# q_infty symbol = 2 int kappa(a)(1-cos(a xi)) da
# trapezoid integration vectorized in chunks
psi_inf = []
for xi in xis:
    psi_inf.append(2*np.trapz(kappa*(1-np.cos(a*xi)), a))
psi_inf = np.array(psi_inf)
arch_df = pd.DataFrame({'xi':xis,'arch_model_symbol':psi_inf})
arch_df.to_csv(OUT/'arch_model_symbol_step79.csv', index=False)

# Frequency split toy: signed residual r(xi) = r0 on low, r1 on high with smooth transition.
# Determine low-mode pole payment needed for balance if arch+prime pay high.
r0 = d_pr + 3.0  # artificially larger than d_pr, so pole must pay 3 on low
r1 = 0.75*d_pr  # high residual less than diagonal repair
low_radius = 0.75
transition = 1/(1+np.exp(10*(xis-low_radius)))
r_sgn = r0*transition + r1*(1-transition)
# Completion balance with pole payment p and arch symbol q_inf + q_pr + d_pr - r_sgn
pole_payments = np.linspace(0, 5, 101)
mins=[]
for p in pole_payments:
    pole_symbol = p*transition
    B = d_pr + q_pr + psi_inf + pole_symbol - r_sgn
    mins.append(B.min())
bal_df = pd.DataFrame({'pole_payment':pole_payments,'min_balance_symbol':mins})
bal_df.to_csv(OUT/'frequency_split_balance_sweep_step79.csv', index=False)

# Required payment roughly to make min >=0
req = pole_payments[np.argmax(np.array(mins)>=0)] if np.any(np.array(mins)>=0) else np.nan
summary = pd.DataFrame([{
    'L':L,
    'num_prime_power_terms':len(weights),
    'sum_prime_weights':weights.sum(),
    'd_pr_diagonal_repair':d_pr,
    'min_signed_prime_symbol':P_signed.min(),
    'min_positive_prime_symbol':q_pr.min(),
    'arch_symbol_at_xi_0':psi_inf[0],
    'arch_symbol_at_xi_max':psi_inf[-1],
    'low_residual_r0':r0,
    'high_residual_r1':r1,
    'required_pole_payment_toy':req,
}])
summary.to_csv(OUT/'completion_balance_summary_step79.csv', index=False)

# Trace not balance: same trace but Loewner fails
trace_counter = pd.DataFrame([
    {'matrix':'A', 'eigenvalues':'[2,0]', 'trace':2, 'max_eig':2, 'status_vs_I':'fails Loewner <= I'},
    {'matrix':'I', 'eigenvalues':'[1,1]', 'trace':2, 'max_eig':1, 'status_vs_I':'budget'},
])
trace_counter.to_csv(OUT/'trace_not_balance_counterexample_step79.csv', index=False)

# Feature slot status table
slot_table = pd.DataFrame([
    {'slot':'prime-power','positive_feature_status':'positive after diagonal repair','matching_status':'signed prime term plus d_pr ||f||^2; diagonal must be licensed by completed carrier','main_gate':'weights positive; tail cutoff declared'},
    {'slot':'archimedean/gamma','positive_feature_status':'plausible positive difference kernel','matching_status':'exact gamma matching and renormalization not yet earned','main_gate':'positive kernel, form closability, low-mode complement'},
    {'slot':'pole/completion','positive_feature_status':'finite/low-mode feature','matching_status':'must handle pole/null modes and low-frequency diagonal','main_gate':'null-mode legality; finite-rank low-mode payment'},
    {'slot':'tail/support','positive_feature_status':'positive feature or explicit defect','matching_status':'finite windows need fixed/exhaustive ledger tail','main_gate':'tail trace -> 0 or explicit nonclaim'},
])
slot_table.to_csv(OUT/'arch_pole_tail_slot_status_step79.csv', index=False)

# Gate table
gates = pd.DataFrame([
    {'gate':'G1 prime diagonal repair','condition':'q_pr = P_pr + d_pr ||f||^2 with d_pr=2 sum w_a','failure_status':'signed_prime_only'},
    {'gate':'G2 archimedean positivity','condition':'gamma slot written as positive renormalized difference feature or defect','failure_status':'signed_gamma_defect'},
    {'gate':'G3 pole/null legality','condition':'pole/completion features pay declared low/null modes','failure_status':'fake_zero_budget'},
    {'gate':'G4 tail/support','condition':'omitted terms are positive features or vanishing fixed/exhaustive defects','failure_status':'moving_ledger_support_only'},
    {'gate':'G5 completion balance','condition':'B_L >= 0 on the completed anti-invariant core','failure_status':'balance_defect'},
    {'gate':'G6 core-to-full','condition':'closability and form-core extension','failure_status':'finite_core_only'},
])
gates.to_csv(OUT/'completion_balance_gate_table_step79.csv', index=False)

# theorem map
thms = pd.DataFrame([
    {'id':'T79.1','name':'Signed-to-positive completion transfer','depends_on':'Step 77, Step 78','status':'proved abstractly'},
    {'id':'T79.2','name':'Archimedean positivity as difference feature','depends_on':'positive kernel integrability','status':'proved conditional'},
    {'id':'T79.3','name':'Low-mode pole payment','depends_on':'finite-rank feature lower bound','status':'proved conditional'},
    {'id':'T79.4','name':'Frequency-split completion balance','depends_on':'low/high operator inequalities','status':'proved conditional'},
])
thms.to_csv(OUT/'theorem_map_step79.csv', index=False)

# Plots
plt.figure(figsize=(8,5))
plt.plot(xis, P_signed, label='signed prime')
plt.plot(xis, q_pr, label='positive shift feature')
plt.plot(xis, repair, '--', label='signed + diagonal repair')
plt.axhline(0,color='k',linewidth=0.7)
plt.xlabel('frequency xi')
plt.ylabel('symbol')
plt.title('Prime signed term vs positive feature')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'prime_completion_symbol_step79.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(xis, psi_inf)
plt.xlabel('frequency xi')
plt.ylabel('archimedean model symbol')
plt.title('Archimedean positive difference-kernel model')
plt.tight_layout()
plt.savefig(OUT/'arch_model_symbol_step79.png', dpi=180)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(pole_payments, mins)
plt.axhline(0,color='k',linewidth=0.7)
plt.xlabel('low-mode pole/completion payment')
plt.ylabel('min balance symbol')
plt.title('Toy frequency-split completion balance')
plt.tight_layout()
plt.savefig(OUT/'frequency_split_balance_sweep_step79.png', dpi=180)
plt.close()

print('Wrote Step 79 artifacts to', OUT)
