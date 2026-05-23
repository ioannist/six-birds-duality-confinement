import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('/mnt/data/rh_membrane_step86_lowfreq_resolution')
OUT.mkdir(parents=True, exist_ok=True)

# 1. Soft-zero no-gap: normalized Fourier packets on [0, eps] for symbol psi ~ xi^2.
# For a normalized packet uniformly supported in [-eps, eps], energy ~ eps^2/3.
eps_values = np.logspace(-4, -0.3, 80)
soft_rows = []
for eps in eps_values:
    energy = eps**2/3.0  # average xi^2 over [-eps, eps]
    soft_rows.append({'epsilon': eps, 'energy_upper_model': energy})
pd.DataFrame(soft_rows).to_csv(OUT/'soft_zero_no_gap_step86.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(eps_values, [r['energy_upper_model'] for r in soft_rows])
plt.xlabel('low-frequency packet width epsilon')
plt.ylabel('model carrier energy')
plt.title('Soft zero: no spectral gap after quotient')
plt.tight_layout()
plt.savefig(OUT/'soft_zero_no_gap_step86.png', dpi=200)
plt.close()

# 2. Cancellation capacity for psi=xi^2 near zero and ghat ~ |xi|^s.
cutoffs = np.logspace(-6, -1, 60)
s_values = [0.0, 0.25, 0.5, 0.55, 0.75, 1.0, 1.5]
rows=[]
# capacity over [cutoff,1] of xi^(2s)/xi^2 = xi^(2s-2)
for s in s_values:
    p = 2*s-2
    for c in cutoffs:
        if abs(p+1) < 1e-12:
            val = np.log(1/c)
        else:
            val = (1**(p+1)-c**(p+1))/(p+1)
        rows.append({'s':s, 'cutoff':c, 'capacity_integral_model':val})
pd.DataFrame(rows).to_csv(OUT/'cancellation_capacity_step86.csv', index=False)

plt.figure(figsize=(7,4.5))
for s in s_values:
    vals = [r['capacity_integral_model'] for r in rows if r['s']==s]
    plt.loglog(cutoffs, vals, label=f's={s}')
plt.gca().invert_xaxis()
plt.xlabel('low-frequency cutoff')
plt.ylabel(r'$\int_{cutoff}^1 \xi^{2s}/\xi^2\,d\xi$')
plt.title('Low-frequency cancellation threshold: s > 1/2')
plt.legend(ncol=2, fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'cancellation_capacity_step86.png', dpi=200)
plt.close()

# 3. Source coercivity model: psi_lambda = xi^2 + lambda on |xi|<delta, xi^2 elsewhere.
# capacity for constant low-frequency probe on [-delta,delta] normalized density: integral 1/(xi^2+lambda)
lambdas = np.logspace(-3, 4, 90)
delta = 0.1
source_rows=[]
# numerical integration grid
x = np.linspace(-delta, delta, 20001)
dx = x[1]-x[0]
for lam in lambdas:
    cap = np.trapz(1/(x*x + lam), x)
    # Compare asymptotics 2delta/lambda for large lambda and pi/sqrt(lambda) for small relative to delta^2
    source_rows.append({'lambda':lam, 'low_sector_capacity':cap, 'large_lambda_asymptotic':2*delta/lam})
pd.DataFrame(source_rows).to_csv(OUT/'source_coercivity_step86.csv', index=False)

plt.figure(figsize=(7,4.5))
plt.loglog(lambdas, [r['low_sector_capacity'] for r in source_rows], label='capacity with low-frequency source')
plt.loglog(lambdas, [r['large_lambda_asymptotic'] for r in source_rows], '--', label='2δ/λ asymptotic')
plt.xlabel('source strength lambda')
plt.ylabel('low-sector capacity')
plt.title('Full-sector source coercivity collapses low-frequency budget')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'source_coercivity_step86.png', dpi=200)
plt.close()

# 4. High/low split: outside delta, psi=xi^2 >= delta^2, high bound <= ||g_hi||^2/delta^2.
# model ghat=exp(-xi^2/(2sigma^2)), split norm and capacity for psi=xi^2.
sigmas = [0.05, 0.1, 0.2, 0.4]
deltas = np.logspace(-3, -0.3, 60)
xx = np.linspace(-5,5,200001)
rows=[]
for sigma in sigmas:
    g2 = np.exp(-xx**2/(sigma**2)) # |ghat|^2
    total_norm = np.trapz(g2, xx)
    for d in deltas:
        low_mask = np.abs(xx)<d
        high_mask = ~low_mask
        low_norm = np.trapz(g2[low_mask], xx[low_mask]) if low_mask.any() else 0
        high_norm = np.trapz(g2[high_mask], xx[high_mask]) if high_mask.any() else 0
        high_bound = high_norm/(d*d)
        rows.append({'sigma':sigma,'delta':d,'total_norm':total_norm,'low_norm':low_norm,'high_norm':high_norm,'high_capacity_bound':high_bound})
pd.DataFrame(rows).to_csv(OUT/'low_high_split_step86.csv', index=False)

plt.figure(figsize=(7,4.5))
for sigma in sigmas:
    vals = [r['high_capacity_bound'] for r in rows if r['sigma']==sigma]
    plt.loglog(deltas, vals, label=f'sigma={sigma}')
plt.xlabel('split delta')
plt.ylabel('high-frequency capacity bound')
plt.title('High/low split: high-frequency coercivity costs 1/delta^2')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(OUT/'low_high_split_step86.png', dpi=200)
plt.close()

# Write summary tables for resolution statuses.
status_rows = [
    {'record':'Q quotient/gap','mathematical_condition':'response space excludes |xi|<delta or carrier has psi>=gamma>0 on legal quotient','conclusion':'coercive membrane on quotient','warning':'quotienting exact kernel alone does not remove continuous soft zero'},
    {'record':'C cancellation','mathematical_condition':'probe/readout Fourier transform vanishes near zero: |ghat|=O(|xi|^s), s>r-1/2 in 1D when psi~|xi|^{2r}','conclusion':'finite low-frequency capacity','warning':'finite capacity is not budget collapse unless constants vanish or ladder squeezes fixed ledger'},
    {'record':'S source coercivity','mathematical_condition':'strict extension adds source with psi_lambda>=lambda theta^{-1} on whole low sector, lambda->infty','conclusion':'low-frequency budget collapse','warning':'must cover full anti-invariant low sector, not one direction'},
    {'record':'D defect/nonclaim','mathematical_condition':'uncovered low sector carried as explicit defect or excluded from claim','conclusion':'scoped statement only','warning':'does not prove full RH-style confinement'},
]
pd.DataFrame(status_rows).to_csv(OUT/'lowfreq_resolution_status_step86.csv', index=False)

print('wrote step86 artifacts to', OUT)
