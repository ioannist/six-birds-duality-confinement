import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import math

out = Path('/mnt/data/rh_membrane_step79_arch_pole_tail')
out.mkdir(parents=True, exist_ok=True)

# Toy von Mangoldt for n <= exp(L)
def von_mangoldt(n):
    # log p if n is p^k, else 0
    x=n
    for p in range(2,int(math.sqrt(n))+1):
        if x%p==0:
            # n must be a power of p
            y=n
            while y%p==0:
                y//=p
            return math.log(p) if y==1 else 0.0
    return math.log(n) if n>=2 else 0.0

L = 8.0
N = int(math.exp(L))
# keep manageable: use n <= 700 for toy weights (support alpha kills high but exp(8)=2980)
Ntoy = 700
rows=[]
for n in range(2,Ntoy+1):
    lam = von_mangoldt(n)
    if lam>0:
        a=math.log(n)
        alpha=max(0.0,1-a/L)**2
        w=lam/math.sqrt(n)*alpha
        if w>0:
            rows.append((n,a,w))
prime_df=pd.DataFrame(rows, columns=['n','a_log_n','w'])
prime_df.to_csv(out/'prime_weights_step79.csv', index=False)

xis = np.linspace(0,40,2000)
a = prime_df['a_log_n'].to_numpy()
w = prime_df['w'].to_numpy()
W = w.sum()
# signed prime symbol for P_pr: -sum w(e^{iaxi}+e^{-iaxi}) = -2 sum w cos(a xi)
signed = np.array([-2*np.sum(w*np.cos(a*x)) for x in xis])
positive = np.array([2*np.sum(w*(1-np.cos(a*x))) for x in xis])
diag = 2*W
repaired = signed + diag

# Archimedean toy kernel. kappa(a)=1/(2 sinh(a/2)); truncated quadrature.
grid_a = np.linspace(1e-5, 30, 6000)
kappa = 1/(2*np.sinh(grid_a/2))
# To avoid infinite diagonal, only difference symbol is finite.
arch = []
for x in xis:
    arch.append(2*np.trapz(kappa*(1-np.cos(grid_a*x)), grid_a))
arch=np.array(arch)

# Pole/completion finite low-mode toy feature: Gaussian low-frequency bump + constant on exact zero mode impossible in continuum, modeled as bump.
# This is not a proof object; it illustrates finite-rank/local low-frequency repair.
for gamma in [0,1,3,5,10]:
    pass
sigma=1.5
pole5 = 5*np.exp(-(xis/sigma)**2)
# Tail toy: omitted positive feature as small high-frequency contribution.
tail = 0.2*(1-np.exp(-xis/5))
completed_toy = positive + arch + pole5 + tail

symbol_df = pd.DataFrame({
    'xi': xis,
    'prime_signed_symbol': signed,
    'prime_diagonal_repair': diag,
    'prime_repaired_symbol': repaired,
    'prime_positive_shift_symbol': positive,
    'archimedean_positive_difference_symbol_toy': arch,
    'pole_low_mode_feature_toy': pole5,
    'tail_positive_feature_toy': tail,
    'completed_positive_symbol_toy': completed_toy
})
symbol_df.to_csv(out/'arch_pole_tail_symbol_audit_step79.csv', index=False)

summary=[]
summary.append({'quantity':'prime_weight_sum', 'value': W, 'interpretation':'sum_a w_a for toy prime cutoff'})
summary.append({'quantity':'prime_diagonal_repair_d_pr', 'value': diag, 'interpretation':'2 sum_a w_a, sharp diagonal repair for signed prime autocorrelation'})
summary.append({'quantity':'min_signed_prime_symbol', 'value': float(signed.min()), 'interpretation':'signed prime slot can be negative'})
summary.append({'quantity':'min_repaired_minus_positive_abs_error', 'value': float(np.max(np.abs(repaired-positive))), 'interpretation':'repair identity signed + d_pr = positive shift symbol'})
summary.append({'quantity':'arch_symbol_at_zero', 'value': float(arch[0]), 'interpretation':'archimedean difference feature vanishes at legal zero'})
summary.append({'quantity':'arch_symbol_max_on_grid', 'value': float(arch.max()), 'interpretation':'toy archimedean difference feature is positive away from zero'})
summary.append({'quantity':'completed_toy_min', 'value': float(completed_toy.min()), 'interpretation':'toy completed positive symbol is nonnegative'})
pd.DataFrame(summary).to_csv(out/'arch_pole_tail_balance_summary_step79.csv', index=False)

# Sweep pole low-frequency bump amplitude and min of arch+pole relative to diagonal repair? demonstrate cannot pay global diagonal by decaying bump.
gammas=np.linspace(0,20,81)
sweep=[]
# Need dominate the prime diagonal repair by arch+pole+tail? On high frequencies arch helps; at xi=0 arch=tail=0, pole gamma.
for g in gammas:
    pole = g*np.exp(-(xis/sigma)**2)
    pay = arch + pole + tail
    min_gap = float(np.min(pay - diag))
    min_gap_low = float(np.min((pay - diag)[xis<1]))
    min_gap_high = float(np.min((pay - diag)[xis>5]))
    sweep.append({'pole_amplitude':g, 'min_pay_minus_diag_all':min_gap, 'min_pay_minus_diag_low_xi':min_gap_low, 'min_pay_minus_diag_high_xi':min_gap_high})
sweep_df=pd.DataFrame(sweep)
sweep_df.to_csv(out/'pole_amplitude_payment_sweep_step79.csv', index=False)

# Write plots
plt.figure(figsize=(8,5))
plt.plot(xis, signed, label='signed prime symbol')
plt.plot(xis, repaired, label='signed + diagonal repair')
plt.plot(xis, positive, linestyle='--', label='positive shift symbol')
plt.xlabel('frequency xi')
plt.ylabel('symbol value')
plt.title('Prime slot: signed autocorrelation vs positive shift feature')
plt.legend()
plt.tight_layout()
plt.savefig(out/'prime_signed_repaired_step79.png', dpi=160)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(xis, arch, label='archimedean difference symbol (toy)')
plt.plot(xis, pole5, label='pole/low-mode feature (toy)')
plt.plot(xis, tail, label='tail feature (toy)')
plt.xlabel('frequency xi')
plt.ylabel('symbol value')
plt.title('Candidate completion slots are positive but play different roles')
plt.legend()
plt.tight_layout()
plt.savefig(out/'arch_pole_tail_symbols_step79.png', dpi=160)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(sweep_df['pole_amplitude'], sweep_df['min_pay_minus_diag_all'], label='all frequencies')
plt.plot(sweep_df['pole_amplitude'], sweep_df['min_pay_minus_diag_low_xi'], label='low frequency')
plt.plot(sweep_df['pole_amplitude'], sweep_df['min_pay_minus_diag_high_xi'], label='high frequency')
plt.axhline(0, linestyle='--')
plt.xlabel('pole/low-mode amplitude')
plt.ylabel('min(completion payment - prime diagonal repair)')
plt.title('Finite low-mode payment does not automatically pay global diagonal')
plt.legend()
plt.tight_layout()
plt.savefig(out/'pole_payment_sweep_step79.png', dpi=160)
plt.close()

# Trace-not-balance toy counterexample
counter=pd.DataFrame([
    {'matrix':'A','a11':2,'a22':0,'trace':2,'max_eig':2,'passes_loewner_vs_I':False},
    {'matrix':'I','a11':1,'a22':1,'trace':2,'max_eig':1,'passes_loewner_vs_I':True}
])
counter.to_csv(out/'trace_not_balance_counterexample_step79.csv', index=False)

# Gate table
components = [
    {'slot':'prime-power','positive_feature':'yes after diagonal repair','earned':'partial','remaining_gate':'match repaired positive shift feature to completed explicit formula prime slot and account for diagonal d_pr'},
    {'slot':'archimedean/gamma','positive_feature':'candidate difference kernel','earned':'candidate','remaining_gate':'derive exact gamma kernel and prove renormalized positive form on core'},
    {'slot':'pole/completion','positive_feature':'finite-rank/moment/null-mode feature','earned':'candidate','remaining_gate':'prove it handles legal null/low modes and supplies correct pole terms'},
    {'slot':'tail/support','positive_feature':'positive omitted-shift features or explicit defect','earned':'open','remaining_gate':'prove fixed/exhaustive tail control'},
    {'slot':'completed balance','positive_feature':'sum of four slots','earned':'open','remaining_gate':'prove B_L >= 0 or quantify E_balance'}
]
pd.DataFrame(components).to_csv(out/'arch_pole_tail_gate_table_step79.csv', index=False)
